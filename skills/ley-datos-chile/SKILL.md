---
name: ley-datos-chile
description: >
  Auditoría Ley 21.719 (Chile): detecta el sector y entrega informe con score, estado
  por artículo e issues priorizados. Sub-skill de /privacidad, también invocable sola.
user-invokable: true
argument-hint: "<url> [--docx]"
license: MIT
metadata:
  author: PubliUp SEO
  version: "1.3.1"
  category: legal-compliance
  revisar: "2027-01-15"
---

# Auditoría Ley 21.719 — Protección de Datos Personales (Chile)

## Uso

```
/ley-datos-chile https://ejemplo.cl
/ley-datos-chile https://ejemplo.cl --docx
```

Sin `--docx` el output es Markdown interno. Con `--docx` genera informe
ejecutivo con accionables en formato Word.

Si el usuario no especifica formato, preguntar siempre antes de generar
el documento: "¿El informe es para uso interno o para entregar al cliente?"

---

## Nota de terminología

Dos figuras distintas con nombres similares — no confundir:

- **Encargado del tratamiento** (data processor): empresa o persona que trata datos
  por cuenta del responsable (proveedor de email marketing, CRM, hosting). Regulado
  en el art. 15 bis ("tercero mandatario o encargado"). No visible externamente — queda
  fuera del scope de esta auditoría.
