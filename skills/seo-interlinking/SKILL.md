---
name: seo-interlinking
description: >
  Audits internal-linking health on an existing website using Screaming Frog exports
  and optional Google Search Console data. Detects orphan pages (indexable pages with
  0-1 internal inlinks), pages buried too deep in click-depth from the homepage,
  internal anchor-text over-optimization, and hub pages that could donate link equity
  to weak pages. Cross-references findings with GSC clicks/impressions to prioritize
  by real impact, then produces a ranked recommendations report (add link from X to Y,
  suggested anchor) -- always reading the target project's own interlinking house
  rules from memory first before suggesting a format. Diagnosis and recommendations
  only: never edits posts, never inserts links, never touches WordPress.
  Use when the user says "auditoría de interlinking", "salud de enlaces internos",
  "páginas huérfanas", "profundidad de clic", "link equity", "internal linking audit",
  "orphan pages", "click depth audit", or asks to find pages with no internal links
  or redistribute internal link authority on an existing site.
  Not for planning a new site's architecture or a new content cluster -- see
  site-architecture or seo-cluster for that.
argument-hint: "<all-inlinks.csv> <internal-overview.csv> --home <url> [--gsc <gsc.csv>]"
metadata:
  category: seo
  author: Zythos Media
---

# SEO Interlinking Audit -- Existing-Site Link Health

Diagnoses the internal-link graph of a site that already exists and already has
content -- orphan pages, pages too deep to get crawled/prioritized, anchor-text
over-optimization, and which high-authority pages could donate link equity to the
weak ones found. Read-only: it never edits a post, never calls a WordPress write
ability, and never inserts a link on its own.

This is the complementary skill to `site-architecture` and `seo-cluster` (which plan
**new** structure or **new** content clusters) and to `seo-programmatic` (which
covers templated pages generated at scale). This skill audits what is already live.

## Quick Reference

| Command | What it does |
|---------|--------------|
| `/seo-interlinking <all-inlinks.csv> <overview.csv> --home <url>` | Full audit: orphans, click depth, anchor text, hub candidates |
| add `--gsc <gsc.csv>` | Prioritizes every finding by real clicks/impressions instead of crawl data alone |
| add `--max-depth <n>` | Override the click-depth threshold (default 4) |
| add `--anchor-repeat-threshold <0-1>` | Override the anchor over-optimization threshold (default 0.8) |

## Required inputs

Two Screaming Frog exports are needed -- **not the same report**. See
`references/screaming-frog-export.md` for exact menu paths if this needs explaining
to a client or a new session:

1. **All Inlinks** (bulk export, `From`/`To`/`Anchor Text` columns) -- this is the
   actual link graph. The "Internal" tab's own `Inlinks`/`Outlinks` columns are just
   counts, they cannot rebuild who-links-to-whom or the anchor text used.
2. **Internal HTML** (or "Internal All" filtered to HTML) -- `Address`, `Indexability`,
   `Status Code` -- used to restrict the audit to indexable, live, HTML pages.

GSC data is optional but strongly recommended -- without it, orphans/deep pages are
ranked only by crawl signals, not by whether Google already sends them traffic. Export
a standard GSC Search Analytics CSV (`Page`, `Clicks`, `Impressions`, `Position`) for
the same property, or ask the user which GSC access method applies to this project
(service account vs. local OAuth token -- see this environment's own GSC access notes)
if a live pull is wanted instead of a CSV.

If the user hasn't provided these files yet, ask for them before running the script --
do not guess file paths.

## Workflow

1. Collect the two Screaming Frog CSVs, the homepage URL, and (if available) the GSC
   CSV or a live GSC pull for the same property.
2. Run the script:
   ```
   python scripts/audit_interlinking.py --inlinks <all-inlinks.csv> --overview <overview.csv> --home <https://example.com/> --gsc <gsc.csv>
   ```
3. Read the JSON the script prints (`summary`, `orphans`, `deep_pages`,
   `anchor_text_flags`, `hub_candidates`).
4. **Before writing a single recommendation, check this environment's project memory
   for that site's own interlinking house rules** (anchor style, how many inline
   links, whether it uses a closing "Recomendamos"/"También te puede interesar" block,
   etc.). Different projects in this environment have different, specific rules --
   never invent a generic format. If no project-specific rule is found, say so
   explicitly rather than assuming one.
5. Render a single prioritized Markdown report, ordered:
   - Orphans with real GSC clicks/impressions first (highest impact: Google already
     wants to send traffic there, it just can't find the page well internally).
   - Then orphans with no GSC signal yet.
   - Then deep pages (same GSC-first ordering).
   - Then anchor-text over-optimization flags.
   Each recommendation names a specific hub candidate to link **from** (pick the
   closest topical match among `hub_candidates`, not just the single highest-traffic
   page for everything) and a suggested anchor text consistent with the project's
   house rules from step 4.
6. Stop there. Do not open the CMS, do not edit a post, do not call any WordPress
   ability to add the link -- hand the report back for the user (or a separate,
   explicitly-confirmed step) to execute.

## Thresholds (script defaults, all overridable via flags)

| Signal | Default | Meaning |
|---|---|---|
| Orphan | 0-1 internal inlinks | On an indexable, 200-status HTML page |
| Deep page | click depth > 4 | BFS distance from the homepage over the internal link graph |
| Anchor over-optimization | one anchor text >= 80% share | Only flagged once a URL has at least 3 internal inlinks |

## Explicitly out of scope

- **SE Ranking** -- retired from this stack entirely, never a data source here.
- **New site or new cluster planning** -- see `site-architecture`, `seo-cluster`,
  `blog-cluster`.
- **Templated/programmatic pages at scale** -- see `seo-programmatic`.
- **Writing anything** -- no post edits, no link insertion, no WordPress writes of
  any kind. Diagnosis and prioritized recommendations only.

## Reference files

- `references/screaming-frog-export.md` -- load on demand: exact Screaming Frog
  report names, menu paths, and column names this skill expects, for when a session
  needs to explain the export steps or troubleshoot a CSV that doesn't parse.
