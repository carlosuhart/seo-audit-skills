# Catálogo de patrones — detección y corrección

Cada patrón: qué es, por qué pasa, cómo se detecta y cómo se corrige. Los ejemplos
numéricos vienen de una auditoría real (medio WordPress, ~2.100 documentos, 4 idiomas).

---

## Enlaces internos

### L1. Prefijo de idioma retirado en enlaces internos

**Qué es:** el idioma por defecto tuvo prefijo (`/es/`) y después se quitó. Los enlaces
escritos en esa época siguen en el contenido; también el campo Website del autor, el
footer, las URL de la página de privacidad del plugin de cookies y la tabla de
redirecciones de Rank Math (cientos de `url_to` apuntando a `/es/`).

**Por qué importa:** cada enlace es una 301 (o una 404 si `/es/` ya no resuelve), y si
el origen marca las 301 como `no-store, private`, Cloudflare no las cachea y un bot que
las recorre tumba el origen.

**Detección:** regex `https?://(www\.)?dominio/es/` sobre `content.raw` de todos los
idiomas, opciones del tema, strings de WPML y tabla `rank_math_redirections`.

**Corrección:** resolver cada URL única en el servidor (slug exacto, `_wp_old_slug`,
reglas de Rank Math, idioma por `icl_translations`), reemplazar por la URL final 200, y
quitar el `<a>` conservando el texto cuando no hay destino. Añadir una regla de
redirección en el edge (`/es/*` → `/*`, 301 dinámica, conservando query string) para
los enlaces externos que no se pueden editar.

### L2. Traducción que enlaza al original existiendo la versión traducida

**Qué es:** al traducir, los enlaces internos se dejan apuntando al idioma original
"hasta que exista traducción", pero nadie vuelve a actualizarlos cuando la traducción
se publica.

**Detección:** mapa de traducciones desde los hreflang del sitemap (Rank Math los
incluye) → para cada enlace de un post en idioma X a una URL de otro idioma, ¿existe la
versión X? Ejemplo real: 130 enlaces en 98 posts. Incluye el caso inverso (original
enlazando a una traducción).

**Corrección:** reemplazar el `href` por la versión del idioma del post. Regla general
para todo enlace interno de una traducción: versión publicada en su idioma si existe;
si no, la original.

### L3. Slugs de traducción inventados

**Qué es:** al traducir con IA, el modelo "adivina" el slug de la versión traducida del
artículo enlazado a partir de su título (`/en/how-is-the-ibu-calculated.../`). La URL
nunca existió.

**Detección:** destinos internos que no están entre las URLs publicadas del volcado →
resolver en vivo → 404. Buscar el artículo real por palabras clave del slug y del
anclaje en el volcado del mismo idioma y del original.

**Corrección:** mapear cada destino a su artículo original y aplicar la regla de L2.
Nunca construir slugs desde títulos; obtenerlos siempre de la REST o del sitemap.

### L4. `?p=ID` a traducciones en borrador

**Qué es:** el enlace se insertó con el ID mientras la traducción enlazada era borrador;
la traducción nunca se publicó → 404 para el visitante.

**Detección:** `href` con `?p=\d+` → consultar estado del ID → `draft`. Obtener su grupo
de traducción (`trid`) y el miembro publicado.

**Corrección:** enlazar la versión publicada del grupo en el idioma del post o, si no
hay, la original.

### L5. Casos menores que aparecen en la misma pasada

- Enlaces relativos (`/slug`) sin dominio: funcionan, pero conviene normalizar.
- Enlaces con fecha (`/2016/10/04/slug/`) de una estructura de permalinks antigua.
- **Autoenlace vía redirección:** el enlace apunta a una URL vieja cuya 301 lleva al
  propio post. Al "corregir" con el destino final queda un autoenlace: quitar el `<a>`.
- Enlace a contenido eliminado a propósito (410): quitar el enlace, conservar el texto.
- Enlaces externos `http://`: pasar a `https://` solo los que responden 200 por HTTPS
  (en una muestra real, 158 de 231).

---

## Contenido

### C1. Shortcode de plugin desinstalado visible en crudo

**Qué es:** se desactiva o desinstala un plugin (cajas de afiliados, tablas, sliders) y
sus shortcodes quedan en el contenido. WordPress no los procesa y `wptexturize` cambia
las comillas: el lector ve `[amazon box=»1789098173″]`. Caso real: 778 shortcodes en
602 posts.

