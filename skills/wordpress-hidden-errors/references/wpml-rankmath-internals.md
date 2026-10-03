# Internals de WPML, Rank Math y plugins relacionados

Referencia para los endpoints temporales de lectura y escritura (Code Snippets) y para
interpretar lo que devuelve la REST.

## REST con WPML

- Sin `lang`, la REST devuelve el idioma por defecto. `lang=all` también, en la práctica.
  Pedir cada idioma por separado (`lang=en`, `lang=pt-br`...).
- `include=1,2,3` se filtra por idioma: un ID de otro idioma no vuelve. Repetir por idioma.
- La REST no expone el grupo de traducción. Fuentes alternativas: hreflang del sitemap
  de Rank Math (solo publicados) o SQL sobre `icl_translations`.
- Al crear por REST, enviar `"lang": "es"` (o el que toque) en el payload; sin él WPML
  puede no registrar el idioma y el sitemap pierde hreflang.

## Tablas de WPML

| Tabla | Uso |
|---|---|
| `{prefix}icl_translations` | `element_id`, `element_type` (`post_post`, `post_page`), `trid` (grupo), `language_code`, `source_language_code` |
| `{prefix}icl_strings` | strings registradas: `id`, `context`, `name`, `value`, `language` |
| `{prefix}icl_string_translations` | `string_id`, `language`, `value`, `status` (10 = completa) |

SQL útiles:

```sql
-- Publicados sin idioma (huérfanos)
SELECT p.ID, p.post_type, p.post_name
FROM {p}posts p
LEFT JOIN {p}icl_translations i
  ON i.element_id = p.ID AND i.element_type = CONCAT('post_', p.post_type)
WHERE p.post_status = 'publish' AND p.post_type IN ('post','page')
  AND i.translation_id IS NULL;

-- Grupo de traducción de un post
SELECT element_id, language_code FROM {p}icl_translations
WHERE trid = (SELECT trid FROM {p}icl_translations WHERE element_id = %d AND element_type = 'post_post');

-- Strings de portada
SELECT id, context, name, value FROM {p}icl_strings
WHERE name IN ('Tagline','Blog Title') OR name LIKE '%homepage_%';
```

Escribir una traducción de string: `icl_add_string_translation($id, $lang, $valor, 10)`.
Obtener un permalink en el idioma correcto dentro de un endpoint:
`do_action('wpml_switch_language', $lang); get_permalink($id); do_action('wpml_switch_language', null);`

## Rank Math — claves que importan

| Opción / meta | Dónde | Nota |
|---|---|---|
| `rank-math-options-titles[pt_page_robots]` + `pt_page_custom_robots` | opción | robots por defecto de páginas |
| `rank-math-options-titles[homepage_title]` | opción | suele ser `%sitename% %page% %sep% %sitedesc%` |
| `rank-math-options-titles[homepage_description]` / `homepage_facebook_description` | opción | strings de WPML |
| `rank-math-options-general[attachment_redirect_default]` | opción | destino de adjuntos huérfanos |
| `rank-math-options-general[redirections_fallback]` | opción | comportamiento ante 404 |
| `rank_math_robots` | post meta | array, p. ej. `['index']` |
| `rank_math_canonical_url` | post meta | canonical personalizado; excluye del sitemap si apunta fuera |
| `rank_math_lock_modified_date` | post meta | bloquea la fecha de modificación |
| `rank_math_title` / `rank_math_description` | post meta | por REST suelen no persistir; verificar en vivo |

Tabla `{prefix}rank_math_redirections`: `sources` es un array serializado
`a:1:{i:0;a:3:{s:6:"ignore";s:0:"";s:7:"pattern";s:N:"ruta/sin/barras";s:10:"comparison";s:5:"exact";}}`,
`url_to`, `header_code`, `status` (`active`/`trashed`), `hits`. La ruta del patrón no
lleva barra inicial ni final y, en multilingüe, incluye el prefijo de idioma si lo
tiene. Si dos reglas casan con la misma ruta gana la anterior: revisar antes de añadir.
La API REST de redirecciones de Rank Math no es fiable; escribir en la tabla y verificar
la respuesta (`x-redirect-by: Rank Math`).

Vaciar caché de sitemap: `\RankMath\Sitemap\Cache::invalidate_storage()`.

## Otros plugins

| Plugin | Clave | Nota |
|---|---|---|
| WP External Links | `wpel-exceptions-settings[subdomains_as_internal_links]` | `'1'` para comparar solo por host |
| Blog2Social | `B2S_PLUGIN_GENERAL_OPTIONS[og_active]`, `[card_active]` | 0 si el plugin SEO emite OG/Twitter |
| Advanced Ads | `post_type = 'advanced_ads'` | el contenido del anuncio puede contener shortcodes |
| Code Snippets | REST `code-snippets/v1/snippets` | crear con `scope: global`, borrar dos veces (`?force=true`) |
| LiteSpeed Cache | `do_action('litespeed_purge_post', $id)`, `do_action('litespeed_purge_all')` | |
| Tema (opciones) | `{tema}_theme_options[footer_copyright]` | el footer suele estar también como string WPML |

## Endpoint temporal: esqueleto

```php
add_action('rest_api_init', function () {
  register_rest_route('diag/v1', '/apply', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function ($req) { global $wpdb; $res = array();
      foreach ($req['batch'] as $b) {
        $id = intval($b['id']);
        $c = $wpdb->get_var($wpdb->prepare("SELECT post_content FROM {$wpdb->posts} WHERE ID=%d", $id));
        if ($c === null) { $res[$id] = array('ok' => false, 'err' => 'no post'); continue; }
        if (md5($c) !== $b['md5']) { $res[$id] = array('ok' => false, 'err' => 'md5'); continue; }
        $n = str_replace($b['from'], $b['to'], $c);
        if ($n !== $c) {
          $wpdb->update($wpdb->posts, array('post_content' => $n), array('ID' => $id));
          clean_post_cache($id); do_action('litespeed_purge_post', $id);
        }
        $res[$id] = array('ok' => true, 'changed' => $n !== $c ? 1 : 0, 'md5' => md5($n));
      }
      return $res; }));
});
```

`str_replace` con arrays aplica los pares en secuencia sobre todo el texto: calcular el
resultado esperado en local con el mismo orden y comparar md5.
