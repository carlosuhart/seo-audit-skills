---
name: javascript-seo
description: >
  Auditoría técnica de sitios renderizados con frameworks JavaScript (React/Next.js,
  Vue/Nuxt y equivalentes, desplegados en Vercel/Netlify u hosting similar sin CMS
  tradicional). Cubre hidratación incompleta, contenido gateado por interacción de UI
  invisible a cualquier crawler, soft-404 sistémico por rutas catch-all, y la
  implementación de canonical/hreflang/cabeceras cuando no existe un plugin SEO que
  las genere — todo el trabajo recae en configuración de framework y componentes.
user-invokable: false
---

# JavaScript SEO — Guía Técnica (frameworks React/Vue, sin CMS)

> A diferencia de WordPress/PrestaShop, aquí no hay un plugin SEO que resuelva meta
> tags, canonical o schema por defecto — cada señal depende de que el framework la
> genere explícitamente, y los bugs más graves no son de configuración sino de
> arquitectura de renderizado.

---

## Cuándo aplica esta guía

Sitio construido con un framework de componentes (React, Vue, Svelte) donde:
- No hay un `wp-admin`, panel de plugin SEO, ni editor de contenido tradicional
- El HTML se genera por SSR/SSG (Next.js, Nuxt, Astro) o se hidrata en el cliente
- El despliegue vive en Vercel, Netlify o similar, con configuración vía archivo de
  proyecto (`next.config.js`, `vercel.json`) en lugar de un panel de administración

**Detección rápida:** buscar en el HTML crudo (`curl`, sin ejecutar JS) marcadores del
framework: `self.__next_f.push(...)` (Next.js App Router), `data-server-rendered`
(Nuxt), o un `<div id="root">`/`<div id="app">` casi vacío seguido de bundles JS
grandes. Si el HTML crudo trae contenido real (headings, enlaces, texto), es SSR/SSG
funcionando bien — si trae solo el shell y el contenido aparece al ejecutar JS, es
CSR (client-side rendering) puro, con todos los riesgos de esta guía.

---

## Hidratación incompleta — el bug más grave y menos obvio

**Síntoma:** navegación, encabezados (H1/H2) y/o datos estructurados JSON-LD no
existen en el HTML que entrega el servidor — solo dentro del payload de hidratación
que React/Vue usa para reconstruir el árbol en el cliente (patrón típico en Next.js:
`self.__next_f.push(['$', 'a', null, {href: '/ruta', children: 'Texto'}])` — la data
existe, pero nunca se serializa como una etiqueta `<a href>` real en el HTML servido).

Esto **no es lo mismo que "hace falta ejecutar JS para ver el contenido"**. Un sitio
JS que hidrata bien produce, tras la ejecución, el mismo árbol semántico que si
hubiera sido HTML estático desde el principio (`<a href>` reales, `<h1>` reales,
`<script type="application/ld+json">` reales). Cuando ni siquiera un crawler que
ejecuta JS encuentra esas etiquetas, el problema es un **hydration mismatch**: el
componente probablemente usa `<div onClick={...}>` en lugar de `<a href="...">`, o
genera el heading/schema en un nodo que el diffing de hidratación nunca inserta al
DOM real servido por el navegador. Confirmarlo en el código requiere que Desarrollo
revise el componente — desde fuera solo se puede documentar el síntoma.

### Método de verificación en 3 pasos, siempre los 3

1. **HTML crudo, sin JS:** `curl` la URL y buscar los elementos esperados
   (`grep -c "<h1"`, `grep -c "application/ld+json"`, contar `<a href=`). Si da 0,
   no basta para concluir el bug — puede ser simplemente CSR normal.
2. **Crawler que ejecuta JS** (Screaming Frog en modo JS Rendering, o el crawler de
   una herramienta de auditoría con soporte JS): si este *también* reporta 0 enlaces
   salientes / 0 H1 / 0 schema, el problema ya no es "falta renderizar" — es hidratación
   rota. Si el crawler JS sí encuentra el contenido pero el curl crudo no, es CSR
   normal (afecta a bots que no ejecutan JS, pero no es hidratación rota).
