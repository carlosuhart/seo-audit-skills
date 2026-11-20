---
name: ley-25326
description: >
  Auditoría Ley 25.326 (Argentina): detecta el sector y entrega informe con score,
  estado por artículo, issues priorizados y sanciones. Sub-skill de /privacidad, también
  invocable sola.
user-invokable: true
argument-hint: "<url> [--docx]"
license: MIT
metadata:
  author: Zythos Media
  version: "1.1.0"
  category: legal-compliance
  revisar: "2027-05-20"
---

# Ley 25.326 — Auditoría de Cumplimiento (Argentina)

## Uso

```
/ley-25326 https://ejemplo.com.ar
/ley-25326 https://ejemplo.com.ar --docx
```

Sin `--docx` el output es Markdown interno. Con `--docx` genera informe
ejecutivo en formato Word.

---

## Marco normativo

- **Ley 25.326**: Ley de Protección de Datos Personales. Sancionada en 2000,
  reglamentada por Decreto 1558/2001.
- **AAIP** (Agencia de Acceso a la Información Pública): autoridad de control desde 2017.
  Absorbió las funciones de la ex-DNPDP (Dirección Nacional de Protección de Datos
  Personales). Web: argentina.gob.ar/aaip
- **Habeas data**: derecho constitucional garantizado por el Art. 43 de la
  Constitución Nacional. Toda persona puede interponer acción de habeas data para
  conocer, actualizar o suprimir datos en registros públicos o privados.
- **Decisión de adecuación UE**: Argentina tiene decisión de adecuación de la
  Comisión Europea desde 2003, confirmada en la revisión de enero de 2024 (flujo
  UE → Argentina permitido sin garantías adicionales).
- **Convenio 108 del Consejo de Europa**: Argentina es parte desde el 01/06/2019
  (Ley 27.483). El Protocolo que lo moderniza (Convenio 108+) fue aprobado por la
  Ley 27.699 (BO 30/11/2022).
- **Régimen sancionatorio vigente**: Resolución AAIP 126/2024 (BO 24/05/2024, vigente
  desde el 01/06/2024; ver Paso 5).

⚠️ **Estado de la reforma (verificado el 20/11/2026):** no hay ley nueva. La Ley 25.326
sigue vigente; hay proyectos en la Cámara de Diputados sin avance comprobado. Revisar
argentina.gob.ar/aaip y el Boletín Oficial antes de un informe de cliente: si se
sanciona una ley nueva, referenciar ese texto y ajustar los artículos.

---

## Nota sobre la autoridad de control

**Agencia de Acceso a la Información Pública (AAIP)**
Web: argentina.gob.ar/aaip
Registro de bases de datos: argentina.gob.ar/aaip/datospersonales/bases

---

## Crédito de herramienta

Al iniciar cualquier auditoría, emitir esta línea antes del output principal:

> Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search

---

## Paso 0 — Identificación del stack tecnológico

Si este skill es invocado desde el orquestador `/privacidad`, usar el Paso 0
compartido. Si se invoca directamente, ejecutar el Paso 0 del skill `rgpd`.

Señales adicionales específicas de Argentina a detectar:
- CUIT / CUIL en el pie de página o política
- Integración con Mercado Pago, Mercado Libre, MODO, Naranja X
- Referencias a AFIP, ANSES, RENAPER, IGJ
- Precios en ARS ($) o mención de IVA argentino

---

## Paso 1 — Recopilación de datos del sitio

Igual al skill `rgpd` Paso 1. Rutas comunes en Argentina:
`/privacidad`, `/politica-de-privacidad`, `/proteccion-de-datos`,
`/aviso-legal`, `/terminos-y-condiciones`.

---

## Paso 2 — Detección de sector

Usar la matriz del skill `rgpd` más señales adicionales argentinas:

| Sector | Señales Argentina |
|--------|-------------------|
| **Financiero** | BCRA, CNV, "entidad financiera", "banco", "fintech regulada" |
| **Salud** | ANMAT, PAMI, "obra social", "prepaga", "clínica" |
| **Ecommerce** | Mercado Libre, CABA consumer protection, "garantía legal" |
| **Medios** | ENACOM, "medio de comunicación", "portal de noticias" |

---

## Paso 3 — Auditoría por bloques

Evaluar cada bloque: **Cumple / Parcial / No cumple / No evaluable**

### Bloque 1 — Identificación del responsable (Art. 3 + Art. 5 + Art. 11)
Peso: 10 pts

Verificar en la política de privacidad:
- [ ] Nombre o razón social del responsable del archivo o banco de datos
- [ ] CUIT o número de persona jurídica (no obligatorio por ley pero estándar en Argentina)
- [ ] Domicilio del responsable (Art. 6 b)
- [ ] Dirección de correo electrónico o canal de contacto directo para ejercicio de derechos

**Entidad extranjera:**
La Ley 25.326 no exige en general un representante con domicilio en Argentina. Si el
responsable no tiene domicilio en el país pero trata datos de titulares argentinos:
- [ ] ¿Hay un canal de contacto operativo para que los titulares ejerzan sus derechos?
- [ ] (Buena práctica, no obligación legal) ¿Identifica un representante local?

### Bloque 2 — Política de privacidad: existencia y acceso
Peso: 5 pts

La Ley 25.326 exige informar al titular sobre el tratamiento (Art. 6).
Aunque no prescribe una "política de privacidad" con ese nombre, es el instrumento
habitual para cumplir con el deber de información:
- [ ] Existe política de privacidad o aviso de privacidad publicado
- [ ] Enlace visible en el footer de todas las páginas
- [ ] Enlace accesible desde formularios que recogen datos
- [ ] Redactada en castellano con lenguaje claro
- [ ] Fecha de última actualización visible

### Bloque 3 — Política de privacidad: contenido mínimo (Art. 6 + Art. 11)
Peso: 15 pts

Verificar que la política incluya (1 pt por ítem):
- [ ] **Art. 6 a):** Finalidad del tratamiento y quiénes pueden ser sus destinatarios
- [ ] **Art. 6 b):** Existencia del archivo o banco de datos, e identidad y domicilio de su responsable
- [ ] **Art. 6 c):** Carácter obligatorio o facultativo de las respuestas
- [ ] **Art. 6 d):** Consecuencias de proporcionar los datos, de negarse o de su inexactitud
- [ ] **Art. 6 e):** Posibilidad de ejercer los derechos de acceso, rectificación y supresión
- [ ] **Leyenda de la AAIP (Res. AAIP 14/2018, art. 3):** "La Agencia de Acceso a la
      Información Pública, en su carácter de Órgano de Control de la Ley N° 25.326, tiene la
      atribución de atender las denuncias y reclamos que interpongan quienes resulten
      afectados en sus derechos por incumplimiento de las normas vigentes en materia de
      protección de datos personales." La resolución apunta a bancos destinados a dar
      informes, pero en la práctica se usa en cualquier política: su ausencia es issue bajo
- [ ] Tipos de datos que se recogen
- [ ] Destinatarios o categorías de destinatarios (terceros, cesionarios)
- [ ] Plazos de conservación o criterios para determinarlos
- [ ] Transferencias internacionales (si aplica) — Art. 12
- [ ] Uso de cookies y tecnologías de rastreo
- [ ] Derecho de habeas data (Art. 43 CN) — mención como derecho constitucional
- [ ] Derecho a reclamar ante la AAIP
- [ ] Procedimiento para ejercer derechos y plazos de respuesta (acceso: 10 días corridos, art. 14.2; rectificación, actualización o supresión: 5 días hábiles, art. 16.2)
- [ ] Datos sensibles tratados (si aplica — Art. 7)

### Bloque 4 — Consentimiento y base jurídica (Art. 5 + Art. 6)
Peso: 10 pts

