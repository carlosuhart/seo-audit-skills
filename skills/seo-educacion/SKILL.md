---
name: seo-educacion
description: >
  SEO para educación superior (universidades, institutos, centros de formación): funnel
  de matrícula, estacionalidad en Perú y Chile, schema Course y EducationalOrganization
  multi-sede, keywords por tier y GEO. Usar con "SEO para universidad", "captación de
  postulantes" o "schema Course".
metadata:
  type: skill
---

# seo-educacion

SEO especializado para instituciones de educación superior: universidades privadas, institutos y centros de formación. Cubre el enrollment funnel completo, estacionalidad por ciclo académico, arquitectura de contenidos por programa, schema Course y Local, y estrategia GEO/AEO para captación de leads.

## Cuándo se activa

- `/seo-educacion audit <url>` — diagnóstico SEO completo de una institución: arquitectura, keywords, schema, enrollment funnel
- `/seo-educacion brief <carrera> <país>` — brief de artículo o página para una carrera/programa específica
- `/seo-educacion keywords <programa> <país>` — keyword research orientado a enrollment: qué buscan los postulantes en cada fase del funnel
- `/seo-educacion calendario <institución> <país>` — mapa de contenidos por ciclo académico con fechas de publicación
- `/seo-educacion schema <url>` — genera schema Course, EducationalOrganization y FAQPage para una página de programa
- `/seo-educacion competidores <institución> <país>` — benchmarking SEO vs. competidores directos

---

## Bloque 1 — Contexto del sector

### El enrollment funnel en educación superior

El journey de un postulante a universidad dura 6-18 meses desde la primera búsqueda hasta la matrícula. No existe una conversión impulsiva. El SEO debe trabajar cada fase:

| Fase | Intención | Tipo de query | Contenido que gana |
|---|---|---|---|
| Awareness | "¿Qué estudiar?" | informacional genérico | artículos de orientación vocacional, comparativas de carreras |
| Consideración | "Mejores universidades para X" | informacional comparativo | rankings, páginas de programa con propuesta de valor diferencial |
| Evaluación | "Universidad X vs Universidad Y" | comparativo transaccional | landing de programa con acreditaciones, empleabilidad, malla |
| Intención | "Precio matrícula Universidad X" | transaccional | pricing page, simulador de beca, CTA de solicitud |
| Conversión | "Postular a Universidad X carrera Y" | navegacional/transaccional | formulario de postulación, landing de inscripción |
| Postventa | "Trámites matrícula Universidad X" | navegacional | portal del estudiante, instructivos |

**Implicación SEO:** El contenido de awareness construye volumen; el contenido de conversión cierra matrículas. Ambos son necesarios y no se canibalizan si la arquitectura está bien diseñada.

### Estacionalidad por ciclo académico

**Perú (ciclos semestrales — aplica a UTP, UPC, USIL, UPSJB, otras):**

| Período | Ciclo | Pico de búsqueda | Tipo de query dominante |
|---|---|---|---|
| Oct–Dic | Admisión Ciclo I (Marzo) | Pico máximo | "postular a [carrera]", "vacantes [universidad] 2025" |
| Ene–Feb | Cierre admisión Ciclo I | Alto | "fecha límite postulación", "requisitos admisión" |
| Mar–Abr | Inicio Ciclo I | Búsquedas de orientación | "[universidad] opiniones", "[carrera] salida laboral" |
| Jul–Ago | Admisión Ciclo II (Agosto/Setiembre) | Segundo pico | mismas queries que Oct-Dic |
| Sep | Cierre Ciclo II | Medio | urgencia ("últimas vacantes") |

**Chile (proceso centralizado DEMRE + admisiones especiales):**

| Período | Evento | Pico de búsqueda |
|---|---|---|
| Oct–Nov | PSU/PAES inscripción | "puntaje para [carrera] [universidad]" |
| Dic–Ene | Resultados PAES + postulación | Pico máximo anual |
| Mar–Abr | Admisión especial / segunda vuelta | "admisión sin PSU", "traslado de carrera" |
| Jul–Ago | Admisión otoño (algunas instituciones) | Pico secundario |

