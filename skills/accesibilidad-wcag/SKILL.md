---
name: accesibilidad-wcag
description: >
  Auditoría de accesibilidad web contra WCAG 2.2 AA sobre sitios en vivo: axe-core 4.14 en escritorio, móvil y
  estados (menú, diálogo, formulario con errores sin enviar nada), recorrido real de teclado (foco visible por
  píxeles, foco tapado por cookies o cabecera fija, foco en contenido oculto, trampas, enlace de salto), reflow a
  320 px, zoom 200%, espaciado 1.4.12 y árbol de accesibilidad; consolidación por criterio con severidad,
  confianza y patrón, protocolo manual con lector de pantalla y contexto legal fechado (EAA, España, ADA, Chile,
  Brasil). Use when user says "accesibilidad", "auditoría de accesibilidad", "WCAG", "es accesible",
  "lector de pantalla", "navegación con teclado", "contraste", "European Accessibility Act", "a11y" o
  "accessibility audit". No para revisar usabilidad general (ux-heuristica), velocidad (core-web-vitals) ni
  preparación para agentes de IA (seo-agentic), aunque las cita.
argument-hint: "<url o lista de URLs> [--mercados cl,eu,us,br] [--uso interno|cliente]"
metadata:
  category: ux
  author: Zythos Media
  version: 1.0.0
  fuentes_revisadas: 2026-10-31
  revisar_fuentes: 2027-04-30
---

# Auditoría de accesibilidad WCAG 2.2 AA

Mide si una persona con discapacidad puede usar el sitio: con lector de pantalla, solo con teclado, con baja
visión, con zoom o con motricidad reducida. El estándar es **WCAG 2.2 nivel AA** (55 criterios). Cubre las
cláusulas web derivadas de WCAG de la norma europea EN 301 549 (capítulo 9, hoy V3.2.1 basada en 2.1 AA), **no**
sus requisitos que no vienen de WCAG ni las obligaciones de información de la EAA (declaración de
accesibilidad, anexos I y V): eso se declara fuera de alcance.

Tres verdades que ordenan todo el trabajo:
- **Las herramientas no prueban la conformidad.** axe no tiene regla para 34 de los 55 criterios, entre
  ellos 5 de los 6 nuevos de 2.2. Un informe sin fallos de axe no dice que el sitio sea accesible.
- **Sin evidencia no hay hallazgo.** Cada hallazgo lleva selector, captura o paso de teclado, y su confianza
  con la fuente. Lo que no se vio es un candidato o una pregunta.
- **Nunca se dice "cumple".** Como mucho: "sin hallazgos en la muestra revisada, con prueba manual completa".

## Paso 0. Alcance

Antes de ejecutar nada, deja escrito:
1. **Muestra** (método WCAG-EM): una muestra estructurada con una página por plantilla (portada, listado,
   detalle, contacto o formulario, compra o registro, 404) en cada idioma, más unas pocas páginas al azar
   del sitemap. Los **procesos completos** (registro, cotización, compra) se auditan de punta a punta, no
   solo su primera pantalla: la conformidad exige el proceso entero. Busca las URL reales en el sitemap o
   con navegación. **No las adivines**: una URL inventada da un 404 que se audita como si fuera la página.
   Declara qué contenido de terceros (chat, mapas, pasarela de pago, widgets) queda fuera de alcance.
2. **Estados**: menú abierto, diálogos (agenda, chat, cotizador), formulario con errores, móvil.
3. **Mercados** donde opera el sitio (idiomas, despacho, moneda). Definen qué fila de `marco-legal.md` se cita.
4. **Uso del entregable**: interno o cliente. Si no está dicho, pregunta.
5. **Redirecciones por IP o idioma**: si el sitio redirige según el país, cada script lleva
   `--bloquear-host <servicio>` para auditar la versión correcta.

## Paso 1. Preparar

```powershell
$s = "$HOME\.claude\skills\accesibilidad-wcag\scripts"
py "$s\setup_axe.py"            # descarga axe-core 4.14.0, verifica sha512, deja vendor/ (una vez)
```

Python siempre con `py` desde PowerShell. Los scripts solo leen: no escriben en ningún CMS y no envían
formularios. `--enviar-vacio` pulsa el botón en modo estricto: sin service workers ni WebSockets, y sin
ninguna petición salvo los recursos estáticos del mismo dominio (ni fetch, ni navegación, ni píxeles de
terceros). En el recorrido manual con el MCP nunca se pulsa enviar, pagar ni agendar.

## Paso 2. Pasada automática

```powershell
$o = "<carpeta del proyecto>\accesibilidad\<AAAAMMDD>"
py "$s\axe_scan.py" --urls-archivo urls.txt --vistas escritorio,movil --out $o
py "$s\axe_scan.py" <url del formulario> --enviar-vacio "form" --out $o
py "$s\axe_scan.py" <url> --clic "<selector del botón del menú>" --estado menu --out $o
py "$s\teclado_foco.py" --urls-archivo urls.txt --out $o
py "$s\teclado_foco.py" <url> --vista movil --out $o
py "$s\adaptacion.py" --urls-archivo urls.txt --idioma es --out $o
py "$s\consolidar.py" --dir $o
```