La Ley 25.326 centra el tratamiento lícito principalmente en el **consentimiento**
(Art. 5), con excepciones tasadas. Es menos granular que el RGPD en cuanto a
bases jurídicas alternativas:

**Excepciones al consentimiento (Art. 5.2):**
No se requiere consentimiento cuando los datos:
- **a)** Se obtienen de fuentes de acceso público irrestricto
- **b)** Se recaban para el ejercicio de funciones propias de los poderes del Estado o
  en virtud de una obligación legal
- **c)** Son listados limitados a nombre, DNI, identificación tributaria o previsional,
  ocupación, fecha de nacimiento y domicilio
- **d)** Derivan de una relación contractual, científica o profesional del titular y son
  necesarios para su desarrollo o cumplimiento
- **e)** Se refieren a operaciones de entidades financieras con sus clientes (Ley 21.526)

Verificar:
- [ ] Cuando la base es el consentimiento: el checkbox no está pre-marcado
- [ ] El consentimiento es libre, expreso e informado (Art. 5.1)
- [ ] Cuando se invocan excepciones al consentimiento: se identifica cuál
- [ ] Para datos sensibles: nadie está obligado a proporcionarlos (Art. 7.1). Solo pueden
      recolectarse y tratarse por razones de interés general autorizadas por ley, o con
      fines estadísticos o científicos cuando no se identifique al titular (Art. 7.2). Está
      prohibido formar bancos de datos que revelen directa o indirectamente datos
      sensibles (Art. 7.3)
- [ ] Formularios solicitan solo los datos necesarios para la finalidad declarada

**Privacidad desde el diseño (no en la ley, buena práctica):**
- [ ] Los formularios no solicitan datos excesivos para la finalidad declarada

### Bloque 5 — Cookies y marketing directo (Art. 5 + recomendaciones AAIP)
Peso: 15 pts

La Ley 25.326 no regula cookies específicamente. Los requisitos derivan del
principio general de consentimiento informado (Art. 5) y de las recomendaciones
de la AAIP. La AAIP ha indicado que las cookies de rastreo no esenciales
requieren consentimiento previo e informado del titular.

**Banner de cookies:**
- [ ] Existe banner o mecanismo de consentimiento de cookies
- [ ] El banner bloquea cookies no esenciales hasta obtener consentimiento activo
- [ ] No hay cookies de análisis, publicidad o rastreo activas antes del consentimiento
- [ ] Opción de rechazo accesible
- [ ] Enlace a política de cookies o privacidad en el propio banner

**Formularios:**
- [ ] Checkbox de consentimiento no pre-marcado para tratamientos no esenciales
- [ ] El checkbox vincula a la política de privacidad
- [ ] Finalidad concreta declarada antes de enviar

**Marketing directo (Art. 27):**
- [ ] Si hay newsletter o comunicaciones comerciales: existe mecanismo de baja claro
- [ ] La política menciona el derecho del titular a pedir el retiro o bloqueo de sus datos
      de los bancos usados para publicidad (Art. 27.3)
- [ ] El opt-out es tan accesible como el opt-in
- [ ] Si se usan datos de fuentes públicas para marketing directo: se informa al
      titular en el primer contacto (Art. 27.3)

**Menores de edad:**
La Ley 25.326 no regula específicamente el consentimiento de menores — aplican
las normas generales del Código Civil y Comercial argentino (Ley 26.994).
Menores de 13 años: requieren representación de padres o tutores.
Menores de 13-18 años: capacidad progresiva según el acto.
- [ ] Si el sitio capta menores: ¿existe verificación de edad o consentimiento parental?

### Bloque 6 — Derechos del titular: canal habilitado (Art. 14–16 + Art. 27)
Peso: 15 pts

La Ley 25.326 reconoce estos derechos, con plazos distintos para cada uno:

1. **Acceso** (Art. 14): conocer los datos sobre sí mismo en cualquier banco de datos.
   Respuesta en **10 días corridos** desde la intimación (Art. 14.2). Es gratuito a
   intervalos no inferiores a seis meses, salvo interés legítimo (Art. 14.3)
