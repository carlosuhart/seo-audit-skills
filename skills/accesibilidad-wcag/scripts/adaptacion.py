"""Adaptación del contenido y estructura: reflow, zoom, espaciado de texto, idioma, puntos de referencia.

Complementa a axe en criterios que dependen del renderizado. Devuelve CANDIDATOS con selector; se
confirman mirando la captura antes de reportarlos.

Criterios que alimenta:
  1.4.10 Reflow            a 320 px CSS de ancho no debe haber scroll horizontal (salvo tablas, mapas,
                           gráficos y similares, que el criterio exceptúa)
  1.4.4  Texto a 200%      equivalente: vista de escritorio a 640 px CSS (1.280 al 200%); se mira scroll
                           horizontal y cuánto alto de pantalla ocupan los elementos fijos
  1.4.12 Espaciado         se aplica la hoja de 1.4.12 y se listan textos que pasan a quedar recortados
  3.1.1  Idioma            atributo lang del documento y si coincide con lo esperado (--idioma)
  1.3.1 / 2.4.1 / 2.4.2    puntos de referencia (main, nav, header, footer), encabezados y title
  Árbol de accesibilidad   se guarda el aria_snapshot de Playwright (YAML) como evidencia y para seo-agentic

Uso (PowerShell):
  py scripts/adaptacion.py https://sitio.cl/ https://sitio.cl/servicios --idioma es --out <dir>
  py scripts/adaptacion.py --urls-archivo urls.txt --bloquear-host <servicio-geoip> --out <dir>

Salida: <out>/adaptacion_<slug>.json, <out>/arbol_<slug>.yml y capturas de 320 px en <out>/capturas/.
"""
from __future__ import annotations

import argparse
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import navegador as nav  # noqa: E402

CSS_1412 = """* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
p { margin-bottom: 2em !important; }"""

JS_DESBORDES = r"""() => {
  const U = window.__a11y; const W = document.documentElement.clientWidth; const out = [];
  const exento = el => el.closest('table, pre, code, [role=grid], [role=img], canvas, svg, iframe, video, [class*=map], [class*=chart], [class*=carousel], [class*=slider], [class*=swiper]');
  // contenedor con scroll propio (auto/scroll): permitido. Con hidden/clip el contenido que sobresale se PIERDE.
  const contenedor = el => { let e = el.parentElement; while (e && e !== document.body && e !== document.documentElement) { const s = U.cs(e);
      if (['auto','scroll'].includes(s.overflowX)) return 'scroll'; if (['hidden','clip'].includes(s.overflowX)) return 'recorta';
      e = e.parentElement; } return null; };
  for (const el of document.querySelectorAll('body *')) {
    if (out.length >= 30 || !U.visible(el)) continue; const r = el.getBoundingClientRect();
    if (r.right <= W + 1 || r.width < 20) continue;
    const c = contenedor(el); if (c === 'scroll') continue;
    // solo el elemento más externo que desborda
    if (el.parentElement && el.parentElement.getBoundingClientRect().right > W + 1 && contenedor(el.parentElement) !== 'scroll') continue;
    const tieneTexto = (el.innerText || '').trim().length > 0;
    if (c === 'recorta' && !tieneTexto && !el.matches('a, button, input, select, img')) continue; // decoración recortada
    out.push({sel: U.sel(el), tag: el.tagName.toLowerCase(), derecha_px: Math.round(r.right), ancho_vista: W,
              exento_posible: !!exento(el), recortado: c === 'recorta', texto: (el.innerText || '').trim().slice(0, 60)});
  }
  return {scroll_width: document.documentElement.scrollWidth, client_width: W, desbordes: out};
}"""

JS_FIJOS = r"""() => { const U = window.__a11y; const H = innerHeight; const out = [];
  for (const el of document.querySelectorAll('body *')) { const s = U.cs(el);
    if (!['fixed','sticky'].includes(s.position) || !U.visible(el)) continue; const r = el.getBoundingClientRect();
    if (r.height < 20 || r.width < innerWidth * 0.5) continue;
    if (el.parentElement && ['fixed','sticky'].includes(U.cs(el.parentElement).position)) continue;
    const bg = s.backgroundColor; const transparente = (bg === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(bg))
      && s.backgroundImage === 'none' && s.boxShadow === 'none';
    out.push({sel: U.sel(el), posicion: s.position, alto_px: Math.round(r.height), pct_alto_vista: Math.round(r.height / H * 100),
              contenedor_transparente: transparente}); }
  return out; }"""

