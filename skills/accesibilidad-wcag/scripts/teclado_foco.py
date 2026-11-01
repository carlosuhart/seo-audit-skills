"""Recorrido de teclado real con Playwright: lo que axe no puede comprobar sobre el foco.

Pulsa Tab como lo haría una persona y en cada paso registra el elemento enfocado. Todo lo que devuelve son
CANDIDATOS con selector y captura: se confirman a mano antes de reportarlos como incumplimiento.

Criterios que alimenta:
  2.1.1 Teclado          elementos con aspecto de control que no reciben foco (div/span clicables)
  2.1.2 Sin trampas      el foco queda girando en un grupo pequeño sin volver al inicio (se confirma con Esc)
  2.4.1 Saltar bloques   existe un enlace "saltar al contenido" y si al activarlo el foco llega al contenido
  2.4.3 Orden del foco   retrocesos grandes en la página y tabindex positivo
  2.4.7 Foco visible     el elemento se ve igual con y sin foco (comparación de píxeles, no outline:none)
  2.4.11 Foco no oculto  una cabecera fija, banner de cookies o chat tapa por completo el elemento enfocado
  Diálogos               con un diálogo modal abierto (--clic), el foco no debe salir de él

Uso (PowerShell):
  py scripts/teclado_foco.py https://sitio.cl/ --out <dir>
  py scripts/teclado_foco.py https://sitio.cl/ --vista movil --out <dir>
  py scripts/teclado_foco.py https://sitio.cl/ --clic "button.abrir-modal" --estado modal --out <dir>
  py scripts/teclado_foco.py https://sitio.com/en/ --bloquear-host <servicio-geoip> --out <dir>

Opciones: --tope 150 (pasos de Tab), --sin-capturas.
Salida: <out>/teclado_<slug>_<vista>[_<estado>].json y recortes en <out>/capturas/.

Límite conocido: quitar el foco para comparar (blur) puede cerrar menús desplegables que se cierran al
perder el foco; esos pasos pueden dar "foco visible" por cambio de contenido. El sesgo es conservador
(puede omitir un fallo, no inventarlo). Las animaciones se reducen con reduced_motion.
"""
from __future__ import annotations

import argparse
import os
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import navegador as nav  # noqa: E402

