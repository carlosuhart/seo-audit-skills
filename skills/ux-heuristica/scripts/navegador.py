"""Utilidades compartidas de navegador para los scripts de ux-heuristica.

Lo importan ui_medicion.py, estados_formulario.py y anotar_capturas.py (copia del mismo módulo de accesibilidad-wcag).

Decisiones que afectan a todos los scripts:
- bypass_csp=True: sin esto la CSP de muchos sitios bloquea los scripts que se inyectan (axe, utilidades).
- service_workers="block": un service worker podría reenviar peticiones que las rutas no ven.
- Las rutas se instalan en el CONTEXTO (cubren popups y ventanas nuevas), no solo en la página.
- Bloqueo opcional de hosts (--bloquear-host): p. ej. un servicio de geolocalización por IP que redirige
  el idioma y falsea la prueba. Se usa una ruta "**/*" que aborta si el host aparece en la URL, porque un
  patrón tipo "**/host/**" no captura todas las peticiones.
- Bloqueo de envíos (parámetro sin_envios de instalar_bloqueos): aborta toda petición que no sea
  GET/HEAD/OPTIONS y cierra los WebSockets.
- Modo estricto (activar_modo_estricto), para probar formularios: desde ANTES de rellenar solo pasan los
  recursos estáticos del mismo dominio (script, estilos, imágenes, fuentes). Se abortan las navegaciones,
  los fetch/XHR de cualquier método, todo tercero (píxeles de conversión de Ads, Meta, GTM, LinkedIn) y
  los formularios GET. Así una prueba no registra conversiones falsas ni deja datos en ningún servidor.
- Ningún script envía datos personales. Los datos de prueba son ficticios (@example.com).
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Iterable
from urllib.parse import urlparse

VIEWPORTS: dict[str, dict[str, Any]] = {
    "escritorio": {"viewport": {"width": 1280, "height": 900}, "is_mobile": False, "has_touch": False,
                   "device_scale_factor": 1},
    "movil": {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True,
              "device_scale_factor": 2},
}

UA_ESCRITORIO = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/141.0.0.0 Safari/537.36")
UA_MOVIL = ("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/141.0.0.0 Mobile Safari/537.36")

METODOS_PERMITIDOS_SIN_ENVIO = {"GET", "HEAD", "OPTIONS"}


def validar_url(url: str) -> str:
    """Acepta solo http(s) con host. Devuelve la URL o termina con error."""
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.netloc:
        sys.exit(f"URL no válida (solo http/https): {url}")
    return url


def leer_urls(urls: Iterable[str], archivo: str | None) -> list[str]:
    """Junta URLs de la línea de comandos y de un archivo (una por línea, # comenta)."""
    out = list(urls or [])
    if archivo:
        with open(archivo, encoding="utf-8") as f:
            out += [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    if not out:
        sys.exit("Indica al menos una URL o --urls-archivo.")
    return [validar_url(u) for u in out]


def nuevo_contexto(browser, vista: str, *, reduced_motion: str | None = None):
    """Crea un contexto con la vista pedida (escritorio | movil)."""
    if vista not in VIEWPORTS:
        sys.exit(f"Vista desconocida: {vista}. Usa: {', '.join(VIEWPORTS)}")
    cfg = dict(VIEWPORTS[vista])
    cfg["user_agent"] = UA_MOVIL if cfg["is_mobile"] else UA_ESCRITORIO
    cfg["bypass_csp"] = True
    cfg["locale"] = "es-CL"
    cfg["service_workers"] = "block"
    if reduced_motion:
        cfg["reduced_motion"] = reduced_motion
    ctx = browser.new_context(**cfg)
    ctx.add_init_script(script=JS_UTILS)  # helpers disponibles en cada página y marco
    return ctx


def instalar_bloqueos(page, hosts: list[str] | None, sin_envios: bool) -> dict[str, list[str]]:
    """Instala los bloqueos en el contexto de la página y devuelve el registro de lo bloqueado."""
    registro: dict[str, list[str]] = {"hosts": [], "envios": [], "estricto": []}
    hosts = [h.lower() for h in (hosts or []) if h]
    if not hosts and not sin_envios:
        return registro
    ctx = page.context

    def manejar(route):
        req = route.request
        url = req.url.lower()
        if hosts and any(h in url for h in hosts):
            registro["hosts"].append(req.url[:200])
            return route.abort()
        if sin_envios and req.method.upper() not in METODOS_PERMITIDOS_SIN_ENVIO:
            registro["envios"].append(f"{req.method} {req.url[:200]}")
            return route.abort()
        return route.fallback()

    ctx.route("**/*", manejar)
    if sin_envios:
        try:  # los WebSockets no pasan por route(): se cierran (LiveView, Socket.io, etc.)
            ctx.route_web_socket("**/*", lambda ws: ws.close())
        except Exception:  # noqa: BLE001  versiones antiguas de Playwright
            pass
    return registro


RECURSOS_ESTATICOS = {"script", "stylesheet", "image", "font", "media"}


def activar_modo_estricto(page, registro: dict[str, list[str]]) -> None:
    """Desde ahora solo pasan GET de recursos estáticos del mismo dominio. Todo lo demás se aborta.

    Se llama ANTES de rellenar un formulario: cubre validaciones remotas al salir del campo, envíos GET,
    navegaciones, píxeles de conversión de terceros y fetch/XHR. Registra lo abortado para el informe.
    Las rutas registradas después corren primero, así que esta tiene prioridad sobre instalar_bloqueos.
    """
    origen = urlparse(page.url).netloc.lower()
    raiz = ".".join(origen.split(".")[-2:])

    def manejar(route):
        req = route.request
        host = urlparse(req.url).netloc.lower()
        mismo = host == origen or host.endswith("." + raiz) or host == raiz
        q = urlparse(req.url.lower()).query  # los datos de prueba viajarían en el query, no en la ruta del archivo
        lleva_datos = any(m in q for m in ("example", "%40", "@", "prueba"))
        if req.method.upper() == "GET" and mismo and req.resource_type in RECURSOS_ESTATICOS and not lleva_datos:
            return route.fallback()
        registro.setdefault("estricto", []).append(f"{req.method} {req.resource_type} {req.url[:160]}")
        return route.abort()

    page.context.route("**/*", manejar)


def abrir(page, url: str, espera_ms: int = 1500) -> int | None:
    """Navega y espera a que la página se asiente. Devuelve el código HTTP o None."""
    resp = None
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=45000)
    except Exception:
        # Sitios con conexiones persistentes nunca llegan a networkidle: basta con load.
        try:
            resp = page.goto(url, wait_until="load", timeout=45000)
        except Exception as e:  # noqa: BLE001
            print(f"[aviso] no se pudo abrir {url}: {e}", file=sys.stderr)
            return None
    page.wait_for_timeout(espera_ms)
    return resp.status if resp else None


def aplicar_acciones(page, clics: list[str] | None, espera_ms: int = 800) -> list[str]:
    """Hace clic en selectores para llegar a un estado (menú abierto, modal, acordeón).

    Devuelve los selectores que no se pudieron pulsar (el estado no se alcanzó y hay que decirlo).
    """
    fallidos = []
    for sel in clics or []:
        try:
            page.locator(sel).first.click(timeout=5000)
            page.wait_for_timeout(espera_ms)
        except Exception:  # noqa: BLE001
            fallidos.append(sel)
    return fallidos


def recorrer_scroll(page, pausa_ms: int = 220, tope: int = 40) -> None:
    """Baja la página por tramos para disparar contenido diferido y animaciones de aparición, y vuelve arriba.

    Sin esto, una captura de página completa sale en blanco en sitios que revelan secciones al hacer scroll.
    """
    try:
        for _ in range(tope):
            fin = page.evaluate("() => { window.scrollBy(0, Math.round(innerHeight * 0.8)); "
                                "return innerHeight + scrollY >= document.documentElement.scrollHeight - 2; }")
            page.wait_for_timeout(pausa_ms)
            if fin:
                break
        page.evaluate("() => window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
    except Exception:  # noqa: BLE001
        pass


def slug(texto: str, largo: int = 60) -> str:
    t = re.sub(r"^https?://", "", texto.lower())
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:largo] or "pagina"


def carpeta_salida(base: str) -> str:
    os.makedirs(base, exist_ok=True)
    return base


def guardar_json(ruta: str, datos: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)


def ahora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def main() -> None:
    """CLI mínima de diagnóstico: muestra las vistas configuradas y valida una URL."""
    import argparse
    ap = argparse.ArgumentParser(description="Módulo compartido; muestra la configuración de vistas.")
    ap.add_argument("--url", help="URL a validar (solo http/https)")
    a = ap.parse_args()
    if a.url:
        validar_url(a.url)
    print(json.dumps({k: v["viewport"] for k, v in VIEWPORTS.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()


# JS reutilizable: selector estable y nombre accesible aproximado de un elemento.
JS_UTILS = r"""
window.__a11y = window.__a11y || (() => {
  const cs = el => getComputedStyle(el);
  const sel = el => {
    if (!el || el.nodeType !== 1) return '';
    if (el.id && /^[A-Za-z][\w-]*$/.test(el.id)) return '#' + el.id;
    const parts = [];
    let e = el, hops = 0;
    while (e && e.nodeType === 1 && hops < 4) {
      let s = e.tagName.toLowerCase();
      if (e.id && /^[A-Za-z][\w-]*$/.test(e.id)) { parts.unshift('#' + e.id); break; }
      const cls = [...e.classList].filter(c => !/^(css|sc|jsx|tw)-|^[a-z]{1,2}\d|__/.test(c)).slice(0, 2);
      if (cls.length) s += '.' + cls.join('.');
      const p = e.parentElement;
      if (p) { const same = [...p.children].filter(k => k.tagName === e.tagName);
        if (same.length > 1) s += ':nth-of-type(' + (same.indexOf(e) + 1) + ')'; }
      parts.unshift(s); e = e.parentElement; hops++;
    }
    return parts.join(' > ');
  };
  const name = el => {
    if (!el) return '';
    let n = (el.getAttribute('aria-label') || '').trim();
    if (!n && el.getAttribute('aria-labelledby')) n = el.getAttribute('aria-labelledby').split(/\s+/)
      .map(id => (document.getElementById(id) || {}).textContent || '').join(' ').trim();
    if (!n && el.labels && el.labels.length) n = [...el.labels].map(l => l.textContent).join(' ').trim();
    if (!n) n = (el.innerText || el.value || el.getAttribute('alt') || el.getAttribute('title') || '').trim();
    if (!n) n = [...el.querySelectorAll('img[alt], svg[aria-label]')].map(i => i.getAttribute('alt') || i.getAttribute('aria-label')).join(' ').trim();
    return n.replace(/\s+/g, ' ').slice(0, 80);
  };
  const visible = el => { if (!el || !el.getBoundingClientRect) return false; const s = cs(el); const r = el.getBoundingClientRect();
    return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05 && r.width > 0 && r.height > 0; };
  const deepActive = () => { let a = document.activeElement;
    while (a && a.shadowRoot && a.shadowRoot.activeElement) a = a.shadowRoot.activeElement; return a; };
  return {cs, sel, name, visible, deepActive};
})();
"""