2. **Rectificación y actualización** (Art. 16): corrección de datos inexactos o
   incompletos, en **5 días hábiles** (Art. 16.2)
3. **Supresión** (Art. 16): eliminación de datos cuyo tratamiento no cumpla la ley,
   también en **5 días hábiles** (Art. 16.2)
4. **Retiro o bloqueo para publicidad** (Art. 27.3): pedir que se retiren o bloqueen sus
   datos de los bancos usados con fines publicitarios
(El Art. 34 regula la legitimación para la acción judicial de habeas data, no un derecho
de oposición.)

Nota: la Ley 25.326 no reconoce explícitamente derechos de portabilidad, limitación
ni de no ser objeto de decisiones automatizadas (a diferencia del RGPD). Si existe
reforma legislativa en vigor, verificar si estos derechos fueron incorporados.

Verificar:
- [ ] Existe mecanismo explícito para ejercer derechos (email, formulario, dirección)
- [ ] Se mencionan los plazos de respuesta (acceso 10 días corridos; rectificación y
      supresión 5 días hábiles). Un plazo de "30 días" es un error frecuente: es issue medio
- [ ] Se mencionan los derechos de acceso, rectificación, actualización, supresión y el
      retiro o bloqueo para publicidad
- [ ] Se indica qué información debe adjuntar el titular (identificación)
- [ ] Se menciona el derecho de habeas data (Art. 43 CN) y la posibilidad de recurrir
      a la justicia o reclamar ante la AAIP si la solicitud no es atendida

### Bloque 7 — Datos sensibles (Art. 7 + Art. 8)
Peso: 10 pts

La Ley 25.326 define como datos sensibles (Art. 2) los que revelan:
- Origen racial y étnico
- Opiniones políticas
- Convicciones religiosas, filosóficas o morales
- Afiliación sindical
- Información referente a la salud o a la vida sexual

Los datos biométricos y genéticos no están explícitamente en la lista (a diferencia
del RGPD). La AAIP puede haber ampliado la interpretación vía resoluciones — verificar.

**Principio general (Art. 7.1):** Está prohibido crear bases de datos sensibles,
salvo las excepciones del propio artículo.

**Si el sitio no recoge datos sensibles:** bloque N/A, asignar 10 pts.

**Si recoge datos sensibles:**
- [ ] Identificados explícitamente en la política
- [ ] Consentimiento expreso del titular (Art. 7.1 — sin excepciones comerciales)
- [ ] Finalidad específica declarada para esos datos
- [ ] Medidas de seguridad reforzadas mencionadas

**Datos de salud (Art. 8):**
- [ ] Los establecimientos sanitarios y los profesionales de la salud pueden tratar los
      datos de salud de sus pacientes, respetando el secreto profesional (el Art. 8
      habilita a esos sujetos; no prohíbe a otros con base legal)
- [ ] Si el sitio es de salud: ¿la política lo menciona?

### Bloque 8 — Transferencias internacionales (Art. 12)
Peso: 10 pts

La Ley 25.326 prohíbe la transferencia de datos personales a países u organismos
internacionales o supranacionales que no proporcionen niveles de protección adecuados
(Art. 12.1). La AAIP mantiene el listado de países con nivel adecuado.

**Excepciones de la propia ley (Art. 12.2):** colaboración judicial internacional;
intercambio de datos médicos por tratamiento del afectado o por investigación
epidemiológica; transferencias bancarias o bursátiles; transferencias acordadas en
tratados internacionales; y cooperación entre organismos de inteligencia contra el crimen
organizado, el terrorismo y el narcotráfico.

