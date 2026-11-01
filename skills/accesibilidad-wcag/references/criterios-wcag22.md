# WCAG 2.2: los 55 criterios A y AA, qué se automatiza y qué no

Fuente normativa: WCAG 2.2, W3C Recommendation del 05/10/2023, versión vigente del 12/12/2024
(https://www.w3.org/TR/WCAG22/). 31 criterios A y 24 AA. 4.1.1 Parsing está eliminado: no se reporta.
Los 6 criterios nuevos A/AA de 2.2 llevan **(2.2)**.

Columna **axe**: cobertura de axe-core 4.14.0. Es inferencia propia cruzando el listado de reglas con cada
criterio (investigación del 31/10/2026), no una tabla de Deque.
- **Alta**: la regla detecta la mayoría de los fallos reales.
- **Parcial**: detecta ausencias o errores de sintaxis, pero la calidad se revisa a mano.
- **—**: no hay regla A/AA.

Columna **script**: qué script propio aporta candidatos (`tec` = teclado_foco.py, `ada` = adaptacion.py,
`axe+form` = axe_scan.py con `--enviar-vacio`). El resto se cubre con la prueba manual
(`protocolo-manual.md`).

| Criterio | Nombre | Nivel | axe | script | Prueba manual mínima |
|---|---|---|---|---|---|
| 1.1.1 | Contenido no textual | A | Parcial | | ¿El alt dice lo que la imagen aporta? ¿Los iconos con función tienen nombre? |
| 1.2.1 | Solo audio y solo vídeo (grabado) | A | — | | Transcripción o alternativa |
| 1.2.2 | Subtítulos (grabado) | A | Parcial | | Subtítulos sincronizados y correctos |
| 1.2.3 | Audiodescripción o alternativa (grabado) | A | — | | Alternativa al contenido visual relevante |
| 1.2.4 | Subtítulos (en directo) | AA | — | | Solo si hay transmisiones en directo |
| 1.2.5 | Audiodescripción (grabado) | AA | — | | Información visual narrada |
| 1.3.1 | Información y relaciones | A | Parcial | ada | Encabezados reales, listas, tablas con cabeceras, campos agrupados |
| 1.3.2 | Secuencia significativa | A | — | | El orden de lectura del lector de pantalla tiene sentido |
| 1.3.3 | Características sensoriales | A | — | | Instrucciones que no dependen solo de forma, color o posición |
| 1.3.4 | Orientación | AA | — | | Funciona en vertical y horizontal |
| 1.3.5 | Identificar el propósito de la entrada | AA | Parcial | | autocomplete correcto en nombre, correo, teléfono |
| 1.4.1 | Uso del color | A | Parcial | | Errores y enlaces que no se distinguen solo por color |
| 1.4.2 | Control del audio | A | Parcial | | Audio automático de más de 3 s se puede parar |
| 1.4.3 | Contraste (mínimo) | AA | Alta | | Texto sobre imagen o degradado: medir a mano |
| 1.4.4 | Cambio de tamaño del texto | AA | Parcial | ada (candidato) | Zoom de texto al 200% sin pérdida (el script mira scroll, no pérdida) |
| 1.4.5 | Imágenes de texto | AA | — | | Texto real, no imagen con texto (banners) |
| 1.4.10 | Reajuste del contenido (reflow) | AA | — | ada | 320 px sin scroll horizontal |
| 1.4.11 | Contraste no textual | AA | — | | Bordes de campos, iconos e indicador de foco a 3:1 |
| 1.4.12 | Espaciado del texto | AA | Parcial | ada | Con la hoja de 1.4.12 no se corta texto |
| 1.4.13 | Contenido al pasar el puntero o con foco | AA | — | | Tooltips y menús se pueden cerrar y no desaparecen al moverse |
| 2.1.1 | Teclado | A | Parcial | tec | Todo se opera con teclado |
| 2.1.2 | Sin trampas para el foco | A | — | tec | El foco siempre puede salir |
| 2.1.4 | Atajos con una tecla | A | — | | Atajos de una letra se pueden desactivar |
| 2.2.1 | Tiempo ajustable | A | Parcial (solo meta refresh) | | Sesiones o carruseles con tiempo |
| 2.2.2 | Pausar, detener, ocultar | A | Parcial (solo blink/marquee) | | Carruseles automáticos con pausa |
| 2.3.1 | Tres destellos o menos | A | — | | Vídeos o animaciones que destellan |
| 2.4.1 | Evitar bloques | A | Parcial | tec | Enlace de salto o regiones main y encabezados |
| 2.4.2 | Título de la página | A | Parcial | ada (vacío) | El title describe la página |
| 2.4.3 | Orden del foco | A | — | tec | Orden lógico, sin foco en contenido oculto |
| 2.4.4 | Propósito de los enlaces (en contexto) | A | Parcial | | "Ver más" sin contexto |
| 2.4.5 | Múltiples vías | AA | — | | Menú más buscador o mapa del sitio |
| 2.4.6 | Encabezados y etiquetas | AA | — | | Encabezados y etiquetas descriptivos |
| 2.4.7 | Foco visible | AA | — | tec | Indicador visible en cada parada |
| 2.4.11 | Foco no oculto (mínimo) **(2.2)** | AA | — | tec | Cabecera fija, cookies o chat no tapan el foco |
| 2.5.1 | Gestos del puntero | A | — | | Pellizcar o deslizar tienen alternativa de un toque |
| 2.5.2 | Cancelación del puntero | A | — | | La acción ocurre al soltar, no al presionar |
| 2.5.3 | Etiqueta en el nombre | A | Parcial | | El nombre accesible contiene el texto visible |
| 2.5.4 | Activación por movimiento | A | — | | Agitar o inclinar tiene alternativa |
| 2.5.7 | Movimientos de arrastre **(2.2)** | AA | — | | Sliders o arrastrables con alternativa sin arrastre |
| 2.5.8 | Tamaño del objetivo (mínimo) **(2.2)** | AA | Parcial | | 24 × 24 px o separación suficiente |
| 3.1.1 | Idioma de la página | A | Alta | ada | lang correcto en cada versión de idioma |
| 3.1.2 | Idioma de las partes | AA | Parcial | | Fragmentos en otro idioma marcados |
| 3.2.1 | Al recibir el foco | A | — | | Enfocar no cambia de página ni abre ventanas |
| 3.2.2 | Al introducir datos | A | — | | Elegir una opción no envía ni redirige sin aviso |
| 3.2.3 | Navegación coherente | AA | — | | Menú en el mismo orden en todas las páginas |
| 3.2.4 | Identificación coherente | AA | — | | Mismo icono o botón con el mismo nombre |
| 3.2.6 | Ayuda coherente **(2.2)** | A | — | | Contacto, chat o ayuda en el mismo lugar relativo |
| 3.3.1 | Identificación de errores | A | — | axe+form | Error descrito en texto junto al campo |
| 3.3.2 | Etiquetas o instrucciones | A | Parcial | axe+form | Etiqueta visible, no solo placeholder |
| 3.3.3 | Sugerencia ante errores | AA | — | axe+form | El mensaje dice cómo corregir |
| 3.3.4 | Prevención de errores (legales, financieros, datos) | AA | — | | Compras o contratos: revisar, corregir o anular |
| 3.3.7 | Entrada redundante **(2.2)** | A | — | | No se pide dos veces el mismo dato en un proceso |
| 3.3.8 | Autenticación accesible (mínimo) **(2.2)** | AA | — | | Se puede pegar en la contraseña; CAPTCHA con alternativa |
| 4.1.2 | Nombre, función, valor | A | Parcial | | Controles personalizados anunciados bien por el lector |
| 4.1.3 | Mensajes de estado | AA | — | axe+form | "Enviado" o "3 resultados" se anuncian sin mover el foco |

## Cifras de contexto (para el informe, con su nivel)

- Deque afirma que axe detecta el 57,38% de los issues (volumen, no criterios). Fecha original no
  confirmada. **Proveedor.**
- WebAIM Million 2026 (30/03/2026): el 95,9% de las portadas tiene fallos detectables y 56,1 errores de
  media. Los más frecuentes son contraste (83,9%), alt ausente (53,1%), campos sin etiqueta (51%), enlaces
  vacíos (46,3%), botones vacíos (30,6%) y falta de lang (13,5%). **Estudio.**
- De los 6 criterios nuevos A/AA de 2.2, axe solo toca 2.5.8. Los otros cinco se prueban a mano.
