# SEO Skills for Claude Code

Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search


A knowledge bas e of 21 skills for technical SEO audits with  Claude Code.
Each skill encodes real-world pa tterns: documented CMS bugs, fix-ready code
s nippets, audit checklists, and edge cases tha t generic AI training data misses.

Covers th e full audit stack — CMS mechanics, Core We b Vitals, schema markup,
cache architecture,  hreflang, third-party script management, and  the tools
SEOs actually use.

- **CMS**: Word Press (Divi, Elementor, WooCommerce), PrestaS hop, Shopify
- **Analytics & tracking**: GA4,  Google Tag Manager
- **SEO tools**: Screamin g Frog, SE Ranking, Semrush
- **Technical**:  robots.txt (+ indexability), sitemap, canonic al tags, redirects, on-page fundamentals, Cor e Web Vitals, cache, images, SSL/HTTPS, schem a markup, hreflang, third-party scripts
- **A I/GEO**: GEO (Generative Engine Optimization) , AI crawler access, llms.txt, Wikidata entit y, brand citation signals

All knowledge is a nonymized and GDPR compliant — no client da ta, no domains,
no identifying information. T he pattern matters, not the source.

---

##  Skills

### CMS — WordPress + Divi

**File: ** `skills/wordpress-divi/SKILL.md`

Covers W ordPress sites built with Divi Theme (Elegant  Themes) 4.27.x.

- **Missing H1** — Divi d oes not generate H1 automatically. Fix: modul e > Design > Heading Tag
- **Massive inline C SS** — Divi Dynamic CSS injects hundreds of  KB per page. Fix: Critical CSS + Improved As set Loading
- **Render-blocking JS** — 10-2 0 scripts without `async`/`defer`. PHP snippe ts with `script_loader_tag` hook (WP 4.1+) to  defer by handle, with jQuery exclusion
- **H ero as CSS background-image** — invisible t o the preload scanner. Fix: `<link rel="prelo ad">` or convert to real `<img>`
- **Security ** — `<meta generator>`, `X-Powered-By`, op en REST API, user enumeration, pingback. PHP  snippets with `wp_robots` (WP 5.7+) and `rest _authentication_errors` (WP 4.4+) hooks
- **V irtual robots.txt** — WordPress generates r obots.txt without a physical file. `robots_tx t` hook (WP 3.0+) to add AI crawler rules
- * *Conditional loading** — Ninja Forms, Dashi cons and GDPR plugins load on all pages. Fix:  `wp_enqueue_scripts` with priority 100+
- Au dit checklist by criticality + common positiv es + Divi/Yoast configuration paths

---

###  CMS — WordPress + Elementor

**File:** `sk ills/wordpress-elementor/SKILL.md`

Covers Wo rdPress sites built with Elementor (free and  Pro), including stacks with WP Rocket and Woo Commerce.

- **Lazy-loaded LCP hero** — Ele mentor and WP Rocket replace `src` with SVG p laceholder. `fetchpriority="high"` becomes us eless even when present. Fix: `e-no-lazyload` , exclude in WP Rocket > Media > LazyLoad
- * *fetchpriority on wrong element** — assigne d to decorative images (separators, dividers)  instead of the real LCP image
- **Excessive  CSS/JS** — 40-90+ resources. Fix: Improved  Asset Loading (Elementor > Settings > Perform ance)
- **Massive HTML payload** — WP Rocke t injects `RocketLazyLoadScripts` and `elemen torFrontendConfig` inline. Observed up to 1.4  MB
- **Elementor lazy load on backgrounds**  — `.e-con.e-parent:nth-of-type(n+4)` hides  backgrounds of sections 4+ until JS marks the m. Causes CLS
- **Missing security headers**  — consistent pattern. Snippets for Nginx an d Apache
- **Version exposure** — Elementor  in meta generator. PHP snippet to remove it
 - **REST Link header** — exposes internal W ordPress IDs. Fix: `remove_action('template_r edirect', 'rest_output_link_header', 11)`
- * *DOM size** — Section/Column (4 divs) vs Fl exbox Containers (2 divs). Fix: Elementor > T ools > Converter
- **WooCommerce** — duplic ate BreadcrumbList (Yoast + Schema Pro), FAQP age without rich results in e-commerce since  2023, missing Product schema, `/my-account/`  in sitemap
- **PHP EOL** — 7.4 EOL since No v 2022. Fix: update in hPanel/cPanel/Plesk
-  **Keyword cannibalization on location pages**  — Elementor makes it easy to duplicate tem plates by city
- Audit checklist by criticali ty + common positives + configuration paths

 ---

