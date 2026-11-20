---
name: ads-asistentes-ia
description: >
  Evalúa la publicidad dentro de asistentes de IA para un cliente: qué plataformas venden anuncios hoy
  (ChatGPT Ads, anuncios en Google AI Overviews y AI Mode, Microsoft Copilot, Amazon Alexa for Shopping)
  y cuáles no (Perplexity, Gemini, Meta AI, Grok), elegibilidad por país e idioma, encaje por tipo de
  negocio (B2B, SaaS, e-commerce, local), forma de compra y presupuesto, medición en GA4 y Ads, riesgos
  y coordinación con SEO y GEO. Entrega un informe de evaluación con escenarios y piloto propuesto.
  Use when user says "anuncios en ChatGPT", "publicidad en IA", "publicidad en asistentes de IA",
  "ads en AI Mode", "anuncios en AI Overviews", "Perplexity ads", "Copilot ads", "ChatGPT Ads",
  "AI ads", "advertising in AI assistants" or "¿conviene invertir en anuncios en IA?". Not for
  organic AI citations (seo-geo), generic Google or Meta campaign management (paid-ads) or ad copy
  production (ad-creative).
argument-hint: "<dominio o cliente> [--pais CL|AR|CO|PE|MX|BR|ES] [--tipo b2b|saas|ecommerce|local] [--uso interno|cliente]"
metadata:
  category: paid-ai
  author: Zythos Media
  version: 1.0.0
  fuentes_revisadas: 2026-10-31
  revisar: 2027-01-31
  frecuencia_revision: trimestral
---

# Publicidad en asistentes de IA: evaluación para un cliente

Responde una pregunta de negocio concreta: si un cliente debe invertir en anuncios dentro de asistentes de IA, en cuál, cuándo y con qué presupuesto. No reemplaza al GEO: los anuncios compran una posición etiquetada como "Patrocinado" junto a la respuesta, no una cita dentro de ella.

**Vigencia.** El mercado cambia mes a mes. Las fuentes de esta skill son del 31/10/2026. Si hoy es posterior al 31/01/2027, o si el informe va a un cliente, vuelve a verificar con WebSearch (modo extended) el estado de cada plataforma en el país del cliente antes de afirmar nada, y actualiza `references/plataformas.md` y `references/fuentes.md`.

## Referencia rápida

| Comando | Qué hace |
|---|---|
| `/ads-asistentes-ia estado [--pais XX]` | Tabla de qué plataformas venden anuncios en ese país e idioma, con fuente y fecha |
| `/ads-asistentes-ia evaluar <dominio> --tipo ...` | Flujo completo de evaluación (pasos 0 a 6) e informe con escenarios |
| `/ads-asistentes-ia piloto <plataforma>` | Diseño de un piloto: presupuesto, duración, medición y criterio de decisión |
| `/ads-asistentes-ia actualizar` | Revisión trimestral de fuentes y de la tabla de plataformas |

## Estado del mercado al 31/10/2026 (resumen)

Detalle, formatos y fuentes en `references/plataformas.md` (cargar bajo demanda).

| Plataforma | ¿Vende anuncios? | Chile y LATAM |
|---|---|---|
| ChatGPT Ads (OpenAI) | Sí. 89 países desde el 21/10/2026. Solo planes Free y Go | Chile, Argentina, Colombia y Perú anunciados el 21/10/2026; México y Brasil desde agosto de 2026. OpenAI habla de 14 países LATAM nuevos pero no publicó la lista completa |
| Google, anuncios dentro de AI Overviews y AI Mode | Sí, en 12 países y solo en inglés | No en Chile. Brasil y México anunciados para el cuarto trimestre de 2026, sin idioma confirmado |
| Google, anuncios encima o debajo de AI Overviews | Sí, en todos los países e idiomas donde hay AI Overviews | Sí, incluido Chile (es inventario de Search de siempre) |
| Microsoft Copilot | Sí, vía Microsoft Advertising | Inglés, francés y alemán confirmados; español anunciado en marzo de 2025. Chile y LATAM sin confirmar |
| Amazon Alexa for Shopping (ex Rufus) | Sí, Sponsored Prompts en Estados Unidos | Sin confirmar fuera de Estados Unidos |
| Perplexity | No. Dejó la publicidad (fin de 2025, confirmado en febrero de 2026) | No aplica |
| Gemini (app) | No. Google dice estar "abierto" (abril de 2026) | No aplica |
| Meta AI | No dentro del chat. Usa las conversaciones para segmentar anuncios en Facebook, Instagram, WhatsApp y Messenger | Los anuncios se compran en Meta Ads de siempre |
| Grok (xAI) | Anunciado en 2025, sin documentación de que esté activo | No aplica |

## Flujo de evaluación

### Paso 0. Datos de entrada

