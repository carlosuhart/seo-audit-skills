---
name: ccpa
description: >
  Auditoría CCPA/CPRA (California): umbrales de aplicación, 8 derechos del consumidor,
  opt-out y contratos con proveedores, con informe de score y sanciones en USD.
  Sub-skill de /privacidad, también invocable sola.
user-invokable: true
argument-hint: "<url> [--docx]"
license: MIT
metadata:
  author: Zythos Media
  version: "1.1.0"
  category: legal-compliance
  revisar: "2027-01-15"
---

# CCPA / CPRA — Auditoría de Cumplimiento (California, EE.UU.)

## Uso

```
/ccpa https://ejemplo.com
/ccpa https://ejemplo.com --docx
```

---

## Marco normativo

- **CCPA**: California Consumer Privacy Act, Cal. Civ. Code §§ 1798.100 et seq.
  En vigor desde el 1 de enero de 2020.
- **CPRA**: California Privacy Rights Act (Proposition 24, aprobada noviembre 2020).
  Modificaciones en vigor desde el **1 de enero de 2023**. Crea la CPPA.
- **CPPA**: California Privacy Protection Agency — autoridad de cumplimiento creada
  por la CPRA. Sustituye parcialmente la aplicación por el Attorney General.
  Web: cppa.ca.gov (también usa la marca pública "CalPrivacy" y privacy.ca.gov; el nombre
  legal no cambió).