### CMS — PrestaShop

**File:** `skill s/prestashop-seo/SKILL.md`

Covers PrestaShop  1.7.x / 8.x, including stacks with CreativeE lements and Nginx/Plesk.

- **sitemap.xml 404 ** — PrestaShop generates the sitemap at `/ 1_index_sitemap.xml`. The standard path does  not exist by default. Fix: 301 redirect in Ng inx or .htaccess
- **Cache-Control: no-store* * — disabled by default on all HTML pages.  Fix: CCC in Advanced Parameters > Performance  (Smart cache CSS/JS, Minify HTML, Move JS to  end)
- **URLs with numeric ID** — `/217-sl ug` is PrestaShop standard. Not an error if t he canonical points to the URL with ID. Migra tion requires a redirect plan
- **Controllers  in sitemap** — CreativeElements and sitema p modules include internal AJAX endpoints. Fi x: exclude from the module or block in robots .txt
- **PHPSESSID with decade-long expiry**  — GDPR/ePrivacy. Fix: `session.cookie_lifet ime = 0` in php.ini
- **Missing OG tags** —  PrestaShop does not generate them by default . Smarty snippets for head.tpl
- **Hero as ba ckground-image** — native sliders and Creat iveElements. Fix: `displayHeader` hook to inj ect preload
- **Security** — Nginx headers,  CSP in report-only mode, `expose_php = Off`
 - **Schema Product + Offer** — generated na tively in PS8 if enabled. AggregateRating req uires a reviews module
- **IndexNow** — imp lementation via `actionObjectProductUpdateAft er` hook
- Backoffice route table + checklist  by criticality + common positives

---

###  Tracking — Google Tag Manager

**File:** `s kills/google-tag-manager/SKILL.md`

GTM debug ging and configuration, focused on the "event  not reaching GA4" scenario.

- **Diagnostic  tree** — 7 ordered steps: paused tag → re strictive trigger → Preview Mode → Consen t Mode → firing order → Measurement ID � � DebugView
- **Preview vs Production** — P review bypasses ad blockers and Consent Mode.  Always test in incognito. `?gtm_debug=x` for  debugging in the real environment
- **dataLa yer** — structure, naming rules, GA4 reserv ed events, how to read the dataLayer in conso le and in the Preview tab
- **Consent Mode v2 ** — mandatory in EEA since March 2024. `an alytics_storage: denied` blocks GA4 tags. Dif ference between Basic and Advanced Consent Mo de. Default + update snippets
- **Firing orde r** — GA4 Configuration Tag must fire on "I nitialization - All Pages" before Event Tags.  Tag Sequencing to guarantee it. Full trigger  hierarchy
- **DebugView** — how to activat e via GTM, Chrome Extension or URL param
- ** Common cases** — AJAX forms vs traditional  submit, Contact Form 7 (`wpcf7mailsent`), Ele mentor Forms, clicks on `tel:` and `mailto:`
 - Container installation verification via con sole and Network tab

---

### Tracking — G A4 Analysis

**File:** `skills/ga4-analysis/S KILL.md`

GA4 data analysis for SEO audits, f ocused on organic vs paid acquisition.

- **U A to GA4 differences** — sessions vs events , bounce rate vs engagement rate, goals vs co nversions, sampling vs BigQuery
- **Organic v s paid** — channel groups, how to isolate O rganic Search, why misconfigured UTMs inflate  organic
- **Attribution models** — Data-dr iven (default), Last click, First click, Line ar, Time decay. Lookback windows. Why GA4 and  Google Ads show different numbers
- **Engage ment** — definition of engaged session (>=1 0s or >=2 pages or conversion), difference fr om UA bounce rate
- **GSC integration** — R eports > Acquisition > Search Console. Limita tion: only sessions where GA4 recorded the vi sit
- **Google Ads integration** — remarket ing audiences, conversion import, organic vs  paid side-by-side analysis
- **DebugView** � � activation, latency, parameter validation
-  **Useful SEO reports** — organic landing p ages, organic queries, pages with high organi c bounce rate
- **Common errors** — paid tr affic in Organic, self-referral, inflated ses sions, duplicate conversions, excessive direc t traffic
- BigQuery export, key dimensions a nd metrics