**Detección:** listar los nombres de shortcode usados (`\[([a-z_][\w-]*)`) y compararlos
con los registrados (`$shortcode_tags` vía endpoint temporal o la lista de plugins
activos). Confirmar en `content.rendered` que se ven.

**Corrección:** decidir con el usuario si se reactiva el plugin o se quitan. Al quitar:

- Sustituir el tramo (shortcode + espacios alrededor) por **un único salto de párrafo**
  en el estilo de saltos del post (`\r\n\r\n` o `\n\n`); vacío al inicio/fin; un espacio
  si estaba en línea entre texto.
- Fusionar tramos contiguos (caja + encabezado + otra caja) para no dejar saltos dobles.
- Quitar también los encabezados que solo existían para la caja: un encabezado
  inmediatamente antes del shortcode y seguido de otro encabezado de nivel igual o
  superior, o del final del contenido (incluye "Recomendamos" vacíos y H2 con el nombre
  del producto). Caso real: 304 encabezados.
- Cubrir variantes sin `]` de cierre.
- Verificar en `content.rendered` que no queda el shortcode ni hay textos pegados.

`scripts/strip_shortcode.py` implementa estas reglas.

### C2. Shortcode dentro de anuncios

**Qué es:** tras limpiar los posts, la caja sigue apareciendo en algunas páginas: viene
de un anuncio de Advanced Ads cuyo contenido completo es el shortcode, insertado con
`[the_ad id]` o rotando en un grupo.

**Detección:** buscar en `post_content` de `post_type='advanced_ads'`; el HTML lo
delata por el envoltorio `*-highlight-wrapper`.

**Corrección:** pasar esos anuncios a borrador (no dejarlos vacíos). `[the_ad id]` de un
anuncio en borrador no imprime nada y el grupo rota entre los demás.

### C3. Traducción con el cuerpo en otro idioma

**Qué es:** el flujo de traducción tradujo título, slug y extracto, pero el cuerpo quedó
en el idioma original (o en un tercer idioma: un PT con el cuerpo en FR). hreflang y
`html lang` declaran un idioma y el texto es otro.

**Detección:** detector simple de idioma por palabras vacías sobre el texto visible
(>80 palabras). Ojo: listas de palabras compartidas entre ES y PT (`que`, `para`, `uma`)
dan falsos positivos; usar palabras exclusivas (`los`, `las`, `del`, `según`).

**Corrección:** retraducir el cuerpo desde el original del grupo (no desde la traducción
mala), conservar estructura, shortcodes, imágenes y bloques JSON-LD (traducidos y
válidos), y llevar los enlaces internos a la versión del idioma (regla L2). Verificar
conteos de `<img>`, `<a>`, `<h2>`, `<h3>` y shortcodes contra el original.

Excepción: contenido patrocinado publicado en otro idioma. Cambiarle el idioma cambia la
URL contratada; es decisión del negocio, no corrección técnica.

### C4. Residuos de la interfaz de un chat de IA

**Qué es:** texto copiado desde la interfaz web de un chat con todo su marcado:
`<article data-turn-id="..." data-testid="conversation-turn-4">`, decenas de clases de
Tailwind, `data-message-author-role`, `data-writing-block`.

**Detección:** regex sobre esas marcas. Variante más discreta: atributos `data-start` y
`data-end` (y clases `whitespace-pre-wrap break-words`) sueltos en `<p>` y `<li>`, sin
contenedor `<article>`; también es texto copiado de un chat. Variante antigua (2023):
contenedores `<div class="... agent-turn">`, `flex flex-grow flex-col`, `flex-col gap-1`
y `markdown prose`. Al desenvolverlos, colapsar siempre los saltos triples resultantes.

**Corrección:** desenvolver solo los contenedores marcados (`article`, `div`, `section`,
`span`) junto con su cierre emparejado; en las etiquetas con significado (`p`, `h2`,
`em`, `li`, `ol`, `ul`, `b`, `i`) borrar solo los atributos. Si al quitar contenedores
quedan tres o más saltos seguidos, colapsarlos a uno de párrafo. Trabajar sobre el texto exacto (sin reserializar con un
parser HTML) y exigir que el texto visible sea idéntico antes y después.

### C5. Saltos de línea escapados

**Qué es:** el contenido se guardó con `\n` literales (barra invertida + n), típico de un
JSON mal desescapado al publicar por API. Todo el post se ve en un bloque con `\n\n`
visibles y el JSON-LD queda inválido.

**Detección:** contar `chr(92)+'n'` en el crudo y en el texto visible renderizado.

**Corrección:** reemplazar `\r\n`, `\n` y `\t` literales por los caracteres reales;
comprobar después que el JSON-LD es válido.

