# Medición, atribución y calidad del lead

Fuentes leídas el 23/10/2026. Niveles entre corchetes (ver `fuentes.md`). Revisar a los 6 meses.

## Lo que hay que saber antes de medir leads orgánicos

**Evento clave frente a conversión.** En GA4, un lead orgánico se mide como *evento clave*; solo es "conversión" si se
importa en Google Ads [Documentado, support.google.com/analytics/answer/13965727].

**Eventos recomendados de leads** [Documentado, developers.google.com/analytics/devguides/collection/ga4/reference/events,
actualizada 16/09/2026]: `generate_lead`, `qualify_lead`, `disqualify_lead`, `working_lead`, `close_convert_lead`,
`close_unconvert_lead`. Alimentan el informe de leads perdidos y descalificados. `form_submit` de la medición mejorada
registra el envío, no que haya funcionado: no sirve como evento clave de lead. Usar `generate_lead` en la confirmación
del servidor o en la página de gracias, una sola vez por envío.

**Filtros.** Tráfico interno por IP (`traffic_type`) y de desarrolladores (`debug_mode`); 24 a 36 horas en aplicarse; lo
excluido no se recupera [Documentado, answer/10104470 y 7201382]. No existe filtro por hostname: localhost, staging o
dominios ajenos se bloquean en GTM y se vigilan con la dimensión Hostname [criterio de práctica].

**Canal de IA.** GA4 tiene canal predeterminado "AI Assistant" (medium `ai-assistant`; ChatGPT, Gemini, Copilot,
Deepseek, Grok, entre otros). AI Overviews y AI Mode siguen dentro de Organic Search [Documentado, answer/9756891;
fecha de lanzamiento 13/05/2026 según prensa]. Para fechas anteriores, regex sobre la fuente. El etiquetado de los
asistentes no es constante (fallo de ChatGPT sin UTM ni referrer el 14/10/2026, corregido al día siguiente) [Proveedor].

**Retención.** 2 o 14 meses; afecta solo exploraciones y embudos [Documentado, answer/7667196]. En la práctica las
propiedades nuevas quedan en 2 meses: verificar en Admin.

**Atribución.** Modelos disponibles: data-driven, último clic pagado y orgánico, último clic de canales pagados de Google;
primer clic, lineal y similares retirados en noviembre de 2023; ventana por defecto 90 días [Documentado,
answer/10596866 y 10597962]. Los informes de adquisición usan su propio ámbito (sesión o primer usuario): un mismo
`generate_lead` cambia de canal según el informe. Anotar siempre modelo y ventana.

## Consentimiento

- Modo básico: si el usuario rechaza, las etiquetas no se disparan y no llega nada. Modo avanzado: llegan pings sin
  cookies y se puede modelar [Documentado, developers.google.com/tag-platform/security/concepts/consent-mode, 30/07/2026].
- Umbral de modelado de comportamiento en GA4: al menos 1.000 eventos diarios con `analytics_storage` denegado durante
  7 días y 1.000 usuarios diarios con consentimiento en 7 de los 28 días previos [Documentado, answer/11161109]. En Google
  Ads: 700 clics en 7 días por país y dominio [Documentado, google-ads/answer/10548233].
- Consecuencia: la mayoría de los sitios de servicios no llega al umbral. GA4 subcuenta los leads orgánicos en una
  proporción cercana a la tasa de rechazo del banner. El volumen se toma del CRM o del backend.

## Calidad del lead

- **Conversiones mejoradas para leads**: datos del formulario hasheados (email o teléfono) y luego importación del lead
  convertido con esos datos [Documentado, google-ads/answer/15713840]. Desde el 15/06/2026 las cargas de conversiones
  offline y de conversiones mejoradas para leads migran a la Data Manager API y quedan bloqueadas en la Google Ads API.
  Es medición de Ads: para el orgánico sirve como referencia de método, no como fuente.
