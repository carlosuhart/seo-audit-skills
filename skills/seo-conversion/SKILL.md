---
name: seo-conversion
description: >
  Conversion-led SEO for leads and sales: classifies the business (B2B demo, self-serve SaaS, local service,
  ecommerce), runs a GA4 measurement gate and prioritizes only the applicable fronts, from buying intent to money
  pages, local, review sites and commercial GEO. Scripts for GSC by buying intent (brand split), money-page inventory,
  content-to-money linking and GA4 checks. Use when user says "SEO que genere leads", "el orgánico no convierte",
  "captación de leads", "SEO transaccional", "SEO de conversión", "páginas de dinero", "BOFU", "organic leads" or
  "SEO for lead generation". Not for pure CRO (page-cro), general technical audits (seo-technical) or product pages
  without a conversion question (seo-ecommerce).
argument-hint: "<url o dominio> [--tipo b2b|saas|local|ecommerce] [--uso interno|cliente]"
metadata:
  category: seo
  author: Zythos Media
  version: 1.0.1
  fuentes_revisadas: 2026-10-23
  revisar_fuentes: 2027-04-23
---

# SEO orientado a conversión y captación

El objetivo no es tráfico: es que la búsqueda orgánica (Google, mapas, asistentes de IA) traiga leads o ventas que el
negocio pueda contar. Esta skill decide **qué frentes de SEO importan para ese negocio, en qué orden y con qué
evidencia**, y delega la ejecución de cada frente en la skill que ya lo cubre. Su aporte propio es la priorización, la
puerta de medición y un conjunto de reglas que salen de errores reales (`references/errores-reales.md`).

Dos principios que no se negocian:
- **La conversión es contexto, no filtro.** Ordena el trabajo y explica el porqué de cada propuesta, pero no excluye
  frentes. Se recupera lo que vende y, a la vez, se construye lo que todavía no vende.
- **Lo que pasa después del formulario no es SEO.** Velocidad de respuesta de ventas, precios, decisión de ofrecer
  prueba gratis: se registran como dependencia de otra área, con la evidencia de la SERP o de los datos, sin prescribirlos.

## Paso 0. Alcance y datos

Antes de tocar herramientas, deja escrito:
1. **Qué cuenta como conversión**: formulario, demo, cotización, llamada, WhatsApp, registro, compra. Y cuál es la
   **fuente de verdad** del volumen (CRM, tickets, correo del formulario, pedidos). GA4 nunca es la fuente de verdad del
   volumen de leads si hay banner de consentimiento.
2. **Accesos**: GSC, GA4, Perfil de Empresa, CRM, Google Ads (solo lectura). Lo que no está accesible se pide al
   cliente; no se supone.
3. **Uso del entregable**: interno (análisis completo) o cliente (ejecutivo, sin jerga). Si no está dicho, pregunta.
4. **Qué está en el alcance de quien pide**: lo que puede ejecutar o pedir a Desarrollo, y lo que depende de otras
   áreas (pagado, gerencia, ventas). Lo segundo va como dependencia, no como tarea.

## Paso 1. Clasificar el negocio

| Tipo | Conversión típica | Ciclo | Señal en el sitio |
|---|---|---|---|
| B2B con demo o cotización | formulario, demo, reunión | semanas o meses | "Agenda", "Cotiza", "Habla con ventas" |
| SaaS de autoservicio | registro, prueba, compra de plan | días | "Prueba gratis", página de precios |
| Servicio local | llamada, WhatsApp, ruta, reserva | horas o días | dirección, zona de servicio, Perfil de Empresa |
| Ecommerce | compra | minutos o días | carro, fichas, Merchant Center |

Un sitio puede ser mixto (hub de servicios con productos SaaS satélite): clasifica **cada sitio o sección** por
separado. La matriz de frentes cambia según el tipo.

## Paso 2. Puerta de medición (siempre primero)

```powershell
py scripts/medicion_ga4.py --list-properties
py scripts/medicion_ga4.py --property properties/<id> --start <AAAA-MM-DD> --end <AAAA-MM-DD> --host <www.dominio> --out <dir>/medicion.json
```

Revisa además el checklist de 14 puntos de `references/medicion.md` (cuadre con el CRM, filtros, consentimiento,
WhatsApp y llamadas, `client_id` para calidad del lead, atribución declarada).

- Si la puerta falla, el diagnóstico de conversión se declara **"condicionado a medición"** y los arreglos de medición
  van primero en el plan. Los frentes que no dependen de GA4 (demanda en GSC, páginas de dinero, técnico, SERP) siguen.
- Nunca concluyas "el orgánico no convierte" con una medición que no cuadra con el CRM.
- Declara siempre la cobertura del consentimiento: con banner denegado por defecto y sin modelado, GA4 subcuenta los
  leads en una proporción cercana a la tasa de rechazo.

## Paso 3. Demanda e intención de compra

