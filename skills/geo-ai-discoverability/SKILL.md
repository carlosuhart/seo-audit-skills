---
name: geo-ai-discoverability
description: >
  Implementa las señales de entidad y contenido para que los buscadores con IA citen el
  sitio: Wikidata, NewsMediaOrganization, Wikipedia, llms.txt, RSL 1.0, E-E-A-T, pasajes
  citables, Knowledge Panel, Preferred Sources e IndexNow. Para auditar un dominio
  completo usar seo-geo; para un post, blog-geo.
---

# GEO/AEO — Generative & Answer Engine Optimization

> GEO no reemplaza al SEO. Google lo confirma oficialmente (2026-06-29): "optimizar para
> AI Search sigue siendo SEO. AEO y GEO son etiquetas rebautizadas para el mismo trabajo."
> Priorizar SEO técnico y calidad de contenido primero; después aplicar señales GEO.

---

## AEO vs GEO — distinción práctica

| Término | Superficie principal | Lever |
|---|---|---|
| **AEO** (Answer Engine Optimization) | Siri, Google Assistant, Alexa, Cortana — respuestas directas en voz/chat | Passages cortos, FAQ schema, respuestas en <40 palabras |
| **GEO** (Generative Engine Optimization) | ChatGPT Search, Perplexity, AI Overviews, AI Mode, Grok — resúmenes extensos con citas | Passages 134-167 palabras, entidad clara, frescura |

En la práctica el stack de implementación es el mismo. La distinción importa solo para calibrar el formato: AEO prioriza respuestas ultracortas y directas; GEO prioriza passages autónomos y autoridad de entidad.

---

## Principio rector — Google lo confirma (2026)

Google publicó que optimizar para AI Search **sigue siendo SEO**:
"AEO y GEO son etiquetas rebautizadas para el mismo trabajo." (developers.google.com/search/docs/fundamentals/ai-optimization-guide, actualizado 2026-06-29)

Las señales de citabilidad en AI Overviews y AI Mode son: contenido que ya rankea bien, estructura clara, passages autónomos, autoridad de entidad. No existe un "truco GEO" separado del SEO de calidad.

---

## Cuatro condiciones para ser citado por AI (en orden de prioridad)

1. **Crawlabilidad** — el AI crawler puede acceder a la página (robots.txt, no JS-only)
2. **Densidad de respuesta a nivel de pasaje** — la página contiene una respuesta clara y extraíble
3. **Claridad de entidad** — el sitio/marca/autor es una entidad conocida y sin ambigüedad
4. **Señales de frescura** — el contenido tiene fecha de publicación visible y dateModified actualizado

Si falta cualquiera de estos cuatro, no habrá cita aunque el contenido sea excelente.

---

## Señal crítica: brand mentions > backlinks

Brand mentions correlacionan **3x más fuerte** con visibilidad en AI que los backlinks.
(Estudio Ahrefs diciembre 2025, 75.000 marcas)

| Señal | Correlación con citas AI |
|---|---|
| Menciones en YouTube | ~0,737 (más alta) |
| Menciones en Reddit | Alta |
| Menciones en X (Grok) | Alta — X es fuente de grounding primaria para Grok |
| Presencia en Wikipedia | Alta |
| Presencia en LinkedIn | Media |
| Domain Rating (backlinks) | ~0,266 (débil) |

Solo el **11% de los dominios** son citados por ChatGPT y Google AI Overviews para la misma query — la optimización por plataforma es imprescindible.

---

## Panorama de plataformas AI Search (agosto 2026)

