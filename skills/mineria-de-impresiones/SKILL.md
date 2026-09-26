---
name: mineria-de-impresiones
description: Convierte datos de Google Search Console en un plan de mejora de contenido accionable. Usa este skill cuando el usuario pida "mejorar contenido con GSC", "minería de impresiones", "optimizar página con Search Console", "clasificar queries", "qué contenido crear según mis datos", "mejorar CTR", "optimizar títulos y metas", o cualquier tarea que use datos de GSC para decidir qué mejorar, qué crear y cómo optimizar contenido. También actívalo con "grupos de queries", "brecha de contenido con GSC", "expandir contenido", "queries con impresiones sin clics", o plan editorial basado en Search Console. Se diferencia de gsc-opportunities (diagnostica QUÉ queries trabajar) porque aquí el foco es CÓMO mejorar contenido, QUÉ crear y CÓMO optimizar títulos/metas clasificando queries por intención. SIEMPRE pide los datos de GSC antes de analizar. NUNCA analices sin datos reales.
---

# Minería de impresiones

Skill para transformar datos reales de Google Search Console en un plan de acción concreto: qué mejorar en la página actual, qué contenido nuevo crear y cómo optimizar títulos y metas para ganar más clics.

## Regla inquebrantable

**SIEMPRE pedir los datos de GSC antes de hacer cualquier cosa.**

Este skill NO funciona sin datos reales. No asumas, no inventes, no especules. Si el usuario activa este skill sin proporcionar datos, el primer paso obligatorio es pedirlos.

### Solicitud de datos (OBLIGATORIA en cada ejecución)

Antes de cualquier análisis, solicitar al usuario:

**Datos mínimos requeridos:**

| Dato | Por qué es necesario |
|------|---------------------|
| URL de la página a analizar | Para entender el contexto y la intención principal |
| Queries asociadas a esa URL | Las keywords que Google ya asocia con la página |
| Clics por query | El tráfico real que entra |
| Impresiones por query | El mercado potencial visible |
| CTR por query | Qué tan atractivo es el resultado |
| Posición promedio por query | Dónde aparece en las SERPs |

**Datos opcionales que enriquecen el análisis:**

| Dato | Valor añadido |
|------|--------------|
| Título actual de la página | Para evaluar si necesita reescritura |
| Meta descripción actual | Para comparar con las queries reales |
| Dispositivo (móvil/escritorio) | El CTR varía mucho entre dispositivos |
| País | Para contextualizar volúmenes y competencia |
| Período de los datos | Para interpretar correctamente (ver sección de contexto de datos) |

**Cómo pedirlo:**

Usar un mensaje directo y claro, tipo:

> Para hacer el análisis de minería de impresiones necesito los datos de Search Console de esa página. Puedes compartirlos de cualquier forma:
>
> - CSV exportado desde GSC (Rendimiento > Filtrar por página > Exportar)
> - Tabla copiada y pegada
> - Captura de pantalla del panel
> - Datos escritos directamente
>
> Lo mínimo que necesito: las queries con sus clics, impresiones, CTR y posición promedio. Si también tienes el título y meta descripción actuales de la página, mejor todavía.

**Si el usuario insiste en que analices sin datos:** Explicar que el valor de este método está precisamente en trabajar con datos reales, no con suposiciones. Ofrecer alternativas como exportar desde GSC o usar la API.

## Filosofía de la minería de impresiones

Cada impresión en Search Console representa una oportunidad donde Google ya asocia tu contenido con una búsqueda real. El trabajo no es adivinar qué keywords perseguir, sino entender qué está pasando con las que Google ya te muestra y decidir inteligentemente qué hacer con cada una.

El error más común: meter todas las queries en una sola página sin distinguir intención. Eso diluye la relevancia y confunde tanto a Google como al usuario.

## Flujo de trabajo completo

### PASO 1: Validar y contextualizar los datos

Antes de clasificar queries, evaluar la calidad de los datos recibidos.

**Verificaciones obligatorias:**

1. **Período de los datos:** Preguntar de qué fechas son los datos si no se especifica. Consultar `references/contexto-datos-gsc.md` para advertencias sobre períodos afectados por el error de registro de impresiones (mayo 2025 - abril 2026).

