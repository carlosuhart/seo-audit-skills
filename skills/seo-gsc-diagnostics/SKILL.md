---
name: seo-gsc-diagnostics
description: >
  Diagnóstico sobre datos reales de GSC: quick wins, canibalización de queries y
  anomalías de clics o impresiones. Usar con "quick wins GSC", "canibalización de
  queries" o "anomalías en Search Console". Para contenido usar mineria-de-impresiones;
  para caídas, seo-gsc-drops.
allowed-tools:
  - Read
  - Bash
  - Write
  - Glob
  - WebSearch
metadata:
  revisar: "2027-05-20"
---

# GSC Diagnostics — Quick wins, canibalización y anomalías

Tres diagnósticos sobre datos reales de Search Console que hoy no cubre ningún otro skill instalado: `mineria-de-impresiones` clasifica y prescribe contenido para una página ya elegida; `seo-gsc-drops` compara dos períodos por caída de clics. Este skill responde tres preguntas distintas sobre el sitio completo o una sección de él: dónde hay ganancias rápidas por CTR, qué queries se están robando tráfico entre páginas propias, y qué días no encajan con el resto de la serie.

Origen: metodología replicada a partir de la evaluación del MCP `thatseoagent/mcp` (2026-09-08) — se descartó instalar el servidor de terceros y se construyó esta lógica sobre el acceso a GSC que ya existe en este entorno (service account / token OAuth local), en vez de depender de software externo sin track record.

## Autenticación

Nunca pedir credenciales nuevas. Usar el acceso ya establecido:

- **Sesion local (interactiva):** token en `~/gsc_token.pkl` (scope `webmasters.readonly`), generado por `gsc_auth.py`. Si expiro o no existe, ejecutar `gsc_auth.py` para regenerarlo: abre navegador y requiere aprobacion interactiva del usuario. La ruta se puede sobrescribir con la variable de entorno `GSC_TOKEN_PATH`.
- **Agente cloud / automatizado:** service account con rol de lectura en Search Console. La ruta de su JSON key y las propiedades a las que tiene acceso se documentan en el CLAUDE.md del entorno. Una service account solo ve las propiedades donde se la agrego explicitamente como usuario, asi que para cualquier dominio fuera de esa lista hay que usar el token local.

El script `scripts/gsc_diagnostics.py` intenta primero el token local; si no existe y se le pasa `--service-account`, usa la service account.

## Paso 0 — Validar el sitio y el rango de fechas

1. Confirmar la property exacta en formato GSC (`sc-domain:ejemplo.com` o `https://www.ejemplo.com/`). Si el usuario da un dominio pelado, listar `sites().list()` y resolver el formato correcto.
2. Rango de fechas por defecto: últimos 90 días (GSC tiene ~3 días de delay, calcular con eso). Si el usuario no especifica, usarlo y avisarlo.
3. Antes de interpretar cualquier número, revisar `reference_gsc_data_quality_2025_2026.md`: si el rango incluye mayo 2025 – abril 2026, advertir inflación de impresiones y priorizar clics.

## Ejecución

```bash
py "$HOME/.claude/skills/seo-gsc-diagnostics/scripts/gsc_diagnostics.py" \
  --site "sc-domain:ejemplo.com" \
  --start 2026-06-01 --end 2026-08-30 \
  [--service-account] [--out "<directorio-de-auditorias>/<proyecto>/gsc_diagnostics_AAAAMMDD.json"]
```

Si `py` falla, probar `python3`, `python`, o correrlo desde PowerShell — no reportar el fallo sin haber probado alternativas (`feedback_python_tools.md`).

El script hace tres llamadas a `searchanalytics.query` (dimensiones `query`, `query+page`, `date`) y calcula:

### 1. Quick wins

Criterio (igual que el ya validado en `mineria-de-impresiones`, no inventar uno nuevo):
- Impresiones ≥ percentil 60 del propio dataset (o ≥ 50 si el sitio es chico)
- Posición entre 5 y 20
- CTR real por debajo del referente de su posición (`referentes-ctr-2026.md` de `mineria-de-impresiones`, o la tabla rápida: pos 1 ~28-34%, pos 2-3 ~10-18%, pos 4-6 ~5-8%, pos 7-10 ~2-4%)

Salida: tabla ordenada por impresiones descendente, columna con la brecha de CTR (referente − real) como proxy de oportunidad.

### 2. Canibalización

Agrupar por query, quedarse con queries donde ≥2 URLs distintas reciben clics o impresiones en el periodo. Piso minimo: la pagina lider necesita ≥3 clics en el periodo. Por debajo de eso un ratio alto es 1-2 clics de casualidad, no senal real (detectado corriendo el script contra un recetario de ~1.500 URLs: sin este piso, 243 de 314 "hallazgos" eran pares 1-1).

Severidad:
- **Alta:** la 2ª página recibe >30% de los clics de la 1ª (split real de intención, están compitiendo de verdad)
- **Media:** la 2ª página recibe 10-30% de los clics de la 1ª
- **Baja / ruido:** <10% — normalmente una mención incidental, no vale la pena tocar

Para cada caso de severidad alta o media, indicar cuál de las dos páginas tiene mejor posición/CTR histórico (candidata a quedarse) y cuál debería redirigir, fusionarse o diferenciar intención — mismo criterio que `feedback_cannibalization_check.md`.

### 3. Anomalías

Serie diaria de clics e impresiones del período. Calcular media y desviación estándar; marcar como anómalo cualquier día con `|z-score| > 2`.