JS_INFO = r"""() => {
  const U = window.__a11y; const el = U.deepActive();
  if (!el || el === document.body || el === document.documentElement) return null;
  const r = el.getBoundingClientRect(); const s = U.cs(el);
  // 2.4.11: muestreo de 5 puntos; tapado si en ningún punto el elemento (o un hijo) está arriba
  const pts = [[0.5,0.5],[0.15,0.15],[0.85,0.15],[0.15,0.85],[0.85,0.85]].map(([fx,fy]) => [r.left + r.width*fx, r.top + r.height*fy]);
  // contención "compuesta": cruza los límites de shadow DOM (un host contiene a los elementos de su sombra)
  const contiene = (a, b) => { let n = b; while (n) { if (n === a) return true; n = n.parentNode || n.host; } return false; };
  let dentro = 0, tapados = 0, tapador = null, tapadorFijo = false, tapadorTransparente = false;
  for (const [x,y] of pts) {
    if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) continue; dentro++;
    let top = document.elementFromPoint(x, y);
    while (top && top.shadowRoot) { const t2 = top.shadowRoot.elementFromPoint(x, y); if (!t2 || t2 === top) break; top = t2; }
    if (!top || contiene(el, top) || contiene(top, el)) continue;
    tapados++; if (!tapador) { let t = top; while (t && t !== document.body) { const p = U.cs(t).position;
      if (p === 'fixed' || p === 'sticky') break; t = t.parentElement; }
      const raiz = t && t !== document.body ? t : null; tapadorFijo = !!raiz; tapador = U.sel(raiz || top);
      const ts = U.cs(top); const bg = ts.backgroundColor;
      tapadorTransparente = (bg === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(bg)) && ts.backgroundImage === 'none'
        && !(top.innerText || '').trim(); }
  }
  // opacidad efectiva y visibilidad heredada: un diálogo cerrado con opacity:0 o detrás del contenido
  let op = 1, e2 = el, invisibleHeredado = false;
  while (e2 && e2.nodeType === 1) { const s2 = U.cs(e2); op *= parseFloat(s2.opacity);
    if (s2.visibility === 'hidden' || s2.display === 'none') invisibleHeredado = true; e2 = e2.parentElement; }
  let fijo = false; for (let e3 = el; e3 && e3.nodeType === 1; e3 = e3.parentElement) { const p3 = U.cs(e3).position;
    if (p3 === 'fixed' || p3 === 'sticky') { fijo = true; break; } }
  const dlg = document.querySelector('dialog[open], [role=dialog][aria-modal=true], [role=alertdialog][aria-modal=true]');
  const dlgVisible = dlg && U.visible(dlg);
  return {sel: U.sel(el), tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '', nombre: U.name(el),
    href: el.getAttribute('href') || '', tabindex: el.getAttribute('tabindex'),
    rect: {x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height)},
    y_doc: Math.round(r.top + scrollY), en_vista: r.bottom > 0 && r.top < innerHeight && r.width > 0 && r.height > 0,
    oculto: (r.width === 0 || r.height === 0 || invisibleHeredado || op < 0.05),
    opacidad_efectiva: Math.round(op * 100) / 100,
    puntos_en_vista: dentro, puntos_tapados: tapados, tapador, tapador_fijo: tapadorFijo,
    tapador_transparente: tapadorTransparente, fijo,
    fuera_de_dialogo: !!(dlgVisible && !dlg.contains(el)), dialogo: dlgVisible ? U.sel(dlg) : null};
}"""

JS_NO_ALCANZABLES = r"""() => {
  const U = window.__a11y; const out = [];
  const enfocable = 'a[href], button, input, select, textarea, summary, iframe, [tabindex], [contenteditable=true]';
  for (const el of document.querySelectorAll('div, span, li, img, svg, i, td, p')) {
    if (out.length >= 40 || !U.visible(el)) continue;
    if (el.matches(enfocable) || el.closest(enfocable) || el.querySelector(enfocable)) continue;
    const s = U.cs(el); const role = el.getAttribute('role') || '';
    const pareceControl = el.hasAttribute('onclick') || ['button','link','tab','menuitem','checkbox','switch','option'].includes(role)
      || (s.cursor === 'pointer' && (!el.parentElement || U.cs(el.parentElement).cursor !== 'pointer'));
    if (!pareceControl) continue;
    const r = el.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    out.push({sel: U.sel(el), tag: el.tagName.toLowerCase(), role, texto: U.name(el), motivo:
      el.hasAttribute('onclick') ? 'onclick sin foco' : role ? 'role=' + role + ' sin tabindex' : 'cursor de mano sin foco'});
  }
  return out;
}"""

JS_TABINDEX_POSITIVO = r"""() => [...document.querySelectorAll('[tabindex]')].filter(e => parseInt(e.getAttribute('tabindex')) > 0)
  .slice(0, 30).map(e => ({sel: window.__a11y.sel(e), tabindex: e.getAttribute('tabindex'), nombre: window.__a11y.name(e)}))"""

JS_TOTAL_ENFOCABLES = r"""() => [...document.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]):not([type=hidden]), select:not([disabled]), textarea:not([disabled]), summary, iframe, [tabindex]:not([tabindex="-1"]), [contenteditable=true]')]
  .filter(e => window.__a11y.visible(e)).length"""


def recorte(info: dict, vp: dict) -> dict | None:
    r = info["rect"]
    x, y = max(0, r["x"] - 8), max(0, r["y"] - 8)
    w, h = min(vp["width"] - x, r["w"] + 16), min(vp["height"] - y, r["h"] + 16)
    if w <= 2 or h <= 2:
        return None
    return {"x": x, "y": y, "width": w, "height": h}


