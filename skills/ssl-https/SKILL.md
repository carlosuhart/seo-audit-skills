---
name: ssl-https
description: >
  HTTPS and SSL/TLS audits: certificates, mixed content, HTTPS redirect chains, HSTS and
  security headers. Use for mixed content, HTTP URLs, certificate issues or HTTP to
  HTTPS migrations.
---

# SSL/HTTPS — Technical SEO

> HTTPS is a confirmed Google ranking signal since 2014. More importantly,
> mixed content blocks resource loading and can cause LCP failures.

---

## Certificate types

| Type | Validation | Issuance time | When to use |
|------|-----------|--------------|-------------|
| DV (Domain Validation) | Domain control only | Minutes | Blogs, informational sites |
| OV (Organization Validation) | Domain + organization | 1-3 days | Business sites |
| EV (Extended Validation) | Full legal verification | 1-7 days | Banks, e-commerce (less relevant today) |
| Wildcard (`*.domain.com`) | Covers all subdomains | Minutes–days | Sites with multiple subdomains |
| SAN (Subject Alternative Names) | Multiple domains in one cert | Minutes–days | Multi-domain hosting |

**Let's Encrypt:** Free DV certificate, auto-renewing, supported by most hosting
panels (cPanel, Plesk, Hostinger hPanel). Sufficient for most SEO client sites.

### Certificate expiration

An expired certificate causes:
- Browser security warnings that block all users
- Googlebot may stop crawling the site
- All Google rankings at risk of rapid drop due to inaccessibility

**Prevention:** Enable auto-renewal in the hosting panel. Most hosts renew
Let's Encrypt automatically. Verify auto-renewal is active, not just installed.

**Monitoring:** Set a calendar reminder 30 days before expiry, or use
uptime monitoring tools that alert on certificate expiry (UptimeRobot,
Better Uptime).

---

## HTTPS redirect — correct configuration

A site migrated to HTTPS must redirect all HTTP traffic to HTTPS with 301s.

### Correct redirect chain

```
http://domain.com/page/      → 301 → https://domain.com/page/   ✓
http://www.domain.com/page/  → 301 → https://domain.com/page/   ✓ (if non-www is canonical)
https://www.domain.com/page/ → 301 → https://domain.com/page/   ✓
```

### Redirect chain problems

**Too many redirects:**
```
http://domain.com/ → 301 → https://domain.com/ → 301 → https://www.domain.com/
```
Every redirect in the chain adds latency and dilutes link equity (historically).
Reduce to a single redirect hop.

**Redirect loop:**
```
http://domain.com/ → 301 → https://domain.com/ → 301 → http://domain.com/
```
Often caused by a server that redirects to HTTPS but an application that
redirects back to HTTP. Check WordPress `siteurl` setting and `.htaccess`.

### WordPress — enforce HTTPS

```apache
# .htaccess — redirect all HTTP to HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
```

Also verify in WordPress > Settings > General:
- WordPress Address (URL): `https://domain.com`
- Site Address (URL): `https://domain.com`

After changing to HTTPS in WordPress settings, regenerate the sitemap and
flush all caches.

### Nginx — enforce HTTPS

```nginx
server {
    listen 80;
    server_name domain.com www.domain.com;
    return 301 https://domain.com$request_uri;
}
```

---

## Mixed content

Mixed content occurs when an HTTPS page loads resources (images, scripts, CSS,
fonts, iframes) over HTTP. This is one of the most common post-migration issues.

### Types of mixed content

**Active mixed content (blocked by browsers):**
- HTTP scripts (`<script src="http://...">`)
- HTTP stylesheets (`<link href="http://...">`)
- HTTP iframes (`<iframe src="http://...">`)

Active mixed content is blocked by all modern browsers. The resource simply
does not load, which can break page functionality or cause LCP failures.

**Passive mixed content (warning in browser):**
- HTTP images (`<img src="http://...">`)
- HTTP video/audio

Passive mixed content loads but triggers a security warning in the browser address bar.
Google may treat HTTPS pages with mixed content as partially insecure.

### How to detect mixed content

**Browser DevTools:**
- Open the page in Chrome > F12 > Console tab
- Mixed content errors appear as "Mixed Content: The page ... was loaded over HTTPS
  but requested an insecure resource..."

**Screaming Frog:**
- Reports > Security Issues > Mixed Content
- Lists all URLs requested over HTTP from HTTPS pages