3. **Dato real de Google** (URL Inspection API o informe de Cobertura en Search
   Console): confirma si Google, con su propio renderizado (segunda ola de indexación),
   está llegando al contenido o no. Un sitio con hidratación rota suele mostrar 0
   páginas indexadas más allá de la home, o "Detectada, actualmente sin indexar" en
   cascada.

**Por qué corregir esto resuelve varios síntomas de una sola vez:** un solo bug de
hidratación en un componente compartido (nav, header) puede romper simultáneamente
navegación, jerarquía de encabezados y datos estructurados en todo el sitio — no
tratarlos como 3 hallazgos independientes si la causa raíz es la misma.

---

## Contenido gateado por interacción de UI — invisible a TODO crawler, incluidos los que ejecutan JS

Distinto del punto anterior: aquí el contenido **si** existe como HTML real y
enlazable, pero solo se revela tras una interacción de usuario que ningún crawler
simula — típicamente un menú desplegable (`dropdown`) que un botón con JavaScript
abre al hacer click, y cuyos elementos internos nunca aparecen en el HTML servido
hasta que ese click ocurre.

**Esto rompe la asunción habitual de "un crawler que ejecuta JS ya ve todo lo que ve
un usuario".** No es así: un crawler con soporte JS renderiza la página, ejecuta
scripts y espera a que la red se estabilice, pero no simula clicks arbitrarios de UI
salvo en configuraciones muy específicas y limitadas (y ningún crawler de propósito
general lo hace por defecto). Si el único camino hacia una URL es "click en este
botón para desplegar el menú", esa URL queda huérfana para efectos prácticos de
descubrimiento — sin importar cuán bien renderice JS el crawler.

### Cómo se detecta (y por qué hace falta más de un método)

1. `curl` sobre la página que contiene el menú: si los `<a href>` de los items del
   dropdown no aparecen en el HTML crudo, es la primera señal.
2. Revisar el `<footer>` u otras rutas alternativas de descubrimiento por si el
   enlace existe en otro lugar del sitio (a veces sí, y el hallazgo real es solo que
   falta desde la navegación principal).
3. Cruzar contra el resultado de un crawler que ejecuta JS real (no solo curl): si
   tampoco las encuentra pese a ejecutar JavaScript, confirma que el bloqueo es la
   interacción, no la falta de renderizado.
4. Verificar en Search Console (URL Inspection) que Google reporta la URL como
   "Unknown"/nunca rastreada — no solo "Descubierta, sin indexar" (que implicaría que
   sí la encontró por algún camino).

**Falso positivo a evitar:** un primer chequeo de enlaces con una regexp poco
delimitada (buscar "cualquier href" en todo el documento) puede capturar hasta el
final del `<body>`, incluidos bloques `<script>` con JSON de hidratación que
mencionan la URL como dato — sin que exista un `<a href>` real. Escopar la búsqueda
al elemento HTML real (`<nav>`, `<footer>`) antes de concluir "sí hay enlace".

**Fix correcto:** el botón que abre/cierra el menú puede seguir siendo interactivo
(UX sin cambios) — lo que debe cambiar es que cada item del menú exista como
`<a href="...">` real en el HTML servido, independiente de si el dropdown está
abierto o cerrado visualmente. El toggle decide visibilidad (CSS/estado), no
existencia en el DOM.

---

## Soft-404 sistémico por rutas catch-all — dos variantes distintas

Frameworks con rutas dinámicas por segmento (ej. `/[lang]/...` en Next.js App
Router) pueden interpretar **cualquier segmento no reconocido como si fuera un
idioma o parámetro válido**, devolviendo contenido real con HTTP 200 en lugar de un
404 verdadero. Verificar ambas variantes por separado — no son el mismo bug:

**Variante 1 — segmento inventado en nivel superior capturado como si fuera válido:**
una ruta de nivel superior con nombre arbitrario (`/cualquier-cosa`, `/robots.php`)
cae en la ruta dinámica genérica y devuelve el contenido completo de la home con
HTTP 200, incluido `<html lang="cualquier-cosa">`. Es un duplicado exacto de la home
bajo cualquier URL inventada — riesgo de contenido duplicado a escala si algo
(backlinks rotos, typos indexados, scrapers) genera tráfico hacia rutas inexistentes.

**Variante 2 — catch-all interno con página de error real pero código HTTP incorrecto:**
una ruta con segmento válido pero sub-ruta inexistente (`/es/producto-que-no-existe`)
cae en un catch-all interno (`[...not-found]`) que sí renderiza una página "404 - No
encontrado" visualmente distinta a la home, pero **sirviéndola con HTTP 200** en
lugar de 404 real. Google clasifica esto como soft-404 en el informe de Cobertura —
categoría distinta de "duplicado con la home" pero igual de dañina para el crawl
budget.

**Verificación:** probar con curl varias rutas inventadas en ambos niveles
(`/xyz123`, `/es/xyz123`) y comparar el código HTTP real (`curl -o /dev/null -w
"%{http_code}"`) contra el contenido servido. Cualquier combinación de "contenido
real + HTTP 200" en una URL que debería ser 404 es soft-404, sin importar si el
contenido visual es la home o una página de error genérica.

**Fix:** ambas rutas catch-all deben invocar el mecanismo nativo de 404 del
framework (en Next.js App Router, `notFound()` de `next/navigation`) para que el
código de respuesta sea 404 real, no 200.

---

## Canonical y hreflang — sin plugin, todo vía metadata del framework

Sin Yoast/Rank Math generándolo automáticamente, cada página debe declarar su propio
canonical y sus etiquetas hreflang recíprocas de forma explícita en el componente o
capa de metadata del framework (en Next.js App Router, la función
`generateMetadata()` de cada ruta). Ver la skill `canonical` para las reglas
generales (self-referencing, coherencia con sitemap) y `hreflang` para reciprocidad
— lo específico de este stack es que no hay UI de plugin donde verificar la
configuración: solo el HTML servido dice la verdad.

**Patrón de bug frecuente en sitios multi-idioma sin canonical:** una cadena de
redirects de detección de idioma en la raíz (`dominio.com` → `www.dominio.com` →
`www.dominio.com/es`) usando código **307 (temporal)** en el primer salto (la
normalización de host, que debería ser permanente) en lugar de reservar el 307 solo
para el salto que sí depende del visitante (la detección de idioma en sí). Sin
canonical que corrija la señal, Google puede terminar indexando la versión sin
`www`/sin idioma como canonical real, en vez de la URL con idioma que sí tiene
contenido. Confirmar con URL Inspection API sobre las 2-3 variantes de la home —
"Duplicate, Google chose different canonical than user" es la señal directa de este
patrón.

---

## Cabeceras HTTP y redirects — configuración de proyecto, no de plugin

En ausencia de un panel de hosting con UI (tipo cPanel/plugin de cabeceras), las
cabeceras de seguridad y los redirects a nivel de host se declaran en el archivo de
configuración del framework/plataforma de despliegue (`next.config.js` con la
función `headers()`, `vercel.json` con `redirects()`). El comportamiento esperado
(qué código HTTP, qué valores de cabecera) es terreno SEO/seguridad verificable por
curl; el código exacto de esa configuración es responsabilidad de Desarrollo — no
prescribir el archivo de config completo en un hallazgo de auditoría, describir el
resultado esperado y dejar el mecanismo a quien conoce el stack real.

