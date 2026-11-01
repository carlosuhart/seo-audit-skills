# Marco legal de la accesibilidad web (revisado al 31/10/2026)

**No es asesoría legal.** Sirve para dar contexto en el informe con la fecha de los hechos y el nivel de
evidencia. La aplicabilidad concreta a una empresa la confirma su asesor legal. Lo marcado **No
confirmado** no se usa como hecho.

## Cómo usarlo

1. Identificar dónde vende o presta servicio el sitio: idiomas, monedas, despacho y mercados
   declarados. No lo define la sede de la empresa.
2. Para cada mercado, citar la fila correspondiente con su fecha y su nivel.
3. Si no hay obligación (por ejemplo, una empresa privada en Chile), decirlo así. El argumento pasa a
   ser de negocio: clientes que no pueden completar el formulario, agentes de IA que leen el árbol de
   accesibilidad, y preparación para mercados que sí lo exigen.

## Unión Europea: European Accessibility Act (Directiva (UE) 2019/882)

| Hecho | Fecha | Nivel |
|---|---|---|
| Aplicable desde el 28/06/2025 (art. 31). | 17/04/2019 | Normativo |
| Cubre comercio electrónico (art. 3.30: contratos de consumo a distancia por web o app), banca para consumidores, transporte, comunicaciones electrónicas, servicios audiovisuales y libros electrónicos (art. 2.2). | 17/04/2019 | Normativo |
| Las microempresas que prestan servicios están exentas: menos de 10 personas y hasta 2 M€ (arts. 4.5 y 3.23). | 17/04/2019 | Normativo |
| El prestador es quien presta el servicio "en el mercado de la Unión" (art. 3.4), sin importar la sede. Los bufetes coinciden en que cubre a empresas de fuera de la UE que venden a consumidores de la UE. No hay FAQ oficial de la Comisión. | 04/2024 | Normativo + interpretación; oficial No confirmado |
| Excluye contenido de terceros no controlado, archivos no actualizados y medios grabados publicados antes del 28/06/2025 (art. 2.4). | 17/04/2019 | Normativo |
| Sanciones: cada Estado las fija, "efectivas, proporcionadas y disuasorias" (art. 30). No se encontraron sanciones ya impuestas. | 31/10/2026 | Normativo; casos No confirmado |
| La norma técnica es EN 301 549. La V3.2.1 (WCAG 2.1 AA) sigue siendo la referencia legal. La V4.1.1 (WCAG 2.2) se publicó el 02/09/2026 pero aún no está citada en el DOUE. Auditar contra 2.2 AA cubre las cláusulas web derivadas de WCAG de ambas versiones, no los requisitos que no vienen de WCAG ni las obligaciones de información de la EAA (declaración de accesibilidad). | 07/09/2026 | Guía oficial (AccessibleEU) |

**España, Ley 11/2023** (transpone la EAA): aplicable desde el 28/06/2025 y exime a las microempresas
de servicios (art. 3.3). Las sanciones siguen la normativa sectorial y, en forma supletoria, el RDLeg
1/2013, con multas de 301 € a 1.000.000 € (art. 83). Los terminales de autoservicio tienen un máximo
de 10 años. Nivel: Normativo (BOE).

## Estados Unidos

| Hecho | Fecha | Nivel |
|---|---|---|
| ADA Título III (privados): no hay reglamento técnico web. El riesgo es la litigación. | — | Inferencia |
| Seyfarth contó 3.117 demandas federales por accesibilidad web en 2025 (+27%). Nueva York y Florida concentran la mayoría. | 03/2026 | Estudio (lectura indirecta) |
| UsableNet contó más de 5.000 demandas digitales en 2025 sumando los tribunales estatales. Cerca del 70% fueron contra ecommerce. | 08/01/2026 | Proveedor |
| ADA Título II (gobiernos estatales y locales) exige WCAG 2.1 AA. Plazos aplazados por la regla del 20/04/2026: 26/04/2027 (50.000 habitantes o más) y 26/04/2028 (el resto). | 20/04/2026 | Guía oficial |
| La Sección 508 (agencias federales) sigue exigiendo WCAG 2.0 A y AA. | 18/01/2017 | Normativo |

