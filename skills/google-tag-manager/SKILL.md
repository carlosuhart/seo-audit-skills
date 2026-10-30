---
name: google-tag-manager
description: >
  Diagnóstico y configuración de Google Tag Manager: eventos que no llegan a GA4,
  dataLayer, Consent Mode v2, orden de disparo y diferencias entre Preview y Producción.
user-invokable: false
---

# Google Tag Manager — Knowledge Base

## Casos de uso cubiertos

1. Evento GTM no se registra en GA4
2. Discrepancia Preview Mode vs Producción
3. dataLayer debugging
4. Consent Mode v2 bloqueando tags
5. Firing order: GA4 Configuration Tag vs Event Tags
6. Container instalado pero no disparando

---

## Diagnóstico: Evento que no llega a GA4

### Árbol de decisión (en orden)

```
1. ¿El tag está pausado?
   GTM UI > Tags > columna Status. Si aparece "Paused", reactivar.

2. ¿El trigger tiene condiciones demasiado restrictivas?
   Revisar Every Page vs Page URL contains vs Custom Event.
   Testear con trigger más amplio para aislar.

3. ¿Preview Mode confirma que el tag dispara?
   GTM > Preview > navegar al evento.
   Si aparece en "Tags Fired" → el problema está en GA4, no en GTM.
   Si NO aparece → el problema está en el trigger o en el dataLayer.

4. ¿Consent Mode v2 está bloqueando?
   Ver sección dedicada abajo.

5. ¿GA4 Configuration Tag disparó ANTES que el Event Tag?
   Ver sección Firing Order abajo.

6. ¿El Measurement ID es correcto?
   GA4 Config Tag > Measurement ID. Debe coincidir con el stream en GA4 Admin.

7. ¿El evento llega a GA4 pero no aparece en informes?
   Los eventos tardan 24-48h en informes estándar. Verificar en DebugView primero.
```

---

## Preview Mode vs Producción

### Diferencias clave

| Comportamiento | Preview Mode | Producción |
|---|---|---|
| Ad blockers | Bypasados | Bloquean si hay reglas para GTM |
| Consent Mode | Bypasado en versiones antiguas | Aplicado según consentimiento real |
| Cache del navegador | Versión de trabajo (no publicada) | Versión publicada |
| Extensiones del navegador | Pueden interferir | Ídem |

### Implicaciones diagnósticas

- Tag dispara en Preview pero NO en producción → **primer sospechoso: Consent Mode o ad blocker**.
- Tag NO dispara en Preview → el problema es del trigger o del dataLayer, no del entorno.
- Testear siempre Preview en incógnito para eliminar extensiones y cookies persistentes.
- Después de cambios en el container: refrescar Preview con el botón "Refresh" — la sesión de debug puede quedar obsoleta.

### Cómo forzar debug en producción

Añadir `?gtm_debug=x` a la URL. Equivale a Preview Mode pero en el entorno real (con ad blockers y consent activos).

---

## dataLayer

### Estructura básica

```javascript
// Push estándar
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  'event': 'nombre_evento',
  'parametro1': 'valor1',
  'parametro2': 'valor2'
});
```

### Reglas de naming

- Los nombres de eventos en `dataLayer.push({'event': '...'})` deben coincidir **exactamente** con el nombre en el Custom Event Trigger de GTM (case-sensitive).
- Evitar espacios — usar guión bajo o camelCase.
- GA4 tiene eventos reservados que no se pueden usar como nombres personalizados: `click`, `view`, `scroll`, `session_start`, `first_visit`.

### Cómo verificar el dataLayer en consola

```javascript
// Ver el estado actual completo
console.log(dataLayer);

// Ver el último push
console.log(dataLayer[dataLayer.length - 1]);
```

En GTM Preview, pestaña "Data Layer" muestra todos los pushes en orden cronológico con sus valores.

### Variables de dataLayer en GTM

GTM UI > Variables > User-Defined Variables > Data Layer Variable.
- Layer Version: Version 2 (estándar moderno).
- Variable Name: coincide con la clave del objeto en el push.

---

## Consent Mode v2

### Contexto

Obligatorio desde marzo 2024 para sitios en el EEE. Si no está configurado, GA4 puede dejar de recibir datos de usuarios que rechazan cookies.

