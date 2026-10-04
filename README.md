# SEO Skills for Claude Code

Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search

A knowledge base of 39 skills for technical SEO audits with Claude Code.
Each skill encodes real-world patterns: documented CMS bugs, fix-ready code
snippets, audit checklists, and edge cases that generic AI training data misses.

Covers the full audit stack — CMS mechanics, JS-framework sites, Core Web Vitals,
schema markup, cache architecture, hreflang, third-party script management, and
the tools SEOs actually use.

- **CMS**: WordPress (Divi, Elementor, WooCommerce, multilingual WPML forensics), PrestaShop, Shopify
- **JS frameworks**: React/Next.js, Vue/Nuxt on Vercel/Netlify — no CMS, no plugin
- **Analytics & tracking**: GA4, Google Tag Manager
- **SEO tools**: Screaming Frog, SE Ranking, Semrush
- **Technical**: robots.txt (+ indexability), sitemap, canonical tags, redirects, on-page fundamentals, Core Web Vitals, cache, images, SSL/HTTPS, schema markup, hreflang, third-party scripts, JavaScript SEO
- **AI/GEO**: GEO (Generative Engine Optimization), AI crawler access, llms.txt, Wikidata entity, brand citation signals

All knowledge is anonymized and GDPR compliant — no client data, no domains,
no identifying information. The pattern matters, not the source.

---

## Skills

Each skill lives in `skills/<name>/SKILL.md`. The details (bugs, fixes, checklists) are inside the file; this list only says what each one is for.

### CMS

| Skill | What it covers |
|---|---|
| `wordpress-divi` | Recurring SEO issues in WordPress + Divi, with fixes and checklist |
| `wordpress-elementor` | Recurring SEO issues in WordPress + Elementor (free and Pro), with fixes and checklist |
| `wordpress-hidden-errors` | Forensic audit of large or multilingual WordPress sites: broken or cross-language links, orphan shortcodes, AI residue, injected scripts, duplicates and poisoned cache, with md5-checked fixes (+ `references/`, `scripts/`) |
| `prestashop-seo` | PrestaShop issues, back office settings, URL structure, sitemap and performance |

### Tracking and tools

| Skill | What it covers |
|---|---|
| `google-tag-manager` | GTM diagnosis: events not reaching GA4, dataLayer, Consent Mode v2, firing order |
| `ga4-analysis` | GA4 analysis: organic vs paid, attribution, channel groupings, period comparison, GSC crossing |
| `screaming-frog` | Crawl modes, CMS configuration, key reports, integrations and known false positives |
| `se-ranking` | Reading SE Ranking data: rank tracking, Site Audit, keywords, competitor gap |
| `semrush` | Semrush in audits: Organic Research, Keyword and Backlink Gap, Site Audit, data reliability |

### Technical

| Skill | What it covers |
|---|---|
| `robots-txt` | robots.txt and indexability: Google spec, templates by site type, Merchant Center, AI bots, meta robots |
| `canonical` | Canonical audits: pagination, parameters, chains, hreflang conflicts and CMS bugs |
| `redirects` | 301/302 redirects: chains, loops, migrations, WordPress, PrestaShop and Cloudflare |
| `on-page-fundamentals` | Title, meta description and H1: lengths, duplicates, cannibalization, CMS bugs, CTR |
| `sitemap` | XML sitemap audits: discovery, URL quality, lastmod integrity, CMS patterns |
| `hreflang` | Hreflang in multilingual WordPress: WPML, TranslatePress, reciprocity, x-default |
| `schema-markup` | JSON-LD: type selection, CMS implementation, documented bugs, validation |
| `javascript-seo` | JS-framework sites without a CMS (Next.js, Nuxt): hydration, gated content, soft-404, config-based canonical |

### Performance and security

| Skill | What it covers |
|---|---|
| `core-web-vitals` | LCP, CLS, INP and TTFB: field vs lab data, diagnostic tree, fixes by CMS |
| `cache-headers` | Cache-Control, CDN vs browser cache, LiteSpeed + Cloudflare, CMS setups |
| `image-optimization` | WebP/AVIF, srcset, LCP image, lazy loading, alt text, CLS |
| `third-party-scripts` | async/defer, impact by vendor, GTM deferral, scripts injected into post content |
| `ssl-https` | Certificates, mixed content, HTTPS redirects, HSTS and security headers |

### Search Console, analytics and AI search

| Skill | What it covers |
|---|---|
| `mineria-de-impresiones` | Turns GSC queries into a content plan: what to improve, create or retitle |
| `seo-gsc-diagnostics` | Quick wins, query cannibalization and anomalies from raw GSC data (+ script) |
| `seo-interlinking` | Internal-linking audit from Screaming Frog + GSC: orphans, depth, anchors, hubs (+ script) |
| `ga4-ai-traffic` | Real referral traffic from AI assistants in GA4, reported as a floor (+ script) |
| `geo-ai-discoverability` | Signals for AI citation: crawler access, llms.txt, Wikidata, schema, citable passages |

### Verticals, defense and commercial

| Skill | What it covers |
|---|---|
| `seo-educacion` | Higher-education SEO: enrollment funnel, seasonality, Course schema, keyword tiers |
| `seo-negativo` | Negative SEO monitoring: link bombing, scraping, penalties, fake reviews, disavow |
| `seo-quote` | Client-ready `.docx` audit with an hours estimate and a USD quote |

### Privacy (8 jurisdictions)

`privacidad` is the orchestrator: it detects which laws apply from the site's targeting (not mere accessibility), runs one shared discovery pass and consolidates the results. Each sub-skill also works on its own and returns a score, an article-by-article table and penalties in local currency.

| Sub-skill | Law | Jurisdiction |
|---|---|---|
| `rgpd` | GDPR (EU 2016/679) | European Union |
| `uk-gdpr` | UK GDPR + PECR 2003 | United Kingdom |
| `ley-datos-chile` | Ley 21.719 | Chile |
| `lgpd` | Lei 13.709/2018 | Brazil |
| `ley-25326` | Ley 25.326 | Argentina |
| `lfpdppp` | LFPDPPP | Mexico |
| `nfadp` | nFADP / revDSG | Switzerland |
| `ccpa` | CCPA / CPRA | California, US |

---

## Installation


### Manual install — Unix / macOS / Linux

```bash
git clone --depth 1 https://github.com/carlosuhart/seo-audit-skills.git
bash seo-audit-skills/install.sh
```

### Manual install — Windows (PowerShell)

```powershell
git clone --depth 1 https://github.com/carlosuhart/seo-audit-skills.git
powershell -ExecutionPolicy Bypass -File seo-audit-skills\install.ps1
```

All scripts copy each `skills/*/SKILL.md` to `~/.claude/skills/[name]/SKILL.md`.
Running them again updates existing skills.

## Works well with

Works standalone. For broader SEO coverage (AI search optimization, local SEO, programmatic SEO), combine with [claude-seo](https://github.com/AgriciDaniel/claude-seo).

## Privacy

All knowledge is anonymized. No client names, domains, or identifying data.
GDPR compliant.

## Contributing

Enrich the skills with real patterns as new issues appear.
Rule: knowledge is added anonymized — the pattern matters, not the source.
