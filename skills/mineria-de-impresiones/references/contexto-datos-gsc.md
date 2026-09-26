# Contexto de datos GSC (2025-2026)

Referencia obligatoria antes de interpretar datos de Google Search Console. Los datos de GSC entre mayo 2025 y abril 2026 tienen problemas documentados que afectan directamente al análisis de minería de impresiones.

## Dos eventos que cambiaron los datos de GSC

### Evento 1: Eliminación del parámetro &num=100 (septiembre 2025)

**Qué pasó:** Entre el 10 y 14 de septiembre de 2025, Google dejó de soportar el parámetro &num=100, que permitía cargar 100 resultados por página en vez de 10. Las herramientas de seguimiento SEO usaban este parámetro de forma masiva.

**Impacto en los datos:**
- Las impresiones cayeron entre 20-50% de un día para otro en la mayoría de sitios
- Las posiciones promedio "mejoraron" artificialmente (datos más limpios)
- Los clics NO se vieron afectados
- El 87.7% de los sitios analizados (muestra de 319) experimentaron caídas de impresiones

**Por qué afectaba las impresiones:** Cada vez que una herramienta de seguimiento cargaba 100 resultados, TODAS las URLs en esa página recibían una impresión en GSC, aunque ningún humano las hubiera visto. Un sitio en posición 65 recibía "impresiones" cada vez que un bot rastreaba los resultados.

**Qué significa para el análisis:**
- Datos de impresiones ANTES de septiembre 2025 están inflados (especialmente para posiciones >10)
- Datos de impresiones DESPUÉS de septiembre 2025 son más precisos y reflejan visibilidad humana real
- Las comparaciones interanuales que crucen septiembre 2025 son poco fiables
- Octubre 2025 en adelante debe tratarse como nueva línea base para impresiones

### Evento 2: Error de registro de impresiones (mayo 2025 - abril 2026)

**Qué pasó:** Google confirmó un error de registro que afectó el reporte de impresiones en Search Console desde el 13 de mayo de 2025 hasta el 27 de abril de 2026. Google lo marcó como resuelto después de esa fecha.

**Impacto en los datos:**
- Las impresiones reportadas durante ese período fueron más altas de lo real
- El CTR calculado fue más bajo de lo real (denominador inflado)
- Los clics NO fueron afectados
- La posición promedio también pudo verse distorsionada
- Google no cuantificó la magnitud de la inflación
- Estimaciones de la industria sugieren entre 30-50% de inflación en impresiones

**Qué significa para el análisis:**
- Todo dato de impresiones entre mayo 2025 y abril 2026 debe interpretarse con cautela
- El CTR real probablemente era MAYOR que el reportado durante ese período
- Los clics son la métrica más confiable de todo el período
- Después de abril 2026, los datos se normalizaron

### Evento 3: Integración de AI Mode en datos de GSC (junio 2025)

**Qué pasó:** Desde el 17 de junio de 2025, Google comenzó a contar clics, impresiones y datos de posición de AI Mode dentro del informe de rendimiento de GSC. Los datos de AI Mode se mezclaron con el tipo de búsqueda "Web" sin filtro dedicado para separarlos.

**Impacto en los datos:**
- Los datos de resultados orgánicos clásicos, fragmentos destacados, AI Overviews y AI Mode están todos mezclados bajo "Web"
- La posición se calcula de forma diferente para cada superficie
- Las preguntas de seguimiento en AI Mode reinician la posición a 1
- No hay forma nativa en GSC de separar datos de AI Mode del resto

## Guía práctica: Cómo interpretar según el período

### Datos anteriores a mayo 2025
- Impresiones relativamente confiables (con la salvedad del parámetro &num=100)
- Buenos para línea base antes de AI Overview a escala
- CTR más representativo de la realidad

### Datos de mayo 2025 a septiembre 2025
- Impresiones afectadas por el error de registro Y por el parámetro &num=100
- Período menos confiable para impresiones
- Clics siguen siendo confiables
- Usar con precaución para minería de impresiones

### Datos de septiembre 2025 a abril 2026
- Se eliminó la inflación por &num=100 (mejora)
- Pero el error de registro seguía activo (impresiones aún infladas)
- Datos mixtos con AI Mode sin filtro
- Clics confiables. Impresiones: interpretar con margen

### Datos posteriores a abril 2026
- Error de registro resuelto
- Sin inflación por &num=100
- Datos más limpios y precisos
- AI Mode sigue mezclado pero las impresiones son reales
- MEJOR PERÍODO para análisis de minería de impresiones

## Cómo comunicar esto al usuario

Si el usuario comparte datos de un período afectado, informar de forma práctica sin alarmar:

**Ejemplo de comunicación:**

> Ojo: tus datos son del período [X], cuando Google tenía un error de registro que inflaba las impresiones reportadas. Los clics son confiables, pero las impresiones (y por tanto el CTR) pueden estar distorsionados. Voy a priorizar usando los clics como señal principal y tratar las impresiones como indicador relativo, no absoluto.

**Si los datos son posteriores a abril 2026:** No mencionar el tema a menos que el usuario pregunte. Los datos son limpios.

## Recomendaciones específicas para el análisis

1. **Priorizar por clics, no solo por impresiones** cuando los datos son del período afectado
2. **No sacar conclusiones de tendencias de CTR** que crucen los puntos de quiebre (septiembre 2025, abril 2026)
3. **Las impresiones relativas siguen siendo útiles** (si la query A tiene 3 veces más impresiones que la query B, esa proporción probablemente se mantiene aunque ambas estén infladas)
4. **Sugerir al usuario exportar datos recientes** (posteriores a abril 2026) si sus datos son del período problemático y la decisión es importante
5. **Para análisis de CTR por posición:** Usar los referentes con la salvedad de que el CTR reportado puede ser artificialmente bajo

## Exportar datos históricos: ventana limitada

GSC retiene datos de 16 meses. Después de ese período, los datos se pierden. Si el usuario necesita conservar datos históricos para comparaciones futuras, recomendar:

- Exportar a Google Sheets o Looker Studio de forma regular
- Conectar GSC con BigQuery para retención a largo plazo
- Anotar los puntos de quiebre (septiembre 2025, abril 2026) en cualquier panel de control

La ventana de 16 meses significa que a mediados de 2026, los datos previos a AI Overview a escala (antes de mayo 2025) ya se están perdiendo. Si el usuario no los exportó, esa línea base desapareció.
