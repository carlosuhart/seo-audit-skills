---
name: seo-negativo
description: Monitoreo continuo de SEO negativo y protocolo de respuesta ante ataques — link bombing, scraping de contenido, penalizaciones manuales, reseñas falsas y ataques de reputación durante migraciones de dominio o rebrandings. Genera disavow.txt. Usar cuando el usuario mencione "SEO negativo", "ataque de backlinks", "link bombing", "scraping de contenido", "penalización manual", "reseñas falsas", "caída sospechosa de rankings", "monitoreo de reputación", "protocolo de rebranding SEO" o pida generar un archivo disavow.
metadata:
  type: skill
---

# seo-negativo

Monitoreo continuo de SEO negativo y protocolo de respuesta ante ataques. Cubre link bombing, scraping de contenido, penalizaciones manuales, reseñas falsas y ataques de reputación durante migraciones de dominio o rebrandings.

## Cuándo se activa

- `/seo-negativo audit <dominio>` — diagnóstico completo del perfil de backlinks + señales de ataque activo
- `/seo-negativo monitor <dominio>` — protocolo de monitoreo continuo: qué trackear, con qué herramientas, frecuencia
- `/seo-negativo alert <síntoma>` — respuesta ante síntoma específico (caída repentina, penalty manual, spike de links tóxicos)
- `/seo-negativo disavow <dominio>` — genera el archivo disavow.txt listo para subir a GSC
- `/seo-negativo rebranding <dominio-origen> <dominio-destino>` — protocolo específico para proteger la transición de marca

---

## Bloque 1 — Diagnóstico inicial

### Inputs requeridos
- Dominio objetivo
- Período de análisis (default: últimos 90 días)
- Acceso a GSC (para manual actions)
- Export de backlinks (Ahrefs / Semrush / DataForSEO)

### Señales de ataque activo — checklist

**Link bombing:**
- Spike de referring domains nuevos >200% en 30 días
- Anchors con keywords de spam (casino, farma, porn, payday loans)
- Dominios fuente con spam score >60
- Links desde redes de blogs privadas (PBN) o directorios masivos
- Múltiples links desde el mismo IP o C-block

**Scraping de contenido:**
- Contenido indexado en dominios distintos al origen (buscar `site:` + fragmentos del contenido)
- Fecha de indexación del scraper anterior a la del original (señal de que Google puede estar confundido)
- Canonical apuntando al scraper en lugar del original

**Penalización manual:**
- Comprobar GSC > Acciones manuales > Cualquier acción activa
- Tipos: "Patrón de links artificiales", "Contenido generado automáticamente", "Encubrimiento"
- Impacto: puede ser parcial (algunas páginas) o de sitio completo

**Ataques de reputación:**
- Reseñas falsas masivas en GBP (spike en 1-2 semanas)
- Menciones negativas coordinadas en foros (Reddit, Trustpilot, Forocoches)
- Perfiles sociales falsos suplantando la marca

### Output del diagnóstico

```
DIAGNÓSTICO SEO NEGATIVO — [dominio] — [fecha]

ESTADO GLOBAL: [LIMPIO / BAJO RIESGO / ATAQUE ACTIVO / PENALIZADO]

1. PERFIL DE BACKLINKS
   Referring domains totales: X
   Nuevos últimos 30 días: X (+X%)
   Dominios tóxicos detectados: X
   Anchors de spam: X

2. PENALIZACIONES MANUALES (GSC)
   Estado: [Ninguna / Activa — tipo]

3. CONTENIDO SCRAPEADO
   URLs detectadas: X
   ¿Google indexa el scraper?: [Sí/No]

4. REPUTACIÓN
   Reseñas GBP últimos 30 días: X (media: X/5)
   Menciones negativas detectadas: X

ACCIONES REQUERIDAS (por urgencia):
P1 [CRÍTICO]: ...
P2 [ALTO]: ...
P3 [MEDIO]: ...
```

---

## Bloque 2 — Monitoreo continuo

### Stack de herramientas por capa

