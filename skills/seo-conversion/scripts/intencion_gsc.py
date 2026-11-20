# -*- coding: utf-8 -*-
"""Search Console por intención de compra: separa marca, sin marca y consultas anonimizadas, clasifica las
consultas sin marca por nivel de intención (transaccional, comparación, definición, categoría, cómo hacer, informativa) y
muestra qué tipo de página responde a cada una. Marca las páginas de dinero que solo reciben consultas de marca.

Uso (PowerShell):
  py intencion_gsc.py --site "sc-domain:ejemplo.com" --start 2026-07-01 --end 2026-09-28 --marca "ejemplo|ejmplo" \
     --config tipos.json --out salida/intencion.json [--service-account] [--mensual]

tipos.json (orden importa, gana el primer patrón que calza con la ruta):
  {"tipos_pagina": {"home": "^/(es/|en/|pt/)?$", "servicio": "/(servicios|services)/", "blog": "/blog/.+"},
   "tipos_dinero": ["servicio"],
   "intencion": {"categoria": "software|sistema|..."}}   <- opcional, reemplaza el patrón por defecto de ese nivel

Los patrones de intención son heurísticos (es/en/pt). Revisa la tabla "sin clasificar" y ajusta tipos.json por cliente.
"""
import argparse
import collections
import json
import re
from urllib.parse import urlparse

from common import gsc_query, gsc_service, guardar

INTENCION = {  # orden de prioridad: la primera que calza
    "transaccional": r"\b(precio|precios|price|pricing|pre[cç]o|cotiza\w*|cotizaci[oó]n|quote|or[cç]amento|contratar|comprar|buy|hire|demo|prueba gratis|free trial|teste gr[aá]tis|plan(es)?\b|planos)\b",
    "comparacion": r"(\bvs\.?\b|versus|alternativ|comparativ|compar(a|ar|e)\b|\bmejor(es)?\b|\bbest\b|\btop ?\d|\bmelhor(es)?\b|review|rese[nñ]a|opiniones|avalia[cç])",
    # Definiciones antes que categoría: "what is ... software" es informativa aunque nombre la categoría.
    "definicion": r"(\bqu[eé] es\b|\bque son\b|\bo que [eé]\b|\bwhat (is|are)\b|definici|significado|meaning|\bes (lo )?que\b$)",
    "categoria": r"\b(software|sistema|plataforma|platform|herramienta|ferramenta|tool|app|servicio|servi[cç]o|services?|empresas? de|agencia|ag[eê]ncia|agency|proveedor|fornecedor|provider|consultor\w*|outsourcing|soluci[oó]n|solu[cç][aã]o)\b",
    "como_hacer": r"^(c[oó]mo|como|how( to| do)?)\b|\bpaso a paso\b|\bstep by step\b",
    "informativa": r"(\bejemplos?\b|examples?|\btipos de\b|\btypes of\b|\bley\b|\blei\b|\blaw\b|\bkpi\b|\bguía\b|\bguide\b)",
}
LOCAL = r"\b(cerca|near me|perto|en (santiago|chile|lima|bogot[aá]|m[eé]xico|madrid)|in (chile|santiago))\b"


def tipo_pagina(url, tipos):
    ruta = urlparse(url).path or "/"
    for nombre, rx in tipos.items():
        if re.search(rx, ruta, re.I):
            return nombre
    return "otra"


def nivel(q, patrones):
    for n, rx in patrones.items():
        if re.search(rx, q, re.I):
            return n
    return "sin_clasificar"


def agrega(acc, r):
    acc[0] += r["clicks"]; acc[1] += r["impressions"]; acc[2] += r["position"] * r["impressions"]