- **Orgánico vía GA4**: Measurement Protocol permite enviar `qualify_lead` o `close_convert_lead` desde el CRM. El
  `client_id` debe coincidir con el del tag y los eventos se pueden fechar hasta 72 horas atrás [Documentado,
  developers.google.com/analytics/devguides/collection/protocol/ga4]. Por eso el formulario debe guardar el `client_id`
  (cookie `_ga`) en un campo oculto que llegue al CRM. Si la calificación tarda más de 72 horas, usar importación de
  eventos (no se une al histórico) o medir en el CRM.
- **Conciliación mensual**: leads del CRM frente a `generate_lead`. Una brecha mayor que la tasa de rechazo del banner es
  un fallo de medición.

## WhatsApp, llamadas y agenda

- WhatsApp: el clic a `wa.me` es un evento `click` saliente; mide intención, no que el mensaje se haya enviado
  [Documentado, answer/9216061]. Crear evento propio con `lead_source=whatsapp` y poner un código de origen en el
  `?text=` (por ejemplo "Hola, vengo de la página X") para conciliar en WhatsApp Business o el CRM.
- Llamadas: los números de desvío de Google solo atribuyen llamadas que vienen de un anuncio [Documentado,
  google-ads/answer/6095883]. Para el orgánico, número dinámico de un proveedor o, como mínimo, el clic en `tel:`.
  El número real sigue en el HTML, en el schema `telephone` y en el Perfil de Empresa.
- Agenda (Calendly y similares): iframe de terceros; la confirmación se captura por `postMessage` o webhook al backend
  y Measurement Protocol [No confirmado por proveedor].

## Atribución declarada ("¿Cómo nos conociste?")

No hay estudio con metodología revisada que compare formatos [No confirmado]. Práctica recomendada: campo opcional,
lista con "Otro" y texto libre, sin opción preseleccionada, con "ChatGPT u otro asistente de IA" y "Búsqueda en Google"
separados. Se guarda junto al canal medido, no lo reemplaza: mide influencia recordada, con sesgo de memoria.

## Tráfico desde IA: cómo reportarlo

Ahrefs: el 0,5% de sus visitas, las que llegan desde IA, generó el 12,1% de sus registros en 30 días [Un sitio,
ahrefs.com/blog/ai-search-traffic-conversions-ahrefs, 16/06/2025]. En un estudio de unos 3.000 sitios, la IA aportaba
0,17% de los visitantes [Estudio de proveedor, ahrefs.com/blog/ai-traffic-study, 06/02/2025]. Con volúmenes así, una
tasa de conversión de IA calculada sobre pocas sesiones no es estable: reportar números absolutos, nunca solo el
multiplicador.

## Checklist de la puerta de medición

Si falla un punto, el diagnóstico es "condicionado a medición". `medicion_ga4.py` cubre los marcados con (s).

1. (s) Evento de lead existe, es único por envío y se dispara en la confirmación, no en el clic. Probar con DebugView.
2. (s) Está marcado como evento clave desde antes del período analizado (no es retroactivo).
3. Cuadra con el backend: CRM o correo del formulario frente a `generate_lead`, mismo mes.
4. Filtro de tráfico interno activo (no en Testing), con las IP vigentes de la oficina y la agencia.
5. Filtro de desarrolladores activo y sin `debug_mode` en el contenedor publicado.
6. (s) Sin hostnames ajenos con datos (localhost, staging, previews, herramientas de prueba).
7. Referencias no deseadas configuradas (pasarelas de pago, SSO, dominios de agenda).
8. Modo de consentimiento identificado (Tag Assistant con el banner rechazado) y cobertura estimada.
9. (s) Retención de 14 meses.
10. Modelo y ventana de atribución anotados en el informe.
11. WhatsApp, llamadas y agenda con evento propio y `lead_source`.
12. (s) Canal de IA visible ("AI Assistant" o regex de respaldo).
13. `client_id` (y gclid si existe) guardado en el lead para medir calidad.
14. "¿Cómo nos conociste?" en el formulario, guardado junto al canal medido.

Señales adicionales que entrega el script: sesiones orgánicas sin página de entrada (el page_view inicial no llega por
consentimiento o etiqueta) y eventos de lead que no están marcados como clave.