| Plataforma | Fuentes primarias | Lever de citación | Motor |
|---|---|---|---|
| **Google AI Overviews** | Top-10 orgánico (92% de citas) | SEO clásico + passages | Gemini 2.5 |
| **Google AI Mode** | Pool amplio, baja correlación con ranking | Frescura + entity authority | Gemini 2.5 Pro |
| **ChatGPT Search** | Wikipedia (47,9%), Reddit (11,3%), índice web | Entidad + fuentes autoritativas | GPT-4o/o3 |
| **Perplexity** | Reddit (46,7%), Wikipedia, web reciente | Frescura (ventana 2-3 días para breaking) | Sonar / Llama |
| **Perplexity Deep Research** | Fuentes primarias, papers, informes | Datos originales, metodología clara | Sonar Pro |
| **Gemini Deep Research** | Academia, noticias, web autoritativa | Datos con atribución + estructura research | Gemini 2.5 Pro |
| **ChatGPT o3 Deep Research** | Web + datos estructurados + APIs | Fuentes primarias verificables | o3 |
| **Microsoft Copilot** | Índice Bing, IndexNow, webs autorizadas | Bing SEO + IndexNow freshness | Prometheus/GPT-4o |
| **Grok (xAI)** | X posts, web via GrokBot, DeepSearch | Menciones en X + grounding web | Grok 4 |
| **Meta AI** | Índice Bing + rastreo Meta, redes sociales | Presencia en FB/Instagram/WhatsApp | Llama |
| **Apple Intelligence/Siri** | Bing (indexación primaria) + web | Datos estructurados + Bing SEO | Llama fine-tuned |
| **DuckDuckGo AI Chat** | DuckDuckGo index + OpenAI/Anthropic/Meta | DuckDuckGo SEO | Múltiples LLMs |
| **NotebookLM** | URLs añadidas manualmente por el usuario | Ser fuente de referencia que otros enlazan | Gemini |

**Implicación práctica:** una estrategia GEO completa no puede ignorar Grok (requiere señales de X.com), Microsoft Copilot (requiere IndexNow), ni Deep Research (requiere datos originales estructurados).

---

## AI crawlers — robots.txt

### Crawlers activos (2026)

| Crawler | Plataforma | User-Agent | Obedece robots.txt |
|---|---|---|---|
| GPTBot | OpenAI / ChatGPT Search | `GPTBot` | Sí |
| OAI-SearchBot | OpenAI search features | `OAI-SearchBot` | Sí |
| ChatGPT-User | ChatGPT browsing (user-triggered) | `ChatGPT-User` | No (user-triggered) |
| PerplexityBot | Perplexity | `PerplexityBot` | Sí |
| Google-Extended | Google AI training y grounding opt-out | `Google-Extended` | Sí |
| Google-CloudVertexBot | Vertex AI Agent (site owner requested) | `Google-CloudVertexBot` | Sí |
| Google-Agent | Project Mariner, agentic browsing | `Google-Agent` | No (user-triggered) |
| Google-NotebookLM | Fetch de URLs añadidas por el usuario | `Google-NotebookLM` | No (user-triggered) |
| anthropic-ai | Claude (training) | `anthropic-ai` | Sí |
| ClaudeBot | Claude (web features) | `ClaudeBot` | Sí |
| GrokBot | xAI / Grok DeepSearch | `Grokbot` | Sí |
| DuckAssistBot | DuckDuckGo AI Chat | `DuckAssistBot` | Sí |
| Meta-ExternalAgent | Meta AI (FB, IG, WA, Messenger) | `meta-externalagent` | Sí |
| Applebot-Extended | Apple Intelligence / Siri | `Applebot-Extended` | Sí |
| cohere-ai | Cohere | `cohere-ai` | Sí |
| Bytespider | ByteDance / TikTok AI | `Bytespider` | Sí |

**Nota crítica:** Los fetchers user-triggered (Google-Agent, Google-NotebookLM, ChatGPT-User) ignoran robots.txt por diseño — no se pueden bloquear con robots.txt, solo con controles server-side.

**Web Bot Auth (RFC 9421):** Los agentes agentic de Google (Google-Agent) pueden autenticarse via header `Signature-Agent` + key directory. Reverse-DNS sigue siendo el fallback para verificación de identidad del bot.

### Postura recomendada en robots.txt

