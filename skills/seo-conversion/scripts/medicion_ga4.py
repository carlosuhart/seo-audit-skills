# -*- coding: utf-8 -*-
"""Puerta de medición en GA4: antes de diagnosticar conversión, comprueba que los datos sirvan. Revisa eventos clave
configurados, retención, hostnames que no son producción (localhost, staging, herramientas de prueba), eventos de lead
posiblemente duplicados, conversión por página de entrada orgánica y sesiones y eventos clave desde asistentes de IA.

No corrige nada: devuelve alertas con la evidencia para decidir si el diagnóstico puede seguir o si primero hay que
arreglar la medición.

Uso (PowerShell):
  py medicion_ga4.py --list-properties
  py medicion_ga4.py --property properties/123456789 --start 2026-07-01 --end 2026-09-28 --host www.ejemplo.com \
     [--lead "generate_lead|form_.*_ok|purchase"] --out salida/medicion.json
"""
import argparse
import collections
import re

import requests

from common import ga4_headers, guardar

ADMIN = "https://analyticsadmin.googleapis.com/v1beta"
DATA = "https://analyticsdata.googleapis.com/v1beta"
IA = r"(chatgpt\.com|chat\.openai\.com|openai|perplexity|gemini\.google|bard\.google|copilot\.microsoft|bing\.com/chat|claude\.ai|you\.com|grok|x\.ai|deepseek|meta\.ai)"
NO_PROD = r"(localhost|127\.0\.0\.1|staging|stage\.|dev\.|test\.|preview|vercel\.app|netlify\.app|pages\.dev|tagassistant|webcache|translate\.goog)"