def foco_visible(page, info: dict, captura: str | None) -> bool | None:
    """Compara el recorte con foco y sin foco. None = no medible (fuera de vista)."""
    clip = recorte(info, page.viewport_size)
    if not clip or not info["en_vista"]:
        return None
    try:
        con = page.screenshot(clip=clip)
        page.evaluate("() => { window.__fe = window.__a11y.deepActive(); window.__fe && window.__fe.blur(); }")
        page.wait_for_timeout(120)
        sin = page.screenshot(clip=clip)
        page.evaluate("() => { window.__fe && window.__fe.focus({focusVisible: true}); }")
        page.wait_for_timeout(120)
    except Exception:  # noqa: BLE001
        return None
    visible = con != sin
    if not visible and captura:
        with open(captura, "wb") as f:
            f.write(con)
    return visible


JS_ES_SALTO = r"""() => { const a = window.__a11y.deepActive(); if (!a) return null;
  const txt = (a.innerText || a.getAttribute('aria-label') || '').trim();
  const h = a.getAttribute('href') || ''; let hash = '';
  if (h) { try { const u = new URL(h, location.href); if (u.pathname === location.pathname && u.hash.length > 1) hash = u.hash; } catch (e) {} }
  const pareceSalto = /saltar|ir al contenido|ir al principal|skip|pular|conteúdo/i.test(txt);
  return {sel: window.__a11y.sel(a), nombre: txt.slice(0, 60), hash, es_salto: !!hash && (pareceSalto || /main|content|contenido|principal/i.test(hash)) || (pareceSalto && a.tagName === 'BUTTON')}; }"""


def probar_skip(page, url: str) -> dict:
    """Primeras 3 paradas de Tab: ¿hay un control de salto (enlace con #ancla resuelto contra la URL, o botón)?
    Al activarlo, ¿el siguiente foco cae en el destino o en main? (un banner de cookies puede tomar el 1.er Tab)."""
    nav.abrir(page, url, espera_ms=800)
    page.mouse.move(0, 0)
    vistos = []
    salto = None
    for _ in range(3):
        page.keyboard.press("Tab")
        page.wait_for_timeout(150)
        info = page.evaluate(JS_ES_SALTO)
        if not info:
            break
        vistos.append(info["nombre"] or info["sel"][-40:])
        if info["es_salto"]:
            salto = info
            break
    if not salto:
        return {"existe": False, "primeras_paradas": vistos}
    res = {"existe": True, "control": salto}
    page.keyboard.press("Enter")
    page.wait_for_timeout(400)
    page.keyboard.press("Tab")
    page.wait_for_timeout(150)
    siguiente = page.evaluate("""(h) => { const t = h ? document.getElementById(decodeURIComponent(h.slice(1))) : null;
        const a = window.__a11y.deepActive(); const main = document.querySelector('main, [role=main]');
        return {sel: a ? window.__a11y.sel(a) : null, destino_existe: !!t,
                en_destino: !!(t && a && (t.contains(a) || t.compareDocumentPosition(a) & 4)),
                en_main: !!(main && a && main.contains(a))}; }""", salto["hash"])
    res.update({"foco_tras_saltar": siguiente, "funciona": bool(siguiente["en_destino"] or siguiente["en_main"])})
    return res


