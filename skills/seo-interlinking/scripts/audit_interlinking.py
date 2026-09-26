#!/usr/bin/env python3
"""
Purpose: Audit internal-linking health of an existing site from Screaming Frog
         exports, optionally weighted by Google Search Console performance.
Input:   Screaming Frog "All Inlinks" bulk export CSV (From, To, Anchor Text) and
         an "Internal HTML" / "Internal All" overview CSV (Address, Indexability,
         Status Code); optional GSC Search Analytics CSV (Page, Clicks, Impressions,
         Position).
Output:  JSON with orphan pages, click-depth outliers, anchor-text over-optimization
         flags, and hub-page candidates -- ranked by GSC signal where available.
Usage:   python scripts/audit_interlinking.py --inlinks all_inlinks.csv \
             --overview internal_html.csv --home https://example.com/ \
             [--gsc gsc.csv] [--max-depth 4] [--anchor-repeat-threshold 0.8]
"""

import argparse
import csv
import json
import sys
from collections import defaultdict, deque
from typing import Any
from urllib.parse import urldefrag


def normalize(url: str) -> str:
    if not url:
        return url
    url = url.strip()
    url, _ = urldefrag(url)
    if url.endswith("/") and url.count("/") > 3:
        url = url[:-1]
    return url


def _get(row: dict, *keys: str, default: str = "") -> str:
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return default


def load_overview(path: str) -> dict[str, dict]:
    pages: dict[str, dict] = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            addr = normalize(_get(row, "Address", "URL"))
            if not addr:
                continue
            indexability = _get(row, "Indexability").strip().lower()
            status = _get(row, "Status Code", "Status").strip()
            content_type = _get(row, "Content Type").lower()
            pages[addr] = {
                "indexable": indexability == "indexable",
                "status": status,
                "is_html": ("html" in content_type) if content_type else True,
            }
    return pages


def load_edges(path: str) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = normalize(_get(row, "From"))
            dst = normalize(_get(row, "To"))
            anchor = _get(row, "Anchor Text", "Anchor").strip()
            if not src or not dst or src == dst:
                continue
            edges.append((src, dst, anchor))
    return edges


def build_graph(
    edges: list[tuple[str, str, str]], pages: dict[str, dict]
) -> tuple[dict[str, set], dict[str, list]]:
    outgoing: dict[str, set] = defaultdict(set)
    inbound: dict[str, list] = defaultdict(list)
    for src, dst, anchor in edges:
        meta = pages.get(dst)
        if meta is not None and not meta.get("is_html", True):
            continue
        outgoing[src].add(dst)
        inbound[dst].append((src, anchor))
    return outgoing, inbound


def click_depth(outgoing: dict[str, set], home: str) -> dict[str, int]:
    depth = {home: 0}
    q = deque([home])
    while q:
        cur = q.popleft()
        for nxt in outgoing.get(cur, ()):
            if nxt not in depth:
                depth[nxt] = depth[cur] + 1
                q.append(nxt)
    return depth


def load_gsc(path: str | None) -> dict[str, dict]:
    perf: dict[str, dict] = {}
    if not path:
        return perf
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = normalize(_get(row, "Page", "page", "url", "URL"))
            if not url:
                continue

            def num(keys: tuple[str, ...], cast, default):
                raw = _get(row, *keys)
                if raw == "":
                    return default
                try:
                    return cast(str(raw).replace(",", "").replace("%", ""))
                except ValueError:
                    return default

            perf[url] = {
                "clicks": num(("Clicks", "clicks"), int, 0),
                "impressions": num(("Impressions", "impressions"), int, 0),
                "position": num(("Position", "position"), float, 0.0),
            }
    return perf


def with_gsc(items: list[dict], gsc: dict[str, dict]) -> list[dict]:
    for item in items:
        item["gsc"] = gsc.get(item["url"], {"clicks": 0, "impressions": 0, "position": None})
    return items


def find_orphans(pages: dict[str, dict], inbound: dict[str, list]) -> list[dict]:
    orphans = []
    for url, meta in pages.items():
        if not meta.get("indexable") or not meta.get("is_html", True):
            continue
        n_inbound = len({src for src, _ in inbound.get(url, [])})
        if n_inbound <= 1:
            orphans.append({"url": url, "inbound_links": n_inbound})
    return orphans


def find_deep_pages(depth: dict[str, int], pages: dict[str, dict], max_depth: int) -> list[dict]:
    deep = []
    for url, d in depth.items():
        meta = pages.get(url)
        if meta is not None and not meta.get("indexable"):
            continue
        if d > max_depth:
            deep.append({"url": url, "depth": d})
    return deep


