#!/usr/bin/env python3
"""
Purpose: quita un shortcode de un plugin desinstalado (p. ej. [amazon box="..."]) sin dejar textos pegados ni
         huecos, y retira los encabezados que solo existían para ese bloque. Genera pairs.json para wp_apply.py.
Input: <dir>/backup/<id>.html (respaldos de wp_apply.py collect), --tag nombre del shortcode.
Output: <dir>/pairs.json {post_id: [[contenido_actual, contenido_nuevo]]} y un informe por consola.
Usage:
  python scripts/strip_shortcode.py plan <dir> --tag amazon [--keep-after the_ad,the_ad_group] [--show 6]
Reglas:
  - el tramo (shortcode o grupo de shortcodes seguidos, con el espacio que lo rodea) se sustituye por un único
    salto de párrafo en el estilo del post (CRLF o LF); vacío al inicio o al final; un espacio si iba en línea;
    "\\n\\n" literal si el post guarda los saltos escapados.
  - tramos contiguos o solapados se fusionan (un solo separador).
  - un encabezado justo antes del tramo se quita si después solo viene otro encabezado de nivel igual o superior,
    shortcodes de --keep-after o el final del contenido (se repite hacia atrás para encabezados anidados).
  - cubre shortcodes sin ] de cierre (terminan en salto de línea).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re

BS = chr(92)


def patterns(tag: str, keep_after: list[str]):
    ws = r'(?:[ \t]|\r?\n|' + re.escape(BS + 'n') + r')*'
    sc = r'(?:<p[^>]*>[ \t]*)?\[' + re.escape(tag) + r'\b[^\]\r\n]*(?:\]|(?=\r?\n))(?:[ \t]*</p>)?'
    pat = re.compile(r'(?P<pre>' + ws + r')(?P<sc>' + sc + r'(?:' + ws + sc + r')*)(?P<post>' + ws + r')')
    head = re.compile(r'<h([1-6])[^>]*>(?:(?!</?h[1-6]).)*?</h\1>' + ws + r'$', re.S)
    keep = '|'.join(re.escape(k) for k in keep_after) or 'a^'
    after = re.compile(r'(?:[ \t]|\r?\n|' + re.escape(BS + 'n') + r'|\[(?:' + keep + r')\b[^\]]*\])*(?:<h([1-6])|$)')
    return ws, pat, head, after


def spans(raw: str, tag: str, keep_after: list[str]):
    ws_re, pat, head, after = patterns(tag, keep_after)
    nl = '\r\n' if '\r\n' in raw else '\n'
    lit = BS + 'n'
    out = []
    for m in pat.finditer(raw):
        a, b, heads = m.start(), m.end(), []
        while True:
            end_at = a + len(m.group('pre')) if not heads else a
            hm = head.search(raw, 0, end_at)
            if not hm or hm.end() != end_at:
                break
            nxt = after.match(raw, b)
            if not nxt or (nxt.group(1) and int(nxt.group(1)) > int(hm.group(1))):
                break
            hs = hm.start()
            a = hs - len(re.search(ws_re + r'$', raw[:hs]).group(0))
            heads.append(re.sub(r'<[^>]+>', '', hm.group(0)).strip())
        pre = raw[a:a + len(re.match(ws_re, raw[a:]).group(0))] if heads else m.group('pre')
        ws = pre + m.group('post')
        if a == 0 or b == len(raw):
            sep = ''
        elif lit in ws and '\n' not in ws:
            sep = lit + lit
        elif '\n' not in ws and pre and m.group('post'):
            sep = ' '
        else:
            sep = nl + nl
        k = len(re.findall(r'\[' + re.escape(tag) + r'\b', m.group('sc')))
        if out and a <= out[-1][1]:
            pa, _, psep, pk, ph = out[-1]
            a = min(a, pa)
            sep = '' if (a == 0 or b == len(raw)) else (psep if psep == lit + lit else nl + nl)
            out[-1] = (a, b, sep, pk + k, ph + heads)
        else:
            out.append((a, b, sep, k, heads))
    return out


def new_content(raw: str, tag: str, keep_after: list[str]) -> tuple[str, int, list[str]]:
    parts, pos, n, heads = [], 0, 0, []
    for a, b, sep, k, h in spans(raw, tag, keep_after):
        parts += [raw[pos:a], sep]; pos = b; n += k; heads += h
    parts.append(raw[pos:])
    return ''.join(parts), n, heads


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['plan'])
    ap.add_argument('dir')
    ap.add_argument('--tag', required=True)
    ap.add_argument('--keep-after', default='the_ad,the_ad_group')
    ap.add_argument('--show', type=int, default=6)
    a = ap.parse_args()
    keep = [x for x in a.keep_after.split(',') if x]
    pairs, tot, nh, bad, shown = {}, 0, 0, [], 0
    for f in sorted(glob.glob(os.path.join(a.dir, 'backup', '*.html'))):
        pid = os.path.basename(f)[:-5]
        raw = open(f, encoding='utf-8', newline='').read()
        if '[' + a.tag not in raw:
            continue
        new, n, heads = new_content(raw, a.tag, keep)
        tot += n; nh += len(heads)
        grew = len(re.findall(r'(?:\r?\n){3,}', new)) > len(re.findall(r'(?:\r?\n){3,}', raw))
        if '[' + a.tag in new or grew:
            bad.append(pid)
        else:
            pairs[pid] = [[raw, new]]
        if shown < a.show:
            for s0, s1, sep, _, h in spans(raw, a.tag, keep)[:1]:
                print('--', pid, h, '\nANTES  ', repr(raw[max(0, s0 - 60):s1 + 50]),
                      '\nDESPUÉS', repr(raw[max(0, s0 - 60):s0] + sep + raw[s1:s1 + 50])); shown += 1
    json.dump(pairs, open(os.path.join(a.dir, 'pairs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'posts {len(pairs)} shortcodes {tot} encabezados quitados {nh} con problemas {bad}')


if __name__ == '__main__':
    main()