Ver la skill `cache-headers` para cabeceras de cacheo y la ausente en este listado
`ssl-https`/`third-party-scripts` para CSP y HSTS — la única diferencia real en
sitios de este stack es dónde vive la configuración, no qué cabeceras hacen falta.

---

## Performance — atributos que no hacen nada si se aplican mal

**`fetchpriority` solo aplica a elementos que descargan un recurso** (`<img>`,
`<link>`, `<script>`, `<iframe>`). Es un error frecuente proponerlo sobre un
elemento de texto (`<h1>`, `<p>`) cuando ese es el elemento LCP identificado por
Lighthouse/PSI — el navegador lo ignora silenciosamente, sin error visible, dando
una falsa sensación de que el hallazgo ya se resolvió. Si el LCP es texto, la causa
del retraso de renderizado está en otro lado (CSS bloqueante de esa sección, carga
de fuente web bloqueante, o hidratación del lado del cliente que retrasa la
aparición del nodo) — investigar esa causa real, no el atributo.

**CSS render-blocking:** distinguir siempre CSS crítico (necesario para pintar el
contenido above-the-fold) de CSS no crítico antes de recomendar "diferir el CSS" en
bloque — diferir indiscriminadamente puede empeorar el LCP que se está intentando
arreglar, o producir FOUC.

**Polyfills de navegadores antiguos** (`Array.prototype.at/flat/flatMap`,
`Object.fromEntries/hasOwn`, etc.) detectados como peso muerto por Lighthouse: no
recomendar eliminarlos sin que Desarrollo confirme primero el browserslist/navegadores
que el negocio realmente necesita soportar — quitarlos a ciegas puede romper
funcionalidad en navegadores todavía en uso por una parte real de la audiencia.

---

## Checklist de auditoría — sitio JS-rendered sin CMS

```
CRÍTICO
[ ] ¿El HTML crudo (curl, sin JS) trae 0 enlaces/headings/schema pese a que el
    contenido sí se ve en el navegador? → verificar si es CSR normal o hidratación
    rota (cruzar con crawler JS, paso 2 de la sección de hidratación)
[ ] ¿Existen URLs reales solo alcanzables mediante interacción de UI (dropdown,
    tab, acordeón) sin ningún <a href> real en el HTML servido?
[ ] ¿Una ruta inventada de nivel superior devuelve HTTP 200 con contenido de home?
[ ] ¿Una sub-ruta inventada bajo un segmento válido devuelve HTTP 200 en vez de 404?
[ ] ¿El primer salto de una cadena de redirects de normalización de host es 307 en
    vez de 301/308 permanente?

ALTO
[ ] ¿Cada ruta declara su propio canonical self-referencing vía metadata del
    framework, o depende de que el navegador nunca lo pida?
[ ] ¿hreflang recíproco entre versiones de idioma, generado por metadata o ausente
    por completo?
[ ] ¿Cabeceras de seguridad (CSP, X-Frame-Options, etc.) declaradas a nivel de
    proyecto, o completamente ausentes por no existir plugin que las agregue?

MEDIO
[ ] ¿fetchpriority aplicado a un elemento que no descarga recursos?
[ ] ¿CSS diferido en bloque sin distinguir crítico de no crítico?
[ ] ¿Polyfills de navegadores antiguos sin confirmar el browserslist real objetivo?

BAJO
[ ] ¿Imágenes sin width/height explícito (riesgo de CLS) en componentes JS?
[ ] ¿aria-label/aria-labelledby ausente en controles que un CMS con plugin de
    accesibilidad hubiera resuelto por defecto?
```

---

## Referencias

- `canonical`, `hreflang`, `cache-headers`, `ssl-https`, `core-web-vitals`,
  `screaming-frog` — skills complementarias, esta guía cubre lo específico de no
  tener CMS/plugin generando las señales automáticamente.
- Indexación y renderizado en Google: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Diagnóstico de rendering: https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript
- `fetchpriority`: https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/fetchPriority
