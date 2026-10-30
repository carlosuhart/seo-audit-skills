---
name: semrush
description: >
  Semrush en auditorías: Organic Research, Keyword y Backlink Gap, Site Audit, Traffic
  Analytics y Position Tracking, con cruce con otras fuentes y fiabilidad de cada dato.
user-invokable: false
---

# Semrush — Knowledge Base

## Menú lateral verificado (2026-08-24)

```
Dashboard
Site Performance
Site Audit
Position Tracking
Competitive Analysis
  Domain Overview
  Organic Rankings
  Top Pages
  Compare Domains
  Keyword Gap
  Backlink Gap
Keyword Research
  Keyword Overview
  Keyword Magic Tool
  Keyword Strategy Builder
  Content Ideas
  SEO Writing Assistant
  Topic Research
Link Building
  Backlinks
  Referring Domains
  Backlink Audit
Extras
  Sensor
  SEOquake
  Semrush Rank
Other
  On Page SEO Checker
  Organic Traffic Insights
```

Dashboard/Site Performance/Site Audit/Position Tracking son herramientas de **Project** (requieren un proyecto ya creado para el dominio). El resto son secciones globales, no dependen de un proyecto.

## Rol en el flujo de auditoría

Semrush complementa SE Ranking y Screaming Frog con:
- Visión del dominio completo (no solo keywords rastreadas manualmente)
- Competitive intelligence: keywords de competidores, backlinks, comparativa de dominios
- Estimación de autoridad de dominio (Authority Score)
- Backlink profile inicial antes de usar herramientas especializadas
- Keyword research con intención de búsqueda clasificada

**No usar Semrush como fuente única para:** posiciones exactas (usar SE Ranking), estado técnico de páginas (usar SF), tráfico real (usar GA4/GSC).

---

## Organic Research

Ruta: **Competitive Analysis → Domain Overview** (resumen) o **Competitive Analysis → Organic Rankings** (listado de keywords). Nomenclatura verificada 2026-08-24 — el menú de Semrush ya no usa "SEO Toolkit"/"Organic Research" como sección, esos reports viven dentro de **Competitive Analysis**.

### Qué muestra

- Keywords orgánicas estimadas en top 100
- Tráfico orgánico estimado (mensual)
- Authority Score del dominio
- Distribución de posiciones (top 3, 4-10, 11-20, 21-50, 51-100)
- Páginas top rankeadas

### Cómo usar en auditoría

1. **Distribución de posiciones** → Si >60% de keywords están en posiciones 21-100, el sitio tiene potencial pero necesita mejoras de contenido/autoridad para subir.
2. **Top páginas** → Las páginas que más tráfico orgánico reciben. Cruzar con GA4 para confirmar. Son las páginas prioritarias en la auditoría.
3. **Tendencia histórica** → Gráfico de tráfico estimado en el tiempo. Cruza con Google Updates para detectar correlaciones.
4. **Branded vs non-branded** → Filtrar keywords que contienen el nombre del cliente vs las que no. Un sitio dependiente de tráfico branded es vulnerable.

### Precisión de los datos de Semrush

| Métrica | Precisión | Notas |
|---|---|---|
| Tráfico estimado | Baja-media (±40%) | Solo referencial, comparativa vs competidores |
| Posiciones | Media | Puede diferir de SE Ranking por fecha de extracción |
| Keywords totales | Media | Semrush indexa un subconjunto de SERPs |
| Authority Score | Referencial | No es PageRank; algoritmo propio de Semrush |

---

## Keyword Gap (competitor analysis)

Ruta: **Competitive Analysis → Keyword Gap** > introducir dominio cliente + hasta 4 dominios competidores en la vista Venn (se pueden cambiar los 4 y re-comparar sin límite ni proyecto nuevo)

### Filtros más útiles para identificar oportunidades

- **Missing**: keywords donde los competidores rankean pero el cliente NO aparece en top 100. Mayor oportunidad.
- **Weak**: keywords donde el cliente rankea pero en posición muy inferior a los competidores. Oportunidad de mejora.
- **Untapped**: keywords donde al menos 2 competidores rankean pero el cliente no. Valida demanda antes de crear contenido.

### Flujo recomendado

1. Exportar "Missing" filtrado por volumen > X (ajustar según nicho) y KD < 50.
2. Agrupar por intent con la columna "Intent" de Semrush.
3. Verificar post-sitemap.xml del cliente para descartar canibalización de intent antes de proponer contenido nuevo.
4. Priorizar los que tienen intent Transaccional o Comercial si el cliente busca conversiones.

### Intents en Semrush

| Intent | Icono | Qué significa |
|---|---|---|
| Informational | I | El usuario busca información |
| Navigational | N | El usuario busca una marca/sitio específico |
| Commercial | C | El usuario está investigando para comprar |
| Transactional | T | El usuario quiere completar una acción (compra, registro) |

---

## Backlink Gap