**Regla de los 90 días:** El contenido publicado hoy no rankea mañana. Para capturar el pico de Oct-Dic, el contenido debe estar publicado y con primeros links en Julio. Esto define el calendario editorial SEO de cualquier institución.

---

## Bloque 2 — Arquitectura de contenido

### Estructura recomendada

```
universidad.edu.pe/
├── carreras/                          ← Hub principal de programas
│   ├── [facultad]/                    ← Nivel facultad (opcional si hay muchas)
│   │   └── [carrera]/                 ← Landing de programa (página de conversión)
│   └── ...
├── admision/                          ← Hub de admisión
│   ├── requisitos/
│   ├── proceso-admision/
│   ├── becas-y-financiamiento/
│   └── fechas-importantes/
├── vida-universitaria/                ← Hub awareness
│   ├── campus/
│   ├── bolsa-de-trabajo/
│   └── testimonios/
└── blog/                              ← Hub de contenido informacional
    ├── orientacion-vocacional/
    ├── mercado-laboral/
    └── noticias-academicas/
```

### Página de programa (landing de conversión) — elementos obligatorios

1. **H1:** "[Carrera] en [Ciudad] — [Universidad]" (incluir localización)
2. **Propuesta de valor diferencial:** en las primeras 100 palabras, qué hace única a esta carrera en esta institución
3. **Tabla de información clave:**
   - Duración (semestres/años)
   - Modalidad (presencial, semipresencial, online)
   - Turno (mañana, tarde, noche, fin de semana)
   - Sede(s) disponibles
   - Costo mensual o anual aproximado
   - Acreditaciones y certificaciones
4. **Malla curricular:** resumida o enlazada (señal de confianza + keywords de asignaturas)
5. **Salida laboral:** 3-5 roles con salary benchmarks si están disponibles
6. **Requisitos de admisión:** específicos y actualizados
7. **CTA principal:** formulario de solicitud de información o botón de postulación
8. **FAQ:** mínimo 5 preguntas con schema FAQPage
9. **Schema Course** (ver Bloque 5)

### Silo de contenido informacional — ejemplo carrera de Administración

```
Hub: ¿Qué estudia un administrador de empresas? → /blog/que-estudia-administracion/
  ├── Spoke 1: ¿Cuánto gana un administrador en Perú? → /blog/sueldo-administrador-peru/
  ├── Spoke 2: ¿Qué diferencia hay entre Administración y Negocios Internacionales? → /blog/administracion-vs-negocios-internacionales/
  ├── Spoke 3: Habilidades que buscan las empresas en administradores → /blog/habilidades-administrador-empresas/
  └── Spoke 4: Carreras afines a Administración → /blog/carreras-afines-administracion/
  
Todos los spokes enlazan a: /carreras/administracion-empresas/ (la landing de conversión)
```

---

## Bloque 3 — Keyword research por programa

### Framework de keywords para educación superior

**Tier 1 — Alta intención, alta competencia (páginas de programa):**
- `[carrera] universidad [ciudad]`
- `estudiar [carrera] en [ciudad]`
- `mejor universidad para [carrera] en [país]`
- `[universidad] [carrera]`
- `postular a [carrera] [universidad]`

**Tier 2 — Intención media, menor competencia (comparativas y evaluación):**
- `[universidad A] vs [universidad B] [carrera]`
- `[carrera] acreditada [país]`
- `[carrera] online [país]`
- `requisitos para estudiar [carrera]`
- `precio carrera [nombre] [universidad]`

**Tier 3 — Informacional, construye awareness y señales E-E-A-T:**
- `qué hace un [profesión]`
- `cuánto gana un [profesión] en [país]`
- `salida laboral [carrera]`
- `diferencia entre [carrera A] y [carrera B]`
- `test vocacional [área]`

**Tier 4 — Long tail de alta conversión (poca búsqueda, máximo intent):**
- `[universidad] admisión [año]`
- `vacantes [carrera] [universidad] [ciclo]`
- `beca [nombre beca] [universidad] requisitos`
- `traslado de carrera [universidad]`
- `convalidación de materias [universidad]`

