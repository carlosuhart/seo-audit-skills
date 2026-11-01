"""Escaneo automático WCAG 2.2 A/AA con axe-core sobre páginas en vivo (Playwright, Python).

Cubre solo lo que una máquina puede comprobar. Cada resultado "incomplete" de axe es revisión manual
obligatoria: se guarda aparte, nunca se descarta. Un informe sin incumplimientos de axe NO significa
que la página cumpla WCAG.

Uso (PowerShell):
  py scripts/setup_axe.py   # una vez
  py scripts/axe_scan.py https://sitio.cl/ https://sitio.cl/contacto --vistas escritorio,movil --out <dir>
  py scripts/axe_scan.py --urls-archivo urls.txt --out <dir>
  # Estado tras abrir algo (menú, modal): se escanea la página con ese estado
  py scripts/axe_scan.py https://sitio.cl/ --clic "button[aria-controls=menu]" --estado menu --out <dir>
  # Formulario con errores visibles, sin enviar nada al servidor
  py scripts/axe_scan.py https://sitio.cl/contacto --enviar-vacio "form#contacto" --out <dir>
  # Sitio que redirige el idioma por IP
  py scripts/axe_scan.py https://sitio.com/en/contact --bloquear-host <servicio-geoip> --out <dir>

Opciones:
  --vistas escritorio,movil  (por defecto escritorio,movil)
  --best-practice            pasada adicional con reglas de buenas prácticas (no son incumplimientos WCAG)
  --sin-envios               aborta toda petición no GET (se activa solo con --enviar-vacio)

Salida: <out>/axe_<slug>_<vista>[_<estado>].json y <out>/axe_resumen_<estado>.json con el agregado.
Cada JSON incluye versión de axe, URL, vista, estado, fecha, bloqueos aplicados y, por regla: id,
impacto, criterios WCAG, nodos (selector, fragmento HTML, resumen del fallo).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import navegador as nav  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXE_JS = os.path.join(RAIZ, "vendor", "axe.min.js")
TAGS_WCAG22AA = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"]  # wcag22a: reglas futuras
MAX_NODOS = 25


def criterios(tags: list[str]) -> list[str]:
    """'wcag143' -> '1.4.3'; 'wcag2411' -> '2.4.11'. Ignora tags de nivel (wcag2aa, wcag21a)."""
    out = []
    for t in tags:
        m = re.fullmatch(r"wcag(\d)(\d)(\d{1,2})", t)
        if m:
            out.append(f"{m.group(1)}.{m.group(2)}.{m.group(3)}")
    return out


def cargar_axe() -> str:
    if not os.path.exists(AXE_JS):
        sys.exit("Falta vendor/axe.min.js. Ejecuta antes: py scripts/setup_axe.py")
    with open(AXE_JS, encoding="utf-8") as f:
        fuente = f.read()
    es = os.path.join(RAIZ, "vendor", "axe-es.json")
    if os.path.exists(es):  # textos de reglas y resúmenes en español
        with open(es, encoding="utf-8") as f:
            fuente += f"\n;axe.configure({{locale: {f.read()}}});"
    return fuente


def inyectar(page, fuente: str) -> None:
    """axe solo analiza los marcos donde también está cargado: se inyecta en todos."""
    for fr in page.frames:
        try:
            fr.evaluate(fuente)
        except Exception:  # noqa: BLE001  marcos de terceros que se cierran o bloquean
            pass


def correr_axe(page, tags: list[str]) -> dict:
    return page.evaluate(
        """async (tags) => {
            const r = await axe.run(document, {runOnly: {type: 'tag', values: tags},
                                               resultTypes: ['violations', 'incomplete']});
            const pick = list => list.map(v => ({id: v.id, impact: v.impact, tags: v.tags, help: v.help,
              helpUrl: v.helpUrl, n: v.nodes.length,
              nodes: v.nodes.slice(0, %d).map(n => ({target: n.target.flat ? n.target.flat().join(' ') : String(n.target),
                html: (n.html || '').slice(0, 300), resumen: (n.failureSummary || '').slice(0, 400)}))}));
            return {version: axe.version, violations: pick(r.violations), incomplete: pick(r.incomplete),
                    passes: r.passes.length, inapplicable: r.inapplicable.length};
        }""" % MAX_NODOS,
        tags,
    )


def enviar_vacio(page, form_sel: str, registro: dict) -> dict:
    """Pulsa el botón de envío del formulario sin rellenar nada, en modo estricto (navegador.py): nada sale
    del navegador salvo recursos estáticos del mismo dominio."""
    nav.activar_modo_estricto(page, registro)
    info = {"formulario": form_sel, "pulsado": False}
    botones = "button[type=submit], input[type=submit], button:not([type])"
    try:
        forms = page.locator(form_sel)
        for i in range(forms.count()):  # el primero VISIBLE con botón: suele haber formularios ocultos (modales)
            boton = forms.nth(i).locator(botones).first
            if boton.count() and boton.is_visible():
                if (forms.nth(i).get_attribute("method") or "get").lower() == "get" and forms.nth(i).get_attribute("action"):
                    info["error"] = "formulario GET con action: se omite (enviarlo navegaría con los campos en la URL)"
                    return info
                url_antes = page.url
                boton.scroll_into_view_if_needed(timeout=4000)
                boton.click(timeout=4000)
                page.wait_for_timeout(1500)
                info.update({"pulsado": True, "indice": i, "boton": (boton.inner_text(timeout=1000) or "")[:40]})
                if page.url != url_antes:  # navegó o quedó en chrome-error://: no se escanea esa página
                    info["error"] = f"la página cambió tras pulsar ({page.url[:80]}); no se escanea el estado"
                return info
        info["error"] = "ningún formulario visible con botón de envío coincide con el selector"
    except Exception as e:  # noqa: BLE001
        info["error"] = str(e)[:200]
    return info


def normalizar(res: dict) -> dict:
    for clave in ("violations", "incomplete"):
        for v in res.get(clave, []):
            v["criterios"] = criterios(v.get("tags", []))
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls-archivo")
    ap.add_argument("--vistas", default="escritorio,movil")
    ap.add_argument("--clic", action="append", help="selector a pulsar antes de escanear (repetible)")
    ap.add_argument("--estado", default="", help="nombre corto del estado alcanzado con --clic")
    ap.add_argument("--enviar-vacio", help="selector del formulario a enviar vacío (sin enviar nada al servidor)")
    ap.add_argument("--bloquear-host", action="append")
    ap.add_argument("--sin-envios", action="store_true")
    ap.add_argument("--best-practice", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    urls = nav.leer_urls(a.urls, a.urls_archivo)
    vistas = [v.strip() for v in a.vistas.split(",") if v.strip()]
    sin_envios = a.sin_envios or bool(a.enviar_vacio)
    estado = a.estado or ("errores-formulario" if a.enviar_vacio else "inicial")
    fuente = cargar_axe()
    out_dir = nav.carpeta_salida(a.out)
    resumen = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for url in urls:
            for vista in vistas:
                ctx = nav.nuevo_contexto(browser, vista)
                page = ctx.new_page()
                bloqueos = nav.instalar_bloqueos(page, a.bloquear_host, sin_envios)
                status = nav.abrir(page, url)
                fila = {"url": url, "vista": vista, "estado": estado, "http": status, "fecha": nav.ahora()}
                if status is None:
                    fila["error"] = "no se pudo abrir"
                    resumen.append(fila)
                    ctx.close()
                    continue
                if status >= 400:
                    print(f"[aviso] {url} respondió HTTP {status}: se escanea igual, pero revisa la URL", file=sys.stderr)
                fallidos = nav.aplicar_acciones(page, a.clic)
                envio = enviar_vacio(page, a.enviar_vacio, bloqueos) if a.enviar_vacio else None
                if envio and envio.get("error"):
                    fila["error"] = envio["error"]
                    print(f"{vista:10} {url} -> estado de formulario no escaneado: {envio['error']}")
                    resumen.append(fila)
                    ctx.close()
                    continue
                inyectar(page, fuente)
                res = normalizar(correr_axe(page, TAGS_WCAG22AA))
                if a.best_practice:
                    bp = correr_axe(page, ["best-practice"])
                    res["best_practice"] = bp["violations"]
                res.update({"url": url, "url_final": page.url, "vista": vista, "estado": estado,
                            "http": status, "fecha": nav.ahora(), "clics_fallidos": fallidos,
                            "envio_vacio": envio, "bloqueos": {k: v[:20] for k, v in bloqueos.items()},
                            "tags": TAGS_WCAG22AA})
                nombre = f"axe_{nav.slug(url)}_{vista}" + (f"_{nav.slug(estado, 20)}" if estado != "inicial" else "")
                nav.guardar_json(os.path.join(out_dir, nombre + ".json"), res)
                por_impacto: dict[str, int] = {}
                for v in res["violations"]:
                    por_impacto[v["impact"] or "sin-impacto"] = por_impacto.get(v["impact"] or "sin-impacto", 0) + 1
                fila.update({"archivo": nombre + ".json", "axe": res["version"],
                             "reglas_incumplidas": len(res["violations"]),
                             "nodos_incumplidos": sum(v["n"] for v in res["violations"]),
                             "por_impacto": por_impacto, "revision_manual": len(res["incomplete"]),
                             "clics_fallidos": fallidos, "url_final": page.url})
                resumen.append(fila)
                print(f"{vista:10} {url} -> {fila['reglas_incumplidas']} reglas, "
                      f"{fila['nodos_incumplidos']} nodos, {fila['revision_manual']} a revisar a mano"
                      + (f"  [clics fallidos: {fallidos}]" if fallidos else ""))
                ctx.close()
        browser.close()
    nav.guardar_json(os.path.join(out_dir, f"axe_resumen_{nav.slug(estado, 20)}.json"), resumen)


if __name__ == "__main__":
    main()