def fmt(acc):
    c, i, pw = acc[:3]
    return {"clics": round(c), "impresiones": round(i), "posicion": round(pw / i, 1) if i else None}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--marca", required=True, help="regex de marca (nombre y variantes mal escritas)")
    ap.add_argument("--config", help="JSON con tipos_pagina, tipos_dinero e intencion")
    ap.add_argument("--out", default="intencion.json")
    ap.add_argument("--service-account", action="store_true")
    ap.add_argument("--mensual", action="store_true", help="agrega tendencia mensual por tipo de página")
    ap.add_argument("--min-impresiones", type=int, default=2)
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding="utf-8")) if a.config else {}
    tipos = cfg.get("tipos_pagina", {"home": r"^/([a-z]{2}(-[a-z]{2})?/?)?$", "blog": r"/blog/.+"})
    dinero = set(cfg.get("tipos_dinero", []))
    patrones = dict(INTENCION); patrones.update(cfg.get("intencion", {}))
    marca = re.compile(a.marca, re.I)

    svc = gsc_service(a.service_account)
    por_pagina = gsc_query(svc, a.site, a.start, a.end, ["page"])
    pq = gsc_query(svc, a.site, a.start, a.end, ["query", "page"])

    total = [0, 0, 0.0]
    t_tipo = collections.defaultdict(lambda: [0, 0, 0.0])
    for r in por_pagina:
        agrega(total, r); agrega(t_tipo[tipo_pagina(r["keys"][0], tipos)], r)

    seg = collections.defaultdict(lambda: [0, 0, 0.0])
    q = collections.defaultdict(lambda: [0, 0, 0.0, collections.Counter()])
    pag_marca = collections.defaultdict(lambda: {"marca": [0, 0, 0.0], "sin_marca": [0, 0, 0.0]})
    for r in pq:
        consulta, pagina = r["keys"]
        es_marca = bool(marca.search(consulta))
        agrega(seg["marca" if es_marca else "sin_marca"], r)
        tp = tipo_pagina(pagina, tipos)
        agrega(pag_marca[pagina]["marca" if es_marca else "sin_marca"], r)
        if not es_marca:
            agrega(q[consulta], r); q[consulta][3][tp] += r["impressions"]
    anon = [max(total[0] - seg["marca"][0] - seg["sin_marca"][0], 0), max(total[1] - seg["marca"][1] - seg["sin_marca"][1], 0), 0.0]

    niveles = collections.defaultdict(lambda: [0, 0, 0.0, 0])
    detalle = collections.defaultdict(list)
    for consulta, v in q.items():
        if v[1] < a.min_impresiones:
            continue
        n = nivel(consulta, patrones)
        niveles[n][0] += v[0]; niveles[n][1] += v[1]; niveles[n][2] += v[2]; niveles[n][3] += 1
        detalle[n].append({"consulta": consulta, **fmt(v), "local": bool(re.search(LOCAL, consulta, re.I)),
                           "responde": v[3].most_common(1)[0][0], "tipos": dict(v[3])})
    for n in detalle:
        detalle[n].sort(key=lambda x: -x["impresiones"])

    # Heurístico: incluye "X vs Y" del propio rubro que pueden no ser de compra (p. ej. temas del blog). Revisar a mano.
    desajuste = [d for n in ("transaccional", "comparacion", "categoria") for d in detalle.get(n, [])
                 if dinero and d["responde"] not in dinero][:40]
    solo_marca = []
    for pagina, v in pag_marca.items():
        if tipo_pagina(pagina, tipos) in dinero:
            m, s = v["marca"][1], v["sin_marca"][1]
            solo_marca.append({"pagina": pagina, "impresiones_marca": round(m), "impresiones_sin_marca": round(s),
                               "pct_marca": round(100 * m / (m + s), 1) if m + s else None,
                               "posicion_sin_marca": fmt(v["sin_marca"])["posicion"]})
    solo_marca.sort(key=lambda x: -(x["pct_marca"] or 0))

    mensual = {}
    if a.mensual:
        filas = gsc_query(svc, a.site, a.start, a.end, ["page", "date"])
        m = collections.defaultdict(lambda: [0, 0])
        for r in filas:
            k = (r["keys"][1][:7], tipo_pagina(r["keys"][0], tipos)); m[k][0] += r["clicks"]; m[k][1] += r["impressions"]
        mensual = {f"{k[0]}|{k[1]}": {"clics": round(v[0]), "impresiones": round(v[1])} for k, v in sorted(m.items())}

    out = {
        "sitio": a.site, "periodo": [a.start, a.end],
        "total": fmt(total),
        "segmentos": {"marca": fmt(seg["marca"]), "sin_marca": fmt(seg["sin_marca"]),
                      "anonimizadas": {"clics": round(anon[0]), "impresiones": round(anon[1]),
                                       "pct_clics": round(100 * anon[0] / total[0], 1) if total[0] else None}},
        "por_tipo_pagina": {k: fmt(v) for k, v in sorted(t_tipo.items(), key=lambda x: -x[1][1])},
        "por_intencion": {k: {**fmt(v), "consultas": v[3]} for k, v in niveles.items()},
        "consultas": {k: v[:60] for k, v in detalle.items()},
        "comerciales_respondidas_por_pagina_no_dinero": desajuste,
        "paginas_dinero_marca_vs_sin_marca": solo_marca,
        "mensual": mensual,
        "paginas": sorted(({"pagina": r["keys"][0], "tipo": tipo_pagina(r["keys"][0], tipos), "clics": round(r["clicks"]),
                            "impresiones": round(r["impressions"]), "posicion": round(r["position"], 1)} for r in por_pagina),
                          key=lambda x: -x["impresiones"]),
    }

    print(f"== {a.site} {a.start} a {a.end}")
    print("total", out["total"])
    for k, v in out["segmentos"].items():
        print(f"  {k:12} {v}")
    print("== por tipo de página")
    for k, v in out["por_tipo_pagina"].items():
        print(f"  {k:12} {v}")
    print("== sin marca por intención (consultas con >= %d impresiones)" % a.min_impresiones)
    for k in list(patrones) + ["sin_clasificar"]:
        if k in out["por_intencion"]:
            print(f"  {k:14} {out['por_intencion'][k]}")
            for d in detalle[k][:5]:
                print(f"      {d['consulta'][:60]:60} {d['clics']:4} {d['impresiones']:6} pos {d['posicion']} -> {d['responde']}")
    if dinero:
        print("== páginas de dinero: impresiones de marca vs sin marca")
        for d in solo_marca[:15]:
            print(f"  {d['pct_marca']}% marca | sin marca {d['impresiones_sin_marca']} impr pos {d['posicion_sin_marca']} | {d['pagina']}")
        print(f"== consultas comerciales que responde una página que no es de dinero: {len(desajuste)}")
        for d in desajuste[:10]:
            print(f"  {d['consulta'][:60]:60} {d['impresiones']:6} pos {d['posicion']} -> {d['responde']}")
    guardar(out, a.out)


if __name__ == "__main__":
    main()
