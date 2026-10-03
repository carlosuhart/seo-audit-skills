#!/usr/bin/env python3
"""
Purpose: escaneo offline de un volcado (wp_dump.py) en busca de los patrones del catálogo que no requieren red.
Input: dump.json; --site; opcional --sitemaps (JSON {url: {lang: url}} con los grupos hreflang del sitemap)
       y --registered (lista de shortcodes registrados, separados por coma, para C1).
Output: findings.json {patrón: [casos]} y un resumen por consola.
Usage: python scripts/wp_scan.py audit/dump.json --site https://www.ejemplo.com [--sitemaps audit/tr.json]
       [--old-prefix es] [--registered caption,toc,the_ad] --out audit/findings.json
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import re

BS = chr(92)
STOP = {
    'es': {'los', 'las', 'del', 'según', 'también', 'pero', 'porque', 'cuando', 'muy', 'sobre'},
    'en': {'the', 'and', 'with', 'which', 'from', 'this', 'that', 'are', 'was', 'have'},
    'pt-br': {'não', 'uma', 'dos', 'das', 'com', 'também', 'mais', 'você', 'pela', 'pelo'},
    'fr': {'les', 'des', 'est', 'une', 'dans', 'pour', 'avec', 'qui', 'sont', 'aux'},
}
AI_MARK = re.compile(r'data-(?:turn-id|message-author-role|writing-block|free-thinking|testid="conversation)|text-token-text|markdown prose')
OBFUSC = re.compile(r'createElement|appendChild|eval\(|atob\(|fromCharCode|document\.write')
HREF = re.compile(r'''\bhref\s*=\s*["']([^"']+)["']''', re.I)


def norm(u: str, site: str) -> str:
    u = html.unescape(u).strip()
    if u.startswith('/') and not u.startswith('//'):
        u = site + u
    host = re.escape(re.sub(r'^https?://(www\.)?', '', site))
    u = re.sub(r'^https?://(?:www\.)?' + host, site, u, flags=re.I)
    u = re.sub(r'#.*$', '', u)
    return u if ('?' in u or u.endswith('/')) else u + '/'


def lang_of(u: str, site: str, langs: list[str], default: str) -> str:
    for lg in langs:
        if lg != default and u.startswith(f'{site}/{lg}/'):
            return lg
    return default


def detect_lang(text: str, declared: str) -> str | None:
    """Idioma dominante por palabras vacías exclusivas; solo se informa si supera al declarado con margen 1,5x
    (listas de nombres propios, embeds o citas en otro idioma dan falsos positivos sin ese margen)."""
    w = re.findall(r'[a-zà-ÿãõçé]+', text.lower())
    if len(w) < 80:
        return None
    sc = {lg: sum(1 for x in w if x in s) for lg, s in STOP.items()}
    top = max(sc, key=sc.get)
    if top != declared and sc[top] >= 1.5 * max(sc.get(declared, 0), 1) and sc[top] >= 8:
        return top
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('dump')
    ap.add_argument('--site', required=True)
    ap.add_argument('--sitemaps')
    ap.add_argument('--old-prefix', default='es', help='prefijo de idioma retirado (L1)')
    ap.add_argument('--default-lang', default='es')
    ap.add_argument('--registered', default='', help='shortcodes registrados (C1)')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    site = a.site.rstrip('/')
    D = json.load(open(a.dump, encoding='utf-8'))
    langs = sorted({d['_lang'] for d in D if d['_lang']}) or [a.default_lang]
    tr = json.load(open(a.sitemaps, encoding='utf-8')) if a.sitemaps else {}
    pub = {norm(d['link'], site): d for d in D}
    reg = {x for x in a.registered.split(',') if x}
    F: dict[str, list] = collections.defaultdict(list)
    sc_count: collections.Counter = collections.Counter()

    for d in D:
        c = d.get('content') or ''
        pid, lg = d['id'], d['_lang'] or a.default_lang
        for u in HREF.findall(c):
            if not re.match(r'(https?:)?//(www\.)?' + re.escape(re.sub(r'^https?://(www\.)?', '', site)), u, re.I) and not u.startswith('/'):
                if u.startswith('http://'):
                    F['L5_http_externo'].append((pid, u))
                continue
            if u.startswith('//'):
                continue
            n = norm(u, site)
            path = n[len(site):]
            if '/wp-content/' in path:
                continue
            if re.match(rf'/{a.old_prefix}(/|$)', path):
                F['L1_prefijo_retirado'].append((pid, u)); continue
            if re.search(r'[?&](p|page_id)=\d+', path):
                F['L4_param_id'].append((pid, u)); continue
            if re.search(r'/\d{4}/\d{2}/', path):
                F['L5_enlace_con_fecha'].append((pid, u))
            if u.startswith('/'):
                F['L5_relativo'].append((pid, u))
            if n in pub:
                tl = lang_of(n, site, langs, a.default_lang)
                if tl != lg and tr.get(n, {}).get(lg):
                    F['L2_cruzado_con_traduccion'].append((pid, lg, n, tr[n][lg]))
                if pub[n]['id'] == pid:
                    F['L5_autoenlace'].append((pid, u))
            elif not re.search(r'/(tag|category|author|autor|page|feed)/|\.(xml|txt|pdf|jpe?g|png|webp)/?$', path) and path != '/':
                F['L3_destino_desconocido'].append((pid, lg, n))
        body = re.sub(r'<script.*?</script>', ' ', c, flags=re.S | re.I)
        for name in re.findall(r'\[([a-z_][\w-]{2,})(?=[\s\]])', body):
            sc_count[name] += 1
            if reg and name not in reg:
                F['C1_shortcode_no_registrado'].append((pid, name))
        text = html.unescape(re.sub(r'<script.*?</script>|<[^>]+>|\[[^\]]*\]', ' ', c, flags=re.S))
        dl = detect_lang(text, lg)
        if dl:
            F['C3_cuerpo_en_otro_idioma'].append((pid, lg, dl, d['link']))
        if AI_MARK.search(c):
            F['C4_residuo_ui_ia'].append(pid)
        if c.count(BS + 'n') >= 5:
            F['C5_saltos_escapados'].append((pid, c.count(BS + 'n')))
        for m in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', c, re.S):
            try:
                json.loads(m.group(1))
            except ValueError as e:
                F['C6_jsonld_invalido'].append((pid, str(e)[:60]))
        for m in re.finditer(r'<script\b(?![^>]*ld\+json)[^>]*>(.*?)</script>', c, re.S | re.I):
            if OBFUSC.search(m.group(1)):
                F['C7_script_dinamico_revisar'].append((pid, re.sub(r'\s+', ' ', m.group(1))[:160]))
        for img in re.findall(r'<img\b[^>]*>', c):
            al = re.search(r'\balt="([^"]*)"', img)
            if not al or not al.group(1).strip():
                F['B_img_sin_alt'].append(pid)
        if d['_type'] == 'posts' and not d.get('featured_media'):
            F['B_sin_imagen_destacada'].append((pid, lg))

    titles = collections.defaultdict(list)
    for d in D:
        titles[(d['_lang'], d['title'].strip().lower())].append(d['id'])
    F['H1_titulo_duplicado'] = [v for v in titles.values() if len(v) > 1]
    if tr:
        F['H1_sitemap_fuera_del_volcado'] = sorted(set(tr) - set(pub))

    json.dump({k: v for k, v in F.items()}, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k in sorted(F):
        print(f'{k}: {len(F[k])}')
    print('shortcodes más usados:', sc_count.most_common(15))


if __name__ == '__main__':
    main()