**curl check (useful for automated monitoring):**
```bash
# Check if a specific resource is served over HTTP
curl -si https://domain.com/ | grep -i "http://"
```

### Common mixed content sources

**WordPress database with old HTTP URLs:**
After migrating to HTTPS, the database still contains `http://` URLs in post content,
widget settings, theme options, and custom fields.

Fix: Search & Replace plugin (Better Search Replace) to update all `http://domain.com`
to `https://domain.com` in the WordPress database.

**Hard-coded HTTP in theme files:**
Some themes hard-code `http://` in PHP template files.
Fix: Search theme files for `http://` and replace with `https://` or `//` (protocol-relative).

**Third-party embeds:**
YouTube, Google Maps, and other embeds often auto-detect protocol.
If they do not, update the embed code manually.

**Plugins storing HTTP URLs in options table:**
Some plugins store their CDN or asset URLs as HTTP in the `wp_options` table.
Fix: update via Better Search Replace or WP-CLI:
```bash
wp search-replace 'http://domain.com' 'https://domain.com' --all-tables
```

**PrestaShop after HTTPS migration:**
PrestaShop stores domain and HTTP/HTTPS preference in `ps_configuration` table:
```sql
UPDATE ps_configuration
SET value = 'https://domain.com'
WHERE name IN ('PS_SHOP_DOMAIN', 'PS_SHOP_DOMAIN_SSL');

UPDATE ps_configuration
SET value = '1'
WHERE name = 'PS_SSL_ENABLED';
```

---

## HSTS — HTTP Strict Transport Security

HSTS instructs browsers to always connect to the domain over HTTPS, even if the
user types `http://` or follows an HTTP link. This eliminates the HTTP→HTTPS
redirect for returning users.

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

| Parameter | Meaning |
|-----------|---------|
| `max-age=31536000` | 1 year — browser remembers HTTPS-only for 1 year |
| `includeSubDomains` | Applies to all subdomains |
| `preload` | Required to be included in browser preload lists |

**HSTS preload list:** Browsers ship with a list of domains that are always HTTPS.
To be included: https://hstspreload.org
Requirements: 1-year max-age, includeSubDomains, preload directive, HTTPS-only site.

**Warning:** HSTS with `includeSubDomains` breaks any subdomain that does not
have a valid SSL certificate. Verify all subdomains are on HTTPS before enabling.

### Configurar HSTS en Cloudflare

Cloudflare → SSL/TLS → Edge Certificates → scroll hasta **HTTP Strict Transport Security (HSTS)** → Enable HSTS.

Configuración recomendada para primera activación:

| Campo | Valor recomendado |
|-------|------------------|
| Enable HSTS | On |
| Max Age | 6 months (15,552,000s) — empezar aquí, no con 1 año |
| Include Subdomains | Off — solo activar si todos los subdominios tienen HTTPS válido |
| Preload | Off — irreversible, requiere cumplir requisitos estrictos antes |
| No-Sniff Header | On |

**Por qué 6 meses y no 1 año:** si se desactiva HTTPS o se desconecta Cloudflare mientras
HSTS está activo, el sitio queda inaccesible para los navegadores que lo tienen cacheado
durante todo el max-age. 6 meses reduce el riesgo de bloqueo prolongado ante un error.

**Resultado esperado en headers:**
```
Strict-Transport-Security: max-age=15552000
```

---

## Security headers

Security headers are not direct ranking signals but they affect user trust, prevent
specific attack classes that can compromise SEO (XSS injecting spam links), and are
increasingly checked by security-conscious clients.

### Minimum recommended headers

```nginx
# Nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

```apache
# Apache / .htaccess
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

### Header reference

| Header | Purpose | Recommended value |
|--------|---------|------------------|
| `Strict-Transport-Security` | Enforce HTTPS | `max-age=31536000; includeSubDomains` |
| `X-Frame-Options` | Prevent clickjacking | `DENY` (or CSP `frame-ancestors 'none'`); `SAMEORIGIN` only with a confirmed need — see below |
| `X-Content-Type-Options` | Prevent MIME sniffing | `nosniff` |
| `Referrer-Policy` | Control referrer data | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Restrict browser features | Deny unused: `geolocation=(), microphone=()` |
| `Content-Security-Policy` | Prevent XSS | Complex — start in `report-only` mode |

