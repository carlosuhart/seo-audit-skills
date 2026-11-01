"""Consolida axe_scan, teclado_foco y adaptacion en hallazgos WCAG 2.2 AA y una tabla de cobertura.

No decide la severidad final: la propone a partir de la regla (impacto de axe o tipo de prueba) y la persona
que audita la ajusta según el camino (un fallo en el formulario de contacto pesa más que en el pie).
Nunca declara "cumple": un criterio sin hallazgo automático queda como "sin hallazgo automático" o
"solo manual", porque las herramientas no prueban la conformidad.

Uso (PowerShell):
  py scripts/consolidar.py --dir <carpeta con los JSON> [--out <carpeta>]

Salida: <out>/hallazgos.json y <out>/hallazgos.md (tabla de hallazgos, revisión manual y cobertura).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import defaultdict
from urllib.parse import urlparse

CRITERIOS = {  # WCAG 2.2, niveles A y AA (4.1.1 eliminado). Nombres en español, uso de trabajo.
    "1.1.1": ("Contenido no textual", "A"), "1.2.1": ("Solo audio y solo vídeo (grabado)", "A"),
    "1.2.2": ("Subtítulos (grabado)", "A"), "1.2.3": ("Audiodescripción o alternativa (grabado)", "A"),
    "1.2.4": ("Subtítulos (en directo)", "AA"), "1.2.5": ("Audiodescripción (grabado)", "AA"),
    "1.3.1": ("Información y relaciones", "A"), "1.3.2": ("Secuencia significativa", "A"),
    "1.3.3": ("Características sensoriales", "A"), "1.3.4": ("Orientación", "AA"),
    "1.3.5": ("Identificar el propósito de la entrada", "AA"), "1.4.1": ("Uso del color", "A"),
    "1.4.2": ("Control del audio", "A"), "1.4.3": ("Contraste (mínimo)", "AA"),
    "1.4.4": ("Cambio de tamaño del texto", "AA"), "1.4.5": ("Imágenes de texto", "AA"),
    "1.4.10": ("Reajuste del contenido (reflow)", "AA"), "1.4.11": ("Contraste no textual", "AA"),
    "1.4.12": ("Espaciado del texto", "AA"), "1.4.13": ("Contenido al pasar el puntero o con foco", "AA"),
    "2.1.1": ("Teclado", "A"), "2.1.2": ("Sin trampas para el foco", "A"),
    "2.1.4": ("Atajos con una tecla", "A"), "2.2.1": ("Tiempo ajustable", "A"),
    "2.2.2": ("Pausar, detener, ocultar", "A"), "2.3.1": ("Tres destellos o menos", "A"),
    "2.4.1": ("Evitar bloques", "A"), "2.4.2": ("Título de la página", "A"), "2.4.3": ("Orden del foco", "A"),
    "2.4.4": ("Propósito de los enlaces (en contexto)", "A"), "2.4.5": ("Múltiples vías", "AA"),
    "2.4.6": ("Encabezados y etiquetas", "AA"), "2.4.7": ("Foco visible", "AA"),
    "2.4.11": ("Foco no oculto (mínimo)", "AA"), "2.5.1": ("Gestos del puntero", "A"),
    "2.5.2": ("Cancelación del puntero", "A"), "2.5.3": ("Etiqueta en el nombre", "A"),
    "2.5.4": ("Activación por movimiento", "A"), "2.5.7": ("Movimientos de arrastre", "AA"),
    "2.5.8": ("Tamaño del objetivo (mínimo)", "AA"), "3.1.1": ("Idioma de la página", "A"),
    "3.1.2": ("Idioma de las partes", "AA"), "3.2.1": ("Al recibir el foco", "A"),
    "3.2.2": ("Al introducir datos", "A"), "3.2.3": ("Navegación coherente", "AA"),
    "3.2.4": ("Identificación coherente", "AA"), "3.2.6": ("Ayuda coherente", "A"),
    "3.3.1": ("Identificación de errores", "A"), "3.3.2": ("Etiquetas o instrucciones", "A"),
    "3.3.3": ("Sugerencia ante errores", "AA"), "3.3.4": ("Prevención de errores (legales, financieros, datos)", "AA"),
    "3.3.7": ("Entrada redundante", "A"), "3.3.8": ("Autenticación accesible (mínimo)", "AA"),
    "4.1.2": ("Nombre, función, valor", "A"), "4.1.3": ("Mensajes de estado", "AA"),
}
assert len(CRITERIOS) == 55, len(CRITERIOS)

# Cobertura de axe por criterio (inferencia de la investigación del 31/10/2026, ver references/criterios-wcag22.md)
AXE_ALTA = {"1.4.3", "3.1.1"}
AXE_PARCIAL = {"2.2.1", "2.2.2", "1.1.1", "1.2.2", "1.3.1", "1.3.5", "1.4.1", "1.4.2", "1.4.4", "1.4.12", "2.1.1", "2.4.1", "2.4.2",
               "2.4.4", "2.5.3", "2.5.8", "3.1.2", "3.3.2", "4.1.2"}
SCRIPTS_PROPIOS = {"2.1.1", "2.1.2", "2.4.1", "2.4.2", "2.4.3", "2.4.7", "2.4.11", "1.4.4", "1.4.10", "1.4.12", "3.1.1"}

SEV = {"critical": "Crítica", "serious": "Grave", "moderate": "Moderada", "minor": "Menor"}
ORDEN_SEV = {"Crítica": 0, "Grave": 1, "Moderada": 2, "Menor": 3}


def cargar(patron: str) -> list[dict]:
    out = []
    for f in sorted(glob.glob(patron)):
        if os.path.basename(f).startswith("axe_resumen"):
            continue
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        d["_archivo"] = os.path.basename(f)
        out.append(d)
    return out


class Acumulador:
    def __init__(self) -> None:
        self.h: dict[str, dict] = {}

    def add(self, clave: str, *, criterios: list[str], titulo: str, severidad: str, confianza: str, fuente: str,
            url: str, vista: str, estado: str, ejemplos: list, n: int = 1, nota: str = "", asesoria: bool = False) -> None:
        """asesoria=True: la condición existe, pero por sí sola no es un incumplimiento del criterio (consejo de
        diseño o candidato que depende del contexto). Nunca marca el criterio como incumplido en la cobertura."""
        x = self.h.setdefault(clave, {"clave": clave, "criterios": criterios, "titulo": titulo, "severidad": severidad,
                                      "confianza": confianza, "fuente": fuente, "paginas": set(), "vistas": set(),
                                      "estados": set(), "ocurrencias": 0, "ejemplos": [], "nota": nota,
                                      "asesoria": asesoria})
        x["paginas"].add(url)
        x["vistas"].add(vista)
        x["estados"].add(estado)
        x["ocurrencias"] += n
        for e in ejemplos:
            if len(x["ejemplos"]) < 6 and e not in x["ejemplos"]:
                x["ejemplos"].append(e)


def no_auditable(r: dict) -> str | None:
    """Una página con error HTTP (bloqueo, desafío anti-bot, 404) o que terminó en otro dominio no se audita:
    sus resultados describirían la página de bloqueo, no el sitio."""
    http = r.get("http")
    if http is not None and http >= 400:
        return f"HTTP {http}"
    fin = r.get("url_final")
    if fin and urlparse(fin).netloc.lower().removeprefix("www.") != urlparse(r["url"]).netloc.lower().removeprefix("www."):
        return f"redirigió a {urlparse(fin).netloc}"
    return None


def procesar(d: str):
    acc, manual = Acumulador(), defaultdict(lambda: {"paginas": set(), "criterios": [], "ayuda": ""})
    paginas, excluidas = set(), {}
    filtro = lambda r: (excluidas.setdefault(r["url"], no_auditable(r)) if no_auditable(r) else None)  # noqa: E731
    for r in cargar(os.path.join(d, "axe_*.json")):
        if "violations" not in r or filtro(r):
            continue
        paginas.add(r["url"])
        for v in r["violations"]:
            acc.add(f"axe:{v['id']}", criterios=v.get("criterios", []), titulo=v["help"],
                    severidad=SEV.get(v["impact"], "Moderada"), confianza="Alta (axe, renderizado)", fuente="axe",
                    url=r["url"], vista=r["vista"], estado=r["estado"], n=v["n"],
                    ejemplos=[n["target"] for n in v["nodes"][:3]])
        for v in r["incomplete"]:
            m = manual[v["id"]]
            m["paginas"].add(r["url"])
            m["criterios"] = v.get("criterios", [])
            m["ayuda"] = v["help"]
    for r in cargar(os.path.join(d, "teclado_*.json")):
        if filtro(r):
            continue
        paginas.add(r["url"])
        res, base = r["resumen"], dict(url=r["url"], vista=r["vista"], estado=r["estado"])
        ej = lambda lista: [f"paso {p['paso']}: {p.get('nombre') or p['sel'][-60:]}" for p in lista[:4]]  # noqa: E731
        if res["foco_no_visible"]:
            acc.add("kbd:foco-no-visible", criterios=["2.4.7"], titulo="El elemento no cambia de aspecto al recibir el foco",
                    severidad="Grave", confianza="Media (diferencia de píxeles, confirmar en la captura)",
                    fuente="teclado", n=len(res["foco_no_visible"]), ejemplos=ej(res["foco_no_visible"]), **base)
        if res["foco_tapado_completo"]:
            acc.add("kbd:foco-tapado", criterios=["2.4.11"], titulo="Una capa fija tapa por completo el elemento enfocado",
                    severidad="Grave", confianza="Media (muestreo de puntos)", fuente="teclado",
                    n=len(res["foco_tapado_completo"]),
                    ejemplos=[f"paso {p['paso']}: {p.get('nombre', '')} tapado por {p.get('tapador', '')[-50:]}"
                              for p in res["foco_tapado_completo"][:4]], **base)
        if res.get("foco_en_contenido_no_visible"):
            acc.add("kbd:foco-invisible", criterios=["2.4.3", "2.4.7"],
                    titulo="El foco entra en contenido que no se ve (menú o diálogo cerrado en el orden de tabulación)",
                    severidad="Grave", confianza="Media (confirmar con la captura y a mano)", fuente="teclado",
                    n=len(res["foco_en_contenido_no_visible"]), ejemplos=ej(res["foco_en_contenido_no_visible"]), **base)
        if r.get("trampa"):
            t = r["trampa"]
            conf = t.get("confirmada")
            acc.add("kbd:trampa", criterios=["2.1.2"],
                    titulo="Trampa de teclado: el foco no sale del grupo" if conf else "El foco se repite en un grupo, pero sale con Esc o Shift+Tab",
                    severidad="Crítica" if conf else "Moderada", asesoria=not conf,
                    confianza="Media (ni Esc + Tab ni Shift+Tab salen del grupo; confirmar a mano)" if conf
                    else "Baja (revisar si el ciclo tiene sentido, p. ej. un menú abierto)",
                    fuente="teclado", ejemplos=[", ".join(s[-30:] for s in t.get("grupo", [])[:3])], **base)
        if res["foco_fuera_de_dialogo"]:
            acc.add("kbd:dialogo", criterios=["2.4.3"], titulo="Con el diálogo abierto, el foco sale del diálogo",
                    severidad="Grave", confianza="Media", fuente="teclado", n=len(res["foco_fuera_de_dialogo"]),
                    ejemplos=ej(res["foco_fuera_de_dialogo"]), **base)
        if r["candidatos_no_alcanzables"]:
            acc.add("kbd:no-alcanzable", criterios=["2.1.1"], titulo="Elementos con aspecto de control que no reciben foco",
                    severidad="Grave", confianza="Baja (candidatos: confirmar que hacen algo al pulsarlos)",
                    fuente="teclado", n=len(r["candidatos_no_alcanzables"]),
                    ejemplos=[f"{c['texto'][:30]} ({c['motivo']})" for c in r["candidatos_no_alcanzables"][:4]], **base)
        if r["tabindex_positivo"]:
            acc.add("kbd:tabindex", criterios=["2.4.3"], titulo="tabindex positivo altera el orden natural del foco",
                    severidad="Moderada", confianza="Alta (atributo en el DOM)", fuente="teclado", asesoria=True,
                    nota="Falla 2.4.3 (F44) solo si el orden resultante no tiene sentido: revisar el recorrido.",
                    n=len(r["tabindex_positivo"]), ejemplos=[t["sel"][-60:] for t in r["tabindex_positivo"][:3]], **base)
        if res["retrocesos_de_orden"]:
            acc.add("kbd:orden", criterios=["2.4.3"], titulo="El foco retrocede en la página (orden que no sigue la lectura)",
                    severidad="Moderada", confianza="Baja (revisar si el orden tiene sentido)", fuente="teclado", asesoria=True,
                    n=len(res["retrocesos_de_orden"]),
                    ejemplos=[f"paso {x['paso']}: sube {x['salto_px']} px" for x in res["retrocesos_de_orden"][:3]], **base)
        skip = r.get("salto_al_contenido")
        if skip is not None:
            if skip.get("existe") and not skip.get("funciona"):
                acc.add("kbd:skip-roto", criterios=["2.4.1"], titulo="El control para saltar al contenido no lleva el foco al contenido",
                        severidad="Grave", confianza="Media", fuente="teclado",
                        ejemplos=[skip.get("control", {}).get("nombre", "")], **base)
            elif not skip.get("existe"):
                acc.add("kbd:sin-skip", criterios=["2.4.1"], titulo="No hay control para saltar al contenido (en las 3 primeras paradas)",
                        severidad="Menor", confianza="Alta", asesoria=True,
                        nota="No es incumplimiento por sí solo: si la página tiene región main y encabezados, 2.4.1 "
                             "puede cumplirse por esa vía. Con menú largo antes del contenido conviene igual.",
                        fuente="teclado", ejemplos=[", ".join(skip.get("primeras_paradas", []))[:80]], **base)
    for r in cargar(os.path.join(d, "adaptacion_*.json")):
        if filtro(r):
            continue
        paginas.add(r["url"])
        base = dict(url=r["url"], vista="320px/640px", estado="inicial")
        rf = r.get("reflow_320", {})
        reales = [x for x in rf.get("desbordes", []) if not x["exento_posible"]]
        if rf.get("scroll_width", 0) > rf.get("client_width", 1) + 1 or reales:
            recortados = [x for x in reales if x.get("recortado")]
            acc.add("ada:reflow", criterios=["1.4.10"],
                    titulo="A 320 px hay scroll horizontal o contenido cortado (perdido) por un contenedor",
                    severidad="Grave", confianza="Media (medido; confirmar en la captura)", fuente="adaptación",
                    n=max(1, len(reales)),
                    ejemplos=[f"{x['sel'][-45:]} hasta {x['derecha_px']} px" + (" (recortado)" if x.get("recortado") else "")
                              for x in (recortados + reales)[:3]]
                    or [f"scrollWidth {rf.get('scroll_width')} > {rf.get('client_width')}"], **base)
        z = r.get("zoom_200", {})
        if z.get("scroll_width", 0) > z.get("client_width", 1) + 1:
            acc.add("ada:zoom", criterios=["1.4.4"], titulo="Equivalente a 200%: aparece scroll horizontal (revisar pérdida de contenido)",
                    severidad="Moderada", confianza="Baja (1.4.4 falla solo si se pierde contenido o función)",
                    fuente="adaptación", asesoria=True,
                    ejemplos=[f"scrollWidth {z.get('scroll_width')} > {z.get('client_width')}"], **base)
        fijos = [f for f in z.get("fijos", []) if not f.get("contenedor_transparente")]
        if sum(f["pct_alto_vista"] for f in fijos) >= 50:
            acc.add("ada:fijos", criterios=["2.4.11"],
                    titulo="Al 200%, los elementos fijos ocupan la mitad o más del alto de la pantalla",
                    severidad="Moderada", confianza="Baja (revisar si tapan contenido o foco)", fuente="adaptación",
                    asesoria=True, ejemplos=[f"{f['sel'][-40:]} {f['pct_alto_vista']}%" for f in fijos[:3]], **base)
        rec = r.get("espaciado_1412_recortes_nuevos", [])
        todos_sol = r.get("espaciado_1412_solapes_nuevos", [])
        sol = [s for s in todos_sol if not s.get("con_capa_fija")]
        fijos_sol = [s for s in todos_sol if s.get("con_capa_fija")]
        if fijos_sol:
            acc.add("ada:espaciado-fijo", criterios=["1.4.12"],
                    titulo="Con el espaciado de 1.4.12, una capa fija (cabecera) crece y se monta sobre el contenido",
                    severidad="Moderada", confianza="Baja (depende del scroll: revisar en la captura)",
                    fuente="adaptación", asesoria=True, n=len(fijos_sol),
                    ejemplos=[s["texto"][:30] for s in fijos_sol[:3]], **base)
        if rec or sol:
            solo_clamp = rec and not sol and all(x["line_clamp"] for x in rec)
            acc.add("ada:espaciado", criterios=["1.4.12"],
                    titulo="Con el espaciado de 1.4.12 hay texto recortado o que se monta sobre otro",
                    severidad="Menor" if solo_clamp else "Moderada", asesoria=bool(solo_clamp),
                    confianza="Baja (extractos truncados a propósito)" if solo_clamp else "Media",
                    fuente="adaptación", n=len(rec) + len(sol),
                    ejemplos=[x["texto"][:40] for x in (sol + rec)[:3]], **base)
        est = r.get("estructura", {})
        if est.get("lang_coincide") is False:
            acc.add("ada:lang", criterios=["3.1.1"], titulo=f"El atributo lang ({est.get('lang')}) no coincide con el idioma de la página",
                    severidad="Grave", confianza="Alta", fuente="adaptación", ejemplos=[est.get("lang", "")], **base)
        if est and not (est.get("title") or "").strip():
            acc.add("ada:sin-title", criterios=["2.4.2"], titulo="La página no tiene title",
                    severidad="Grave", confianza="Alta", fuente="adaptación", ejemplos=[""], **base)
        if est and est.get("main") == 0:
            acc.add("ada:sin-main", criterios=["1.3.1", "2.4.1"], titulo="No hay región principal (main)",
                    severidad="Menor", confianza="Alta", fuente="adaptación", asesoria=True,
                    nota="Buena práctica: por sí solo no incumple 1.3.1 ni 2.4.1.", ejemplos=[""], **base)
    return acc, manual, paginas, excluidas


def patron(n: int, total: int) -> str:
    if total > 1 and n == total:
        return "Sistémico"
    return "Plantilla" if n > 1 else "Página"


def cobertura(hallazgos: list[dict], manual: dict) -> list[dict]:
    con_hallazgo = defaultdict(list)
    for h in hallazgos:
        for c in h["criterios"]:
            # una señal de asesoría nunca cuenta como incumplimiento, aunque su confianza sea Alta
            con_hallazgo[c].append("Asesoria" if h.get("asesoria") else h["confianza"].split(" ")[0])
    en_manual = {c for m in manual.values() for c in m["criterios"]}
    filas = []
    for c, (nombre, nivel) in CRITERIOS.items():
        if c in con_hallazgo:
            estado = ("Incumplimiento detectado" if "Alta" in con_hallazgo[c]
                      else "Candidato a confirmar" if any(x != "Asesoria" for x in con_hallazgo[c])
                      else "Solo observaciones que por sí solas no incumplen; falta prueba manual")
        elif c in en_manual:
            estado = "Revisión manual pendiente (axe no concluyó)"
        elif c in AXE_ALTA or c in AXE_PARCIAL or c in SCRIPTS_PROPIOS:
            estado = "Sin hallazgo automático; falta prueba manual"
        else:
            estado = "Solo prueba manual"
        filas.append({"criterio": c, "nombre": nombre, "nivel": nivel, "estado": estado})
    return filas


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    out = a.out or a.dir
    acc, manual, paginas, excluidas = procesar(a.dir)
    excluidas = {u: m for u, m in excluidas.items() if m}
    total = len(paginas)
    hallazgos = []
    for h in acc.h.values():
        h["patron"] = patron(len(h["paginas"]), total)
        for k in ("paginas", "vistas", "estados"):
            h[k] = sorted(h[k])
        hallazgos.append(h)
    hallazgos.sort(key=lambda h: (ORDEN_SEV.get(h["severidad"], 9), -len(h["paginas"]), -h["ocurrencias"]))
    for i, h in enumerate(hallazgos, 1):
        h["id"] = f"A11Y-{i:02d}"
    man = [{"regla": k, "ayuda": v["ayuda"], "criterios": v["criterios"], "paginas": sorted(v["paginas"])}
           for k, v in manual.items()]
    cob = cobertura(hallazgos, manual)
    datos = {"paginas": sorted(paginas), "paginas_no_auditables": excluidas, "hallazgos": hallazgos,
             "revision_manual_axe": man, "cobertura": cob}
    with open(os.path.join(out, "hallazgos.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)

    L = [f"# Hallazgos automáticos WCAG 2.2 AA ({total} páginas)", "",
         "Resultados de herramientas: son la base de la auditoría, no la auditoría. Confirmar cada candidato y "
         "completar la prueba manual antes de reportar.", ""]
    if excluidas:
        L += ["## Páginas no auditables (fuera de los resultados)", "",
              "Respondieron con error o terminaron en otro dominio: los resultados describirían la página de bloqueo.", ""]
        L += [f"- {u}: {m}" for u, m in excluidas.items()] + [""]
    L += ["| ID | Severidad propuesta | Confianza | Criterio | Hallazgo | Patrón | Páginas | Vistas | Ejemplos |",
          "|---|---|---|---|---|---|---|---|---|"]
    for h in hallazgos:
        tipo = " (por sí solo no es incumplimiento: revisar)" if h.get("asesoria") else ""
        L.append(f"| {h['id']} | {h['severidad']} | {h['confianza']} | {', '.join(h['criterios'])} | {h['titulo']}{tipo} | "
                 f"{h['patron']} | {len(h['paginas'])} | {', '.join(h['vistas'])} | {'; '.join(map(str, h['ejemplos'][:3]))[:160]} |")
    L += ["", "## Revisión manual que pide axe (incomplete)", "", "| Regla | Criterios | Páginas | Qué revisar |", "|---|---|---|---|"]
    L += [f"| {m['regla']} | {', '.join(m['criterios'])} | {len(m['paginas'])} | {m['ayuda']} |" for m in man]
    L += ["", "## Cobertura por criterio (55 criterios A/AA)", "", "| Criterio | Nombre | Nivel | Estado |", "|---|---|---|---|"]
    L += [f"| {c['criterio']} | {c['nombre']} | {c['nivel']} | {c['estado']} |" for c in cob]
    with open(os.path.join(out, "hallazgos.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    resumen = defaultdict(int)
    for c in cob:
        resumen[c["estado"]] += 1
    print(json.dumps({"paginas": total, "hallazgos": len(hallazgos),
                      "por_severidad": {s: sum(1 for h in hallazgos if h["severidad"] == s) for s in ORDEN_SEV},
                      "cobertura": dict(resumen), "salida": os.path.join(out, "hallazgos.md")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
