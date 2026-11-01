# Severidad, confianza, formato del hallazgo y del informe

Adaptado con atribución de dos fuentes MIT: el esquema de severidad por categorías de
`Community-Access/accessibility-agents` (`kb-web-severity-scoring`) y la regla de evidencia con fuente
nombrada de `paulunemoon/ux-audit-skill`. **Sin puntaje compuesto de 0 a 100**: una nota global sugiere
una medición que no existe y se confunde con conformidad.

## Severidad (la propone consolidar.py, la decide quien audita)

| Severidad | Qué significa | Ejemplos típicos |
|---|---|---|
| **Crítica** | Una persona no puede completar una tarea principal o queda atrapada | Trampa de teclado, campo obligatorio sin etiqueta, botón de envío sin nombre, error que solo se indica con color, CAPTCHA sin alternativa |
| **Grave** | La tarea se puede completar, pero con dificultad seria en un camino principal | Foco invisible en el menú o el formulario, contraste insuficiente en texto principal, foco tapado por el banner de cookies, foco que entra en un diálogo cerrado, error no asociado al campo |
| **Moderada** | Dificultad en caminos secundarios o un problema que cuesta tiempo, no éxito | Orden de foco extraño en el pie, varios h1, enlace a pestaña nueva sin aviso, autocomplete ausente |
| **Menor** | Pulido. Nadie abandona por esto | Title redundante, alt no vacío en imagen decorativa, falta de enlace de salto con regiones bien hechas |

Ajustes:
- **El camino pesa.** El mismo fallo sube un nivel en el formulario de contacto, el carro o el checkout
  y baja uno en una página que casi nadie visita. Se dice en el hallazgo por qué se ajustó.
- **La frecuencia pesa.** Un problema sistémico (en todas las plantillas) se prioriza sobre uno puntual
  de igual severidad: se arregla una vez y se resuelve en todo el sitio.
- El impacto de axe (`critical`, `serious`, `moderate`, `minor`) es el punto de partida, no la decisión.

## Confianza (siempre con la fuente entre paréntesis)

| Nivel | Cuándo |
|---|---|
| **Alta** | Lo detectó axe sobre el renderizado, o un atributo del DOM, o se confirmó a mano (teclado, lector) |
| **Media** | Lo detectó un script propio por medición (píxeles, puntos tapados, desbordes) y no se confirmó aún |
| **Baja** | Candidato que depende del contexto (orden de foco, texto truncado, cursor de mano sin foco) |

Fuentes válidas: `(axe, renderizado)`, `(medido, píxeles)`, `(manual, teclado)`, `(manual, NVDA)`,
`(árbol de accesibilidad)`, `(código fuente)`. Nunca se usa una palabra más fuerte que la que se ganó.
Un candidato de confianza Baja no va al informe de cliente sin confirmarlo; queda en "a confirmar".

## Patrón

`consolidar.py` lo calcula sobre las páginas auditadas:
- **Sistémico**: aparece en todas las páginas, normalmente en la cabecera, el menú, el pie, las cookies o
  el chat. Un arreglo lo resuelve en todo el sitio.
- **Plantilla**: aparece en varias páginas del mismo tipo. Se arregla el componente.
- **Página**: es propio de una página.

## Esquema de cada hallazgo

```
ID            A11Y-NN (estable entre revisiones)
Criterio      número y nombre WCAG 2.2, nivel (p. ej. 2.4.11 Foco no oculto (mínimo), AA)
Severidad     Crítica | Grave | Moderada | Menor (+ motivo si se ajustó)
Confianza     Alta | Media | Baja (fuente)
Patrón        Sistémico | Plantilla | Página, con las páginas y vistas
Evidencia     lo que se vio: selector, texto del elemento, captura, paso de Tab, nodo de axe
A quién afecta  la consecuencia para la persona, no la cita del criterio
Recomendación el comportamiento esperado, no el código
Prueba de aceptación  cómo se verifica que quedó resuelto (repetible, con la herramienta)
```

"A quién afecta" se escribe desde la persona: "Quien navega con teclado llega al botón Conocer más y
no lo ve, porque el banner de cookies lo tapa", no "incumple 2.4.11".

**Recomendación sobre código ajeno:** describir el comportamiento esperado y la prueba de aceptación,
no dictar la implementación deducida de JavaScript minificado. La forma de implementarlo la decide
Desarrollo. Ejemplo de prueba de aceptación: "Con el banner de cookies visible, al recorrer la portada
con Tab ningún elemento enfocado queda totalmente oculto (teclado_foco.py sin entradas en
foco_tapado_completo)".

## Estructura del informe

1. **Alcance y método**: páginas y plantillas, estados (menú, diálogo, formulario con error, móvil),
   herramientas y versiones (axe 4.14.0, Playwright), si hubo lector de pantalla real y cuál, y qué
   quedó fuera.
2. **Resumen**: 3 a 5 frases sobre qué impide hoy usar el sitio, a quién, y qué conviene resolver
   primero.
3. **Hallazgos priorizados**: primero los sistémicos y los del camino de conversión.
4. **Cobertura por criterio**: la tabla de 55 criterios con su estado. Nunca "cumple". Lo más que se
   puede decir es "sin hallazgos en la muestra revisada, con prueba manual completa".
5. **Contexto legal**: solo los mercados donde opera el sitio, con fecha y nivel (`marco-legal.md`).
6. **Qué está bien**: breve y concreto, para calibrar.
7. **Pendientes**: lo que requiere lector de pantalla, acceso o una decisión del cliente.

Uso interno o cliente: si no está dicho, se pregunta. La versión para cliente omite selectores y
nombres de reglas y deja la evidencia en un anexo.

## Entrega en el formato del cliente

Si el cliente tiene su propia skill o plantilla de entrega (documento de corrección para Desarrollo,
ticket, informe), el documento final se redacta con ella y esta skill aporta los hallazgos confirmados con
su evidencia y sus pruebas de aceptación. El anexo privado `casos-privados.md`, si existe, dice cuál
corresponde a cada cliente.

Si el formato pide un apartado de impacto en SEO, se escribe con honestidad: la accesibilidad no es un
factor de ranking. Lo que se gana es que más personas completen el formulario o la compra, que los
agentes de IA que leen el árbol de accesibilidad entiendan los controles, y que el title, los
encabezados y los alt, que Google sí lee, queden correctos.

Cuando el diseño visual lo define otro equipo (contraste de la marca, tamaños, disposición), se reporta
la observación con medidas y capturas y se deja la solución a ese equipo, salvo que se pida una
propuesta.

## Seguimiento entre auditorías

Se compara con la revisión anterior por ID y criterio y cada hallazgo se marca como Resuelto, Nuevo,
Persiste o Empeoró (sube de severidad). Las pruebas de aceptación de cada hallazgo son el guion de la
reverificación.