### C6. JSON-LD inline inválido

Escapes no válidos en JSON (`\'`), bloques vacíos, `<p>` metidos por `wpautop` en un
script con líneas en blanco. Validar cada bloque con `json.loads`; corregir el escape o
compactar el script en una línea.

### C7. Script ofuscado inyectado en el contenido

**Qué es:** un `<script>` dentro de `post_content` que arma la URL por partes
(`x_=("us")+("ta"); x_+="t"+(".")...`) y hace `document.createElement("script")` +
`appendChild`. Carga un dominio externo de rastreo o fraude publicitario en cada visita.

**Detección:** scripts no JSON-LD con `createElement|appendChild|eval(|atob(|fromCharCode|document.write`.
Descartar los propios (widgets del sitio) por contexto.

**Corrección:** eliminar el `<script>` completo; avisar como hallazgo de seguridad
(revisar cómo entró: cuenta comprometida, plugin, copia de contenido) y buscar el mismo
patrón en opciones y widgets.

### C8. Páginas de un plugin desinstalado (membresías, tiendas, formularios)

Se desinstala un plugin que creaba sus propias páginas (Paid Memberships Pro: pago,
niveles, login) y las páginas siguen publicadas, indexables y en el sitemap, mostrando
sus shortcodes en crudo (`[pmpro_checkout]`). Detección: shortcodes no registrados en
páginas (no solo en posts). Corrección: borrador + 301 a la portada o a la página que
sustituya la función.

### L6. Slug cambiado sin redirección

Al optimizar un post se cambió su slug y no se creó la 301: la URL antigua (la que
tenía enlaces externos y posición en Google) da 404. Aparece como enlace interno roto
cuyo destino correcto es un post existente con slug casi igual. Corrección: 301 de la URL
antigua a la nueva y reemplazo de los enlaces internos. Revisar en GSC si hay más URLs que
daban clics y hoy responden 404.

### C9. Receta recreada en el idioma destino (duplicado por un proceso de traducción)

El pipeline que traduce del sitio A al sitio B no detecta que la receta ya existía en B
con otro slug y crea una segunda versión. Quedan dos URLs en B que canibalizan, y el
hreflang de A apunta a una mientras otra parte del contenido enlaza a la otra (pares no
recíprocos). Detección: títulos duplicados o casi duplicados en B y la comprobación de
reciprocidad del hreflang entre los dos volcados. Corrección: no aplicar a ciegas "gana la
de más clics"; pesar clics y, además, cuántos enlaces internos y del otro sitio apuntan a
cada una y cuál tiene el contenido más completo. Si la vieja tiene clics marginales,
quedarse con la nueva (301 vieja → nueva); si la vieja tiene tráfico real, al revés y
actualizar los enlaces.

### P8. Caché de CDN envenenada con la página antibot del hosting

Una regla de caché de HTML con TTL forzado (`edge_ttl: override_origin`) ignora el
`Cache-Control: private, no-store` de la página de comprobación de Imunify360/similar
(`One moment, please...`, `请稍候…`, recarga cada 5 s) y la sirve como si fuera la
página real, a visitantes y a Googlebot, durante todo el TTL. Detección: pedir la portada
y URLs clave con varios UA; un `<title>` de espera, sin canonical ni H1, con
`cf-cache-status: HIT` y `age` alto. Corrección inmediata: purgar esa URL. Corrección de
raíz: `edge_ttl: respect_origin`; si el origen no manda `Cache-Control` en el HTML normal,
Cloudflare lo sigue cacheando (verificar MISS→HIT), y deja de congelar lo marcado no-store.

### H4. Hreflang entre dos dominios armado con "el primer enlace"

Un snippet que genera el hreflang tomando el primer enlace al otro dominio que aparezca en
el contenido es frágil: si el cuerpo enlaza antes a otro artículo del otro sitio, el par
queda mal. Además, una URL fija con `www` en la portada apunta a una redirección si el
otro dominio es sin www. Verificar reciprocidad cruzando los dos volcados (para cada post
de A, el primer enlace a B debe existir en B y su primer enlace a A debe volver al post).

---

## WPML y estructura

### H1. Posts publicados sin idioma en WPML

**Qué es:** duplicados de traducciones creados al fallar un flujo (el post se creó pero
no se vinculó). No tienen fila en `icl_translations`, así que no salen en la REST de
ningún idioma, pero Rank Math sí los mete en el sitemap con una URL sin prefijo que
redirige. A veces comparten slug con el original y la URL la sirve el bueno.