---

### Tool — SE Ranking

**F ile:** `skills/se-ranking/SKILL.md`

SE Ranki ng data interpretation in the context of SEO  audits.

- **Rank tracking** — normal volat ility (+-3) vs real drop (>5 positions sustai ned 7+ days) vs sudden drop (possible update) . Diagnostic tree before acting
- **SERP Feat ures** — position 4 with Featured Snippet c an outperform position 1 without feature in r eal CTR
- **Site Audit** — static crawler ( no JS rendering). Issues = signals, not concl usions. Prioritization table: high/medium/low  priority by real impact
- **Documented false  positives** — H1 missing in Divi/Elementor , duplicate content from pagination, broken l inks in JS, dynamic meta description
- **Traf fic estimation** — error margin +-40-60%. U se as trend, not absolute figure. Comparison  with GA4 and GSC
- **Keyword research** — r ecommended flow from seed keywords to intent  assignment. Volume differences between SE Ran king, Semrush and Google Ads
- **Competitor a nalysis** — Share of Voice, Keyword Gap, wh en to use Semrush for discovery and SE Rankin g for precise tracking
- Integration with GSC , Screaming Frog and Semrush

---

### Tool � �� Screaming Frog

**File:** `skills/screamin g-frog/SKILL.md`

Technical use of Screaming  Frog SEO Spider in audits.

- **Spider vs JS  Rendering** — Spider: fast, does not execut e JS. JS Rendering: uses Chromium, 5-10x slow er, mandatory for Divi/Elementor. Selective c rawl by URL list for large sites
- **CMS conf iguration** — WordPress (exclusions for wp- admin, feeds, searches; JS timeout 10s) and P restaShop (session/currency/language paramete rs to exclude; Accept-Language header)
- **Ke y reports** — Response Codes (302->301 redi rects, linked 404s, 500s), Page Titles (missi ng, duplicate, length), Meta Description, H1  (missing, multiple), Canonicals (pointing to  404, missing canonical), Directives (unintent ional noindex), Images (alt text, size)
- **O rphan pages** — Bulk Export > All Inlinks.  Pages without internal links that rank in SE  Ranking = opportunity to improve internal Pag eRank
- **Integration** — GSC (impressions/ clicks columns in crawl), GA4 (sessions per U RL), PSI (selective crawl only)
- **False pos itives** — H1 missing in Divi/Elementor, du plicate content in pagination without canonic al, broken links in JS modals, slow page with out CDN cache, images missing alt in CSS back grounds
- **Performance** — estimated time  table by site size and crawl mode. Minimum 8G B RAM for JS rendering

---

### Tool — Sem rush

**File:** `skills/semrush/SKILL.md`

Se mrush use and interpretation as a complementa ry tool in the audit stack.

- **Organic Rese arch** — position distribution (top 3 / 4-1 0 / 11-100), top pages, historical trend, bra nded vs non-branded. Precision: +-40%, use as  trend
- **Keyword Gap** — Missing (biggest  opportunity), Weak (improve position), Untap ped (validate demand). Intents: Informational , Navigational, Commercial, Transactional
- * *Backlink Gap** — domains linking to compet itors but not the client. Filter by Authority  Score >30
- **Site Audit** — basic crawler . In the audit flow, Screaming Frog is the ma in crawler. Semrush Site Audit as secondary c heck
- **Traffic Analytics** — total traffi c estimation (not just organic). Useful for c hannel comparison with competitors. Do not us e as real figures
- **Authority Score** — p roprietary metric, not PageRank. Range table.  Use as comparative reference, not as a targe t
- **SE Ranking vs Semrush** — SE Ranking  for precise tracking of defined keywords, Sem rush for full domain discovery. Flow: Semrush  discovers, SE Ranking tracks
- **Why positio ns differ** — measurement date, datacenter,  request location
- Useful exports, limitatio ns to communicate to the client

---

### Tec hnical — robots.txt + Indexability

**File: ** `skills/robots-txt/SKILL.md`

Full technic al specification and templates by site type,  with focus on Google Merchant Center. Include s meta robots and X-Robots-Tag indexability c ontrol.