### Cómo bloquea los tags de GA4

Por defecto, GA4 tags respetan `analytics_storage`. Si el usuario rechaza:
- `analytics_storage: 'denied'` → GA4 Event Tags **no disparan** (o envían pings sin identificador de usuario).
- Si el tag tiene configuración Basic Consent Mode: espera al consentimiento para disparar.
- Si el tag tiene configuración Advanced Consent Mode: dispara sin cookies, envía datos modelados.

### Diagnóstico Consent Mode

1. En la consola del navegador, antes de aceptar cookies:
```javascript
// Ver el estado del consentimiento
console.log(window.dataLayer.filter(x => x[0] === 'consent'));
```

2. En GTM Preview, pestaña "Consent": muestra el estado de cada señal (`analytics_storage`, `ad_storage`, `functionality_storage`, etc.).

3. Si `analytics_storage: denied` y el tag no tiene la opción "Override consent settings" → el tag no disparará hasta que el usuario acepte.

### Configuración correcta en GTM

```
GA4 Configuration Tag:
  - Consent Settings > No additional consent required
  ó
  - Activar "Advanced Consent Mode" (envía pings modelados)

CMP (Consent Platform):
  - Debe hacer dataLayer.push con gtag('consent', 'update', {...}) al aceptar/rechazar
  - Timing: ANTES de que dispare el GA4 Configuration Tag
```

### Consent Mode implementado correctamente

```javascript
// Defaults (en el <head>, antes del snippet de GTM)
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'wait_for_update': 500
});

// Update tras aceptar (callback del CMP)
gtag('consent', 'update', {
  'analytics_storage': 'granted',
  'ad_storage': 'granted'
});
```

---

## Firing Order: GA4 Configuration Tag vs Event Tags

### El problema más común

GA4 Event Tags necesitan que el GA4 Configuration Tag haya disparado primero. Si el Event Tag dispara antes (o si la Configuration Tag no dispara en absoluto), el evento se pierde.

### Configuración correcta

| Tag | Trigger | Tag Sequencing |
|---|---|---|
| GA4 Configuration | Initialization - All Pages | Ninguno |
| GA4 Event | Custom Event / Click / etc. | "Fire a tag before" → GA4 Configuration Tag |

En GTM UI: Edit Tag > Advanced Settings > Tag Sequencing > Fire a tag before [tag name] fires.

### Por qué "Initialization - All Pages" para la Configuration Tag

El trigger "Initialization" dispara antes que "All Pages" / "Page View". Garantiza que el gtag esté disponible cuando lleguen los eventos de página.

Jerarquía de triggers (orden de disparo):
```
1. Consent Initialization
2. Initialization
3. Page View (DOM Not Ready)
4. DOM Ready
5. Window Loaded
6. Custom Events (cuando ocurren)
```

---

## Verificación en GA4 DebugView

Ruta: GA4 > Admin (columna Property) > DebugView

### Activar modo debug

**Opción 1 — GTM:** Añadir parámetro `debug_mode: true` en el GA4 Configuration Tag > Fields to Set.

**Opción 2 — URL:** Añadir `?_gl=debug` (no oficial, puede variar).

**Opción 3 — Chrome Extension:** "Google Analytics Debugger" — activa debug en toda la sesión.

### Qué confirma DebugView

- El evento llega a GA4 en tiempo real (< 1 minuto de latencia).
- Los parámetros del evento tienen los valores correctos.
- El `measurement_id` corresponde al stream correcto.

Si el evento aparece en DebugView pero no en informes → problema de definición de evento en GA4, no de tracking.

---

## Casos frecuentes en clientes

### Container GTM instalado pero sin datos en GA4

1. Verificar que el snippet de GTM está en `<head>` (noscript en `<body>`).
2. En WordPress/Divi: algunos plugins de caché sirven HTML sin GTM si el snippet se añadió después de que el caché se generó. Purgar caché.
3. En PrestaShop: verificar que el hook `displayHeader` tiene el snippet (no solo `displayFooter`).

### Evento de formulario no llega a GA4