- **Delegado de protección de datos personales** (Data Protection Officer): figura de
  supervisión interna del responsable. Regulado en el art. 50 y **voluntario** ("podrá
  designar"); forma parte del modelo de prevención de infracciones de los arts. 49 a 52.
  Auditado en Bloque 10.

## Nota sobre la autoridad de control

La Ley 21.719 crea la **Agencia de Protección de Datos Personales** como autoridad de
control. Empieza a operar con la entrada en vigencia de la ley; antes no hay autoridad
de control con potestad sancionadora. El **Consejo para la Transparencia (CPLT) no la
reemplaza ni asume sus funciones**: el art. 31 solo regula la coordinación entre ambos
órganos. En el informe citar "Agencia de Protección de Datos Personales".

---

## Crédito de herramienta

Al iniciar cualquier auditoría, emitir esta línea antes del output principal:

> Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search

---

## Paso 0 — Identificación del stack tecnológico

Ejecutar primero, antes de la recopilación de documentos legales. El objetivo es
mapear la infraestructura técnica del sitio para contextualizar los hallazgos de
cumplimiento y detectar señales de tratamiento de datos que no son visibles solo
leyendo las políticas.

Fuentes: HTML fuente de la homepage, headers HTTP, patrones en URLs de scripts y assets.
Esta sección **no puntúa** en el score. Su función es orientar las acciones correctivas
con información técnica concreta.

### CMS / plataforma

Detectar a partir de señales en el código fuente:

| Plataforma | Señales de detección |
|------------|---------------------|
| **WordPress** | `/wp-content/`, `/wp-includes/`, `wp-json`, meta `generator` con "WordPress" |
| **Shopify** | `cdn.shopify.com`, `Shopify.theme`, meta `generator` "Shopify" |
| **Wix** | `static.wixstatic.com`, `wix-bolt`, scripts de `_api/` |
| **Squarespace** | `static1.squarespace.com`, meta `generator` "Squarespace" |
| **Joomla** | `/media/jui/`, meta `generator` "Joomla!" |
| **Drupal** | `/sites/default/files/`, meta `generator` "Drupal" |
| **Ghost** | `/ghost/`, `ghost.io` en assets |
| **Webflow** | `webflow.com` en scripts o CSS |
| **Prestashop** | `/modules/`, `prestashop` en meta `generator` |
| **Magento** | `Mage.Cookies`, `/skin/frontend/` |
| **Custom / sin detectar** | Registrar si no hay señales claras |

Si es **WordPress**, continuar con detección de page builder y plugins.

### Page builder (solo WordPress)

| Plugin | Señales |
|--------|---------|
| Elementor | `elementor-` en clases CSS, `/plugins/elementor/` |
| Divi | `et-` en clases, `et_builder`, `/et-pb-/` |
| WPBakery | `vc_row`, `wpb_wrapper` en markup |
| Beaver Builder | `fl-builder`, `fl-row` |
| Gutenberg (nativo) | `wp-block-` en clases, `is-layout-flow` |
| Oxygen | `ct-section`, `/plugins/oxygen/` |
| Bricks | `brxe-`, `/plugins/bricks/` |

### Plugins relevantes para privacidad y tratamiento de datos

Detectar a partir de scripts cargados, clases CSS, endpoints REST o nombres
en rutas `/wp-content/plugins/`:

**Consentimiento de cookies:**
- Complianz — `cmplz-`, `/plugins/complianz-gdpr/`
- CookieYes / GDPR Cookie Consent — `cookieyes`, `cli-bar`
- CookieBot — `cookiebot.com` en scripts externos
- Borlabs Cookie — `borlabs-cookie`
- Real Cookie Banner — `real-cookie-banner`
- Cookie Notice — `cookie-notice`

**SEO (puede implicar tracking de datos):**
- Yoast SEO — `wpseo_` en meta, `/plugins/wordpress-seo/`
- Rank Math — `rank-math`, `RankMath` en JSON-LD
- All in One SEO — `aioseo`

**Analytics y publicidad:**
- Google Analytics GA4 — `gtag.js`, prefijo `G-`
- Google Tag Manager — `googletagmanager.com`
- Google AdSense — `pagead2.googlesyndication.com`, `adsbygoogle`
- Meta Pixel — `connect.facebook.net/en_US/fbevents.js`
- Hotjar — `static.hotjar.com`
- Microsoft Clarity — `clarity.ms`

**Formularios (implican recogida de datos personales):**
- Contact Form 7 — `wpcf7`, `/plugins/contact-form-7/`
- WPForms — `wpforms`, `/plugins/wpforms-lite/`
- Gravity Forms — `gform_`, `/plugins/gravityforms/`
- Ninja Forms — `nf-form`

**Email marketing (implican transferencia de datos a terceros):**
- Mailchimp — `list-manage.com`, `chimpstatic.com`
- Mailerlite — `mailerlite.com`
- ActiveCampaign — `activehosted.com`

**E-commerce (datos de pago + historial de compras):**
- WooCommerce — `woocommerce`, `/wc-ajax=`, `wc_cart_hash`

**Notificaciones push (recogen tokens de dispositivo):**
- OneSignal — `onesignal.com`
- PushEngage — `pushengage.com`

**Cache / rendimiento:**
- LiteSpeed Cache — header `X-LiteSpeed-Cache`, `lscache` en respuesta
- W3 Total Cache — `w3tc`
- WP Rocket — `wprocket`, `wp-rocket`

**Afiliados y redes publicitarias nativas:**
- AdSkeeper — `jsc.adskeeper.com`
- MGID — `jsc.mgid.com`
- Taboola — `cdn.taboola.com`
- Outbrain — `widgets.outbrain.com`
- Vidoomy — `ads.vidoomy.com`

### CDN

| CDN | Señal de detección |
|-----|--------------------|
| **Cloudflare** | Header `CF-Ray`, `Server: cloudflare` |
| **AWS CloudFront** | `cloudfront.net` en assets, header `X-Amz-Cf-Id` |
| **Fastly** | Header `X-Served-By` con `cache-`, dominio `fastly.com` |
| **Akamai** | Header `X-Check-Cacheable`, dominio `akamaized.net` |
| **BunnyCDN** | Dominio `b-cdn.net` en assets |
| **jsDelivr** | `cdn.jsdelivr.net` |

Nota: Cloudflare actúa como CDN y proxy inverso. Si está presente, la IP de origen
y el hosting real no son determinables externamente.

### Servidor y tecnología de alojamiento

Detectar a partir del header `Server` y `X-Powered-By`:

| Señal | Interpretación |
|-------|---------------|
| `Server: LiteSpeed` | LiteSpeed — frecuente en SiteGround, Hostinger, HostGator |
| `Server: Apache` | Apache — hosting compartido o VPS |
| `Server: nginx` | Nginx — VPS o hosting gestionado |
| `X-Powered-By: PHP/x.x` | Versión de PHP — relevante si < 8.0 (EOL) |
| `Server: cloudflare` | Hosting real no determinable externamente |

Cruzar con lo que la política de privacidad declare como proveedor de hosting.
Si hay discrepancia (política dice proveedor A, headers apuntan a B), registrarlo.

### Output del Paso 0

Presentar en el informe como **Sección 0 — Stack tecnológico** antes de la tabla
de cumplimiento, con este formato:

```
CMS:                    [nombre + versión si detectable, o "no determinado"]
Page builder:           [nombre o "no aplica / no detectado"]
CDN:                    [nombre o "no detectado"]
Servidor / hosting:     [nombre o "no determinable (Cloudflare proxy)"]
Plugins detectados:     lista agrupada por categoría
Scripts de terceros:    lista con dominio y finalidad probable
Implicación:            [p.ej. "sin plugin de cookies detectado → issue crítico previsible en Bloque 5"]
```

---

## Paso 1 — Recopilación de datos del sitio

Ejecutar en paralelo:

1. **WebFetch homepage** — detectar: sector, idioma, formularios visibles,
   banner de cookies, enlace a política de privacidad, datos que se recogen.
2. **WebFetch política de privacidad** — buscar el enlace en footer, header,
   formularios de contacto, y en rutas comunes: `/privacidad`, `/politica-de-privacidad`,
   `/privacy`, `/legal/privacidad`. Si no se encuentra, registrar como issue crítico.
3. **WebFetch página de contacto / formulario principal** — detectar campos
   solicitados, checkboxes de consentimiento, texto legal adjunto.
4. **Headers HTTP** — verificar HTTPS, HSTS, CSP, X-Frame-Options, Referrer-Policy.

No construir URLs. Usar solo las encontradas en el sitio.

---

## Paso 2 — Detección de sector

Analizar el contenido del homepage para clasificar el sitio en uno de estos sectores.
Un sitio puede pertenecer a más de uno.

| Sector | Señales de detección |
|--------|---------------------|
| **Salud / médico** | términos de salud, síntomas, diagnóstico, clínica, hospital, farmacia, ficha médica |
| **Ecommerce** | carrito de compras, productos con precio, checkout, SKUs, stock |
| **Fintech / financiero** | crédito, préstamo, inversión, cuenta, pago, CMF, Banco Central |
| **Educación** | cursos, alumnos, matrícula, colegio, universidad, menores de edad |
| **SaaS / tecnología** | software, API, suscripción, plan, dashboard, integración |
| **Medios / publicidad** | noticias, artículos, publicidad programática, newsletter |
| **Servicios profesionales** | consultoría, abogado, contador, RRHH, reclutamiento |
| **General / sin sector específico** | fallback si no hay señales claras |

Registrar sector(es) detectado(s). Aplicar requisitos adicionales del sector
en los bloques 7, 9 y 10 según corresponda.

---

## Paso 3 — Auditoría por bloques

Evaluar cada bloque. Asignar uno de cuatro estados:

- **Cumple** — verificado en el sitio live
- **Parcial** — presente pero incompleto
- **No cumple** — ausente o incorrecto
- **No evaluable** — requiere acceso al backend o no es visible externamente

### Bloque 1 — Identificación del responsable del tratamiento (art. 14 ter)
Peso: 10 pts

Verificar que en la política de privacidad aparezca:
- [ ] Nombre o razón social del responsable
- [ ] RUT o identificación legal
- [ ] Domicilio
- [ ] Dirección de correo o medio de contacto directo

Parcial si aparece el nombre pero faltan RUT o domicilio.
Si la entidad no tiene domicilio en Chile y trata datos de personas que residen en el
país, la ley **no exige representante**: exige "señalar y mantener actualizado y
operativo, un correo electrónico u otro medio de contacto idóneo" para los titulares y la
Agencia. Su ausencia es issue grave.

### Bloque 2 — Política de privacidad: existencia y acceso (art. 14 ter)
Peso: 5 pts

- [ ] Existe una política de privacidad publicada
- [ ] Enlace visible en el footer de todas las páginas
- [ ] Enlace accesible desde formularios que recogen datos
- [ ] Redactada en español (o idioma del sitio)
- [ ] Fecha de última actualización visible

### Bloque 3 — Política de privacidad: contenido mínimo (art. 14 ter, deber de información y transparencia)
Peso: 15 pts

Verificar que la política incluya explícitamente:
- [ ] **a)** Finalidad(es) del tratamiento — para qué se usan los datos
- [ ] **b)** Base legal de cada finalidad (ver Bloque 4 para las 6 bases válidas)
- [ ] **c)** Tipos de datos que se recogen
- [ ] **d)** Destinatarios o categorías de destinatarios (terceros, proveedores, filiales)
- [ ] **e)** Plazos de conservación o criterios para determinarlos
- [ ] **f)** Derechos del titular: acceso, rectificación, cancelación, oposición, portabilidad,
     limitación y derecho a no ser objeto de decisiones basadas exclusivamente en
     tratamiento automatizado