- **Google specification** — Allow /Disallow precedence (longest rule wins), use r-agent matching (specific does not inherit f rom `*`), `*` and `$` wildcards, AdsBot outsi de the `*` wildcard
- **Merchant Center** —  MC error table and its cause in robots.txt,  official solution (Googlebot + Googlebot-imag e with empty `Disallow:`), `*` block directiv es that cause disapprovals
- **Templates** � � informational site/blog, e-commerce without  MC, e-commerce with MC (with "what NOT to in clude" section)
- **AI governance** — table  of training bots (block) vs AI search bots ( allow). Difference between GPTBot and ChatGPT -User
- **Indexability** — meta robots dire ctives (noindex, nofollow, noarchive, noimage index), X-Robots-Tag HTTP header, LiteSpeed C ache noindex bug, Disallow vs noindex conflic t resolution
- **GSC coverage report** — in dexability states interpretation, "Google cho se different canonical", noindex on pages tha t should be indexed
- **Screaming Frog** —  Indexability column, Non-Indexable filter, UR Ls in Sitemap Non-Indexable
- **WordPress** � �� how to edit: SEO plugin, physical file, PH P hook
- Evaluation checklist by criticality  (critical / high / medium / low)

---

### Te chnical — Canonical Tags

**File:** `skills /canonical/SKILL.md`

Canonical tag implement ation, auditing, and CMS-specific bugs.

- ** Fundamentals** — when to use canonical vs 3 01, mandatory rules (absolute URL, one per pa ge, self-reference, sitemap/hreflang coherenc e)
- **Pagination** — self-referencing cano nical on page 2+, why canonical to page 1 rem oves paginated pages from the index
- **URL p arameters** — tracking/UTM parameters, WooC ommerce faceted navigation, PrestaShop LayerN avigation
- **WordPress** — Yoast (relative  canonical bug in subdirectory), Rank Math +  Elementor duplicate canonical bug
- **WooComm erce** — products in multiple categories (p rimary category required), variation URLs, tr ansactional endpoint canonicals
- **PrestaSho p** — URL with numeric ID, LayerNavigation  facet URLs, `PS_CANONICAL_REDIRECT` and `PS_L AYERED_FULL_TREE`
- **Canonical chains** —  how chains form, PageRank deprecation per hop , fix via direct canonical to final URL
- **J avaScript rendering** — canonical injected  by JS vs static HTML, GSC URL Inspection to v erify rendered canonical
- **Common errors**  — canonical to redirect, canonical to 404,  canonical to noindex, multiple canonicals, re lative canonical
- **GSC signals** — "Dupli cate without user-selected canonical", "Googl e chose different canonical"
- Audit checklis t by criticality

---

### Technical — Redi rects

**File:** `skills/redirects/SKILL.md`
 
301/302 redirect implementation, chains, loo ps, and migration planning.

- **Redirect typ es** — 301/302/307/308 comparison table wit h PageRank transmission and correct use cases 
- **Redirect chains** — how they form (mig rations, HTTP→HTTPS, multiple rebrands), cr awl budget impact, fix
- **Redirect loops** � �� causes (bad .htaccess rules, bidirectional  migration), detection with curl, fix
- **Wor dPress** — Redirection plugin (limitations  vs server-level), .htaccess RewriteRule patte rns, Nginx `return 301`, multisite subdirecto ry handling
- **PrestaShop** — Tráfico > R edirecciones SEO & URLs, Friendly URLs activa tion, category/product URL mapping from datab ase
- **PageRank transmission** — 301 trans mits ~99% (2016 update), 302 not guaranteed,  chain impact on crawl budget not on PageRank
 - **Migration checklist** — pre-migration c rawl, URL mapping priorities (by inlinks), im plementation, link update, sitemap update, GS C Change of Address
- **Crawl budget** — GS C crawl stats high redirect %, Screaming Frog  All Inlinks to Redirects report
- **Special  cases** — HTTPS+www in one hop vs two, soft  404 vs redirect, redirect to homepage as wea k fallback
- Audit checklist by criticality

 ---

### Technical — On-Page Fundamentals

 **File:** `skills/on-page-fundamentals/SKILL. md`

Title tags, meta descriptions, and H1: o ptimization rules, common errors, and audit w orkflow.