| Capa | Herramienta | Frecuencia | Umbral de alerta |
|---|---|---|---|
| Backlinks nuevos | Ahrefs Alerts / GSC | Diaria | >50 nuevos RD/día |
| Tráfico orgánico | GSC + GA4 | Diaria | Caída >20% en 7 días |
| Penalizaciones | GSC Acciones manuales | Semanal | Cualquier acción nueva |
| Menciones de marca | Google Alerts / Brand24 | Diaria | Sentimiento negativo |
| Reseñas GBP | GBP Dashboard | Diaria | Rating <4.0 o spike de 1-estrella |
| Indexación | GSC Cobertura | Semanal | Caída >5% páginas indexadas |
| Uptime | UptimeRobot / StatusCake | Continuo | Downtime >2 min |

### Dashboard mínimo viable (sin herramientas paid)

1. GSC: Rendimiento (clics/impresiones 28 días), Cobertura, Acciones manuales
2. Google Alerts: `"marca"`, `"marca" site:reddit.com`, `"marca" spam`
3. Bing Webmaster Tools: backlinks (segunda fuente gratuita)
4. GBP: reseñas y Q&A
5. Ahrefs/Semrush free tier: spike mensual de referring domains

### Frecuencia de revisión recomendada

- **Diaria** (5 min): GSC clics, alertas Google, GBP
- **Semanal** (30 min): perfil de backlinks completo, indexación, menciones
- **Mensual** (2h): diagnóstico completo, actualización del disavow si necesario
- **Durante migración/rebranding**: diaria ampliada (ver Bloque 4)

---

## Bloque 3 — Protocolo de respuesta

### Escenario A — Link bombing detectado

**Criterio de activación:** >500 nuevos referring domains en 14 días con spam score >50 en >30% de ellos.

**Pasos:**
1. Exportar todos los backlinks nuevos (últimos 30 días) con spam score
2. Filtrar dominios con spam score >40 O anchors de spam
3. Generar disavow.txt (ver `/seo-negativo disavow`)
4. Subir a GSC Search Console > Desautorizar links
5. Documentar con capturas: fecha de detección, volumen, dominios fuente
6. Si hay penalización manual asociada: solicitar reconsideración tras subir el disavow (esperar 2-4 semanas entre subida y solicitud)

**Tiempo esperado de recuperación:** 2-6 semanas desde subida del disavow si no hay penalización manual. Con penalización manual: 4-12 semanas tras aprobación de reconsideración.

### Escenario B — Penalización manual activa

**Criterio de activación:** Acción manual visible en GSC.

**Pasos:**
1. Leer el tipo exacto de la acción y el alcance (parcial vs. sitio completo)
2. Identificar las URLs afectadas
3. Limpiar la causa (links artificiales: disavow; contenido spam: eliminar o noindex; encubrimiento: corregir)
4. Documentar cada acción tomada con fecha y evidencia
5. Redactar solicitud de reconsideración (formato GSC): qué pasó, qué se corrigió, por qué no volverá a ocurrir
6. Monitorear respuesta (Google tarda 2-4 semanas)

**Nota crítica:** No solicitar reconsideración antes de haber corregido TODAS las causas. Una solicitud denegada crea historial negativo.

### Escenario C — Scraping con inversión de autoridad

**Criterio de activación:** Google indexa el contenido scrapeado antes que el original, o el scraper acumula más backlinks.

**Pasos:**
1. Implementar Schema `datePublished` correcto en el original si no existe
2. Verificar que el canonical del original apunta a sí mismo
3. Enviar URLs originales a inspección en GSC para forzar crawl
4. Solicitar DMCA takedown al hosting del scraper (usar `whoishostingthis.com` + formulario DMCA de Google)
5. Si el scraper tiene backlinks valiosos: outreach directo a los sitios enlazadores para corregir el destino
6. Bloquear el scraper en `robots.txt` si es identificable por User-Agent

### Escenario D — Ataque de reseñas falsas (GBP)

**Pasos:**
1. Documentar las reseñas con capturas (fecha, texto, perfil del revisor)
2. Reportar cada reseña individualmente desde GBP como "no cumple las políticas"
3. Si el patrón es coordinado (>10 reseñas en 48h del mismo período): escalar a Google Business Support con evidencia del patrón
4. Responder públicamente a cada reseña falsa con tono profesional y neutro (no acusar directamente)
5. Activar campaña de captación de reseñas reales entre clientes verificados para diluir el efecto

---

## Bloque 4 — Protocolo rebranding (dominio-origen → dominio-destino)