```powershell
py scripts/intencion_gsc.py --site "sc-domain:<dominio>" --start <...> --end <...> --marca "<regex de marca>" --config tipos.json --out <dir>/intencion.json --mensual
```

`tipos.json` define los tipos de página por ruta y cuáles son de dinero (ejemplo en el docstring del script).

- **Separa marca, sin marca y anonimizadas antes de leer cualquier posición.** Una página de servicio "en posición 13"
  puede estar recibiendo solo búsquedas de su propia marca.
- Clasifica la demanda sin marca por nivel de intención: transaccional, comparación, categoría, cómo hacer, definición,
  informativa (`references/intencion-y-paginas.md`). Los patrones son heurísticos: revisa "sin clasificar" y ajusta.
- La demanda que todavía no rankea no está en GSC: complétala con la herramienta de volumen que corresponda al cliente y
  valida los volúmenes bajos o contradictorios con una segunda fuente (Keyword Planner o Trends). Dos herramientas
  pueden diferir 25 veces para la misma keyword.

## Paso 4. Páginas de dinero

```powershell
py scripts/paginas_dinero.py --sitemap https://<dominio>/sitemap.xml --patron "<regex de rutas de dinero>" --out <dir>/paginas_dinero.json
py scripts/enlazado_dinero.py --sitemap https://<dominio>/sitemap.xml --dinero dinero.json --intencion <dir>/intencion.json --out <dir>/enlazado.json
```

- **Lista los sitemaps y el sitio en vivo antes de proponer cualquier página nueva.** Proponer una página que ya existe
  invalida el diagnóstico completo frente al cliente.
- Para cada búsqueda de compra, comprueba qué tipo de página gana el top 5 (`seo-sxo`) y qué URL del sitio la recibe
  hoy. Si gana la categoría, el listado o el comparador, optimizar la ficha o el servicio no basta. Si en la sesión no
  hay acceso a la SERP, no repitas lo que dice el enunciado: deja la verificación como primera acción del frente, con
  las búsquedas concretas a revisar y qué decisión cambia según el tipo de página que gane.
- Enlazado: nombra la diferencia entre enlaces de menú y pie y enlaces en el contenido, y elige los artículos a
  enlazar por impresiones o clics reales (lista `sin_enlace_a_dinero` de `enlazado_dinero.py`, ordenada con
  `--intencion`), no por afinidad temática.
- **Comprabilidad**: antes de priorizar una página, confirma que se puede comprar o contratar (en stock, visible, sin
  redirección, en zona de despacho). Mide qué parte de los clics orgánicos llega a páginas que no convierten por
  diseño o por estado.
- Lo que solo aparece tras ejecutar JavaScript (formularios, CTA, banner que tapa el CTA en móvil) se revisa con
  navegador (`seo-visual` o Playwright), no con el HTML del script.

## Paso 5. Frentes y prioridad por tipo de negocio

Abre solo los frentes aplicables. C = crítico, A = alto, M = medio, — = no aplica salvo excepción.

| # | Frente | B2B | SaaS | Local | Ecom | Ejecuta | Referencia |
|---|---|---|---|---|---|---|---|
| 1 | Medición, atribución y calidad del lead | C | C | C | C | `ga4-analysis`, `google-tag-manager`, `attribution`, `revops` | medicion.md |
| 2 | Demanda e intención de compra | C | C | A | A | `mineria-de-impresiones`, `seo-dataforseo` | intencion-y-paginas.md |
| 3 | Tipo de página frente a la SERP | C | C | C | C | `seo-sxo` | intencion-y-paginas.md |
| 4 | Salud técnica de las páginas de dinero | A | A | A | C | `seo-technical`, `canonical`, `robots-txt`, `core-web-vitals` | intencion-y-paginas.md |
| 5 | CRO de página y formulario | C | A | C | A | `page-cro`, `form-cro`, `signup-flow-cro` | intencion-y-paginas.md |
| 6 | Enlazado del contenido a las páginas de dinero | C | A | M | A | `seo-interlinking` | intencion-y-paginas.md |
| 7 | Snippet como filtro del clic | A | A | A | A | `on-page-fundamentals`, `schema-markup` | intencion-y-paginas.md |
| 8 | SERP de marca | A | A | A | A | `seo-geo` (entidad), `seo-local` | intencion-y-paginas.md |
| 9 | SEO local y Perfil de Empresa | — | — | C | M | `seo-local`, `seo-maps` | off-site-ia-local.md |
| 10 | Off-page comercial: reseñas, directorios, comparadores | C | C | A | M | `seo-competitor-pages`, `digital-pr`, `seo-backlinks` | off-site-ia-local.md |
| 11 | GEO en búsquedas comerciales | C | C | M | M | `geo-platform-audit`, `seo-ai-search-share-of-voice`, `ga4-ai-traffic` | off-site-ia-local.md |
| 12 | Landings por país e idioma | A | M | — | M | `seo-hreflang`, `hreflang` | intencion-y-paginas.md |
| 13 | Páginas de compra a escala | A | C | M | M | `seo-programmatic` | escala-pagado-pruebas.md |
| 14 | Herramientas gratuitas y lead magnets | A | A | — | — | `free-tool-strategy`, `lead-magnets` | escala-pagado-pruebas.md |
| 15 | Solapamiento orgánico y pagado | M | M | M | M | `paid-ads` (solo análisis) | escala-pagado-pruebas.md |
| 16 | Pruebas con grupo de control | M | M | M | A | `ab-test-setup` | escala-pagado-pruebas.md |
| 17 | Ecommerce: catálogo y Merchant Center | — | — | — | C | `seo-ecommerce` | — |

