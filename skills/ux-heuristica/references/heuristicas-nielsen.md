# Las 10 heurísticas de Nielsen, con qué mirar en un sitio real

Fuente: Jakob Nielsen, "10 Usability Heuristics for User Interface Design"
(https://www.nngroup.com/articles/ten-usability-heuristics/), de 1994, con la redacción vigente de 2020 y
la última revisión de la página del 30/01/2024. Las heurísticas no cambiaron desde 1994. La columna "qué
mirar" es síntesis propia (nivel Práctica) adaptada a sitios B2B con formularios de lead y a ecommerce
chileno.

| N.º | Heurística | Qué mirar en la página | Script que ayuda |
|---|---|---|---|
| H1 | **Visibilidad del estado del sistema** | Al enviar: ¿el botón muestra que está enviando y luego hay confirmación clara? ¿Agregar al carro da feedback y actualiza el contador? ¿El menú marca dónde estoy? ¿El checkout muestra el progreso? ¿Los filtros dicen cuántos resultados quedan? Pasados 10 s sin respuesta, ¿hay indicador de progreso? | estados_formulario |
| H2 | **Coincidencia entre el sistema y el mundo real** | Lenguaje del cliente, sin jerga interna ni nombres de módulos que el comprador no conoce. En Chile: comuna, región, RUT, teléfono +56, CLP con punto de miles. Categorías con los nombres que usa la gente | — |
| H3 | **Control y libertad** | Ventanas y pop-ups con X visible que también se cierran con Esc. Quitar un producto del carro y deshacerlo. Volver atrás en el checkout sin perder datos. El botón atrás del navegador no rompe los filtros ni el formulario | — |
| H4 | **Consistencia y estándares** | El mismo botón primario en todo el sitio. El logo lleva al inicio. El carro arriba a la derecha. Los enlaces parecen enlaces. Los mismos términos para lo mismo: si "cotizar" y "solicitar demo" son distintos, se explica | ui_medicion (censo, alturas, tamaños) |
| H5 | **Prevención de errores** | Formato pedido explicado antes de escribir. Teclado móvil correcto (type email o tel). Selector en vez de texto libre donde corresponde. Stock y mínimo de compra visibles antes del carro. Obligatorios marcados | estados_formulario |
| H6 | **Reconocer antes que recordar** | Etiqueta visible sobre el campo, no solo placeholder. Resumen del pedido visible en el checkout. Filtros aplicados visibles y removibles. Autocompletado o búsquedas recientes | estados_formulario |
| H7 | **Flexibilidad y eficiencia** | autocomplete del navegador en nombre, correo, teléfono y dirección. Recompra o lista habitual en supermercado. Búsqueda por nombre, marca o SKU. Sesión que recuerda direcciones | estados_formulario |
| H8 | **Diseño estético y minimalista** | El CTA principal domina la primera pantalla. Banners, carruseles y pop-ups no compiten con la tarea. La ficha muestra primero precio, formato y disponibilidad. El banner de cookies no tapa el botón principal | ui_medicion (capturas) |
| H9 | **Reconocer, diagnosticar y recuperarse de errores** | Mensaje junto al campo, específico y con la solución. Se conserva lo escrito. Si el envío falla, se dice y se ofrece otra vía (correo, WhatsApp). Página de "sin resultados" con alternativas. 404 útil | estados_formulario |
| H10 | **Ayuda y documentación** | FAQ de despacho, cambios y devoluciones enlazada desde la ficha y el checkout. En B2B: implementación, soporte y contacto fáciles de encontrar. Ayuda contextual en campos poco claros (por qué se pide el RUT) | — |

## Marco complementario

ISO 9241-110:2020 (principios de interacción) es de pago. Solo se confirmaron en fuente pública la
adecuación a la tarea (5.1), la robustez ante errores de uso (5.6) y el compromiso del usuario (5.7). No
se cita la lista completa de siete principios como hecho.

## Cómo usarlas sin caer en opinión

- La heurística es el **porqué** de un hallazgo, no el hallazgo. El hallazgo es lo que le pasa a la persona:
  "Quien escribe su teléfono con letras ve el campo vaciarse sin explicación" (H9), no "viola H9".
- Una heurística sin tarea afectada no es un hallazgo. Es una observación de pulido o de gusto, y se
  rotula como tal.
- Cuando el problema es de cumplimiento verificable (contraste, foco, lector de pantalla, objetivo de
  24 px), se deriva a `accesibilidad-wcag`. Aquí solo se describe el síntoma de uso.