- **Title tag** — length (50-60 c hars), structure by page type (homepage/categ ory/product/article/local), Google rewrite ca uses, keyword stuffing
- **Meta description**  — length (140-155 chars), when Google igno res it, structure by page type, why absence i s not always bad
- **H1** — one per page ru le, H1 ≠ title tag relationship, hierarchy  structure, H1 in theme header on all pages
-  **CMS bugs** — Divi H1 not auto-generated,  Elementor H1 conflict with theme, WP Rocket +  Elementor template H1 duplication
- **WooCom merce** — product title template without pu rchase keyword, PrestaShop category meta titl e defaulting to category name
- **Cannibaliza tion** — GSC query appearing across two URL s, detection in Screaming Frog, fix options ( differentiate vs consolidate)
- **Screaming F rog** — missing/duplicate/overlength titles , missing/duplicate meta descriptions, missin g/multiple H1
- **GSC CTR analysis** — page s with >100 impressions and CTR <2% in positi on 1-5 as title optimization candidates
- Aud it checklist by criticality

---

### Technic al — Sitemap XML

**File:** `skills/sitemap /SKILL.md`

Technical audit knowledge for XML  sitemaps, covering discovery, structural val idation, URL quality, and live sampling.

- * *Discovery** — robots.txt `Sitemap:` direct ive first, standard path fallback (`/sitemap_ index.xml`, `/sitemap.xml`, PrestaShop `/1_in dex_sitemap.xml`)
- **Critical blockers** —  X-Robots-Tag noindex on the sitemap (HTTP 20 0 but unprocessable), HTTP status != 200, XML  parse errors. Fixes for LiteSpeed Cache, Apa che, Nginx
- **Sitemap index** — sub-sitema ps returning 404, empty sub-sitemaps, authors  sub-sitemap (thin content)
- **URL quality**  — HTTP/HTTPS mixing, www/non-www inconsist ency, trailing slash inconsistency, uppercase  paths, UTM/tracking parameters, staging URLs , cross-domain URLs, robots.txt Disallow conf licts
- **lastmod integrity** — presence ra te, `1970-01-01` Rank Math bug, invalid forma t, future dates, all-identical dates (static  generation), all very old dates
- **Sampling* * — live checks for broken URLs, redirects  (>20%), noindex pages in sitemap, canonical m ismatch, slow response times (crawl budget im pact)
- **CMS patterns** — WordPress/Yoast,  WordPress/Rank Math (documented bugs), WordP ress/WooCommerce (`/my-account/`, product var iations, out-of-stock, product tags, endpoint s), PrestaShop default path, Shopify limitati ons, Magento
- Audit checklist by criticality  (critical / high / medium / low) + common po sitives

---

### Technical — Hreflang

**F ile:** `skills/hreflang/SKILL.md`

Hreflang i mplementation and auditing for multilingual o r multi-regional WordPress sites.

- **Fundam entals** — when to implement, when not to,  mandatory syntax, reciprocity rule and self-r eference
- **WPML** — configuration, indexa ble test page issue, conflict with page build ers
- **TranslatePress** — duplicate hrefla ng conflict with Yoast. Solution: disable in  one of the two
- **Yoast + independent instal lations** — incorrect WebSite schema @id in  subdirectory. PHP snippet fix
- **HFCM (manu al implementation)** — when to use instead  of a global plugin. Per-page setup
- **Hrefla ng Manager Lite** — global mode risk with p artial translation: generates massive broken  reciprocity
- **Common errors** — broken re ciprocity, URLs with 404/redirect, incorrect  language code, missing x-default, duplicate h reflang
- **Validation** — Screaming Frog H reflang tab (noreturn, incorrect code, non-ca nonical), GSC > International, manual JS veri fication snippet
- **Single-language multi-re gion** — es-ES / es-MX / es-AR structure, x -default placement, canonical per region, Wor dPress implementation options
- Checklist by  criticality (critical / high / medium / low)
 
---

### Technical — Schema Markup

**File :** `skills/schema-markup/SKILL.md`

JSON-LD  structured data implementation, validation, a nd E-E-A-T signals.