### Métricas objetivo por tier

| Tier | Volumen objetivo | KD objetivo | Página destino |
|---|---|---|---|
| 1 | 500-10.000/mes | Hasta 60 | Landing de programa |
| 2 | 100-1.000/mes | Hasta 45 | Landing de programa / comparativa |
| 3 | 200-5.000/mes | Hasta 35 | Artículo de blog |
| 4 | 10-200/mes | Hasta 25 | Landing de admisión / FAQ |

### Herramientas y flujo

1. DataForSEO MCP para volumen y KD en el país objetivo (CL, PE, CO, MX según cliente)
2. SE Ranking para posiciones actuales de la institución vs. competidores
3. GSC para identificar queries donde ya rankea pero tiene CTR bajo (título/meta a optimizar)
4. Google Trends para validar estacionalidad de cada carrera (algunas son más marcadas que otras)

---

## Bloque 4 — Benchmarking competidores

### Competidores tipo por mercado

**Perú — universidades privadas principales:**
| Institución | URL | Grupo | Fortaleza SEO |
|---|---|---|---|
| UPC | upc.edu.pe | Intercorp | Contenido de blog maduro, schema implementado |
| UTP | utp.edu.pe | Intercorp | Volumen alto de programas, SEO técnico sólido |
| USIL | usil.edu.pe | Independiente | Foco en turismo y hotelería |
| UPSJB | upsjb.edu.pe | Independiente | Ciencias de la salud |
| ESAN | esan.edu.pe | Independiente | Posgrado y MBA |
| PUCP | pucp.edu.pe | Pontificia | Autoridad institucional alta |

**Chile — universidades privadas:**
| Institución | URL | Fortaleza SEO |
|---|---|---|
| UDD | udd.cl | Contenido ejecutivo, MBA |
| UNAB | unab.cl | Volumen amplio de carreras |
| UST | ust.cl | SEO local por campus |
| UTEM | utem.cl | Técnico y tecnológico |

### Métricas de benchmarking a capturar

- Tráfico orgánico estimado (Semrush / Ahrefs)
- Keywords en top 10 por carrera relevante
- Número de páginas de programa indexadas
- Presencia de schema Course
- Velocidad de página en mobile (PageSpeed Insights)
- Autoridad de dominio (DA/DR)
- Perfil de backlinks: ¿tienen cobertura de medios? ¿rankings externos?

### Output de benchmarking

```
BENCHMARKING SEO EDUCACIÓN — [institución cliente] vs. competidores
País: [X] | Fecha: [X]

POSICIONAMIENTO GENERAL
| Institución | Tráfico orgánico est. | KWs top 10 | DA |
|---|---|---|---|
| Cliente | X | X | X |
| Competidor 1 | X | X | X |
| Competidor 2 | X | X | X |

GAPS DE KEYWORDS (competidores rankean, cliente no)
| Keyword | Competidor que rankea | Volumen | KD | Oportunidad |
|---|---|---|---|---|

GAPS DE SCHEMA
| Institución | Course | EducationalOrganization | LocalBusiness | FAQPage |

RECOMENDACIÓN: [top 3 acciones para cerrar la brecha]
```

---

## Bloque 5 — Schema markup para educación

