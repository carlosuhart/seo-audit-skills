---
name: ga4-ai-traffic
description: Mide tráfico referido desde plataformas de AI Search (ChatGPT, Perplexity, Gemini, Copilot, Claude, Grok, Meta AI) usando datos reales de GA4. Usa este skill cuando el usuario pida "tráfico desde ChatGPT", "cuánto tráfico llega de IA", "AI referral traffic", "visitas desde Perplexity/Copilot/Gemini", "cómo va creciendo el tráfico de AI search", o cualquier medición de sesiones/usuarios que lleguen desde un asistente de IA. No confundir con geo-platform-audit (eso mide cómo te describe cada plataforma, no cuánto tráfico real envía) ni con seo-geo (auditoría de citabilidad, no de tráfico).
allowed-tools:
  - Read
  - Bash
  - Write
  - Glob
---

# GA4 AI Traffic — tráfico referido desde AI Search

Ningún otro skill instalado mide esto: `geo-platform-audit` y `seo-geo` evalúan citabilidad y percepción de marca en plataformas AI, no el tráfico real que ya está llegando desde ellas. Esta es la brecha genuina que motivó construir este skill — se detectó evaluando el MCP `thatseoagent/mcp` (2026-09-08), cuya herramienta `ga4_ai_traffic` no tiene equivalente en el stack actual. Se decidió replicar la lógica sobre el acceso a GA4 ya existente en vez de instalar el servidor de terceros.

## Autenticación

Solo funciona en sesion local: la service account de GSC no tiene scope de Analytics. Usar el token `~/ga4_gsc_token.pkl`, que ya incluye `analytics.readonly` (generado por `ga4_gsc_auth.py`). Si no existe o expiro, ejecutar `ga4_gsc_auth.py` para regenerarlo. La ruta se puede sobrescribir con la variable de entorno `GA4_TOKEN_PATH`.

Si se invoca desde un agente cloud sin acceso a ese token, decirlo explícitamente y ofrecer correrlo en sesión local — nunca inventar el número.

## Paso 0 — Resolver el GA4 Property ID

GA4 no permite matchear un dominio contra una property automáticamente (el nombre de la property es el display name que eligió el usuario, no el dominio). Pasos:

1. `py scripts/ga4_ai_traffic.py --list-properties` — lista cuentas y properties accesibles con el token actual
2. Confirmar con el usuario cuál property corresponde al dominio en cuestión si hay ambigüedad
3. Guardar el mapeo dominio→property ID en la memoria del proyecto correspondiente para no repetir esta pregunta en la siguiente sesión

## Ejecución

```bash
py "$HOME/.claude/skills/ga4-ai-traffic/scripts/ga4_ai_traffic.py" \
  --property "properties/123456789" \
  --start 2026-06-01 --end 2026-08-30 \
  [--out "<directorio-de-auditorias>/<proyecto>/ga4_ai_traffic_AAAAMMDD.json"]
```

El script corre `runReport` con dimensiones `sessionSource`, `sessionMedium`, `date`, `landingPage` y métricas `sessions`, `totalUsers`, `engagementRate`, `keyEvents` (si hay conversiones definidas — `ga4_key_events` no existe en este stack, así que si el reporte viene vacío en esa métrica, decir "sin key events configurados", nunca "cero conversiones").

### Clasificación de fuentes AI

El script matchea `sessionSource` contra esta lista y agrupa por plataforma:

| Plataforma | Dominios de origen |
|---|---|
| ChatGPT | `chatgpt.com`, `chat.openai.com` |
| Perplexity | `perplexity.ai` |
| Gemini | `gemini.google.com`, `bard.google.com` |
| Copilot | `copilot.microsoft.com`, `bing.com` (con `medium=referral` y trayecto de chat — ver límite abajo) |
| Claude | `claude.ai` |
| Meta AI | `meta.ai` |
| Grok | `grok.com`, `x.com` (marcar como "posible", ver límite abajo) |
| You.com / Phind | `you.com`, `phind.com` |

## Salida

```
## Tráfico AI Search — [property] ([start] a [end])

| Plataforma | Sesiones | Usuarios | Engagement rate | Tendencia vs. período anterior |
|---|---|---|---|---|

### Top landing pages por plataforma
| Plataforma | Página | Sesiones |
|---|---|---|

**Total tráfico AI Search: X sesiones (Y% del total de sesiones orgánicas+referral del período)**
```

Calcular la tendencia corriendo el mismo reporte sobre el período inmediatamente anterior de igual longitud.

## Límites — declarar siempre, nunca callarlos

- **Esto es un piso, no un techo.** Muchas apps de chat (ChatGPT app móvil, Copilot en Windows) no envían referrer, o lo envían como `(direct)`. El tráfico real desde AI Search es mayor al medido — decirlo en cada entrega, no solo la primera vez.
- **Copilot y Grok tienen falsos positivos.** `bing.com` mezcla búsqueda tradicional con Copilot; `x.com` mezcla redes sociales con respuestas de Grok. Reportarlos como "posible/no aislable con GA4 estándar", nunca como cifra exacta.
- **Sitios con volumen bajo:** con <100 sesiones totales en el período, cualquier desglose por plataforma es ruido. Avisarlo y sugerir ampliar el rango de fechas antes de sacar conclusiones.
- Esto mide tráfico ya generado, no potencial. Para saber por qué una plataforma no envía tráfico, encadenar con `seo-geo` o `geo-platform-audit`.

## Dependencias

- Si el hallazgo es "tráfico bajo/nulo desde una plataforma" y se quiere entender la causa → `geo-platform-audit <marca> <url>`
- Si se quiere mejorar citabilidad para elevar este número → `seo-geo` o `geo-ai-discoverability`
