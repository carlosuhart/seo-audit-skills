#!/usr/bin/env python3
"""
Purpose: volcado completo de posts y páginas publicados, por idioma, con contenido crudo (context=edit).
Input: variables de entorno de wp_common.py; --langs con los códigos de idioma de WPML/Polylang.
Output: JSON con una lista de documentos {id, _type, _lang, link, slug, title, excerpt, content, ...}.
Usage: python scripts/wp_dump.py --out audit/dump.json --langs es,en,pt-br,fr [--pause 1.5]
Notas: secuencial a propósito (no cargar el origen en paralelo). lang=all no devuelve traducciones en WPML.
"""
from __future__ import annotations

import argparse
import json
import time

import httpx

from wp_common import SITE, api_client

FIELDS = 'id,date,modified,slug,status,link,title,content,excerpt,author,featured_media,parent,template'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--langs', default='', help='es,en,... (vacío = sin parámetro lang)')
    ap.add_argument('--pause', type=float, default=1.5)
    a = ap.parse_args()
    api = api_client()
    langs = [x for x in a.langs.split(',') if x] or [None]
    out: list[dict] = []
    for typ in ('posts', 'pages'):
        fields = FIELDS + (',categories,tags' if typ == 'posts' else '')
        for lang in langs:
            page = 1
            while True:
                params = {'per_page': 50, 'page': page, 'status': 'publish', 'context': 'edit', '_fields': fields}
                if lang:
                    params['lang'] = lang
                r = None
                for _ in range(4):
                    try:
                        r = api.get(f'{SITE}/wp-json/wp/v2/{typ}', params=params); break
                    except httpx.HTTPError:
                        time.sleep(10)
                if r is None or r.status_code != 200 or not r.json():
                    break
                data = r.json()
                for x in data:
                    x.update(_type=typ, _lang=lang or '', content=x['content']['raw'],
                             title=x['title']['raw'], excerpt=x.get('excerpt', {}).get('raw', ''))
                out.extend(data)
                print(typ, lang, 'página', page, 'acumulado', len(out), flush=True)
                if page >= int(r.headers.get('x-wp-totalpages', 1)):
                    break
                page += 1
                time.sleep(a.pause)
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('documentos', len(out))


if __name__ == '__main__':
    main()