### CSP baseline directives frequently missing

Even in an initial `Content-Security-Policy-Report-Only` rollout scoped to the site's
real scripts/styles/fonts/connections, two low-risk hardening directives are commonly
left out and should be added from the start unless there's a specific reason not to:

```
object-src 'none';
base-uri 'self';
```

`object-src 'none'` blocks legacy `<object>`/`<embed>`/`<applet>` plugin content —
almost no modern site legitimately needs this. `base-uri 'self'` prevents an injected
`<base>` tag from hijacking all relative URLs on the page. Neither typically breaks
functionality, unlike `script-src`/`style-src` restrictions which do need a real
inventory of the site's own inline scripts/styles before tightening.

Also confirm the policy actually reaches a reporting endpoint (`report-uri` or the
newer `report-to`) — without one, Report-Only violations only show up in whichever
browser console someone happens to have open, not systematically.

### `includeSubDomains` and `preload` on HSTS — audit subdomains first

Adding `includeSubDomains` to `Strict-Transport-Security` without first confirming
every active subdomain serves valid HTTPS can break subdomains that aren't HTTPS-ready.
`preload` is a further commitment (submission to browser preload lists is difficult to
reverse) — treat it as a separate decision made only after `includeSubDomains` has
been live and confirmed safe, not as one more parameter to add at the same time.
In a written fix this does not need its own gated phase: put `preload` in the same
header block with an explicit caution note next to it (see "Delivery format" below).

### Default values and wording that hold up in review

- **`frame-ancestors` / `X-Frame-Options`: start from `'none'` / `DENY`.** `'self'` /
  `SAMEORIGIN` is justified only by a confirmed need to frame the site. "Same origin" means the
  exact origin, not "another domain of the same company group": framing from a sister domain
  needs an explicit `frame-ancestors https://sister.example` allowlist, not `SAMEORIGIN`.
  The minimal snippets above use `SAMEORIGIN` because it never breaks anything; in a written
  recommendation, default to the restrictive value and relax it when a real use case appears.
- **`Cross-Origin-Opener-Policy: same-origin` can break OAuth, payment popups and cross-window
  integrations**, including ones opened by a third-party widget on a site with no visible login.
  Add a functional check of those flows to the validation.
- **A Report-Only period is evidence only if the reports land somewhere.** Before treating
  3-5 days of Report-Only as clearance to enforce, confirm the `report-uri` / `report-to`
  endpoint exists and stores reports. Otherwise the "monitoring" is fictitious.
- **Risk wording:** a missing header is not a confirmed vulnerability. Write "without CSP the
  site loses a mitigation layer against some XSS scenarios", not "the site is exposed to XSS".
  Overstating it is less precise, not more rigorous.
- **Delivery format that gets implemented:** one "new state" block with all headers together
  (HSTS with `includeSubDomains; preload` on the same line), and the cautions (audit subdomains
  before preload, verify the report endpoint, test OAuth/popups) as notes next to the block or
  as validation items — not as numbered phases each gated on the previous one. The only
  sequence worth keeping explicit: CSP always starts in Report-Only and is enforced only after
  a real monitoring period with no unexpected violations.
- **Security findings outside the SEO scope** (tokens in URLs, exposed panels, PII in analytics)
  are reported as informative items: what is visible and why it matters, never the values.

### CSP Report-Only in "learning mode" — HTTP 500/504 from oversized headers

Seen on several WordPress sites on shared hosting, with identical symptoms each time: the whole
domain returns 500 (or the origin hangs with 504 behind Cloudflare) on every route that runs PHP,
**nothing in `error_log`**, and restoring a backup does not help. The host, if it answers at all,
mentions "header size limit reached".

**Cause:** a security plugin with a CSP *learning mode* (e.g. Really Simple Security) writes the
policy into `wp-content/advanced-headers.php`, loaded on every request via `auto_prepend_file`
(from `.htaccess` / `.user.ini`) before WordPress boots. In learning mode the plugin keeps
appending every third-party domain it sees to `Content-Security-Policy-Report-Only`. On sites
with programmatic ads the list never stabilises: one case reached 11,850 characters and 388
ad-tech domains. Once the header exceeds the server limit, every response fails. Backups don't
help because the file was already bloated when they were taken.

