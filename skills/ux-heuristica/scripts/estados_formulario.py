"""Estados de un formulario sin enviar nada: inicial, vacío, datos inválidos y datos válidos con el envío bloqueado.

Responde las preguntas heurísticas de un formulario de lead, registro o contacto con capturas de cada estado:
  H1 Estado del sistema   ¿se ve que algo pasa al pulsar? ¿el botón cambia o se bloquea (doble envío)?
  H5 Prevención           tipo de campo (email, tel) que abre el teclado correcto; obligatorios marcados
  H6 Reconocer            etiqueta visible o solo placeholder
  H7 Eficiencia           autocomplete en nombre, correo, teléfono, empresa
  H8 Minimalismo          el botón de envío queda tapado (banner de cookies, chat)
  H9 Errores              al enviar vacío o con formato erróneo: ¿hay mensaje que diga cómo corregir? ¿se
                          conserva lo escrito? Y cuando el envío falla (red bloqueada): ¿el sitio lo dice, se
                          queda colgado o muestra la pantalla de error del framework?

Seguridad de la prueba (ver navegador.py):
  - Contexto sin service workers, rutas a nivel de contexto (cubren popups) y WebSockets cerrados.
  - MODO ESTRICTO desde antes de rellenar o pulsar: solo pasan GET de recursos estáticos del mismo dominio.
    Se abortan fetch/XHR de cualquier método, navegaciones (formularios GET), píxeles de conversión de
    terceros (Ads, Meta, GTM, LinkedIn) y cualquier petición que lleve el correo ficticio. Ninguna prueba
    llega al servidor del sitio ni registra conversiones falsas.
  - Datos ficticios (prueba.zz@example.com). Nunca datos de la persona que audita.
  - Lo que se ve en "valido_bloqueado" es la reacción del sitio a un fallo de red provocado por la prueba.
    Se reporta como "manejo de fallo del envío" y su severidad se calibra como caso de borde.

Límite: con el envío bloqueado no se puede ver el camino de éxito (confirmación, qué pasa después) ni probar
carro y checkout. Eso requiere un envío autorizado y etiquetado por el cliente, o un entorno de pruebas.

Uso (PowerShell):
  py "$HOME\\.claude\\skills\\ux-heuristica\\scripts\\estados_formulario.py" https://sitio.cl/contacto --out <dir>
  ... --form "#contacto form" --vistas escritorio,movil --out <dir>
  ... --clic "button.abrir-demo" --out <dir>        # formulario dentro de una ventana

Salida: <out>/form_<slug>_<vista>.json y capturas del formulario por estado en <out>/capturas/.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import navegador as nav  # noqa: E402

CORREO = "prueba.zz@example.com"
BOTON_SUBMIT = "button[type=submit], input[type=submit]"
BOTON_SIN_TIPO = "button:not([type])"
EXITO = re.compile(r"gracias|recibimos|hemos recibido|enviado con|mensaje enviado|thank you|received|obrigad", re.I)

JS_INVENTARIO = r"""(form) => { const U = window.__a11y; const campos = [];
  const asterisco = el => ['::before', '::after'].some(p => /\*/.test(getComputedStyle(el, p).content || ''));
  const clasifica = (nombre, etiqueta, ph) => { const s = [nombre, etiqueta, ph].join(' | ').toLowerCase();
    if (/mail|correo/.test(s)) return 'correo';
    if (/(^|[^a-z])(empresa|company|compa[ñn][ií]a|organizaci[oó]n|raz[oó]n social)/.test(s)) return 'empresa';
    if (/(^|[^a-z])(tel|tel[eé]fono|fono|phone|celular|m[oó]vil|whatsapp)([^a-z]|$)/.test(s)) return 'telefono';
    if (/(^|[^a-z])(nombre|name|apellido)([^a-z]|$)/.test(s)) return 'nombre'; return ''; };
  for (const el of form.querySelectorAll('input, select, textarea')) {
    const t = (el.getAttribute('type') || el.tagName).toLowerCase();
    if (['hidden','submit','button','reset','image'].includes(t) || !U.visible(el)) continue;
    let visible = '', nodoEtiqueta = null;
    if (el.labels && el.labels.length) { const ls = [...el.labels].filter(U.visible); visible = ls.map(l => l.innerText).join(' ').trim(); nodoEtiqueta = ls[0]; }
    if (!visible) { const p = el.closest('label'); if (p && U.visible(p)) { visible = p.innerText.trim(); nodoEtiqueta = p; } }
    if (!visible) { // texto corto justo encima del campo (etiqueta visual no asociada en el código)
      const er = el.getBoundingClientRect();
      buscar: for (let p = el.parentElement, h = 0; p && h < 3; p = p.parentElement, h++) {
        for (const k of p.querySelectorAll('label, span, p, div, legend')) {
          if (k.contains(el) || k.children.length > 1 || !U.visible(k)) continue; const tx = (k.innerText || '').trim();
          if (!tx || tx.length > 60) continue; const kr = k.getBoundingClientRect();
          if (kr.bottom <= er.top + 4 && kr.bottom >= er.top - 40 && kr.right > er.left && kr.left < er.right) { visible = 'cercano: ' + tx; nodoEtiqueta = k; break buscar; }
        } } }
    const marca = /\*|obligatori|requerid|required/i.test(visible) || !!(nodoEtiqueta && (asterisco(nodoEtiqueta) || [...nodoEtiqueta.querySelectorAll('*')].some(asterisco)));
    campos.push({sel: U.sel(el), tag: el.tagName.toLowerCase(), type: t, name: el.name || '', etiqueta_visible: visible.slice(0, 60),
      etiqueta_asociada: !!(el.labels && el.labels.length) || !!el.getAttribute('aria-labelledby') || !!el.getAttribute('aria-label'),
      placeholder: el.getAttribute('placeholder') || '', required: el.required || el.getAttribute('aria-required') === 'true',
      marca_obligatorio: marca, autocomplete: el.getAttribute('autocomplete') || '', inputmode: el.getAttribute('inputmode') || '',
      valor: (el.value || '').slice(0, 40), pide: clasifica(el.name || el.id || '', visible, el.getAttribute('placeholder') || '')});
  }
  return {campos, nota_obligatorios: /todos los campos son obligatorios|campos obligatorios|\* ?(campo )?obligatorio|required fields/i.test(form.innerText),
    casilla_consentimiento: [...form.querySelectorAll('input[type=checkbox]')].some(c => /privacidad|datos|acepto|consent|términos|terminos/i.test((c.closest('label') || c.parentElement || {}).innerText || '')),
    enlace_privacidad: [...form.querySelectorAll('a')].some(a => /privacidad|privacy|datos personales/i.test(a.innerText + a.href)),
    campo_trampa: [...form.querySelectorAll('input')].filter(i => !U.visible(i) && i.type !== 'hidden').map(i => i.name).slice(0, 3)};
}"""

JS_TEXTOS = r"""(form) => { // textos visibles del bloque del formulario y de alertas o avisos (toasts) de la página
  const U = window.__a11y; let zona = form; for (let i = 0; i < 2 && zona.parentElement && zona.parentElement !== document.body; i++) zona = zona.parentElement;
  const out = new Set(); const w = document.createTreeWalker(zona, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const t = w.currentNode.textContent.trim().replace(/\s+/g, ' '); const p = w.currentNode.parentElement;
    if (t && t.length < 220 && p && U.visible(p) && !['SCRIPT','STYLE','OPTION'].includes(p.tagName)) out.add(t); }
  for (const e of document.querySelectorAll('[role=alert], [role=status], [role=alertdialog]')) { const t = (e.innerText || '').trim(); if (t && U.visible(e)) out.add(t.slice(0, 220)); }
  return [...out]; }"""

JS_REACCION = r"""(form) => { const U = window.__a11y;
  const invalidos = [...form.querySelectorAll(':invalid')].filter(e => e.tagName !== 'FORM' && e.tagName !== 'FIELDSET');
  const cuerpo = document.body.innerText;
  const a = U.deepActive(); const esControl = a && a.matches && a.matches('input, select, textarea, button, a');
  return {avisos_nativos: invalidos.length, primer_aviso_nativo: invalidos[0] ? invalidos[0].validationMessage : '',
    aria_invalid: form.querySelectorAll('[aria-invalid=true]').length,
    foco_en: a ? (esControl ? U.name(a) : a.tagName.toLowerCase()) : null,
    foco_en_campo_con_error: !!(a && a.matches && (a.matches(':invalid') || a.getAttribute('aria-invalid') === 'true')),
    formulario_visible: U.visible(form),
    pantalla_error_framework: /Application error|Unhandled Runtime Error|Something went wrong|Internal Server Error|This page could not be|ChunkLoadError/i.test(cuerpo.slice(0, 3000)) && cuerpo.length < 1500};
}"""

JS_OBSERVAR = r"""(form) => { // feedback del envío en TODO el formulario (React puede reemplazar el botón)
  const textos = () => [...form.querySelectorAll('button, input[type=submit]')].map(b => (b.innerText || b.value || '').trim()).join('|');
  const t0 = textos(); window.__btn = {cambio: false, textos: []};
  new MutationObserver(() => { const b = [...form.querySelectorAll('button, input[type=submit]')];
    const ocupado = b.some(x => x.disabled || x.getAttribute('aria-busy') === 'true' || x.getAttribute('aria-disabled') === 'true')
      || !!form.querySelector('[aria-busy=true], [class*=spinner], [class*=loading], [class*=Loading]');
    const t = textos(); if (ocupado || t !== t0) { window.__btn.cambio = true;
      if (t !== t0 && window.__btn.textos.length < 3) window.__btn.textos.push(t.slice(0, 40)); } })
    .observe(form, {attributes: true, childList: true, subtree: true, characterData: true}); }"""

JS_TAPADOR = r"""(b) => { const r = b.getBoundingClientRect(); const x = r.left + r.width / 2, y = r.top + r.height / 2;
  const t = document.elementFromPoint(x, y); if (!t || t === b || b.contains(t)) return null;
  let e = t; while (e && e !== document.body) { const p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') break; e = e.parentElement; }
  return window.__a11y.sel(e && e !== document.body ? e : t) + ' «' + ((e || t).innerText || '').trim().replace(/\s+/g, ' ').slice(0, 50) + '»'; }"""


def valor_para(c: dict, valido: bool) -> str | None:
    t, pide = c["type"], c["pide"]
    if c["tag"] == "select" or t in ("checkbox", "radio", "file", "range", "color", "date", "datetime-local", "time"):
        return None
    if t == "email" or pide == "correo":
        return CORREO if valido else "nombre@"
    if t == "tel" or pide == "telefono":
        return "+56 9 1234 5678" if valido else "abc"
    if t == "number":
        return "5" if valido else "-"
    if t == "url":
        return "https://example.com" if valido else "sitio"
    if pide == "empresa":
        return "Empresa de Prueba"
    if c["tag"] == "textarea":
        return "Mensaje de prueba de usabilidad, no contactar."
    return "Prueba Usabilidad"


def rellenar(page, inventario: dict, valido: bool) -> list[str]:
    fallos = []
    for c in inventario["campos"]:
        loc = page.locator(c["sel"]).first
        try:
            v = valor_para(c, valido)
            if v is not None:
                try:
                    loc.fill(v, timeout=2500)
                except Exception:  # noqa: BLE001  p. ej. type=number que no acepta el texto
                    if c["type"] == "number" or c["pide"] == "telefono":
                        loc.fill("912345678" if valido else "0", timeout=2500)
                    else:
                        raise
            elif valido and c["type"] == "checkbox" and c["required"]:
                loc.check(timeout=2500, force=True)
            elif valido and c["tag"] == "select":
                if loc.locator("option").count() > 1:
                    loc.select_option(index=1, timeout=2500)
            elif valido and c["required"]:
                fallos.append(f"{c['sel'][-40:]} ({c['type']}, obligatorio sin rellenar)")
        except Exception:  # noqa: BLE001
            fallos.append(c["sel"][-50:])
    return fallos


def localizar_form(page, sel: str):
    """El primer formulario visible con un botón de envío visible. Prefiere type=submit; si no hay, el
    último button sin tipo con texto (evita botones de mostrar contraseña o selectores)."""
    forms = page.locator(sel)
    for i in range(forms.count()):
        f = forms.nth(i)
        if not f.is_visible():
            continue
        subs = f.locator(BOTON_SUBMIT)
        for j in range(subs.count()):
            if subs.nth(j).is_visible():
                return f, subs.nth(j)
        sin = f.locator(BOTON_SIN_TIPO)
        for j in reversed(range(sin.count())):
            b = sin.nth(j)
            if b.is_visible() and (b.inner_text(timeout=1000) or "").strip():
                return f, b
    return None, None


def intentos(registro: dict, desde: int, raiz: str) -> list[str]:
    """Peticiones bloqueadas después del clic que van al propio sitio (o a su backend) y llevan datos."""
    out = []
    for e in registro.get("estricto", [])[desde:]:
        metodo, tipo, url = (e.split(" ", 2) + ["", ""])[:3]
        host = urlparse(url).netloc.lower()
        if (metodo != "GET" or tipo in ("fetch", "xhr", "document")) and (host.endswith(raiz) or tipo == "document"):
            out.append(e)
    return out


def estado(page, url: str, form_sel: str, clics, modo: str, dir_cap: str, prefijo: str, registro: dict) -> dict:
    nav.abrir(page, url, espera_ms=1200)
    fallidos = nav.aplicar_acciones(page, clics)
    form, boton = localizar_form(page, form_sel)
    if not form:
        return {"error": "no hay formulario visible con botón de envío", "clics_fallidos": fallidos}
    handle = form.element_handle()
    inv = page.evaluate(JS_INVENTARIO, handle)
    inv["boton"] = (boton.inner_text(timeout=1000) or boton.get_attribute("value") or "").strip()[:40]
    res = {"clics_fallidos": fallidos}
    if modo == "inicial":
        res["inventario"] = inv
    else:
        nav.activar_modo_estricto(page, registro)  # ANTES de rellenar: cubre validaciones remotas al salir del campo
        raiz = ".".join(urlparse(page.url).netloc.lower().split(".")[-2:])
        antes: dict = {}
        if modo in ("invalido", "valido_bloqueado"):
            res["no_rellenados"] = rellenar(page, inv, modo == "valido_bloqueado")
            antes = {c["sel"]: c["valor"] for c in page.evaluate(JS_INVENTARIO, handle)["campos"] if c["valor"]}
        textos_antes = set(page.evaluate(JS_TEXTOS, handle))
        page.evaluate(JS_OBSERVAR, handle)
        n_antes = len(registro.get("estricto", []))
        try:
            boton.scroll_into_view_if_needed(timeout=3000)
            res["boton_tapado_por"] = boton.evaluate(JS_TAPADOR)
            boton.click(timeout=3000)
        except Exception as e:  # noqa: BLE001
            res["error_click"] = str(e)[:150]
            try:  # requestSubmit aplica la misma validación que un clic real
                form.evaluate("(f, b) => f.requestSubmit(b)", boton.element_handle())
                res["envio_programatico"] = True
            except Exception as e2:  # noqa: BLE001
                res["error_envio"] = str(e2)[:150]
        page.wait_for_timeout(3500 if modo == "valido_bloqueado" else 1200)
        try:
            res["reaccion"] = page.evaluate(JS_REACCION, handle)
        except Exception:  # noqa: BLE001  el formulario pudo desmontarse
            res["reaccion"] = {"formulario_visible": False}
        try:  # texto que apareció tras pulsar: el mensaje, sea cual sea la clase CSS que use el sitio
            nuevos = [t for t in page.evaluate(JS_TEXTOS, handle) if t not in textos_antes]
        except Exception:  # noqa: BLE001
            nuevos = []
        res["reaccion"]["textos_nuevos"] = nuevos[:10]
        res["reaccion"]["texto_exito"] = any(EXITO.search(t) for t in nuevos)
        res["intentos_de_envio_bloqueados"] = intentos(registro, n_antes, raiz)[:5]
        if modo == "invalido" and antes:
            try:
                despues = {c["sel"]: c["valor"] for c in page.evaluate(JS_INVENTARIO, handle)["campos"]}
            except Exception:  # noqa: BLE001
                despues = {}
            # solo cuenta como perdido lo que quedó vacío: un componente que limpia "abc" en un teléfono no borra nada
            perdidos = [s[-40:] for s, v in antes.items() if not despues.get(s, "")]
            res["valores_conservados"] = not perdidos
            res["valores_perdidos"] = perdidos
        res["url_tras_envio"] = page.url
        try:
            res["boton_observado"] = page.evaluate("window.__btn || null")
        except Exception:  # noqa: BLE001
            res["boton_observado"] = None
    cap = os.path.join(dir_cap, f"{prefijo}_{modo}.png")
    try:
        (form if form.is_visible() else page).screenshot(path=cap)
    except Exception:  # noqa: BLE001
        page.screenshot(path=cap)
    res["captura"] = os.path.basename(cap)
    return res


def senales(r: dict) -> list[dict]:
    """Traduce los estados en señales heurísticas a confirmar (no son hallazgos todavía)."""
    out = []
    inv = r["estados"].get("inicial", {}).get("inventario")
    if not inv:
        return out
    add = lambda h, s, d: out.append({"heuristica": h, "senal": s, "detalle": d})  # noqa: E731
    grupos: dict[tuple[str, str], list[str]] = {}
    nombre = lambda c: (c["etiqueta_visible"] or c["placeholder"] or c["sel"][-30:])[:28]  # noqa: E731
    for c in inv["campos"]:
        g = None
        if not c["etiqueta_visible"] and c["placeholder"]:
            g = ("H6", "campos solo con placeholder (al escribir se pierde qué pedía)")
        elif not c["etiqueta_visible"]:
            g = ("H6", "campos sin etiqueta visible")
        if g:
            grupos.setdefault(g, []).append(nombre(c))
        if c["etiqueta_visible"] and not c["etiqueta_asociada"]:
            grupos.setdefault(("H6 / accesibilidad-wcag", "etiqueta visible no asociada al campo"), []).append(nombre(c))
        if c["pide"] == "correo" and c["type"] != "email":
            grupos.setdefault(("H5", "correo sin type=email (teclado móvil genérico)"), []).append(nombre(c))
        if c["pide"] == "telefono" and c["type"] != "tel" and c["inputmode"] not in ("tel", "numeric"):
            grupos.setdefault(("H5", "teléfono sin type=tel (teclado móvil genérico)"), []).append(nombre(c))
        if c["pide"] in ("nombre", "correo", "telefono", "empresa") and not c["autocomplete"]:
            grupos.setdefault(("H7", "sin autocomplete en datos que el navegador puede rellenar"), []).append(nombre(c))
        if c["required"] and not c["marca_obligatorio"] and not inv.get("nota_obligatorios"):
            grupos.setdefault(("H5", "obligatorios sin marca visible"), []).append(nombre(c))
    for (h, s), lista in grupos.items():
        add(h, f"{s} ({len(lista)})", ", ".join(lista))
    add("info", "campos visibles", str(len(inv["campos"])))

    hay_mensaje = lambda x: bool(x.get("textos_nuevos"))  # noqa: E731
    e = r["estados"]
    for modo in ("vacio", "invalido", "valido_bloqueado"):
        tap = e.get(modo, {}).get("boton_tapado_por")
        if tap:
            add("H8", "el botón de envío está tapado al ir a pulsarlo", tap)
            break

    v, ve = e.get("vacio", {}).get("reaccion", {}), e.get("vacio", {})
    if v and ve.get("error_envio"):
        add("no probado", "no se pudo pulsar el botón en el estado vacío", ve["error_envio"][:90])
    elif v and not hay_mensaje(v) and not v.get("avisos_nativos") and not v.get("aria_invalid"):
        add("H1/H9", "enviar vacío no produce ningún mensaje ni aviso", "captura: " + ve.get("captura", ""))
    elif v and not hay_mensaje(v) and v.get("avisos_nativos"):
        add("H9", "solo avisos nativos del navegador (un mensaje a la vez, texto genérico)", v.get("primer_aviso_nativo", ""))
    elif v and hay_mensaje(v):
        add("ok", "enviar vacío muestra mensajes", " | ".join(v["textos_nuevos"][:3])[:120])
    marcados = any(c["marca_obligatorio"] for c in inv["campos"]) or inv.get("nota_obligatorios")
    ya_dicho = any(s["senal"].startswith("obligatorios sin marca") for s in out)
    if v and (hay_mensaje(v) or v.get("avisos_nativos")) and not marcados and not ya_dicho:
        add("H5", "el formulario exige campos que no marca como obligatorios antes de enviar",
            " | ".join(v.get("textos_nuevos", [])[:2])[:100] or v.get("primer_aviso_nativo", ""))

    i = e.get("invalido", {})
    if i.get("reaccion") and not i.get("error_envio") and not hay_mensaje(i["reaccion"]) and not i["reaccion"].get("avisos_nativos"):
        add("H9", "con correo o teléfono mal escrito no hay mensaje", "captura: " + i.get("captura", ""))
    if i.get("valores_conservados") is False:
        add("H9", "tras el error se borra lo escrito", ", ".join(i.get("valores_perdidos", []))[:80])

    vb = e.get("valido_bloqueado", {})
    rb = vb.get("reaccion", {})
    if vb and not vb.get("intentos_de_envio_bloqueados"):
        motivo = ("el sitio no intentó enviar: la validación del cliente lo detuvo o faltó un campo "
                  f"({', '.join(vb.get('no_rellenados', [])) or 'ver textos_nuevos'})")
        add("no probado", "manejo del fallo del envío", motivo[:160])
    elif rb.get("pantalla_error_framework"):
        add("H9", "si el envío falla, aparece la pantalla de error del framework (caso de borde: calibrar severidad)",
            "captura: " + vb.get("captura", ""))
    elif rb.get("texto_exito"):
        add("H9", "muestra éxito aunque el envío fue bloqueado (puede confirmar sin respuesta del servidor)",
            " | ".join(rb.get("textos_nuevos", [])[:2])[:100])
    elif rb.get("formulario_visible") is not False and not hay_mensaje(rb):
        add("H1/H9", "si el envío falla, no se informa nada (la persona no sabe si se envió)", "captura: " + vb.get("captura", ""))
    elif hay_mensaje(rb):
        add("ok", "si el envío falla, el sitio lo informa", " | ".join(rb["textos_nuevos"][:2])[:120])
    obs = vb.get("boton_observado")
    if vb.get("intentos_de_envio_bloqueados") and obs is not None and not obs.get("cambio"):
        add("H1", "al enviar, el formulario no muestra indicio de carga (riesgo de doble envío)", inv.get("boton") or "")
    elif obs and obs.get("textos"):
        add("ok", "el botón da feedback al enviar", " -> ".join(obs["textos"]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls-archivo")
    ap.add_argument("--form", default="form", help="selector del formulario (se usa el primero visible con botón)")
    ap.add_argument("--clic", action="append", help="selector a pulsar antes (abrir la ventana del formulario)")
    ap.add_argument("--vistas", default="escritorio,movil")
    ap.add_argument("--bloquear-host", action="append")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = nav.carpeta_salida(a.out)
    dir_cap = nav.carpeta_salida(os.path.join(out, "capturas"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for url in nav.leer_urls(a.urls, a.urls_archivo):
            for vista in [v.strip() for v in a.vistas.split(",") if v.strip()]:
                prefijo = f"form_{nav.slug(url, 40)}_{vista}"
                r = {"url": url, "vista": vista, "formulario": a.form, "fecha": nav.ahora(), "estados": {},
                     "bloqueado_por_la_prueba": {}}
                for modo in ("inicial", "vacio", "invalido", "valido_bloqueado"):
                    ctx = nav.nuevo_contexto(browser, vista)
                    page = ctx.new_page()
                    reg = nav.instalar_bloqueos(page, a.bloquear_host, True)
                    r["estados"][modo] = estado(page, url, a.form, a.clic, modo, dir_cap, prefijo, reg)
                    r["bloqueado_por_la_prueba"][modo] = {k: v[:15] for k, v in reg.items() if v}
                    ctx.close()
                r["senales"] = senales(r)
                nav.guardar_json(os.path.join(out, prefijo + ".json"), r)
                print(f"\n{url} [{vista}]")
                if "error" in r["estados"]["inicial"]:
                    print("  " + r["estados"]["inicial"]["error"])
                for s in r["senales"]:
                    print(f"  {s['heuristica']:22} {s['senal']}: {s['detalle'][:90]}")
                total = sum(len(v) for m in r["bloqueado_por_la_prueba"].values() for v in m.values())
                print(f"  peticiones abortadas por la prueba: {total}")
        browser.close()


if __name__ == "__main__":
    main()