1. ¿El formulario hace submit tradicional (recarga de página) o AJAX?
   - Submit tradicional: usar trigger "Form Submission" con "Wait for Tags" y "Check Validation".
   - AJAX: el formulario no recarga la página, el trigger "Form Submission" no dispara. Necesita Custom Event via dataLayer.push en el callback de éxito.

2. En Elementor Forms: activar "Success Message" como indicador o usar el hook `elementor_pro/forms/new_record` para hacer push al dataLayer.

3. En Contact Form 7: evento `wpcf7mailsent` disponible como Custom Event.

```javascript
// Contact Form 7 → GTM
document.addEventListener('wpcf7mailsent', function(event) {
  dataLayer.push({
    'event': 'form_submit',
    'form_id': event.detail.contactFormId
  });
}, false);
```

### Click en enlace de teléfono/email no registrado

```javascript
// GTM: Click Trigger
Trigger Type: Click - Just Links
Wait for Tags: checked (500ms)
Check Validation: checked
Trigger fires on: Click URL - contains - tel: (o mailto:)
```

---

## WooCommerce — Enhanced Ecommerce (GA4)

GA4 Enhanced Ecommerce tracking via GTM requires pushing structured `items` arrays
to the dataLayer on specific user actions. Native WooCommerce does not push these
automatically — they require custom implementation.

### Required events for GA4 Enhanced Ecommerce

| Event | When to fire | Required parameters |
|-------|-------------|---------------------|
| `view_item_list` | Product listing pages | `items[]`, `item_list_name` |
| `select_item` | Click on product in list | `items[]`, `item_list_name` |
| `view_item` | Product detail page | `items[]` |
| `add_to_cart` | Add to cart button | `items[]`, `currency`, `value` |
| `remove_from_cart` | Remove from cart | `items[]`, `currency`, `value` |
| `view_cart` | Cart page load | `items[]`, `currency`, `value` |
| `begin_checkout` | Checkout start | `items[]`, `currency`, `value` |
| `purchase` | Order confirmation page | `transaction_id`, `items[]`, `currency`, `value` |

### dataLayer push structure

```javascript
// Example: add_to_cart
dataLayer.push({
  event: 'add_to_cart',
  ecommerce: {
    currency: 'EUR',
    value: 29.99,
    items: [{
      item_id: 'SKU-123',
      item_name: 'Product Name',
      item_category: 'Category Name',
      price: 29.99,
      quantity: 1
    }]
  }
});
```

**Important:** GA4 ecommerce events require the `ecommerce` object to be
inside the dataLayer push, not as top-level keys.

### Implementation options for WooCommerce

**Option A — Plugin (recommended):**
- "Pixel Your Site" Pro: full GA4 ecommerce dataLayer out of the box
- "Duracelltomi Google Tag Manager for WordPress": includes WooCommerce ecommerce

**Option B — Custom PHP:**
```php
// Enqueue a JS file that pushes to dataLayer on add-to-cart AJAX
add_action('woocommerce_add_to_cart', function($cart_item_key, $product_id, $quantity) {
    $product = wc_get_product($product_id);
    // Build items array and output as inline JS
    wc_enqueue_js("dataLayer.push({
        event: 'add_to_cart',
        ecommerce: {
            currency: '" . get_woocommerce_currency() . "',
            value: " . $product->get_price() . ",
            items: [{ item_id: '" . $product->get_sku() . "',
                       item_name: '" . esc_js($product->get_name()) . "',
                       price: " . $product->get_price() . ",
                       quantity: {$quantity} }]
        }
    });");
}, 10, 3);
```

### `purchase` event on order confirmation

The most critical ecommerce event. Common issues:

1. **Fires on every page load** of the thank-you page, not just once.
   Fix: store `transaction_id` in a cookie/session and check before pushing.

2. **Fires in Preview Mode but not in production.**
   Cause: Consent Mode blocking before purchase confirmation.
   Fix: ensure purchase event fires even with `analytics_storage: denied`
   (use Advanced Consent Mode so GA4 receives modelado data).

3. **`transaction_id` is not unique** across orders.
   Fix: use WooCommerce order ID, not a session variable.

---

## Consent Mode with WordPress GDPR plugins

### Interaction with CMPs (GDPR plugins)

