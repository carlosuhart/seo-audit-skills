---
name: seo-quote
description: >
  Genera un informe de auditoría SEO en formato .docx para cotizaciones y propuestas comerciales.
  Recopila datos mínimos del sitio (volumen, stack, issues críticos), calcula horas de trabajo
  y genera un presupuesto en USD. Output: documento entregable al cliente.
  Invocar cuando el usuario pida "cotización SEO", "presupuesto SEO", "propuesta SEO", "informe de auditoría para cliente" o "/seo-quote".
user-invokable: true
argument-hint: "<url> [--rate <usd/h>] [--lang es|en]"
---

# SEO Quote Report Generator

Genera un informe-propuesta SEO en .docx listo para entregar a un cliente potencial.
No es una auditoría completa: es la exploración mínima suficiente para justificar un diagnóstico, definir un scope de trabajo y calcular un presupuesto creíble.

---

## Parámetros de entrada

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `<url>` | requerido | URL raíz del sitio a auditar |
| `--rate` | 60 | Tarifa hora en USD |
| `--lang` | es | Idioma del documento (es / en) |

---

## Fase 1: Recolección de datos mínimos

Ejecutar en este orden. Detener y reportar si una fuente falla; continuar con las demás.

### 1.1 Volumen del sitio (sitemap)

```
GET <url>/sitemap.xml
GET <url>/sitemap_index.xml   (si el anterior falla o es índice)
GET <url>/post-sitemap.xml    (WordPress)
GET <url>/page-sitemap.xml    (WordPress)
```

Extraer:
- Total de URLs indexadas (suma de todos los sitemaps)
- Desglose por tipo: posts, páginas, categorías, productos (si aplica)
- Fecha del lastmod más reciente y más antiguo (señal de frecuencia de publicación)

Si no hay sitemap: registrar como issue crítico y estimar volumen desde robots.txt o crawl de homepage.

### 1.2 Stack tecnológico (homepage)

WebFetch de `<url>` (homepage). Detectar:

- CMS (WordPress, PrestaShop, Shopify, Wix, custom)
- Plugin SEO activo (Rank Math, Yoast, AIOSEO, The SEO Framework, ninguno)
- Cache/CDN (LiteSpeed Cache, WP Rocket, Cloudflare, W3 Total Cache)
- Constructor de páginas (Divi, Elementor, Gutenberg, otro)
- Advertising (Advanced Ads, AdSense, Mediavine, etc.)
- Analytics/Tag Manager (GA4, GTM, Site Kit)

Señales de detección:
- `X-Powered-By`, `Server` headers
- Clases CSS: `elementor-`, `et_pb_`, `wp-block-`
- Paths: `/wp-content/`, `/wp-json/`, `/modules/`, `cdn.shopify.com`
- Meta generators

### 1.3 robots.txt

```
GET <url>/robots.txt
```

Verificar:
- Existe y es accesible
- Referencia al sitemap principal
- No bloquea recursos CSS/JS críticos ni el raíz `/`
- Reglas de AI crawlers presentes/ausentes (GPTBot, ClaudeBot, PerplexityBot)

### 1.4 Señales on-page homepage

Desde el WebFetch de 1.2, extraer:

- `<title>` tag (presente/ausente, longitud)
- `<meta name="description">` (presente/ausente, longitud)
- H1 (presente/ausente, texto)
- Canonical (apunta a sí mismo o a otra URL)
- `<meta name="robots">` si existe
- OG tags presentes (og:title, og:description, og:image)
- Schema JSON-LD: listar @types detectados

### 1.5 Core Web Vitals (DataForSEO o PageSpeed)

Si DataForSEO MCP disponible: `on_page_lighthouse` sobre la homepage.
Si no: WebFetch de `https://pagespeed.web.dev/report?url=<url>` para extraer scores visibles.

Registrar:
- Performance score (Lighthouse)
- LCP, INP/FID, CLS valores si visibles
- Mobile vs Desktop si hay diferencia notable

### 1.6 Autoridad de dominio (DataForSEO backlinks)

Si DataForSEO MCP disponible: `backlinks_summary` para el dominio raíz.

Extraer:
- Referring domains
- Backlinks total
- Rank (DataForSEO Rank o similar)

Si no disponible: omitir sección en el documento o indicar "datos pendientes de herramienta de backlinks".

---

## Fase 2: Clasificación de complejidad

Asignar el sitio a uno de tres tiers basándose en los datos recolectados.