- [ ] **g)** Procedimiento para ejercer derechos y plazo de respuesta (30 días corridos,
     prorrogables una vez por 30; bloqueo temporal en 2 días hábiles — art. 11)
- [ ] **h)** Transferencias internacionales (si aplica) y garantías adoptadas
- [ ] **i)** Uso de cookies y tecnologías de rastreo
- [ ] **j)** Contacto del delegado de protección de datos (si se designó)
- [ ] **k)** Derecho a reclamar ante la Agencia de Protección de Datos Personales

Las letras de esta lista son un orden de trabajo de la skill, no las letras del art. 14 ter.

Adicionalmente, la ley exige que los elementos esenciales (categorías de datos,
finalidades, derechos del titular) sean **visibles de forma destacada** en el sitio
(no solo en un documento largo). Verificar que exista al menos un resumen accesible
o que la política sea de lectura razonablemente directa.

Puntuación parcial: 1 pt por ítem presente, máx. 15.

### Bloque 4 — Base legal del tratamiento declarada (arts. 12 y 13: consentimiento en el 12, las demás bases en el 13)
Peso: 10 pts

La Ley 21.719 reconoce seis bases legales válidas. Verificar que la política:
- [ ] Declare la base legal de cada finalidad de tratamiento
- [ ] Use las bases correctas — las seis válidas son:
  1. Consentimiento del titular
  2. Cumplimiento de obligación legal del responsable
  3. Ejecución de un contrato en que el titular es parte (o medidas precontractuales)
  4. Interés legítimo del responsable o de un tercero
  5. Obligaciones económicas, financieras, bancarias o comerciales (base específica de la ley chilena)
  6. Establecimiento, ejercicio o defensa de pretensiones legales
