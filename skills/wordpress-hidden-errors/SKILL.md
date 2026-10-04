---
name: wordpress-hidden-errors
description: >
  Auditoría forense de errores ocultos en WordPress grande y multilingüe (WPML o
  Polylang, Rank Math, LiteSpeed, Cloudflare): los que no ve Screaming Frog ni GSC
  porque viven en la base de datos, el contenido crudo o la configuración de plugins.
  Volcado por idioma vía REST, escaneo offline (prefijos de idioma retirados, enlaces
  cruzados de idioma, slugs de traducción inventados, ?p= a borradores, traducciones
  con el cuerpo en otro idioma, posts sin idioma, shortcodes de plugins desinstalados,
  residuos de chat de IA, scripts inyectados, JSON-LD roto) y corrección con control
  md5 sin mover la fecha de modificación. Use when user says "errores ocultos",
  "auditoría profunda WordPress", "qué más está roto", "limpieza masiva de contenido",
  "WPML", "shortcodes en crudo" o "URLs fantasma en el sitemap". No usar para una
  sola URL (seo-page) ni para CWV.
user-invokable: true
---

# WordPress Hidden Errors — auditoría forense de contenido y configuración

Encuentra y corrige errores estructurales que no ve un crawler: viven en `post_content`,
en tablas de WPML, en opciones de plugins o en reglas de Cloudflare. Nació de una
auditoría real de un medio WordPress con 2.000+ documentos en 4 idiomas donde un solo
patrón (enlaces internos con un prefijo de idioma retirado) afectaba a 1.300 posts y
nadie lo había detectado.

## Cuándo usarla

- Sitio WordPress con cientos o miles de posts, sobre todo multilingüe.
- Hubo migraciones, cambios de configuración de idiomas, cambios de plugin o mucha
  producción con IA o traducción automática.
- Síntomas sin causa clara: URLs raras en GSC, 404 que nadie enlaza "a propósito",
  sitemap con URLs que redirigen, traducciones que no posicionan.

## Requisitos

- Application password de WordPress con `manage_options` (para escrituras) en
  variables de entorno: `WP_SITE`, `WP_USER`, `WP_APP_PASSWORD`.
- Plugin Code Snippets activo (las escrituras en base de datos usan un endpoint REST
  temporal que se crea y se borra en la misma ejecución).
- Opcional: token de Cloudflare con Cache Purge, WAF y Single Redirect.

## Reglas de seguridad (leer antes de tocar nada)

1. **Nunca carga paralela contra el origen.** Hosting compartido o con poca CPU cae con
   un crawl concurrente. Todo en secuencia con pausa (1 a 2 s); las verificaciones
   externas (otros dominios) sí pueden ir en paralelo.
2. **User-Agent de navegador actual.** Los WAF suelen bloquear `python`, `curl` y rangos
   concretos de Chrome usados por bots. Si aparece un 403 nuevo, consultar los eventos
   del firewall antes de suponer credenciales malas; cambiar la versión del UA suele
   bastar. Nunca desactivar la regla.
3. **Primero leer, después escribir.** Toda escritura se calcula offline sobre un
   respaldo exacto del `content.raw` actual (no sobre el volcado de días antes: otras
   correcciones lo cambian) y se aplica con control md5.
4. **Contenido y configuración son permisos distintos.** Editar `post_content` es una
   cosa; cambiar robots.txt, opciones de plugins, reglas WAF, mandar posts a la
   papelera o crear redirecciones es otra. Pedir autorización explícita al usuario
   para cada lote de configuración y documentar el lote antes de ejecutarlo.
5. **Respaldar cada valor anterior** (archivo local o una opción WP de respaldo) y
   borrar el snippet temporal al terminar (en Code Snippets el primer DELETE manda a la
   papelera; repetir con `?force=true`).
6. **No mover la fecha de modificación por limpiezas.** Escribir directo en
   `post_content` vía `$wpdb->update` + `clean_post_cache`. Solo las reescrituras
   editoriales reales (una traducción nueva, por ejemplo) pasan por la REST normal.

