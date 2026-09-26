# Referentes de CTR por posición (2026)

Referencia para interpretar correctamente el CTR de las queries analizadas. Estos datos son contextuales, no absolutos. Siempre comparar contra el CTR promedio del propio sitio como línea base principal.

## La realidad del CTR en 2026

El concepto de "CTR correcto por posición" se debilitó significativamente. En 2026 el CTR depende de múltiples factores simultáneos:

- Intención de búsqueda (informacional vs transaccional vs navegacional)
- Dispositivo (escritorio vs móvil tienen diseños y profundidad de desplazamiento diferentes)
- Características de la SERP presentes (paquete local, preguntas relacionadas, compras, videos, panel de conocimiento)
- Presencia de AI Overview (el factor de mayor impacto negativo)
- Sesgo de marca (queries de marca inflan el CTR artificialmente)

Cualquier referente debe tratarse como punto de partida, no como verdad absoluta.

## CTR por posición: SERPs sin AI Overview

Fuente: Metaanálisis de First Page Sage y datos agregados de múltiples estudios (2025-2026).

| Posición | CTR estimado | Rango realista |
|----------|-------------|----------------|
| 1 | ~28-34% | 20-40% según intención |
| 2 | ~15-18% | 12-22% |
| 3 | ~10-12% | 8-15% |
| 4 | ~7-8% | 5-10% |
| 5 | ~5-6% | 3-8% |
| 6 | ~4-5% | 2.5-6% |
| 7 | ~3-4% | 2-5% |
| 8 | ~2.5-3.5% | 1.5-4% |
| 9 | ~2-3% | 1.2-3.5% |
| 10 | ~1.8-2.5% | 1-3% |
| 11-20 | <1.5% | Variable, mucho menor |

## CTR por posición: SERPs CON AI Overview

El impacto de AI Overviews es severo, especialmente en posición 1.

Datos relevantes:
- Posición 1 con AI Overview: el CTR cae aproximadamente un 50% o más frente a SERPs sin AI Overview
- Ahrefs estimó (diciembre 2025) que la presencia de AI Overview se correlaciona con un CTR promedio 58% menor para la página en posición 1
- CTR general en queries con AI Overview: ~0.64% promedio frente a ~2.8-3.8% sin AI Overview (datos de Seer Interactive)
- El CTR para queries SIN AI Overview subió de 2.8% (enero 2025) a 3.8% (febrero 2026), lo que indica que las SERPs sin AI se están volviendo más valiosas

## Señales de presencia de AI Overview en los datos

No siempre se puede verificar directamente si hay AI Overview, pero los datos de GSC dan pistas:

| Señal en los datos | Causa probable |
|-------------------|----------------|
| Posición 1-3 con CTR < 5% en query informacional | AI Overview o fragmento destacado absorbiendo clics |
| Impresiones altas + CTR muy bajo + posición buena | SERP saturada de características (AI Overview, preguntas relacionadas, videos) |
| CTR bajó significativamente en últimos 12 meses sin cambio de posición | Probable expansión de AI Overview a esa query |

## Cómo usar estos referentes en el análisis

1. **Calcular el CTR esperado** para la posición de cada query (usando la tabla sin AI Overview como techo)
2. **Comparar con el CTR real** reportado en GSC
3. **Si el CTR real < 50% del esperado:** Investigar causa (AI Overview, snippet malo, desajuste de intención)
4. **Si el CTR real > esperado:** Aprender de ese resultado (¿qué hace bien el snippet?)

## Diferencias por tipo de intención

| Tipo de intención | CTR típico posición 1 | Sensibilidad a AI Overview |
|-------------------|----------------------|---------------------------|
| Navegacional | 40-60% | Baja (el usuario busca un sitio específico) |
| Transaccional | 25-35% | Media (depende si hay anuncios de compras) |
| Comercial/comparativa | 15-25% | Media-Alta |
| Informacional | 15-30% | Muy alta (principal objetivo de AI Overviews) |

## Diferencias por dispositivo

- Escritorio: CTR generalmente mayor en posiciones 1-3
- Móvil: CTR se distribuye más uniformemente; posiciones 4-6 capturan mayor porcentaje relativo que en escritorio
- La caída de impresiones de septiembre 2025 afectó más a datos de escritorio (la mayoría de rastreadores usaban escritorio)

## Tendencias clave para 2026

- La brecha de CTR entre posición 1 y posiciones 6-10 se está cerrando (posiciones 6-10 obtienen ~30% más clics que antes)
- Queries transaccionales y locales mantienen CTR más estable (menos afectadas por AI Overviews)
- La marca como factor de CTR gana importancia: los usuarios reconocen marcas y hacen clic incluso en posiciones inferiores
- Contenido con diferenciación clara (datos propios, herramientas, análisis original) mantiene mejor CTR frente a AI Overviews

## Implicaciones para la minería de impresiones

Al analizar queries de alta oportunidad:

1. **Queries informacionales en posición 1-5 con CTR bajo:** Antes de optimizar el snippet, verificar si AI Overview es la causa. Si lo es, la optimización de título/meta tiene límite. Considerar optimizar para ser citado en el AI Overview (estructura clara, respuestas directas, datos factuales).

2. **Queries transaccionales/comerciales en posición 5-15 con CTR bajo:** Aquí sí hay alto potencial de mejora de CTR vía títulos y metas. Estas queries son menos afectadas por AI Overviews.

3. **Queries en posición 6-10 con impresiones altas:** Estas posiciones están ganando valor relativo. Una mejora de posición de 8 a 5 puede tener mayor impacto en CTR que hace 2 años.

4. **No asumir que todo CTR bajo es problema del snippet.** Puede ser estructura de la SERP. Cruzar con tipo de intención antes de sugerir reescritura.
