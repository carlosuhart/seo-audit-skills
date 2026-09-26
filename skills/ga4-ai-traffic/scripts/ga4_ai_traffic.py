"""
GA4 AI Traffic — trafico referido desde plataformas de AI Search, usando el
token local que ya incluye scope analytics.readonly (ga4_gsc_auth.py).

Uso:
  py ga4_ai_traffic.py --list-properties
  py ga4_ai_traffic.py --property "properties/123456789" --start 2026-06-01 --end 2026-08-30
"""

import argparse
import json
import os
import pickle
from pathlib import Path

from googleapiclient.discovery import build

LOCAL_TOKEN = Path(os.environ.get("GA4_TOKEN_PATH", str(Path.home() / "ga4_gsc_token.pkl")))

AI_SOURCES = {
    "ChatGPT": ["chatgpt.com", "chat.openai.com"],
    "Perplexity": ["perplexity.ai"],
    "Gemini": ["gemini.google.com", "bard.google.com"],
    "Copilot": ["copilot.microsoft.com", "bing.com"],
    "Claude": ["claude.ai"],
    "Meta AI": ["meta.ai"],
    "Grok": ["grok.com", "x.com"],
    "You.com / Phind": ["you.com", "phind.com"],
}

UNCERTAIN_PLATFORMS = {"Copilot", "Grok"}


def get_creds():
    if not LOCAL_TOKEN.exists():
        raise SystemExit(
            f"No hay token local en {LOCAL_TOKEN}. Correr ga4_gsc_auth.py primero "
            "(requiere sesion local, la service account no tiene scope de Analytics)."
        )
    with open(LOCAL_TOKEN, "rb") as f:
        return pickle.load(f)


def classify_source(source: str):
    source = (source or "").lower()
    for platform, domains in AI_SOURCES.items():
        if any(d in source for d in domains):
            return platform
    return None


def list_properties(creds):
    admin = build("analyticsadmin", "v1beta", credentials=creds)
    accounts = admin.accounts().list().execute()
    out = []
    for acc in accounts.get("accounts", []):
        props = admin.properties().list(filter=f"parent:{acc['name']}").execute()
        for p in props.get("properties", []):
            out.append({"account": acc.get("displayName"), "property": p.get("name"),
                        "display_name": p.get("displayName")})
    return out


def run_report(creds, property_id, start, end):
    data_api = build("analyticsdata", "v1beta", credentials=creds)
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": "sessionSource"}, {"name": "sessionMedium"},
                        {"name": "landingPage"}],
        "metrics": [{"name": "sessions"}, {"name": "totalUsers"},
                    {"name": "engagementRate"}],
        "limit": 100000,
    }
    resp = data_api.properties().runReport(property=property_id, body=body).execute()
    return resp.get("rows", [])


def aggregate(rows):
    by_platform = {}
    landing_pages = {}
    for row in rows:
        source = row["dimensionValues"][0]["value"]
        landing_page = row["dimensionValues"][2]["value"]
        sessions = int(row["metricValues"][0]["value"])
        users = int(row["metricValues"][1]["value"])
        engagement = float(row["metricValues"][2]["value"])

        platform = classify_source(source)
        if not platform:
            continue

        agg = by_platform.setdefault(platform, {"sessions": 0, "users": 0,
                                                  "engagement_sum": 0.0, "rows": 0})
        agg["sessions"] += sessions
        agg["users"] += users
        agg["engagement_sum"] += engagement * sessions
        agg["rows"] += 1

        lp_key = (platform, landing_page)
        landing_pages[lp_key] = landing_pages.get(lp_key, 0) + sessions

    summary = []
    for platform, agg in by_platform.items():
        avg_engagement = agg["engagement_sum"] / agg["sessions"] if agg["sessions"] else 0
        summary.append({
            "platform": platform, "sessions": agg["sessions"], "users": agg["users"],
            "engagement_rate": round(avg_engagement * 100, 1),
            "uncertain": platform in UNCERTAIN_PLATFORMS,
        })
    summary.sort(key=lambda x: x["sessions"], reverse=True)

    top_pages = sorted(
        [{"platform": p, "page": lp, "sessions": s} for (p, lp), s in landing_pages.items()],
        key=lambda x: x["sessions"], reverse=True,
    )[:30]

    return summary, top_pages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--property", default=None)
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--list-properties", action="store_true")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    creds = get_creds()

    if args.list_properties:
        for p in list_properties(creds):
            print(f"{p['account']:30} {p['display_name']:30} {p['property']}")
        return

    if not (args.property and args.start and args.end):
        raise SystemExit("--property, --start y --end son requeridos (o usar --list-properties).")

    rows = run_report(creds, args.property, args.start, args.end)
    summary, top_pages = aggregate(rows)

    result = {
        "property": args.property, "start": args.start, "end": args.end,
        "by_platform": summary, "top_landing_pages": top_pages,
        "total_ai_sessions": sum(p["sessions"] for p in summary),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nGuardado en {args.out}")


if __name__ == "__main__":
    main()