**Diagnosis:**
```bash
# Size of the generated header file (over ~8 KB is a red flag)
ls -l wp-content/advanced-headers.php
grep -c "Report-Only" wp-content/advanced-headers.php
# Header size on a working response
curl -sI https://example.com/ | wc -c
```

**Fix:**
1. Remove the Report-Only line from `advanced-headers.php` (keep a dated backup). The site comes
   back immediately.
2. Turn learning mode off in the plugin (in Really Simple Security: Content Security Policy →
   exit learning mode → save), or the plugin will regenerate the line. Check afterwards that the
   plugin rewrote the *definitive* file: in one case it only regenerated
   `advanced-headers-test.php` and the line had to be removed by hand.
3. Uninstalling the plugin does **not** delete `advanced-headers.php` or the `auto_prepend_file`
   directive — remove both by hand.
4. Check every other site with the same plugin: same plugin + ad stack = same time bomb.

**False leads to avoid:** a WAF rule blocking requests to paths containing `advanced-headers`
does nothing (the file is included server-side, never requested over HTTP). The host naming the
file is not evidence of malware: read its contents before assuming a compromise. If 502/503/504
errors persist at a lower rate after the fix, check the database engine: MyISAM tables written
on every ad impression or click (ad plugins, analytics, Action Scheduler) cause lock contention
that looks like a capacity problem; converting them to InnoDB took the error rate in one case
from ~20% to ~4%.

### X-Powered-By exposure

`X-Powered-By: PHP/8.1` reveals the PHP version and can be used to target
known vulnerabilities.

Fix:
```ini
; php.ini
expose_php = Off
```
```nginx
; nginx.conf
fastcgi_hide_header X-Powered-By;
```

---

## HTTPS migration checklist

For sites migrating from HTTP to HTTPS (or post-migration audit):

```
PRE-MIGRATION
[ ] SSL certificate installed and valid
[ ] Auto-renewal configured
[ ] All subdomains have certificates (if using includeSubDomains)

REDIRECT CONFIGURATION
[ ] HTTP → HTTPS 301 redirect configured
[ ] www → non-www (or vice versa) redirect in same hop
[ ] No redirect chains longer than 1 hop to final HTTPS URL
[ ] Verify in browser and with curl -L http://domain.com/

MIXED CONTENT
[ ] WordPress database updated (http:// → https://) via Better Search Replace
[ ] Hard-coded HTTP in theme PHP files updated
[ ] Third-party embed codes updated
[ ] No mixed content errors in browser DevTools Console
[ ] Screaming Frog: Security Issues > Mixed Content = empty

CONFIGURATION
[ ] WordPress siteurl and home updated to https://
[ ] Sitemap regenerated (all URLs now https://)
[ ] robots.txt Sitemap directive uses https://
[ ] Canonical tags on all pages use https://

HSTS
[ ] HSTS header configured (after confirming HTTPS is stable)
[ ] Security headers configured

GSC AND INDEXATION
[ ] New https:// property added in Google Search Console
[ ] Sitemap submitted in https:// property
[ ] GSC coverage report monitored for errors post-migration
[ ] Internal links updated from http:// to https:// (or relative URLs)
[ ] Backlinks from external sites will follow 301 to HTTPS — acceptable

MONITORING
[ ] Certificate expiry alert set (30 days before expiry)
[ ] Uptime monitoring active for HTTPS URLs
```

---

## Audit checklist (ongoing)

```
CRITICAL
[ ] Valid SSL certificate (not expired)
[ ] HTTP redirects to HTTPS (301)
[ ] No active mixed content (blocked scripts/CSS/iframes over HTTP)
[ ] No redirect loops

HIGH
[ ] No redirect chain longer than 1 hop to final URL
[ ] HSTS header present
[ ] X-Powered-By header removed
[ ] Siteurl/home in WordPress uses https://

MEDIUM
[ ] Passive mixed content (HTTP images) resolved
[ ] Security headers: X-Frame-Options, X-Content-Type-Options, Referrer-Policy
[ ] HTTPS consistent in sitemap URLs
[ ] HTTPS consistent in canonical tags
[ ] Certificate auto-renewal active

LOW
[ ] HSTS preload list submission (optional but good for high-traffic sites)
[ ] Content-Security-Policy in report-only mode
[ ] Permissions-Policy header configured
[ ] SSL rating A or A+ on Qualys SSL Labs (ssllabs.com/ssltest/)
```