Pide o reúne antes de empezar: dominio, país o países objetivo, idioma, tipo de negocio, objetivo (leads, ventas, demanda de marca), CPA o costo por lead aceptable, presupuesto mensual disponible, y si el informe es interno o para el cliente. Si falta el país o el objetivo, pregúntalo: sin eso la evaluación no tiene base.

### Paso 1. Elegibilidad por país e idioma

Para cada plataforma de la tabla, marca uno de tres estados en el país e idioma del cliente:

- **Disponible confirmado**: fuente primaria (blog oficial o centro de ayuda) que nombra el país.
- **Anunciado sin fecha o sin lista completa**: hay anuncio oficial pero el país no aparece nombrado o no tiene fecha.
- **No disponible o sin confirmar**: ninguna fuente lo confirma. Dilo así en el informe, nunca lo infieras.

Regla: en ChatGPT Ads la segmentación por ubicación se consulta en el catálogo de la API (`/geo_lookup/search`) o en Ads Manager. Si el cliente tiene cuenta, verifica ahí que su país aparezca antes de proponer el piloto.

### Paso 2. Encaje por tipo de negocio

| Tipo | Encaje esperado | Plataforma a mirar primero | Advertencia |
|---|---|---|---|
| E-commerce | Alto donde hay formatos de producto | Google (Shopping y Performance Max ya sirven en AI Mode donde está activo), ChatGPT (feeds de producto, oCPC con feed en beta abierta), Copilot (Merchant Center) | Exige feed limpio. Sin feed no hay formato de producto |
| SaaS self-serve | Medio | ChatGPT Ads con objetivo de conversión (registro o prueba) | Mide la activación, no solo el registro |
| B2B con demo o venta consultiva | Bajo a medio, incierto | ChatGPT Ads con piloto acotado | OpenAI no publica benchmarks B2B y la evidencia pública es anecdótica: trata el piloto como exploratorio. Ciclo largo: medir lead calificado en CRM, no clic |
| Local o de servicio | Bajo hoy | Google Search de siempre (los anuncios encima o debajo de AI Overviews ya existen); AI Mode con anuncios de inventario local solo en prueba | ChatGPT no tiene formato local documentado |

Usa la skill `seo-conversion` para clasificar el negocio y saber qué convierte antes de decidir.

### Paso 3. Forma de compra y presupuesto

- **ChatGPT Ads**: Ads Manager en autoservicio o socios tecnológicos y API (`developers.openai.com/ads`). Objetivos Reach (por impresión), Clicks (CPC) y Conversions (oCPC: cobra por clic, optimiza a un evento estándar). Presupuesto diario o total; el mínimo diario depende de la moneda de la cuenta y la documentación no lo publica. Las pujas sugeridas de USD 3 a 5 por clic que circulan vienen de guías de terceros, no de OpenAI: trátalas como referencia a validar en la cuenta. Segmentación por "context hints" (no son palabras clave exactas, hasta 2.000 por grupo), ubicación, plataforma (iOS, Android, web) y audiencias propias (mínimo 25.000 usuarios coincidentes para incluir). Formato documentado: `chat_card` (título de 3 a 50 caracteres, cuerpo hasta 100, imagen) y tarjetas de producto con feed.
- **Google**: no se compra por separado. Search, Shopping y Performance Max existentes son elegibles automáticamente; AI Max for Search y la concordancia amplia acceden a coincidencia contextual, la exacta y de frase solo con intención comercial directa. No se puede excluir ni segmentar solo AI Mode o AI Overviews; se controla con negativas y exclusiones de marca.
- **Copilot**: campañas de Microsoft Advertising elegibles; AI Max en piloto abierto desde mayo de 2026 con opt-in.

Regla de presupuesto: el piloto se dimensiona por el número de conversiones necesarias para decidir, no por un monto fijo. Calcula `presupuesto = conversiones objetivo / tasa de conversión esperada x CPC estimado` y muestra tres escenarios (CPC bajo, medio y alto). Criterio práctico (no es una regla de las plataformas): si el resultado no alcanza unas 20 a 30 conversiones en el periodo, el piloto difícilmente permitirá decidir; dilo.

### Paso 4. Medición en GA4 y en la plataforma

- **ChatGPT Ads**: instala el píxel de OpenAI y la Conversions API (OpenAI la describe como más fiable que el píxel solo). Ventanas por clic de 7, 14 o 30 días (30 por defecto) y por vista de 0 o 1 día (1 por defecto): apaga la de vista o repórtala aparte para no inflar resultados. Configura la plantilla de parámetros (`query_string_template`) con `utm_source`, `utm_medium=cpc` y `utm_campaign`; sin UTM, GA4 puede mezclar el tráfico pagado de ChatGPT con el canal de referencia o de asistentes de IA orgánico.
- **Google**: AI Overviews y AI Mode van agregados en los informes de campaña y de términos de búsqueda, sin segmento propio. No prometas medir el aporte aislado de AI Mode.
- **GA4**: separa en una exploración `chatgpt.com / referral` (orgánico) de `openai / cpc` (pagado). Cruza con la skill `ga4-analysis` y, para el tráfico orgánico desde IA, con `ga4-ai-traffic`.
- **Decisión**: costo por lead calificado o por venta en el CRM, comparado con Google Ads del mismo cliente. Nunca CTR ni CPC solos.

