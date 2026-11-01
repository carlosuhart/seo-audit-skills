# Fuentes, atribuciones y revisión

Fuentes leídas el 31/10/2026. Próxima revisión: **30/04/2027**, o antes si EN 301 549 V4.1.1 se cita
en el DOUE, si el DOJ publica una regla nueva o si sale axe-core 5.

## Normativas y oficiales

| Fuente | URL | Fecha |
|---|---|---|
| WCAG 2.2 (Recommendation) | https://www.w3.org/TR/WCAG22/ | 12/12/2024 |
| Novedades de WCAG 2.2 | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ | 05/10/2023 |
| Understanding 2.4.11, 2.5.7, 2.5.8, 3.3.8, 1.4.10, 1.4.12 | https://www.w3.org/WAI/WCAG22/Understanding/ | 2.2 vigente |
| Easy Checks del W3C | https://www.w3.org/WAI/test-evaluate/easy-checks/ | 21/03/2024 |
| Estado de WCAG 3 | https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/ | 25/09/2026 |
| Directiva (UE) 2019/882, arts. 2, 3, 4, 30, 31, 32 | https://www.legislation.gov.uk/eudr/2019/882 | 17/04/2019 |
| AccessibleEU, EN 301 549 actualizada | https://accessible-eu-centre.ec.europa.eu/content-corner/news/european-accessibility-standard-en-301-549-has-been-updated-2026-09-07_en | 07/09/2026 |
| ETSI EN 301 549 V4.1.1 | https://www.etsi.org/deliver/etsi_en/301500_301599/301549/ | 02/09/2026 |
| Ley 11/2023 (España) | https://www.boe.es/buscar/act.php?id=BOE-A-2023-11022 | 08/05/2023 |
| RDLeg 1/2013 (España), art. 83 | https://www.boe.es/buscar/act.php?id=BOE-A-2013-12632 | 29/11/2013 |
| Regla del Título II de la ADA y su prórroga | https://www.ada.gov/resources/2024-03-08-web-rule/ | 20/04/2026 |
| Sección 508 | https://www.access-board.gov/ict/ | 18/01/2017 |
| Decreto 1/2015 (Chile) | https://www.bcn.cl/leychile/navegar?i=1078308 | 11/06/2015 |
| Ley 20.422 (Chile) | https://www.bcn.cl/leychile/navegar?idNorma=1010903 | 2010 |
| Ley 21.180 (Chile) | https://www.bcn.cl/leychile/navegar?idNorma=1138479 | 2019 |
| DS 11/2023, Norma Técnica de Calidad y Funcionamiento | https://www.diariooficial.interior.gob.cl/publicaciones/2023/08/17/43629/01/2361375.pdf | 17/08/2023 |
| FTC, orden final contra accessiBe | https://www.ftc.gov/news-events/news/press-releases/2025/04/ftc-approves-final-order-requiring-accessibe-pay-1-million | 22/04/2025 |
| Google, page experience | https://developers.google.com/search/docs/appearance/page-experience | 22/09/2026 |
| Lighthouse Agentic Browsing | https://developer.chrome.com/docs/lighthouse/agentic-browsing | 05/05/2026 |
| Herramienta computer use de Anthropic | https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool | 31/10/2026 |

## Estudios, proveedores y opinión experta

| Fuente | URL | Fecha | Nivel |
|---|---|---|---|
| WebAIM Million 2026 | https://webaim.org/projects/million/ | 30/03/2026 | Estudio |
| Cobertura de axe (57,38%) | https://www.deque.com/automated-accessibility-coverage-report/ | sin fecha | Proveedor |
| Reglas de axe-core y sus etiquetas | https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md | 31/10/2026 | Oficial de la herramienta |
| Demandas web 2025 (Seyfarth) | https://www.adatitleiii.com/2026/03/federal-court-website-accessibility-lawsuit-filings-bounce-back-in-2025/ | 03/2026 | Estudio |
| Demandas digitales 2025 (UsableNet) | https://blog.usablenet.com/ada-web-lawsuit-trends-2026 | 08/01/2026 | Proveedor |
| Atajos de NVDA | https://webaim.org/resources/shortcuts/nvda | 25/09/2020 | Guía |
| VoiceOver | https://webaim.org/articles/voiceover/ | 17/06/2026 | Guía |
| Overlay Fact Sheet | https://overlayfactsheet.com/en/ | 31/10/2026 | Opinión experta colectiva |
| Mueller: la accesibilidad no es factor directo | https://www.searchenginejournal.com/google-accessibility-not-a-direct-ranking-factor/443784/ | 29/03/2022 | Portavoz, vía prensa |

## Atribuciones de código y método

- **axe-core** 4.14.0, Deque Systems, MPL-2.0 (https://github.com/dequelabs/axe-core). Se descarga con
  `setup_axe.py`, se verifica con el hash sha512 del registro npm y se usa sin modificar. No se versiona
  en el repositorio.
- **Community-Access/accessibility-agents** (MIT): categorías de severidad, clasificación sistémico /
  plantilla / página y estados de seguimiento.
- **paulunemoon/ux-audit-skill** (MIT): confianza con fuente nombrada y regla "sin evidencia no hay
  hallazgo".
- **EnchStyle/ui-ux-audit-skill** (MIT): método de foco visible por diferencia de píxeles, reimplementado
  dentro del recorrido real con Tab.
- No se reutiliza nada de Intopia (CC BY-NC-SA) ni del MCP de Deque (de pago).

## Investigación completa

Está en la carpeta de desarrollo, que no se versiona. Son dos documentos: el 01 recoge WCAG, la
cobertura de axe y el marco legal, con evidencia por fila. El 02 revisa las skills existentes y el
tooling.