Common GDPR plugins: Moove GDPR, CookieYes, Complianz, Real Cookie Banner.

Each must push a `gtag('consent', 'update', {...})` call to the dataLayer
when the user accepts or rejects. Without this update call, GA4 tags remain
blocked indefinitely after the default `denied` state.

**Verify the update is happening:**
```javascript
// In Chrome DevTools Console after accepting cookies:
window.dataLayer.filter(item => item[0] === 'consent')
// Should show at least two entries:
// 1. default {analytics_storage: 'denied', ad_storage: 'denied'}
// 2. update {analytics_storage: 'granted', ad_storage: 'granted'}
```

**Timing issue:** If the CMP's update call fires after the GA4 Configuration Tag,
GA4 may have already initialized in `denied` state. Fix: verify the CMP fires
the update before or immediately after the GTM initialization.

**CookieYes + GTM:**
CookieYes has native GTM integration — it fires a custom event `cookieyes-accept-all`
that can be used as a trigger in GTM to update consent and fire tags.

**Complianz + GTM:**
Complianz can trigger GTM consent update via its `cmplz_after_analytics_consent` event.

### Default consent state

The `gtag('consent', 'default', {...})` call must appear in the HTML before the
GTM container snippet. If it appears after, the default state is applied after
GTM has already run.

```html
<!-- Correct order in <head> -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  // Default: deny all until user accepts
  gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'wait_for_update': 500
  });
</script>
<!-- GTM snippet AFTER the consent default -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-XXXXX"></script>
```

---

## Consent Mode en sitios con navegación sin recarga (SPA, Astro ClientRouter, Next.js)

Patrones verificados en auditorías reales. Casi todos fallan en silencio: el banner se ve bien,
el código "parece" correcto y las etiquetas igual disparan antes de aceptar, o nunca disparan
en la visita que acepta.

### 1. Primero comprobar que el consentimiento se registra de verdad — el shim de gtag

```javascript
// INCORRECTO — rest params o función flecha empujan un Array
window.gtag = window.gtag || function (...args) { window.dataLayer.push(args); };

// CORRECTO — GTM solo procesa como comando gtag el objeto `arguments`
window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
```

Con el shim incorrecto, `consent default` y `consent update` se ignoran y **todas las etiquetas
disparan sin consentimiento**. Señales: `google_tag_data.ics.entries` muestra las cuatro señales
como `{"implicit":true}` y los hits llevan `gcd=13l3l3l3l1l1`. Es un error típico de quien
"moderniza" el snippet a ES6.

**Prueba obligatoria (no basta leer el código):** navegador automatizado en contexto limpio,
leer `google_tag_data.ics.entries` y contar peticiones antes de aceptar a `g/collect`,
`clarity.ms`, `doubleclick.net`, `googlesyndication.com`, `googleadservices.com` y `google.com/ccm`.
Un regex que omita alguno de esos dominios da un falso "no sale nada".

### 2. Etiqueta bloqueada en Initialization: actualizar el consentimiento no la reevalúa

Si la etiqueta exige consentimiento adicional (`analytics_storage`) y su único activador es
Initialization, con default `denied` queda bloqueada por completo. Al aceptar, `consent update`
**no la vuelve a evaluar**. Hace falta un evento después del update y un activador de ese evento:

```javascript
gtag('consent', 'update', { analytics_storage: 'granted' });
window.dataLayer.push({ event: 'consent_update' });
```

### 3. Nunca "Una vez por página" en una etiqueta que se reactiva con consent_update

Con `once_per_load`, el intento bloqueado en Initialization **gasta la única activación de la
página** (en el runtime de gtm.js el registro de "una vez por página" envuelve también el
`onFailure`). Al aceptar, la etiqueta no dispara y **la primera visita que acepta queda sin
page_view**. Correcto:

- Opción de activación: "Una vez por evento".
- Empujar `consent_update` **solo desde el clic en Aceptar**, nunca desde la función que
  reaplica la preferencia guardada en cada carga o navegación.
- Guarda contra duplicados: empujar solo si la preferencia previa no era "aceptado" (cubre
  reabrir el banner y aceptar otra vez, y listeners apilados por la navegación sin recarga).

### 4. Google tag de Google Ads (AW-) sin consentimiento adicional = modo avanzado

