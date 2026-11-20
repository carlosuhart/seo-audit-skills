---
name: uk-gdpr
description: >
  Auditoría UK GDPR y PECR 2003 (Reino Unido tras el Brexit): detecta el sector y
  entrega informe con score, estado por artículo, issues priorizados y sanciones en GBP.
  Sub-skill de /privacidad, también invocable sola.
user-invokable: true
argument-hint: "<url> [--docx]"
license: MIT
metadata:
  author: Zythos Media
  version: "1.1.0"
  category: legal-compliance
  revisar: "2027-05-20"
---

# UK GDPR + PECR — Auditoría de Cumplimiento

## Uso

```
/uk-gdpr https://ejemplo.co.uk
/uk-gdpr https://ejemplo.co.uk --docx
```

Sin `--docx` el output es Markdown interno. Con `--docx` genera informe
ejecutivo en formato Word.

Si el usuario no especifica formato, preguntar antes de generar el documento.

---

## Marco normativo aplicable

- **UK GDPR**: Reglamento UE 2016/679 tal como quedó incorporado al derecho
  del Reino Unido mediante la European Union (Withdrawal) Act 2018. Los artículos
  conservan la misma numeración que el RGPD europeo. Supervisado por la ICO.
- **Data Protection Act 2018 (DPA 2018)**: complementa el UK GDPR con disposiciones
  nacionales (tratamiento de datos de empleados, inteligencia, etc.).
- **PECR 2003** (Privacy and Electronic Communications Regulations): transpone la
  Directiva ePrivacy 2002/58/CE. Regula cookies, comunicaciones de marketing y
  redes de comunicación electrónica. Reformada por la DUAA 2025: nuevas excepciones
  al consentimiento de cookies (Anexo A1) y multas alineadas con el UK GDPR, ambas
  desde el 05/02/2026.
- **Children's Code (Age Appropriate Design Code, 2021)**: código de la ICO para
  servicios online dirigidos a menores de 18 años. Establece 15 estándares de
  privacidad por diseño para este segmento.
