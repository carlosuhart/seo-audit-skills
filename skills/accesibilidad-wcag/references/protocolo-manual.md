# Protocolo manual: lo que ninguna herramienta prueba

Se hace después de los scripts, sobre las mismas páginas y estados. El objetivo no es repetir lo
automático, sino cerrar los criterios marcados "Solo prueba manual" o "falta prueba manual" en la tabla
de cobertura de `consolidar.py`. Cada prueba deja evidencia: captura, paso y qué se oyó o vio.

W3C avisa que sus propias "Easy Checks" "cover just a few accessibility issues"
(https://www.w3.org/WAI/test-evaluate/easy-checks/, 21/03/2024). Una revisión manual parcial se declara
parcial.

## Herramientas en esta sesión

- **Chrome DevTools MCP**: `navigate_page`, `press_key` (Tab, Shift+Tab, Enter, Escape, flechas),
  `take_snapshot` (árbol de accesibilidad con roles y nombres), `take_screenshot`, `evaluate_script`,
  `lighthouse_audit` (categoría Accessibility, usa axe: no suma cobertura a axe_scan.py).
- **Playwright** (scripts de la skill) para repetir un estado: `--clic` abre menús o modales.
- **Lector de pantalla real**: NVDA en Windows o VoiceOver en macOS e iOS. Lo maneja la persona
  que audita. Claude no oye la salida de voz: el árbol de `take_snapshot` aproxima lo que se anuncia, pero
  no lo reemplaza. Si no hubo lector real, el informe lo dice.

## 1. Teclado (2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 3.2.1)

Partir de los candidatos de `teclado_foco.py` y confirmar cada uno con la captura.

1. Menú principal: ¿se abre con Enter o Espacio y se recorren los subniveles? ¿Escape lo cierra y
   devuelve el foco al botón?
2. Diálogos (agenda, cotizador, chat, galería): el foco entra al abrir, Tab queda dentro, Escape cierra
   y el foco vuelve al disparador. Con el diálogo cerrado, sus campos no deben recibir foco.
3. Pestañas, acordeones, carruseles, selects personalizados: se operan con teclado y anuncian su estado.
4. Enfocar un elemento no debe cambiar de página ni abrir ventanas (3.2.1).
5. Foco no oculto: con el banner de cookies sin cerrar y con la cabecera fija, recorrer la página. Si
   el elemento enfocado queda totalmente tapado, falla 2.4.11 (fallo F110; arreglo C43 con
   `scroll-padding`).

## 2. Lector de pantalla (1.1.1, 1.3.1, 1.3.2, 2.4.6, 4.1.2, 4.1.3)

Con NVDA: NVDA+↓ lee, H salta encabezados (1-6 por nivel), D regiones, K enlaces, F campos, T tablas,
NVDA+F7 lista de elementos y NVDA+Espacio cambia de modo
(https://webaim.org/resources/shortcuts/nvda). Con VoiceOver en macOS: Cmd+F5, VO = Control+Opción,
VO+U rotor, VO+Cmd+H siguiente encabezado (https://webaim.org/articles/voiceover/).

- La lista de encabezados resume la página. La de regiones tiene main, navegación y pie.
- Imágenes con función: el alt describe la función ("Ir al inicio"), no el archivo.
- Controles personalizados: se anuncian con rol, nombre y estado (expandido, seleccionado, marcado).
- Formulario: cada campo se anuncia con su etiqueta, si es obligatorio y su error.
- Mensajes de estado (4.1.3): "Gracias, recibimos tu solicitud", "Agregado al carro" o "12 resultados"
  se anuncian sin mover el foco.

## 3. Formularios (1.3.5, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 3.3.8)

Base: `axe_scan.py --enviar-vacio` (con el envío al servidor bloqueado).

- Enviar vacío y con un correo inválido: ¿el error aparece en texto, junto al campo y dice cómo
  corregir? ¿El foco va al primer error o hay un resumen enlazado?
- El placeholder no reemplaza a la etiqueta: al escribir, ¿se sigue sabiendo qué campo es?
- `autocomplete` en nombre, correo, teléfono, empresa y dirección (1.3.5).
- Procesos de varios pasos: no pedir dos veces el mismo dato (3.3.7).
- Compra, contrato o datos legales: revisar antes de confirmar, corregir o anular (3.3.4).
- Acceso o registro: se puede pegar en la contraseña. Bloquear el pegado falla 3.3.8. Un CAPTCHA de
  texto distorsionado o una operación matemática necesitan alternativa.
- **Nunca enviar un formulario real** sin la autorización del responsable del sitio. Los datos de
  prueba son ficticios (@example.com).

## 4. Visual y adaptación (1.4.1, 1.4.4, 1.4.5, 1.4.10, 1.4.11, 1.4.12, 1.4.13)

- Zoom del navegador al 200% y al 400%: sin pérdida de contenido ni de funciones y sin scroll en dos
  ejes a 320 px. Las tablas de datos, los mapas y los gráficos están exceptuados de 1.4.10.
- Contraste de lo que axe marca como "revisión manual": texto sobre fotos, degradados y vídeos.
- Contraste no textual a 3:1: borde de campos, iconos con función e indicador de foco.
- Tooltips y menús al pasar el puntero: se cierran con Escape, se puede mover el puntero encima de
  ellos y no desaparecen solos (1.4.13).
- Errores, enlaces dentro del texto y estados: que no dependan solo del color (1.4.1).
- Banners con texto dentro de la imagen (1.4.5): muy común en ecommerce y en portadas.

## 5. Movimiento, tiempo y puntero (2.2.1, 2.2.2, 2.5.1, 2.5.2, 2.5.7, 2.5.8)

- Carruseles o animaciones automáticas: se pueden pausar (2.2.2, A). Respetar `prefers-reduced-motion`
  es 2.3.3, que es AAA: se recomienda, pero no es exigible para AA.
- Sesiones o carritos que caducan: aviso y posibilidad de extender el tiempo (2.2.1).
- Sliders de precio, mapas o elementos que se arrastran: alternativa sin arrastre (2.5.7).
- Tamaño del objetivo: 24 × 24 px CSS o separación equivalente. Ejemplo del W3C: botones de 20 × 20 con
  4 px de separación pasan, sin separación fallan. Los enlaces dentro del texto están exceptuados.

## 6. Criterios que solo se cierran a mano (un paso por criterio)

| Criterio | Procedimiento |
|---|---|
| 1.2.1-1.2.5 Medios | Por cada vídeo o audio propio: transcripción (1.2.1), subtítulos sincronizados (1.2.2), audiodescripción o alternativa si lo visual informa algo que no se dice (1.2.3 y 1.2.5). 1.2.4 solo si hay transmisiones en directo. Sin medios: No aplica |
| 1.3.3 Características sensoriales | Buscar instrucciones del tipo "pulsa el botón verde" o "a la derecha": deben nombrar también el control |
| 1.3.4 Orientación | En móvil, girar a horizontal: el sitio no debe bloquear una orientación |
| 2.1.4 Atajos con una tecla | Pulsar letras sueltas fuera de campos de texto: si algo se activa, debe poder desactivarse o cambiarse |
| 2.3.1 Destellos | Vídeos o animaciones con destellos rápidos: no más de tres por segundo |
| 2.4.4 Propósito de los enlaces | Listar enlaces con NVDA+F7: "Ver más" o "Aquí" sin contexto en la misma frase o ítem fallan |
| 2.5.1 Gestos del puntero | Carruseles con deslizar o mapas con pellizcar: debe haber botones de un toque |
| 2.5.2 Cancelación del puntero | Presionar un botón y arrastrar fuera antes de soltar: la acción no debe ejecutarse |
| 2.5.3 Etiqueta en el nombre | Comparar el texto visible del botón con su nombre accesible (axe ayuda); para control por voz, el nombre empieza por el texto visible |
| 2.5.4 Activación por movimiento | Si agitar o inclinar hace algo, hay alternativa en pantalla |
| 3.2.2 Al introducir datos | Elegir una opción en un select o marcar una casilla no envía ni cambia de página sin aviso |

## 7. Modos y dispositivos que se olvidan

- **Alto contraste forzado** (Windows, `forced-colors`): con el modo activo, botones, bordes de campos,
  iconos y el foco siguen viéndose. En Playwright se emula con `forced_colors="active"`.
- **Lector de pantalla en móvil**: TalkBack (Android) y VoiceOver (iOS) recorriendo el menú y el
  formulario con gestos. Los errores de móvil son distintos a los de escritorio.
- **Contraste del indicador de foco** (1.4.11): el contorno o la sombra del foco debe tener 3:1 contra el
  fondo. Que "cambie" (2.4.7) no basta si el cambio casi no se ve.

## 8. Coherencia entre páginas (2.4.5, 3.2.3, 3.2.4, 3.2.6, 3.1.2)

Comparar al menos tres plantillas (portada, servicio o producto, contacto o ficha):
- El menú está en el mismo orden y lugar. Los iconos y botones repetidos tienen el mismo nombre.
- El contacto, el chat o la ayuda aparecen en el mismo lugar relativo (3.2.6, nuevo en 2.2).
- Hay al menos dos vías para llegar a una página: menú y buscador, o menú y mapa del sitio (2.4.5).
- Las versiones en otro idioma tienen el lang correcto y marcan los fragmentos en otro idioma (3.1.2).
  Si el sitio redirige por IP, probar cada idioma con `--bloquear-host` para no auditar la versión
  equivocada.

## Muestra de páginas

Una página por plantilla, no por URL: portada, listado o categoría, detalle (servicio, producto o
post), contacto o formulario, flujo de compra o registro, y la página de error 404. Para cada una se
revisan el estado inicial y los estados que cambian la interfaz: menú abierto, diálogo abierto,
formulario con errores y móvil. Lo que no se revisó se lista en el informe.