def anchor_text_report(inbound: dict[str, list], threshold: float) -> list[dict]:
    findings = []
    for url, sources in inbound.items():
        anchors = [a.strip().lower() for _, a in sources if a and a.strip()]
        if len(anchors) < 3:
            continue
        counts: dict[str, int] = defaultdict(int)
        for a in anchors:
            counts[a] += 1
        top_anchor, top_count = max(counts.items(), key=lambda kv: kv[1])
        share = top_count / len(anchors)
        if share >= threshold:
            findings.append(
                {
                    "url": url,
                    "dominant_anchor": top_anchor,
                    "dominant_share": round(share, 2),
                    "total_internal_anchors": len(anchors),
                    "distinct_anchors": len(counts),
                }
            )
    return findings


def find_hub_candidates(
    pages: dict[str, dict], outgoing: dict[str, set], gsc: dict[str, dict], top_n: int = 20
) -> list[dict]:
    hubs = []
    for url, meta in pages.items():
        if not meta.get("indexable") or not meta.get("is_html", True):
            continue
        out_count = len(outgoing.get(url, ()))
        g = gsc.get(url, {})
        clicks = g.get("clicks", 0)
        impressions = g.get("impressions", 0)
        if out_count == 0 and clicks == 0 and impressions == 0:
            continue
        hubs.append({"url": url, "outlinks": out_count, "clicks": clicks, "impressions": impressions})
    hubs.sort(key=lambda h: (h["clicks"], h["impressions"]), reverse=True)
    return hubs[:top_n]


def run(args: argparse.Namespace) -> dict[str, Any]:
    pages = load_overview(args.overview)
    edges = load_edges(args.inlinks)
    outgoing, inbound = build_graph(edges, pages)
    home = normalize(args.home)
    depth = click_depth(outgoing, home)
    gsc = load_gsc(args.gsc)

    orphans = with_gsc(find_orphans(pages, inbound), gsc)
    orphans.sort(key=lambda o: (o["gsc"]["clicks"], o["gsc"]["impressions"]), reverse=True)

    deep = with_gsc(find_deep_pages(depth, pages, args.max_depth), gsc)
    deep.sort(key=lambda d: (d["gsc"]["clicks"], d["gsc"]["impressions"]), reverse=True)

    anchors = anchor_text_report(inbound, args.anchor_repeat_threshold)
    hubs = find_hub_candidates(pages, outgoing, gsc)

    return {
        "summary": {
            "home": home,
            "pages_in_overview": len(pages),
            "edges_parsed": len(edges),
            "reachable_from_home": len(depth),
            "orphans_found": len(orphans),
            "deep_pages_found": len(deep),
            "anchor_overoptimization_flags": len(anchors),
            "max_depth_threshold": args.max_depth,
            "anchor_repeat_threshold": args.anchor_repeat_threshold,
            "gsc_provided": bool(args.gsc),
        },
        "orphans": orphans[:200],
        "deep_pages": deep[:200],
        "anchor_text_flags": anchors[:200],
        "hub_candidates": hubs,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit internal-linking health from Screaming Frog exports")
    parser.add_argument("--inlinks", required=True, help="Screaming Frog 'All Inlinks' bulk export CSV")
    parser.add_argument("--overview", required=True, help="Screaming Frog 'Internal HTML'/'Internal All' export CSV")
    parser.add_argument("--home", required=True, help="Homepage URL to compute click depth from")
    parser.add_argument("--gsc", help="Optional GSC Search Analytics export CSV (Page, Clicks, Impressions, Position)")
    parser.add_argument("--max-depth", type=int, default=4, help="Flag pages deeper than this click depth (default 4)")
    parser.add_argument(
        "--anchor-repeat-threshold",
        type=float,
        default=0.8,
        help="Flag a URL when one anchor text is >= this share of its internal inlinks (default 0.8)",
    )
    parser.add_argument("--output", "-o", help="Write JSON to this file instead of stdout")
    ns = parser.parse_args()

    try:
        result = run(ns)
        rendered = json.dumps(result, indent=2, ensure_ascii=False)
        if ns.output:
            with open(ns.output, "w", encoding="utf-8") as fh:
                fh.write(rendered)
            print(json.dumps({"status": "ok", "written_to": ns.output, "summary": result["summary"]}, indent=2))
        else:
            print(rendered)
    except Exception as exc:  # noqa: BLE001 - CLI boundary, report and exit non-zero
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)