- **Data (Use and Access) Act 2025 (DUAA)**: sanción real el 19/06/2025. El grueso de
  la Parte 5, que modifica el UK GDPR, la DPA 2018 y las PECR, rige desde el 05/02/2026
  (SI 2026/82, https://www.legislation.gov.uk/uksi/2026/82/made). El deber de gestionar
  reclamaciones rige desde el 19/06/2026, y la Information Commission sustituye al
  Information Commissioner desde el 30/09/2026. Cambios que importan en una auditoría
  web: excepciones nuevas al consentimiento de cookies, intereses legítimos reconocidos,
  decisiones automatizadas (Arts. 22A-22D), reclamaciones ante el responsable y multas
  PECR de hasta £17.500.000 o el 4 %.

⚠️ El UK GDPR es normativa británica independiente desde Brexit. No confundir
con el RGPD europeo (UE). La UE renovó su decisión de adecuación para el Reino Unido
el 19/12/2025, con vigencia hasta el 27/12/2031. Son dos marcos jurídicos distintos
con articulación bilateral.

---

## Nota sobre la autoridad de control

**Information Commission (sigue usando la sigla ICO)**
Desde el 30/09/2026 la autoridad es la Information Commission, un órgano colegiado
que sucede al Information Commissioner con las mismas funciones (DUAA 2025). En los
informes se puede seguir escribiendo "ICO".
Web: ico.org.uk | Notificación de brechas: ico.org.uk/report-a-breach
Registro de responsables: ico.org.uk/registration (obligatorio para la mayoría)

El Reino Unido no participa en el CEPD/EDPB desde Brexit. La ICO emite sus
propias directrices y participa en el Global Privacy Assembly.

---

## Crédito de herramienta

Al iniciar cualquier auditoría, emitir esta línea antes del output principal:

> Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search

---

## Paso 0 — Identificación del stack tecnológico

Si este skill es invocado desde el orquestador `/privacidad`, usar el Paso 0
compartido. Si se invoca directamente, ejecutar el Paso 0 del skill `rgpd` —
la detección de stack es idéntica. No duplicar.

---

## Paso 1 — Recopilación de datos del sitio

Igual al skill `rgpd` Paso 1, adaptando las rutas de búsqueda de la política:
- Rutas comunes en UK: `/privacy`, `/privacy-policy`, `/data-protection`,
  `/cookie-policy`, `/legal/privacy`.
- Verificar también la sección de footer y cualquier enlace "Privacy" o "Cookies"
  en la navegación principal.

---

## Paso 2 — Detección de sector

Usar la misma matriz de sectores del skill `rgpd`. Añadir:

| Sector | Señales adicionales UK |
|--------|------------------------|
| **Servicios financieros** | FCA (Financial Conduct Authority), FCA register, "authorised by FCA" |
| **Salud** | NHS, CQC (Care Quality Commission), "regulated by CQC" |
| **Educación** | Ofsted, "academy trust", DfE registration |
| **Medios** | Ofcom, BBC, ITV, licencia de broadcasting |

---

## Paso 3 — Auditoría por bloques

Evaluar cada bloque: **Cumple / Parcial / No cumple / No evaluable**

### Bloque 1 — Identificación del responsable (Art. 13/14 UK GDPR + Art. 27 UK GDPR)
Peso: 10 pts

- [ ] Nombre o razón social del responsable del tratamiento
- [ ] Domicilio en el Reino Unido (o representante en UK si el responsable no tiene establecimiento en UK)
- [ ] Dirección de correo electrónico o formulario de contacto para protección de datos
- [ ] Número de Companies House o equivalente (no obligatorio por UK GDPR pero su presencia facilita verificación)

**Representante en UK (Art. 27 UK GDPR):**
Si el responsable no tiene establecimiento en el Reino Unido pero ofrece bienes
o servicios a interesados en el UK o monitoriza su comportamiento:
- [ ] Designación de representante en UK en la política
- [ ] Datos de contacto del representante publicados
- [ ] El representante está establecido en el Reino Unido

**Registro en la ICO:**
La mayoría de organizaciones que tratan datos personales deben registrarse en la ICO
(tarifa anual). No es auditable externamente, pero su mención en la política como
señal de cumplimiento proactivo es positiva.
- [ ] ¿La política menciona el número de registro ICO o el estado de registro?

### Bloque 2 — Política de privacidad: existencia y acceso (Art. 12 UK GDPR)
Peso: 5 pts

- [ ] Existe política de privacidad publicada
- [ ] Enlace visible en el footer de todas las páginas
- [ ] Enlace accesible desde formularios que recogen datos personales
- [ ] Redactada en inglés (o idioma del sitio) con lenguaje claro y sencillo (Art. 12.1)
- [ ] Fecha de última actualización visible

### Bloque 3 — Política de privacidad: contenido mínimo (Art. 13/14 UK GDPR)
Peso: 15 pts

Mismos ítems que el skill `rgpd` Bloque 3 (Art. 13/14 conservan numeración idéntica).
Verificar adicionalmente:
- [ ] Se menciona la ICO como autoridad de control competente (no la AEPD u otra DPA europea)
- [ ] Se menciona el derecho a reclamar ante la ICO (ico.org.uk/make-a-complaint)
- [ ] Si aplica el Children's Code: se menciona el tratamiento de datos de menores
      de 18 años bajo los 15 estándares del código

### Bloque 4 — Base jurídica del tratamiento + privacidad por diseño (Art. 6 + Art. 25 UK GDPR)
Peso: 10 pts

Las seis bases jurídicas son idénticas al RGPD (Art. 6.1 UK GDPR).
Verificar los mismos ítems del skill `rgpd` Bloque 4.

Añadir verificación específica UK:
- [ ] Si se invoca "interés legítimo" (Art. 6.1f): menciona el Legitimate Interests
      Assessment (LIA) — equivalente UK al test de equilibrio europeo
- [ ] Excepción desde el 05/02/2026: para los **intereses legítimos reconocidos** del
      Anexo 1 del UK GDPR (añadido por la DUAA: seguridad nacional, emergencias,
      prevención de delitos, protección de personas vulnerables, entre otros) no se
      exige el test de ponderación. En un sitio comercial es raro que apliquen: la
      analítica y la publicidad siguen necesitando LIA o consentimiento

### Bloque 5 — Consentimiento, cookies y marketing directo (Art. 7 UK GDPR + PECR 2003)
Peso: 15 pts

**Marco de cookies: PECR 2003 Regulation 6 y Anexo A1 (DUAA 2025)**
Las PECR exigen consentimiento previo e informado para almacenar información o
acceder a información en el dispositivo del usuario. El estándar de consentimiento
debe cumplir el UK GDPR Art. 7, y el consentimiento "implícito por continuar
navegando" no es válido.

**Excepciones sin consentimiento desde el 05/02/2026** (sección 112 y Anexo 12 de la
DUAA, nuevo Anexo A1 de las PECR, https://www.legislation.gov.uk/ukpga/2025/18/schedule/12):
- Lo estrictamente necesario para el servicio que pide el usuario, y la transmisión.
- **Estadísticas propias** para mejorar el servicio o el sitio, solo si: se usan solo
  para eso, no se comparten salvo para esa mejora, se informa con claridad y hay un
  medio **simple y gratuito para oponerse**.
- **Apariencia o funcionalidad** del sitio (preferencias del usuario), con las mismas
  condiciones.
- Geolocalización en emergencias.

La publicidad, el perfilado y la analítica de terceros que reutiliza los datos siguen
exigiendo consentimiento. La ICO publicó su guía final sobre tecnologías de
almacenamiento y acceso el 29/04/2026; según los resúmenes publicados, lee la excepción
de analítica de forma estrecha (medir el rendimiento del propio sitio entra; conocer a la
audiencia con fines comerciales, no). Antes de un informe de cliente, leer la guía en
ico.org.uk para confirmar el alcance exacto. Si un cliente declara su analítica como exenta, la auditoría verifica
las cuatro condiciones, en especial que el medio de oposición exista y funcione.

**Banner de cookies:**
- [ ] Existe banner o CMP
- [ ] El banner bloquea cookies no esenciales hasta obtener consentimiento activo
- [ ] No hay cookies de publicidad o rastreo activas antes del consentimiento
- [ ] Si hay analítica activa sin consentimiento: cumple las cuatro condiciones de la
      excepción estadística (uso propio para mejora, sin compartir, información clara,
      medio simple y gratuito para oponerse). Si falta una, es un incumplimiento
- [ ] Opción de rechazo tan accesible como la aceptación
- [ ] Configuración granular por categoría
- [ ] Enlace a política de cookies en el propio banner
- [ ] El consentimiento es revocable fácilmente

**Formularios (Art. 7 UK GDPR):**
- [ ] Checkbox de consentimiento no pre-marcado cuando la base es el consentimiento
- [ ] Checkbox vincula a la política de privacidad
- [ ] Finalidad declarada antes de enviar

**Consentimiento de menores:**
El UK GDPR (Art. 8) fija la edad en **13 años** para servicios de la sociedad
de la información (inferior al default de 16 años del RGPD europeo).
El Children's Code amplía la protección a todos los menores de 18 en servicios
online dirigidos a ellos.
- [ ] Si el sitio puede captar menores de 13: mecanismo de verificación de edad o
      consentimiento parental
- [ ] Si el sitio va dirigido a menores de 18: aplicar los 15 estándares del Children's Code
      (privacidad por defecto, geolocalización off por defecto, no perfilado sin consentimiento,
      no nudge techniques, etc.)
- [ ] Si no va dirigido a menores: declararlo explícitamente

**Marketing directo (PECR 2003 + Art. 21.2 UK GDPR):**
- [ ] Si hay email marketing: existe mecanismo de baja claro (enlace unsubscribe)
- [ ] El opt-out no requiere más pasos que el opt-in
- [ ] La política menciona el derecho de oposición al marketing directo

### Bloque 6 — Derechos del interesado (Art. 15–22 UK GDPR + Art. 12)
Peso: 15 pts

Los derechos de acceso (15), rectificación (16), supresión (17), limitación (18),
portabilidad (20), oposición (21) y retirada del consentimiento (7.3) conservan la
numeración del RGPD. Plazo de respuesta: **un mes** (Art. 12.3).

**Decisiones automatizadas: Arts. 22A-22D UK GDPR desde el 05/02/2026** (sustituyen al
Art. 22, sección 80 de la DUAA). Se permite la decisión automatizada significativa,
salvo con datos de categorías especiales, si hay salvaguardas: informar de ella,
permitir impugnarla y obtener intervención humana.

Verificar los mismos ítems del skill `rgpd` Bloque 6.

Verificación adicional UK:
- [ ] Se menciona el derecho a reclamar ante la **ICO** (no otras DPAs europeas)
- [ ] Se indica cómo presentar una Data Subject Access Request (DSAR)
- [ ] **Reclamaciones ante el responsable (desde el 19/06/2026):** la política ofrece un
      medio para reclamar directamente (formulario o correo). El responsable debe acusar
      recibo en 30 días y responder sin demora indebida
- [ ] Si hay decisiones automatizadas significativas: la política las informa y explica
      cómo impugnarlas y pedir intervención humana (Arts. 22A-22D)

### Bloque 7 — Categorías especiales y menores (Art. 9 UK GDPR + Children's Code)
Peso: 10 pts

Las categorías especiales son idénticas al RGPD (Art. 9.1 UK GDPR). Las bases
de excepción (Art. 9.2) conservan la misma numeración.

Verificar los mismos ítems del skill `rgpd` Bloque 7 con estas diferencias:

**Menores:**
- Umbral para consentimiento propio: **13 años** (no 16)
- Children's Code aplica a servicios online dirigidos a menores de 18
- [ ] Si el servicio capta menores de 18: ¿cumple los 15 estándares del Children's Code?
  Estándares clave verificables externamente:
  - Privacidad por defecto: configuración más privada activada por defecto
  - No geolocalización activada por defecto
  - No nudge techniques para debilitar privacidad
  - No compartir datos de menores con terceros para marketing

**DPIA (Data Protection Impact Assessment — equivalente a EIPD):**
Mismos criterios de obligatoriedad que el RGPD (Art. 35 UK GDPR).
ICO ha publicado su propio screening template para DPIA.

### Bloque 8 — Transferencias internacionales (Art. 44–49 UK GDPR)
Peso: 10 pts

**El Reino Unido tiene su propia lista de decisiones de adecuación**, independiente
de la lista de la Comisión Europea. La ICO la mantiene en ico.org.uk.

**Países con adecuación UK (lista ICO — verificar actualización):**
Argentina · Canada · Faroe Islands · Guernsey · Israel · Isle of Man · Japan ·
Jersey · New Zealand · Republic of Korea · Switzerland · Uruguay ·
EEA countries (todos los estados miembro de la UE + Noruega + Islandia + Liechtenstein) ·
**EE.UU.**: UK-US Data Bridge en vigor desde el 12/10/2023 (organizaciones certificadas
en el marco del DPF de EE.UU. con extensión UK; verificar registro en la lista del DOC)

Nota: los flujos UK → UE son libres por la lista de adecuación británica, y los flujos
UE → UK por la decisión de adecuación de la Comisión Europea, renovada el 19/12/2025
hasta el 27/12/2031. Desde el 05/02/2026 la DUAA cambió el criterio británico para
nuevas adecuaciones ("data protection test"); las existentes siguen valiendo.

**Garantías válidas cuando no hay adecuación UK:**
- Cláusulas de transferencia internacional (IDTA — International Data Transfer Agreement,
  versión UK aprobada por ICO, diferente de las CCT europeas)
- Addendum al UK de las CCT europeas (aprobado por ICO como alternativa a la IDTA)
- Normas Corporativas Vinculantes (BCR) aprobadas por ICO

Verificar:
- [ ] La política declara si se realizan transferencias fuera del UK y EEE
- [ ] Se identifican los países de destino
- [ ] Se indica la garantía adoptada (adecuación UK, UK-US Data Bridge, IDTA, addendum)
- [ ] Si hay trackers de EE.UU.: ¿la política menciona el UK-US Data Bridge o IDTA?

### Bloque 9 — Seguridad técnica (Art. 32 UK GDPR)
Peso: 5 pts

Mismos ítems del skill `rgpd` Bloque 9. Añadir:
- [ ] La política menciona la obligación de notificar brechas a la **ICO** en 72 horas
- [ ] Si sector financiero/salud: CSP y X-Frame-Options verificados

### Bloque 10 — Data Protection Officer / DPO (Art. 37–39 UK GDPR)
Peso: 5 pts

Los criterios de obligatoriedad son idénticos al RGPD (Art. 37.1 UK GDPR):
(a) autoridad pública, (b) monitorización sistemática a gran escala,
(c) tratamiento a gran escala de categorías especiales.

La ICO recomienda que cualquier organización que no esté obligada evalúe
igualmente la designación voluntaria de un DPO.

- [ ] La política indica si existe o no un DPO designado
- [ ] Si existe: nombre o rol y dirección de contacto publicados (Art. 37.7)
- [ ] Si no existe y es PYME fuera de Art. 37.1: indicar "no obligatorio" y asignar pts

---

## Paso 4 — Score global

Mismo sistema de puntuación que `rgpd` (suma de bloques / 100).

| Rango | Interpretación |
|-------|---------------|
| 80–100 | Postura defensible — cumplimiento sustancial |
| 60–79 | Riesgo moderado |
| 40–59 | Riesgo alto |
| 0–39 | Riesgo crítico |

---

## Paso 5 — Clasificación de issues y sanciones (Art. 83 UK GDPR)

El UK GDPR mantiene la estructura de dos niveles de sanción del RGPD, en GBP:

| Nivel | Multa máxima | Artículos típicos |
|-------|-------------|-------------------|
| **Superior** | £17.500.000 o 4% facturación mundial anual | Art. 5, 6, 7, 9, 12–22D, 44–49 |
| **Estándar** | £8.700.000 o 2% facturación mundial anual | Art. 8, 25, 32, 33–34, 37–39 |

La ICO aplica el mayor de los dos valores. Considera atenuantes y agravantes
similares a los del RGPD (Art. 83.2 UK GDPR). Importes de la DPA 2018, sección 157.

**Cookies y marketing se multan por las PECR, no por el Art. 83.** Para conductas desde
el 05/02/2026 la multa PECR llega a **£17.500.000 o el 4 % de la facturación mundial
anual**, lo que sea mayor, y ya no exige "daño sustancial" (sección 115 de la DUAA).
Antes de esa fecha el tope era £500.000.

**Issues críticos** (riesgo nivel superior):
- Política de privacidad inexistente
- Cookies no esenciales activas sin consentimiento ni excepción del Anexo A1 (PECR Reg. 6; multa PECR hasta £17.500.000 o 4 %)
- Sin base jurídica declarada
- Datos de categorías especiales sin consentimiento explícito
- Sin HTTPS
- Responsable fuera de UK sin representante designado (Art. 27)
- DPO obligatorio no designado

**Issues medios** (riesgo nivel superior o estándar):
- Base jurídica por finalidad incompleta
- Derechos sin canal ni plazo de respuesta
- Transferencias fuera de UK/EEE no declaradas
- Banner de cookies solo informativo
- Marketing directo sin mecanismo de baja (PECR)
- Servicios con menores de 18 sin aplicar Children's Code

**Issues bajos:**
- Falta fecha de actualización en política
- DPO no mencionado donde no es obligatorio
- Headers de seguridad recomendados ausentes

---

## Paso 6 — Output según modo

### Modo interno (Markdown)

```markdown
# Auditoría UK GDPR — [dominio]
Fecha: [fecha] | Sector: [sector] | Score: [X/100]

## Stack tecnológico
[usar resultados del Paso 0 compartido si viene del orquestador]

## Resumen
[postura general, issues críticos, riesgo sancionador estimado en GBP]

## Tabla de cumplimiento
| Bloque | Peso | Pts | Estado | Evidencia |
...

## Issues críticos / medios / bajos
...

## Notas metodológicas
- Verificado externamente
- Pendiente de acceso al backend
- Marco aplicado: UK GDPR y PECR tal como quedaron tras la DUAA 2025 (05/02/2026)
```

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_uk-gdpr_[fecha].md`.

### Modo cliente (`--docx`)

Misma estructura que el skill `rgpd` modo `--docx`, adaptada a UK:
- Autoridad de control: ICO
- Multas en GBP
- Referencias a PECR, Children's Code e IDTA en lugar de ePrivacy/CCT

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_uk-gdpr_[fecha].docx`.

---

## Notas de alcance

Mismas limitaciones que el skill `rgpd`: solo se audita lo visible externamente.
Adicional UK: el registro en la ICO no es auditable externamente.

## Actualización normativa

- **UK GDPR**: en vigor desde el 1 de enero de 2021 (post-Brexit).
- **Children's Code**: en vigor desde septiembre 2021.
- **UK-US Data Bridge**: en vigor desde el 12/10/2023.
- **IDTA**: aprobada por ICO en marzo 2022; addendum a CCT europeas aprobado en marzo 2022.
- **Data (Use and Access) Act 2025**: sanción real 19/06/2025; grueso de la Parte 5 desde
  el 05/02/2026; reclamaciones desde el 19/06/2026; Information Commission desde el
  30/09/2026.
- **Guía final de la ICO sobre tecnologías de almacenamiento y acceso:** 29/04/2026.
- **Adecuación UE → UK:** renovada el 19/12/2025, vigente hasta el 27/12/2031.
- **Versión de esta skill:** 1.1.0 (2026-11-20). Revisada contra legislation.gov.uk y la
  Comisión Europea el 20/11/2026.