- [ ] No use "consentimiento" como base cuando el tratamiento es necesario para el contrato
- [ ] Los formularios de captación no usen casillas pre-marcadas
- [ ] Se distinga entre finalidades obligatorias y opcionales

**Privacidad por diseño (verificación externa):**
- [ ] Los formularios solicitan solo los datos estrictamente necesarios para la finalidad declarada
- [ ] Las opciones de suscripción a comunicaciones comerciales no están pre-seleccionadas

### Bloque 5 — Consentimiento, cookies y marketing directo (Art. 12)
Peso: 15 pts

⚠️ Nota: La Ley 21.719 no contiene un artículo específico de cookies — los requisitos
derivan de las reglas generales de consentimiento (Art. 12) y de la guía SERNAC.
Los ítems de granularidad y rechazo equivalente son mejores prácticas del estándar
internacional, no obligaciones expresas de la ley chilena. Se incluyen como buenas
prácticas recomendadas; marcarlos como "Parcial" si no se cumplen, no como "No cumple".

**Banner de cookies:**
- [ ] Existe banner o mecanismo de consentimiento de cookies
- [ ] El banner bloquea cookies no esenciales hasta obtener consentimiento activo
- [ ] No hay cookies de análisis, publicidad o rastreo activas antes del consentimiento
- [ ] *(Buena práctica)* Existe opción de configuración granular (analítica / marketing / funcional)
- [ ] *(Buena práctica)* El rechazo es tan accesible como la aceptación

**Formularios:**
- [ ] Los formularios con tratamiento de datos incluyen checkbox de consentimiento no pre-marcado
- [ ] El checkbox vincula a la política de privacidad
- [ ] Se indica la finalidad concreta del formulario antes de enviar

**Marketing directo:**
La ley otorga al titular el derecho de oposición específico al marketing directo.
El responsable debe cesar ese tratamiento al recibir la oposición. Verificar:
- [ ] Si el sitio tiene newsletter o comunicaciones comerciales: ¿existe un mecanismo
     de baja/opt-out claro (enlace en email, formulario, o dirección de contacto)?
- [ ] ¿La política menciona el derecho de oposición al marketing directo?
- [ ] Si hay formulario de suscripción a comunicaciones: ¿el checkbox de marketing
     es independiente del consentimiento para el servicio principal?

Verificar cookies de terceros activas antes del consentimiento inspeccionando el
código fuente del homepage. Si el banner no existe o es solo informativo, reportar
el ítem de bloqueo como No cumple.

### Bloque 6 — Derechos del titular: canal habilitado
Peso: 15 pts

⚠️ Nota: La numeración exacta de los artículos de derechos del titular en el texto
oficial publicado no ha podido confirmarse directamente en esta versión del skill
(la BCN no siempre es accesible). Las referencias de artículo para este bloque se
omiten hasta verificación y se cita solo la ley en general. No afecta al contenido
de los checklists. Excepción verificada el 2026-10-01: el plazo de respuesta está en
el art. 11. Cuando la web de la BCN no carga, el texto oficial completo se obtiene con
`https://nuevo.leychile.cl/servicios/Navegar/get_norma_json?idNorma=1209272` (JSON).

La Ley 21.719 reconoce **siete derechos del titular**:
1. Acceso
2. Rectificación
3. Cancelación / Supresión
4. Oposición
5. Portabilidad
6. Limitación del tratamiento
7. No ser objeto de decisiones basadas exclusivamente en tratamiento automatizado

Verificar:
- [ ] Existe un mecanismo explícito para ejercer derechos (email, formulario, dirección postal)
- [ ] Se menciona el plazo de respuesta: 30 días corridos desde el ingreso de la solicitud,
     prorrogables una sola vez por otros 30 días corridos, y 2 días hábiles para la solicitud
     de bloqueo temporal (art. 11 de la Ley 19.628, texto modificado por la Ley 21.719).
     No usar "15 días hábiles": ese plazo de la ley corresponde a impugnaciones y descargos
     ante la Agencia, no a la respuesta del responsable al titular
- [ ] Se mencionan los **siete** derechos, incluidos Portabilidad, Limitación y el
     derecho frente a decisiones automatizadas
