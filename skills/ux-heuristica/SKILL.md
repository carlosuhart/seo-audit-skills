---
name: ux-heuristica
description: >
  Evaluación heurística de UX/UI de sitios en vivo y de diseños en Figma antes de desarrollo: las 10 heurísticas de
  Nielsen aplicadas por tarea (formulario de lead B2B, búsqueda, ficha, carro y checkout de ecommerce), recorrido
  cognitivo, severidad 1-4 con frecuencia, impacto y persistencia, confianza con fuente y captura anotada obligatoria
  por hallazgo. Scripts para probar formularios en cuatro estados sin enviar nada (vacío, datos erróneos, fallo del
  envío), medir la interfaz a 360, 768 y 1.280 px y marcar hallazgos sobre capturas. Use when user says "UX",
  "UI", "usabilidad", "evaluación heurística", "revisión de UX", "auditoría UX", "qué falla en este flujo",
  "revisa el diseño en Figma", "revisa el formulario", "por qué no completan el formulario", "heuristic
  evaluation" o "UX review". No para accesibilidad normativa (accesibilidad-wcag), persuasión y pruebas A/B
  (page-cro, form-cro) ni intención de búsqueda (seo-sxo), a los que deriva.
argument-hint: "<url, flujo o enlace de Figma> [--tipo b2b|ecommerce|saas] [--uso interno|cliente]"
metadata:
  category: ux
  author: Zythos Media
  version: 1.0.0
  fuentes_revisadas: 2026-10-31
  revisar_fuentes: 2027-04-30
---

# Evaluación heurística UX/UI

Evalúa interfaces que ya existen (sitio en vivo) o que están por construirse (Figma), y entrega hallazgos que
un equipo puede ejecutar. No rediseña ni escribe un ensayo sobre heurísticas.

**La regla que gobierna todo: cada hallazgo lleva evidencia.** Captura anotada, pasos para reproducirlo,
heurística violada, tarea afectada y confianza con su fuente. Lo que no se vio es una hipótesis y se
redacta como pregunta. Un modelo que evalúa sin ver produce hallazgos plausibles que no existen: por eso
los scripts devuelven señales a confirmar, no conclusiones.

## Paso 0. Leer el encargo

Antes de abrir nada, deja escrito en un párrafo (va arriba del informe):
1. **¿Evaluar o construir?** Esta skill evalúa. Si el pedido es diseñar o construir, se dice en una línea.
   Si es "revisa y corrige", primero se entrega la evaluación y después se corrige.
2. **Alcance**: sitio completo, un flujo, unas pantallas o una dimensión. No se amplía en silencio. Lo que
   queda fuera pero afecta a un hallazgo se nombra como "fuera de alcance" y se dice qué cambiaría.
3. **Tipo de negocio y tareas que importan**: B2B (lead, demo, cotización), ecommerce (búsqueda a compra),
   SaaS (registro, prueba). Las tareas salen de ahí (`references/flujos-y-formularios.md`) y **las páginas
   se eligen con datos** si hay acceso: páginas de entrada con más tráfico orgánico (GSC), páginas de salida
   y embudo (GA4, `ga4-analysis`) y búsquedas internas. Sin datos, se declara que la muestra es por criterio.
4. **Audiencia y riesgo**: experta, general o mixta (la jerga y la densidad se juzgan distinto), y si hay
   dinero, datos personales o decisiones irreversibles.
5. **Evidencia disponible**, de más a menos fiable: sitio en vivo · Figma por MCP · capturas del cliente ·
   descripción (solo hipótesis). La confianza de cada hallazgo no supera la de su fuente.
6. **Uso**: interno o cliente. Si no está dicho, pregunta.

Busca las URL reales en el sitemap o navegando. **No las adivines**: una URL inventada devuelve un 404
que se evalúa como si fuera la página.

## Paso 1. Medir (sitio en vivo)

Python siempre con `py` desde PowerShell. Los scripts solo leen y no envían formularios: bloquean service
workers, WebSockets, navegaciones, fetch/XHR y píxeles de terceros desde antes de rellenar.

```powershell
$s = "$HOME\.claude\skills\ux-heuristica\scripts"
$o = "<carpeta del cliente>\ux\<AAAAMMDD>"
py "$s\ui_medicion.py" <url portada> <url servicio o ficha> <url contacto> --out $o
py "$s\estados_formulario.py" <url con el formulario> --vistas escritorio,movil --out $o
py "$s\estados_formulario.py" <url> --clic "<botón que abre la ventana>" --out $o   # formulario en ventana
```

| Script | Qué responde |
|---|---|
| `ui_medicion.py` | Scroll horizontal, objetivos táctiles, texto chico, alineaciones, tarjetas desparejas, deriva de tokens (radios, sombras, tamaños), con capturas de página completa a 360, 768 y 1.280 px |
| `estados_formulario.py` | Inventario de campos (etiqueta, placeholder, tipo, autocomplete, obligatorios) y reacción al enviar vacío, con datos erróneos y con el envío bloqueado: mensajes, datos conservados, feedback del botón, pantalla de error del framework |
| `anotar_capturas.py` | Marca cada hallazgo con su ID y un color por severidad, sobre la página en vivo (por selector) o sobre una imagen o frame exportado |

