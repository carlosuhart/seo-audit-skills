#!/usr/bin/env python3
"""
Purpose: aplica reemplazos exactos en post_content con respaldo y control md5, sin mover la fecha de modificación.
Input: <dir>/pairs.json = {post_id: [[desde, hasta], ...]} calculado sobre los respaldos de <dir>/backup/.
Output: <dir>/done.json con ok/err por post.
Usage:
  python scripts/wp_apply.py collect <dir> --ids 12,34,56   # respaldo del content.raw actual + md5
  python scripts/wp_apply.py plan <dir>                     # prueba en seco: posts que cambian
  python scripts/wp_apply.py apply <dir> [--batch 10]       # escribe vía snippet temporal y lo borra
Seguridad: el servidor rechaza el post si su md5 actual no coincide con el del respaldo, y el md5
resultante debe coincidir con el calculado en local.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time

from wp_common import APPLY_PHP, SITE, api_client, snippet_create, snippet_delete


def md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def collect(d: str, ids: list[int], pause: float = 1.0) -> None:
    """Respalda content.raw de cada ID. Reanudable (salta lo ya respaldado) y con reintentos ante cortes."""
    import httpx
    api = api_client()
    os.makedirs(f'{d}/backup', exist_ok=True)
    items_f = f'{d}/items.json'
    items = json.load(open(items_f, encoding='utf-8')) if os.path.exists(items_f) else {}
    for n_, i in enumerate(ids, 1):
        if str(i) in items:
            continue
        r = None
        for attempt in range(5):
            time.sleep(pause * (1 if attempt == 0 else 4 ** attempt))
            try:
                r = api.get(f'{SITE}/wp-json/wp/v2/posts/{i}', params={'context': 'edit', '_fields': 'id,link,content'})
                if r.status_code != 200:
                    r = api.get(f'{SITE}/wp-json/wp/v2/pages/{i}', params={'context': 'edit', '_fields': 'id,link,content'})
                break
            except httpx.HTTPError as e:
                print('reintento', i, type(e).__name__, flush=True); api = api_client()
        if r is None or r.status_code != 200:
            print('no encontrado', i, flush=True); continue
        raw = r.json()['content']['raw']
        items[str(i)] = {'link': r.json()['link'], 'md5': md5(raw)}
        open(f'{d}/backup/{i}.html', 'w', encoding='utf-8', newline='').write(raw)
        if n_ % 25 == 0:
            json.dump(items, open(items_f, 'w', encoding='utf-8'), indent=1); print(n_, '/', len(ids), flush=True)
    json.dump(items, open(items_f, 'w', encoding='utf-8'), indent=1)
    print('respaldados', len(items))


def build(d: str) -> tuple[list[dict], dict]:
    items = json.load(open(f'{d}/items.json', encoding='utf-8'))
    pairs = json.load(open(f'{d}/pairs.json', encoding='utf-8'))
    todo, expect = [], {}
    for pid, pr in pairs.items():
        raw = open(f'{d}/backup/{pid}.html', encoding='utf-8', newline='').read()
        new = raw
        for a, b in pr:
            new = new.replace(a, b)
        if new != raw:
            expect[pid] = md5(new)
            todo.append({'id': int(pid), 'md5': items[pid]['md5'], 'from': [a for a, _ in pr], 'to': [b for _, b in pr]})
    return todo, expect


def apply(d: str, batch: int) -> None:
    todo, expect = build(d)
    print('por escribir', len(todo), flush=True)
    api = api_client(); done = {}
    sid = snippet_create(api, APPLY_PHP)
    try:
        for k in range(0, len(todo), batch):
            chunk = todo[k:k + batch]
            res = api.post(f'{SITE}/wp-json/wphe-diag/v1/apply', json={'batch': chunk}).json()
            for b in chunk:
                pid = str(b['id']); j = res.get(pid, {})
                done[pid] = {'ok': bool(j.get('ok') and j.get('md5') == expect[pid]), 'err': j.get('err')}
            print(k + len(chunk), '/', len(todo), flush=True)
            time.sleep(5)
    finally:
        json.dump(done, open(f'{d}/done.json', 'w', encoding='utf-8'), indent=1)
        snippet_delete(api, sid)
    print('ok', sum(v['ok'] for v in done.values()), 'errores', {k: v for k, v in done.items() if not v['ok']})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['collect', 'plan', 'apply'])
    ap.add_argument('dir')
    ap.add_argument('--ids', default='')
    ap.add_argument('--batch', type=int, default=10)
    ap.add_argument('--pause', type=float, default=1.0)
    a = ap.parse_args()
    if a.cmd == 'collect':
        collect(a.dir, [int(x) for x in a.ids.split(',') if x], a.pause)
    elif a.cmd == 'plan':
        todo, _ = build(a.dir)
        print('posts que cambian', len(todo), [t['id'] for t in todo][:50])
    else:
        apply(a.dir, a.batch)


if __name__ == '__main__':
    main()