2. **Volumen mínimo:** Filtrar ruido. Queries con menos de 10 impresiones en el período analizado rara vez aportan información accionable (excepto en sitios muy nuevos o nichos ultra-específicos).

   **Si TODA la muestra está por debajo de 10 impresiones:** No abandonar el análisis. Cambiar de enfoque:
   - Bajar el umbral a 3 impresiones para detectar señales tempranas
   - Priorizar queries con al menos 1 clic (señal de relevancia confirmada por humano)
   - Trabajar con métricas relativas dentro del dataset, no con benchmarks absolutos
   - Avisar al usuario que las recomendaciones son hipótesis a validar, no conclusiones
   - Sugerir ampliar el período de datos (6 o 12 meses en vez de 3) si está disponible
   - Para sitios muy nuevos: priorizar Grupos B y C (crear contenido) sobre Grupo A (optimizar lo existente), porque el problema suele ser cobertura temática, no CTR

3. **Calcular líneas base del sitio:**
   - CTR promedio de la página: `(Total clics / Total impresiones) * 100`
   - Posición promedio ponderada
   - Estos valores son el punto de referencia para todo el análisis

4. **Detectar anomalías:**
   - CTR inusualmente bajo en posiciones top 3 → probable AI Overview o fragmento destacado robando clics
   - Impresiones altísimas con 0 clics → verificar si la posición es >30 (normal) o <10 (problema de snippet)
   - Queries con CTR mucho mayor al promedio → investigar por qué funcionan (aprender de los ganadores)

### PASO 2: Identificar queries de alta oportunidad

De todas las queries, extraer las que tienen mayor potencial de mejora:

**Criterios de oportunidad:**

| Señal | Qué indica |
|-------|-----------|
| Impresiones altas + CTR bajo (<3%) | Google te muestra pero nadie hace clic |
| Posición 5-20 | Zona donde pequeñas mejoras mueven la aguja |
| Impresiones altas + posición 11-20 | A un empujón de primera página |
| CTR muy por debajo del referente de esa posición | El snippet no está funcionando |

**Referentes de CTR por posición (2026):**

Consultar `references/referentes-ctr-2026.md` para datos actualizados. Tener en cuenta que estos referentes han cambiado significativamente con la expansión de AI Overviews.

Referencia rápida (SERPs sin AI Overview):
- Posición 1: ~28-34%
- Posición 2: ~15-18%
- Posición 3: ~10-12%
- Posiciones 4-6: ~5-8%
- Posiciones 7-10: ~2-4%

Con AI Overview presente, estos números pueden caer un 50% o más en la posición 1.

**Ojo:** No existe un "CTR universal correcto". Depende del tipo de query, las características de la SERP, el dispositivo y si hay AI Overview. Siempre usar el CTR promedio del propio sitio como referencia principal.

### PASO 3: Clasificación de queries en 3 Grupos

Este es el paso más importante del análisis. Cada query se clasifica según su relación con la intención principal de la página.

#### Grupo A: Fortalecer en la página actual

**Criterio:** La query es directamente relevante para la intención principal de la página.

**Señales para clasificar como Grupo A:**
- La query describe exactamente lo que la página trata
- Variaciones de la keyword principal (sinónimos, cola larga)
- Preguntas que la página debería responder naturalmente
- Subtemas que encajan orgánicamente en el contenido existente

**Ejemplo:** Si la página es sobre "cómo elegir hosting web", queries como "mejor hosting para WordPress", "hosting barato confiable", "qué buscar en un hosting" son Grupo A.

#### Grupo B: Contenido de soporte

**Criterio:** La query está relacionada pero no encaja completamente en la página actual. Necesita su propia sección robusta o un artículo de soporte enlazado.

**Señales para clasificar como Grupo B:**
- Comparte tema pero la intención es parcialmente diferente
- Respondería mejor con profundidad que la página actual no puede darle sin desviarse
- Subtemas que merecen desarrollo propio pero mantienen relación temática

**Ejemplo:** Si la página es sobre "cómo elegir hosting web", queries como "migrar hosting sin perder SEO" o "hosting vs servidor dedicado diferencias" son Grupo B.

#### Grupo C: Artículo independiente

**Criterio:** La intención de búsqueda es claramente diferente. Forzar esta query en la página actual diluiría la relevancia.

**Señales para clasificar como Grupo C:**
- Intención de búsqueda diferente (informacional vs transaccional, por ejemplo)
- El usuario busca algo que merece una página completa propia
- Incluirlo en la página actual crearía confusión de intención
- Potencial suficiente para posicionar de forma independiente