**Detección:** URLs del sitemap que no están en el volcado → SQL de posts publicados sin
fila en `icl_translations` (ver internals). Comparar con el grupo de traducción del
artículo para saber cuál es el bueno (`postid-N` en el `body class` de la URL servida).

**Corrección:** papelera + 301 a la versión correcta del grupo (si comparte slug con el
bueno, solo papelera). Un duplicado con `-2` en el slug y sin grupo es el mismo caso.

### H2. Strings de portada sin traducir

**Qué es:** la portada de cada idioma muestra title y meta description en el idioma
original porque las strings de WPML String Translation existen pero no tienen
traducción: `Tagline` (context `WP`, usado por `%sitedesc%` en el title de Rank Math),
`[rank-math-options-titles]homepage_description` y
`[rank-math-options-titles]homepage_facebook_description`.

**Corrección:** `icl_add_string_translation($string_id, $lang, $valor, 10)`. Verificar en
vivo title, meta description y og:description de cada portada. No traducir el nombre
del sitio si es marca.

### H3. Plugin de enlaces externos y `home_url()` por idioma

**Qué es:** WP External Links decide "interno" comparando con `home_url('')`, que en una
traducción es `https://dominio/en`. Todo enlace propio fuera del prefijo del idioma
(selector de idioma, logo, enlaces al original, caja de autor) se marca externo y recibe
`rel="external noopener noreferrer"`.

**Corrección:** activar `subdomains_as_internal_links` (compara solo el host). No usar
la lista de exclusiones con "tratar como internos": suele contener enlaces patrocinados
que deben conservar su tratamiento.

---

## Configuración de plugins

### P1. Redirección de adjuntos a una URL obsoleta

Rank Math `attachment_redirect_default` apuntando a `/es` (o a una portada vieja): toda
página de adjunto sin entrada padre redirige a un 404. Se manifiesta en URLs que parecen
posts (un slug de traducción que coincide con el nombre de una imagen). Corregir a la
portada actual.

### P2. Canonical personalizado heredado

`rank_math_canonical_url` con el prefijo viejo, o apuntando a un artículo sin relación
(tres guías de bares canonizadas a "cómo hacer cerveza artesanal"). Rank Math excluye del
sitemap todo post cuyo canonical apunta a otra URL. Quitar el meta si no hay
consolidación real; si la hay (artículos hermanos casi idénticos), conservar y limpiar la
URL.

### P3. Noindex por defecto que tapa contenido nuevo

`pt_page_robots = ['noindex']` con `pt_page_custom_robots = on`: todas las páginas nacen
noindex (útil para legales y membresía). Una herramienta nueva publicada como página
queda fuera del índice y del sitemap. Excepción por página con
`rank_math_robots = ['index']`; no tocar la regla global.

### P4. Plugin social que duplica Open Graph

Blog2Social con `og_active` y `card_active` imprime su propio bloque (`og:title`,
`og:url` relativo, `og:article:published_time` con espacio) además del de Rank Math.
Desactivar ambos en `B2S_PLUGIN_GENERAL_OPTIONS` cuando el plugin SEO ya los emite.

### P5. robots.txt físico con bloques de plugins

- Plugins de Content-Signal añaden bloques `# BEGIN ... # END` con su propio
  `User-Agent: *`; tras dos guardados con valores distintos quedan señales opuestas.
  Dejar un solo bloque (el más reciente), conservando los marcadores para que el plugin
  lo reemplace en lugar de duplicarlo.
- Grupos de bots con solo `Crawl-delay` no heredan los `Disallow` del grupo `*`.
- `Disallow: /tag/` no cubre `/en/tag/`: añadir `/*/tag/` en multilingües con prefijo.
- Si hay archivo físico, el robots.txt virtual de WordPress/Rank Math no se sirve.

### P6. WAF que bloquea feeds

Reglas "anti-bot" genéricas copiadas entre zonas con `uri.path contains "/feed/"`:
lectores RSS y agregadores no verificados reciben 403, aunque el robots.txt diga lo
contrario. Quitar la condición; el resto de la regla (impostores de GPTBot desde redes
que no son de OpenAI, por ejemplo) suele estar bien.

### P7. Cabecera Link a llms.txt por idioma

Plugins de visibilidad IA añaden `Link: <home_url>/llms.txt; rel="describedby"`; en las
traducciones apunta a `/en/llms.txt`, que no existe. Redirección en el edge
`/(en|pt-br|fr)/llms.txt` → `/llms.txt`.