- [ ] Se indica qué información debe adjuntar el titular al hacer la solicitud
- [ ] Se menciona el derecho a reclamar ante la Agencia de Protección de Datos Personales
     si la solicitud no es atendida o es rechazada

**Decisiones automatizadas — verificación adicional:**
Si el sitio usa scoring, recomendaciones algorítmicas, aprobación automática de
créditos o cualquier sistema de decisión automatizado con efectos sobre el titular:
- [ ] ¿La política menciona este tipo de tratamiento?
- [ ] ¿Existe canal para solicitar revisión humana de la decisión?

### Bloque 7 — Datos sensibles (art. 2 g y art. 16) y datos de niños, niñas y adolescentes
Peso: 10 pts

Primero determinar si el sitio recoge datos sensibles. El art. 2 g) define como datos
sensibles los que revelen:
- Origen étnico o racial
- Afiliación política, sindical o gremial
- Situación socioeconómica
- Convicciones ideológicas o filosóficas
- Creencias religiosas
- Datos relativos a la salud
- Perfil biológico humano
- Datos biométricos
- Vida sexual, orientación sexual e identidad de género

**Los datos de niños, niñas y adolescentes no son datos sensibles: tienen un régimen
propio** (art. 16 quáter). La propia ley fija los tramos: niños y niñas son los menores
de 14 años, y adolescentes los mayores de 14 y menores de 18. Para menores de 14 años se
requiere el consentimiento de padres o representantes legales.

**Si el sitio no recoge ninguna de estas categorías:** bloque N/A, asignar 10 pts automáticamente.

**Si recoge datos sensibles:**
- [ ] Se identifican explícitamente como datos sensibles en la política
- [ ] Se solicita consentimiento explícito y diferenciado (no agrupado con otros datos)
- [ ] Se indica finalidad específica para esos datos
- [ ] Se mencionan medidas de seguridad reforzadas en la política

**Requisitos adicionales por sector:**

*Salud/médico:*
- [ ] Datos de salud tratados solo con consentimiento del paciente o autorización legal
- [ ] No se comparten datos clínicos con terceros sin consentimiento específico
- [ ] Si hay ficha clínica electrónica, se indica el marco legal aplicable (Ley 20.584 superpuesta)

*Educación (menores):*
- [ ] Datos de menores requieren consentimiento del padre/madre/tutor (verificar umbral
     exacto cuando se publique el reglamento)
- [ ] Se identifica explícitamente si el servicio está dirigido a menores
- [ ] No se solicita domicilio ni teléfono como datos requeridos para menores

*Ecommerce:*
- [ ] Datos de pago no se almacenan localmente si se usa pasarela de terceros (indicarlo)
- [ ] Historial de compras declarado como dato personal con plazo de retención

*Fintech/financiero:*
- [ ] Se menciona la regulación CMF superpuesta si aplica
- [ ] Datos financieros tratados con garantías adicionales (base legal 5 — obligaciones
     económico-financieras — o consentimiento explícito)

### Bloque 8 — Transferencias internacionales (arts. 27 a 29)
Peso: 10 pts

Detectar transferencias probables: CDNs, plataformas de email marketing, CRMs,
herramientas de análisis, servicios en la nube con sede fuera de Chile.

- [ ] La política declara si se realizan transferencias internacionales
- [ ] Se identifican los países o regiones de destino
- [ ] Se indica la garantía adoptada. Las vías de los arts. 27 y 28 son:
  - País con nivel de protección adecuado, determinado por la Agencia (art. 28)
  - Cláusulas contractuales u otros instrumentos jurídicos con garantías adecuadas
  - Normas corporativas vinculantes / Binding Corporate Rules (BCR)
  - Modelo de cumplimiento o certificación
  - Sin esas garantías, solo transferencias **específicas y no habituales** en los casos
    que la ley enumera (por ejemplo, con consentimiento expreso). El consentimiento no
    sirve como garantía general para flujos habituales, como la analítica
- [ ] Si no se realizan transferencias internacionales, se indica explícitamente

### Bloque 9 — Seguridad técnica (art. 14 quinquies) y vulneraciones (art. 14 sexies)
Peso: 5 pts

La ley exige medidas que garanticen **confidencialidad, integridad, disponibilidad
y resiliencia** del tratamiento. Verificar lo observable externamente:

- [ ] HTTPS activo en todas las páginas (sin mixed content)
- [ ] Certificado SSL válido y no expirado
- [ ] HSTS habilitado (Strict-Transport-Security en headers)
- [ ] No hay redirección de HTTP a HTTPS rota
- [ ] La política menciona las medidas de seguridad y, preferiblemente, los cuatro
     atributos: confidencialidad, integridad, disponibilidad y resiliencia

