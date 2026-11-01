# Severidad, confianza, evidencia y límites del evaluador único

## Escala de severidad (Nielsen 0-4)

Adaptado de Nielsen, "Severity Ratings for Usability Problems"
(https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/, 01/11/1994). Nivel Guía.
Las etiquetas y significados de la tabla son una adaptación propia de la escala original de 0 a 4.

| Valor | Etiqueta para el informe | Significado |
|---|---|---|
| 4 | **Crítica** | Impide completar la tarea o causa pérdida de datos o de dinero en un flujo de conversión |
| 3 | **Alta** | Problema mayor: muchas personas fallan, dudan o se equivocan en un camino principal |
| 2 | **Media** | Problema menor o problema principal que cuesta tiempo y no éxito |
| 1 | **Baja** | Cosmético: se arregla si hay tiempo |
| 0 | (se descarta) | En la revisión se concluye que no es un problema |

Factores (Nielsen): frecuencia, impacto, persistencia e impacto de mercado.

**Regla de combinación** (síntesis propia, nivel Práctica):
- Frecuencia: 1 = una página o un caso raro, 2 = una plantilla o un flujo, 3 = todo el sitio o el
  flujo de conversión.
- Impacto: 1 = demora, 2 = error recuperable con esfuerzo, 3 = bloquea la tarea o pierde datos o dinero.
- Impacto 3 en un flujo de conversión (formulario de lead, carro, checkout, registro) **con frecuencia 2 o
  3** (afecta a quien recorre el flujo, no a un caso raro) = **4**.
- Impacto 3 en un caso raro o fuera de conversión, o impacto 2 con frecuencia 3 = **3**.
- Impacto 2 local = **2**. Impacto 1 = **1**.
- La persistencia sube como máximo un nivel. El impacto de mercado (daña la confianza o la marca aunque
  sea fácil de sortear) también puede subir un nivel. Se escribe en una línea por qué se asignó la nota.
- Un fallo que solo aparece porque la prueba lo provocó (red bloqueada) es un caso raro mientras no haya
  datos de que ocurre en la realidad.

## Tipo de hallazgo

Adaptado de paulunemoon/ux-audit-skill (MIT).
- **Defecto**: rompe, confunde o bloquea. Se afirma.
- **Oportunidad**: funciona, pero podría funcionar mejor. Se dice así.
- **Gusto**: personas razonables opinan distinto. Se rotula "gusto" y **nunca** se clasifica como 3 o 4.

Las restricciones deliberadas se respetan: un formulario largo por exigencia regulatoria o una pantalla
densa para usuarios expertos. Se evalúa cómo está resuelto el compromiso, no que exista.

## Confianza, siempre con la fuente

| Nivel | Cuándo |
|---|---|
| **Alta** | Reproducible en el sitio en vivo, con captura, y apoyado en una guía externa o en datos (GA4, grabaciones) |
| **Media** | Reproducible con captura, apoyado solo en la heurística |
| **Baja** | Hipótesis: deducido de un diseño estático o de una descripción. Se redacta como pregunta y pide validación |

Fuentes: `(sitio en vivo, escritorio)`, `(sitio en vivo, móvil 390 px)`, `(Figma, frame X)`,
`(captura del cliente)`, `(medido, ui_medicion)`, `(GA4)`. En un diseño de Figma, lo que el diseño
muestra es Alta como intención de diseño, y su comportamiento en ejecución es Baja.

## Ficha mínima de evidencia por hallazgo

Basada en NN/g, "UX Expert Reviews" (https://www.nngroup.com/articles/ux-expert-reviews/, 25/02/2018).

| Campo | Contenido |
|---|---|
| ID y título | `UX-NN`. El título describe el problema, no la solución |
| Ubicación | URL exacta o frame de Figma con enlace, vista (escritorio o móvil y ancho), estado |
| Pasos | Secuencia numerada desde una URL de entrada, con los datos ficticios usados |
| Evidencia | Captura anotada (`anotar_capturas.py`). **Sin captura, el hallazgo no entra al documento** |
| Heurística | H1 a H10 y, si aplica, guía externa con URL (Baymard pública, GOV.UK, NN/g) |
| Tarea afectada | Lead, búsqueda, ficha, carro, checkout o registro, y cómo (demora, error, abandono). Dato de analítica si existe |
| Severidad | 1 a 4, con frecuencia, impacto y persistencia en una línea |
| Tipo | Defecto, Oportunidad o Gusto |
| Recomendación | Comportamiento esperado y verificable, o "requiere test con usuarios" si no hay certeza |
| Prueba de aceptación | Cómo se comprueba que quedó resuelto (por ejemplo, repetir `estados_formulario.py` y que desaparezca la señal) |
| Confianza | Alta, Media o Baja, con su fuente |

Filtro antes del documento: se descarta lo que no tiene captura, pasos o heurística. Lo estético sin
tarea afectada pasa a "observación de gusto". Lo que es de otra disciplina se deriva
(`salida-y-derivaciones.md`). La severidad se revisa en una segunda pasada, idealmente al día siguiente.

## El límite del evaluador único

- En seis proyectos, un evaluador solo encontró en promedio **el 35%** de los problemas. Nielsen
  recomienda unos cinco evaluadores y nunca menos de tres
  (https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/,
  1994, Investigación).
- Un evaluador encontró el 42% de los problemas mayores y el 32% de los menores. La heurística y el
  test con usuarios encuentran conjuntos distintos (Nielsen, 1995, Investigación).
- Cuando evalúa un modelo de IA el riesgo es otro: hallazgos plausibles que no se reproducen. Un estudio
  de 2025 con GPT-4o como evaluador reportó 27 falsos positivos (https://arxiv.org/pdf/2506.16345,
  preprint). Por eso esta skill exige la captura y la reproducción de cada hallazgo, y los scripts
  devuelven señales a confirmar, no conclusiones.

**Mitigación obligatoria:**
1. Varias pasadas separadas: exploración, una pasada por heurística, una por tarea y una por dispositivo.
2. Recorrido por tareas con las cuatro preguntas del recorrido cognitivo (`flujos-y-formularios.md`).
3. Cambio de persona: comprador B2B que compara, usuario técnico y comprador apurado en móvil.
4. Apoyo externo de cada hallazgo de severidad 3 o 4 en una guía o en datos.
5. Datos de comportamiento si existen: embudo de GA4 (`ga4-analysis`), búsquedas internas, grabaciones.
6. Segunda revisión de la severidad con un revisor a ciegas para los 3 y 4: un subagente en contexto
   nuevo que solo ve las capturas y la descripción, sin la severidad propuesta.
7. Declarar en el informe que es la evaluación de un solo experto y recomendar test con usuarios para
   los hallazgos críticos.