### Tier A — Sitio pequeño / simple
- Menos de 100 URLs en sitemap
- CMS estándar (WordPress básico, Wix, Squarespace)
- Sin plugin SEO activo o configuración mínima
- Sin e-commerce
- Performance score ≥ 70 mobile

### Tier B — Sitio mediano / estándar
- 100–1.000 URLs
- WordPress con plugin SEO (Rank Math, Yoast)
- Page builder activo (Elementor, Divi)
- CDN/cache presente pero con posibles conflictos
- E-commerce pequeño (WooCommerce < 500 productos)
- Performance score 50–70 mobile

### Tier C — Sitio grande / complejo
- Más de 1.000 URLs
- Stack complejo (múltiples plugins de cache, ads, analytics, builders)
- E-commerce grande (>500 productos) o multiidioma (hreflang)
- Performance issues críticos (score < 50 mobile)
- Problemas de indexación detectados
- Presencia en múltiples mercados/idiomas

---

## Fase 3: Detección de issues

Catalogar cada issue encontrado en Fase 1 asignando:
- **Criticidad**: Crítico / Alto / Medio / Bajo
- **Descripción**: qué se detectó
- **Impacto SEO**: por qué importa (en una línea, lenguaje no técnico)
- **Horas estimadas de corrección**: ver tabla de horas

### Tabla de issues frecuentes y horas por tier

| Issue | Criticidad | Horas Tier A | Horas Tier B | Horas Tier C |
|-------|-----------|--------------|--------------|--------------|
| Sin sitemap XML | Crítico | 1 | 2 | 3 |
| robots.txt mal configurado | Crítico | 1 | 1 | 2 |
| Sin plugin SEO activo | Crítico | 2 | 3 | 5 |
| Sin schema markup | Alto | 2 | 4 | 8 |
| Meta descriptions ausentes/duplicadas (bulk) | Alto | 2 | 6 | 14 |
| Títulos fuera de rango o duplicados (bulk) | Alto | 2 | 6 | 14 |
| Sin H1 o H1 incorrecto (bulk) | Alto | 2 | 4 | 10 |
| Core Web Vitals en rojo (LCP/INP/CLS) | Alto | 4 | 8 | 16 |
| Sin HTTPS o mixed content | Crítico | 2 | 3 | 5 |
| Headers de seguridad ausentes | Medio | 1 | 2 | 3 |
| Redirect chains (3+ hops) | Alto | 2 | 4 | 8 |
| Páginas huérfanas significativas | Medio | 2 | 4 | 8 |
| Imágenes sin alt text (bulk) | Medio | 1 | 3 | 8 |
| Contenido delgado (< 300 palabras) en páginas clave | Alto | 3 | 8 | 20 |
| Sin canonical en páginas de listado/paginación | Medio | 1 | 2 | 4 |
| AI crawlers sin gestionar (robots.txt) | Bajo | 1 | 1 | 2 |
| Sin llms.txt (GEO/visibilidad en AI Search) | Bajo | 1 | 2 | 3 |
| E-E-A-T débil (sin autor, sin about, sin trust signals) | Alto | 3 | 6 | 10 |
| Hreflang ausente en sitio multiidioma | Crítico | 4 | 8 | 16 |

Para issues no listados: estimar horas con el criterio de complejidad del tier + factor de volumen de páginas afectadas.

---

## Fase 4: Plan de trabajo

Organizar las acciones en 3 fases temporales. Cada fase tiene un objetivo y un conjunto de acciones.

### Estructura del plan

**Fase 1 — Fundamentos técnicos (semanas 1–2)**
Acciones críticas y altas que bloquean el SEO base: sitemap, robots.txt, redirects, HTTPS, schema básico, plugin SEO configurado.
Sin esta fase, el resto del trabajo no tiene tracción.

**Fase 2 — Optimización on-page y contenido (semanas 3–6)**
Optimización de titles, meta descriptions, H1, imágenes. Mejora de contenido en páginas prioritarias (las que ya rankean o tienen potencial alto). Interlinking.

**Fase 3 — Autoridad y visibilidad AI (semanas 7–12)**
Link building, schema avanzado (FAQ, Article, Organization), GEO (llms.txt, AI crawler policy, structured data para AI citation), reporting mensual.

Ajustar el cronograma si el tier es A (compresión posible a 6 semanas) o C (extensión a 16–20 semanas).

---

## Fase 5: Cálculo de presupuesto

