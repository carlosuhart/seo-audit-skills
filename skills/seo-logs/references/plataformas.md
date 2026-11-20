# Cómo conseguir los logs según la plataforma

Fuentes consultadas el 31/10/2026. Precios y planes cambian: confirmar en la página
del proveedor antes de recomendar una compra. Revisar este archivo el 30/04/2027.

## Resumen de decisión

| Plataforma | Mejor fuente | Retención típica | Requiere desarrollo | Formato para parse_logs.py |
|---|---|---|---|---|
| WordPress en Apache (cPanel, Plesk) | access log del servidor | lo que defina el hosting (rotación) | No | `combined` |
| WordPress en Nginx | `access.log` de Nginx | rotación de logrotate | No | `combined` |
| WordPress en LiteSpeed / OpenLiteSpeed | access log del vhost | rotación del hosting | No | `combined` (ver nota) |
| WordPress con plugin VigIA | MCP `mcp__vigia__*` | la del plugin | No | No aplica, ya viene agregado |
| Cualquier sitio detrás de Cloudflare | Logpush (`http_requests`) o AI Crawl Control | según destino | Configurar destino | `cloudflare` |
| Next.js / Astro en Vercel | Observability Plus o Log Drains | 30 días (Plus) | Drains: sí (destino) | `vercel` |
| Sin acceso a nada | GSC Estadísticas de rastreo + Bing WMT | 90 días aprox. (GSC) | No | No aplica |

## Apache (y la mayoría de hostings compartidos)

Formato `combined` estándar de Apache:
`%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-agent}i"`

Ubicaciones frecuentes: `/var/log/apache2/access.log` (Debian/Ubuntu),
`/var/log/httpd/access_log` (RHEL), y en cPanel "Raw Access" o
`~/logs/` o `/usr/local/apache/domlogs/<dominio>`. Muchos hostings compartidos
solo guardan uno a siete días: pedir al cliente que active el archivado de logs
antes de la ventana que se quiere analizar. Con `vhost_combined` la línea empieza
con `host:puerto`; el script lo detecta.

## Nginx

Formato `combined` predefinido (nginx.org, ngx_http_log_module):

```
log_format combined '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```

Ruta por defecto `/var/log/nginx/access.log`, rotado por logrotate en `.1`, `.2.gz`.
Si el servidor usa un `log_format` propio, pedir la directiva para ajustar el regex o
exportar en `combined`. Detrás de un proxy o CDN, `$remote_addr` es la IP del proxy:
hace falta `real_ip_header` (por ejemplo `CF-Connecting-IP`) o la verificación de bots
falla en todas las peticiones.

## LiteSpeed / OpenLiteSpeed

LiteSpeed Enterprise es compatible con la configuración de Apache y en los hostings
con cPanel escribe los logs de dominio en formato combined. OpenLiteSpeed permite
definir el formato del access log por vhost. No se confirmó en documentación oficial
el formato por defecto de cada edición (la página de LiteSpeed consultada devolvió
404 el 31/10/2026): revisar las primeras líneas antes de analizar. Si el script marca
muchas `lineas_no_reconocidas`, el formato no es combined.

## Cloudflare

- **Logpush**: la página de Logpush (actualizada el 30/10/2026) indica disponibilidad en
  Free, Pro, Business y Enterprise, con la disponibilidad de cada dataset sujeta a los
  productos de la cuenta. Fuentes de terceros y versiones anteriores de la documentación
  lo daban como exclusivo de Enterprise: confirmar en el panel de la zona antes de
  prometerlo. Dataset `http_requests`, archivos NDJSON comprimidos con gzip. Campos
  necesarios: `ClientIP`, `ClientRequestHost`, `ClientRequestMethod`, `ClientRequestURI`,
  `ClientRequestUserAgent`, `EdgeResponseStatus`, `EdgeStartTimestamp` y
  `VerifiedBotCategory`. `BotScore` solo existe con Bot Management.
  Fuente: https://developers.cloudflare.com/logs/logpush/ y
  https://developers.cloudflare.com/logs/logpush/logpush-job/datasets/zone/http_requests/
- **AI Crawl Control** (antes AI Audit): disponible en todos los planes según la
  documentación. Muestra qué servicios de IA acceden, patrones de peticiones y quién
  cumple o incumple robots.txt. Sirve para la parte de IA sin exportar logs; no da el
  cruce con sitemap ni con GSC. Fuente: https://developers.cloudflare.com/ai-crawl-control/