**Sector salud / fintech:** verificar también:
- [ ] CSP (Content-Security-Policy) configurado
- [ ] X-Frame-Options o frame-ancestors configurado

**Vulneraciones (art. 14 sexies):** el responsable debe reportarlas a la Agencia "por los
medios más expeditos posibles y sin dilaciones indebidas", y comunicarlas también a los
titulares cuando afecten datos sensibles, datos de menores de 14 años o datos de
obligaciones económicas, financieras, bancarias o comerciales.
- [ ] La política describe cómo se gestionan y comunican las vulneraciones de seguridad

### Bloque 10 — Delegado de protección de datos (art. 50, voluntario)
Peso: 5 pts

⚠️ Nota: a diferencia del RGPD (Art. 37), la ley chilena **no obliga** a designar un
delegado: el art. 50 dice que el responsable "podrá designar" uno, que nombra la máxima
autoridad directiva. Es una pieza del modelo de prevención de infracciones (arts. 49 a
52), que también es voluntario y, si se certifica, puede atenuar la responsabilidad.

Verificar:
- [ ] Si existe delegado: nombre o rol publicado
- [ ] Si existe delegado: dirección de contacto publicada
- [ ] Si no existe: no es un incumplimiento; registrar "Delegado no designado (voluntario,
      art. 50)" y asignar pts completos

Si el sitio menciona estar acogido a un modelo de prevención certificado:
- [ ] Indica el organismo certificador
- [ ] Menciona el alcance y vigencia de la certificación

---

## Paso 4 — Score global

```
Score = suma de puntos obtenidos en cada bloque / 100
```

| Rango | Interpretación |
|-------|---------------|
| 80–100 | Postura defensible — cumplimiento sustancial |
| 60–79 | Riesgo moderado — gaps importantes sin issues críticos |
| 40–59 | Riesgo alto — múltiples incumplimientos relevantes |
| 0–39 | Riesgo crítico — ausencia de elementos esenciales |

Los bloques con estado "No evaluable" no penalizan ni suman.
Los bloques N/A (datos sensibles cuando no aplica) suman pts completos.

---

## Paso 5 — Clasificación de issues y sanciones asociadas

La Ley 21.719 establece tres niveles de infracción. Incluir el riesgo de sanción
en cada issue del informe para contextualizar el impacto económico real.

| Nivel | Multa máxima | Ejemplos de conductas |
|-------|-------------|----------------------|
| Gravísima | Hasta 20.000 UTM | Tratar datos sensibles sin consentimiento; transferir datos internacionalmente sin garantías; vulnerar datos sin notificar |
| Grave | Hasta 10.000 UTM | No atender derechos del titular; falta de política de privacidad; no tener base legal declarada |
| Leve | Amonestación escrita o hasta 5.000 UTM | Política incompleta; falta de enlace en footer; plazos de retención no especificados |

Montos del art. 35. **Reincidencia** (art. 36): hay reincidencia cuando el responsable fue
sancionado dos o más veces en los últimos treinta meses. En ese caso la multa puede llegar
al triple y, si no es empresa de menor tamaño (Ley 20.416), al 2 % de los ingresos
anuales en infracciones graves o al 4 % en gravísimas. Las empresas de menor tamaño pueden
recibir amonestación en vez de multa durante los primeros 12 meses de vigencia (art. sexto
transitorio). UTM = Unidad Tributaria Mensual: convertir a CLP con el valor del mes de la
auditoría (sii.cl) y no usar equivalencias en USD sin fecha.

**Crítico** (bloquea cumplimiento mínimo — riesgo gravísimo o grave):
- Política de privacidad inexistente → riesgo grave
- Sin mecanismo de ejercicio de derechos → riesgo grave
- Cookies no esenciales activas sin consentimiento → riesgo grave
- Datos sensibles tratados sin consentimiento explícito diferenciado → riesgo gravísimo
- Sin HTTPS → riesgo grave (falla en integridad y confidencialidad)
- Sin base legal declarada para ninguna finalidad → riesgo grave
- Entidad sin domicilio en Chile que no informa un correo u otro medio de contacto idóneo y operativo → riesgo grave

**Medio** (gap relevante — riesgo grave o leve, plazo recomendado 30–60 días):
- Política existe pero falta base legal por finalidad → riesgo grave
- Derechos mencionados pero sin canal ni plazo de respuesta → riesgo grave
- Derecho a no ser objeto de decisiones automatizadas no mencionado → riesgo grave
- Transferencias internacionales no declaradas → riesgo gravísimo si se realizan
- Banner de cookies solo informativo (sin rechazo activo) → riesgo grave
- Marketing directo sin mecanismo de baja → riesgo grave