- **Type selection** —  by page type: Organization/LocalBusiness, Ar ticle, FAQPage, BreadcrumbList, Product+Offer , MedicalWebPage, AggregateRating
- **Documen ted bugs** — Rank Math `datePublished=1970- 01-01`, Rank Math lowercase `@type`, logo < 1 12×112px, `relevantSpecialty`/`specialty` wi th text or wrong enum URL (`PhysicalTherapy`  is a business @type, not a MedicalSpecialty v alue — correct: `Physiotherapy`), `sameAs`  with dead URLs (Google+), duplicate `@id` in  subdirectory Yoast installations
- **FAQPage* * — rich results restricted to gov/health s ince 2023, but still valuable for semantic un derstanding, Bing, and AI extraction (ChatGPT , Perplexity, AI Overviews)
- **E-E-A-T** —  author schema with `jobTitle`, `description` , consistent `@id` across Article and Person  pages; embedded Person schema (no `@id`) when  author archive page does not yet exist
- **C MS implementation** — Yoast, Rank Math, Woo Commerce, PrestaShop; output buffer fix patte rn deployable via functions.php, Code Snippet s plugin, HFCM, or must-use plugin
- **Valida tion workflow** — validator.schema.org vs R ich Results Test vs GSC Enhancements (differe nt tools, different purposes)
- **MedicalWebP age** — does not generate GSC enhancement r eport; value is semantic, E-E-A-T, and AI ext raction
- Audit checklist by criticality

--- 

### AI / GEO — Generative Engine Optimiza tion

**File:** `skills/geo-ai-discoverabilit y/SKILL.md`

Optimize for citation by AI assi stants (Google AI Overviews, ChatGPT, Perplex ity, Bing Copilot).

- **AI crawler access**  — robots.txt rules for GPTBot, OAI-SearchBo t, PerplexityBot, Google-Extended, Anthropic- AI; decision logic for training vs citation a ccess
- **llms.txt** — file structure, impl ementation for WordPress and static sites, li nking from robots.txt
- **Wikidata entity** � �� minimum viable entity for brand/publicatio n authority, required statements, linking to  Organization schema via `sameAs`
- **NewsMedi aOrganization schema** — `publishingPrincip les`, `masthead`, `description`, ISSN for pub lications
- **Passage-level citability** —  answer-first structure, named statistics form at, anti-patterns that reduce AI extraction
-  **E-E-A-T for AI** — author `jobTitle` + ` description` as primary authority signals, ab out/masthead requirements
- **Platform-specif ic** — Google AI Overviews (organic ranking  matters), Perplexity (authorship + dates), C hatGPT/SearchGPT (Bing index + OAI-SearchBot) , Bing Copilot (FAQ schema weighted)
- **Wiki pedia** — notability threshold, approach, W ikidata link
- **Citation monitoring** — ma nual spot-check method, DataForSEO LLM mentio ns API
- Audit checklist by criticality

---
 
### Performance — Core Web Vitals

**File: ** `skills/core-web-vitals/SKILL.md`

LCP, CL S, INP, and TTFB diagnosis and optimization a cross CMS platforms.

- **Field vs lab data**  — CrUX vs Lighthouse, when each is authori tative, minimum traffic threshold for CrUX da ta
- **LCP diagnostic tree** — LCP element  identification, lazy-loaded hero image, fetch priority placement, preload hints, format and  file size
- **CLS causes and fixes** — mis sing image dimensions, web font FOUT, dynamic  content injection, Elementor lazy background  shift, cookie banners
- **INP** — long tas ks, third-party script competition, DOM size,  forced reflows. Replaced FID in March 2024
-  **TTFB** — relationship to LCP, OPcache, p age cache, CDN for HTML
- **CMS-specific** � � Divi (inline CSS, background hero), Element or (lazy LCP, WP Rocket conflict, DOM size),  PrestaShop (Cache-Control: no-store, CCC), Sh opify (app scripts)
- Measurement tools (PSI,  CrUX, DevTools, WebPageTest) and audit check list

---

### Performance — Cache Headers
 
**File:** `skills/cache-headers/SKILL.md`

C ache-Control strategy, CDN configuration, and  CMS-specific caching setup.

- **Cache-Contr ol directives** — `max-age`, `s-maxage`, `n o-cache`, `no-store`, `immutable`, `stale-whi le-revalidate` with use cases per content typ e
- **Cache layers architecture** — browser  cache → CDN → reverse proxy → page cac he → object cache → OPcache → database
 - **ETag and Last-Modified** — validation m echanics, Googlebot crawl budget impact, mult i-server inode ETag problem
- **WordPress** � �� WP Rocket (cache exclusions for WooCommerc e), LiteSpeed Cache (X-Robots-Tag bug on XML) , Redis object cache
- **PrestaShop** — CCC  options table, Smarty cache, Varnish and ful l-page cache options
- **Nginx** — FastCGI  page cache snippet, static asset cache header s, cache bypass for logged-in users
- **CDN**  — what CDNs cache by default (assets yes,  HTML no), Cloudflare "Cache Everything" rule,  cache invalidation strategies
- Diagnosing c ache issues with curl and response headers