### Servicios contemplados

Construir una tabla de servicios con horas por servicio basándose en los issues detectados y el tier.

| Servicio | Descripción | Horas | Tarifa (USD/h) | Total (USD) |
|---------|-------------|-------|----------------|-------------|
| Auditoría SEO técnica inicial | Revisión completa del estado técnico | X | rate | $ |
| Configuración plugin SEO | Setup completo Rank Math / Yoast | X | rate | $ |
| Optimización on-page (bulk) | Titles, metas, H1 en N páginas prioritarias | X | rate | $ |
| Schema markup | Implementación tipos clave | X | rate | $ |
| Core Web Vitals | Diagnóstico y correcciones de performance | X | rate | $ |
| Optimización de contenido | Mejora de N artículos existentes | X | rate | $ |
| Interlinking | Análisis y ejecución de links internos | X | rate | $ |
| GEO / AI Search Visibility | llms.txt, AI crawlers, structured data GEO | X | rate | $ |
| Seguimiento mensual | Reporting + ajustes + monitorización | X | rate | $ |

Solo incluir los servicios pertinentes para los issues detectados. No inflar con servicios que no aplican.

### Cálculo de horas por volumen de sitio

Para optimizaciones bulk (titles, metas, contenido), usar esta escala:
- 1–50 páginas: horas base del issue
- 51–200 páginas: horas base × 2,5
- 201–500 páginas: horas base × 5
- 501–1.000 páginas: horas base × 8
- >1.000 páginas: horas base × 12 + evaluar automatización/scripting (descuento 30% si se aplica scripting)

### Totales

- **Total horas proyecto**: suma
- **Total presupuesto (USD)**: horas × tarifa
- **Opción mantenimiento mensual**: horas mensuales × tarifa
- **Forma de pago sugerida**: 50% inicio / 50% entrega (one-time) o mensual (mantenimiento)

Usar formato numérico europeo en el documento: punto para miles, coma para decimales.
En código Python interno usar float estándar; solo formatear al escribir el documento.

---

## Fase 6: Generación del documento .docx

Generar un script Python con python-docx y ejecutarlo. Guardar en `<directorio-de-auditorias>/<cliente>/cotizacion-seo-<slug-dominio>-<YYYY-MM-DD>.docx`.

Crear el directorio si no existe.

### Estructura del documento

```
1. Portada
   - Título: "Diagnóstico SEO y Propuesta de Trabajo"
   - Subtítulo: <nombre del sitio> | <fecha>
   - Preparado para: [nombre cliente si disponible]
   - Preparado por: Zythos Media

2. Resumen ejecutivo (1 página)
   - Estado actual: tier + score resumen
   - Issues críticos detectados: N (lista breve)
   - Oportunidad estimada: descripción cualitativa del potencial
   - Inversión total: USD X.XXX

3. Situación actual del sitio
   3.1 Datos generales
       - URL, CMS, stack tecnológico
       - Volumen: N URLs indexadas (posts, páginas, otros)
       - Frecuencia de publicación (estimada)
       - Autoridad de dominio (si disponible)
   3.2 Core Web Vitals
       - Tabla LCP / INP / CLS + valoración pass/warn/fail
   3.3 Visibilidad en búsqueda (si hay datos GSC disponibles)

4. Problemas detectados
   Tabla con columnas: Prioridad | Problema | Impacto | Solución propuesta
   Ordenar de Crítico a Bajo.
   Lenguaje orientado al cliente, no técnico.

5. Plan de trabajo
   5.1 Fase 1 — Fundamentos técnicos
   5.2 Fase 2 — Optimización on-page y contenido
   5.3 Fase 3 — Autoridad y visibilidad AI
   Cada fase: objetivo, acciones, entregables esperados.

6. Cronograma
   Tabla: Fase | Actividad | Semanas | Responsable

7. Presupuesto
   Tabla de servicios con horas y costes.
   Totales bien delimitados.
   Nota de condiciones de pago.

8. Próximos pasos
   3 bullets claros: qué debe hacer el cliente para arrancar.
```

### Estilos del documento