```
# AI search — permitir todos los crawlers de indexación/citación
User-agent: GPTBot
Disallow:

User-agent: OAI-SearchBot
Disallow:

User-agent: PerplexityBot
Disallow:

User-agent: anthropic-ai
Disallow:

User-agent: ClaudeBot
Disallow:

User-agent: Grokbot
Disallow:

User-agent: DuckAssistBot
Disallow:

User-agent: meta-externalagent
Disallow:

User-agent: Applebot-Extended
Disallow:

# Google-Extended: bloquear SOLO si se quiere opt-out de training de Google AI.
# Bloquearlo NO impide aparecer en AI Overviews ni AI Mode — son controles separados.
# User-agent: Google-Extended
# Disallow: /
```

**Reglas de decisión:**
- `Google-Extended` controla training de Gemini/Vertex, NO aparición en AI Overviews/AI Mode.
- Bloquear `GPTBot` u `OAI-SearchBot` significa que ChatGPT Search no citará la página.
- No bloquear `Googlebot` nunca — afecta búsqueda orgánica y AI Overviews simultáneamente.

---

## llms.txt — resumen de contexto para AI tools

llms.txt es un archivo de texto plano en `/llms.txt`. **Google lo ignora explícitamente** (confirmado en guía AI optimization 2026-06-29, y por Gary Illyes y John Mueller). **Bing Copilot/Microsoft Copilot, Perplexity, ChatGPT/OpenAI y otros LLMs sí pueden leerlo.**

**Cuándo implementarlo:** siempre — el coste es mínimo y aporta contexto a plataformas no-Google.
**Cuándo NO prometerlo:** como lever de ranking en Google Search, AI Overviews o AI Mode.

### Estructura mínima

```markdown
# Nombre del sitio

> Descripción en una frase de qué cubre este sitio.

## Sobre el sitio

Párrafo breve: quién lo gestiona, estándares editoriales, cobertura temática.

## Secciones principales

- [Nombre de sección](https://dominio.com/seccion/): descripción breve
- [Nombre de sección](https://dominio.com/seccion/): descripción breve

## Contenido destacado

- [Título del artículo](https://dominio.com/slug/): descripción en una línea
- [Título del artículo](https://dominio.com/slug/): descripción en una línea

## Contacto / Editorial

- Contacto: email@dominio.com
- Política editorial: https://dominio.com/politica-editorial/

## Licencia

Contenido bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
```

### Implementación

1. Crear como archivo estático, no dinámico
2. Servir en `https://dominio.com/llms.txt` (raíz, o en un subpath si el archivo cubre solo esa sección — ver regla de especificidad abajo)
3. WordPress: añadir vía FTP o plugin de archivos estáticos en `/`
4. Incluir las páginas de mayor valor — no todo el sitio

### Reglas estrictas de formato (fuente: llmstxt.org, verificado 09/09/2026)

El estándar no es solo una convención de estilo — define un orden y una sintaxis precisos, pensados para que herramientas puedan parsearlo con "técnicas de programación clásicas (parsers y regex)", no solo con lectura humana. Checklist de validación:

1. **H1 — única sección obligatoria.** Debe existir exactamente un `# Nombre del sitio` al inicio (después de un BOM opcional). Sin H1, el archivo no es válido aunque el resto esté bien formado.
2. **Blockquote inmediato tras el H1** — un resumen corto (`> ...`) con la información clave para entender el resto del archivo.
3. **Secciones de detalle opcionales** — cualquier bloque markdown que no sea un heading, entre el blockquote y las listas de archivos.
4. **Listas de archivos delimitadas por H2** — cada sección de enlaces va bajo su propio `## Encabezado`.
5. **Sintaxis de enlace obligatoria dentro de esas listas — este es el punto que falla en la práctica:** cada ítem debe ser un hipervínculo markdown real, `[nombre](url)`, opcionalmente seguido de `:` y una nota. **"Etiqueta: https://..." (URL en texto plano, sin corchetes) no cumple el estándar**, aunque el archivo tenga contenido real y URLs correctas — un parser que busca `[texto](url)` no detecta nada y reporta el archivo como "sin enlaces".
6. **Especificidad por path:** si existen varios `llms.txt` en distintas rutas (ej. `/llms.txt` y `/docs/llms.txt`), cada uno cubre las URLs bajo su propio path, y ante solapamiento el agente debe usar el más específico.