- --

### Performance — Image Optimization

* *File:** `skills/image-optimization/SKILL.md` 

Format selection, responsive images, LCP ha ndling, and CMS-specific optimization.

- **F ormat selection** — WebP vs AVIF vs JPEG/PN G comparison, file size targets by image type 
- **Responsive images** — `srcset`, `sizes ` attribute explanation, what happens when `s izes` is missing
- **LCP images** — never l azy-load, `fetchpriority="high"`, `<link rel= "preload">` in `<head>`, only one `fetchprior ity` per page
- **Lazy loading** — when to  use and when not to. Elementor and WP Rocket  lazy-loading paradox on hero images
- **alt t ext** — content vs decorative images, keywo rd-stuffing pitfalls, WooCommerce product alt 
- **CLS prevention** — explicit `width` +  `height`, `aspect-ratio` CSS alternative
- ** CSS background-image vs `<img>`** — preload  scanner visibility, when each is appropriate 
- **CMS specifics** — WordPress (ShortPixe l, Smush, attachment page noindex), PrestaSho p (thumbnail regeneration), WooCommerce galle ry

---

### Security — SSL/HTTPS

**File:* * `skills/ssl-https/SKILL.md`

Certificate ma nagement, mixed content, HTTPS migration, and  security headers.

- **Certificate types** � �� DV, OV, EV, wildcard, SAN. Let's Encrypt a uto-renewal
- **HTTPS redirect** — correct  single-hop chain, redirect loops, WordPress a nd Nginx configuration
- **Mixed content** � � active (blocked) vs passive (warning), dete ction via DevTools and Screaming Frog, WordPr ess database search-replace, PrestaShop `ps_c onfiguration` table
- **HSTS** — directives , preload list requirements, risks of `includ eSubDomains` with non-HTTPS subdomains
- **Se curity headers** — HSTS, X-Frame-Options, X -Content-Type-Options, Referrer-Policy, Permi ssions-Policy, X-Powered-By removal
- **HTTPS  migration checklist** — pre-migration, red irects, mixed content, WordPress config, GSC,  monitoring

---

### Performance — Third-P arty Scripts

**File:** `skills/third-party-s cripts/SKILL.md`

Script loading strategies,  CWV impact by vendor, GTM optimization, and s cript auditing.

- **Loading strategies** —  `async` vs `defer` vs blocking, dynamic impo rt for interaction-triggered scripts
- **CWV  impact by vendor** — analytics (GA4, Matomo ), advertising (Meta Pixel, Hotjar, Clarity),  chat widgets, fonts (Google Fonts self-hosti ng), maps (facade pattern), video embeds
- ** Facade pattern** — lazy-load maps and YouTu be players on user interaction
- **GTM tag au dit** — identifying unused tags, trigger op timization (DOM Ready vs Window Loaded), tag  sequencing
- **Auditing third-party footprint ** — Chrome DevTools Coverage tab, PSI "Red uce third-party code", Screaming Frog source  code extraction
- Audit checklist by impact l evel

---

## Installation

### Plugin instal l (Claude Code 1.0.33+)

```
/plugin install  seo-audit-skills@uhartharper-seo-audit-skills 
```

### Manual install — Unix / macOS / L inux

```bash
git clone --depth 1 https://git hub.com/uhartharper/seo-audit-skills.git
bash  seo-audit-skills/install.sh
```

### Manual  install — Windows (PowerShell)

```powershe ll
git clone --depth 1 https://github.com/uha rtharper/seo-audit-skills.git
powershell -Exe cutionPolicy Bypass -File seo-audit-skills\in stall.ps1
```

All scripts copy each `skills/ */SKILL.md` to `~/.claude/skills/[name]/SKILL .md`.
Running them again updates existing ski lls.

## Works well with

Works standalone. F or broader SEO coverage (AI search optimizati on, local SEO, programmatic SEO), combine wit h [claude-seo](https://github.com/AgriciDanie l/claude-seo).

## Privacy

All knowledge is  anonymized. No client names, domains, or iden tifying data.
GDPR compliant.

## Contributin g

Enrich the skills with real patterns as ne w issues appear.
Rule: knowledge is added ano nymized — the pattern matters, not the sour ce.
 