def recorrer(page, tope: int, dir_capturas: str | None, prefijo: str) -> dict:
    page.mouse.move(0, 0)
    page.evaluate("() => { document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); }")
    pasos, visitas, primero, fin = [], {}, None, "tope alcanzado"
    seguidos_iframe = 0
    for i in range(tope):
        page.keyboard.press("Tab")
        page.wait_for_timeout(110)
        info = page.evaluate(JS_INFO)
        if info is None:
            fin = "el foco salió de la página (volvió a la barra del navegador)"
            break
        clave = f"{info['sel']}|{info['y_doc']}"
        if primero is None:
            primero = clave
        elif clave == primero:
            fin = "ciclo completo (volvió al primer elemento)"
            break
        if info["tag"] == "iframe":
            seguidos_iframe += 1
        else:
            seguidos_iframe = 0
        visitas[clave] = visitas.get(clave, 0) + 1
        cap = os.path.join(dir_capturas, f"{prefijo}_foco_{i:03d}.png") if dir_capturas else None
        info["foco_visible"] = None if info["tag"] == "iframe" else foco_visible(page, info, cap)
        if info["foco_visible"] is False and cap:
            info["captura"] = os.path.basename(cap)
        info["paso"] = i + 1
        pasos.append(info)
        if visitas[clave] >= 3 and seguidos_iframe < 3:
            fin = "posible trampa: el mismo elemento se repite sin volver al inicio"
            break
    return {"pasos": pasos, "fin": fin}


def confirmar_trampa(page, pasos: list[dict]) -> dict:
    """Si hubo posible trampa: el grupo = elementos repetidos en el recorrido. Prueba Esc + Tab y Shift+Tab
    y mira si el foco llega a algún elemento FUERA de ese grupo (no basta con que cambie de elemento)."""
    cuenta: dict[str, int] = {}
    for p in pasos:
        cuenta[p["sel"]] = cuenta.get(p["sel"], 0) + 1
    grupo = {s for s, n in cuenta.items() if n >= 2}

    def sale(tecla: str) -> bool:
        for _ in range(len(grupo) + 3):
            page.keyboard.press(tecla)
            page.wait_for_timeout(90)
            info = page.evaluate(JS_INFO)
            if info is None or info["sel"] not in grupo:
                return True
        return False

    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    sale_tab = sale("Tab")
    sale_shift = sale("Shift+Tab")
    return {"grupo": sorted(grupo)[:10], "sale_con_esc_y_tab": sale_tab, "sale_con_shift_tab": sale_shift,
            "confirmada": not sale_tab and not sale_shift}