- Fuente cuerpo: Calibri 11
- Fuente títulos: Calibri 14 (sección), 12 (subsección), bold
- Tabla issues: header fila oscura (#1F4E79), texto blanco; filas alternas blancas y #D6E4F0
- Tabla presupuesto: header fila oscura (#1F4E79), texto blanco; fila total en bold con fondo #E8F5E9
- Sin emojis. Sin bullet points estilo ChatGPT. Prosa directa.

### Plantilla Python base

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
import os

def fmt_usd(value):
    """Formato europeo: 1.234,50"""
    s = f"{value:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def add_table_row(table, cells, bold=False, bg_color=None, text_color=None):
    row = table.add_row()
    for i, text in enumerate(cells):
        cell = row.cells[i]
        cell.text = str(text)
        run = cell.paragraphs[0].runs[0] if cell.paragraphs[0].runs else cell.paragraphs[0].add_run(str(text))
        run.font.size = Pt(10)
        run.bold = bold
        if text_color:
            run.font.color.rgb = RGBColor(*text_color)
        if bg_color:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), bg_color)
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)
    return row

# --- Datos del sitio (completar con los datos recolectados) ---
DATOS = {
    "url": "https://www.debosaber.cl",
    "nombre": "DeboSaber.cl",
    "cms": "WordPress",
    "plugin_seo": "Rank Math",
    "cache": "LiteSpeed Cache",
    "constructor": "Gutenberg",
    "urls_total": 710,
    "urls_posts": 710,
    "urls_paginas": 0,
    "tier": "C",
    "tarifa": 60,
    "fecha": datetime.now().strftime("%d/%m/%Y"),
    "cliente": "DeboSaber.cl",
    "preparado_por": "Zythos Media",
}

ISSUES = [
    # (prioridad, problema, impacto, solucion, horas)
    ("Crítico", "Sin sitemap XML activo", "Google no puede descubrir ni rastrear las páginas eficientemente", "Activar y configurar sitemap en Rank Math", 2),
    ("Alto", "Meta descriptions duplicadas o ausentes en >50% de posts", "El buscador genera snippets automáticos que no invitan al clic", "Optimización bulk de meta descriptions en posts prioritarios", 14),
    # ... más issues
]

SERVICIOS = [
    # (servicio, descripcion, horas, tarifa)
    ("Auditoría SEO técnica inicial", "Revisión completa del estado técnico con informe detallado", 8, DATOS["tarifa"]),
    ("Optimización on-page bulk", f"Titles, metas y H1 en {DATOS['urls_posts']} posts", 28, DATOS["tarifa"]),
    # ... más servicios
]

# --- Generación del documento ---
doc = Document()

# Estilos globales
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# ... (código completo del documento)

output_path = f"<directorio-de-auditorias>/{DATOS['nombre'].lower().replace('.', '-')}/cotizacion-seo-{DATOS['nombre'].lower().replace('.', '-')}-{datetime.now().strftime('%Y-%m-%d')}.docx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
doc.save(output_path)
print(f"Documento guardado: {output_path}")
```

El script real generado debe estar completamente funcional y rellenar todos los datos recolectados en las fases 1–5.

---

## Output final esperado

1. El documento `.docx` guardado en `<directorio-de-auditorias>/<cliente>/cotizacion-seo-<slug>-<fecha>.docx`
2. En el chat: resumen de 5 líneas con:
   - Tier asignado
   - Issues críticos detectados (N)
   - Total horas estimadas
   - Presupuesto total (USD, formato europeo)
   - Ruta del archivo generado

---

## Notas de comportamiento

- No preguntar por datos si se pueden obtener en Fase 1. Solo preguntar si una fuente crítica falla y no hay alternativa.
- Si DataForSEO no está disponible, omitir esas secciones del documento con nota "Datos pendientes de herramienta de backlinks".
- El documento va dirigido al cliente, no al equipo técnico. Lenguaje claro, sin jerga SEO innecesaria.
- Nunca inventar datos de tráfico, rankings o backlinks sin fuente verificada.
- Si el usuario proporciona datos GSC o de ranking, incorporarlos en la sección "Visibilidad en búsqueda".
- Formato numérico europeo en todo el documento (punto miles, coma decimales).
- Actualizar CLAUDE.md del proyecto si se identifica información nueva del cliente durante la ejecución.

---

## Reglas de cálculo de horas — verificación interna

Antes de escribir el presupuesto, verificar que las horas sean coherentes con el tier:

| Tier | Rango total horas típico (proyecto inicial) |
|------|---------------------------------------------|
| A    | 12–30 horas                                 |
| B    | 30–80 horas                                 |
| C    | 80–200 horas                                |

Si el total calculado cae fuera del rango, revisar los multiplicadores de volumen antes de ajustar la tarifa.