| Script | Qué responde | Criterios |
|---|---|---|
| `axe_scan.py` | Fallos automáticos por regla, con nodos; los `incomplete` van a revisión manual | 21 criterios, alta o parcial |
| `teclado_foco.py` | Recorrido real con Tab: foco visible, tapado, en contenido oculto, trampas, salto, orden, diálogos | 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.11 |
| `adaptacion.py` | Reflow a 320 px en escritorio, equivalente de zoom 200%, espaciado 1.4.12 (recortes y solapes), lang, title, regiones, árbol de accesibilidad | 1.4.4 (candidato), 1.4.10, 1.4.12, 3.1.1, 2.4.2 |
| `consolidar.py` | Hallazgos con severidad propuesta, confianza y patrón; separa incumplimientos de buenas prácticas; aparta las páginas no auditables; tabla de cobertura de 55 criterios | todos |

Si un estado no se alcanzó (`clics_fallidos`), si la página respondió 4xx o 5xx (un desafío anti-bot
también) o si terminó en otro dominio, `consolidar.py` la saca de los resultados y la lista como "no
auditable". Se dice en el informe y se repite con otro acceso; no se completa con suposiciones.

Límite conocido: una capa con `pointer-events: none` (degradado sobre la cabecera) no la detecta el
muestreo de 2.4.11; se revisa en la captura.

## Paso 3. Confirmar los candidatos

Todo lo que no tiene confianza Alta se mira antes de reportarlo:
- **Foco no visible**: abre la captura en `capturas/`. Si el elemento cambia de forma sutil (subrayado,
  sombra), no es un fallo. Sí lo es si el cambio no se distingue.
- **Foco en contenido no visible**: suele ser un diálogo o un menú cerrado que conserva sus campos en el orden
  de Tab. Se confirma recorriendo con DevTools MCP (`press_key` Tab y `take_screenshot`).
- **Foco tapado**: ocurre con el banner de cookies visible o con la cabecera fija. Se confirma con la captura
  de esa parada.
- **No alcanzables con teclado**: se confirma que el elemento hace algo al pulsarlo con el ratón. Si no hace
  nada, se descarta.
- **Texto recortado con 1.4.12**: un extracto truncado a propósito (line-clamp con enlace al artículo) no
  suele ser pérdida de contenido. Se reporta como Menor o se descarta, y se dice por qué.

## Paso 4. Prueba manual

`references/protocolo-manual.md`: teclado en menús y diálogos, lector de pantalla, formularios con error,
zoom 200% y 400%, contraste sobre imágenes, movimiento, objetivos táctiles, coherencia entre páginas. Cierra
los criterios que la tabla de cobertura marca como "Solo prueba manual". Si no hubo lector de pantalla real,
se declara: el árbol de `take_snapshot` aproxima, no reemplaza.

## Paso 5. Severidad y prioridad

`references/severidad-y-salida.md`. La severidad de axe es el punto de partida; quien audita la ajusta por
camino y frecuencia:
1. Crítica y Grave en el camino de conversión (formulario, carro, checkout, registro).
2. Sistémicas (cabecera, menú, cookies, chat, pie): un arreglo y se resuelve todo el sitio.
3. Plantilla.
4. Página.

## Paso 6. Entregar

Estructura y esquema de hallazgo en `references/severidad-y-salida.md`. Cada hallazgo lleva la prueba de
aceptación con la que se verifica que quedó resuelto, y esa misma prueba es el guion de la reverificación.

- **Formato del cliente**: si el cliente tiene su propia skill o plantilla de entrega (ver el anexo
  privado), el documento final se redacta con ella y esta skill aporta los hallazgos confirmados. Si no la
  tiene, se entrega un informe .md o .docx según el pedido, en la carpeta de trabajo del cliente.
- **Compras públicas o clientes en la UE** que pidan un informe de conformidad: se puede entregar en formato
  ACR (plantilla VPAT, edición WCAG o EU), criterio por criterio con "Soporta / Soporta parcialmente / No
  soporta / No aplica", solo con la prueba manual completa.
- **Contexto legal**: solo los mercados del sitio, con la fecha y el nivel de evidencia. Aclara que no es
  asesoría legal.

## Reglas duras

- No decir que un sitio "cumple WCAG" ni dar un puntaje global de accesibilidad.
- No recomendar overlays o widgets de accesibilidad automática. Si el sitio tiene uno, se reporta como riesgo.
- No prometer ranking en Google por accesibilidad. El argumento es de personas, de conversión y de agentes que
  leen el árbol.
- No afirmar que el Decreto 1/2015 exige una versión de WCAG: pide "estándares de la W3C" sin versión.
- No citar WCAG 2.1 como vigente para auditar: el estándar es 2.2, y 4.1.1 Parsing no se reporta.
- No dictar implementación inferida de código minificado: comportamiento esperado más prueba de aceptación.
- No enviar formularios reales ni datos personales. Los datos de prueba son ficticios.
- No mezclar `best-practice` de axe con incumplimientos WCAG.

## Relación con otras skills

| Necesidad | Skill |
|---|---|
| Usabilidad, flujos, mensajes, jerarquía visual | `ux-heuristica` (deriva aquí lo de accesibilidad) |
| Árbol de accesibilidad para agentes, WebMCP, llms.txt | `seo-agentic` |
| Formularios que convierten | `form-cro`, `seo-conversion` |
| CLS, INP, LCP | `core-web-vitals` |
| Consentimiento y avisos de privacidad (lo legal) | `privacidad` |

Si existe `references/casos-privados.md` (anexo local, no versionado), léelo: tiene los casos reales del
entorno y sus archivos.