### Paso 5. Riesgos

Volumen limitado en mercados recién abiertos; solo usuarios Free y Go (en B2B, los decisores suelen usar planes de pago sin anuncios); temas sensibles o regulados excluidos (salud, salud mental, política); sin benchmarks públicos de OpenAI; atribución por vista que infla conversiones; en Google, sin control ni reporte separado; datos de rendimiento de Microsoft y Google son internos de cada empresa.

### Paso 6. Informe con escenarios

Usa el formato de salida de abajo. Lenguaje de escenarios ("si el CPC chileno queda cerca del de Google, entonces..."), nunca afirmaciones tajantes sobre resultados futuros.

## Coordinación con SEO y GEO

- **Pago y orgánico son libros separados.** OpenAI declara que los anuncios no influyen en las respuestas y se muestran aparte, etiquetados. Google los etiqueta como "Patrocinado" y los separa visualmente. Ningún estudio público muestra que comprar anuncios aumente las citas orgánicas: un estudio de un proveedor de software SEO (SE Ranking, sin replicar) encontró anuncios en cerca del 26% de 50.006 prompts comerciales y la URL anunciada citada en el 0,09%.
- **El anuncio no reemplaza la cita.** Si la marca ya aparece citada en las respuestas para sus consultas clave, el anuncio en esas mismas consultas puede canibalizar clics que llegarían gratis. Mide la presencia orgánica primero con `seo-ai-search-share-of-voice` o `geo-platform-audit` y prioriza el pago donde la marca no aparece.
- **Google AI Mode**: Google afirma que el CTR de los listados de producto patrocinados y orgánicos ya es similar en AI Mode (datos internos de Estados Unidos). Las campañas de Shopping y Performance Max compiten por el mismo espacio que el feed orgánico de Merchant Center.
- **Lo que comparten**: la calidad de la landing, el feed de productos y la claridad de la oferta sirven a ambos. Las mejoras de `seo-geo` y `geo-ai-discoverability` siguen siendo la base.

## Formato de salida del informe

1. **Respuesta corta** (3 a 4 frases): recomendación con escenario, plataforma y fecha propuesta.
2. **Qué se vende hoy en el país del cliente**: tabla de plataformas con estado (confirmado, anunciado, no disponible), fuente y fecha.
3. **Encaje con el negocio**: tipo de negocio, qué convierte hoy y qué dice la data propia (GA4, CRM, Ads).
4. **Escenarios**: conservador (no invertir y preparar medición), piloto (presupuesto, duración, plataforma, criterio de éxito) y expansión (si el piloto cumple). Cada uno con supuestos explícitos.
5. **Medición**: qué se instala, cómo se separa pago de orgánico en GA4 y cuál es la métrica de decisión.
6. **Riesgos y datos no confirmados**: lista honesta de lo que no se pudo verificar.
7. **Coordinación con SEO y GEO**: qué se mantiene en orgánico y dónde el pago aporta.
8. **Fuentes**: URL, fecha de publicación y fecha de consulta.

Reglas de redacción: números con formato europeo (1.000,50), tuteo, sin emojis. Si es para el cliente, sin jerga y con la decisión como de gerencia. Las fechas de piloto son propuestas, no compromisos.

## Errores frecuentes

- Afirmar disponibilidad por país sin fuente primaria del país concreto. Un anuncio de "14 países LATAM" no confirma un país no nombrado.
- Confundir anuncios encima o debajo de AI Overviews (disponibles en todo el mundo) con anuncios dentro de AI Overviews o AI Mode (12 países, inglés).
- Recomendar Perplexity Ads o anuncios en Gemini: no existen al 31/10/2026.
- Presentar como de OpenAI cifras de CPC o de rendimiento que vienen de agencias.
- Medir el piloto por clics o CTR en un negocio B2B.

## Archivos de referencia

- `references/plataformas.md`: tabla por plataforma con estado, países, formatos, compra, medición, fuente y fecha. Cargar bajo demanda.
- `references/fuentes.md`: fuentes con URL, fecha de publicación y fecha de consulta. Cargar al citar o al actualizar.

## Skills relacionadas

`seo-conversion` (qué convierte), `ga4-analysis` y `ga4-ai-traffic` (medición), `seo-geo`, `geo-platform-audit` y `seo-ai-search-share-of-voice` (presencia orgánica en IA), `paid-ads` (gestión de campañas de Google y Meta), `ad-creative` (piezas).
