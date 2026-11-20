# Páginas a escala, herramientas gratuitas, orgánico frente a pagado y pruebas

Fuentes leídas el 23/10/2026. Niveles entre corchetes (ver `fuentes.md`).

## 1. Páginas de compra a escala (frente 13)

Integraciones, alternativas, sectores, ubicaciones, rutas: el formato que más leads suele traer en SaaS, y el de más
riesgo.

- Política vigente de *scaled content abuse*: muchas páginas generadas para manipular rankings y no para ayudar,
  "no matter how it's created" [Documentado, developers.google.com/search/docs/essentials/spam-policies, actualizada
  28/08/2026; origen en el blog del 05/03/2024].
- *Doorway abuse*: páginas para búsquedas similares, como páginas por región o ciudad que llevan a una misma página, o
  páginas casi iguales más parecidas a resultados de búsqueda que a una jerarquía navegable [Documentado, misma URL].
- Contenido generado con IA: precisión, calidad y relevancia, con revisión manual de los datos [Documentado,
  using-gen-ai-content, 01/10/2026].

Prueba operativa por página: ¿aporta algo que su hermana no tiene, para quien llega desde esa búsqueda (datos propios,
condiciones, ejemplos, precios, integraciones reales)? Si solo cambia una variable, es riesgo alto. Lanzar como piloto
(pocas páginas), medir a 28 días y escalar con evidencia. No hay casos independientes con método que prueben éxito o
penalización de SEO programático [No confirmado]: los casos que circulan vienen de proveedores.

## 2. Herramientas gratuitas y lead magnets (frente 14)

Una herramienta (calculadora, rastreador, verificador, plantilla) puede ganar SERP de "cómo hacer" o de categoría donde
un texto no gana, y captar contactos con intención. No hay datos primarios verificables de tráfico y leads de
herramientas gratuitas [No confirmado]: se propone como hipótesis, con medición propia (sesiones orgánicas, uso, leads
atribuidos). Diseño y alcance con `free-tool-strategy` y `lead-magnets`. Revisar la SERP antes: si el top lo ocupan
herramientas, un artículo no compite.

## 3. Orgánico frente a pagado (frente 15)

Análisis, no gestión de pujas (eso es del área de pagado).
- Estudios de Google: 89% de los clics de anuncios es incremental en promedio (2011); con orgánico en posición 1 baja a
  50%, en posiciones 2 a 4 es 81% (2012) [Estudio, autor interesado: Google vende los anuncios].
- En búsquedas de marca sin competencia, la incrementalidad es casi nula (eBay, Econometrica 2015) o de 1% a 4%
  (Bing, Marketing Science 2018) [Estudio]. No usar el 89% para justificar anuncios donde ya se rankea.
- El informe "Paid & organic" de Google Ads (con Search Console vinculado) muestra solapamiento consulta a consulta, solo
  anuncios de texto y solo desde la vinculación; no mide incrementalidad [Documentado, google-ads/answer/3097241].
  Incrementalidad solo con prueba de pausa con control.
- Lo útil para el SEO: búsquedas de compra donde se paga y no se rankea (oportunidad orgánica con demanda probada y
  conversión medida en Ads) y búsquedas donde se rankea primero y se paga sin competencia (dato para el área de pagado).

## 4. Pruebas con grupo de control (frente 16)

- La unidad es la página, no el usuario: Googlebot es un solo visitante. Se agrupan páginas de la misma plantilla en
  control y variante y se pronostica la variante desde el control [Proveedor con método publicado, SearchPilot,
  29/07/2026].
- Un antes y después dice que algo cambió, no por qué: updates, estacionalidad y competencia se mueven a la vez.
- Sin mínimo publicado de tamaño o duración [No confirmado]. Regla prudente: muchas páginas homogéneas, tráfico
  suficiente para que el intervalo excluya cero, al menos un recrawl completo de las variantes y semanas completas.
- Riesgos: core update durante la prueba, enlazado interno que mezcla grupos, impresiones de GSC infladas entre mayo
  de 2025 y abril de 2026 (medir en clics o sesiones).
- La intuición falla: en un ejercicio de predicción de SearchPilot, el público acertó el signo del efecto una de cada
  tres veces [Proveedor]. Por eso se prueba.

Para pocas páginas (un sitio B2B con 10 servicios), un grupo de control de páginas parecidas que no se tocan, más el
cruce con el calendario de updates, es lo honesto; se reporta como evidencia débil.
