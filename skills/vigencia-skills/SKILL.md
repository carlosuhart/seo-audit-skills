---
name: vigencia-skills
description: >
  Mantiene al día el catálogo de skills de SEO, GEO y AEO. Inventaría qué skills tienen fecha
  de revisión o de fuentes y cuáles están vencidas o sin fecha, revisa cada mes las fuentes
  que cambian la práctica (Search Central, actualizaciones del algoritmo, crawlers y
  publicidad de las plataformas de IA, Bing, schema.org) y entrega una lista de qué skill
  parchear y con qué fuente, sin editar nada por su cuenta. Use when user says "vigencia de
  las skills", "skills al día", "revisión mensual de skills", "qué skills están
  desactualizadas", "novedades de Google para las skills", "skill freshness" o "monthly
  skill review". Corre el primer día hábil de cada mes. No sirve para el chequeo estructural
  diario del catálogo (carga sin errores), que es otro paso.
metadata:
  category: seo
  author: Zythos Media
  version: 1.0.0
  creado: 2026-10-31
  revisar: 2027-04-30
---

# Vigencia de skills: revisión mensual

Las skills envejecen sin avisar. Una guía de Google que cambia, un crawler nuevo o un formato
de anuncio que llega a un país dejan una skill en falso, y nadie lo nota hasta que el error
llega a un entregable. Esta skill convierte el "mantenerse al día" en un proceso con fecha.

## Cuándo

- El primer día hábil de cada mes, como parte del primer chequeo del día.
- A pedido, después de un Core Update o de un anuncio grande de una plataforma de IA.

## Paso 1: inventario

```
py "<carpeta de la skill>\scripts\vigencia.py" "C:\Users\<usuario>\.claude\skills" -o "<scratchpad>\vigencia.json"
```

Clasifica cada skill según su SKILL.md. La fecha `revisar:` se lee solo del SKILL.md; las
fechas de fuentes se buscan también en `references/*.md` ("fuentes", "sources", "consultado",
"verificado", "checked", "updated", "as of" y similares), y una fecha futura nunca cuenta como
fuente:

| Estado | Criterio |
|---|---|
| `vencida` | Su fecha `revisar:` ya pasó (el script sale con código 1) |
| `por_vencer` | Vence en 30 días o menos (`--dias-aviso`) |
| `fuentes_viejas` | Sin `revisar:` y con fuentes de más de 180 días (`--fuente-max-dias`) |
| `sin_fecha` | Sin fecha de revisión ni de fuentes |
| `vigente` / `vigente_por_fuentes` | El resto |

Antes de reportar una `fuentes_viejas`, abrir la línea que generó la fecha: una fecha de
plantilla o de ejemplo ("Last updated" de un formulario) no es una fuente vieja, y una skill
de terceros con fuentes viejas se corrige con un parche o al actualizar la suite, no a mano.

Las skills `sin_fecha` no son un error en sí: muchas son de terceros o de procedimiento. Se
priorizan las que hacen afirmaciones sobre plataformas externas (Google, IA, anuncios, leyes).

## Paso 2: barrido de fuentes del mes

Revisar las novedades desde la última revisión (la fecha está en la memoria del proyecto de
skills). Con WebSearch en modo `extended` y varias búsquedas en paralelo:

| Fuente | Qué buscar | Skills que suele tocar |
|---|---|---|
| Google Search Central Blog y el changelog de la documentación (https://developers.google.com/search/updates) | Cambios en guías, structured data retirado o nuevo, AI features | seo-technical, seo-schema, schema-markup, canonical, seo-geo |
| Changelog de crawling de Google (https://developers.google.com/crawling/docs/changelog), DISTINTO del anterior | robots.txt, user agents nuevos o renombrados, IP ranges, frecuencia de rastreo, controles de entrenamiento IA | robots-txt, seo-logs (bots.json), seo-agentic, seo-geo |
| Google Search Status Dashboard | Core, spam y otros updates con sus fechas | seo-gsc-drops, seo-report, CLAUDE.md (sección de updates) |
| Documentación de crawlers de OpenAI, Anthropic, Perplexity, Apple, Meta y Google-Extended | User-agents nuevos, rangos IP, cambios de robots | seo-geo, seo-agentic, robots-txt, seo-logs |
| Publicidad en asistentes de IA (OpenAI, Google Ads, Microsoft Advertising) | Países, formatos, medición | ads-asistentes-ia (revisión trimestral) |
| Bing Webmaster Blog e IndexNow | Copilot, IndexNow, informes nuevos | bing-wmt, seo-bing, geo-ai-discoverability |
| schema.org (releases) y Search Gallery de Google | Tipos o propiedades nuevas o retiradas | seo-schema, schema-markup |
| Lighthouse y PageSpeed Insights (release notes) | Métricas o categorías nuevas (Agentic Browsing) | core-web-vitals, seo-agentic |
| GA4 y Search Console (novedades de producto) | Informes, filtros, cambios de datos | ga4-analysis, seo-google, ga4-ai-traffic |
| Leyes de datos de las jurisdicciones cubiertas | Plazos y reformas | privacidad y sus 8 sub-skills |

Si una página de documentación muestra un "Last updated" reciente sin entrada en ningún
changelog, comparar su texto con una copia anterior (Wayback Machine,
`https://archive.org/wayback/available?url=<url>&timestamp=<AAAAMMDD>`, descargando con
`id_` para tener el HTML original) y reportar la frase exacta que cambió.

Reglas de evidencia: fuente primaria, fecha de publicación y fecha de consulta. Un rumor o una
nota de prensa no basta para cambiar una skill. Si algo no está confirmado, se dice.

## Paso 3: informe y propuesta

Entregar una tabla: skill, qué cambió, fuente con fecha, propuesta de cambio (una línea) y
prioridad. **No editar ninguna skill sin el OK del usuario.** Con el OK:
- Skills propias: editar la fuente en `seo-skills/skills/<nombre>/`, copiarla a
  `.claude/skills/` y actualizar `metadata.revisar` y la fecha de las fuentes.
- Skills de terceros sobreescritas por un installer: el cambio va como bloque en
  `.claude/skills/_patches/<skill>/` y se registra en `scripts/patch_claude_seo.py`, nunca
  directo en el SKILL.md.
- Toda skill que haga afirmaciones sobre plataformas externas debe quedar con `revisar:` en su
  `metadata`.

## Paso 4: cierre

Guardar en la memoria del proyecto de skills la fecha de esta revisión, lo cambiado y lo
pendiente. La próxima revisión parte desde esa fecha.

## Errores frecuentes

| Situación | Acción |
|---|---|
| Una fuente devuelve 403 | Buscar cobertura secundaria fiable e indicarlo en la fuente |
| El script marca una fecha que no es de fuentes (por ejemplo, la fecha de un estudio citado) | Agregar `revisar:` explícito en la metadata de esa skill |
| Una actualización de un installer borró un parche | Correr `patch_claude_seo.py` y revisar sus avisos |