Este bloque es específico para migraciones de marca donde el dominio cambia (ej. movistar.cl → tigo.cl). El riesgo de SEO negativo se multiplica durante la transición porque:
- El dominio origen pierde autoridad gradualmente y se convierte en blanco fácil
- El dominio destino empieza sin historial y es vulnerable a link bombing preventivo
- Competidores pueden comprar branded keywords del origen en paid para capturar tráfico en fuga

### Ventana de riesgo crítico: semanas 1-8 post-migración

**Semana 1-2 (post-lanzamiento dominio destino):**
- Baseline de backlinks del dominio destino el día 0 (antes de cualquier anuncio público)
- Configurar alertas de Ahrefs/Semrush en AMBOS dominios
- Activar Google Alerts para: marca nueva, marca antigua, "[marca nueva] spam", "[marca antigua] spam"
- Verificar GSC change of address completado
- Comprobar que los 301s tienen < 3 segundos de respuesta (302 o meta refresh = crisis)

**Semana 3-4:**
- Revisar perfil de backlinks del dominio origen: ¿alguien está construyendo links tóxicos al dominio origen sabiendo que tiene 301s hacia el destino?
- Revisar branded search en paid: ¿competidores pujando por la marca antigua? ¿por la nueva?
- Primer chequeo de indexación del dominio destino en GSC

**Semana 5-8:**
- Disavow preventivo si hay link bombing al origen (los 301s transfieren el daño)
- Monitoring de menciones en foros de consumidores (el rebranding genera conversación negativa orgánica — no confundir con ataque coordinado)
- Revisión de GBP: ¿se ha actualizado el nombre de la ficha? ¿hay fichas duplicadas antiguas?

**Métricas de semáforo para la transición:**

| Métrica | Verde | Amarillo | Rojo |
|---|---|---|---|
| Tráfico orgánico dominio destino (vs. baseline origen) | >80% en semana 8 | 60-80% | <60% |
| Nuevos RD tóxicos/semana | <20 | 20-100 | >100 |
| Penalizaciones manuales activas | 0 | — | Cualquiera |
| Branded search volume (marca nueva) | Creciendo | Estable | Cayendo |
| Posición media en SERP para brand queries | <3 | 3-10 | >10 |

---

## Bloque 5 — Generador de disavow.txt

### Formato esperado del export de backlinks

CSV con columnas: `url` o `domain`, `spam_score`, `anchor` (opcional).

### Criterios de inclusión en el disavow (aplicar OR — cualquier criterio es suficiente)

1. Spam score ≥ 45 (Moz) o puntuación tóxica Semrush
2. Anchor de spam: casino, pharma, adult, payday loans, "buy followers", "cheap"
3. Dominio en listas negras conocidas (StopForumSpam, Spamhaus)
4. TLD de riesgo alto: .xyz, .top, .click, .link, .pw, .tk, .cf, .ml, .ga — solo si el contenido es spam
5. Ratio links/dominio > 100 (link farm)
6. Dominio con >50% de sus links salientes hacia el mismo nicho de spam

### Output

```
# Disavow file — [dominio] — generado [fecha]
# Total dominios desautorizados: X
# Criterio de inclusión: spam score >=45, anchors de spam, link farms

domain:spam-example1.com
domain:spam-example2.net
# [sigue la lista]
```

**Instrucciones de subida:**
1. GSC > seleccionar propiedad > herramienta disavow (URL directa: search.google.com/search-console/disavow-links)
2. El archivo reemplaza el anterior — siempre incluir dominios del disavow previo más los nuevos
3. Google confirma recepción inmediatamente pero el procesamiento tarda semanas
4. Guardar copia en `claude-seo/[cliente]/disavow_[fecha].txt`

---

## Notas de uso en contexto de agencia (Havas)

- Al onboardear un cliente nuevo: ejecutar `/seo-negativo audit` antes de proponer cualquier estrategia — el baseline puede revelar ataques previos que explican caídas de tráfico históricas
- En clientes de telecomunicaciones o educación: los ataques de reseñas falsas son más comunes que el link bombing — priorizar Bloque 3 Escenario D
- Durante cualquier migración de dominio: activar Bloque 4 automáticamente desde la semana -2 (antes del lanzamiento)
- Los archivos disavow de clientes son información sensible — no incluir en repos públicos ni en auditorías compartidas con el cliente sin redacción
