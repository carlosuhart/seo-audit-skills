#!/usr/bin/env python3
"""
Purpose: utilidades compartidas: clientes HTTP, snippet temporal de Code Snippets y endpoint de escritura con md5.
Config (variables de entorno):
  WP_SITE          https://www.ejemplo.com (sin barra final)
  WP_USER          usuario con application password y manage_options
  WP_APP_PASSWORD  application password
  WP_UA            User-Agent opcional (por defecto, un Chrome reciente; los WAF bloquean python/curl)
Requiere: httpx (pip install httpx[http2])
"""
from __future__ import annotations

import base64
import os
import sys
import time

import httpx

SITE = os.environ.get('WP_SITE', '').rstrip('/')
UA = os.environ.get('WP_UA', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36')


def _auth() -> str:
    user, pwd = os.environ.get('WP_USER'), os.environ.get('WP_APP_PASSWORD')
    if not (SITE and user and pwd):
        sys.exit('Faltan WP_SITE, WP_USER o WP_APP_PASSWORD en el entorno.')
    return 'Basic ' + base64.b64encode(f'{user}:{pwd}'.encode()).decode()


def public_client() -> httpx.Client:
    return httpx.Client(http2=True, headers={'User-Agent': UA}, timeout=60, follow_redirects=False)


def api_client() -> httpx.Client:
    return httpx.Client(http2=True, headers={'User-Agent': UA, 'Authorization': _auth()}, timeout=180)


APPLY_PHP = r'''
add_action('rest_api_init',function(){
 register_rest_route('wphe-diag/v1','/apply',array('methods'=>'POST',
  'permission_callback'=>function(){return current_user_can('manage_options');},
  'callback'=>function($req){global $wpdb; $res=array();
   foreach($req['batch'] as $b){ $id=intval($b['id']);
    $c=$wpdb->get_var($wpdb->prepare("SELECT post_content FROM {$wpdb->posts} WHERE ID=%d",$id));
    if($c===null){ $res[$id]=array('ok'=>false,'err'=>'no post'); continue; }
    if(md5($c)!==$b['md5']){ $res[$id]=array('ok'=>false,'err'=>'md5'); continue; }
    $n=str_replace($b['from'],$b['to'],$c);
    if($n!==$c){ $wpdb->update($wpdb->posts,array('post_content'=>$n),array('ID'=>$id)); clean_post_cache($id); do_action('litespeed_purge_post',$id); }
    $res[$id]=array('ok'=>true,'changed'=>$n!==$c?1:0,'md5'=>md5($n)); }
   return $res;}));
});'''


def snippet_create(api: httpx.Client, code: str, name: str = 'TEMP wphe-diag') -> int:
    """Crea y activa un snippet temporal. Devuelve su id."""
    r = api.post(f'{SITE}/wp-json/code-snippets/v1/snippets',
                 json={'name': name, 'code': code, 'scope': 'global', 'active': True})
    j = r.json()
    if r.status_code >= 400 or j.get('code_error'):
        sys.exit(f'No se pudo crear el snippet: {r.status_code} {j}')
    time.sleep(3)
    return int(j['id'])


def snippet_delete(api: httpx.Client, sid: int) -> None:
    """Borra el snippet (el primer DELETE lo manda a la papelera, el segundo lo elimina)."""
    for params in ({}, {'force': 'true'}):
        try:
            api.delete(f'{SITE}/wp-json/code-snippets/v1/snippets/{sid}', params=params)
        except httpx.HTTPError:
            pass
        time.sleep(1)


if __name__ == '__main__':
    # Comprobación de configuración: python scripts/wp_common.py
    auth = _auth()
    r = api_client().get(f'{SITE}/wp-json/wp/v2/users/me', params={'context': 'edit', '_fields': 'id,name,capabilities'})
    caps = r.json().get('capabilities', {}) if r.status_code == 200 else {}
    print('sitio', SITE, '| HTTP', r.status_code, '| manage_options', bool(caps.get('manage_options')))
