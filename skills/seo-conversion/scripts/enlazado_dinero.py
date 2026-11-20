# -*- coding: utf-8 -*-
"""Puente del contenido a las páginas de dinero: recorre las URL del sitemap y cuenta los enlaces hacia cada grupo de
páginas de dinero, separando los del menú y pie (todo el HTML) de los que están dentro del contenido principal, con sus
textos ancla. Lista las páginas con más tráfico orgánico que no enlazan ninguna página de dinero desde el contenido.

Un enlace de menú en 300 páginas no equivale a un enlace en contexto: lo que lleva al lector de un artículo a contratar
es el enlace dentro del texto.

Uso (PowerShell):
  py enlazado_dinero.py --sitemap https://www.ejemplo.com/sitemap.xml --dinero dinero.json --out salida/enlazado.json \
     [--intencion salida/intencion.json] [--max 400] [--pausa 0.4]

dinero.json: {"servicios": "/(servicios|services)/[a-z-]+/?$", "contacto": "/(contacto|contact)/?$"}
--intencion: el JSON de intencion_gsc.py, para ordenar las páginas sin enlace por clics e impresiones reales.
"""
import argparse
import collections
import json
import re
import time
from urllib.parse import urlparse

from common import contenido_principal, enlaces, fetch, guardar, normalizar, sitemap_urls


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sitemap", required=True)
    ap.add_argument("--dinero", required=True, help="JSON {grupo: regex de ruta}")
    ap.add_argument("--intencion", help="salida de intencion_gsc.py (opcional)")
    ap.add_argument("--out", default="enlazado.json")
    ap.add_argument("--max", type=int, default=400, help="máximo de páginas a descargar")
    ap.add_argument("--pausa", type=float, default=0.4)
    a = ap.parse_args()

    grupos = json.load(open(a.dinero, encoding="utf-8"))
    host = urlparse(a.sitemap).netloc.replace("www.", "")
    urls = [u for u in sitemap_urls(a.sitemap) if urlparse(u).netloc.replace("www.", "") == host][: a.max]
    print(f"páginas del sitemap a recorrer: {len(urls)}")

    total = collections.Counter(); cuerpo = collections.Counter()
    anclas = collections.defaultdict(collections.Counter); fuentes = collections.defaultdict(set)
    sin_enlace = []
    for i, u in enumerate(urls, 1):
        r = fetch(u)
        if r is None or r.status_code != 200:
            continue
        html = r.text
        es_dinero = any(re.search(rx, urlparse(u).path, re.I) for rx in grupos.values())
        enlaza = False
        for href, _ in enlaces(html):
            ruta = urlparse(normalizar(href, u)).path
            for g, rx in grupos.items():
                if re.search(rx, ruta, re.I):
                    total[g] += 1
        for href, ancla in enlaces(contenido_principal(html)):
            ruta = urlparse(normalizar(href, u)).path
            for g, rx in grupos.items():
                if re.search(rx, ruta, re.I):
                    cuerpo[g] += 1; anclas[g][ancla or "(sin texto)"] += 1; fuentes[g].add(urlparse(u).path); enlaza = True
        if not enlaza and not es_dinero:
            sin_enlace.append(u)
        if i % 50 == 0:
            print(f"  {i}/{len(urls)}")
        time.sleep(a.pausa)

    trafico = {}
    if a.intencion:
        # Las URL de intencion_gsc.py vienen de "paginas_dinero_marca_vs_sin_marca" y de "consultas"; usamos por_pagina si existe.
        datos = json.load(open(a.intencion, encoding="utf-8"))
        for fila in datos.get("paginas", []):
            trafico[fila["pagina"].rstrip("/")] = fila
    sin_enlace_orden = sorted(sin_enlace, key=lambda u: -(trafico.get(u.rstrip("/"), {}).get("impresiones", 0)))

    print("== enlaces a páginas de dinero: en todo el HTML vs dentro del contenido")
    for g in grupos:
        print(f"  {g:14} total {total[g]:5} | en contenido {cuerpo[g]:4} desde {len(fuentes[g]):3} páginas | anclas {anclas[g].most_common(5)}")
    print(f"== páginas que no enlazan ninguna página de dinero desde el contenido: {len(sin_enlace)} de {len(urls)}")
    for u in sin_enlace_orden[:15]:
        print("  ", u)
    guardar({"recorridas": len(urls), "total": dict(total), "en_contenido": dict(cuerpo),
             "anclas": {g: dict(c) for g, c in anclas.items()}, "fuentes": {g: sorted(s) for g, s in fuentes.items()},
             "sin_enlace_a_dinero": sin_enlace_orden}, a.out)


if __name__ == "__main__":
    main()