**Vías habituales para un sitio comercial** (fuera del Art. 12.2):
- País con nivel adecuado según la lista de la autoridad (Disposición DNPDP 60-E/2016)
- Consentimiento expreso del titular para la transferencia (Decreto 1558/2001, art. 12)
- Cláusulas contractuales modelo: las de la Disposición 60-E/2016 y las de la Red
  Iberoamericana de Protección de Datos, aprobadas por la Resolución AAIP 198/2023
  (BO 18/10/2023); las dos siguen vigentes

Verificar:
- [ ] La política declara si se realizan transferencias internacionales
- [ ] Se identifican los países de destino
- [ ] Se indica la base o garantía adoptada (país con adecuación, consentimiento, excepción)
- [ ] Si hay trackers de EE.UU. activos (Google, Meta, etc.): ¿la política lo declara?
      Nota: EE.UU. no tiene decisión de adecuación argentina genérica — verificar
      si el responsable ha adoptado garantías contractuales o si la AAIP ha publicado
      alguna habilitación específica

### Bloque 9 — Seguridad técnica (Art. 9)
Peso: 5 pts

La Ley 25.326 obliga al responsable a adoptar medidas técnicas y organizativas
necesarias para garantizar la seguridad y confidencialidad de los datos, impidiendo
adulteración, pérdida, consulta o tratamiento no autorizado (Art. 9.1).

Verificar lo observable externamente:
- [ ] HTTPS activo en todas las páginas
- [ ] Certificado SSL/TLS válido y no expirado
- [ ] HSTS habilitado
- [ ] No hay redirección HTTP → HTTPS rota
- [ ] La política menciona medidas de seguridad adoptadas
- [ ] La política menciona el deber de confidencialidad (Art. 10)

**Violación de datos:**
La Ley 25.326 no establece una obligación expresa de notificación de brechas
comparable al RGPD. La AAIP puede requerir información ante incidentes. Verificar
si existe resolución de la AAIP sobre notificación de incidentes.
- [ ] Si existe regulación AAIP sobre brechas: ¿la política la menciona?

### Bloque 10 — Registro de bases de datos ante la AAIP (Art. 21–24)
Peso: 5 pts

La Ley 25.326 exige la inscripción de los archivos, registros, bases o bancos de
datos ante el Registro Nacional de Bases de Datos de la AAIP (Art. 21.1).
Los responsables de bases de datos privadas con datos de personas físicas deben
registrarse antes de iniciar el tratamiento.

No existe en el RGPD ni en la LGPD; en la región, Uruguay también exige registro
(Ley 18.331).
No es auditable externamente, pero su cumplimiento es verificable consultando
el registro público de la AAIP.

- [ ] La política menciona el número de inscripción en el Registro Nacional de
      Bases de Datos de la AAIP, o indica que la base está registrada
- [ ] Si el sitio recoge datos de personas físicas argentinas y no menciona
      el registro: registrar como issue medio (obligación legal activa)

Nota: Las personas jurídicas públicas y ciertos registros específicos tienen
régimen diferente. Verificar la categoría del responsable.

---

## Paso 4 — Score global

```
Score = suma de puntos obtenidos / 100
```

| Rango | Interpretación |
|-------|---------------|
| 80–100 | Postura defensible |
| 60–79 | Riesgo moderado |
| 40–59 | Riesgo alto |
| 0–39 | Riesgo crítico |

---

## Paso 5 — Clasificación de issues y sanciones (Art. 31 + Art. 32)

La Ley 25.326 (Art. 31) prevé apercibimiento, suspensión, multa de ARS 1.000 a
ARS 100.000, y clausura o cancelación del archivo o banco de datos. La graduación vigente
es la de la **Resolución AAIP 126/2024** (BO 24/05/2024, vigente desde el 01/06/2024),
que derogó la Disposición 7/2005 y las Resoluciones 240/2022 y 244/2022:

| Gravedad | Sanciones |
|---|---|
| **Leve** | Hasta 2 apercibimientos y/o multa de ARS 1.000 a ARS 80.000 |
| **Grave** | Hasta 4 apercibimientos, suspensión de 1 a 30 días y/o multa de ARS 80.001 a ARS 90.000 |
| **Muy grave** | Hasta 6 apercibimientos, suspensión de 31 a 365 días, clausura o cancelación y/o multa de ARS 90.001 a ARS 100.000 |