Ruta: **Competitive Analysis → Backlink Gap** (no está en la sección Link Building — verificado 2026-08-24)

Compara el perfil de backlinks del cliente vs competidores para identificar dominios que enlazan a los competidores pero no al cliente.

### Cómo usar

1. Exportar dominios que enlazan a 2+ competidores pero no al cliente.
2. Filtrar por Authority Score > 30 (dominios con cierta relevancia).
3. Evaluar si son oportunidades reales de link building o solo directorios/spam.

**Nota:** Para análisis profundo de backlinks, las herramientas especializadas (Ahrefs, Moz, o la skill `seo-backlinks`) son más precisas. Semrush Backlink Gap es útil para una primera vista comparativa rápida.

---

## Site Audit de Semrush

### Posición en el flujo

Semrush Site Audit es un crawler básico. En el flujo de auditoría:
- SF es el crawler principal (más datos, más configuración)
- Semrush Site Audit es un check secundario o para clientes sin licencia de SF

### Diferencias con Screaming Frog

| Funcionalidad | Semrush Site Audit | Screaming Frog |
|---|---|---|
| JS Rendering | Limitado | Completo (modo dedicado) |
| Velocidad | Más lento (servidor remoto) | Más rápido (local) |
| Datos on-page | Básicos | Muy detallados |
| Integración GSC/GA4 | Sí | Sí |
| Custom extraction | No | Sí (regex) |
| Core Web Vitals | Sí (via API) | Sí (via PSI API) |
| Crawl budget analysis | Básico | Avanzado |

### Issues de Site Audit: falsos positivos frecuentes

Los mismos que Screaming Frog en modo Spider (ver skill `screaming-frog` > sección Falsos
Positivos), más estos, verificados en vivo en auditorías reales:

| Issue de Semrush | Por qué suele ser falso | Cómo confirmarlo |
|---|---|---|
| Invalid robots.txt | Directivas válidas que Semrush no reconoce (`Content-Signal`, `License`) | Validar con el probador de GSC |
| Broken external links 429 / 403 | `wa.me`, LinkedIn y varios medios devuelven 429/403 a HEAD o a bots y 200 en GET desde navegador | `curl` con GET y UA de navegador |
| Blocked / noindex | Noindex deliberado (login, registro, páginas de filtro) | Revisar la intención con el cliente |
| Low text to HTML ratio | Frameworks JS (Next.js, Astro) inflan el HTML con el payload de hidratación | Contar palabras visibles: páginas con miles de palabras salen con ratio 0,02 |
| HTTPS "Not implemented" | El proyecto quedó configurado con `scheme: http` | `siteaudit/info`; corregir el proyecto, no el sitio |
| International SEO "Not implemented" / hreflang 0 | Metadata en el `<body>` (Next.js 15.2+ con metadata en streaming): Semrush ignora el hreflang fuera del `<head>` | Ver skill `javascript-seo` |
| Hreflang language mismatch | Página de ~40 palabras con el formulario renderizado solo en cliente, o listados de nombres propios | Leer el HTML del servidor |
| Http homepage sin 301 | Responde 308, que es equivalente | `curl -I` |
| Link text "Learn more" sin descripción | La tarjeta también enlaza con el nombre del producto y el botón lleva `aria-label` descriptivo | Inspeccionar el DOM |
| Structured data: SoftwareApplication sin `aggregateRating`/`offers` | Decisión correcta de no fabricar reseñas ni precios | Documentar la decisión |
| Incorrect pages in sitemap + hreflang mismatch masivos tras activar JS | El sitio redirige por IP en el cliente y el bot rastrea desde EE. UU. (lo manda al idioma inglés) | Ver skill `hreflang`, error de redirección por IP |

### Revisar errores, warnings y notices de todos los proyectos

Procesar solo los warnings, o solo el proyecto principal, deja fuera problemas reales: en una
auditoría con varios dominios, los errores de los dominios secundarios escondían dos hallazgos
nuevos (un logo roto y title/meta duplicados). Protocolo por proyecto:

1. `siteaudit/info` → recorrer `errors`, `warnings` y `notices` con count > 0.
2. Para cada issue, sus URL (`snapshot/{snapshot_id}/issue/{issue_id}`).
3. Verificar cada una en vivo y clasificar: real nuevo / ya cubierto por una corrección pedida /
   falso positivo.
4. `new_count` > 0 con `delta` 0 es rotación de URLs, no aumento.

### Site Audit por API REST — trampas verificadas

La API REST con API key funciona aunque el MCP de Semrush esté sin autenticar.

- Endpoints útiles: `reports/v1/projects/{id}/siteaudit/info` (configuración + `current_snapshot`
  con errores/warnings/notices, `delta` y `new_count`), `meta/issues` (nombres de cada issue),
  `siteaudit/history?limit=1` (último snapshot), `snapshot/{sid}/issue/{iid}` (URL afectadas),
  `siteaudit/launch` (relanzar).
