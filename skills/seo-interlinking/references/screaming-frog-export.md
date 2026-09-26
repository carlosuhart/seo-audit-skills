# Screaming Frog exports required by seo-interlinking

Two separate reports. Exporting the wrong one is the most common failure mode --
the "Internal" tab's own Inlinks/Outlinks columns are *counts*, not the graph, and
carry no anchor text.

## 1. All Inlinks (the actual link graph)

- After a completed crawl: **Bulk Export > Links > All Inlinks**
- Columns used by `audit_interlinking.py`: `From`, `To`, `Anchor Text` (also accepts
  a column literally named `Anchor` if the SF version labels it that way)
- One row per link instance, not per page -- a page with 40 internal links in produces
  40 rows with that page in the `To` column.
- This is what lets the script rebuild who links to whom and what anchor text was used.

## 2. Internal HTML overview (the page list to filter against)

- **Internal tab > filter to HTML > Export**, or **Internal > All > Export** if the
  filter isn't available in that SF version
- Columns used: `Address`, `Indexability`, `Status Code` (falls back to `Status` if
  present under that name instead), `Content Type`
- Used to restrict the audit to indexable, 200-status, HTML pages only -- redirects,
  noindex pages, images, and non-200 responses are excluded from orphan/depth findings
  by design; a "redirect with no inlinks" is a different problem, see the `redirects`
  skill.

## GSC export (optional, but do ask for it)

- Standard Search Analytics export, page-level: `Page`, `Clicks`, `Impressions`,
  `Position`. Any CSV with those columns (case-insensitive) works.
- Without it, the script still runs -- orphans and deep pages are just ranked by
  crawl signal alone, which under-prioritizes pages Google is already trying to send
  traffic to.

## Common gotchas

- Trailing-slash mismatches between the two exports and the GSC export cause a page
  to look like two different URLs. The script normalizes by stripping the URL fragment
  and one trailing slash on paths deeper than the root -- if a project uses `www.`
  and non-`www.` interchangeably, or `http`/`https` inconsistently in old exports,
  normalize the CSV before running the script rather than trusting the tool to guess.
- A homepage URL passed via `--home` that doesn't exactly match its row in the crawl
  (protocol, trailing slash, `www.`) will produce a click-depth graph rooted nowhere --
  every page will look "unreachable" instead of just deep. Copy the exact `Address`
  value for the homepage row from the Internal export.
