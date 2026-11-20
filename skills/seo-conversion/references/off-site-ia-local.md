# SEO local, off-page comercial y GEO en búsquedas de compra

Fuentes leídas el 23/10/2026. Niveles entre corchetes (ver `fuentes.md`).

## 1. SEO local y Perfil de Empresa (frente 9)

**Métricas de la ficha** [Documentado, support.google.com/business/answer/9918094]: llamadas = toques en el botón de
llamar (no llamadas atendidas ni marcadas a mano); mensajes = conversaciones; reservas = solo vía proveedor integrado;
rutas = solicitudes depuradas; clics al sitio. **Los datos mezclan orgánico y Google Ads.**

Consecuencias para el diagnóstico:
- Llamadas, mensajes, rutas y reservas desde la ficha nunca llegan a GA4. Pide el informe de rendimiento de la ficha
  del mismo período y súmalo como conversiones fuera del sitio. "El SEO local no genera leads" no se concluye con GA4.
- Revisa si el enlace del sitio en la ficha lleva UTM y compruébalo con un clic real. Sin UTM, el tráfico de la ficha
  se mezcla con el orgánico y la home parece convertir más de lo que convierte.
- Para leads reales, pide el registro de llamadas de la centralita o del proveedor de seguimiento.

**Teléfono y seguimiento de llamadas.** Las directrices piden número local, bajo control directo del negocio, sin
redirección a landings; los números adicionales están permitidos [Documentado, answer/3038177]. Google no habla del
seguimiento de llamadas por nombre: la práctica de número de seguimiento como principal y el real como adicional viene
de proveedores [Proveedor]. Preséntalo como riesgo de consistencia, no como riesgo de ranking demostrado.

**Ranking local.** Relevancia, distancia y prominencia; las reseñas y su nota ayudan; no se puede pagar por mejor
posición [Documentado, answer/7091].

**Qué mueve la conversión local.** Encuesta Whitespark 2026 (47 expertos, opinión, no correlación): encabezan la nota de
Google de 4 a 5, el sentimiento positivo del texto, la proximidad, el sitio móvil y la cantidad de reseñas con texto
[Estudio de opinión experta, 06/11/2025]. BrightLocal 2026 (1.002 adultos de EE. UU.): 97% lee reseñas de negocios
locales; 74% busca reseñas de los últimos 3 meses; 31% solo usa negocios de 4,5 o más (17% antes); tras leer reseñas
positivas, 54% visita el sitio; 45% usa ya IA generativa para recomendaciones locales (6% el año anterior) [Estudio,
11/02/2026]. No hay estudio serio sobre qué parte de los leads locales nace en la ficha frente al sitio [No confirmado]:
se mide en el cliente.

**Reseñas: lo prohibido.** Reseñas pagadas o incentivadas, filtrar quién puede reseñar (gating), reseñas de empleados
[Documentado, contributionpolicy/answer/7400114]. Es riesgo de eliminación de reseñas y de la ficha.

**Páginas por ciudad.** Si solo cambian el nombre de la ciudad y empujan a la misma conversión, encajan en el ejemplo de
doorway de Google (ver `escala-pagado-pruebas.md`).

## 2. Off-page comercial: reseñas, directorios y comparadores (frente 10)

En búsquedas de compra B2B el top suele estar ocupado por listados "mejores X", comparadores y directorios. Estar bien
en esas páginas es captación directa, y además alimenta a la IA.

- G2 compró Capterra, GetApp y Software Advice (anuncio 29/01/2026, cierre 05/02/2026) [Documentado, comunicado de G2 y
  10-K de Gartner vía prensa]. Hoy son una sola red: contar presencia en "cuatro plataformas" sobrestima la diversidad.
- Citas de IA en consultas de software B2B: los sitios de reseñas pesan 7% a 9% de las citas en dos estudios de 2026
  (Overthink, ~1.260 prompts en 4 motores: red G2 8,0%; Growfusely, 128 consultas: 7,3%). En Overthink, el 70,8% de las
  páginas citadas lleva "best", "top" o similar en el título, y el peso de cada tipo de fuente cambia mucho por motor
  [Estudio, 14/07/2026 y 28/07/2026]. No prometas que estar en G2 o Capterra garantiza citas.
- Sin datos con método sobre Clutch o directorios de servicios [No confirmado]: se mide qué aparece en la SERP y en las
  respuestas de IA del cliente.

**Comparativas propias ("X vs Y", "alternativas a X", "mejores X").** Google pide evidencia de uso propio, explicar qué
diferencia a cada opción, justificar cada posición y que la lista se sostenga sola [Documentado, write-high-quality-reviews
y reviews-system, 10/12/2025]. El sistema de reseñas puede evaluar todo el sitio si hay mucho contenido de ese tipo. No
hay regla que prohíba que una empresa se compare con su competencia; sí aplica el mismo estándar aunque gane el cliente.
La ejecución la cubre `seo-competitor-pages`.

## 3. GEO en búsquedas comerciales (frente 11)

La pregunta no es "¿me citan?" sino "¿me recomiendan cuando alguien pide proveedor de X?".
1. Arma la lista de prompts comerciales del cliente (categoría, comparación, "mejor proveedor de X en <país>", problema
   que resuelve) y mide por motor (`geo-platform-audit`, `seo-ai-search-share-of-voice`). No extrapoles de ChatGPT a AI
   Overviews: las fuentes citadas difieren mucho.
2. Anota qué citan cuando no aparece el cliente: páginas dedicadas de competidores (por normativa, por partner, por
   sector), listados, directorios, mapas. Eso dice qué tipo de página falta o dónde hay que estar.
3. Mide el resultado en sesiones y eventos clave del canal "AI Assistant" (`ga4-ai-traffic`), en números absolutos.

La implementación de entidad (Wikidata, schema de organización, `sameAs`) la cubre `geo-ai-discoverability`; la
citabilidad de un artículo, `blog-geo`.