## Proceso

### 1. Volcado completo

```bash
python scripts/wp_dump.py --out audit/dump.json --langs es,en,pt-br,fr
```

Recorre `posts` y `pages` publicados por idioma con `context=edit` (contenido crudo).
`lang=all` NO devuelve las traducciones en WPML: hay que pedir cada idioma. Los posts
publicados sin idioma asignado en WPML no salen en ningún idioma (ver patrón H1).

### 2. Escaneo offline

```bash
python scripts/wp_scan.py audit/dump.json --site https://www.ejemplo.com --sitemaps audit/sitemaps.json --out audit/findings.json
```

Detecta los patrones del catálogo que se resuelven sin red. `--sitemaps` (opcional)
es un JSON `{url: {es: url, en: url}}` con los grupos hreflang leídos del sitemap; con
él se detectan los enlaces cruzados de idioma y las URLs del sitemap que no están en
el volcado.

### 3. Verificación en vivo (secuencial)

Resolver cada destino interno desconocido siguiendo redirecciones (máx. 6 saltos) y
clasificar: 200 directo, redirección a 200, redirección a portada, 404/410. Cruzar con
la base de datos (endpoint temporal de solo lectura) para saber si un destino roto es
un borrador, un post sin idioma o un slug que nunca existió. Detalle en
`references/patterns.md`.

### 4. Corrección

Construir `pairs.json` = `{post_id: [[desde, hasta], ...]}` con reemplazos exactos y
aplicar:

```bash
python scripts/wp_apply.py collect audit/fix1 --ids 123,456
python scripts/wp_apply.py apply audit/fix1
```

`apply` comprueba en el servidor que el md5 del contenido actual coincide con el del
respaldo, aplica `str_replace` secuencial y devuelve el md5 nuevo, que debe coincidir
con el calculado en local. Si no coincide, ese post no se escribe.

Para quitar shortcodes de un plugin desinstalado conservando los saltos de párrafo y
retirando los encabezados que solo existían para ese bloque:

```bash
python scripts/strip_shortcode.py plan audit/strip --tag amazon
```

### 5. Purga y verificación

- Purgar Cloudflare por URL en lotes de 30 (la caché de HTML suele estar en 4 h, y las
  301 también se cachean). LiteSpeed: `litespeed_purge_post` por post o
  `litespeed_purge_all` cuando cambia algo global (footer, anuncios, opciones).
- Verificar sobre `content.rendered` (pasa por `wpautop` y los shortcodes) y una muestra
  de páginas públicas, no solo sobre el crudo.

## Catálogo de patrones (resumen)

| Id | Patrón | Severidad | Cómo se ve |
|----|--------|-----------|------------|
| L1 | Enlaces internos con prefijo de idioma retirado (`/es/...`) | Alta | 301 masivos, a veces a 404 |
| L2 | Enlace de traducción a la versión original existiendo la traducida | Alta | Señal de idioma cruzada |
| L3 | Slugs de traducción inventados (construidos desde el título) | Alta | 404 en EN/PT/FR |
| L4 | `?p=ID` a traducciones en borrador | Alta | 404 |
| L5 | Autoenlaces vía redirección, enlaces relativos, enlaces con fecha antigua | Media | 301 o bucle |
| C1 | Shortcode de plugin desinstalado visible en crudo | Alta | Texto `[plugin ...]` en la página |
| C2 | Shortcode dentro de anuncios (Advanced Ads) | Alta | Igual, pero no está en el post |
| C3 | Traducción con el cuerpo en otro idioma | Alta | Título traducido, cuerpo original |
| C4 | Residuos de UI de chat de IA (`data-turn-id`, clases Tailwind) | Media | DOM inflado, delata origen |
| C5 | Saltos de línea escapados (`\n` literal) | Alta | Se ven `\n\n` en la página |
| C6 | JSON-LD inline inválido (`\'`, contenido escapado) | Media | Schema ignorado |
| C7 | Script ofuscado inyectado en `post_content` | Crítica | Carga de dominio externo |
| H1 | Posts publicados sin idioma en WPML (duplicados) | Media | URLs fantasma en el sitemap |
| H2 | Strings de portada sin traducir en WPML String Translation | Alta | Title/meta en otro idioma |
| H3 | Plugin de enlaces externos usa `home_url()` del idioma | Media | Enlaces propios marcados externos |
| P1 | Redirección de adjuntos a URL obsoleta | Alta | Todo adjunto huérfano a 404 |
| P2 | Canonical personalizado con prefijo viejo o destino ajeno | Alta | Post fuera del sitemap |
| P3 | Noindex por defecto en un tipo de contenido que tapa páginas nuevas | Alta | Herramienta propia sin indexar |
| P4 | Plugin social que duplica todo el bloque Open Graph | Media | Dos og:url, uno relativo |
| P5 | robots.txt físico con bloques contradictorios añadidos por plugins | Media | Content-Signal opuestos |
| P6 | Regla WAF genérica que bloquea `/feed/` | Media | RSS 403 a lectores |
| P7 | Cabecera `Link: describedby` a `llms.txt` por idioma inexistente | Baja | 404 anunciado en cabecera |