Si el sitio redirige el idioma por IP, agrega `--bloquear-host <servicio>` a cada script.

## Paso 2. Recorrer las tareas

Para cada tarea del Paso 0, en escritorio y en móvil, con las cuatro preguntas del recorrido cognitivo
(`references/flujos-y-formularios.md`). Usa Chrome DevTools MCP (`navigate_page`, `click`,
`take_screenshot`) o Playwright. Anota cada paso que falla y su captura.

**En el recorrido con el MCP nunca se pulsa enviar, agregar al carro, pagar, registrarse ni agendar**: el
MCP no bloquea nada y esas acciones crean datos reales en el sitio del cliente. El paso de envío lo prueba
`estados_formulario.py`. El camino de éxito (confirmación, qué pasa después, correo de respuesta, llegada
al CRM) y el carro y el checkout se evalúan solo con un **envío autorizado y etiquetado por el cliente**
("PRUEBA, no contactar") o en un entorno de pruebas. Si no hay autorización, se declara como no evaluado.

Después, una pasada por heurística con `references/heuristicas-nielsen.md` sobre las mismas pantallas,
para encontrar lo que el recorrido no tocó.

## Paso 3. Diseños en Figma

`references/figma-revision.md`: acceso por MCP (`create_session`, `get_metadata`, `get_screenshot`,
`get_variable_defs`), qué se puede y qué no se puede evaluar en un diseño estático, y la checklist de
revisión antes de desarrollo (estados, breakpoints, contenido realista, mensajes de error, flujos
completos, notas para desarrollo, y que el rediseño no pierda lo que hoy funciona). Si el conector no
responde, se piden las exportaciones: **no se opina sobre un diseño que no se vio**.

## Paso 4. Confirmar, clasificar y filtrar

`references/severidad-y-evidencia.md`:
- Cada señal de los scripts se mira en su captura antes de pasar a hallazgo. Ejemplos reales de falsos
  positivos: una etiqueta visible no asociada en el código parece "campo sin etiqueta", y un mensaje de
  error con clases CSS propias parece "sin mensaje". La captura decide.
- Severidad 1-4 con frecuencia, impacto y persistencia en una línea. Tipo: Defecto, Oportunidad o Gusto
  (el gusto nunca es 3 ni 4).
- Confianza con fuente: `(sitio en vivo, móvil 390 px)`, `(Figma, frame X)`, `(medido)`, `(GA4)`.
- Los hallazgos 3 y 4 se apoyan en una guía externa o en datos (`references/evidencia-externa.md`) y se
  re-califican a ciegas: un subagente en contexto nuevo recibe solo las capturas y la descripción de cada
  hallazgo (sin la severidad propuesta) y asigna la suya. Si difieren en más de un punto, se discute y se
  anota el motivo.
- Lo que solo aparece porque la prueba provocó el fallo (red bloqueada) es un caso de borde: se califica
  según lo probable que sea en la realidad (errores registrados, Sentry, GA4), no como bloqueo seguro.
- Lo que pertenece a otra disciplina se deriva (`references/salida-y-derivaciones.md`): contraste, foco o
  lector de pantalla van a `accesibilidad-wcag`; "convence poco" va a CRO; intención de búsqueda va a
  `seo-sxo`.

## Paso 5. Entregar

Estructura en `references/salida-y-derivaciones.md`: alcance, resumen, ganancias rápidas, hallazgos por
tarea, plan priorizado, qué funciona bien, preguntas abiertas y derivaciones. Cada hallazgo lleva su
captura anotada (`anotar_capturas.py`) y la prueba de aceptación con la que se verifica que quedó
resuelto. Si el cliente tiene su propia skill o plantilla de entrega, el documento se redacta con ella.

Prioridad: primero lo que bloquea una tarea de conversión (4), después lo que afecta a todo el sitio o a
la plantilla más visitada, y al final el pulido. **Doce hallazgos reales valen más que cuarenta**: si una
pasada encuentra treinta cosas, se reportan las que importan y se dice que se vieron treinta.

## Reglas duras

- Sin captura y pasos no hay hallazgo. Sin tarea afectada no hay defecto: es observación de gusto.
- No presentar una hipótesis como observada. No inflar la confianza: un diseño estático no muestra el
  comportamiento.
- No dar un puntaje global de UX.
- No reportar "falta validación en línea" como problema grave: las fuentes discrepan. Sí la validación
  que marca error mientras la persona escribe.
- No citar cifras de Baymard como benchmark del cliente ni como promesa de mejora. No mezclar sus dos
  conteos de campos (11,3 frente a 14,88) ni sus dos cifras de cuenta obligatoria (18% frente a 24%).
- No enviar formularios reales ni usar datos personales. Datos ficticios, envío bloqueado.
- No proponer precios, pruebas gratis ni cambios de oferta: son decisiones de negocio. Se presenta la
  evidencia y queda como consulta.
- No dictar implementación sobre código ajeno: comportamiento esperado más prueba de aceptación.
- Declarar que es la evaluación de un solo experto (en seis proyectos, un evaluador solo encontró en
  promedio el 35% de los problemas; Nielsen, 1994) y recomendar test con usuarios para los críticos.

Si existe `references/casos-privados.md` (anexo local, no versionado), léelo: tiene los casos reales, las
reglas de entrega de cada cliente y sus archivos.