Un frente aplicable que no se revisa se declara en el informe con el motivo (sin acceso, fuera de alcance, sin datos).
Nunca se omite en silencio.

## Paso 6. Priorizar

Ordena las acciones por **impacto esperado en conversiones × confianza de la evidencia ÷ esfuerzo**, y marca la
dependencia (quién la ejecuta).

- El impacto se estima con datos del sitio: demanda sin marca de la página, tasa de conversión de páginas comparables
  (no benchmarks de proveedores), estado de comprabilidad.
- La confianza usa los niveles de `references/fuentes.md`: Documentado, Estudio, Un sitio, Proveedor, No confirmado.
  Una acción apoyada solo en una cifra de proveedor se presenta como hipótesis con plan de medición.
- Medición rota y páginas de dinero no indexables van antes que cualquier contenido nuevo.

## Paso 7. Medir el resultado

Cada acción de prioridad alta lleva: línea base (fecha, métrica, fuente), métrica de éxito en conversiones o leads
calificados (no impresiones), fecha de revisión y, si hay varias páginas de la misma plantilla, **grupo de control**.
Un antes y después sin control se reporta como correlación y se cruza con el calendario de updates de Google. En
períodos de mayo de 2025 a abril de 2026 mide en clics y sesiones, no en impresiones.

## Salida

Estructura del informe:
1. Resumen (3 a 5 frases): dónde se pierden hoy los leads o las ventas orgánicas y qué se hace primero.
2. Estado de la medición (puerta superada o "condicionado a medición", cobertura del consentimiento).
3. Demanda: marca, sin marca y anonimizadas; intención de compra; qué página recibe cada búsqueda de compra.
4. Frentes revisados, con hallazgos y evidencia (dato del sitio o fuente con nivel), y frentes no revisados con motivo.
5. Plan priorizado: acción, frente, impacto, confianza, esfuerzo, responsable, dependencia, métrica y fecha de revisión.
6. Dependencias de otras áreas, con la evidencia que las justifica.

## Reglas duras

- No leer posiciones de páginas de dinero sin separar marca. No proponer páginas sin revisar sitemaps y sitio en vivo.
- No diagnosticar conversión con medición rota; no usar GA4 como fuente de verdad del volumen de leads.
- No citar multiplicadores de conversión de IA, CTR o "leads desde la ficha" como benchmark: se miden en el sitio.
- No prometer estrellas por testimonios propios en `Organization` o `LocalBusiness` (no son elegibles).
- No proponer páginas que redefinan el negocio (un vertical o servicio que la empresa no ofrece o no decidió): eso es
  decisión de negocio. Se presenta la evidencia de demanda y se registra como consulta.
- Páginas a escala (por ciudad, sector, integración, naviera, ruta): cada vez que las propongas, nombra explícitamente
  el riesgo de doorway y scaled content abuse de las políticas de Google y explica qué aporta cada página que su
  hermana no tiene. Si solo cambia una variable y empuja a la misma conversión, no se propone.
- Cifras por página tal como vienen en los datos: no las resumas en un rango ("91% a 100% de marca") si alguna página
  lo contradice. Nombra las excepciones.
- Un enlace de menú no es un puente: lo que cuenta es el enlace dentro del contenido.

Detalle y origen de cada regla: `references/errores-reales.md`. Si existe `references/casos-privados.md` (anexo local,
no versionado), léelo: enlaza cada regla con el caso real del entorno, sus archivos y su estado.

## Scripts

Python siempre con `py` desde PowerShell. Credenciales por variables de entorno (`GSC_TOKEN_PATH`,
`GSC_SERVICE_ACCOUNT_KEY`, `GA4_TOKEN_PATH`), nunca rutas fijas. Los scripts solo leen; no escriben en ningún CMS ni
en las consolas.

| Script | Responde |
|---|---|
| `medicion_ga4.py` | ¿Los datos de GA4 sirven? Hosts ajenos, lead duplicado, sesiones sin entrada, IA, retención |
| `intencion_gsc.py` | ¿Qué demanda de compra hay y qué página la recibe? Marca, sin marca, anonimizadas |
| `paginas_dinero.py` | ¿Las páginas de dinero existen, son indexables y permiten convertir? |
| `enlazado_dinero.py` | ¿El contenido lleva a las páginas de dinero o solo el menú? |
