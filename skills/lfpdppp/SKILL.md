---
name: lfpdppp
description: >
  Auditoría LFPDPPP y su Reglamento (México): detecta el sector y entrega informe con
  score, estado por artículo, issues priorizados y sanciones. Sub-skill de /privacidad,
  también invocable sola.
user-invokable: true
argument-hint: "<url> [--docx]"
license: MIT
metadata:
  author: Zythos Media
  version: "2.0.0"
  category: legal-compliance
  revisar: "2027-03-20"
---

# LFPDPPP — Auditoría de Cumplimiento (México)

## Uso

```
/lfpdppp https://ejemplo.com.mx
/lfpdppp https://ejemplo.com.mx --docx
```

Sin `--docx` el output es Markdown interno. Con `--docx` genera informe
ejecutivo en formato Word.

---

## Marco normativo

- **LFPDPPP (nueva)**: Ley Federal de Protección de Datos Personales en Posesión de los
  Particulares publicada en el DOF el **20/03/2025**, en vigor desde el **21/03/2025**.
  **Abroga la ley de 2010** (artículo segundo transitorio). Todos los artículos de esta
  skill corresponden a la ley de 2025. Solo aplica a **particulares** (personas físicas y
  morales del sector privado); el sector público se rige por la ley general de sujetos
  obligados, fuera del scope de esta skill.
- **Autoridad**: **Secretaría Anticorrupción y Buen Gobierno** (Art. 2.XV). El INAI se
  extinguió con la reforma de 2025: no citarlo como autoridad vigente.
- **Reglamento**: el del 21/12/2011 sigue citado por la ley (Art. 2.XIII) y se aplica solo
  en lo que no la contradiga. Al 20/11/2026 no se encontró un reglamento nuevo: revisar
  el DOF antes de un informe de cliente.
- **Lineamientos del Aviso de Privacidad** (DOF 17/01/2013): referencia práctica en lo que
  no contradigan la ley nueva.