- **Attorney General de California**: mantiene competencia concurrente en algunas áreas.
- **Reglamentos de la CPPA**: opt-out signals (GPC), contratos con contratistas y
  proveedores de servicios, datos de menores y, desde el 01/01/2026, el paquete aprobado
  por la OAL el 23/09/2025 (https://cppa.ca.gov/announcements/2025/20250923.html):
  - **Evaluaciones de riesgo:** obligatorias desde el 01/01/2026 para quien vende o
    comparte datos (publicidad entre contextos incluida) o trata datos sensibles; la
    primera entrega a la CPPA vence el 01/04/2028.
  - **Decisiones automatizadas (ADMT) en decisiones significativas:** aviso previo,
    opt-out y acceso desde el 01/01/2027.
  - **Auditorías de ciberseguridad:** primeras entregas el 01/04/2028, 2029 o 2030 según
    facturación (más de USD 100 millones, de 50 a 100 millones, menos de 50 millones).
- **Delete Act y DROP:** los data brokers deben registrarse y, desde el 01/08/2026,
  procesar cada 45 días las solicitudes de borrado de la plataforma DROP (abierta a
  consumidores el 01/01/2026), con multa de USD 200 por solicitud y día. Solo aplica si
  el sitio vende datos de consumidores con los que no tiene relación directa.
- **AB 566 (Opt Me Out Act, firmada el 08/10/2025):** obliga a los navegadores a ofrecer
  una señal de opt-out desde el 01/01/2027; más usuarios llegarán con GPC activo.

⚠️ **CCPA ≠ RGPD**: La CCPA aplica un modelo **opt-out** (el consumidor opta por
salir), no un modelo opt-in como el RGPD. No requiere base jurídica para cada
tratamiento, pero sí exige transparencia y respeto de los derechos de opt-out.

⚠️ **CCPA es UMBRAL-DEPENDIENTE**: Solo aplica a empresas for-profit. Verificar
si el sitio auditado supera al menos uno de los tres umbrales (ver Bloque 0).

⚠️ **Versión normativa**: La CPPA continúa publicando reglamentos. Verificar
cppa.ca.gov para actualizaciones antes de finalizar cualquier auditoría.

---

## Paso 0 — Verificación de aplicabilidad (umbral)

La CCPA/CPRA solo aplica a empresas **for-profit** que hacen negocios en California
y cumplen **al menos uno** de estos tres umbrales:

| Umbral | Criterio |
|--------|---------|
| **A** | Ingresos brutos anuales > USD 26.625.000 en el año natural anterior (ajuste por IPC desde el 01/01/2025; el próximo ajuste bienal toca en 2027) |
| **B** | Compra, venta o compartición de datos personales de ≥ 100.000 consumidores o unidades familiares en California por año (§ 1798.140(d)(1)(B); la CPRA quitó "recepción") |
| **C** | ≥ 50% de los ingresos anuales provienen de la venta o compartición de datos personales de consumidores |

**Proceso:**
1. Si el sitio es de una ONG, entidad pública o empresa sin ánimo de lucro: CCPA no aplica → reportar como N/A.
2. Si la empresa es for-profit pero no hay evidencia de superar ningún umbral: reportar como "probablemente no sujeto a CCPA — aplicabilidad a verificar con el cliente".
3. Si hay indicios de superar uno o más umbrales (escala, publicidad dirigida, e-commerce de volumen, integración con brokers de datos): continuar la auditoría.

**Señales que sugieren aplicabilidad:**
- Publicidad comportamental o programática activa (Google Ads, Meta Pixel, etc.)
- Sitios de e-commerce a escala
- Operaciones de generación de leads
- Empresa con presencia en California o enfocada al mercado de EE.UU.
- Integración con data brokers o plataformas de datos de terceros

Si no se puede determinar la aplicabilidad: continuar la auditoría con nota de contingencia.

---

## Paso 0b — Stack tecnológico

Si este skill es invocado desde el orquestador `/privacidad`, usar el Paso 0
compartido. Si se invoca directamente, ejecutar el Paso 0 del skill `rgpd`.

Señales adicionales específicas de CCPA/California:
- "California Privacy" / "CCPA" / "CPRA" / "Do Not Sell" en el footer o política
- "California Residents" en la política de privacidad
- "Global Privacy Control" o señal GPC mencionada
- ".ca.gov" en páginas de referencia de derechos
- USD como moneda; sede declarada en California o EE.UU.

---

## Paso 1 — Recopilación de datos del sitio

Rutas comunes de políticas de privacidad CCPA:
- `/privacy-policy`
- `/privacy`
- `/california-privacy-rights`
- `/ccpa`
- `/do-not-sell`
- `/do-not-sell-my-personal-information`

---

## Paso 2 — Detección de sector

Usar la matriz del skill `rgpd`. Sectores con regulación adicional en California:

| Sector | Regulación adicional |
|--------|---------------------|
| **Salud** | CMIA (Confidentiality of Medical Information Act); posibles exclusiones HIPAA |
| **Financiero** | GLBA (Gramm-Leach-Bliley Act) — datos financieros pueden tener exención parcial |
| **Educación** | FERPA — datos de estudiantes pueden estar excluidos |
| **Menores** | COPPA (federal); CCPA secc. 1798.120(c) — prohibición de venta de datos de menores < 16 |

⚠️ CCPA tiene interacciones complejas con leyes sectoriales federales. Si aplica un sector regulado, verificar si existen datos excluidos del ámbito de la CCPA.

---

## Paso 3 — Auditoría por bloques

Evaluar: **Cumple / Parcial / No cumple / No evaluable**

### Bloque 1 — Identificación del negocio y datos de contacto (§ 1798.130)
Peso: 10 pts

Verificar en la política de privacidad (Privacy Policy):
- [ ] Nombre o razón social del negocio
- [ ] Datos de contacto para ejercicio de derechos: email designado O formulario web
- [ ] Teléfono gratuito (toll-free) — exigido salvo que el negocio opere exclusivamente en línea y tenga relación directa con el consumidor: en ese caso basta un email (§ 1798.130(a)(1)(A))
- [ ] Sede o domicilio del responsable (no exigido pero buena práctica)
- [ ] Fecha de "última actualización" de la política de privacidad

### Bloque 2 — Política de privacidad: existencia y acceso (§ 1798.130)
Peso: 5 pts

La CCPA exige una Privacy Policy "conspicuamente publicada":
- [ ] Existe política de privacidad publicada
- [ ] Enlace visible en el footer (el término exacto "Privacy Policy" es el estándar)
- [ ] Accesible desde la página de inicio con un solo clic
- [ ] Si el negocio tiene app o tienda online: enlace en el punto de recogida de datos
- [ ] Versión exclusiva para "California Residents" o sección dedicada claramente identificada

### Bloque 3 — Política de privacidad: contenido mínimo (§ 1798.110 + § 1798.115 + § 1798.130)
Peso: 15 pts

La CCPA exige informar sobre (1 pt por ítem):

**Categorías de datos y finalidades:**
- [ ] Categorías de información personal (PI) recogida en los últimos 12 meses
- [ ] Finalidades para las que se usa cada categoría de PI
- [ ] Categorías de fuentes de las que se recoge PI
- [ ] Categorías de terceros con los que se comparte PI

**Ventas y compartición:**
- [ ] Categorías de PI vendida o compartida en los últimos 12 meses
  (o declaración de que no se vende ni comparte PI)
- [ ] Categorías de terceros a los que se vende o comparte PI

**Información personal sensible (SPI — CPRA):**
- [ ] Si se recoge SPI: categorías específicas de SPI recogidas
- [ ] Finalidades del tratamiento de SPI
- [ ] Si SPI se usa más allá de lo necesario para el servicio: derechos de limitación

**Periodos de conservación:**
- [ ] Para cada categoría de PI: periodo de conservación o criterios para determinarlo
  (CPRA — § 1798.100(a)(3))

**Derechos del consumidor:**
- [ ] Lista de los 8 derechos (ver Bloque 6)
- [ ] Mecanismo(s) para ejercerlos
- [ ] Descripción del proceso de verificación de identidad
- [ ] Derecho a no ser discriminado por ejercer sus derechos (§ 1798.125)

**Menores:**
- [ ] Si el negocio vende datos de menores: mencionar el régimen específico
  (< 13 años: consentimiento de padre/tutor; 13-15: opt-in del propio menor)

**Actualización anual:**
- [ ] La política se actualiza al menos una vez al año (§ 1798.130(a)(5))
  — verificar fecha de última actualización

### Bloque 4 — Opt-out: "Do Not Sell or Share My Personal Information" (§ 1798.120 + § 1798.121)
Peso: 15 pts

Este es uno de los elementos más específicos de la CCPA. No tiene equivalente
directo en el RGPD.

**"Venta" y "compartición" (sharing) en la CCPA/CPRA:**
- **Venta**: intercambio de PI por dinero u otra contraprestación de valor
- **Compartición (sharing)**: transferir PI a un tercero para publicidad comportamental
  entre contextos (cross-context behavioral advertising) — aunque sea sin pago (CPRA)
- **Descarga práctica**: si el sitio usa Meta Pixel, Google Analytics con señales de
  audience, Google Ads, o cualquier cookie publicitaria de terceros activa sin opt-out:
  casi seguramente está "vendiendo" o "compartiendo" PI bajo la definición CCPA

**Requisitos:**
- [ ] Enlace "Do Not Sell or Share My Personal Information" o "Do Not Sell My PI"
  visible en el footer de la página de inicio y de todas las páginas donde se recojan datos,
  o el enlace alternativo único "Your Privacy Choices" con el ícono oficial (Reglamentos
  CPPA § 7015)
- [ ] El enlace es funcional y lleva a un mecanismo de opt-out
- [ ] El mecanismo de opt-out es gratuito
- [ ] No se exige crear una cuenta para ejercer el opt-out
- [ ] Si el negocio declara que NO vende ni comparte PI: debe ser verificable
  (revisar trackers activos antes de aceptar esta declaración)

**Global Privacy Control (GPC) — § 1798.135(b) + Reglamentos CPPA:**
- [ ] El sitio reconoce y respeta la señal GPC (obligatorio para negocios sujetos a CPRA)
- [ ] La política menciona la señal GPC o "señales de preferencia del usuario"
- [ ] **Prueba en vivo:** con GPC activo en el navegador, los píxeles publicitarios no se
  disparan, incluso con la sesión iniciada. Es lo que ya se sanciona: Honda
  (USD 632.500, marzo de 2025), Todd Snyder (USD 345.178, mayo de 2025) y Tractor Supply
  (USD 1.350.000, 30/09/2025), más un barrido conjunto de California, Colorado y
  Connecticut sobre GPC (09/09/2025). Fuente:
  https://cppa.ca.gov/announcements/2025/20250930.html

**Nota:** Si se detectan cookies de publicidad comportamental activas (antes de cualquier opt-out) pero no hay enlace "Do Not Sell or Share": issue crítico.

### Bloque 5 — Información Personal Sensible (SPI) y derecho de limitación (§ 1798.121 CPRA)
Peso: 10 pts

La CPRA añade la categoría de **Sensitive Personal Information (SPI)** con un derecho
propio de limitación ("Limit the Use of My Sensitive Personal Information").

**Categorías de SPI (§ 1798.140(ae)):**
- Social Security Number (SSN), número de pasaporte, número de licencia de conducir
- Información de cuenta financiera, tarjeta de crédito/débito con credenciales de acceso
- Datos de geolocalización precisa
- Datos raciales o étnicos, religiosos o filosóficos, sindicales
- Datos de correo, emails o SMS privados sin el fin de prestar el servicio
- Datos genéticos
- Datos biométricos procesados para identificar unívocamente a una persona
- Datos de salud (diagnóstico, tratamiento)
- Datos sobre vida sexual u orientación sexual
- Credenciales de acceso a una cuenta (usuario más contraseña o pregunta de seguridad)
- Datos neuronales (añadidos por SB 1223, desde el 01/01/2025)

**Si el sitio NO recoge ni usa SPI:** marcar N/A, 10 pts.

**Si recoge o usa SPI:**
- [ ] Categorías de SPI identificadas en la política
- [ ] Finalidades del tratamiento de SPI declaradas
- [ ] Enlace separado "Limit the Use of My Sensitive Personal Information"
  (si la SPI se usa para más de los propósitos permitidos sin limitación)
- [ ] El mecanismo de limitación es funcional y gratuito
- [ ] Si la SPI se "vende" o "comparte": el enlace "Do Not Sell or Share" lo cubre también

### Bloque 6 — Derechos del consumidor (§ 1798.100–1798.125)
Peso: 15 pts

La CCPA/CPRA reconoce 8 derechos. Plazo de respuesta: **45 días calendario**
(prorrogables 45 días adicionales con notificación). El negocio puede limitar a 2 al año
las solicitudes de acceso (saber y portabilidad, § 1798.130(a)(2)(B)); no hay ese límite
para los demás derechos:

1. **Derecho a saber** (§ 1798.110): qué PI se recopila, de dónde, con qué fin,
   con quién se comparte; por defecto los últimos 12 meses, pero para datos recogidos
   desde el 01/01/2022 el consumidor puede pedir un periodo mayor, salvo que sea
   imposible o desproporcionado (§ 1798.130(a)(2)(B))
2. **Derecho a eliminar** (§ 1798.105): solicitar eliminación de PI recopilada;
   aplican excepciones (legal, seguridad, fraude, etc.)
3. **Derecho a corregir** (§ 1798.106 — CPRA): solicitar corrección de PI inexacta
4. **Derecho a opt-out de venta/compartición** (§ 1798.120/121): no se puede
   discriminar al consumidor por ejercerlo (§ 1798.125)
5. **Derecho a limitar el uso de SPI** (§ 1798.121 — CPRA): limitar el uso de SPI
   a los propósitos mínimos necesarios para prestar el servicio
6. **Derecho a la portabilidad** (§ 1798.100(d)): recibir PI en formato portable y
   usable; aplica a solicitudes de acceso
7. **Derecho a no ser discriminado** (§ 1798.125): el negocio no puede negar servicios,
   cobrar más o dar calidad inferior por ejercer derechos CCPA
8. **Derecho a opt-out de decisiones automatizadas** (§ 1798.185(a)(16) — Reglamento
   CPPA): reglamento aprobado el 23/09/2025; para decisiones significativas, aviso
   previo, opt-out y acceso exigibles desde el 01/01/2027

**Menores (§ 1798.120(c)):**
- < 13 años: prohibición de venta salvo consentimiento opt-in del padre/tutor
- 13–15 años: prohibición de venta salvo consentimiento opt-in del propio menor
- Infracción con menores: multa de USD 7.988 por violación (vs. USD 2.663 otros casos; importes ajustados por IPC desde el 01/01/2025)

Verificar:
- [ ] Todos los derechos mencionados en la política
- [ ] Canal funcional para ejercer derechos: email designado Y/O formulario web
- [ ] Teléfono gratuito disponible (si procede por tamaño de negocio)
- [ ] Plazo de respuesta de 45 días mencionado
- [ ] Proceso de verificación de identidad descrito (razonable, no excesivamente oneroso)
- [ ] Declaración explícita de no discriminación por ejercer derechos

### Bloque 7 — Acuerdos con proveedores de servicios y contratistas (§ 1798.140(ag) y (j))
Peso: 10 pts

La CPRA establece tres tipos de terceros receptores de PI:
- **Service provider** (proveedor de servicios): recibe PI solo para prestar el servicio;
  necesita contrato específico que prohíbe venta/compartición y limita uso
- **Contractor** (contratista): recibe PI bajo contrato pero puede procesarla en sus propios
  sistemas; también necesita contrato equivalente
- **Third party** (tercero): todos los demás; la venta/compartición con ellos activa el
  derecho de opt-out

**Nota práctica:** Los trackers de publicidad (Meta Pixel, Google Ads, etc.) que reciben
PI para sus propias finalidades son "terceros", no "service providers" — activan el régimen
de opt-out aunque el negocio los llame "proveedores".

Verificar:
- [ ] La política distingue entre "service providers / contractors" y "terceros"
- [ ] Si el sitio usa terceros publicitarios: reconoce que comparte/vende PI con ellos
- [ ] La política menciona que existen contratos con service providers que limitan el uso
- [ ] No hay trackers de publicidad activos sin haberse declarado en la sección de "venta/compartición"

### Bloque 8 — Seguridad y notificación de brechas (§ 1798.100(e) + § 1798.150)
Peso: 5 pts

La CCPA no establece medidas de seguridad específicas, pero exige medidas
"razonables". La CPRA añade que el tratamiento debe limitarse a lo necesario.

**Derecho de acción privada por brechas (§ 1798.150):**
Los consumidores cuyos datos fueron comprometidos en una brecha por falta de
medidas de seguridad razonables tienen derecho a daños de **USD 107 a USD 799**
por consumidor por incidente (importes ajustados por IPC desde el 01/01/2025), o los
daños reales si son mayores.
Esto es un derecho de acción privada — no requiere intervención de la CPPA.

Verificar:
- [ ] HTTPS activo en todas las páginas
- [ ] Certificado SSL/TLS válido y no expirado
- [ ] HSTS habilitado
- [ ] La política menciona que se adoptan medidas de seguridad razonables
- [ ] Si la política menciona brechas: describe el proceso o referencia la notificación
  (California tiene ley de notificación de brechas separada — Cal. Civ. Code § 1798.82)

### Bloque 9 — Tratamiento de datos de menores (§ 1798.120(c) + COPPA)
Peso: 5 pts

**Si el sitio no está dirigido a menores ni recoge datos de menores:** N/A, 5 pts.

**Si el sitio puede llegar a menores:**
- [ ] La política indica cómo se gestiona la información de menores
- [ ] Si recoge datos de menores < 13: menciona el consentimiento parental requerido
- [ ] Si puede vender datos de menores 13–15: menciona el opt-in del menor requerido
- [ ] No hay mecanismo para que menores < 13 se registren sin consentimiento parental
- [ ] Si opera bajo COPPA (federal, < 13): verificar cumplimiento COPPA separadamente

### Bloque 10 — Autenticidad y actualización de la política (§ 1798.130(a)(5))
Peso: 10 pts

La CCPA exige que la Privacy Policy sea actualizada al menos **cada 12 meses**
y que refleje las prácticas reales del negocio.

Verificar:
- [ ] Fecha de "última actualización" o "Last Updated" visible
- [ ] La fecha es de hace menos de 12 meses respecto a la auditoría
- [ ] Las categorías de PI declaradas coinciden con los trackers y formularios activos
  detectados en el Paso 0 (coherencia política vs. realidad técnica)
- [ ] Si el sitio usa Google Analytics, Meta Pixel, u otros trackers: están declarados
  en la sección de categorías de PI recogida y de terceros
- [ ] La política distingue correctamente entre "venta" y "compartición" per CPRA
- [ ] Si hay prácticas de publicidad comportamental: están reconocidas como "compartición"

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

## Paso 5 — Clasificación de issues y sanciones (§ 1798.155 + § 1798.150)

**Sanciones administrativas (CPPA — § 1798.155):**
| Conducta | Sanción por violación |
|---|---|
| Violación no intencional | USD 2.663 |
| Violación intencional | USD 7.988 |
| Violación con datos de menores < 16 | USD 7.988 siempre (no existe la escala "no intencional") |

Importes ajustados por IPC desde el 01/01/2025 (antes USD 2.500 y USD 7.500), en
§ 1798.155 y § 1798.199.90. Fuente: https://cppa.ca.gov/regulations/cpi_adjustment.html
(17/12/2024). El próximo ajuste bienal toca en 2027: verificar antes de citar.

No hay límite global establecido por ley, pero el CPPA puede multar por cada
"violación" — y si se afecta a miles de consumidores, las multas se multiplican.

**Derecho de acción privada (§ 1798.150):**
- USD 107–799 por consumidor por incidente de brecha de datos
- Los daños reales si son mayores
- Acciones de clase son posibles

**Críticos:**
- Sin enlace "Do Not Sell or Share" cuando el sitio claramente vende/comparte PI → § 1798.120/121
- Trackers publicitarios activos sin declaración ni opt-out → USD 7.988/violación intencional
- Píxeles publicitarios que se disparan con GPC activo → riesgo ya sancionado (Honda, Todd Snyder, Tractor Supply)
- Sin política de privacidad publicada → § 1798.130
- Sin mecanismo para ejercer derechos → § 1798.130
- Venta/compartición de datos de menores < 16 sin opt-in → USD 7.988 por violación
- Sin HTTPS → § 1798.150 (riesgo de acción privada en caso de brecha)

**Medios:**
- Política existe pero sin sección para residentes de California
- Sin teléfono gratuito cuando es exigible
- Sin fecha de actualización o desactualizada (> 12 meses)
- SPI recogida pero sin enlace "Limit the Use" si aplica
- No se menciona el período de conservación de datos (CPRA § 1798.100(a)(3))
- Política no distingue "service provider" de "tercero"
- GPC no mencionado ni respetado

**Bajos:**
- Falta declaración explícita de no discriminación
- Proceso de verificación de identidad no descrito
- Plazo de 45 días no mencionado explícitamente

---

## Paso 6 — Output según modo

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_ccpa_[fecha].md` o `.docx`.

Modo `--docx`: misma estructura que `rgpd`, adaptada:
- Autoridad: CPPA (cppa.ca.gov) + Attorney General de California
- Sanciones: USD 2.663 / USD 7.988 por violación; USD 107–799 acción privada por brecha (importes de 2025)
- Umbral de aplicabilidad: incluir sección de "Alcance y aplicabilidad" al inicio
- Idioma del informe: inglés (si el sitio auditado es en inglés) o español
- Pie de página: hipervínculo "Zythos Media" → https://zythos.media

---

## Actualización normativa

- **CCPA base**: en vigor desde 1 enero 2020.
- **CPRA modificaciones**: en vigor desde 1 enero 2023.
- **Ajuste por IPC**: umbral USD 26.625.000, multas USD 2.663 / 7.988, acción privada
  USD 107–799, desde el 01/01/2025. Próximo ajuste en 2027.
- **Reglamentos CPPA (aprobados 23/09/2025, vigentes 01/01/2026)**: evaluaciones de
  riesgo desde 01/01/2026 (primera entrega 01/04/2028); ADMT desde 01/01/2027; auditorías
  de ciberseguridad 2028-2030 según facturación.
- **GPC**: obligatorio; sanciones aplicadas en 2025. AB 566 obliga a los navegadores a
  ofrecer la señal desde el 01/01/2027.
- **Delete Act / DROP**: DROP abierto a consumidores el 01/01/2026; brokers procesan
  desde el 01/08/2026.
- **Versión de esta skill:** 1.1.0 (2026-11-20). Revisada contra cppa.ca.gov y el
  Civil Code el 20/11/2026.
