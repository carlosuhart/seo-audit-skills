"""Marca hallazgos sobre capturas: recuadro de color por severidad y el ID del hallazgo.

Dos modos:
  1. Página en vivo, por selector CSS (lo habitual): toma la captura de página completa y dibuja el recuadro
     sobre la posición real de cada elemento.
  2. Imagen existente (exportación de Figma o captura entregada por el cliente): coordenadas como fracción
     (0 a 1) del ancho y alto de la imagen.

Basado en annotate.py de EliaAlberti/ux-audit-skill (MIT, https://github.com/EliaAlberti/ux-audit-skill),
ampliado con el modo por selector y la escala de severidad de esta skill.

marcas.json, modo 1:
  {"url": "https://sitio.cl/", "vista": "movil", "marcas": [{"id": "UX-03", "sev": 3, "selector": "#cf-telefono"}]}
marcas.json, modo 2:
  {"imagen": "frame.png", "marcas": [{"id": "UX-07", "sev": 2, "x": 0.06, "y": 0.42, "w": 0.88, "h": 0.10}]}

sev: 4 crítica (rojo), 3 alta (naranja), 2 media (amarillo), 1 baja (azul), 0 fortaleza (verde).

Uso (PowerShell):
  py scripts/anotar_capturas.py marcas.json --out <archivo.png> [--bloquear-host <servicio-geoip>]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import navegador as nav  # noqa: E402

COLORES = {4: "#C62828", 3: "#EF6C00", 2: "#F9A825", 1: "#1565C0", 0: "#2E7D32"}


def fuente(tam: int):
    for ruta in ("C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Helvetica.ttc",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(ruta, tam)
        except Exception:  # noqa: BLE001
            continue
    return ImageFont.load_default()


def dibujar(img: Image.Image, cajas: list[dict]) -> Image.Image:
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)
    W, H = img.size
    escala = max(1.0, min(W, 1600) / 1200.0)
    grosor = max(3, round(4 * escala))
    tam = max(16, round(22 * escala))
    f = fuente(tam)
    pad = round(tam * 0.35)
    for c in cajas:
        color = COLORES.get(int(c.get("sev", 2)), "#EF6C00")
        x0, y0, x1, y1 = c["x0"], c["y0"], c["x1"], c["y1"]
        d.rectangle([x0, y0, x1, y1], outline=color, width=grosor)
        etiqueta = str(c["id"])
        tw = d.textlength(etiqueta, font=f)
        ph = tam + 2 * pad
        py = y0 - ph - grosor if y0 - ph - grosor > 0 else y1 + grosor
        py = min(py, H - ph)
        px = min(max(0, x0), W - (tw + 2 * pad))
        d.rectangle([px, py, px + tw + 2 * pad, py + ph], fill=color)
        d.text((px + pad, py + pad), etiqueta, fill="white", font=f)
    return img


def modo_imagen(spec: dict, base: str) -> tuple[Image.Image, list[str]]:
    ruta = spec["imagen"] if os.path.isabs(spec["imagen"]) else os.path.join(base, spec["imagen"])
    img = Image.open(ruta)
    W, H = img.size
    cajas = [{"id": m["id"], "sev": m.get("sev", 2), "x0": m["x"] * W, "y0": m["y"] * H,
              "x1": (m["x"] + m.get("w", 0.05)) * W, "y1": (m["y"] + m.get("h", 0.05)) * H} for m in spec["marcas"]]
    return dibujar(img, cajas), []


def modo_url(spec: dict, hosts, tmp_png: str) -> tuple[Image.Image, list[str]]:
    from playwright.sync_api import sync_playwright
    no_encontrados = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = nav.nuevo_contexto(b, spec.get("vista", "escritorio"), reduced_motion="reduce")
        page = ctx.new_page()
        nav.instalar_bloqueos(page, hosts, True)
        if nav.abrir(page, nav.validar_url(spec["url"])) is None:
            b.close()
            sys.exit(f"No se pudo abrir {spec['url']} (¿sin conexión o sitio caído?). No se generó la captura.")
        nav.aplicar_acciones(page, spec.get("clics"))
        nav.recorrer_scroll(page)
        cajas = []
        for m in spec["marcas"]:
            try:
                r = page.evaluate("""(s) => { const e = document.querySelector(s); if (!e) return null;
                    const r = e.getBoundingClientRect(); return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; }""",
                                  m["selector"])
            except Exception:  # noqa: BLE001  selector CSS inválido
                r = None
            if not r or r["w"] == 0:
                no_encontrados.append(m["id"])
                continue
            m_ = 6
            cajas.append({"id": m["id"], "sev": m.get("sev", 2), "x0": r["x"] - m_, "y0": r["y"] - m_,
                          "x1": r["x"] + r["w"] + m_, "y1": r["y"] + r["h"] + m_})
        # scale="css": las cajas están en píxeles CSS; en móvil (densidad 2) la captura debe estar en la misma escala
        page.screenshot(path=tmp_png, full_page=True, scale="css")
        ctx.close()
        b.close()
    img = dibujar(Image.open(tmp_png), cajas)
    if cajas and not spec.get("pagina_completa"):  # recorte alrededor de las marcas, para que la captura sirva en un Fix
        W, H = img.size
        top = max(0, int(min(c["y0"] for c in cajas)) - 260)
        bot = min(H, int(max(c["y1"] for c in cajas)) + 260)
        img = img.crop((0, top, W, bot))
    return img, no_encontrados


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marcas")
    ap.add_argument("--out", required=True)
    ap.add_argument("--bloquear-host", action="append")
    a = ap.parse_args()
    with open(a.marcas, encoding="utf-8") as fh:
        spec = json.load(fh)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if "url" in spec:
        img, faltan = modo_url(spec, a.bloquear_host, a.out + ".base.png")
    elif "imagen" in spec:
        img, faltan = modo_imagen(spec, os.path.dirname(os.path.abspath(a.marcas)))
    else:
        sys.exit("marcas.json necesita 'url' o 'imagen'.")
    img.save(a.out)
    if os.path.exists(a.out + ".base.png"):
        os.remove(a.out + ".base.png")
    print(json.dumps({"salida": a.out, "marcas": len(spec["marcas"]) - len(faltan), "no_encontradas": faltan},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