Con default `denied`, la Google tag de Ads sin consentimiento adicional igual envía en cada carga
un ping sin cookies a `pagead2.googlesyndication.com/ccm/collect` con URL, IP y gclid, **también
después de rechazar**. Si el requisito es que no salga nada antes del consentimiento: exigir
`ad_storage` como consentimiento adicional y activarla con `consent_update`. Costo que hay que
comunicar: Google Ads pierde esa señal para modelar conversiones. La cookie `_gcl_aw` la escribe
la propia Google tag AW al aceptar; no depende del vinculador de conversiones.

### 5. Quién envía los page_view siguientes en una navegación sin recarga

La "página" de GTM dura toda la navegación interna: Initialization y `gtm.js` no se repiten.
Los page_view de las páginas siguientes los envía la medición mejorada de GA4 por cambios del
historial (`enhancedMeasurementSettings.pageChangesEnabled`, consultable con la Admin API
v1alpha). Comprobar que esté activa antes de afirmar que no hay pérdidas ni duplicados. Si el
banner corre en el evento de carga de cada página (p. ej. `astro:page-load`) y reaplica la
elección guardada, no empujar `consent_update` desde ahí (ver punto 3).

### 6. Criterios de aceptación para validar un cambio de consentimiento

| Escenario | Resultado esperado |
|---|---|
| Primera visita, sin interactuar | Ningún disparo de etiquetas que exigen consentimiento |
| Aceptar | Un disparo y exactamente un page_view de la página de llegada (DebugView) |
| Navegación interna tras aceptar | Un page_view por página |
| Recarga | Preferencia persistente, sin banner, un page_view |
| Rechazar | Ningún disparo; etiquetas de Ads según la decisión del punto 4 |
| Cada idioma o plantilla | Repetir la tabla |

### 7. Excepción de bloqueo para todos los eventos (filtrar entornos de prueba)

Activador de evento personalizado con regex `.*` + condición (p. ej. Page Hostname distinto del
de producción), usado como excepción en todas las etiquetas. En el contenedor compilado,
Initialization, Consent Initialization, `gtm.js` y los clics son predicados sobre la misma
variable `_event` que los eventos personalizados (`_eq _event gtm.init`), así que `.*` también
los cubre. Si alguien lo objeta, se refuta mostrando los predicados del gtm.js publicado; igual
conviene pedir que la Vista previa muestre bloqueadas las Google tags de Initialization.

### 8. Clic en un elemento hijo de un enlace

Con el activador "Clic - Solo enlaces", GTM toma como Click Element el `<a>` más cercano aunque
el clic caiga en un `<span>` interno, así que "Atributo del elemento" y Click URL leen el enlace.
El riesgo de atributo vacío es del activador "Todos los elementos" (ahí sí hace falta
`closest()`). Pedir igual una prueba de clic sobre el hijo en la validación.

### 9. Todo cambio de consentimiento mueve los KPIs

Un banner nuevo, Consent Mode o un cambio de etiquetas sube o baja sesiones, conversiones y leads
atribuidos sin que cambie el negocio. Antes de publicar: avisar la fecha a quien reporta KPIs y
a quien gestiona Ads, listar qué indicadores pueden moverse, anotar la fecha en GA4 y marcarla
como cambio de medición en toda comparación de períodos posterior.

---

## Container Snippets — Verificación de instalación

### Verificar que GTM está cargando

En consola del navegador:
```javascript
// Confirma que el objeto GTM existe
console.log(typeof google_tag_manager);

// Ver todos los containers cargados
console.log(Object.keys(google_tag_manager));
// Devuelve algo como: ['GTM-XXXXXXX']
```

### Verificar con Network tab

DevTools > Network > filtrar por `gtm.js`. Debe devolver 200. Si devuelve 404 → el container ID es incorrecto o GTM está bloqueado.

---

## Referencias

- GTM Help: https://support.google.com/tagmanager
- Consent Mode v2: https://developers.google.com/tag-platform/security/guides/consent
- GA4 Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- dataLayer spec: https://developers.google.com/tag-platform/tag-manager/web/datalayer
- GTM firing order: https://support.google.com/tagmanager/answer/6103696