**Ejemplo:** Si la página es sobre "cómo elegir hosting web", queries como "cómo instalar WordPress paso a paso" o "qué es un CDN" son Grupo C.

#### Regla de desempate (cuando una query podría ser A o B, o B o C)

Cuando una query encaja en dos grupos, aplicar este criterio en orden:

1. **Pregunta de cobertura:** ¿La página actual puede responder esta query en máximo 2-3 párrafos sin desviar la intención principal? Si sí → Grupo A. Si requiere más extensión → Grupo B o C.

2. **Pregunta de intención:** ¿La intención de búsqueda de la query es la misma que la intención principal de la página (informacional, comercial, transaccional, navegacional)? Si sí → Grupo A o B. Si es diferente → Grupo C.

3. **Pregunta de canibalización:** ¿Si creo un artículo separado para esta query, competiría con la página actual por la misma búsqueda? Si sí → Grupo A (fortalecer, no dividir). Si no → Grupo B o C según las dos preguntas anteriores.

4. **Tie-break final A vs B:** Si después de los 3 pasos sigue empatada entre A y B, ganar Grupo A. Forzar contenido nuevo cuando se puede fortalecer lo existente es esfuerzo desperdiciado.

5. **Tie-break final B vs C:** Si sigue empatada entre B y C, ganar Grupo B. Mantener cohesión temática del clúster es mejor que dispersión.

Estas reglas garantizan consistencia entre ejecuciones del mismo análisis.

#### Cómo presentar la clasificación

Tabla clara con cada query y su grupo asignado:

```
| Query | Clics | Impr | CTR | Pos | Grupo | Razón |
|-------|-------|------|-----|-----|-------|-------|
| [query] | X | X | X% | X | A/B/C | [explicación breve] |
```

Ordenar por impresiones (descendente) dentro de cada grupo para priorizar.

### PASO 4: Plan de optimización de contenido (Grupo A)

Para las queries clasificadas como Grupo A, generar recomendaciones concretas:

**4.1 Estructura de contenido**

Analizar las queries del Grupo A y sugerir:

- **Nuevos H2/H3** que respondan directamente a las queries detectadas
- **Subtemas faltantes** que las queries revelan como brechas de contenido
- **Preguntas frecuentes** extraídas directamente de las queries tipo pregunta (5-10 preguntas)
- **Comparaciones o casos de uso** si las queries los sugieren

**Reglas para las sugerencias:**
- Cada encabezado sugerido debe mapear a queries reales del conjunto de datos
- No sugerir secciones genéricas que no tengan respaldo en los datos
- Priorizar por volumen de impresiones de las queries asociadas
- Mantener coherencia con la intención principal de la página

**4.2 Mejora de profundidad temática**

- Identificar ángulos que las queries revelan pero el contenido actual probablemente no cubre
- Sugerir datos, ejemplos o evidencia que enriquecerían las secciones
- Recomendar elementos de E-E-A-T: experiencia demostrable, datos propios, opinión experta

**Foco:** Contenido útil para personas, no relleno para bots. Si una sección no aporta valor real al lector, no sugerirla.

### PASO 5: Plan de expansión de contenido (Grupos B y C)

#### Para queries del Grupo B:

Dos opciones según el caso:

**Opción 1: Sección de soporte dentro de la página**
- Si la query puede responderse en 200-400 palabras sin desviar la intención principal
- Sugerir ubicación dentro de la estructura existente
- Indicar cómo enlazar internamente

**Opción 2: Artículo de soporte independiente**
- Si la query necesita desarrollo propio para satisfacer la intención
- Para cada artículo sugerido, entregar:

```
Título sugerido: [título optimizado]
Keyword objetivo: [la query o variación optimizada]
Intención de búsqueda: [informacional / comercial / transaccional / navegacional]
Relación con página principal: [cómo se conectan temáticamente]
Enlace interno sugerido: [desde dónde y hacia dónde enlazar, con texto ancla]
```

#### Para queries del Grupo C:

Artículos completamente nuevos. Para cada uno:

```
Título sugerido: [título optimizado]
Keyword objetivo: [la query principal]
Intención de búsqueda: [tipo de intención]
Formato recomendado: [guía, comparativa, tutorial, listado, etc.]
Enlace interno: [cómo conectar con la página original y el clúster]
Prioridad: [alta/media/baja basada en impresiones y potencial]
```

