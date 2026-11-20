# -*- coding: utf-8 -*-
"""Inventario de páginas de dinero (servicio, producto, precios, demo, registro, contacto, categoría): estado HTTP sin
seguir redirecciones, indexabilidad (meta robots, X-Robots-Tag, canonical), presencia en el sitemap, title y H1, y la
capacidad de convertir que se ve en el HTML: formularios, CTA, teléfono, WhatsApp, email, precios y tipos de schema.

Responde dos preguntas antes de proponer nada: ¿la página existe y Google puede indexarla? y ¿desde ella se puede
convertir sin depender de JavaScript? (lo que solo aparece tras ejecutar JS se revisa con navegador, ver SKILL.md).

Uso (PowerShell):
  py paginas_dinero.py --urls urls.txt --out salida/paginas_dinero.json
  py paginas_dinero.py --sitemap https://www.ejemplo.com/sitemap.xml --patron "/(servicios|precios|demo|contacto)" --out ...
  Agrega --sitemap aunque pases --urls para comprobar si cada URL está en él.
"""
import argparse
import json
import re
from urllib.parse import urlparse

from common import fetch, guardar, sitemap_urls, texto

CTA = r"(?i)(cotiz|quote|or[cç]amento|demo|agend|schedul|reserv|book|prueba|trial|teste|gratis|free|grátis|contact|contato|habl|talk|fale|llam|call|whatsapp|comprar|buy|add to cart|agregar al carro|solicit|request|diagn[oó]stico|registr|sign ?up|crear cuenta|create account|criar conta|empez|start|comec|precio|pricing|pre[cç]o)"
PRECIO = r"(?i)(\$\s?\d|US\$|USD|CLP|R\$|€|\bUF\s?\d|\d+[.,]?\d*\s?(usd|clp|eur)\b|/mes\b|/month\b|/m[eê]s\b|por mes|per month)"


def analiza(url, en_sitemap):
    r = fetch(url, allow_redirects=False)
    if r is None:
        return {"url": url, "estado": "ERROR"}
    h = r.text if r.status_code == 200 else ""
    meta_rob = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', h, re.I)
    can = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', h, re.I)
    tit = re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I)
    h1 = [texto(x) for x in re.findall(r"<h1\b[^>]*>(.*?)</h1>", h, re.S | re.I)]
    anclas = re.findall(r'<a\b[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', h, re.S | re.I)
    botones = [texto(b) for b in re.findall(r"<button\b[^>]*>(.*?)</button>", h, re.S | re.I)]
    ctas = sorted({texto(t)[:50] for href, t in anclas if re.search(CTA, texto(t) + " " + href)} | {b[:50] for b in botones if b and re.search(CTA, b)})
    schema = sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', h)))
    noindex = bool(re.search(r"noindex", (meta_rob.group(1) if meta_rob else "") + " " + r.headers.get("X-Robots-Tag", ""), re.I))
    canonical = can.group(1) if can else ""
    propia = canonical.rstrip("/") == url.rstrip("/") if canonical else None
    alertas = []
    if r.status_code != 200:
        alertas.append(f"HTTP {r.status_code}" + (f" -> {r.headers.get('location')}" if r.headers.get("location") else ""))
    if noindex:
        alertas.append("noindex")
    if canonical and not propia:
        alertas.append("canonical a otra URL")
    if en_sitemap is False and r.status_code == 200:
        alertas.append("fuera del sitemap")
    if r.status_code == 200 and not re.search(r"<form\b", h, re.I) and not ctas:
        alertas.append("sin formulario ni CTA en el HTML (revisar con navegador)")
    if r.status_code == 200 and len(h1) != 1:
        alertas.append(f"{len(h1)} H1")
    return {
        "url": url, "estado": r.status_code, "location": r.headers.get("location"),
        "noindex": noindex, "canonical": canonical, "canonical_propio": propia, "en_sitemap": en_sitemap,
        "title": texto(tit.group(1))[:90] if tit else "", "h1": h1[:2],
        "formularios": len(re.findall(r"<form\b", h, re.I)), "ctas": ctas[:15],
        "telefono": bool(re.search(r'href="tel:', h, re.I)),
        "whatsapp": bool(re.search(r"wa\.me/|api\.whatsapp\.com|web\.whatsapp\.com", h, re.I)),
        "email": bool(re.search(r'href="mailto:', h, re.I)),
        "precio_visible": bool(re.search(PRECIO, texto(h))), "schema": schema, "alertas": alertas,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls", help="archivo con una URL por línea")
    ap.add_argument("--sitemap", help="sitemap o índice; con --patron selecciona URLs, sin --urls")
    ap.add_argument("--patron", help="regex sobre la ruta para elegir páginas de dinero del sitemap")
    ap.add_argument("--out", default="paginas_dinero.json")
    a = ap.parse_args()
    if not a.urls and not (a.sitemap and a.patron):
        ap.error("usa --urls o --sitemap con --patron")

    del_sitemap = sitemap_urls(a.sitemap) if a.sitemap else None
    norm = {u.rstrip("/") for u in del_sitemap} if del_sitemap is not None else None
    if a.urls:
        urls = [l.strip() for l in open(a.urls, encoding="utf-8") if l.strip() and not l.startswith("#")]
    else:
        urls = sorted({u for u in del_sitemap if re.search(a.patron, urlparse(u).path, re.I)})
    print(f"páginas a revisar: {len(urls)}" + (f" | URLs en sitemap: {len(del_sitemap)}" if del_sitemap is not None else ""))

    filas = [analiza(u, (u.rstrip("/") in norm) if norm is not None else None) for u in urls]
    for f in filas:
        print(f"{f.get('estado')} | {'; '.join(f.get('alertas', [])) or 'ok'} | form {f.get('formularios')} tel {f.get('telefono')} wa {f.get('whatsapp')} precio {f.get('precio_visible')} | {f['url']}")
    resumen = {"revisadas": len(filas), "con_alertas": sum(1 for f in filas if f.get("alertas")),
               "no_200": sum(1 for f in filas if f.get("estado") != 200),
               "fuera_sitemap": sum(1 for f in filas if f.get("en_sitemap") is False),
               "sin_precio_visible": sum(1 for f in filas if f.get("estado") == 200 and not f.get("precio_visible"))}
    print("resumen", resumen)
    guardar({"resumen": resumen, "paginas": filas}, a.out)


if __name__ == "__main__":
    main()