Detección y corrección de cada uno en `references/patterns.md`. Tablas, claves de
opciones y consultas SQL de WPML y Rank Math en `references/wpml-rankmath-internals.md`.

## Trampas operativas aprendidas

- **Un heredoc o `-c` de shell come las barras invertidas.** Para buscar o reemplazar
  `\n` o `\'` literales, escribir el script en un archivo y usar `chr(92)`.
- **robots.txt con saltos mixtos** (`\r\n` y `\n` en el mismo archivo) rompe los regex;
  normalizar antes.
- **`include=` en la REST filtra por idioma.** Para traer IDs de varios idiomas hay que
  repetir la consulta con cada `lang`.
- **Una traducción "rota" puede ser otra cosa**: el `?p=` de un widget JavaScript propio
  (`'?p=' + id`) no es un enlace roto. Mirar el contexto antes de corregir.
- **El destino de una redirección puede ser el propio post.** Antes de reemplazar un
  enlace por el destino final de su redirección, comprobar que no sea un autoenlace.
- **Verificar "estático" no basta para scripts.** LiteSpeed puede mover JS inline a un
  archivo combinado; confirmar en navegador real.

- **md5 que nunca coincide.** Si un post tiene bytes en otra codificación (ISO-8859-1
  en contenido antiguo), el `content.raw` de la REST no es idéntico a `post_content` y el
  servidor rechaza la escritura por md5. Para esos posts, aplicar solo los fragmentos
  cambiados (por ejemplo el `href="..."` exacto) con un endpoint que exija que cada
  fragmento exista en la base de datos, y verificar después por la REST.
- **WAF que exige cabeceras de navegador en escrituras.** `wp_common.api_client()` ya
  envía `Origin` y `Referer` de wp-admin; si aún hay 403/503 en Code Snippets, revisar
  eventos del firewall.

- **Un enlace con `#` al mismo post no es un autoenlace.** Los índices (`[toc]` y similares)
  enlazan a `post/#seccion`; al normalizar la URL quitando el fragmento parecen autoenlaces.
  Excluir siempre los `href` con `#` antes de quitar autoenlaces, y comparar el número de
  anclas antes y después de cada lote.
- **Cortes de conexión en hosting compartido.** `wp_apply.py collect` es reanudable y
  reintenta con espera creciente; ante un `ReadError`, comprobar que el sitio responde y
  relanzar con `--pause` mayor, nunca en paralelo.

## Entregable

Informe interno con hallazgos por severidad, IDs afectados (JSON aparte), causa raíz y
lote de corrección propuesto separado en "contenido" y "configuración". Tras aplicar:
tabla de verificación en vivo y lista de respaldos para revertir.

## Reference files

- `references/patterns.md` -- detección y corrección de cada patrón del catálogo
- `references/wpml-rankmath-internals.md` -- tablas WPML, opciones de Rank Math y otros plugins, SQL útil