**Por qué esto importa ahora, no solo en teoría:** desde 2026 Lighthouse incluye la categoría "Agentic Browsing" (aún en desarrollo, sujeta a cambios), que audita automáticamente esta sintaxis exacta. El mensaje de error real que emite cuando falla la regla 5 es *"File does not appear to contain any links"* — no dice "formato incorrecto", dice literalmente que no encuentra enlaces, aunque el archivo esté lleno de URLs en texto plano. **Patrón real recurrente:** en dos auditorías de dominios de producto de una misma marca (sept. 2026) el llms.txt tenía contenido completo y correcto pero con URLs en formato "Etiqueta: url" en vez de markdown — mismo error, dos veces, confirma que es el fallo más común al implementar este archivo a mano. Antes de dar un llms.txt por bien implementado, verificar la regla 5 línea por línea, no solo que el archivo exista y devuelva 200.

---

## RSL 1.0 (Really Simple Licensing)

Estándar de licenciamiento legible por AI publicado en diciembre 2025. Respaldado por Reddit, Yahoo, Medium, Quora, Cloudflare, Akamai, Creative Commons.

**Propósito:** comunicar de forma machine-readable si el contenido puede ser usado para training, indexación o snippets AI.

### Implementación

Opción A — dentro de llms.txt (al inicio del archivo):
```
# RSL 1.0
# https://rsl.it/
License: CC-BY-SA-4.0
Contact: editor@dominio.com
AI-training: allowed
AI-indexing: allowed
AI-snippets: allowed
```

Opción B — archivo separado `/rsl.txt`:
```
RSL/1.0
AI-training: allowed
AI-indexing: allowed
AI-snippets: allowed
Contact: editor@dominio.com
License: CC-BY-4.0
```

**Decisión de política:** `allowed` maximiza visibilidad AI. `disallowed` para training protege el contenido de ser usado para entrenar modelos, sin afectar la aparición en respuestas de búsqueda AI que usan grounding web (no training).

---

## AI Mode vs AI Overviews — dos motores, no uno

Google fusionó la UX en "una experiencia seamless" en Google I/O 2026 (2026-05-19). Los dos motores de citación siguen siendo técnicamente distintos. Overlap de URLs citadas: **13,7%** (estudio Ahrefs, 540.000 pares de queries).

| Factor | AI Overviews | AI Mode |
|---|---|---|
| Correlación con ranking orgánico | Alta (92% de citas son top 10) | Baja — cita más allá de posición 5 |
| Señal de frescura | Relevante | Muy alta — contenido <3 meses tiene 3x más probabilidad de citación |
| Señal de entidad | Domain authority | Entity authority (Wikidata, sameAs) |
| Lever principal | SEO orgánico + densidad de pasajes | Frescura + dateModified + Q-number Wikidata |
| Promedio de dominios citados por query | ~5 | ~9 (pool más amplio) |

**Implicación práctica:** rankear bien en orgánico alimenta AI Overviews automáticamente. Para AI Mode: fechas visibles + `dateModified` en schema + Q-number Wikidata en `sameAs` + actualización cada 2-3 meses en páginas pillar.

---

## Deep Research optimization

Los motores de Deep Research (Gemini Deep Research, Perplexity Pro, ChatGPT o3 Deep Research) realizan investigación multi-paso y citan más fuentes por query, con mayor énfasis en:

**Señales diferenciales vs búsqueda estándar:**
- Datos originales propios (encuestas, estudios, experimentos) tienen 5-8x más peso
- Metodología explícita (cómo se obtuvo el dato) aumenta la citabilidad
- Referencias a fuentes primarias (papers, organismos oficiales) son leverage fuerte
- Estructura tipo research paper: metodología > hallazgos > implicaciones