JS_RECORTES = r"""() => { const U = window.__a11y; const out = [];
  for (const el of document.querySelectorAll('body *')) {
    if (out.length >= 60 || !U.visible(el)) continue;
    const tieneTexto = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2);
    if (!tieneTexto) continue; const s = U.cs(el);
    const ocultaY = ['hidden','clip'].includes(s.overflowY) || ['hidden','clip'].includes(s.overflow);
    const ocultaX = ['hidden','clip'].includes(s.overflowX) || ['hidden','clip'].includes(s.overflow);
    const recY = ocultaY && el.scrollHeight > el.clientHeight + 2;
    const recX = ocultaX && el.scrollWidth > el.clientWidth + 2;  // los puntos suspensivos también pierden texto
    const clamp = s.webkitLineClamp && s.webkitLineClamp !== 'none';
    if (recY || recX || (clamp && el.scrollHeight > el.clientHeight + 2))
      out.push({sel: U.sel(el), texto: (el.innerText || '').trim().slice(0, 60), eje: recY ? 'vertical' : 'horizontal',
                line_clamp: !!clamp, puntos_suspensivos: s.textOverflow === 'ellipsis'});
  }
  return out; }"""

# 1.4.12: el fallo más común no es el recorte sino el texto que se sale de una caja de alto fijo y se monta
# sobre el bloque siguiente. Se comparan solapes entre bloques de texto hermanos antes y después.
JS_SOLAPES = r"""() => { const U = window.__a11y; const out = [];
  const bloques = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,label,button,a,dt,dd,figcaption,td,th')]
    .filter(e => U.visible(e) && (e.innerText || '').trim().length > 2).slice(0, 600);
  const rect = e => e.getBoundingClientRect();
  const fijo = e => { for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const p = U.cs(x).position;
    if (p === 'fixed' || p === 'sticky') return true; } return false; };
  for (let i = 0; i < bloques.length && out.length < 40; i++) { const a = bloques[i], ra = rect(a);
    for (let j = i + 1; j < Math.min(bloques.length, i + 8); j++) { const b = bloques[j];
      if (a.contains(b) || b.contains(a)) continue; const rb = rect(b);
      const x = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left), y = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
      // con una capa fija (cabecera que crece al espaciar) el solape depende del scroll: se marca aparte
      if (x > 4 && y > 4) out.push({par: U.sel(a) + ' || ' + U.sel(b), texto: (a.innerText || '').trim().slice(0, 40),
                                     con_capa_fija: fijo(a) || fijo(b)}); } }
  return out; }"""

JS_ESTRUCTURA = r"""() => { const U = window.__a11y;
  const cuenta = q => [...document.querySelectorAll(q)].filter(U.visible).length;
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role=heading]')].filter(U.visible)
     .map(h => ({nivel: h.getAttribute('aria-level') || h.tagName[1], texto: (h.innerText || '').trim().slice(0, 70)}));
  return {lang: document.documentElement.getAttribute('lang'), title: document.title,
    main: cuenta('main, [role=main]'), nav: cuenta('nav, [role=navigation]'), header: cuenta('body > header, [role=banner]'),
    footer: cuenta('body > footer, [role=contentinfo]'), h1: hs.filter(h => String(h.nivel) === '1').length,
    encabezados: hs.slice(0, 60), meta_viewport: (document.querySelector('meta[name=viewport]') || {}).content || null};
}"""