**Importante:** Ordenar los artículos sugeridos por prioridad (impresiones × potencial de CTR estimado).

#### Filtro de rentabilidad editorial (cuántos artículos del Grupo C ejecutar)

Cuando el análisis genera muchos artículos sugeridos para Grupo C (5 o más), aplicar este filtro para definir cuántos vale la pena producir.

Calcular para cada artículo sugerido un **Score de Rentabilidad** con 3 componentes:

**1. Potencial de tráfico (40% del score):**
- Suma de impresiones de la query principal + queries relacionadas del Grupo C
- Multiplicar por CTR esperado según posición objetivo (consultar `references/referentes-ctr-2026.md`)
- Resultado: visitas mensuales estimadas

**2. Dificultad de posicionamiento (30% del score, inversa):**
- Posición actual de la query (si ya aparece): más cercano a 1 = más fácil
- Si no aparece: estimar competencia del nicho (alta/media/baja)
- Penalizar queries con SERP saturada de AI Overviews, anuncios o features dominantes
- Penalizar queries dominadas por sitios con autoridad muy superior

**3. Esfuerzo de producción (30% del score, inversa):**
- Artículos cortos (800-1.200 palabras): esfuerzo bajo
- Artículos medios (1.500-2.500 palabras): esfuerzo medio
- Guías largas (>3.000 palabras): esfuerzo alto
- Artículos que requieren investigación primaria, herramientas o datos propios: esfuerzo muy alto

**Clasificación final por score:**

| Score | Recomendación |
|-------|---------------|
| Top 20% del listado | EJECUTAR YA (alta rentabilidad, prioridad inmediata) |
| 20% siguiente | EJECUTAR EN 60-90 DÍAS (segunda ola) |
| 40% medio | EVALUAR según capacidad del equipo (no urgente) |
| 20% inferior | DESCARTAR o postergar 6+ meses (baja rentabilidad) |

**Regla práctica:** Si el listado tiene 12 artículos sugeridos, ejecutar 2-3 ya, 2-3 en el siguiente trimestre, y considerar el resto como banco de ideas para más adelante.

**Avisar al usuario** del score con explicación breve de por qué cada artículo cae en su tramo. No entregar 12 ideas sin priorización clara.

### PASO 6: Optimización de CTR (Títulos y meta descripciones)

Esta es la parte con mayor impacto inmediato para queries del Grupo A en buenas posiciones.

**6.1 Reescritura de títulos (3-5 variaciones)**

Reglas para los títulos sugeridos:
- Basados en las queries reales del conjunto de datos (usar el lenguaje del usuario)
- 55-60 caracteres máximo (para evitar truncamiento)
- Incluir la keyword objetivo naturalmente
- Técnicas de atracción aplicables:
  - Números específicos ("7 criterios", "en 2026")
  - Palabras de poder (sin exagerar): guía, paso a paso, comparativa, errores
  - Coincidencia de intención clara (que el título prometa lo que el contenido entrega)
  - Curiosidad genuina (no anzuelo vacío)

**6.2 Reescritura de meta descripciones (2-3 variaciones)**

Reglas para las meta descripciones:
- 150-155 caracteres máximo
- Incluir keyword objetivo en los primeros 100 caracteres
- Describir el beneficio concreto de hacer clic
- Incluir diferenciador frente a la competencia si es posible
- Llamada a la acción sutil cuando aplique

**6.3 Análisis de características de la SERP**

Si es posible inferir de los datos (CTR anormalmente bajo en posición 1-3):
- Advertir sobre probable AI Overview o fragmento destacado
- Sugerir optimización para datos estructurados (schema)
- Recomendar formato de contenido que compita por el fragmento destacado (listas, tablas, definiciones directas)

### PASO 7: Arquitectura de clúster y enlazado interno

Conectar todo el trabajo de los pasos anteriores en una arquitectura de clúster coherente. El enlazado interno no son sugerencias sueltas: es la implementación física del clúster temático que se construyó en los pasos 3, 4 y 5.

**7.1 Construir el mapa del clúster antes de proponer enlaces**

Antes de generar textos ancla, dibujar mentalmente el clúster resultante:

- **Página pilar:** La página analizada (cubre el tema central, fortalecida con queries del Grupo A)
- **Páginas de soporte (Grupo B):** Cada una responde una intención específica relacionada
- **Páginas satélite (Grupo C):** Temas diferentes pero del mismo universo temático
- **Páginas externas relevantes del sitio:** Contenido ya existente que también encaja en este clúster