def informe(prop, h, body):
    r = requests.post(f"{DATA}/{prop}:runReport", headers=h, json=body, timeout=60).json()
    if "error" in r:
        return [], r["error"].get("message")
    dims = [d["name"] for d in body["dimensions"]]; mets = [m["name"] for m in body["metrics"]]
    filas = [{**dict(zip(dims, [v["value"] for v in f["dimensionValues"]])),
              **dict(zip(mets, [float(v["value"]) for v in f["metricValues"]]))} for f in r.get("rows", [])]
    return filas, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list-properties", action="store_true")
    ap.add_argument("--property")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--host", help="hostname de producción esperado")
    ap.add_argument("--lead", default=r"generate_lead|form.*(ok|submit|enviado|success)|lead|contact|cotiza|quote|demo|sign_up|purchase|whatsapp|click_to_call|llamada",
                    help="regex de eventos que representan un lead o venta")
    ap.add_argument("--out", default="medicion.json")
    a = ap.parse_args()
    h = ga4_headers()

    if a.list_properties:
        r = requests.get(f"{ADMIN}/accountSummaries?pageSize=200", headers=h, timeout=60).json()
        for c in r.get("accountSummaries", []):
            for p in c.get("propertySummaries", []):
                print(p["property"], "|", p.get("displayName"), "|", c.get("displayName"))
        return
    if not (a.property and a.start and a.end):
        ap.error("--property, --start y --end son obligatorios")

    alertas = []
    rng = [{"startDate": a.start, "endDate": a.end}]
    ke = requests.get(f"{ADMIN}/{a.property}/keyEvents", headers=h, timeout=60).json().get("keyEvents", [])
    eventos_clave = [k["eventName"] for k in ke]
    ret = requests.get(f"{ADMIN}/{a.property}/dataRetentionSettings", headers=h, timeout=60).json()
    retencion = ret.get("eventDataRetention")
    if retencion in ("TWO_MONTHS", "TWO_MONTHS_RETENTION"):
        alertas.append("retención de eventos en 2 meses: no permite comparar con el año anterior en exploraciones")
    if not eventos_clave:
        alertas.append("sin eventos clave configurados")

    hosts, err = informe(a.property, h, {"dateRanges": rng, "dimensions": [{"name": "hostName"}],
                                         "metrics": [{"name": "sessions"}, {"name": "screenPageViews"}, {"name": "keyEvents"}], "limit": 100})
    for f in hosts:
        f["paginas_por_sesion"] = round(f["screenPageViews"] / f["sessions"], 2) if f["sessions"] else None
        if re.search(NO_PROD, f["hostName"], re.I) or (a.host and f["hostName"] not in (a.host, "(not set)") and f["sessions"] > 0 and not f["hostName"].endswith(a.host.replace("www.", ""))):
            alertas.append(f"hostname ajeno a producción con datos: {f['hostName']} ({int(f['sessions'])} sesiones, {int(f['keyEvents'])} eventos clave)")

    ev, _ = informe(a.property, h, {"dateRanges": rng, "dimensions": [{"name": "eventName"}, {"name": "sessionDefaultChannelGroup"}],
                                    "metrics": [{"name": "eventCount"}, {"name": "keyEvents"}, {"name": "sessions"}], "limit": 1000})
    lead = collections.Counter(); lead_canal = collections.defaultdict(collections.Counter); lead_ses = collections.Counter()
    for f in ev:
        if re.search(a.lead, f["eventName"], re.I):
            lead[f["eventName"]] += f["eventCount"]; lead_canal[f["eventName"]][f["sessionDefaultChannelGroup"]] += f["eventCount"]
            lead_ses[f["eventName"]] += f["sessions"]
    for n, c in lead.items():
        # Un lead real rara vez se repite en la misma sesión; >1,3 disparos por sesión apunta a activadores dobles.
        if lead_ses[n] and c / lead_ses[n] > 1.3 and n != "purchase":
            alertas.append(f"'{n}' se dispara {round(c / lead_ses[n], 2)} veces por sesión ({int(c)} en {int(lead_ses[n])} sesiones): revisar activadores duplicados")
    nombres = list(lead)
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            x, y = lead[nombres[i]], lead[nombres[j]]
            if x and y and (abs(x - 2 * y) <= max(1, 0.1 * x) or abs(y - 2 * x) <= max(1, 0.1 * y)):
                alertas.append(f"posible duplicado: {nombres[i]}={int(x)} y {nombres[j]}={int(y)} (uno es el doble del otro; revisar activadores)")
    for n in nombres:
        if n not in eventos_clave and lead[n] > 0:
            alertas.append(f"evento de lead '{n}' con {int(lead[n])} disparos no está marcado como evento clave")

    canales, _ = informe(a.property, h, {"dateRanges": rng, "dimensions": [{"name": "sessionDefaultChannelGroup"}],
                                         "metrics": [{"name": "sessions"}, {"name": "keyEvents"}], "limit": 50})
    landing, _ = informe(a.property, h, {"dateRanges": rng, "dimensions": [{"name": "landingPage"}],
                                         "metrics": [{"name": "sessions"}, {"name": "keyEvents"}, {"name": "engagementRate"}],
                                         "dimensionFilter": {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {"value": "Organic Search"}}},
                                         "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}], "limit": 100})
    sin_landing = sum(f["sessions"] for f in landing if f["landingPage"] in ("(not set)", ""))
    tot_org = sum(f["sessions"] for f in landing)
    if tot_org and sin_landing / tot_org > 0.05:
        alertas.append(f"{round(100 * sin_landing / tot_org, 1)}% de sesiones orgánicas sin página de entrada: el page_view inicial no se registra (consentimiento o etiqueta)")
    fuentes, _ = informe(a.property, h, {"dateRanges": rng, "dimensions": [{"name": "sessionSource"}],
                                         "metrics": [{"name": "sessions"}, {"name": "keyEvents"}], "limit": 500})
    ia = [f for f in fuentes if re.search(IA, f["sessionSource"], re.I)]

    if any(f["sessionDefaultChannelGroup"] == "AI Assistant" for f in canales):
        print("nota: la propiedad ya usa el canal predeterminado 'AI Assistant'; comparar con la lista de fuentes de IA")
    out = {"propiedad": a.property, "periodo": [a.start, a.end], "eventos_clave": eventos_clave, "retencion": retencion,
           "hosts": hosts, "eventos_lead": dict(lead), "eventos_lead_por_canal": {k: dict(v) for k, v in lead_canal.items()},
           "canales": canales, "landing_organico": landing, "ia": ia, "alertas": alertas, "error_hosts": err}
    print(f"== {a.property} {a.start} a {a.end}")
    print("eventos clave:", eventos_clave, "| retención:", retencion)
    print("hosts:", [(f["hostName"], int(f["sessions"]), f["paginas_por_sesion"]) for f in hosts[:8]])
    print("eventos de lead:", {k: int(v) for k, v in lead.items()})
    print("canales:", [(f["sessionDefaultChannelGroup"], int(f["sessions"]), int(f["keyEvents"])) for f in canales[:10]])
    print("orgánico, páginas de entrada con eventos clave:", [(f["landingPage"][:50], int(f["sessions"]), int(f["keyEvents"])) for f in landing if f["keyEvents"]][:10])
    print("asistentes de IA:", [(f["sessionSource"], int(f["sessions"]), int(f["keyEvents"])) for f in ia])
    print("== ALERTAS" if alertas else "== sin alertas")
    for x in alertas:
        print("  -", x)
    guardar(out, a.out)


if __name__ == "__main__":
    main()