Para cada día anómalo detectado:
0. Revisar primero la página de anomalías de datos de Search Console (https://support.google.com/webmasters/answer/6211453). Un error de registro de Google produce exactamente el mismo dibujo que una caída real. Ejemplo: del 9 al 11/11/2026 un error bajó las impresiones del informe de IA generativa, en los mismos días en que arrancaba el core update de noviembre (10/11/2026). Si la fecha coincide con un error de registro, reportarlo así y no como caída.
1. Cruzar la fecha con el calendario de Google Algorithm Updates (`feedback_google_updates.md` — usar WebSearch si el rango es reciente y no hay calendario cargado en memoria)
2. Reportar el cruce como **hipótesis a validar**, nunca como causa confirmada, salvo coincidencia exacta de fecha con un update documentado
3. Si no hay update que coincida, buscar causas propias primero: cambio de contenido, migración, incidente técnico (revisar `project_*` de ese cliente en memoria antes de concluir "causa desconocida")

## Salida

```
## GSC Diagnostics — [site] ([start] a [end])

### Quick wins (top 20)
| Query | Página | Impr | Pos | CTR real | CTR referente | Brecha |
|-------|--------|------|-----|----------|----------------|--------|

### Canibalización
| Query | Página A (líder) | Página B | Clics A | Clics B | % B/A | Severidad | Recomendación |
|-------|-------------------|----------|---------|---------|-------|-----------|----------------|

### Anomalías
| Fecha | Clics | Impr | Z-score | ¿Coincide con Update? | Hipótesis |
|-------|-------|------|---------|------------------------|-----------|

**Nota de calidad de datos:** [advertencia de período si aplica]
```

Guardar el JSON crudo en el directorio de auditorias del proyecto.

## Límites — declarar siempre

- Quick wins y canibalización se calculan sobre el período pedido; un período corto (<28 días) da señal débil, avisarlo.
- El z-score de anomalías es sensible a series cortas o con mucho ruido natural (sitios de bajo volumen): con <30 días de datos, no reportar anomalías, decirlo explícitamente en vez de forzar un cálculo poco confiable.
- Esto es diagnóstico, no prescripción de contenido. Para el plan de qué escribir/reescribir en una página con quick wins, encadenar con `mineria-de-impresiones`.
- Un dato de URL Inspection de ayer puede haber cambiado hoy (Google rastreó entremedio). Antes de entregar un documento que cite el estado de indexación de una URL, reinspeccionarla el mismo día.

## Filtros nuevos de la API Search Analytics (16/11/2026)

Google amplió `searchanalytics.query` (https://developers.google.com/search/blog/2026/11/search-analytics-api-update, consultado 20/11/2026):

- **Marca / sin marca:** dimensión o filtro `brandedClassification` con valores `BRANDED` y `NON_BRANDED` (solo operador `equals`). Datos desde el 21/02/2026, solo en propiedades de nivel superior con volumen suficiente; si la propiedad no califica, no devuelve filas. No se puede combinar con un filtro de `query` en la misma petición.
- **Búsqueda multimodal:** `type: webMultimodal` (Google Lens, Rodea para buscar y subida de imágenes en Search).
- **Varios países o dispositivos a la vez:** `dimensionFilterGroups[].filterLists[]` con `dimension` (`country` o `device`) y `expressions[]`. Países en ISO 3166-1 alfa-3; dispositivos `DESKTOP`, `MOBILE`, `TABLET`. No filtrar la misma dimensión en `filters` y en `filterLists` a la vez.

Uso en este diagnóstico:
- **Quick wins y canibalización sin marca:** correrlos con `brandedClassification = NON_BRANDED` cuando la propiedad califica. Las queries de marca casi siempre tienen CTR alto y una sola página relevante, así que meten ruido en ambos cálculos. Es la clasificación de Google, no una lista de términos propia: declarar cuál se usó.
- **Si la propiedad no califica** (sin filas), volver a separar con una lista de términos de marca confirmada por el usuario, como antes.

## Solicitudes manuales de indexación — el cupo no es público

Cuando el diagnóstico termina en una lista de URL para "Solicitar indexación" en la UI de GSC:

- Google no publica el cupo de solicitudes manuales. Observado en uso real: se agota con una
  tanda de unas 10 URL, y al día siguiente solo dejó pedir 2 más tras una tanda hecha por la
  tarde, lo que apunta a una ventana móvil de 24 h y no a un reinicio a medianoche (hipótesis,
  no confirmada). No afirmar que cada propiedad tiene su propio cupo.
- Una sola tanda por día, ordenada por prioridad de negocio; lo que sobra pasa a la cola del día
  siguiente, pedida a una hora posterior a la de la tanda anterior.
- Cada URL de la tanda se valida en vivo antes de entregarla: 200, indexable, canonical propia y
  todavía sin indexar en URL Inspection (las que Google indexó entremedio salen de la lista).
- No volver a pedir una URL ya solicitada: reinspeccionarla a los 3-4 días.
- En inspecciones largas por API, timeout en cada consulta y salida sin buffer (`python -u`)
  para que un cuelgue no pierda el lote.

## Dependencias

- Si el usuario pide el plan de contenido para las queries detectadas → `mineria-de-impresiones`
- Si el usuario pide comparar contra el período anterior por caída → `seo-gsc-drops`
- Si el hallazgo de canibalización lleva a decidir consolidar o no un artículo nuevo → `blog-cannibalization` (si está instalada) o una revisión manual del solapamiento de intención