### Schema Course — estructura completa

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Administración de Empresas",
  "description": "Carrera de Administración de Empresas con enfoque en gestión estratégica y emprendimiento. Modalidad presencial y semipresencial.",
  "provider": {
    "@type": "EducationalOrganization",
    "name": "Universidad Privada X",
    "sameAs": "https://www.universidad.edu.pe",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Av. Principal 123",
      "addressLocality": "Lima",
      "addressRegion": "Lima",
      "addressCountry": "PE"
    }
  },
  "courseMode": ["onsite", "blended"],
  "educationalCredentialAwarded": "Licenciado en Administración de Empresas",
  "occupationalCredentialAwarded": "Título Profesional",
  "timeToComplete": "P5Y",
  "offers": {
    "@type": "Offer",
    "category": "Paid",
    "priceCurrency": "PEN"
  },
  "hasCourseInstance": [
    {
      "@type": "CourseInstance",
      "courseMode": "onsite",
      "courseSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1Y",
        "startDate": "2026-03-01"
      },
      "location": {
        "@type": "Place",
        "name": "Campus Lima Norte",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Av. Los Alisos 456",
          "addressLocality": "Independencia",
          "addressRegion": "Lima",
          "addressCountry": "PE"
        }
      }
    }
  ]
}
```

**Notas de implementación:**
- `courseMode`: valores válidos — "onsite", "online", "blended"
- `timeToComplete`: formato ISO 8601 duration ("P5Y" = 5 años, "P10S" = 10 semestres)
- Si hay múltiples sedes: un `hasCourseInstance` por sede
- No poner precio específico si varía por sede/modalidad — omitir `price` en `offers`

### Schema EducationalOrganization — homepage

```json
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "Universidad Privada X",
  "alternateName": "UPX",
  "url": "https://www.universidad.edu.pe",
  "logo": "https://www.universidad.edu.pe/logo.png",
  "sameAs": [
    "https://www.facebook.com/universidadx",
    "https://www.linkedin.com/school/universidadx",
    "https://twitter.com/universidadx"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "admissions",
    "telephone": "+51-1-XXXXXXX",
    "availableLanguage": "Spanish"
  }
}
```

### Schema LocalBusiness para sedes múltiples

Cuando la institución tiene varias sedes físicas, cada sede debe tener su propia página y su propio schema:

```json
{
  "@context": "https://schema.org",
  "@type": ["EducationalOrganization", "LocalBusiness"],
  "name": "Universidad Privada X — Campus Lima Norte",
  "parentOrganization": {
    "@type": "EducationalOrganization",
    "name": "Universidad Privada X"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Av. Los Alisos 456",
    "addressLocality": "Independencia",
    "addressRegion": "Lima",
    "addressCountry": "PE"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -11.9954,
    "longitude": -77.0545
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "07:00",
      "closes": "22:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:00",
      "closes": "18:00"
    }
  ]
}
```

**Nota:** `geo` con coordenadas reales es obligatorio para elegibilidad en Google Maps y Local Pack. Siempre verificar coordenadas en Google Maps antes de incluirlas.

---

## Bloque 6 — SEO local para instituciones multi-sede

### Prioridades por sede

1. **Perfil de Google Business (GBP):** una ficha por sede, verificada, con nombre "Universidad X — Campus [nombre]"
2. **Página de sede en el sitio:** URL `/campus/[nombre-sede]/` con schema LocalBusiness
3. **NAP consistente:** Nombre, dirección y teléfono idénticos en sitio, GBP, directorios y redes sociales
4. **Reseñas:** responder al 100% de reseñas negativas en <48h; campaña de captación entre estudiantes activos
5. **Fotos:** mínimo 10 fotos en GBP por sede (instalaciones, aulas, biblioteca, cafetería)

### Keywords locales — estructura

`[carrera] [distrito/ciudad]` — ejemplo: "administración de empresas Lima Norte", "ingeniería industrial Miraflores"

Estas keywords tienen competencia mucho menor que las generales y convierten mejor porque el postulante ya sabe el área geográfica donde quiere estudiar.

---

## Bloque 7 — GEO/AEO para captación de leads

### Por qué GEO importa en educación

Los asistentes de IA son consultados cada vez más para decisiones de largo plazo con alta incertidumbre — exactamente el perfil del postulante universitario. Preguntas como "¿cuál es la mejor universidad privada para estudiar psicología en Lima?" o "¿qué carrera tiene mejor salida laboral en Perú?" aparecen en ChatGPT, Perplexity y Google AI Overviews.

### Optimizaciones específicas para captación en AI

1. **Respuesta directa en las primeras 60 palabras de cada página de programa:**
   "La carrera de [X] en [Universidad] tiene una duración de [Y] años y forma profesionales en [áreas clave]. Los egresados trabajan principalmente en [sectores] con un salario promedio de [rango] según [fuente, año]."

2. **Bloques citables de 130-170 palabras:** cada sección de la página de programa debe poder funcionar como respuesta autónoma si es extraída por un LLM.

3. **Datos verificables con fuentes:** salarios (INEI, Trabajando.com, Bumeran), tasas de empleabilidad (seguimiento de egresados si la institución lo publica), acreditaciones (SINEACE para Perú, CNAP para Chile).

4. **FAQPage schema:** las preguntas más comunes del postulante en formato FAQ con respuestas de 40-80 palabras cada una.

5. **Wikidata:** si la institución no tiene entrada verificada en Wikidata, crearla. Bing Copilot y varios LLMs priorizan entidades verificadas para recomendaciones institucionales.

6. **llms.txt:** incluir la institución, los programas principales y las URLs de cada carrera en formato machine-readable.

### Preguntas frecuentes de postulantes — base para FAQPage y contenido GEO

- ¿Cuánto cuesta estudiar [carrera] en [universidad]?
- ¿Cuántos años dura la carrera de [carrera]?
- ¿Qué requisitos necesito para postular?
- ¿[Universidad] está acreditada para [carrera]?
- ¿Cuánto gana un [profesión] en [país]?
- ¿Qué diferencia hay entre [carrera A] y [carrera B]?
- ¿[Universidad] ofrece becas? ¿Cómo aplicar?
- ¿Hay modalidad virtual para [carrera]?
- ¿Cómo es el proceso de admisión?
- ¿Puedo trasladarme desde otra universidad?

---

## Bloque 8 — Calendario editorial por ciclo (plantilla)

### Plantilla para institución con dos ciclos anuales (ejemplo: Perú)

| Mes | Acción de contenido | Tipo | Keyword objetivo |
|---|---|---|---|
| Enero | Artículos de orientación vocacional | Blog (awareness) | "qué carrera estudiar", "test vocacional" |
| Febrero | Landing de admisión Ciclo I actualizada | Página (conversión) | "postular [universidad] 2026" |
| Marzo | Testimonios de ingresantes Ciclo I | Blog (social proof) | "[universidad] opiniones", "[universidad] comentarios" |
| Abril | Artículos de salida laboral por carrera | Blog (consideración) | "cuánto gana un [profesión] en Perú" |
| Mayo | Comparativas de carreras afines | Blog (evaluación) | "[carrera A] vs [carrera B]" |
| Junio | Contenido de becas y financiamiento | Página (conversión) | "becas [universidad]", "financiamiento carrera" |
| Julio | Landing de admisión Ciclo II + urgencia | Página (conversión) | "postular [universidad] segundo ciclo 2026" |
| Agosto | Artículos de vida universitaria | Blog (awareness) | "[universidad] campus", "vida universitaria" |
| Setiembre | Cierre Ciclo II — contenido de urgencia | Blog + landing | "últimas vacantes [universidad]" |
| Octubre | Inicio anticipado admisión Ciclo I 2027 | Página (conversión) | "admisión [universidad] 2027" |
| Noviembre | Contenido PAES/admisión especial (Chile) / ECAPREV (Perú) | Blog (awareness) | keywords de examen de admisión |
| Diciembre | Balance anual + proyecciones mercado laboral | Blog (GEO/citabilidad) | "[carrera] perspectivas laborales 2027" |

---

## Notas de uso en contexto de agencia (Havas)

- El cliente universidad peruana (sin nombre confirmado al inicio del rol) es probablemente UTP o UPC (grupo Intercorp): revisar cuál de los dos tiene más gaps SEO para orientar la estrategia desde el día 1.
- Las páginas de programa son las páginas de mayor ROI — priorizar sobre blog en los primeros 90 días.
- En educación, el tiempo de resultado SEO es largo (6-12 meses). Ser explícito con el cliente sobre la regla de los 90 días para fijar expectativas realistas desde el onboarding.
- Los rankings de universidades (QS, THE, nacionales) son backlinks de altísimo valor — si la institución aparece en alguno, asegurarse de que el link apunta al dominio correcto.
- Nunca incluir precios exactos en el schema o en las meta descriptions sin verificar que están actualizados en el sitio — en educación cambian cada ciclo.