**Formato óptimo para Deep Research:**
```
H2: Hallazgos principales
[Cifra clave con fuente y año en la primera frase]

H3: Metodología
[Cómo se recopiló el dato, tamaño de muestra, período]

H3: Implicaciones
[Por qué importa el hallazgo — autónomo, sin referencias cruzadas]
```

**Quick win:** si el sitio tiene datos propios (GSC, encuestas a clientes, análisis internos), publicarlos como posts de datos con metodología explícita. Son la fuente más citable en Deep Research.

---

## Grok / xAI — señales específicas

Grok 4 usa DeepSearch para rastreo web en tiempo real. Las señales específicas para Grok difieren del resto de plataformas:

**Señales primarias:**
- Menciones en X (Twitter) — Grok usa X como fuente de grounding primaria
- Cuenta verificada en X con posting regular en el nicho
- GrokBot rastrea las páginas enlazadas desde X
- Threads de X con datos y análisis del dominio temático

**Implicación práctica:**
- Presencia activa en X con posts que enlacen al sitio es el lever más directo para Grok
- Una comunidad en X alrededor del nicho (respuestas, retweets, menciones) amplifica el efecto
- GrokBot respeta robots.txt: añadir `User-agent: Grokbot / Disallow:` activa crawling

---

## Microsoft Copilot — señales específicas

Microsoft Copilot (anteriormente Bing Copilot) usa el índice de Bing como base. Señales diferenciales:

**IndexNow — lever de frescura más directo disponible:**
```python
# Notificar a Bing/Copilot inmediatamente al publicar o actualizar
import requests

def submit_indexnow(url, key):
    payload = {
        "host": "dominio.com",
        "key": key,
        "keyLocation": f"https://dominio.com/{key}.txt",
        "urlList": [url]
    }
    requests.post("https://api.indexnow.org/indexnow", json=payload)
```

1. Obtener clave en bing.com/webmasters → IndexNow
2. Alojar `{clave}.txt` en la raíz del dominio
3. Enviar cada URL nueva/actualizada a `api.indexnow.org`
4. Bing comparte señal con otros motores adheridos (Yandex, Seznam, etc.)

**Bingbot** es el crawler primario — asegurar que Bingbot no esté bloqueado en robots.txt.

---

## Meta AI — señales específicas

Meta AI usa el índice de Bing más rastreo propio via `meta-externalagent`. Está integrado en WhatsApp, Instagram, Facebook y Messenger.

**Señales:**
- Presencia activa en páginas de Facebook e Instagram del negocio
- Posts de FB/IG que enlacen al sitio (crawleados por meta-externalagent)
- Permitir `meta-externalagent` en robots.txt
- Indexación normal en Bing (Meta reutiliza ese índice)

---

## Knowledge Panel — optimización y claim

El Knowledge Panel de Google es la señal de entidad más visible y la que más impacta la citabilidad en AI Overviews.

### Claim del Knowledge Panel

1. Buscar el nombre del negocio/marca en Google
2. Si aparece Knowledge Panel, hacer clic en "Reclamar este panel"
3. Autenticar vía Google Account verificada con perfil público relevante
4. Proporcionar al menos un perfil social o página About verificable

**Sin Knowledge Panel aún:**
- El trigger más fiable es una entidad en Wikidata con `official website` correcto
- Segundo trigger: presencia en Google Business Profile (para negocios locales)
- Tercer trigger: cobertura en medios reconocidos (sin Wikipedia se puede tener KP)

### Campos clave del Knowledge Panel

| Campo | Cómo controlarlo |
|---|---|
| Descripción | Primera frase del artículo de Wikipedia / About page bien escrita |
| Logo | Schema Organization.logo mínimo 112x112px |
| Redes sociales | sameAs con URLs exactas de los perfiles |
| Fundación | Wikidata P571 (inception date) |
| Sede | Wikidata P159 o Schema Organization.address |

---

## Wikidata — señal de autoridad de entidad

Wikidata es la base de datos estructurada usada por Google Knowledge Graph, Wikipedia y la mayoría de sistemas AI para resolver identidad de entidades.

### Crear entidad en Wikidata