Si una misma conducta genera varias multas, el total tiene un tope de 500 veces el máximo
de la escala. El pago voluntario dentro de 20 días hábiles reduce la multa al 50 %. Los
montos no se indexan: el peso real de una sanción está en la suspensión, la clausura y el
daño reputacional, no en la multa.

**Adicionalmente:** El titular puede interponer acción de habeas data ante la
Justicia Federal o Nacional (Art. 43 CN) de forma directa, independientemente
de la vía administrativa ante la AAIP.

**Críticos** (incumplimiento directo de la ley):
- Sin información mínima al titular sobre el tratamiento → Art. 6
- Datos sensibles tratados sin consentimiento expreso → Art. 7
- Sin mecanismo de ejercicio de derechos → Art. 14-16
- Transferencia internacional a país sin nivel adecuado sin garantías → Art. 12
- Sin HTTPS → Art. 9 (seguridad)

**Medios** (gap relevante):
- Política existe pero falta información mínima del Art. 6
- Base jurídica no declarada por finalidad
- Derechos mencionados sin canal ni plazo (acceso 10 días corridos; rectificación y supresión 5 días hábiles)
- Transferencias internacionales no declaradas
- Base de datos no registrada ante la AAIP → Art. 21

**Bajos:**
- Falta fecha de actualización en la política
- Política sin enlace desde formularios secundarios
- Plazos de retención no especificados

---

## Paso 6 — Output según modo

### Modo interno (Markdown)

```markdown
# Auditoría Ley 25.326 — [dominio]
Fecha: [fecha] | Sector: [sector] | Score: [X/100]

## Stack tecnológico
[usar Paso 0 compartido si viene del orquestador]

## Resumen
[postura general, issues críticos, riesgo sancionador]

## Tabla de cumplimiento
| Bloque | Peso | Pts | Estado | Evidencia |
...

## Issues críticos / medios / bajos
...

## Notas metodológicas
- Verificado externamente
- Registro AAIP no verificable externamente
- ⚠️ Verificar si existe reforma legislativa en vigor a la fecha de uso
```

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_ley25326_[fecha].md`.

### Modo cliente (`--docx`)

Misma estructura que `rgpd` modo `--docx`, adaptada:
- Autoridad: AAIP
- Sanciones en ARS (verificar valores vigentes)
- Referencia al habeas data constitucional
- Pie de página: hipervínculo "Zythos Media" → https://zythos.media

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_ley25326_[fecha].docx`.

---

## Notas de alcance

Mismas limitaciones que el skill `rgpd`. Adicional:
- El registro ante la AAIP (Bloque 10) no es auditable externamente
- El historial de sanciones de la AAIP es público pero requiere consulta directa

## Actualización normativa

- **Ley 25.326**: sancionada en 2000, Decreto reglamentario 1558/2001.
- **AAIP**: autoridad de control desde 2017.
- **Reforma legislativa**: sin ley nueva al 20/11/2026; proyectos en Diputados sin avance
  comprobado. Verificar en argentina.gob.ar/aaip y el Boletín Oficial antes de usar.
- **Sanciones**: Resolución AAIP 126/2024, vigente desde el 01/06/2024.
- **Transferencias**: Disposición 60-E/2016 y Resolución AAIP 198/2023 (cláusulas modelo).
- **Convenio 108**: parte desde el 01/06/2019; Convenio 108+ aprobado por Ley 27.699 (2022).
- **Habeas data**: Art. 43 CN — derecho constitucional independiente de la ley ordinaria.
- **Versión de esta skill:** 1.1.0 (2026-11-20). Plazos de los arts. 14 y 16, art. 6,
  excepciones de los arts. 5.2, 7.2 y 12.2 y régimen sancionatorio corregidos contra
  InfoLEG y la AAIP.