**Bajo** (mejora de postura — riesgo leve):
- Falta fecha de actualización en la política
- Delegado de protección de datos no mencionado (voluntario, solo informativo)
- Política sin enlace desde formularios secundarios
- Plazos de retención no especificados para algún tipo de dato
- Política no menciona los cuatro atributos de seguridad

---

## Paso 6 — Output según modo

### Modo interno (Markdown, sin `--docx`)

```markdown
# Auditoría Ley 21.719 — [dominio]
Fecha: [fecha]  |  Sector: [sector detectado]  |  Score: [X/100]

## Stack tecnológico
CMS: [nombre]  |  CDN: [nombre]  |  Servidor: [nombre]
Plugins relevantes: [lista]
Scripts de terceros activos: [lista con finalidad]
Implicación: [nota sobre lo que el stack anticipa en la auditoría]

## Resumen
[2–3 líneas: postura general, issues críticos detectados, riesgo sancionador]

## Tabla de cumplimiento
| Bloque | Peso | Pts obtenidos | Estado | Evidencia |
|--------|------|--------------|--------|-----------|
| 1. Identificación responsable | 10 | X | Cumple/Parcial/No cumple | ... |
...

## Issues críticos

**[Nombre del issue]** (Bloque X — Ley 21.719)
Evidencia: [qué se encontró o qué falta]
Riesgo sancionador: [Infracción grave/gravísima — hasta X UTM]
→ Acción: [qué hay que hacer concretamente]

## Issues medios

**[Nombre del issue]** (Bloque X — Ley 21.719)
Evidencia: [qué se encontró o qué falta]
Riesgo sancionador: [nivel y multa estimada]
→ Acción: [qué hay que hacer]
→ Plazo sugerido: [30 / 60 días]

## Issues bajos

**[Nombre del issue]** (Bloque X — Ley 21.719)
→ Acción: [qué hay que hacer]

## Notas metodológicas
- Qué se verificó externamente
- Qué requiere acceso al backend para confirmar
- Advertencia: reglamento de la ley en elaboración — algunos requisitos pueden
  refinarse cuando se publique (estimado 2026–2027)
```

---
_Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search_

Guardar en `<directorio-de-auditorias>/[cliente o dominio]/auditoria_ley21719_[fecha].md`.

### Modo informe cliente (`--docx`)

Preguntar primero: "¿Quieres el informe en lenguaje técnico o ejecutivo simplificado?"

Estructura del .docx:
1. Portada: dominio, fecha, score global, sector
2. Resumen ejecutivo (máx. 1 página, sin jerga legal, incluir riesgo sancionador total estimado)
3. Stack tecnológico: CMS, page builder, CDN, servidor, plugins detectados, scripts de terceros activos e implicación para el cumplimiento
4. Tabla de cumplimiento con semáforo visual (Cumple / Parcial / No cumple)
5. Issues críticos con acción concreta, artículo / obligación infringida y riesgo de multa
6. Issues medios con recomendación, plazo sugerido y riesgo de multa
7. Issues bajos como listado
8. Próximos pasos priorizados (top 5)
9. Nota metodológica: qué se auditó externamente, qué está fuera de scope y
   advertencia sobre el reglamento en elaboración
10. Pie de página (en todas las páginas del documento): texto "Desarrollado por Zythos Media — Especialistas en SEO & IA Search" con hipervínculo sobre "Zythos Media" apuntando a https://zythos.media

Guardar en `<directorio-de-auditorias>/[cliente o dominio]/auditoria_ley21719_[fecha].docx`.

### Comparativa RGPD (solo si el usuario lo solicita explícitamente)

Añadir columna "Equivalente RGPD" en la tabla de cumplimiento y sección de gaps
entre Ley 21.719 y RGPD relevantes para el sitio auditado.
No incluir por defecto.

---

## Integración con el stack SEO y anonimización

### Cuándo se invoca esta skill automáticamente

`/seo audit <url>` la lanza como subagente condicional cuando detecta sitio chileno.
Señales de detección: TLD `.cl`, RUT/SII/CMF/SERNAC en el contenido, moneda CLP.
El score de cumplimiento Ley 21.719 se integra en el reporte unificado del audit.

### Flujos de trabajo combinados

**Auditoría completa de sitio chileno:**
```
/seo audit <url>           → lanza ley-datos-chile automáticamente
/ley-datos-chile <url>     → auditoría standalone si solo se necesita cumplimiento legal
```

**Post-auditoría recomendada (según hallazgos):**

| Hallazgo en ley-datos-chile | Skill a invocar después |
|-----------------------------|------------------------|
| Schema de política de privacidad ausente o mejorable | `/seo schema <url>` |
| Headers de seguridad insuficientes (Bloque 9) | `/seo technical <url>` — sección Security |
| Cookie consent sin configurar correctamente | `/seo technical <url>` — sección JS Rendering |
| Sitio con datos sensibles de salud | `/seo local <url>` si es clínica/consultorio — detecta señales E-E-A-T médico |
| Transferencias a CDN/plataformas internacionales no declaradas | `/seo geo <url>` — identifica terceros con rastreadores activos |