1. Ir a https://www.wikidata.org/wiki/Special:NewItem
2. Añadir label (nombre) y description (una línea) en ES y EN mínimo
3. Añadir aliases (nombres alternativos, abreviaciones)
4. Statements obligatorios para publicación/medio:
   - `instance of` (P31): `online newspaper` / `digital media` / `magazine`
   - `official website` (P856): URL completa con HTTPS — debe coincidir exactamente con el dominio canónico
   - `country` (P17): país correspondiente
   - `language of work or name` (P407): idioma principal
   - `inception` (P571): fecha de fundación
5. Anotar el Q-number asignado y añadirlo al schema Organization via `sameAs`

### Vincular schema a Wikidata

```json
"sameAs": [
  "https://www.wikidata.org/wiki/Q[número]",
  "https://www.facebook.com/...",
  "https://www.instagram.com/...",
  "https://x.com/..."
]
```

### Presencia mínima viable

- Label + description en ES y EN
- `instance of` (P31)
- `official website` (P856) — exactamente igual al dominio canónico
- `inception` (P571)
- Al menos un identificador externo (ISSN, perfil social, Q-number de Wikipedia)

Sin `official website` exactamente igual al dominio, Google puede no conectar la entidad Wikidata con el sitio en el Knowledge Graph.

---

## Schema NewsMediaOrganization — para publicaciones y medios

Para blogs, medios y marcas de contenido, `NewsMediaOrganization` da señales de atribución AI más fuertes que `Organization` genérico.

```json
{
  "@context": "https://schema.org",
  "@type": "NewsMediaOrganization",
  "@id": "https://dominio.com/#organization",
  "name": "Nombre de la publicación",
  "url": "https://dominio.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://dominio.com/logo.png",
    "width": 300,
    "height": 300
  },
  "description": "Misión editorial en una frase",
  "foundingDate": "2020",
  "inLanguage": "es",
  "publishingPrinciples": "https://dominio.com/politica-editorial/",
  "masthead": "https://dominio.com/acerca-de/",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q[número]",
    "https://www.facebook.com/publicacion",
    "https://x.com/publicacion",
    "https://www.instagram.com/publicacion",
    "https://www.linkedin.com/company/publicacion"
  ]
}
```

**Campos clave para citabilidad AI:**
- `publishingPrinciples` — Google y AI tools usan esto para evaluar credibilidad
- `masthead` — URL de la página de equipo/acerca de. Requerido para señales de elegibilidad News
- `description` — se convierte en cómo los AI tools describen la fuente al citarla
- **Logo mínimo 112x112px** — Google requiere esto para rich results. 60x60 no es válido

**ISSN:** Si la publicación tiene ISSN, añadir `"issn": "XXXX-XXXX"`. Es la señal de autoridad de entidad más fuerte disponible para publicaciones.

---

## Citabilidad a nivel de pasaje — estructura de contenido

Los AI tools extraen respuestas a nivel de pasaje, no de página. **Longitud óptima: 134-167 palabras** por pasaje autónomo (estudio SE Ranking, 1,3M citas). El 44% de las citas AI provienen del primer 30% de la página.

Contenido <3 meses tiene **3x más probabilidad de ser citado**. Páginas sin actualizar en 6+ meses pierden elegibilidad de citación.

### Patrones de alta citabilidad

**Estructura answer-first (más citable en búsqueda estándar):**
```
H2: ¿Qué es [tema]?
Primera frase: [Tema] es [definición directa en una frase].
Segunda frase: [Detalle de soporte más importante].
Resto del párrafo: contexto, matices, ejemplos. [~134-167 palabras total]
```

**Estadísticas con atribución (formato más extraíble):**
```
Según [Fuente] ([Año]), el X% de [población] [acción].
```
Incluir siempre: año, nombre de la fuente, el claim específico. Claims vagos no son extraíbles.

**Para Deep Research — formato research:**
```
H2: [Hallazgo o dato clave]
Primera frase: [cifra + fuente + año]
H3: Metodología: [cómo se obtuvo]
H3: Implicaciones: [por qué importa — autónomo]
```

