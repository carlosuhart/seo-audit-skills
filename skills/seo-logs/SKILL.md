---
name: seo-logs
description: >
  Análisis de logs de servidor para SEO y GEO: consigue los logs según la plataforma
  (Apache, Nginx, LiteSpeed, Cloudflare, Vercel, WordPress con VigIA), verifica
  Googlebot, Bingbot y bots de IA por DNS o rangos IP, mide rastreo por sección y por
  bot, códigos de respuesta, presupuesto gastado en parámetros y redirecciones, URLs del
  sitemap nunca rastreadas, huérfanas rastreadas y bots de IA por tipo (entrenamiento,
  búsqueda, usuario), y lo cruza con la indexación de GSC. Script parse_logs.py con
  salida JSON. Use when user says "análisis de logs", "log file analysis", "qué bots
  visitan", "rastreo de Googlebot", "bots de IA en el servidor", "crawl budget",
  "presupuesto de rastreo", "server logs" o "descubierta sin indexar, ¿pasa Googlebot?".
  Not for robots.txt rules (robots-txt) or AI citability (seo-geo).
argument-hint: "<access.log | drain.ndjson> [--sitemap sitemap.xml] [--gsc paginas.csv] [--verify-dns]"
metadata:
  category: seo
  author: Zythos Media
  fuentes: "2026-10-31"
  revisar: "2027-04-30"
---

# SEO Logs -- qué rastrean de verdad Google, Bing y los bots de IA

Los logs son la única fuente que dice qué URLs pidió cada bot, cuándo y con qué
respuesta. GSC muestra una muestra agregada solo de Google; los logs confirman si
Googlebot visita las páginas "Descubierta: actualmente sin indexar" y qué bots de IA
entran de verdad, separados de los que se hacen pasar por ellos.

## Quick Reference

| Paso | Qué haces | Salida |
|---|---|---|
| 1. Conseguir logs | Elegir la fuente por plataforma (`references/plataformas.md`) | Archivos `.log`, `.gz`, `.ndjson` |
| 2. Procesar | `py scripts/parse_logs.py ...` | JSON con agregados |
| 3. Verificar bots | `--verify-dns` y/o `--ip-ranges` | Verificado, falso, no verificable |
| 4. Cruzar | `--sitemap`, `--gsc`, `--known-urls` | No rastreadas, huérfanas, cruce de indexación |
| 5. Diagnosticar | Diagnóstico paso a paso (abajo) | Hallazgos priorizados |
| 6. Informar | Formato de informe (abajo) | Informe interno o para cliente |

## Relación con otras skills (no duplicar)

- Tabla de bots de IA, qué controla cada token y cómo escribir robots.txt:
  `robots-txt`, `seo-technical` (sección AI crawlers) y `seo-geo` (crawler access).
  Esta skill no repite esas tablas; usa `references/bots.json` solo para clasificar
  user-agents y saber cómo verificarlos.
- Política de agentes, Content-Signal y WAF frente a agentes: `seo-agentic`
  (`references/access-policy.md`).
- Estado de indexación por URL desde la API: `seo-google` (URL Inspection).
- Huérfanas y profundidad de clic con crawl interno: `seo-interlinking`. Los logs
  aportan si Google sigue pidiendo esas URLs.
- Rastreo de Bing por API: `bing-wmt`. WordPress con plugin VigIA: MCP `mcp__vigia__*`.

## Paso 1. Conseguir los logs

Detalle, fuentes y precios en `references/plataformas.md` (cargar bajo demanda).

1. **WordPress en Apache, Nginx o LiteSpeed**: pedir el access log en formato combined de
   al menos 30 días (ideal 60 a 90). En hosting compartido suele haber solo 1 a 7 días:
   pedir que activen el archivado antes de la ventana a analizar.
2. **WordPress con VigIA**: usar `mcp__vigia__vigia-get-top-crawlers`,
   `vigia-get-crawler-stats` y `vigia-get-top-pages` para tendencias. VigIA no verifica
   IP; para cruce con sitemap y GSC hace falta el access log.
3. **Detrás de Cloudflare**: Logpush del dataset `http_requests` o AI Crawl Control para
   la parte de IA. El log del origen pierde lo que sirvió la caché.
4. **Vercel (Next.js, Astro)**: Observability Plus (30 días, vista AI Traffic y bots
   verificados) o Drains en NDJSON. Sin presupuesto: registro en middleware con
   `waitUntil()` o `after()`, que requiere desarrollo.
5. **Sin acceso**: GSC Estadísticas de rastreo y Bing WMT. Son agregados y no dicen
   nada de bots de IA de terceros; declararlo en el informe.

