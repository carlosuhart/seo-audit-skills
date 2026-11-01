# Recorrido por tareas, formularios, mensajes de error, móvil y navegación

## Recorrido cognitivo: cuatro preguntas por paso

Fuente: NN/g, "Evaluate Interface Learnability with Cognitive Walkthroughs"
(https://www.nngroup.com/articles/cognitive-walkthroughs/, 13/02/2022). Nivel Guía.

1. ¿La persona intentará lograr el resultado correcto?
2. ¿Notará que la acción correcta está disponible?
3. ¿Asociará esa acción con lo que quiere lograr?
4. Después de actuar, ¿verá que avanza hacia su objetivo?

Un "no" en cualquiera de las cuatro hace fallar el paso. Se registra paso por paso, desde una persona
definida.

## Personas y tareas por tipo de sitio (síntesis, Práctica)

| Sitio | Persona | Tareas a recorrer |
|---|---|---|
| B2B (tecnología, logística, SaaS) | Responsable de compra que compara proveedores | Entender qué hace la empresa en la primera pantalla. Encontrar el servicio que le aplica. Saber el precio, un rango o cómo se cotiza. Ver casos y clientes. Enviar el formulario. Saber qué pasa después y en qué plazo |
| B2B | Usuario técnico que evalúa | Encontrar integraciones, especificaciones, seguridad y soporte. Compartir material con su jefe |
| Ecommerce de alimentos (Chile) | Comprador en móvil | Buscar por nombre o marca. Filtrar por categoría o formato. Ver en la ficha precio, formato o peso, precio por unidad y disponibilidad. Agregar al carro. Ver el costo y el plazo de despacho por comuna **antes** de pagar. Pagar como invitado. Recibir la confirmación |
| Ecommerce | Cliente recurrente | Iniciar sesión, repetir un pedido, cambiar la dirección |

## Formularios de lead, contacto y registro

`estados_formulario.py` cubre la parte medible. Guías:

| Tema | Guía | Fuente y nivel |
|---|---|---|
| Largo | Solo los campos que se usan. Lo que se puede deducir o pedir después, fuera | NN/g, "Website Forms Usability", 01/05/2016, Guía |
| Diseño | Una columna, etiqueta pegada al campo, orden lógico, radios en vez de desplegable para 2 o 3 opciones, obligatorios y opcionales distinguidos, formato explicado antes, sin botón Borrar | mismo |
| Etiquetas | El placeholder desaparece al escribir, obliga a recordar, se confunde con un dato precargado y suele tener contraste bajo. Etiqueta visible siempre | NN/g, "Placeholders in Form Fields Are Harmful", 2014, rev. 2018, Investigación |
| Validación en línea | **Las fuentes discrepan.** NN/g: solo donde los errores son frecuentes y sin marcar errores antes de tiempo. Baymard: al salir del campo. GOV.UK: al enviar. **No se reporta "falta validación en línea" como problema grave.** Sí se reporta el error que aparece mientras la persona todavía escribe | NN/g 14/05/2023 · Baymard 09/01/2024 · GOV.UK |
| Después de enviar | Página o mensaje que dice qué pasa, en cuánto tiempo y por qué canal. Si el envío falla, se dice y se ofrece otra vía | Práctica |
| Doble envío | El botón cambia a "Enviando…" o se bloquea mientras se procesa | Práctica, H1 |

**Prueba segura:** nunca se envían formularios reales sin autorización del responsable del sitio. Los
datos son ficticios. `estados_formulario.py` bloquea toda petición que no sea GET y cualquier GET con el
correo de prueba.

## Mensajes de error

Fuente: NN/g, "Error-Message Guidelines" (https://www.nngroup.com/articles/error-message-guidelines/,
14/05/2023), y GOV.UK Design System, componente "Error message". Nivel Guía.

- **Dónde:** junto al campo y, en formularios largos, también en un resumen arriba con el mismo texto.
- **Cómo se ve:** texto más icono o borde, nunca solo color. Con una gravedad proporcional: una ventana
  modal solo para lo que bloquea.
- **Qué dice:** qué falló y cómo arreglarlo, con la etiqueta del campo ("Ingresa tu correo, por ejemplo
  nombre@empresa.cl"). Se evitan "inválido", "error", "ups" y los códigos técnicos. Sin humor y sin
  culpar a la persona.
- **Qué conserva:** lo escrito. Borrar el formulario tras un error es un defecto.
- **Cuándo:** no antes de tiempo. Un campo vacío mientras la persona explora no es un error.
- **Falla del envío:** la pantalla genérica del framework ("Application error", "Reload") en vez de un
  mensaje es un defecto en un flujo de conversión. Su severidad depende de cuán seguido falle el envío en
  la realidad: si la prueba lo provocó y no hay datos de errores, es un caso de borde (2 o 3). Si hay
  errores registrados o la validación del cliente no existe (como un registro que manda al servidor datos
  vacíos), sube.

Tiempos de respuesta (Nielsen, 1993): 0,1 s se percibe instantáneo, 1 s mantiene el hilo y 10 s es el
límite de atención, desde donde hace falta un indicador de progreso.

## Móvil y objetivos táctiles

| Criterio | Valor | Fuente |
|---|---|---|
| Recomendación de uso | 1 × 1 cm físicos con unos 2 mm de separación | NN/g, 05/05/2019 |
| Recomendación de uso | unos 48 px con unos 8 px de separación | web.dev, 31/03/2020 |
| Mínimo de cumplimiento | 24 × 24 px CSS o separación equivalente (WCAG 2.5.8, AA) | W3C, Understanding 2.5.8 |

Entre 24 y 48 px, en vistas táctiles, se reporta como **oportunidad de uso**. Bajo 24 px va a
`accesibilidad-wcag` como posible incumplimiento. En escritorio sin pantalla táctil no se reporta.

## Navegación y arquitectura de la información

Fuente: NN/g, "Menu-Design Checklist: 17 UX Guidelines" (https://www.nngroup.com/articles/menu-design/,
07/06/2024). Nivel Guía.

En escritorio, el menú es visible (no solo hamburguesa) y está donde se espera. Indica la ubicación
actual. Las etiquetas son claras, conocidas y empiezan por la palabra clave. Una flecha marca qué abre un
submenú, y el submenú se abre con clic, no solo al pasar el puntero. No hay cascadas de varios niveles.
En páginas largas el menú queda fijo. Los megamenús son para sitios grandes y los menús secuenciales
para móvil.

Si el problema es que la página no responde a la intención de quien llega desde Google (tipo de página
equivocado), se deriva a `seo-sxo`. Si es la estructura del sitio, a `site-architecture`.