### Anti-patrones (reducen citabilidad)

- Párrafos introductorios largos antes de la respuesta real
- Respuestas enterradas en el medio de párrafos largos
- Claims sin año ni fuente
- Respuestas que requieren leer múltiples secciones para ensamblarse

---

## E-E-A-T para citabilidad AI

| Señal | Implementación |
|---|---|
| Nombre del autor + credenciales | Byline visible + schema Person con `jobTitle` |
| Página de bio del autor | URL dedicada con schema Person, sameAs LinkedIn + X |
| Página About/masthead | Lista al equipo editorial, contacto, misión |
| Política editorial | Página separada enlazada desde footer/about |
| Fuentes citadas inline | Fuentes nombradas con links, no "según los expertos" |
| Fechas de contenido visibles | `datePublished` y `dateModified` visibles para usuarios |

---

## Wikipedia — señal de entidad máxima

Wikipedia es fuente de entrenamiento y señal de autoridad para la mayoría de sistemas AI. ChatGPT cita Wikipedia en el 47,9% de sus respuestas.

### Umbral de notabilidad

- Cobertura en medios establecidos (no press releases propios)
- ISSN o reconocimiento institucional
- Mínimo 3 fuentes independientes que cubran la publicación (no el contenido que produce)

No crear un artículo de Wikipedia sin notabilidad documentada. Un intento fallido dificulta futuras creaciones.

### Proceso

1. Verificar notabilidad antes de redactar
2. Borradores en Wikipedia Sandbox: https://en.wikipedia.org/wiki/Wikipedia:Sandbox
3. Solo hechos verificables con referencias, sin lenguaje promocional
4. Tras creación: añadir propiedad `Wikipedia article` en Wikidata vinculando al artículo

---

## Señales de marca en plataformas externas

| Plataforma | Acción | Prioridad | Motor AI que usa la señal |
|---|---|---|---|
| YouTube | Canal con contenido del nicho | Alta (correlación 0,737) | Google AI Overviews/Mode, ChatGPT |
| Reddit | Presencia en subreddits del nicho | Alta (Perplexity cita Reddit 46,7%) | Perplexity, ChatGPT |
| X (Twitter) | Cuenta activa, posts con links | Alta para Grok | Grok/xAI |
| Wikipedia | Entrada verificada | Alta si hay notabilidad | Todos los modelos |
| Wikidata | Entidad con Q-number | Alta — siempre factible | Google AI, ChatGPT, Claude |
| LinkedIn | Página de empresa completa | Media | ChatGPT, Perplexity |
| Facebook | Página de empresa con posts | Media para Meta AI | Meta AI |
| Google Preferred Sources | Comunicar a audiencia para que añadan | Alta (>345K fuentes) | Google AI Overviews/Mode |

**Google Preferred Sources (acción concreta):** los usuarios pueden marcar sitios como "fuentes preferidas" en AI Search. Google trabaja para usarlo como señal de ranking. Publicar instrucción en newsletter/redes: "Puedes añadir [dominio] como fuente preferida en Google AI Search para ver nuestro contenido en tus respuestas."

---

## Monitoreo de citaciones AI

### Baseline manual (gratuito, hacer una vez al trimestre)

1. Abrir ChatGPT, Perplexity, Google AI (con AI Mode), Microsoft Copilot, Grok
2. Preguntar sobre 5-10 temas clave del sitio
3. Registrar: aparece el sitio en las fuentes, en qué plataformas, con qué anchor
4. Fecha del baseline para comparar tras 4-8 semanas de cambios GEO

### DataForSEO — LLM mentions tracking (automatizado)

- `mcp__dfs-mcp__ai_opt_llm_ment_search` — búsqueda de menciones por marca/dominio
- `mcp__dfs-mcp__ai_opt_llm_ment_agg_metrics` — métricas agregadas de visibilidad AI
- `mcp__dfs-mcp__ai_opt_llm_ment_top_domains` — dominios más citados en el nicho
- `mcp__dfs-mcp__ai_opt_llm_ment_top_pages` — páginas más citadas en el nicho