- Fuente del texto: DOF 20/03/2025 (copia íntegra consultada en
  https://www.inah.gob.mx/images/transparencia/20_03_2025_Decreto_inai.pdf).

---

## Nota sobre el aviso de privacidad

En México, el documento de cumplimiento principal se denomina **aviso de privacidad**
(no "política de privacidad"). Existen tres tipos según el Reglamento y los Lineamientos:

| Tipo | Cuándo usar | Contenido |
|------|-------------|-----------|
| **Integral** | Recabación directa, suficiente espacio | Todos los elementos del Art. 15 |
| **Simplificado** | Recabación en formularios, espacio reducido | Fracciones I a IV del Art. 15 y dónde consultar el integral (Art. 16.II) |
| **Corto / de capa** | Pantallas pequeñas, QR, voz | Datos de contacto + enlace al integral |

El aviso simplificado y el corto siempre deben enlazar al aviso integral completo.

---

## Nota sobre la autoridad de control

**Secretaría Anticorrupción y Buen Gobierno** (Art. 2.XV de la LFPDPPP de 2025).
Recibe el procedimiento de protección de derechos (Art. 40), que el titular puede iniciar
dentro de los 15 días siguientes a la respuesta del responsable o al vencimiento del plazo
para darla. El INAI ya no existe: un aviso que lo cite como autoridad está desactualizado
(issue bajo, no crítico).

---

## Crédito de herramienta

Al iniciar cualquier auditoría, emitir esta línea antes del output principal:

> Desarrollado por [Zythos Media](https://zythos.media) — Especialistas en SEO & IA Search

---

## Paso 0 — Identificación del stack tecnológico

Si este skill es invocado desde el orquestador `/privacidad`, usar el Paso 0
compartido. Si se invoca directamente, ejecutar el Paso 0 del skill `rgpd`.

Señales adicionales específicas de México a detectar:
- RFC en el pie de página o aviso de privacidad
- Integración con SPEI, CoDi, CONEKTA, OpenPay, Clip
- Referencias al SAT, IMSS, CONDUSEF, PROFECO, COFEPRIS
- Precios en MXN ($) con indicación de IVA (16%)
- Plataformas de e-learning mexicanas: Domestika MX, Crehana MX

---

## Paso 1 — Recopilación de datos del sitio

Igual al skill `rgpd` Paso 1. Rutas comunes en México:
`/aviso-de-privacidad`, `/privacidad`, `/aviso-privacidad`,
`/politica-de-privacidad`, `/terminos-y-condiciones`.

Verificar también el footer para "Aviso de Privacidad" como enlace estándar.

---

## Paso 2 — Detección de sector

Usar la matriz del skill `rgpd` más señales adicionales mexicanas:

| Sector | Señales México |
|--------|---------------|
| **Financiero** | CNBV, SOFOM, "institución financiera", CONDUSEF |
| **Salud** | COFEPRIS, SSA, IMSS, ISSSTE, "medicamento", "hospital" |
| **Telecomunicaciones** | IFT, "concesionaria", "servicio de internet" |
| **Educación** | SEP, "bachillerato", "licenciatura", RVOE |
| **Ecommerce** | PROFECO, "garantía del consumidor", facturación electrónica SAT |

---

## Paso 3 — Auditoría por bloques

Evaluar cada bloque: **Cumple / Parcial / No cumple / No evaluable**

### Bloque 1 — Identificación del responsable (Art. 15.I)
Peso: 10 pts

Verificar en el aviso de privacidad:
- [ ] Nombre o denominación social del responsable (Art. 15.I)
- [ ] Domicilio del responsable (Art. 15.I)
- [ ] RFC (no obligatorio expresamente por la LFPDPPP pero estándar en México)
- [ ] Dirección de correo electrónico o canal de contacto para ejercicio de derechos ARCO

**Responsable extranjero:**
Si el responsable no tiene establecimiento en México pero trata datos de titulares en
México:
- [ ] ¿El aviso indica un domicilio o medio para recibir solicitudes ARCO?

**Persona o departamento de datos personales (Art. 29 — OBLIGATORIO):**
La ley de 2025 obliga a todo responsable a designar una persona o departamento de datos
personales que tramite las solicitudes ARCO y fomente la protección de datos en la
organización:
- [ ] ¿El aviso identifica a la persona o departamento de datos personales y su contacto?
      Si no aparece: issue medio

### Bloque 2 — Aviso de privacidad: existencia y acceso (Arts. 14-16)
Peso: 5 pts

El aviso de privacidad es **obligatorio** antes o en el momento de recabar datos:
- [ ] Existe aviso de privacidad publicado (integral o simplificado con enlace al integral)
- [ ] Enlace visible en el footer de todas las páginas
- [ ] Enlace accesible desde formularios que recogen datos personales
- [ ] Redactado en español con lenguaje claro (Art. 8 Reglamento)
- [ ] Fecha de última actualización visible
- [ ] Si es aviso simplificado: enlace al aviso integral completo

### Bloque 3 — Aviso de privacidad: contenido mínimo (Art. 15 + Lineamientos)
Peso: 15 pts

El Art. 15 de la ley de 2025 fija el contenido del aviso integral (1 pt por ítem):

- [ ] **Art. 15.I:** Identidad y domicilio del responsable
- [ ] **Art. 15.II:** Datos personales que se tratan, **identificando los sensibles**
- [ ] **Art. 15.III:** Finalidades del tratamiento, **distinguiendo las que requieren
      consentimiento** de las que no
- [ ] **Art. 15.IV:** Opciones y medios para que el titular limite el uso o divulgación
- [ ] **Art. 15.V:** Medios para ejercer derechos ARCO
- [ ] **Art. 15.VI:** Procedimiento y medio por el cual se comunicarán los cambios al aviso
- [ ] **Transferencias (Art. 35):** a quién y para qué, con una cláusula para que el titular
      acepte o no la transferencia cuando requiera consentimiento
- [ ] Base de tratamiento: consentimiento o excepción del Art. 9
- [ ] Plazo de conservación o criterio para determinarlo
- [ ] Mecanismos de revocación del consentimiento
- [ ] Persona o departamento de datos personales (Art. 29)
- [ ] Derecho a iniciar el procedimiento de protección de derechos ante la Secretaría
      Anticorrupción y Buen Gobierno (Art. 40)
- [ ] Cambios al aviso: indicar cómo se notificarán (web, email, u otro medio)
- [ ] *(Lineamientos)* Fecha de última actualización del aviso
- [ ] *(Lineamientos)* Datos de contacto del responsable para solicitudes ARCO

### Bloque 4 — Consentimiento y base jurídica (Arts. 7, 8 y 9)
Peso: 10 pts

La LFPDPPP centra el tratamiento lícito en el **consentimiento** (Art. 7), con un catálogo
de **excepciones** (Art. 9, fracciones I a VII) más acotado que el RGPD:
- **Regla general: el consentimiento tácito es válido** (el titular no se opone tras
  conocer el aviso).
- **Consentimiento expreso** para datos financieros o patrimoniales.
- **Datos sensibles (Art. 8):** consentimiento expreso y por escrito, con firma autógrafa,
  firma electrónica o cualquier mecanismo de autenticación.

**Excepciones al consentimiento (Art. 9):**
- Esté previsto en una ley
- Los datos figuren en fuentes de acceso público
- Los datos se sometan a un procedimiento previo de disociación
- Tenga el propósito de cumplir obligaciones derivadas de una relación jurídica
  entre el titular y el responsable
- Exista una situación de emergencia que potencialmente pueda dañar a un individuo
- Sean indispensables para la atención médica, prevención o diagnóstico, prestación
  de asistencia sanitaria, o gestión de servicios de salud
- Se dicte resolución de autoridad competente

Verificar:
- [ ] Cuando la base es el consentimiento: el aviso indica cómo se otorga y revoca
- [ ] El consentimiento es libre, específico e informado (Art. 7)
- [ ] Si se recaban datos financieros o patrimoniales: consentimiento expreso
- [ ] Cuando se invocan excepciones (Art. 9): se identifica cuál aplica
- [ ] Para datos sensibles: consentimiento expreso y por escrito con firma autógrafa,
      electrónica o mecanismo de autenticación (Art. 8). Un checkbox simple no basta
- [ ] El aviso indica el procedimiento para revocar el consentimiento

**Datos sensibles sin consentimiento:** solo cuando lo exija una relación jurídica
preexistente y lo establezca expresamente una ley.

### Bloque 5 — Cookies y marketing directo (Art. 7 + Lineamientos)
Peso: 15 pts

La LFPDPPP no regula cookies específicamente. Los Lineamientos del Aviso de Privacidad
(2013) exigen que, cuando se usen cookies u otras tecnologías de rastreo, el aviso informe
sobre su uso y los medios para desactivarlas. Como la regla general es el consentimiento
tácito (Art. 7), **la ley mexicana no exige un opt-in previo para cookies**: el mínimo
legal es informar y permitir desactivarlas. Un banner con bloqueo previo es buena
práctica, no obligación.

**Cookies:**
- [ ] El aviso de privacidad describe las cookies y tecnologías de rastreo usadas
- [ ] El aviso explica cómo desactivarlas
- [ ] Existe una forma de rechazarlas u oponerse
- [ ] (Buena práctica) Banner que bloquea las cookies publicitarias hasta el consentimiento

**Formularios:**
- [ ] Checkbox de consentimiento no pre-marcado cuando la base es el consentimiento
- [ ] El checkbox vincula al aviso de privacidad
- [ ] Finalidad concreta declarada antes de enviar

**Marketing directo y publicidad:**
- [ ] Si hay newsletter o comunicaciones comerciales: existe mecanismo de baja claro
- [ ] El aviso menciona la opción de limitar el uso de datos para publicidad (Art. 15.IV)
- [ ] El opt-out es tan accesible como el opt-in

**Menores de edad:**
La ley de 2025 no regula expresamente a los menores. Se aplican las reglas de
representación del Código Civil Federal (plena capacidad a los 18 años) y del Reglamento
de 2011 en lo que no contradiga la ley:
- [ ] Si el sitio puede captar menores: ¿existe verificación de edad o consentimiento
      del padre/madre/tutor?
- [ ] Si no va dirigido a menores: declararlo en el aviso

### Bloque 6 — Derechos ARCO: canal habilitado (Arts. 22–26 + Art. 31)
Peso: 15 pts

La LFPDPPP reconoce los **4 derechos ARCO** (Arts. 22 a 26). El responsable debe
**responder en 20 días hábiles** y, si procede, **hacer efectiva la solicitud en 15 días
hábiles** más (Art. 31); ambos plazos pueden ampliarse una vez por un periodo igual,
justificándolo:

1. **Acceso**: conocer qué datos tiene el responsable y para qué
2. **Rectificación**: corregir datos inexactos o incompletos
3. **Cancelación**: supresión de datos, con un periodo de bloqueo previo (Art. 24)
4. **Oposición** (Art. 26): por causa legítima, y también **al tratamiento automatizado
   que produzca efectos sin intervención humana** (Art. 26.II)

Nota: la ley no incluye portabilidad ni limitación como derechos autónomos.

Verificar:
- [ ] Existe mecanismo explícito para ejercer derechos ARCO (email, formulario, domicilio)
- [ ] Se mencionan los plazos: 20 días hábiles de respuesta y 15 de ejecución (Art. 31)
- [ ] Se mencionan los cuatro derechos, incluida la oposición al tratamiento automatizado
- [ ] El aviso indica qué información debe adjuntar el titular en su solicitud
- [ ] Se menciona el procedimiento de protección de derechos ante la **Secretaría
      Anticorrupción y Buen Gobierno** (Art. 40), dentro de los 15 días siguientes a la respuesta
- [ ] El ejercicio de derechos es gratuito para el titular (Art. 34)

### Bloque 7 — Datos sensibles (Art. 2.VI + Art. 8)
Peso: 10 pts

La LFPDPPP define como datos sensibles (Art. 2.VI) los que afecten la esfera más íntima
del titular o cuya utilización indebida pueda dar lugar a discriminación o conlleve un
riesgo grave. La lista es **enunciativa** (no cerrada):
- Origen racial o étnico
- Estado de salud presente o futuro
- Información genética
- Creencias religiosas, filosóficas y morales
- Opiniones políticas
- Preferencia sexual

Nota: la ley de 2025 ya no menciona la afiliación sindical en la lista, pero como es
enunciativa puede seguir siendo sensible según el contexto. No incluye los datos
biométricos expresamente.

**Si el sitio no recoge datos sensibles:** bloque N/A, asignar 10 pts.

**Si recoge datos sensibles (Art. 8):**
- [ ] Se identifica expresamente en el aviso que se tratan datos sensibles
- [ ] El aviso indica la finalidad específica de esos datos
- [ ] Consentimiento expreso y por escrito (o electrónico equivalente) del titular
- [ ] No se crean bases de datos con datos sensibles sin justificación legítima
- [ ] Medidas de seguridad reforzadas para datos sensibles mencionadas

**Sector salud:**
- [ ] Datos de salud tratados solo por profesionales o establecimientos con obligación
      de confidencialidad
- [ ] Consentimiento informado específico para uso de datos clínicos

### Bloque 8 — Transferencias de datos (Arts. 35–36)
Peso: 10 pts

La LFPDPPP distingue entre:
- **Transferencia** (Art. 35): comunicación de datos a un tercero distinto del responsable
  y del encargado. Se informa en el aviso con una cláusula para que el titular la acepte
  o no, y el receptor asume las obligaciones del responsable.
- **Remisión**: comunicación al encargado del tratamiento (proveedor de servicios); no
  requiere consentimiento del titular si hay contrato.

**Excepciones al consentimiento para transferencias (Art. 36, fracciones I a VII):**
- Prevista en una ley o en un tratado del que México sea parte
- Necesaria para la prevención o el diagnóstico médico, la asistencia sanitaria o la
  gestión de servicios de salud
- **A sociedades del mismo grupo** (controladoras, subsidiarias o afiliadas) que operen
  con los mismos procesos y políticas internas
- Necesaria por un contrato celebrado o por celebrar en interés del titular
- Necesaria para salvaguardar el interés público o la procuración de justicia
- Necesaria para el reconocimiento, ejercicio o defensa de un derecho en un proceso judicial
- Necesaria para mantener o cumplir una relación jurídica con el titular

**Transferencias internacionales:** la ley no las prohíbe; aplican las mismas reglas y el
receptor asume las obligaciones del responsable. Mecanismos habituales: cláusulas
contractuales y políticas corporativas.

Verificar:
- [ ] El aviso declara las transferencias nacionales e internacionales con su cláusula de
      aceptación (Art. 35)
- [ ] Se identifican los destinatarios o categorías de destinatarios
- [ ] Se indica la finalidad de cada transferencia
- [ ] Para transferencias internacionales: se indica el mecanismo de garantía
- [ ] Si hay trackers de EE.UU. activos (Google, Meta): ¿el aviso los declara?

### Bloque 9 — Seguridad técnica y vulneraciones (Arts. 18-19)
Peso: 5 pts

La LFPDPPP obliga al responsable a implementar medidas de seguridad administrativas,
técnicas y físicas para proteger los datos contra daño, pérdida, alteración, destrucción o
uso, acceso o tratamiento no autorizado.

Verificar lo observable externamente:
- [ ] HTTPS activo en todas las páginas
- [ ] Certificado SSL/TLS válido y no expirado
- [ ] HSTS habilitado
- [ ] No hay redirección HTTP → HTTPS rota
- [ ] El aviso menciona que se adoptan medidas de seguridad

**Vulneraciones de seguridad (Art. 19):**
Cuando una vulneración afecte de forma significativa los derechos patrimoniales o morales
del titular, el responsable debe informarle **de forma inmediata** para que adopte
medidas. La ley no obliga a notificar a la Secretaría.
- [ ] Si el aviso menciona el procedimiento ante vulneraciones de seguridad:
      señalar como señal positiva

### Bloque 10 — Persona o departamento de datos personales y autorregulación (Arts. 29 y 37)
Peso: 5 pts

La designación de una persona o departamento de datos personales es **obligatoria**
para todo responsable (Art. 29): tramita las solicitudes ARCO y fomenta la protección de
datos. El Art. 37 promueve la autorregulación (esquemas, sellos, certificaciones), que
cuenta como señal de cumplimiento.

- [ ] El aviso identifica a la persona o departamento de datos personales
- [ ] Sus datos de contacto están publicados para solicitudes ARCO
- [ ] Si el responsable está adherido a un esquema de autorregulación: lo menciona
- [ ] Si no se identifica a la persona o departamento: issue medio (obligatorio, Art. 29)

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

## Paso 5 — Clasificación de issues y sanciones (Arts. 58–59 LFPDPPP)

Las infracciones están en el Art. 58 y las multas en el Art. 59, en **UMA** (Unidad de
Medida y Actualización), ya no en días de salario mínimo:

| Fracción del Art. 59 | Multa | Infracciones (Art. 58) |
|---|---|---|
| **II** | 100 a 160.000 UMA | Fracciones II a VII: por ejemplo, omitir elementos del aviso de privacidad, no atender derechos ARCO |
| **III** | 200 a 320.000 UMA | Fracciones VIII a XVIII: confidencialidad, seguridad, transferencias sin cumplir la ley, datos sensibles o financieros sin el consentimiento expreso requerido |
| **IV** | Multa adicional de 100 a 320.000 UMA | Si la infracción persiste |

Con datos sensibles, las multas pueden duplicarse. Convertir a MXN con el valor de la UMA
vigente (inegi.org.mx) al elaborar el informe. Las sanciones civiles y penales (Arts. 61 a
64) son aparte.

**Críticos:**
- Aviso de privacidad inexistente → Arts. 14-15
- Sin base jurídica declarada → Art. 7
- Datos sensibles sin consentimiento expreso y por escrito → Art. 8
- Sin mecanismo de ejercicio de derechos ARCO → Arts. 22-26
- Transferencias sin informar al titular → Art. 35
- Sin HTTPS → medidas de seguridad (Art. 18)

**Medios:**
- Aviso existe pero falta contenido mínimo del Art. 15
- Derechos ARCO mencionados sin canal ni plazo (20 días hábiles de respuesta, 15 de ejecución)
- Persona o departamento de datos personales no identificado → Art. 29
- Cookies no informadas en el aviso o sin forma de desactivarlas
- Marketing directo sin mecanismo de baja
- El aviso cita al INAI como autoridad (desactualizado desde el 21/03/2025)

**Bajos:**
- Falta fecha de actualización en el aviso
- Aviso sin enlace desde formularios secundarios
- No se menciona el procedimiento de notificación de cambios al aviso

---

## Paso 6 — Output según modo

### Modo interno (Markdown)

```markdown
# Auditoría LFPDPPP — [dominio]
Fecha: [fecha] | Sector: [sector] | Score: [X/100]

## Stack tecnológico
[usar Paso 0 compartido si viene del orquestador]

## Resumen
[postura general, issues críticos, riesgo sancionador en UMA y su equivalente en MXN]

## Tabla de cumplimiento
| Bloque | Peso | Pts | Estado | Evidencia |
...

## Issues críticos / medios / bajos
...

## Notas metodológicas
- Verificado externamente
- La designación interna de la persona o departamento de datos solo se verifica por lo publicado
- UMA: valor vigente en inegi.org.mx
```

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_lfpdppp_[fecha].md`.

### Modo cliente (`--docx`)

Misma estructura que `rgpd` modo `--docx`, adaptada:
- Autoridad: Secretaría Anticorrupción y Buen Gobierno
- Multas en UMA, con su equivalente en MXN (valor vigente en inegi.org.mx)
- Terminología mexicana: aviso de privacidad, derechos ARCO, titular
- Pie de página: hipervínculo "Zythos Media" → https://zythos.media

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_lfpdppp_[fecha].docx`.

---

## Notas de alcance

Mismas limitaciones que el skill `rgpd`. Adicional:
- La gestión interna de la persona o departamento de datos y los esquemas de
  autorregulación no son auditables externamente

## Actualización normativa

- **LFPDPPP 2025**: DOF 20/03/2025, en vigor el 21/03/2025; abroga la ley de 2010.
- **Autoridad**: Secretaría Anticorrupción y Buen Gobierno; el INAI se extinguió.
- **Reglamento**: el de 2011 se aplica en lo que no contradiga la ley; sin reglamento
  nuevo al 20/11/2026.
- **Lineamientos del Aviso de Privacidad**: DOF 17/01/2013, como referencia práctica.
- **Multas**: en UMA (Art. 59).
- **Versión de esta skill:** 2.0.0 (2026-11-20). Reescrita sobre la ley de 2025: artículos
  del aviso (15-16), consentimiento (7-9), derechos ARCO (22-26, 31, 34), persona o
  departamento obligatorio (29), transferencias (35-36), vulneraciones (19), sanciones
  (58-59) y procedimiento ante la Secretaría (40).