**Antes de compartir el reporte:**
```
# Anonimizar reporte si contiene PII del cliente auditado
/anonimizar <directorio-de-auditorias>/[cliente]/auditoria_ley21719_[fecha].md --ley chile
/anonimizar <directorio-de-auditorias>/[cliente]/auditoria_ley21719_[fecha].docx --ley chile
```

Usar `--ley chile` (no `--ley todo`) para evitar falsos positivos en números de artículos.

### Notas sobre skills de terceros

`seo-audit` y `seo` son de AgriciDaniel/claude-seo v2.2.0 — se sobreescriben al actualizar.
Tras cada actualización de claude-seo, re-aplicar:
- Línea en `seo-audit`: spawn condicional de `ley-datos-chile` para sitios `.cl`
- Línea en `seo` quick reference: `/ley-datos-chile <url>`
- Línea en `seo` orchestration: paso `10b` de detección de sitio chileno

---

## Notas de alcance

Esta auditoría cubre lo verificable externamente sin acceso al backend:
- Documentos públicos del sitio
- Comportamiento observable de cookies y formularios
- Headers HTTP

Quedan fuera de scope sin acceso interno:
- Contratos con encargados del tratamiento (data processors) — art. 15 bis
- Registros de actividades de tratamiento — Art. 15
- Procedimientos internos de respuesta a solicitudes de derechos
- Medidas de seguridad técnicas internas (cifrado en reposo, control de accesos)
- Reportes de vulneraciones a la Agencia (art. 14 sexies)
- Modelos de cumplimiento certificados y su contenido interno

Siempre indicar este alcance en la sección de notas metodológicas del informe.

---

## Actualización normativa

- **Ley 21.719** publicada el 13 de diciembre de 2024.
- **Vigencia: 15/10/2027.** La ley de postergación (Boletín 18.623-07, despachada por el
  Congreso el 17/11/2026 sin modificaciones) sustituye la regla original del artículo
  primero transitorio (01/12/2026) por esa fecha fija. Amplía el Consejo Directivo de la
  Agencia de 3 a 5 miembros, con mandato de 6 años sin reelección y renovación parcial, y
  pide enviar la primera nómina al Senado al menos 9 meses antes de la vigencia. **No
  cambia obligaciones ni multas.** El régimen de amonestación para empresas de menor tamaño
  durante los primeros 12 meses (artículo sexto transitorio) se mantiene; se rechazó
  extenderlo a todas las empresas.
  - Al 20/11/2026 faltaba la publicación en el Diario Oficial: cuando se publique, anotar
    aquí el número de ley y la fecha de publicación (diariooficial.interior.gob.cl y la
    ficha de la BCN, idNorma 1209272).
  - Hasta el 15/10/2027 sigue rigiendo la Ley 19.628 original, sin interés legítimo como
    base de licitud y sin Agencia: presentar la auditoría como **preparación para la
    vigencia**, no como incumplimiento actual sancionable.
- **Reglamentos:** sin publicar al 20/11/2026; pueden precisar adecuación de países,
  certificación y modelo de prevención.
- **Agencia de Protección de Datos Personales:** se constituye con la vigencia de la ley. El
  CPLT no ejerce sus funciones en ningún momento (art. 31: solo coordinación).
- **Versión de esta skill:** 1.3.1 (2026-11-20). Vigencia al 15/10/2027 (ley de postergación,
  Boletín 18.623-07). Versión 1.3.0 (2026-11-20). Cambios: artículos verificados en el texto
  oficial de la BCN (idNorma 1209272): delegado voluntario (art. 50), encargado (art. 15 bis),
  información (14 ter), seguridad (14 quinquies), vulneraciones (14 sexies), transferencias
  (27-29), sanciones y reincidencia (35-36); el CPLT no asume funciones; sin exigencia de
  representante para extranjeros (basta un medio de contacto); datos sensibles según el
  art. 2 g) y menores con régimen propio; estado del Boletín 18.623-07.
  Versión anterior: 1.2.2 (2026-10-01). Cambios: plazo de respuesta a solicitudes de derechos corregido a 30 días corridos prorrogables por 30, y bloqueo temporal en 2 días hábiles (art. 11, verificado en el texto oficial de la BCN), en Bloques 3 y 6; endpoint JSON de la BCN para obtener el texto oficial. Versión anterior: 1.2.1 (2026-07-03) — crédito Zythos Media añadido al inicio de ejecución, plantilla Markdown y pie de página del .docx. Verificar actualizaciones cuando se publique el reglamento o cuando la APDP emita sus primeras instrucciones.