- **`management/v1/projects/{id}/siteaudit/save` sobrescribe toda la configuración.** Leer antes
  `siteaudit/info` y reenviar todos los campos; guardar un respaldo del JSON previo.
- `save` exige `pageLimit` en camelCase (con `pages_limit` responde 400 "pageLimit must not be null").
  Body que funciona: `domain` (sin protocolo; con protocolo da 400 RFC 1035), `pageLimit`,
  `userAgentType`, `scheduleDay`, `crawlSubdomains`, `respectCrawlDelay`, `scheme` (campo no
  documentado, `"https"`), `crawlSourceType`, `crawlSourceUrl`, `notify`, `allow`, `disallow`,
  `removedParameters`, `jsRendering`.
- **Con `crawlSourceType` = sitemap, si el save no envía `crawlSourceUrl` queda en null:** el
  rastreo programado se salta sin registrar fallo (`last_failed_audit` sigue en 0) y `launch`
  devuelve 500 "Internal Server Error". Se arregla reenviando la URL del sitemap.
- `jsRendering: RENDER_ALL` cambia los resultados en sitios JS: desaparecen falsos "Missing h1"
  y aparecen problemas que antes no veía. Comparar el Site Health antes y después del cambio de
  configuración, no contra el rastreo anterior como si fuera evolución del sitio.

---

## Traffic Analytics

Ruta: Semrush > Traffic Analytics > dominio

Estimación de tráfico total (no solo orgánico) basada en clickstream data.

### Cuándo es útil

- Comparar tráfico estimado del cliente vs competidores (en términos relativos, no absolutos)
- Ver qué canales usa el competidor (Direct, Search, Social, Referral, Paid)
- Identificar si un competidor está invirtiendo fuertemente en Paid Search (señal para la estrategia)

### Cuándo NO usar

- Para reportar tráfico real del cliente → usar GA4
- Para tomar decisiones sobre keywords específicas → usar SE Ranking + GSC

---

## Position Tracking en Semrush vs SE Ranking

Si el cliente tiene SE Ranking configurado correctamente, no es necesario duplicar el tracking en Semrush.

**Usar Semrush Position Tracking solo para:**
- Comparativa directa con competidores en las mismas keywords (Share of Voice)
- Clientes sin SE Ranking aún configurado

### Por qué las posiciones difieren entre herramientas

- Diferente fecha/hora de medición
- Diferente localización de la solicitud (SF mide desde UK por defecto, SE Ranking desde España si está configurado así)
- Diferentes SERPs: Semrush puede medir desde datacenter distinto

---

## Authority Score

Métrica propia de Semrush. No equivale a PageRank de Google.

| AS | Interpretación general |
|---|---|
| < 20 | Dominio nuevo o sin backlinks relevantes |
| 20-40 | Autoridad baja-media, típico de PYMES locales |
| 40-60 | Autoridad media, sitios establecidos con backlinks |
| 60-80 | Autoridad alta, publishers o marcas con presencia nacional |
| > 80 | Dominios de referencia (Wikipedia, periódicos, etc.) |

**Usar como referencia comparativa**, no como objetivo absoluto. Lo importante es la tendencia (¿sube o baja?) y la posición relativa vs competidores directos.

---

## Exports útiles para informes

| Export | Ruta en Semrush | Uso |
|---|---|---|
| Organic keywords | Organic Research > Positions > Export | Base para análisis de visibilidad |
| Top pages | Organic Research > Pages > Export | Páginas prioritarias del cliente |
| Missing keywords | Keyword Gap > Missing > Export | Oportunidades de contenido |
| Referring domains | Backlink Analytics > Referring Domains | Perfil de backlinks |
| Competitor comparison | Traffic Analytics > Bulk Analysis | Comparativa de canales |

---

## Integración con otras herramientas del flujo

### Semrush + SE Ranking

- Semrush: visión completa del dominio, discovery de keywords no rastreadas
- SE Ranking: seguimiento preciso de keywords definidas, histórico de posiciones

Flujo: Semrush identifica keywords valiosas no rastreadas → añadir al proyecto de SE Ranking.

### Semrush + GSC

- Semrush tráfico estimado vs GSC clics reales: usar GSC como verdad
- Si Semrush estima mucho más tráfico que GSC muestra en clics → probable que haya keywords rankeando en imágenes, noticias u otros SERPs que no generan clics web

### Semrush + Screaming Frog

- Semrush identifica páginas con tráfico estimado
- SF audita esas páginas en profundidad
- Priorizar correcciones técnicas en páginas que Semrush marca con tráfico relevante

---

## Limitaciones a comunicar al cliente

- Las cifras de tráfico de Semrush son estimaciones, no datos reales.
- El Authority Score es una métrica de Semrush, no una señal directa de Google.
- Semrush puede no indexar todas las keywords de nicho — especialmente en nichos locales o en español con poco volumen.
- Los datos de backlinks pueden tener lag de varias semanas vs backlinks reales actuales.
