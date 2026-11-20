# -*- coding: utf-8 -*-
"""Utilidades compartidas de seo-conversion: autenticación GSC/GA4 portable, descarga de páginas,
lectura recursiva de sitemaps, extracción de enlaces y escritura de JSON.

Credenciales (nunca rutas fijas en el código):
  GSC_TOKEN_PATH           token OAuth local de Search Console (pickle). Default: ~/gsc_token.pkl
  GSC_SERVICE_ACCOUNT_KEY  JSON de service account, usado con --service-account
  GA4_TOKEN_PATH           token OAuth local con scope analytics.readonly. Default: ~/ga4_gsc_token.pkl
"""
import json
import os
import pickle
import re
import sys
import time
from pathlib import Path

import requests

# User-agent genérico de navegador. No incluir nunca datos personales ni de contacto.
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def gsc_service(service_account=False):
    from googleapiclient.discovery import build
    if service_account:
        from google.oauth2 import service_account as sa
        key = os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "")
        if not key or not Path(key).exists():
            raise SystemExit("Falta GSC_SERVICE_ACCOUNT_KEY o el archivo no existe.")
        creds = sa.Credentials.from_service_account_file(key, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
        return build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    tok = Path(os.environ.get("GSC_TOKEN_PATH", str(Path.home() / "gsc_token.pkl")))
    if not tok.exists():
        raise SystemExit(f"No hay token de Search Console en {tok}. Define GSC_TOKEN_PATH o usa --service-account.")
    with open(tok, "rb") as f:
        creds = pickle.load(f)
    _refresh(creds)
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def ga4_headers():
    tok = Path(os.environ.get("GA4_TOKEN_PATH", str(Path.home() / "ga4_gsc_token.pkl")))
    if not tok.exists():
        raise SystemExit(f"No hay token de GA4 en {tok}. Define GA4_TOKEN_PATH.")
    with open(tok, "rb") as f:
        creds = pickle.load(f)
    _refresh(creds)
    return {"Authorization": f"Bearer {creds.token}"}


def _refresh(creds):
    if getattr(creds, "valid", True):
        return
    from google.auth.transport.requests import Request
    creds.refresh(Request())


def gsc_query(service, site, start, end, dimensions, filters=None, row_limit=25000):
    """Devuelve todas las filas paginando de a 25.000."""
    rows, start_row = [], 0
    while True:
        body = {"startDate": start, "endDate": end, "dimensions": dimensions, "rowLimit": row_limit, "startRow": start_row}
        if filters:
            body["dimensionFilterGroups"] = [{"filters": filters}]
        resp = service.searchanalytics().query(siteUrl=site, body=body).execute()
        chunk = resp.get("rows", [])
        rows += chunk
        if len(chunk) < row_limit:
            return rows
        start_row += row_limit


def fetch(url, allow_redirects=True, timeout=30):
    """GET con reintento simple. Devuelve el Response o None."""
    for intento in range(2):
        try:
            r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=allow_redirects)
            # Sin charset en la cabecera, requests asume ISO-8859-1 y rompe tildes y eñes.
            if r.encoding is None or r.encoding.lower() == "iso-8859-1":
                r.encoding = r.apparent_encoding or "utf-8"
            return r
        except requests.RequestException:
            time.sleep(2 * (intento + 1))
    return None


def sitemap_urls(url, _vistos=None):
    """URLs de un sitemap o índice de sitemaps, recursivo."""
    vistos = _vistos if _vistos is not None else set()
    if url in vistos:
        return []
    vistos.add(url)
    r = fetch(url)
    if r is None or r.status_code != 200:
        return []
    out = []
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text):
        loc = loc.replace("&amp;", "&")
        if loc.split("?")[0].endswith(".xml"):
            out += sitemap_urls(loc, vistos)
        else:
            out.append(loc)
    return out


def texto(html):
    return " ".join(re.sub(r"<[^>]+>", " ", html or "").split())


def enlaces(html):
    """Lista de (href, texto ancla)."""
    return [(h, texto(t)[:80]) for h, t in re.findall(r'<a\b[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', html or "", re.S | re.I)]


def contenido_principal(html):
    """<main> sin nav, footer, header ni form. Si no hay <main>, el <body> sin esos bloques."""
    m = re.search(r"<main\b.*?</main>", html or "", re.S | re.I) or re.search(r"<body\b.*?</body>", html or "", re.S | re.I)
    bloque = m.group(0) if m else ""
    return re.sub(r"<(nav|footer|header|form|aside)\b.*?</\1>", " ", bloque, flags=re.S | re.I)


def normalizar(href, base):
    from urllib.parse import urljoin
    return urljoin(base, href).split("#")[0]


def guardar(obj, ruta):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
    print(f"\nJSON: {ruta}")