## Chile

| Hecho | Fecha | Nivel |
|---|---|---|
| El Decreto 1/2015 (SEGPRES) rige los sitios de los órganos de la Administración del Estado. Su art. 5 pide aplicar "los estándares internacionales definidos por la W3C" **sin fijar versión ni nivel**. Que exija WCAG 2.2 es falso, aunque lo afirmen algunos proveedores. | 11/06/2015 | Normativo |
| La Norma Técnica de Calidad y Funcionamiento de la Ley 21.180 (DS 11/2023) no trata la accesibilidad. No se encontró otra norma técnica de accesibilidad posterior. | 17/08/2023 | Normativo; inexistencia No confirmado |
| Empresas privadas: no hay una obligación web específica. La Ley 20.422 da una acción general ante el juez de policía local (art. 57), con multa de 10 a 120 UTM (art. 58). No se encontró jurisprudencia sobre sitios web. | 2010 | Normativo; jurisprudencia No confirmado |
| La Ley 21.015 es de inclusión laboral y no aplica a la web. | — | No confirmado (texto no revisado) |

## Otros mercados

| País | Hecho | Nivel |
|---|---|---|
| Brasil | La Lei 13.146/2015 (LBI), art. 63, exige accesibilidad en los sitios de empresas con sede o representación comercial en el país, con símbolo visible. Su reglamentación sigue pendiente según el MPF. | Normativo (lectura indirecta); reglamentación No confirmado |
| México | La Ley General para la Inclusión de las Personas con Discapacidad fue reformada en su art. 32 (DOF 06/01/2023). Alcance para particulares sin confirmar. | No confirmado |
| Reino Unido | Las Accessibility Regulations 2018 rigen el sector público. La exigencia de 2.2 AA y el alcance de la Equality Act para privados están sin confirmar. | Normativo (2018); resto No confirmado |

## Overlays (widgets de "accesibilidad automática")

La FTC ordenó a accessiBe pagar 1 millón de USD por afirmar sin sustento que su widget hacía conformes
con WCAG a los sitios (orden final del 22/04/2025, Guía oficial). El Overlay Fact Sheet, firmado por más
de 1.000 profesionales, explica que no reparan de forma fiable el alt, las etiquetas, el teclado ni los
errores, y que pueden revelar el uso de tecnología de apoyo. **Nunca se recomiendan como solución.** Si
el sitio tiene uno, se reporta como riesgo y se recomienda corregir en el código.

## Accesibilidad y SEO

- Google no usa la accesibilidad como factor directo de ranking (John Mueller, 25/03/2022; página de
  page experience actualizada el 22/09/2026). **No se promete ranking por accesibilidad.**
- Sí comparte señales que Google y los asistentes leen: title, encabezados, alt, texto de los enlaces y
  estabilidad visual (CLS, que sí es Core Web Vital).
- Agentes de IA: según Chrome, "Agents rely on the accessibility tree as their primary data model"
  (Lighthouse Agentic Browsing, experimental, 05/05/2026). OpenAI dice que Atlas usa roles y etiquetas
  ARIA. Computer use de Anthropic trabaja con capturas y no con el árbol. Lo que se puede afirmar es que
  un árbol limpio ayuda a los agentes que lo leen, sin nombrar plataformas como lectores confirmados
  más allá de lo documentado. Para el detalle se usa `seo-agentic`.

## Pendientes de verificación (revisar el 30/04/2027)

Cita de EN 301 549 V4.1.1 en el DOUE · FAQ de la Comisión sobre empresas de fuera de la UE · sanciones
EAA impuestas · nueva propuesta del DOJ · art. 32 de la ley mexicana · reglamentación del art. 63 de la
LBI · exigencias del Reino Unido · fecha del estudio de Deque · norma técnica chilena posterior al
Decreto 1/2015.