- Con Cloudflare delante, el log del servidor de origen solo ve lo que no sirvió la
  caché y la IP es de Cloudflare: el log de origen subestima el rastreo.

## Vercel (Next.js, Astro)

- **Runtime Logs** (todos los planes): retención 1 hora en Hobby, 1 día en Pro, 3 días en
  Enterprise y 30 días con Observability Plus (ventana máxima de 14 días seguidos). Solo
  incluyen las peticiones estáticas servidas desde caché de forma parcial; para todas las
  estáticas hay que usar Drains. Fuente: https://vercel.com/docs/logs/runtime
- **Observability Plus**: Pro y Enterprise, USD 1,20 por millón de eventos, activado por
  defecto en equipos creados o pasados a Pro desde el 03/04/2026. Retención 30 días y
  desglose de CDN Requests por ruta. El changelog del 27/10/2026 añadió la vista
  Observability > AI Traffic (peticiones por bot de IA verificado, páginas más rastreadas,
  recuperaciones de asistentes, peticiones de Markdown y errores); la consulta por CLI
  (`vc metrics vercel.ai_traffic.count --group-by botName`) requiere Plus. Vercel marca
  los bots como verificados, suplantados o no verificables.
  Fuentes: https://vercel.com/docs/observability/observability-plus ,
  https://vercel.com/changelog/ai-traffic-insights-now-available-in-vercel-observability
- **Drains** (antes Log Drains): Pro y Enterprise, no Hobby ni Pro Trial. USD 0,50 por GB
  medido sin comprimir. Formato JSON (array) o NDJSON; cada petición trae un objeto
  `proxy` con `clientIp`, `path` (con query), `userAgent` (array), `statusCode`,
  `timestamp`, `host` y `vercelCache`. Hay que elegir las fuentes `static`, `lambda`,
  `edge`, `redirect` y `external`, sin `build`. Necesita un destino HTTP propio o una
  integración. Filtro útil para abaratar:
  `contains(log/userAgent, 'bot')`. Fuente: https://vercel.com/docs/drains y
  https://vercel.com/docs/drains/reference/logs
- **Registro propio en middleware**: el middleware (o `proxy.ts` en Next.js 16) lee
  `user-agent`, ruta e IP y los escribe en una base de datos sin bloquear la respuesta con
  `waitUntil()` de `@vercel/functions`, o con `after()` de `next/server` en Next.js 15.1 o
  superior. Las promesas de `waitUntil()` comparten el tiempo máximo de la función.
  Requiere desarrollo y una base de datos; tiene sentido si no se quiere pagar Plus ni
  Drains, o si se quiere guardar más de 30 días. Fuente:
  https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package
- Un middleware no ve las peticiones que el CDN resuelve sin ejecutarlo si el `matcher`
  las excluye; revisar el matcher antes de confiar en los totales.

## WordPress con VigIA

El MCP `mcp__vigia__*` da estadísticas de crawlers por sitio (top crawlers, top páginas,
reglas de robots y bloqueos). Detecta por user-agent sin verificar IP, así que los totales
de bots de IA incluyen suplantaciones. Úsalo para tendencias y, si hace falta precisión o el
cruce con GSC y sitemap, pide el access log del servidor.

## Alternativa sin logs

- **GSC, Configuración > Estadísticas de rastreo**: solo en propiedades de dominio o de
  prefijo en la raíz. Muestra peticiones totales, tamaño, tiempo medio de respuesta y el
  desglose por respuesta, tipo de archivo, propósito (descubrimiento o actualización) y tipo
  de Googlebot, más el estado del host (robots.txt, DNS, conectividad) de los últimos 90
  días. Los ejemplos de URL son una muestra, no la lista completa.
  Fuente: https://support.google.com/webmasters/answer/9679690
- **Bing Webmaster Tools**: el informe de rendimiento muestra peticiones de rastreo, errores
  de rastreo y páginas indexadas (hasta seis meses, exportable a CSV); el Explorador del
  sitio da la fecha del último rastreo por URL y existe Control de rastreo. La API de Bing
  WMT expone las estadísticas de rastreo (ver skill `bing-wmt`).
  Fuente: https://www.bing.com/webmasters/help/search-performance-c680da36
- Ninguno de los dos dice nada sobre bots de IA de terceros.