def medir(browser, url: str, ancho: int, alto: int, movil: bool, hosts, captura: str | None) -> dict:
    vista = "movil" if movil else "escritorio"
    ctx = nav.nuevo_contexto(browser, vista)
    page = ctx.new_page()
    page.set_viewport_size({"width": ancho, "height": alto})
    nav.instalar_bloqueos(page, hosts, False)
    http = nav.abrir(page, url)
    if http is None:
        ctx.close()
        return {"error": "no se pudo abrir"}
    nav.recorrer_scroll(page)
    d = page.evaluate(JS_DESBORDES)
    d["http"] = http
    d["fijos"] = page.evaluate(JS_FIJOS)
    if captura:
        page.screenshot(path=captura, full_page=False)
        d["captura"] = os.path.basename(captura)
    ctx.close()
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls-archivo")
    ap.add_argument("--idioma", help="idioma esperado de la página (es, en, pt...)")
    ap.add_argument("--bloquear-host", action="append")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out_dir = nav.carpeta_salida(a.out)
    dir_cap = nav.carpeta_salida(os.path.join(out_dir, "capturas"))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for url in nav.leer_urls(a.urls, a.urls_archivo):
            s = nav.slug(url, 50)
            res = {"url": url, "fecha": nav.ahora()}
            # 1.4.10 se define como escritorio con zoom a 320 px CSS: contexto de ESCRITORIO (sin is_mobile, que haría
            # respetar un meta viewport fijo y ocultaría el desborde), y 1.4.4 equivalente (escritorio a 640 px)
            res["reflow_320"] = medir(browser, url, 320, 640, False, a.bloquear_host,
                                      os.path.join(dir_cap, f"reflow320_{s}.png"))
            res["zoom_200"] = medir(browser, url, 640, 450, False, a.bloquear_host,
                                    os.path.join(dir_cap, f"zoom200_{s}.png"))
            # 1.4.12 espaciado de texto + estructura + árbol, en escritorio normal
            ctx = nav.nuevo_contexto(browser, "escritorio")
            page = ctx.new_page()
            nav.instalar_bloqueos(page, a.bloquear_host, False)
            http = nav.abrir(page, url)
            res["http"] = http
            if http is not None and http >= 400:
                print(f"[aviso] {url} respondió HTTP {http}: consolidar.py la dejará fuera como no auditable", file=sys.stderr)
            if http is not None:
                res["url_final"] = page.url
                nav.recorrer_scroll(page)
                antes = {r["sel"] for r in page.evaluate(JS_RECORTES)}
                solapes_antes = {s["par"] for s in page.evaluate(JS_SOLAPES)}
                page.add_style_tag(content=CSS_1412)
                page.wait_for_timeout(500)
                despues = page.evaluate(JS_RECORTES)
                res["espaciado_1412_recortes_nuevos"] = [r for r in despues if r["sel"] not in antes]
                res["espaciado_1412_solapes_nuevos"] = [s for s in page.evaluate(JS_SOLAPES) if s["par"] not in solapes_antes]
                est = page.evaluate(JS_ESTRUCTURA)
                if a.idioma and est["lang"]:
                    est["lang_coincide"] = est["lang"].lower().split("-")[0] == a.idioma.lower()
                res["estructura"] = est
                try:
                    page.reload(wait_until="load")
                    page.wait_for_timeout(800)
                    arbol = page.locator("body").aria_snapshot()
                    ruta = os.path.join(out_dir, f"arbol_{s}.yml")
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(arbol)
                    res["arbol"] = os.path.basename(ruta)
                except Exception as e:  # noqa: BLE001
                    res["arbol_error"] = str(e)[:200]
            ctx.close()
            nav.guardar_json(os.path.join(out_dir, f"adaptacion_{s}.json"), res)
            r320, z = res["reflow_320"], res["zoom_200"]
            est = res.get("estructura", {})
            print(f"{url}: reflow320 scroll {r320.get('scroll_width')}/{r320.get('client_width')} "
                  f"({len(r320.get('desbordes', []))} desbordes); zoom200 scroll {z.get('scroll_width')}/{z.get('client_width')}, "
                  f"fijos {[f['pct_alto_vista'] for f in z.get('fijos', [])]}% alto; espaciado: "
                  f"{len(res.get('espaciado_1412_recortes_nuevos', []))} recortes y "
                  f"{len(res.get('espaciado_1412_solapes_nuevos', []))} solapes nuevos; lang={est.get('lang')} "
                  f"main={est.get('main')} h1={est.get('h1')}")
        browser.close()


if __name__ == "__main__":
    main()
