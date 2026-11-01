# Estructura del informe, entrega y derivaciones

## Estructura del informe

1. **Alcance y lectura del encargo** (un párrafo): qué se evaluó (sitio, flujo, pantallas o Figma), con
   qué acceso, para qué audiencia (experta, general o mixta) y con qué riesgo (dinero, datos, salud).
   Se declara que es la evaluación de un solo experto.
2. **Resumen** (5 a 8 frases): las tres cosas que más afectan las tareas que importan al negocio.
3. **Ganancias rápidas**: alto impacto y bajo esfuerzo, como lista separable.
4. **Hallazgos por tarea o por flujo** (no por heurística), de mayor a menor severidad, con la ficha de
   `severidad-y-evidencia.md`.
5. **Plan priorizado**: orden de trabajo, no una matriz 2 × 2.
6. **Qué funciona bien, y qué se dejó a propósito**: breve. Lo segundo nombra lo que alguien esperaría ver
   marcado y explica por qué no se marcó.
7. **Preguntas abiertas e hipótesis**: lo que necesita datos o test con usuarios.
8. **Derivaciones**: hallazgos que pertenecen a otra disciplina, con la skill que los toma.

Sin puntaje global de UX ("3,7/5"): implica una medición que no se hizo. Una nota por dimensión del 1 al 5
es opcional, solo en enteros y con una línea de justificación.

Uso interno o cliente: si no está dicho, se pregunta. La versión para cliente no usa jerga (sin
"heurística", sin selectores) y deja la evidencia técnica en un anexo.

## Entrega en el formato del cliente

- Si el cliente tiene su propia skill o plantilla de entrega (documento para Desarrollo, ticket), el
  documento final se redacta con ella y esta skill aporta los hallazgos confirmados, con capturas
  anotadas y pruebas de aceptación. El anexo privado `casos-privados.md`, si existe, dice cuál
  corresponde a cada cliente y qué reglas propias tiene.
- **Impacto en SEO, si el formato lo pide, honesto:** la usabilidad no es un factor directo de ranking. El
  argumento es que el tráfico orgánico que ya llega convierta mejor, que la página responda lo que busca
  quien llega desde Google o un asistente, y que los cambios no rompan lo que hoy posiciona.
- Cuando el diseño lo define otro equipo, se reportan observaciones con medidas y capturas, y la
  solución queda a cargo de ese equipo salvo que se pida una propuesta.
- Antes de describir un hallazgo, se cruza con lo ya reportado al cliente: puede estar pedido o resuelto.

Sin formato propio: informe .md o .docx en la carpeta de trabajo del cliente.

## Derivaciones (dónde termina la heurística)

| Si el hallazgo es… | Va a |
|---|---|
| Contraste, foco, lector de pantalla, objetivo <24 px, etiqueta no asociada | `accesibilidad-wcag` (con su criterio WCAG) |
| "Convence poco", propuesta de valor, prueba A/B | `page-cro`, `form-cro`, `signup-flow-cro`, `seo-conversion` |
| La página no responde a la intención de búsqueda (tipo de página equivocado) | `seo-sxo` |
| Estructura del sitio, menú, URL, enlazado | `site-architecture`, `seo-interlinking` |
| Lentitud o saltos de diseño medidos | `core-web-vitals` |
| ¿Ocurre de verdad? (abandono por paso, errores de formulario en datos) | `ga4-analysis`, `funnel-analysis`, `google-tag-manager` |
| Calidad editorial, profundidad, E-E-A-T | `seo-content` |
| Banner de cookies, consentimiento, aviso de privacidad (lo legal) | `privacidad`, `ley-datos-chile` (aquí solo si bloquea la tarea) |
| Ficha, catálogo, Merchant Center | `seo-ecommerce` |
| Formularios para agentes de IA (WebMCP) | `seo-agentic` |