**Reglas del clúster:**
- La página pilar enlaza hacia TODAS las páginas de soporte (Grupo B)
- Cada página de soporte (Grupo B) enlaza de vuelta a la pilar Y a 1-2 páginas de soporte hermanas
- Las páginas satélite (Grupo C) enlazan a la pilar (mención contextual) pero no requieren enlace recíproco si la intención difiere mucho
- Evitar enlazado desde la pilar a páginas satélite si compiten por la misma intención de búsqueda

**7.2 Generar textos ancla anclados al mapa del clúster**

Para cada enlace propuesto, entregar:

```
Origen: [URL o sección específica que enlaza]
Destino: [URL del artículo del Grupo B o C]
Texto ancla sugerido: [3 variaciones]
Justificación: [por qué este enlace fortalece el clúster, basado en qué query]
Ubicación en el contenido: [párrafo o sección concreta donde insertar]
```

**Tipos de textos ancla según función en el clúster:**

| Tipo | Cuándo usar | Ejemplo |
|------|------------|---------|
| Coincidencia exacta | Solo desde la página pilar hacia 1 página de soporte clave | "guía de migración de hosting" |
| Coincidencia parcial | La opción más usada (80% de los enlaces) | "cómo migrar tu hosting sin perder tráfico" |
| Contextual / frase natural | Para enlaces dentro de párrafos narrativos | "este aspecto lo cubrimos en detalle al hablar sobre [tema]" |
| Pregunta directa | Para enlaces desde secciones de preguntas frecuentes | "¿Y si quiero cambiar de hosting más adelante?" |

**Reglas de aplicación:**
- Cada texto ancla debe sonar natural dentro de su párrafo de origen
- No repetir el mismo texto ancla en múltiples enlaces hacia la misma URL desde la misma página
- Mantener proporción: ~70% parcial, ~15% contextual, ~10% pregunta directa, ~5% exacta
- Cada enlace propuesto debe responder a una query real del análisis

**7.3 Visualización del clúster resultante**

Entregar un mapa simple del clúster, tipo árbol:

```
[Página pilar - URL analizada]
  ├── Soporte B1: [título artículo] (cubre queries: X, Y, Z)
  │     └── enlaza de vuelta a pilar + a soporte B2
  ├── Soporte B2: [título artículo] (cubre queries: A, B)
  │     └── enlaza de vuelta a pilar + a soporte B1
  ├── Satélite C1: [título artículo] (intención diferente, mismo universo temático)
  └── Satélite C2: [título artículo]
```

**7.4 Páginas existentes del sitio**

Si el usuario menciona o se infiere que tiene contenido relacionado ya publicado, recomendarle:
- Hacer un inventario de URLs del mismo universo temático
- Revisar oportunidades de enlazar desde esas páginas hacia la pilar y viceversa
- Sugerirle que comparta una lista de URLs relacionadas para ampliar el mapa del clúster

### PASO 8: Entrega del resultado final

Estructurar la entrega así:

```
1. RESUMEN EJECUTIVO CON PRIORIDADES
   - Estado actual de la página (CTR promedio, posición promedio, oportunidad estimada)
   - Hallazgo principal
   - Impacto potencial estimado
   - **Las 3 acciones más rentables a ejecutar esta semana** (basadas en relación impacto/esfuerzo)
   - Plazo estimado para ver resultados de cada una

2. PLAN PRIORIZADO DE ACCIONES (horizonte temporal)
   - **Esta semana (ganancias rápidas):** reescritura de título/meta de la página actual, ajustes menores de contenido
   - **Próximas 4 semanas (mejoras de contenido):** nuevas secciones, preguntas frecuentes, profundización del Grupo A
   - **Próximos 90 días (contenido nuevo):** artículos del Grupo C top 20% según filtro de rentabilidad editorial
   - **Banco de ideas (sin fecha):** resto del Grupo C para evaluar más adelante

3. TABLA DE CLASIFICACIÓN DE QUERIES
   - Todas las queries clasificadas en Grupo A / B / C con métricas

4. PLAN DE MEJORA DEL CONTENIDO EXISTENTE (Grupo A)
   - Nuevos encabezados sugeridos
   - Subtemas faltantes
   - Preguntas frecuentes recomendadas
   - Mejoras de profundidad

5. PLAN DE CONTENIDO NUEVO (Grupos B y C)
   - Artículos de soporte (Grupo B)
   - Artículos independientes (Grupo C) con score de rentabilidad editorial
   - Cada uno con título, keyword, intención y enlazado

6. OPTIMIZACIÓN DE CTR
   - Títulos sugeridos (3-5)
   - Meta descripciones sugeridas (2-3)
   - Alertas sobre características de la SERP si aplica

7. ARQUITECTURA DE CLÚSTER Y ENLAZADO INTERNO
   - Mapa del clúster resultante
   - Textos ancla por enlace propuesto
   - Ubicación específica de cada enlace
```

