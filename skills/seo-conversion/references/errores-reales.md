# Errores reales y la regla que dejaron

Cada regla salió de un diagnóstico de conversión real (sitios B2B de servicios y SaaS, y un ecommerce de alimentos) en
2026. Están anonimizadas. Si una regla choca con lo que dice la SERP o el dato del sitio, gana el dato, pero hay que
decir por qué se aparta.

## Medición

1. **Datos de desarrollo dentro de producción.** Un sitio mostraba 15 páginas por sesión; el real era 1,4. La causa
   eran sesiones desde `localhost` con el mismo ID de medición (93 páginas por sesión). Regla: revisar el hostname
   antes de leer cualquier métrica de comportamiento.
2. **Lead contado dos veces.** `generate_lead` se disparaba por el evento del formulario y por un activador de URL de la
   página de gracias. La conversión de Ads heredaba el doble. Regla: un disparo por envío; quitar activadores por URL
   cuando ya hay evento del formulario.
3. **Sesiones sin página de entrada.** Entre 8% y 12% de las sesiones orgánicas no tenía landing: el page_view inicial
   no se enviaba antes del consentimiento. Regla: medir esa proporción y declararla.
4. **Banner que no bloquea.** Un shim de `gtag` mal escrito (`function (...args) { dataLayer.push(args) }` en lugar de pasar `arguments`) hacía que GTM ignorara
   el consentimiento: se medía antes de elegir y aunque se rechazara. Regla: verificar con navegador que con el banner
   rechazado no salen peticiones, no solo leer la configuración.
5. **Tráfico interno y pruebas.** Un puñado de usuarios internos sumaba más sesiones orgánicas que muchos clientes, y
   había campañas "prueba" en los datos. Regla: filtros activos y conciliación con el CRM antes de calcular tasas.
6. **Fuente de verdad.** Ninguna de las cifras de leads de GA4 cuadraba con los tickets. Regla: el volumen viene del
   CRM o del backend; GA4 sirve para comparar páginas y canales.

## Demanda y posiciones

7. **La posición comercial era de marca.** Se informó "posición 13,5 para desarrollo de software a medida" en la página
   de servicio; todas sus impresiones venían de búsquedas con el nombre de la empresa, y la página no aparecía para la
   keyword. Regla: separar marca, sin marca y anonimizadas antes de leer la posición de una página de dinero.
8. **Volúmenes que no cuadran.** La misma keyword tenía 2.400 búsquedas en una herramienta y 90 en otra (que además daba
   20 a una variante casi igual). Regla: no planificar con una sola fuente; validar con Keyword Planner y Trends.
9. **Cero clics de compra.** Seis sitios sumaban cero clics en 90 días por búsquedas de compra sin marca, y una
   herramienta de terceros no registraba ni una keyword en el país. Regla: empezar por GSC sin marca; las herramientas
   de terceros fallan en mercados chicos.

## Páginas

10. **Proponer páginas que ya existían.** Se recomendó crear landings por módulo y por funcionalidad que estaban
    publicadas desde hacía días. Regla: listar sitemaps y revisar el sitio en vivo antes de proponer.
11. **Clics a páginas que no venden.** El 48% de los clics orgánicos a fichas llegaba a productos ocultos, agotados,
    informativos o en 404; las fichas comprables convertían 3,35% y las no comprables 0%. Regla: comprobar
    comprabilidad antes de priorizar texto.
12. **Familias que no convierten.** Las familias con más impresiones convertían 0% y la línea propia 7,5%. El plan inicial
    priorizó por visibilidad. Regla: cruzar demanda con conversión por familia, como contexto. Se recupera lo que vende
    y se sigue construyendo en lo que no vende.
13. **Redefinir el negocio.** Una landing "software para logística" definía a la empresa como especialista en algo que su
    sitio no decía. Regla: no proponer páginas que cambien el posicionamiento; presentar la demanda y consultar.

## Puente y conversión

14. **El menú no es un puente.** Cada servicio tenía unos 375 enlaces desde menú y pie, pero solo 9 a 16 páginas lo
    enlazaban dentro del contenido, y los artículos con más impresiones no enlazaban ninguno. Regla: contar enlaces en
    contexto.
15. **El CTA tapado en móvil.** El banner de cookies ocupaba el 31% del primer pantallazo y cubría el CTA de la home; el
    encabezado móvil no tenía CTA y el formulario estaba al 84-88% de páginas de 12 a 15 pantallas. Regla: revisar el
    móvil con capturas, no con el HTML.
16. **Agenda que pide datos primero.** El agendamiento exigía nombre, correo y teléfono antes de mostrar la
    disponibilidad. Regla: revisar el paso a paso del CTA hasta la confirmación.
17. **Lo que gana en la SERP de compra.** En Brasil ganaban proveedores con prueba gratis de 15 días y precios públicos;
    el cliente solo ofrecía demo y no tenía página de precios. Regla: documentarlo como dependencia de negocio con la
    evidencia de la SERP, sin prescribirlo.
18. **Lo que cita la IA cuando no está el cliente.** En cuatro preguntas comerciales a ChatGPT el cliente no aparecía; se
    citaban páginas dedicadas de competidores (por normativa, por partner, por sector), directorios y mapas. Regla:
    anotar qué se cita en su lugar; eso dice qué tipo de página o presencia falta.

## Alcance

19. **Separar lo que se puede pedir.** Un plan de 34 acciones mezclaba cosas del SEO con decisiones de pagado, gerencia y
    ventas. Regla: dividir en lo que se ejecuta o se pide a Desarrollo y lo que depende de otras áreas; lo segundo va
    como dependencia con evidencia.
20. **Cifras de proveedores.** Multiplicadores de conversión de IA (4x, 5x, 23x) circulan atribuidos a terceros. El 23x
    es de un solo sitio. Regla: medir en el sitio; citar solo con nivel de evidencia.