Antes de analizar: confirmar zona horaria, que no falten días (rotación) y que la IP
registrada es la del cliente real y no la de un proxy o CDN. Si es la del proxy, la
verificación de bots marcará todo como falso.

Privacidad: los logs contienen IP de personas. Trabajar con copias locales, no subirlos
a servicios externos, y no incluir IP en entregables salvo las de bots suplantados.

## Paso 2. Procesar con el script

```
py scripts/parse_logs.py access.log access.log.1.gz \
   --sitemap sitemap.xml --gsc paginas.csv --known-urls crawl_interno.txt \
   --verify-dns --dns-cache dns_cache.json --top 50 -o resultado.json
```

- Formato automático (`combined`, `vercel`, `cloudflare`) o forzado con `--format`.
- `--host` filtra cuando el archivo mezcla dominios.
- `--section-depth 2` para separar `/blog/categoria/` de `/blog/otra/`.
- `--gsc-status "Descubierta: actualmente sin indexar"` cuando el export de GSC es por
  motivo y no trae columna de estado.
- `--ip-ranges GPTBot=gptbot.json` (repetible) verifica contra rangos ya descargados.
  El script no descarga nada; las URL de cada JSON están en `references/bots.json`.
- Sitemap índice: el script lista los hijos en `sitemaps_hijos_no_cargados`; descárgalos
  y pásalos con `--sitemap` repetido.
- Ejecutar Python por PowerShell en Windows (`py -X utf8 ...`).

Si el JSON trae muchas `lineas_no_reconocidas`, el formato no es combined: revisar las
primeras líneas y pedir el `log_format` antes de seguir.

## Paso 3. Verificación de bots

El user-agent se falsifica fácil. Sin verificar, los totales de "Googlebot" o "GPTBot"
pueden ser scrapers.

| Operador | Método oficial | Dominio o JSON |
|---|---|---|
| Google | DNS inverso y directo, o rangos | `googlebot.com`, `google.com`, `googleusercontent.com`; `common-crawlers.json`, `special-crawlers.json`, `user-triggered-fetchers*.json` |
| Microsoft | DNS inverso y directo, o rangos | `search.msn.com`; `bingbot.json` |
| Apple | DNS inverso y directo, o rangos | `applebot.apple.com`; `applebot.json` |
| Common Crawl | DNS inverso (solo IPv4) o rangos | `crawl.commoncrawl.org`; `ccbot.json` |
| OpenAI | Rangos por bot | `gptbot.json`, `searchbot.json`, `chatgpt-user.json` |
| Anthropic | Rangos (una lista para todos) | `claude.com/crawling/bots.json` |
| Perplexity | Rangos por bot | `perplexitybot.json`, `perplexity-user.json` |
| Meta, ByteDance | Sin método publicado | No verificable, solo señal |

Estados que devuelve el script: `verificado`, `falso` (IP fuera de rango o DNS que no
cierra), `pendiente` (límite de consultas o fallo de red), `sin_verificar` (no se pidió
verificación) y `no_verificable` (el operador no publica método).

Reglas:
- Las peticiones `falso` se excluyen de los cruces con sitemap y GSC, pero se informan.
- `--verify-dns` hace una consulta por IP única (con caché y límite `--verify-dns-max`).
  Googlebot rota pocas IP por día, así que el costo es bajo.
- Un bot de IA `sin_verificar` se informa como "declarado", nunca como confirmado.
- Google-Extended y Applebot-Extended no aparecen en logs: son tokens de robots.txt.

## Paso 4. Métricas que importan

Calcular sobre peticiones verificadas, o declaradas si no hubo verificación, y decirlo.

1. **Frecuencia de rastreo por sección y por bot** (`bots.*.secciones`, `por_dia`): qué
   parte del sitio recibe el rastreo frente a su valor de negocio.
2. **Códigos de respuesta por bot** (`status`, `pct_4xx`, `pct_5xx`): con más de 5% de
   4xx o cualquier racha de 5xx, Google reduce el ritmo de rastreo.
3. **Presupuesto en parámetros** (`pct_con_parametros`, `parametros_top`): utm, orden,
   filtros y sesiones que Googlebot sigue pidiendo.
4. **Presupuesto en redirecciones** (`pct_redirecciones`, `urls_3xx_top`): enlaces
   internos y sitemaps que apuntan a URLs que redirigen.
5. **URLs del sitemap nunca rastreadas** (`sitemap.lista_nunca_rastreadas_googlebot`)
   en el periodo, y su porcentaje de cobertura.
6. **Rastreo de huérfanas** (`googlebot_fuera_de_sitemap`): URLs que Google pide y que
   no están en sitemap ni en el crawl interno (`--known-urls`).
