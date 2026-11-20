# Intención de compra, páginas de dinero y SERP

Fuentes leídas el 23/10/2026. Niveles entre corchetes (ver `fuentes.md`).

## 1. Intención de compra (frente 2)

Método de base: priorizar por intención de compra, no por volumen (Pain Point SEO, Grow and Convert, actualizado
17/03/2026) [Proveedor con datos propios]. Orden de prioridad: **categoría y comparación** ("software de X", "X vs Y",
"alternativas a X", "mejores X") por encima de **cómo hacer** con intención de herramienta ("cómo controlar el
combustible de una flota"), y el contenido informativo al final. Su dato: posts de fondo de embudo con 4,78% de
conversión frente a 0,19% de los de tope, en su cartera de clientes y contando solo registros o formularios de
producto. Vale como dirección, no como benchmark.

Niveles que usa `intencion_gsc.py`, en orden de prioridad:

| Nivel | Señales (es/en/pt) | Página que suele ganar |
|---|---|---|
| Transaccional | precio, cotizar, contratar, comprar, demo, prueba gratis | servicio, precios, ficha |
| Comparación | vs, alternativas, mejores, comparativa, opiniones | comparativa, listado de terceros |
| Definición | qué es, what is, o que é | artículo, glosario |
| Categoría | software, sistema, servicio, empresa de, proveedor | servicio, categoría, directorio |
| Cómo hacer | cómo, how to, paso a paso | guía, que puede llevar a una herramienta |
| Informativa | tipos de, ejemplos, ley, KPI, guía | artículo |

Una búsqueda de categoría puede ser informativa en la SERP ("servicios cloud" puede devolver definiciones). El nivel
lo confirma la SERP, no la palabra.

**Una comparación con cero volumen puede ser la que más convierte** (caso citado por Grow and Convert): no descartar
"X vs Y" o "alternativas a X" por volumen bajo cuando X es un competidor directo.

## 2. Tipo de página frente a la SERP (frente 3)

Para cada búsqueda de compra con demanda: mirar el top 5 móvil del país (`seo-sxo`, `seo-dataforseo`) y anotar el tipo
de página que gana (servicio, categoría, comparador, directorio, lista "mejores X", herramienta gratuita). Si el tipo
que gana no existe en el sitio, la acción es crear ese tipo o estar presente en las páginas que ganan (frente 10), no
reescribir la página equivocada.

## 3. El comprador que prefiere informarse solo

- El 67% de los compradores B2B prefiere comprar sin vendedor (61% el año anterior); el 45% usó IA en su última compra
  [Estudio, Gartner, encuesta de 646 compradores, 09/03/2026]. Para tareas de encaje ("¿sirve para mi empresa?") siguen
  prefiriendo hablar con el proveedor [Estudio, Gartner, 25/06/2025].
- Sin precios visibles, los usuarios se van a la competencia; mostrar al menos niveles o precios de escenarios típicos;
  no exigir registro antes de dar información [Estudio, NN/g, informe B2B y artículo "Show prices for common scenarios"].
- Implicación: una página de dinero B2B tiene que responder sin pedir datos qué hace, para quién, cuánto cuesta (o de
  qué depende), cómo se compara y qué pasa al pedir la demo. Precio y prueba gratis son decisiones de negocio: se
  documenta la SERP (qué ofrecen los que ganan) y se registra como dependencia.

## 4. Salud técnica de las páginas de dinero (frente 4)

`paginas_dinero.py` y luego la skill técnica que corresponda. Mínimo: 200 sin redirección, indexable, canonical propio,
en el sitemap, rastreada recientemente (URL Inspection: último rastreo), un H1, CTA y formulario visibles sin
JavaScript o comprobados con navegador, CWV del formulario en móvil. Una página de servicio que Google no rastrea
desde hace dos meses no se arregla con contenido.

## 5. CRO de página y formulario (frente 5)

Lo ejecutan `page-cro` y `form-cro`. Lo que aporta el ángulo SEO:
- Coherencia entre la búsqueda y la promesa del primer pantallazo (la consulta que trae la visita está en GSC).
- Móvil primero: banner de cookies que tapa el CTA, encabezado sin CTA, formulario al final de páginas largas,
  agendamiento que pide datos antes de mostrar disponibilidad. Comprobarlo con capturas reales.
- Prueba y confianza cerca del CTA: casos con cifras, clientes, certificaciones y normas que el comprador busca.

## 6. Enlazado del contenido a las páginas de dinero (frente 6)

`enlazado_dinero.py`. Cuenta por separado los enlaces de menú y pie y los que están dentro del contenido. Prioriza las
páginas con más impresiones que no enlazan ninguna página de dinero. El enlace va en el párrafo donde el problema del
lector coincide con lo que se vende, con un ancla descriptiva; no en una caja genérica al final. Medir después la
conversión asistida por artículo (primer y último clic).

## 7. Snippet como filtro del clic (frente 7)

- Google usa el `<title>` cerca del 87% de las veces y lo reescribe a partir de H1, anclas y otras fuentes
  [Documentado, blog Search Central 17/09/2021 y title-link, 10/12/2025]. Si lo reescribe, el problema es la
  alineación title, H1 y contenido. La meta description es una propuesta: el snippet cambia por consulta
  [Documentado, snippet, 20/04/2026].
- Que un title "que filtra" baje clics y suba la conversión es hipótesis: no hay estudio público con método
  [No confirmado]. Se prueba con datos del sitio.
- Estrellas: los testimonios propios en `Organization` o `LocalBusiness` no son elegibles, tampoco vía widget de
  terceros [Documentado, review-snippet, 08/09/2026]. Merchant listings y product snippets exigen página de un solo
  producto [Documentado, product-snippet, 08/09/2026]. `SoftwareApplication` exige `offers.price` y reseñas válidas.

## 8. SERP de marca (frente 8)

Lo que el comprador ve al buscar el nombre: ficha, reseñas, Knowledge Panel, anuncios de competidores, resultados de
terceros. Google Ads permite usar marcas ajenas como keyword [Documentado, adspolicy/answer/6118]. En Bing, sin
competidores pujando, el anuncio de marca propio suma 1% a 4% de clics; si hay competidores y la marca no se anuncia,
estos se llevan 18% a 42% [Estudio, Simonov, Nosko y Rao, Marketing Science 2018]. Revisar si hay competidores en la
SERP de marca antes de opinar sobre la puja (la puja la decide el área de pagado).

## 9. Landings por país e idioma (frente 12)

hreflang correcto (`seo-hreflang`) no basta: la oferta tiene que ser local (moneda, teléfono y canal del país,
normativa citada, prueba gratis si los que ganan la ofrecen). Una página traducida con la oferta de otro país convierte
como página de otro país.
