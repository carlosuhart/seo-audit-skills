# Revisión de diseños en Figma antes de desarrollo

Revisar un diseño antes de que se construya es lo más barato. NN/g lo recomienda en cualquier etapa con
un prototipo suficientemente detallado ("UX Expert Reviews", 2018). No existe una checklist primaria de
revisión de diseño para el traspaso a desarrollo: la de abajo es síntesis propia (nivel Práctica).

## Acceso por el MCP de Figma

1. Extraer `fileKey` y `nodeId` de la URL (`figma.com/design/<fileKey>/...?node-id=1-2` → nodeId `1:2`).
2. `create_session` con el fileKey y la tarea, antes de cualquier otra herramienta del archivo.
3. `get_metadata` para el árbol de frames (qué pantallas y estados existen).
4. `get_screenshot` de cada frame a revisar. Se guarda la imagen como evidencia.
5. `get_variable_defs` para los tokens de color y tipografía (contraste y consistencia).
6. `get_design_context` solo si hace falta leer textos o medidas exactas de un nodo.

Límites conocidos: las capturas en base64 se degradan en sesiones largas, porque ocupan contexto.
Conviene revisar por bloques de pantallas. Los recursos firmados del CDN no se bajan con curl. Un archivo
de Figma no es un inventario de estados: lo que no está dibujado no existe para el desarrollador.

Si el conector falla (404 o sin permiso), se pide a quien corresponda la exportación PNG de los frames y
se revisa con `anotar_capturas.py` en modo imagen. No se opina sobre un diseño que no se vio.

## Qué se puede y qué no se puede evaluar en un diseño estático

| Se puede | No se puede, o solo en parte |
|---|---|
| Jerarquía visual, CTA, contenido de la primera pantalla | Tiempos de carga, LCP, INP, CLS |
| Etiquetas, textos, nombres del menú, orden de campos | Validación real y teclado móvil |
| Cantidad de campos y pasos, si están todos los frames | Autocompletado y gestores de contraseñas |
| Consistencia de componentes y tokens | Foco, orden de tabulación y lector de pantalla, salvo que estén anotados |
| Contraste (con los tokens) y tamaño de objetivos | Breakpoints que no se diseñaron |
| Estados, solo si se diseñaron | Contenido real: nombres largos, sin foto, precios largos, traducciones |
| Recorrido de tareas en un prototipo enlazado | Errores del servidor, pasarela de pago, despacho real |

Todo hallazgo sobre Figma lleva la confianza "(Figma, frame X)". El comportamiento que el diseño implica
pero no muestra es Baja.

## Checklist de revisión antes de desarrollo

1. **Estados de cada componente interactivo**: normal, al pasar el puntero, foco visible, presionado,
   deshabilitado, cargando, error y éxito. Si no están, una nota que diga que usa los del sistema de
   diseño.
2. **Estados de cada vista con datos**: vacío, cargando, error, y "sin resultados" en cada búsqueda.
3. **Breakpoints**: móvil (360-390 px), tableta y escritorio, o reglas de adaptación escritas.
4. **Contenido realista**: textos largos, títulos de producto de dos líneas, precios en CLP con punto de
   miles, productos sin foto, formulario con error en varios campos a la vez.
5. **Mensajes de error escritos**, no "Lorem ipsum" ni "Error".
6. **Flujos completos en el prototipo**, incluido el camino de error: de la portada al envío del
   formulario, de la búsqueda a la confirmación del pedido.
7. **Tamaños táctiles y contraste anotados.**
8. **Notas para desarrollo** sobre lo que no se ve: orden de foco, menús, validación, qué pasa al volver
   atrás.
9. **Comparación con el sitio actual**: lo que hoy funciona no se pierde en el rediseño. Incluye lo que
   sostiene el SEO (textos, encabezados, URL, enlaces internos): si el rediseño lo cambia, se avisa.

## Cómo se redacta

- **"Falta definir"**: un estado o breakpoint ausente. Suele ser severidad 2 o 3 según el flujo.
- **"Problema de diseño"**: está presente y genera un problema de uso.
- **"Gusto"**: preferencia estética sin tarea afectada. Se rotula así o se omite.

Cuando el diseño lo define el equipo de Diseño del cliente, el documento reporta observaciones con
capturas y medidas y no propone soluciones de diseño, salvo que se pida una propuesta puntual. Las
reglas de cada cliente están en el anexo privado.