7. **Bots de IA por tipo** (`por_categoria`): `ia_entrenamiento`, `ia_busqueda` e
   `ia_usuario` se leen distinto. Las visitas `ia_usuario` (ChatGPT-User,
   Claude-User, Perplexity-User) son personas preguntando por el contenido en ese
   momento y son la señal más cercana a una cita.
8. **Cruce con GSC** (`cruce_gsc.por_estado`): por estado de indexación, cuántas URLs
   recibieron Googlebot en el periodo y cuándo fue la última visita.
9. **Recursos y móvil** (`pct_recursos`, `pct_movil`): Googlebot debe ser
   mayoritariamente smartphone; si pide pocos CSS/JS puede no estar renderizando.

## Diagnóstico paso a paso (árbol)

```
¿Hay Googlebot verificado en el periodo?
├─ No → revisar robots.txt, WAF/CDN bloqueando Google, DNS y estado del host en GSC.
└─ Sí → ¿Las URLs "Descubierta: sin indexar" reciben Googlebot?
    ├─ No (sin_googlebot alto) → problema de descubrimiento o prioridad:
    │    ¿pct_con_parametros + pct_redirecciones > 20%?
    │    ├─ Sí → presupuesto desperdiciado: canonicals, enlaces internos limpios,
    │    │       robots.txt para facetas, sitemaps sin URLs que redirigen.
    │    └─ No → poca demanda o autoridad: enlaces internos desde páginas fuertes
    │            (seo-interlinking), sitemap con lastmod real, menos URLs nuevas a la vez.
    └─ Sí (con_googlebot alto) → Google las vio y decidió no indexar:
         calidad, duplicado o canonical (seo-content, canonical), no rastreo.
¿pct_5xx > 1% o 5xx en racha? → servidor primero; Google baja el ritmo.
¿Huérfanas con 200 rastreadas? → enlazarlas o redirigirlas/retirarlas.
¿Bots de IA de búsqueda o usuario con 4xx/5xx o bloqueados por WAF?
   → revisar firewall y robots.txt (robots-txt, seo-agentic) según la política del cliente.
¿Muchos "falso"? → scrapers con UA de bot: regla de WAF por verificación, no por UA.
```

Límites honestos: un periodo corto no prueba que una URL "nunca" se rastrea; usar al
menos 30 días y decir "en el periodo analizado". Los logs de origen detrás de un CDN
subestiman. La IA que no se identifica no aparece.

## Formato de informe

Preguntar si es uso interno o para cliente. Estructura:

1. **Alcance**: sitio, fuente de logs, periodo (desde, hasta, días con datos), si hubo
   verificación y qué parte quedó `pendiente` o `no_verificable`.
2. **Resumen** en tres o cuatro frases: qué bots rastrean, cuánto y el hallazgo principal.
3. **Tabla por bot**: peticiones, URLs únicas, % 3xx, % 4xx, % 5xx, % parámetros,
   verificación.
4. **Rastreo por sección** frente a importancia de negocio.
5. **Sitemap y huérfanas**: cobertura, ejemplos de nunca rastreadas, huérfanas con 200.
6. **Cruce con GSC** por estado de indexación, con la lectura del árbol.
7. **Bots de IA** por tipo, con la advertencia de verificación de cada operador.
8. **Acciones priorizadas** (impacto, esfuerzo, quién lo hace) y fecha para repetir la
   medición con el mismo método.

Números en formato europeo en entregables (1.234 peticiones, 12,5%). No incluir IP de
personas.

## Reference Files

- `references/plataformas.md`: cómo sacar los logs por plataforma, retención, planes y
  precios con fuente y fecha. Cargar bajo demanda en el Paso 1.
- `references/bots.json`: user-agents, categoría y método de verificación de cada bot,
  con fuente. Lo usa el script; editarlo para añadir bots (orden: específicos primero).
- `scripts/parse_logs.py`: parser y agregador (solo stdlib, Python 3.11+).
- `scripts/tests/`: muestras sintéticas (combined, Vercel, Cloudflare, sitemap, GSC y
  rangos de prueba) para comprobar el script tras cualquier cambio.

## Errores frecuentes

- Contar Google-InspectionTool como rastreo: son pruebas en vivo de GSC; el script lo
  separa de Googlebot.
- Dar por buenos totales de bots de IA sin verificar: informar como "declarados".
- Cruzar URLs con host o barra final distinta: el script compara por ruta normalizada.
- Analizar logs rotados incompletos: revisar `periodo.dias_con_datos` contra el rango.
- Confundir el Googlebot de imágenes o AdsBot con el rastreo de páginas: van separados.