Usar para establecer baseline cuantitativo y medir variación mensual.

---

## Checklist de implementación GEO completa

```
CRAWLABILIDAD
[ ] GPTBot + OAI-SearchBot permitidos (ChatGPT Search)
[ ] PerplexityBot permitido
[ ] anthropic-ai + ClaudeBot permitidos
[ ] Grokbot permitido (Grok / xAI)
[ ] DuckAssistBot permitido
[ ] meta-externalagent permitido (Meta AI)
[ ] Applebot-Extended permitido (Apple Intelligence)
[ ] Bingbot no bloqueado (Microsoft Copilot)
[ ] Google-Extended: decisión documentada (training vs AI Overviews son controles separados)

LLMS.TXT + RSL 1.0
[ ] /llms.txt existe en raíz del dominio
[ ] Incluye descripción, secciones clave, contenido destacado, contacto
[ ] URLs en llms.txt canónicas y devuelven 200
[ ] H1 único al inicio + blockquote de resumen inmediatamente después (única sección obligatoria + resumen, ver reglas estrictas arriba)
[ ] Enlaces en las listas de archivos usan sintaxis markdown [texto](url), NUNCA "Etiqueta: url" en texto plano — verificar línea por línea, es el fallo más común (ver nota Lighthouse "Agentic Browsing")
[ ] RSL 1.0 declarado (en llms.txt o /rsl.txt)
[ ] Alcance comunicado: Google lo ignora; puede ayudar en Bing/Perplexity/ChatGPT/Grok

ENTIDAD (WIKIDATA + KNOWLEDGE PANEL)
[ ] Entidad Wikidata existe con URL oficial exacta (P856)
[ ] inception date (P571) en Wikidata
[ ] Q-number en Organization/NewsMediaOrganization sameAs
[ ] Knowledge Panel reclamado (si existe)
[ ] Schema type correcto para el tipo de sitio
[ ] publishingPrinciples + masthead poblados (publicaciones)
[ ] Logo mínimo 112x112px en schema
[ ] sameAs incluye X.com, LinkedIn, Wikipedia (si existe)

MICROSOFT COPILOT
[ ] IndexNow configurado (clave + archivo en raíz + envío automático al publicar)
[ ] Bingbot no bloqueado
[ ] Bing Webmaster Tools verificado

GROK / XAI
[ ] Cuenta verificada en X activa con posts que enlazan al sitio
[ ] Grokbot permitido en robots.txt
[ ] Posts de X cubren los temas clave del nicho

META AI
[ ] Página de Facebook/Instagram activa con posts que enlazan al sitio
[ ] meta-externalagent permitido

CONTENIDO CITABLE
[ ] Páginas clave usan estructura answer-first
[ ] Pasajes de 134-167 palabras autónomos en secciones principales
[ ] Estadísticas incluyen año y nombre de fuente inline
[ ] Schema Person del autor incluye jobTitle y description
[ ] datePublished visible para usuarios y en schema
[ ] dateModified actualizado en páginas revisadas recientes
[ ] Plan de actualización cada 2-3 meses en páginas pillar

DEEP RESEARCH (si el nicho tiene queries de investigación)
[ ] Al menos un post de datos originales (encuesta, análisis propio) con metodología explícita
[ ] Estructura: hallazgos > metodología > implicaciones en posts de datos

E-E-A-T
[ ] Página About/masthead existe
[ ] Páginas de bio de autor existen con schema Person
[ ] Política editorial enlazada desde footer

SEÑALES DE MARCA EXTERNAS
[ ] Baseline de citación AI establecido (fecha + plataformas + resultados)
[ ] Presencia activa en Reddit y/o YouTube (según nicho)
[ ] Presencia activa en X si Grok es plataforma relevante para el nicho
[ ] Google Preferred Sources comunicado a la audiencia
[ ] DataForSEO LLM mentions trackeado para nombre de marca y dominio
```
