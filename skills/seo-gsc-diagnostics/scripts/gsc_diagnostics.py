"""
GSC Diagnostics — quick wins, canibalizacion y anomalias sobre datos reales
de Search Console. Reutiliza el patron de autenticacion ya establecido en
gsc_auth.py (token local) o la service account documentada en CLAUDE.md.

Uso:
  py gsc_diagnostics.py --site "sc-domain:ejemplo.com" --start 2026-06-01 --end 2026-08-30
  py gsc_diagnostics.py --site "https://www.ejemplo.com/" --start ... --end ... --service-account
"""

import argparse
import json
import os
import pickle
import statistics
from pathlib import Path

from googleapiclient.discovery import build

LOCAL_TOKEN = Path(os.environ.get("GSC_TOKEN_PATH", str(Path.home() / "gsc_token.pkl")))
SERVICE_ACCOUNT_KEY = os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "")  # JSON key; ruta propia de cada entorno

CTR_BENCHMARKS = [
    (1, 1, 0.31), (2, 2, 0.165), (3, 3, 0.11),
    (4, 6, 0.065), (7, 10, 0.03), (11, 20, 0.015),
]


def ctr_benchmark(position: float) -> float:
    for lo, hi, ctr in CTR_BENCHMARKS:
        if lo <= position <= hi:
            return ctr
    return 0.01


def get_service():
    if args.service_account:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY,
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
        )
        return build("searchconsole", "v1", credentials=creds)

    if not LOCAL_TOKEN.exists():
        raise SystemExit(
            f"No hay token local en {LOCAL_TOKEN}. Correr gsc_auth.py primero, "
            "o pasar --service-account si el sitio esta entre las propiedades que cubre la service account."
        )
    with open(LOCAL_TOKEN, "rb") as f:
        creds = pickle.load(f)
    return build("searchconsole", "v1", credentials=creds)


def query_gsc(service, site, start, end, dimensions, row_limit=25000):
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    resp = service.searchanalytics().query(siteUrl=site, body=body).execute()
    return resp.get("rows", [])


def detect_quick_wins(rows_query_page):
    impressions = [r["impressions"] for r in rows_query_page]
    if not impressions:
        return []
    impressions.sort()
    p60_idx = int(len(impressions) * 0.6)
    threshold = max(impressions[p60_idx] if p60_idx < len(impressions) else 50, 50)

    wins = []
    for r in rows_query_page:
        pos = r["position"]
        impr = r["impressions"]
        ctr = r["clicks"] / impr if impr else 0
        if impr >= threshold and 5 <= pos <= 20:
            bench = ctr_benchmark(pos)
            if ctr < bench:
                query, page = r["keys"]
                wins.append({
                    "query": query, "page": page, "impressions": impr,
                    "position": round(pos, 1), "ctr_real": round(ctr * 100, 2),
                    "ctr_benchmark": round(bench * 100, 2),
                    "gap": round((bench - ctr) * 100, 2),
                })
    wins.sort(key=lambda x: x["impressions"], reverse=True)
    return wins[:20]


MIN_CLICKS_FLOOR = 3  # por debajo de esto, un ratio alto es 1-2 clics de casualidad, no señal real


def detect_cannibalization(rows_query_page):
    by_query = {}
    for r in rows_query_page:
        query, page = r["keys"]
        by_query.setdefault(query, []).append({
            "page": page, "clicks": r["clicks"], "impressions": r["impressions"],
            "position": r["position"],
        })

    findings = []
    for query, pages in by_query.items():
        if len(pages) < 2:
            continue
        pages.sort(key=lambda p: p["clicks"], reverse=True)
        leader, runner_up = pages[0], pages[1]
        if leader["clicks"] < MIN_CLICKS_FLOOR:
            continue
        ratio = runner_up["clicks"] / leader["clicks"]
        if ratio < 0.10:
            continue
        severity = "Alta" if ratio > 0.30 else "Media"
        findings.append({
            "query": query, "page_a": leader["page"], "page_b": runner_up["page"],
            "clicks_a": leader["clicks"], "clicks_b": runner_up["clicks"],
            "ratio_pct": round(ratio * 100, 1), "severity": severity,
        })
    findings.sort(key=lambda x: (x["severity"] != "Alta", -x["clicks_a"]))
    return findings


def detect_anomalies(rows_date):
    clicks_series = [(r["keys"][0], r["clicks"]) for r in rows_date]
    if len(clicks_series) < 30:
        return {"insufficient_data": True, "days": len(clicks_series)}

    values = [c for _, c in clicks_series]
    mean = statistics.mean(values)
    stdev = statistics.pstdev(values) or 1e-9

    anomalies = []
    for date, clicks in clicks_series:
        z = (clicks - mean) / stdev
        if abs(z) > 2:
            impressions = next(
                (r["impressions"] for r in rows_date if r["keys"][0] == date), None
            )
            anomalies.append({
                "date": date, "clicks": clicks, "impressions": impressions,
                "z_score": round(z, 2),
            })
    anomalies.sort(key=lambda x: x["date"])
    return {"insufficient_data": False, "anomalies": anomalies}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--service-account", action="store_true")
    parser.add_argument("--out", default=None)
    global args
    args = parser.parse_args()

    service = get_service()

    rows_query_page = query_gsc(service, args.site, args.start, args.end, ["query", "page"])
    rows_date = query_gsc(service, args.site, args.start, args.end, ["date"])

    result = {
        "site": args.site,
        "start": args.start,
        "end": args.end,
        "quick_wins": detect_quick_wins(rows_query_page),
        "cannibalization": detect_cannibalization(rows_query_page),
        "anomalies": detect_anomalies(rows_date),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nGuardado en {args.out}")


if __name__ == "__main__":
    main()