def analizar(rec: dict) -> dict:
    pasos = rec["pasos"]
    completo = lambda p: p["puntos_en_vista"] and p["puntos_tapados"] == p["puntos_en_vista"]  # noqa: E731
    # Foco en contenido que la persona no ve: opacidad nula, oculto por herencia, o detrás de contenido
    # que NO es fijo (típico de un diálogo o menú cerrado que sigue en el orden de tabulación).
    invisibles = [p for p in pasos if p["oculto"] or (completo(p) and not p["tapador_fijo"] and not p["tapador_transparente"])]
    ids_invisibles = {p["paso"] for p in invisibles}
    # 2.4.11: tapado por completo por una capa fija o pegajosa (cabecera, banner de cookies, chat)
    tapados = [p for p in pasos if completo(p) and p["tapador_fijo"] and not p["tapador_transparente"]]
    ids_tapados = {p["paso"] for p in tapados}
    # 2.4.7 solo donde el elemento está a la vista: si está tapado o invisible, la causa es otra
    medibles = [p for p in pasos if p["foco_visible"] is not None and p["paso"] not in ids_invisibles | ids_tapados]
    sin_foco = [p for p in medibles if p["foco_visible"] is False]
    a_revisar = [p for p in pasos if completo(p) and p["tapador_transparente"]]
    parciales = [p for p in pasos if p["puntos_en_vista"] and 0 < p["puntos_tapados"] < p["puntos_en_vista"]]
    retrocesos = []
    for a, b in zip(pasos, pasos[1:]):  # los fijos (cabecera, chat) no tienen posición de lectura en la página
        if not a.get("fijo") and not b.get("fijo") and a["y_doc"] - b["y_doc"] > 400 and b["y_doc"] > 200:
            retrocesos.append({"de": a["sel"], "a": b["sel"], "salto_px": a["y_doc"] - b["y_doc"], "paso": b["paso"]})
    fuera = [p for p in pasos if p["fuera_de_dialogo"]]
    corto = lambda p: {k: p.get(k) for k in ("paso", "sel", "tag", "nombre", "captura", "tapador") if p.get(k) is not None}  # noqa: E731
    return {
        "pasos_recorridos": len(pasos), "fin": rec["fin"],
        "foco_medible": len(medibles), "foco_no_visible": [corto(p) for p in sin_foco],
        "foco_tapado_completo": [corto(p) for p in tapados],
        "foco_tapado_por_capa_transparente_revisar": [corto(p) for p in a_revisar],
        "foco_tapado_parcial": len(parciales),
        "foco_en_contenido_no_visible": [corto(p) for p in invisibles],
        "retrocesos_de_orden": retrocesos[:20],
        "foco_fuera_de_dialogo": [corto(p) for p in fuera],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls-archivo")
    ap.add_argument("--vista", default="escritorio")
    ap.add_argument("--clic", action="append")
    ap.add_argument("--estado", default="inicial")
    ap.add_argument("--bloquear-host", action="append")
    ap.add_argument("--tope", type=int, default=150)
    ap.add_argument("--sin-capturas", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out_dir = nav.carpeta_salida(a.out)
    dir_cap = None if a.sin_capturas else nav.carpeta_salida(os.path.join(out_dir, "capturas"))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for url in nav.leer_urls(a.urls, a.urls_archivo):
            ctx = nav.nuevo_contexto(browser, a.vista, reduced_motion="reduce")
            page = ctx.new_page()
            bloqueos = nav.instalar_bloqueos(page, a.bloquear_host, False)
            status = nav.abrir(page, url)
            if status is None:
                ctx.close()
                continue
            if status >= 400:
                print(f"[aviso] {url} respondió HTTP {status} (¿bloqueo o desafío anti-bot?): consolidar.py la "
                      f"dejará fuera como no auditable", file=sys.stderr)
            page.evaluate(nav.JS_UTILS)
            fallidos = nav.aplicar_acciones(page, a.clic)
            page.evaluate(nav.JS_UTILS)
            total = page.evaluate(JS_TOTAL_ENFOCABLES)
            prefijo = f"{nav.slug(url, 40)}_{a.vista}" + (f"_{nav.slug(a.estado, 15)}" if a.estado != "inicial" else "")
            rec = recorrer(page, a.tope, dir_cap, prefijo)
            trampa = confirmar_trampa(page, rec["pasos"]) if rec["fin"].startswith("posible trampa") else None
            no_alcanzables = page.evaluate(JS_NO_ALCANZABLES)
            tab_pos = page.evaluate(JS_TABINDEX_POSITIVO)
            skip = probar_skip(page, url) if a.estado == "inicial" else None
            res = {"url": url, "url_final": page.url, "vista": a.vista, "estado": a.estado, "http": status,
                   "fecha": nav.ahora(), "clics_fallidos": fallidos, "bloqueos": bloqueos,
                   "enfocables_visibles_estimados": total, "resumen": analizar(rec), "trampa": trampa,
                   "candidatos_no_alcanzables": no_alcanzables, "tabindex_positivo": tab_pos,
                   "salto_al_contenido": skip, "pasos": rec["pasos"]}
            nav.guardar_json(os.path.join(out_dir, f"teclado_{prefijo}.json"), res)
            r = res["resumen"]
            print(f"{url} [{a.vista}/{a.estado}] {r['pasos_recorridos']} pasos de {total} enfocables; fin: {r['fin']}; "
                  f"foco no visible {len(r['foco_no_visible'])}/{r['foco_medible']}; tapado {len(r['foco_tapado_completo'])}; "
                  f"en contenido no visible {len(r['foco_en_contenido_no_visible'])}; "
                  f"retrocesos {len(r['retrocesos_de_orden'])}; sin foco (candidatos) {len(no_alcanzables)}; "
                  f"salto al contenido: {'sí' if skip and skip.get('existe') else 'no' if skip else 'n/a'}")
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