## Contexto de datos GSC (2025-2026)

**Leer siempre `references/contexto-datos-gsc.md` antes de interpretar datos.**

Resumen rápido: Google tuvo un error de registro de impresiones desde mayo 2025 hasta abril 2026. Los datos de impresiones de ese período pueden estar inflados. Los clics NO fueron afectados. Además, desde septiembre 2025, Google eliminó el parámetro &num=100, lo que redujo impresiones artificiales generadas por bots y herramientas de seguimiento.

Implicación práctica: Si los datos del usuario son de ese período, advertirlo. Las impresiones pueden estar infladas, el CTR calculado puede ser más bajo de lo real. Usar los clics como métrica más confiable para priorizar.

## Diferencia con otros skills

| Aspecto | mineria-de-impresiones | gsc-opportunities | seo-content-creator |
|---------|-------------------|-------------------|---------------------|
| **Pregunta central** | "¿Cómo mejoro esta página y qué contenido nuevo creo?" | "¿Qué queries trabajo primero?" | "Redáctame un artículo SEO" |
| **Entrada** | Datos GSC de UNA página específica | Datos GSC del sitio completo | Brief + keywords |
| **Salida** | Plan de contenido: mejoras + nuevo contenido + CTR | Diagnóstico priorizado por cuadrantes | Artículo redactado y optimizado |
| **Enfoque** | Prescriptivo (qué hacer y cómo) | Diagnóstico (dónde están las oportunidades) | Ejecución (crear el contenido) |

**Flujo combinado ideal:**
1. `gsc-opportunities` → detecta las páginas con mayor oportunidad
2. `impression-mining` → para cada página prioritaria, genera el plan de acción
3. `seo-content-creator` → ejecuta la creación de artículos nuevos sugeridos
4. `interlinking-builder` → implementa la estrategia de enlaces internos

## Directrices generales

- **NUNCA analizar sin datos reales.** Si no hay datos, pedir. Si los datos son insuficientes, pedir más.
- No sugerir relleno de keywords. La densidad de keywords no es un factor que optimizar.
- Ser específico con las recomendaciones. "Mejorar el contenido" no es accionable. "Agregar una sección H2 sobre [tema específico] que responda a la query [query real con X impresiones]" sí lo es.
- Cada sugerencia debe tener respaldo en los datos proporcionados.
- Priorizar por impacto/esfuerzo: ganancias rápidas primero (optimización de CTR), mejoras de contenido después, contenido nuevo al final.
- Tener en cuenta el impacto de AI Overviews en los referentes de CTR. Consultar `references/referentes-ctr-2026.md`.
- Cuando las impresiones crecen pero los clics no, no asumir automáticamente que es un problema del sitio. Puede ser efecto de AI Overviews satisfaciendo la intención directamente en la SERP.

## Formato de entrega

| Formato | Cuándo usarlo |
|---------|---------------|
| **Análisis conversacional** | Por defecto, respuesta directa en el chat |
| **Documento Word** | Si el usuario pide informe formal (usar skill docx) |
| **Excel** | Si el usuario pide datos para trabajar (usar skill xlsx) |

## Dependencias

Ninguna específica. El análisis se hace con la información proporcionada por el usuario.

Si el usuario pide resultado en Word → usar skill `docx`
Si el usuario pide resultado en Excel → usar skill `xlsx`
Si el usuario pide redactar un artículo sugerido → usar skill `seo-content-creator`
Si el usuario pide implementar el enlazado interno → usar skill `interlinking-builder`

## Créditos

Metodología de minería de impresiones adaptada y enriquecida por Diego González, consultor SEO.
Basada en el marco de "Impression Mining SEO Strategy" con mejoras en clasificación de intención, contexto de datos GSC 2025-2026 y adaptación al ecosistema de AI Overviews.
