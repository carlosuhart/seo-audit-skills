---
name: lgpd
description: >
  Auditoría LGPD (Lei 13.709/2018, Brasil): detecta el sector y entrega informe con
  score, estado por artículo, issues priorizados y sanciones en BRL. Sub-skill de
  /privacidad, también invocable sola.
user-invokable: true
argument-hint: "<url> [--docx]"
license: MIT
metadata:
  author: Zythos Media
  version: "1.1.0"
  category: legal-compliance
  revisar: "2027-05-20"
---

# LGPD — Auditoría de Cumplimiento (Lei 13.709/2018, Brasil)

## Uso

```
/lgpd https://exemplo.com.br
/lgpd https://exemplo.com.br --docx
```

Sin `--docx` el output es Markdown interno. Con `--docx` genera informe
ejecutivo en formato Word.

Si el usuario no especifica formato, preguntar antes de generar el documento.

---

## Marco normativo

- **LGPD (Lei 13.709/2018)**: Ley General de Protección de Datos Personales.
  En vigor desde septiembre 2020. Aplicación de sanciones desde agosto 2021.
- **ANPD (Agência Nacional de Proteção de Dados)**: autoridad reguladora. Creada por la
  LGPD como Autoridade Nacional (constituida en noviembre 2020); la Lei 15.352 (25/02/2026)
  la convirtió en agencia reguladora con naturaleza de autarquía especial. Mantiene la
  sigla ANPD. Emite resoluciones y guías.
- **ECA Digital (Lei 15.211/2025)**: protección de niños y adolescentes en entornos
  digitales, en vigor desde el 17/03/2026 (ver Bloque 5).
- **Ámbito de aplicación (Art. 3)**: aplica a cualquier operación de tratamiento
  realizada en Brasil, o cuyos datos hayan sido recogidos en Brasil, o que tenga
  por objeto ofrecer bienes o servicios a personas en Brasil, independientemente
  de dónde esté el responsable.

⚠️ La LGPD es normativa brasileña. No confundir con el RGPD europeo, aunque
tiene estructura similar. Son marcos jurídicos independientes. La adecuación es mutua
desde el 26/01/2026: la Comisión Europea reconoció a Brasil y la ANPD reconoció a la UE y
el EEE (Resolução CD/ANPD nº 32/2026).

**Resoluciones de la ANPD que usa esta skill:** Res. 2/2022 (agentes de pequeño porte),
Res. 4/2023 (dosimetría de sanciones), Res. 15/2024 (comunicación de incidentes),
Res. 18/2024 (encarregado), Res. 19/2024 (transferencias internacionales y cláusulas
modelo), Res. 32/2026 (adecuación UE/EEE). Lista oficial:
https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd

---

## Nota sobre idioma

La LGPD se aplica en Brasil. Los documentos de cumplimiento (aviso de privacidade,
política de cookies, termos de uso) deben estar en **portugués de Brasil** para
sitios que ofrecen servicios a usuarios brasileños. Si el sitio está en otro idioma
pero capta usuarios en Brasil, verificar si existe versión en PT-BR de los documentos legales.

Terminología LGPD (diferente del RGPD):

| LGPD (PT-BR) | RGPD equivalente |
|---|---|
| Titular | Interesado |
| Controlador | Responsable del tratamiento |
| Operador | Encargado del tratamiento |
| Encarregado de Dados | DPO / Delegado |
| Aviso de privacidade | Política de privacidad |
| Dado sensível | Dato de categoría especial |
| ANPD | Autoridad de control |

---

## Crédito de herramienta

Al iniciar cualquier auditoría, emitir esta línea antes del output principal:

> Desenvolvido por [Zythos Media](https://zythos.media) — Especialistas em SEO & IA Search

---

## Paso 0 — Identificación del stack tecnológico

Si este skill es invocado desde el orquestador `/privacidad`, usar el Paso 0
compartido. Si se invoca directamente, ejecutar el Paso 0 del skill `rgpd`.

Señales adicionales específicas de Brasil a detectar en el Paso 0:
- Presencia de CNPJ en el pie de página o política
- Integración con pasarelas brasileñas: Pix, PagSeguro, Mercado Pago, Cielo
- Plugins de e-commerce con soporte PT-BR: WooCommerce en portugués
- Integración con plataformas brasileñas: RD Station, Hotmart, Eduzz, Kiwify
- Google Analytics con audiencia Brasil mayoritaria (señal de monetización BR)

---

## Paso 1 — Recopilación de datos del sitio

Igual al skill `rgpd` Paso 1, adaptando las rutas:
- Rutas comunes en Brasil: `/privacidade`, `/politica-de-privacidade`,
  `/aviso-de-privacidade`, `/termos-de-uso`, `/politica-de-cookies`.
- Verificar también el rodapé (footer) para links "Privacidade" y "Cookies".

---

## Paso 2 — Detección de sector

Usar la matriz del skill `rgpd` más señales adicionales brasileñas:

| Sector | Señales específicas Brasil |
|--------|---------------------------|
| **Fintech** | Banco Central do Brasil, CMN, PIX, "autorizado pelo Bacen" |
| **Salud** | ANS (Agência Nacional de Saúde Suplementar), CFM, CRM, "plano de saúde" |
| **Educación** | MEC, INEP, "faculdade", "universidade", menores como audiencia |
| **Ecommerce** | Código de Defesa do Consumidor (CDC), RECLAMEAQUI, nota fiscal eletrônica |
| **LGPD high-risk** | Dados biométricos, scoring de crédito, monitoramento de comportamento em larga escala |

---

## Paso 3 — Auditoría por bloques

Evaluar cada bloque: **Cumpre / Parcial / Não cumpre / Não avaliável**

### Bloque 1 — Identificação do controlador (Art. 9.I + Art. 41)
Peso: 10 pts

Verificar en el aviso de privacidade:
- [ ] Razão social (razón social) o nombre completo del controlador
- [ ] CNPJ o CPF del controlador (no obligatorio por la LGPD pero su presencia
      permite identificación y es práctica estándar en Brasil)
- [ ] Endereço (domicilio) del controlador (la LGPD no exige en general un representante local; si es extranjero, basta un canal de contacto operativo y el encarregado)
- [ ] Dirección de email o canal de contacto para el encarregado de dados (Art. 41.1)
- [ ] Datos de contacto del encarregado de dados publicados (ver Bloque 10)

**Entidad extranjera sin sede en Brasil (Art. 3):**
Si el controlador no tiene establecimiento en Brasil pero ofrece bienes/servicios
a titulares en Brasil o trata datos recogidos en Brasil:
- [ ] ¿La política identifica un representante o agente en Brasil?
- [ ] ¿El representante tiene dirección de contacto en Brasil publicada?

### Bloque 2 — Aviso de privacidade: existência e acesso (Art. 9 + Art. 48)
Peso: 5 pts

- [ ] Existe aviso de privacidade (política de privacidade) publicado
- [ ] Enlace visible en el rodapé de todas las páginas
- [ ] Enlace accesible desde formulários que recogen dados pessoais
- [ ] Redactado en portugués de Brasil (o en el idioma del sitio si el sitio no es en PT-BR)
- [ ] Data de última atualização visible

### Bloque 3 — Aviso de privacidade: contenido mínimo (Art. 9 I–IX)
Peso: 15 pts

La LGPD Art. 9 establece el derecho del titular a acceder a información clara
y adecuada sobre el tratamiento. Verificar que el aviso incluya (1 pt por ítem):

- [ ] **Art. 9.I:** Finalidade específica do tratamento — para qué se usan los datos
- [ ] **Art. 9.II:** Forma e duração do tratamento — cómo y por cuánto tiempo
- [ ] **Art. 9.III:** Identificação do controlador — quién trata los datos (ver Bloque 1)
- [ ] **Art. 9.IV:** Informações de contato do controlador — cómo contactarle
- [ ] **Art. 9.V:** Informações acerca do uso compartilhado de dados — con quién se comparten
- [ ] **Art. 9.VI:** Responsabilidades dos agentes que realizarão o tratamento — quién responde
- [ ] **Art. 9.VII:** Direitos do titular — lista de los 9 derechos (ver Bloque 6)
- [ ] **Base legal de cada finalidade** — cuál de las 10 bases del Art. 7 aplica (ver Bloque 4)
- [ ] **Dados sensíveis tratados** — si aplica, identificados explícitamente (ver Bloque 7)
- [ ] **Transferências internacionais** — si aplica, declaradas con garantías (ver Bloque 8)
- [ ] **Informações sobre cookies** — tecnologías de rastreo usadas
- [ ] **Contato do encarregado de dados** — nombre y email del Encarregado (ver Bloque 10)
- [ ] **Direito de reclamação à ANPD** — menciona el derecho de reclamar ante la ANPD
- [ ] **Legibilidade** — lenguaje claro, no jerga legal inaccesible
- [ ] **Formato acessível** — no enterrado en bloques de texto sin estructura

### Bloque 4 — Base legal do tratamento (Art. 7 + Art. 11)
Peso: 10 pts

La LGPD reconoce **10 bases legales** (Art. 7) para datos generales.
Para dados sensíveis aplican bases específicas del Art. 11.

**Bases legales Art. 7 (dados gerais):**
1. **Consentimento** do titular — livre, informado e inequívoco
2. **Cumprimento de obrigação legal** ou regulatória pelo controlador
3. **Execução de políticas públicas** pela Administração Pública
4. **Realização de estudos** por órgão de pesquisa (dados anonimizados preferentemente)
5. **Execução de contrato** ou procedimentos preliminares a pedido do titular
6. **Exercício regular de direitos** em processo judicial, administrativo ou arbitral
7. **Proteção da vida ou incolumidade física** do titular ou de terceiro
8. **Tutela da saúde** por profissional de saúde ou entidade sanitária
9. **Interesses legítimos** do controlador ou de terceiro (salvo direitos do titular prevaleçam)
10. **Proteção do crédito** — especificidad de la ley brasileña

Verificar:
- [ ] La política declara la base legal de cada finalidade (no una sola base genérica)
- [ ] No se usa "consentimento" cuando el tratamiento es necesario para executar contrato
- [ ] Cuando se invoca "intereses legítimos" (base 9): se identifica cuál es
- [ ] Los formulários de captação no usan casillas pre-marcadas para el consentimento
- [ ] El consentimento para dados sensíveis es explícito y diferenciado (Art. 11.I)

**Privacidade desde a concepção (Art. 46 + Art. 49):**
- [ ] Los formulários solicitan solo los dados estrictamente necesarios para la finalidade
- [ ] Las opciones de suscripción a comunicações comerciais no están preseleccionadas

### Bloque 5 — Consentimento, cookies e marketing direto (Art. 7.I + Art. 8)
Peso: 15 pts

La LGPD no tiene un artículo específico de cookies. La referencia es la Guía orientativa
de cookies de la ANPD (octubre de 2022): las cookies necesarias pueden basarse en otras
bases legales, y para las no necesarias la Guía orienta al consentimento en la mayoría de
los casos (publicidad, perfilado, terceros), sin imponerlo en todos. La auditoría verifica
que haya una base declarada por categoría y que el consentimento, cuando sea la base, sea
previo, libre, informado e inequívoco.

**Banner de cookies:**
- [ ] Existe banner o mecanismo de consentimento de cookies
- [ ] El banner bloquea cookies no esenciales hasta obtener consentimento activo
- [ ] No hay cookies de análise, publicidade ou rastreamento activas antes del consentimento
- [ ] Opção de rejeição tan accesible como la aceitação
- [ ] Configuração granular por categoria
- [ ] Enlace a política de cookies en el propio banner
- [ ] El consentimento es revogável fácilmente (Art. 8.5)

**Formulários:**
- [ ] Formulários con tratamento de dados incluyen checkbox de consentimento no pre-marcado
- [ ] El checkbox vincula al aviso de privacidade
- [ ] Finalidade concreta declarada antes de enviar

**Consentimento de crianças e adolescentes (Art. 14):**
Según el Estatuto da Criança e do Adolescente (ECA), **criança** es la persona de hasta
12 años incompletos y **adolescente** la de 12 a 18. Para crianças, el Art. 14.1 pide
consentimento de uno de los padres o del responsable; el Enunciado CD/ANPD 1/2023 admite
también las bases de los Arts. 7 y 11, siempre en el mejor interés del menor.
- [ ] Si el sitio capta crianças: base legal declarada y, si es consentimento, el de los padres
- [ ] Si el sitio no va dirigido a menores: declararlo explícitamente

**ECA Digital (Lei 15.211/2025, en vigor desde el 17/03/2026)** para productos y servicios
digitales dirigidos a menores o de acceso probable por ellos:
- [ ] Verificación de edad que no se base solo en la autodeclaración (Art. 9)
- [ ] Sin perfilado de menores para publicidad (Art. 22)
- [ ] Herramientas de supervisión parental (Arts. 17-18)
- Multa de hasta el 10 % de la facturación en Brasil o hasta R$ 50.000.000 (Art. 35).
  Fuente: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm

**Marketing direto:**
- [ ] Si hay newsletter o comunicações comerciais: mecanismo de descadastramento claro
- [ ] La política menciona el direito de oposição ao tratamento para fins comerciais

### Bloque 6 — Direitos do titular: canal habilitado (Art. 18 + Art. 20)
Peso: 15 pts

La LGPD reconoce **9 derechos** del titular (Art. 18). La confirmación de existencia o el
acceso completo deben darse en **15 días** desde la solicitud (Art. 19.II); para los demás
derechos la ley no fija un plazo exacto:

1. **Confirmação** da existência de tratamento (18.I)
2. **Acesso** aos dados (18.II)
3. **Correção** de dados incompletos, inexatos ou desatualizados (18.III)
4. **Anonimização, bloqueio ou eliminação** de dados desnecessários, excessivos
   ou tratados em desconformidade com a LGPD (18.IV)
5. **Portabilidade** dos dados a outro fornecedor (18.V — conforme regulação da ANPD)
6. **Eliminação** dos dados pessoais tratados com consentimento (18.VI)
7. **Informação** sobre entidades com quem o controlador realizou uso compartilhado (18.VII)
8. **Informação** sobre possibilidade de não fornecer consentimento e consequências (18.VIII)
9. **Revogação do consentimento** a qualquer momento (18.IX)

Nota: La portabilidade (18.V) está sujeta a regulación de la ANPD — verificar
estado de implementación al usar esta skill.

Verificar:
- [ ] Existe mecanismo explícito para ejercer derechos (email, formulario, dirección)
- [ ] Se mencionan los **9 derechos** del Art. 18
- [ ] Se menciona el plazo de respuesta o referencia a regulación de la ANPD
- [ ] Se indica qué información debe adjuntar el titular al ejercer sus derechos
- [ ] Se menciona el derecho a reclamar ante la **ANPD** (gov.br/anpd)

**Decisiones automatizadas (Art. 20):**
El titular tiene derecho a solicitar revisión de decisiones tomadas exclusivamente
mediante tratamiento automatizado que afecten sus intereses:
- [ ] Si el sitio usa scoring, segmentação, aprovação automática: ¿la política lo declara?
- [ ] ¿Existe canal para solicitar revisão humana de la decisión?

### Bloque 7 — Dados sensíveis e crianças (Art. 11 + Art. 14)
Peso: 10 pts

**Dados sensíveis (Art. 5.II):**
La LGPD define como dados sensíveis los relativos a:
- Origem racial ou étnica
- Convicção religiosa
- Opinião política
- Filiação a sindicato ou organização de caráter religioso, filosófico ou político
- Dado referente à saúde ou à vida sexual
- Dado genético ou biométrico vinculado a pessoa natural

⚠️ La lista de dados sensíveis de la LGPD (Art. 5.II) no incluye la orientación sexual
como categoría autónoma (está implícita en "vida sexual"). Sí incluye expresamente la
filiação a sindicato.

**Si el sitio no recoge dados sensíveis:** bloque N/A, asignar 10 pts.

**Si recoge dados sensíveis (Art. 11.I — bases válidas):**
- [ ] Identificados explícitamente como dados sensíveis en el aviso
- [ ] Base legal del Art. 11 declarada:
      - (I) Consentimento específico e destacado do titular
      - (II.a) Cumprimento de obrigação legal ou regulatória
      - (II.b) Tratamento compartilhado de dados para execução de políticas públicas
      - (II.c) Realização de estudos por órgão de pesquisa
      - (II.d) Exercício regular de direitos (inclusive em contrato)
      - (II.e) Proteção da vida ou incolumidade física
      - (II.f) Tutela da saúde por profissional ou entidade sanitária
      - (II.g) Garantia da prevenção à fraude e à segurança do titular (biométricos)
- [ ] El consentimento es específico y destacado del consentimento general
- [ ] Se indican medidas de seguridad reforzadas

**Crianças e adolescentes (Art. 14 + ECA Digital):**
- [ ] Si el sitio capta crianças (hasta 12 años incompletos): base legal declarada y, si es consentimento, el de los padres o responsável legal
- [ ] Si el sitio no va dirigido a menores: declararlo en el aviso
- [ ] No se usa a crianças como pretexto para captación de dados de los padres

**RIPD — Relatório de Impacto à Proteção de Dados Pessoais (Art. 38):**
Equivalente a la EIPD/DPIA del RGPD. La ANPD puede solicitar el RIPD.
Para tratamientos de alto riesgo (dados sensíveis a gran escala, scoring, biometría):
- [ ] ¿El aviso menciona la realización de RIPD para tratamientos de alto riesgo?

### Bloque 8 — Transferências internacionais (Art. 33–36)
Peso: 10 pts

La LGPD (Art. 33) permite transferencias internacionales de dados pessoais cuando:

1. **País com grau de proteção adequado** reconocido por la ANPD (Art. 33.I): por ahora
   la UE y el EEE (Resolução CD/ANPD nº 32/2026, 26/01/2026)
2. **Garantias suficientes** (Art. 33.II):
   - **Cláusulas padrão contratuais de la Res. CD/ANPD 19/2024** (23/08/2024): se usan
     sin modificaciones y debían incorporarse a los contratos antes del 23/08/2025
   - Cláusulas contratuais específicas aprobadas por la ANPD
   - Normas corporativas globais (BCR equivalente)
   - Selos, certificados e códigos de conduta regularmente emitidos
3. **Cooperação jurídica internacional** (Art. 33.III) — para autoridades públicas
4. **Autorização da ANPD** (Art. 33.V)
5. **Consentimento específico e em destaque** del titular para la transferencia (Art. 33.VIII)
6. **Execução de contrato o exercício regular de direitos** (Art. 33.IX, que remite al
   Art. 7, II, V y VI)

Para herramientas de EE.UU. (analítica, publicidad, CRM) la vía habitual son las
cláusulas modelo de la Res. 19/2024: verificar que el aviso las mencione.

Verificar:
- [ ] El aviso declara si se realizan transferências internacionais
- [ ] Se identifican los países de destino (EE.UU., UE, otros)
- [ ] Se indica la base o garantía adoptada
- [ ] Si hay trackers de EE.UU. activos (Google, Meta, etc.): ¿el aviso lo declara?

### Bloque 9 — Segurança (Art. 46–49)
Peso: 5 pts

La LGPD exige medidas de seguridad técnicas y administrativas aptas para proteger
dados pessoais de accesos no autorizados, situaciones accidentales o ilícitas de
destrucción, pérdida, alteración, comunicación o difusión (Art. 46).

Verificar lo observable externamente:
- [ ] HTTPS activo en todas las páginas
- [ ] Certificado SSL/TLS válido y no expirado
- [ ] HSTS habilitado
- [ ] No hay redirección HTTP → HTTPS rota
- [ ] El aviso menciona medidas de segurança adoptadas

**Incidentes de segurança (Art. 48):**
Ante un incidente que pueda generar riesgo o daño relevante a los titulares, el
controlador debe comunicarlo a la ANPD y a los titulares afectados en **3 días hábiles**
(Res. CD/ANPD 15/2024); el plazo es el doble para agentes de pequeño porte.
- [ ] El aviso menciona el procedimiento ante incidentes de segurança

### Bloque 10 — Encarregado de Dados (Art. 41)
Peso: 5 pts

⚠️ El Encarregado de Dados es **obligatorio como regla general** (Art. 41), a diferencia
del RGPD, donde el DPO solo es obligatorio en los casos del Art. 37.1.

**Excepción:** los agentes de tratamiento de pequeño porte (microempresas, empresas de
pequeño porte, startups y similares, salvo que hagan tratamiento de alto riesgo) están
dispensados de designarlo (Res. CD/ANPD 2/2022), pero deben ofrecer un canal de
comunicación con el titular. Los requisitos del encarregado (identidad y contacto
publicados de forma clara en el sitio) están en la Res. CD/ANPD 18/2024.

Funciones del Encarregado (Art. 41.2):
- Aceitar reclamações e comunicações dos titulares
- Prestar esclarecimentos e adotar providências
- Receber comunicações da ANPD e adotar providências
- Orientar os funcionários do controlador sobre LGPD
- Executar demais atribuições determinadas pelo controlador o por normas complementares

Verificar:
- [ ] El aviso identifica al Encarregado de Dados
- [ ] Nombre o cargo del Encarregado publicado (Art. 41.1)
- [ ] Dirección de **email** del Encarregado publicada (obligatorio — es el canal principal)
- [ ] Si no existe Encarregado: issue crítico, salvo agente de pequeño porte sin
      tratamiento de alto riesgo (Res. 2/2022), que solo necesita un canal de contacto

---

## Paso 4 — Score global

```
Score = suma de puntos obtenidos / 100
```

| Rango | Interpretación |
|-------|---------------|
| 80–100 | Postura defensible — cumplimento sustancial |
| 60–79 | Risco moderado |
| 40–59 | Risco alto |
| 0–39 | Risco crítico |

---

## Paso 5 — Clasificação de issues e sanções (Art. 52)

La LGPD establece un sistema de sanciones administrativas (Art. 52):

| Sanción | Detalle |
|---------|---------|
| **Advertência** | Con indicación de plazo para medidas correctivas |
| **Multa simples** | Hasta 2% de la facturación de la persona jurídica en Brasil (excluidos impuestos), limitado a **R$ 50.000.000** por infracción |
| **Multa diária** | Hasta el mismo límite total |
| **Publicização** | Divulgación pública de la infracción |
| **Bloqueio dos dados** | Bloqueo de los datos hasta regularización |
| **Eliminação dos dados** | Eliminación de los datos personales |
| **Suspensão** | Suspensión parcial del banco de datos por hasta 6 meses |
| **Proibição** | Prohibición parcial o total de actividades de tratamiento |

La multa simple llega hasta el **2 % de la facturación** del grupo en Brasil en el último
ejercicio, con un **tope de R$ 50.000.000 por infracción** (Art. 52.II). El cálculo y la
clasificación de infracciones (leves, medias y graves) siguen el reglamento de dosimetría,
Res. CD/ANPD 4/2023.

**Críticos** (bloquean cumplimento mínimo):
- Aviso de privacidade inexistente → Art. 9
- Sin Encarregado de Dados designado → Art. 41 (salvo pequeño porte, Res. 2/2022)
- Sin base legal para ninguna finalidade → Art. 7
- Dados sensíveis sin consentimento específico ni otra base del Art. 11 → Art. 11
- Sin mecanismo de exercício de direitos → Art. 18
- Sin HTTPS → Art. 46

**Medios** (plazo recomendado 30–60 días):
- Cookies de publicidad o perfilado sin consentimento previo ni otra base declarada → Art. 7 + Guía de cookies ANPD
- Aviso existe pero falta base legal por finalidade → Art. 7
- Direitos mencionados sin canal ni plazo de atendimento → Art. 18
- Transferências internacionais no declaradas → Art. 33
- Banner de cookies solo informativo → Art. 7.I
- Marketing sin mecanismo de descadastramento → Art. 18
- RIPD probable pero no mencionado → Art. 38

**Bajos:**
- Data de atualização ausente en el aviso
- Aviso sin enlace desde formulários secundarios
- Prazos de retenção no especificados para algún tipo de dado

---

## Paso 6 — Output según modo

### Modo interno (Markdown)

```markdown
# Auditoria LGPD — [domínio]
Data: [data] | Setor: [setor] | Score: [X/100]

## Stack tecnológico
[usar resultados del Paso 0 compartido]

## Resumo
[postura geral, issues críticos, risco sancionatório estimado em BRL]

## Tabela de conformidade
| Bloco | Peso | Pts | Status | Evidência |
...

## Issues críticos / médios / baixos
...

## Notas metodológicas
- Verificado externamente
- Pendiente de acceso al backend
- Nota: lista de países com adequação da ANPD y normativa de transferências
  internacionales pueden estar en actualización — verificar em gov.br/anpd
```

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_lgpd_[fecha].md`.

### Modo cliente (`--docx`)

Misma estructura que `rgpd` modo `--docx`, adaptada a LGPD:
- Autoridad: ANPD
- Multas en BRL
- Terminología en portugués de Brasil
- Pie de página: "Desenvolvido por Zythos Media — Especialistas em SEO & IA Search"
  con hipervínculo a https://zythos.media

Guardar en `<directorio-de-auditorias>/[cliente]/auditoria_lgpd_[fecha].docx`.

---

## Notas de alcance

Mismas limitaciones que el skill `rgpd`: solo auditable externamente.
Adicional LGPD: el Relatório de Impacto (RIPD) es un documento interno.

## Atualização normativa

- **LGPD** (Lei 13.709/2018): en vigor septiembre 2020; sanciones desde agosto 2021.
- **ANPD**: Agência Nacional de Proteção de Dados desde la Lei 15.352 (25/02/2026).
- **Transferências internacionais**: Res. 19/2024; cláusulas modelo obligatorias desde el
  23/08/2025.
- **Adequação**: UE y EEE (Res. 32/2026); la UE reconoció a Brasil el 26/01/2026.
- **Incidentes**: 3 días hábiles (Res. 15/2024). **Encarregado**: Res. 18/2024, con
  dispensa para pequeño porte (Res. 2/2022).
- **ECA Digital** (Lei 15.211/2025): en vigor desde el 17/03/2026.
- **Versão desta skill:** 1.1.0 (2026-11-20). Revisada contra planalto.gov.br y gov.br/anpd
  el 20/11/2026.
