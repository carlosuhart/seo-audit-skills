#!/usr/bin/env python3
"""
Purpose: Inventario de vigencia del catálogo de skills. Lee el frontmatter y el cuerpo de cada
         SKILL.md, extrae las fechas de revisión ("revisar", "review", "next_review"), las de
         fuentes ("fuentes", "sources", "Fuentes fechadas", "leídas el") y la última
         modificación, y clasifica cada skill como vencida, por vencer, vigente o sin fecha.
Input:   carpeta de skills (por defecto ~/.claude/skills), opcionalmente --dias-aviso N.
Output:  JSON con el resumen y la lista por estado. Código de salida 1 si hay vencidas.
Usage:   py vigencia.py [carpeta] [--dias-aviso 30] [--fuente-max-dias 180] [-o salida.json]
Solo stdlib. Solo lectura.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

RX_ISO = r"(20\d{2})-(\d{2})-(\d{2})"
RX_EU = r"(\d{1,2})/(\d{1,2})/(20\d{2})"
RX_REVISAR = re.compile(r"(?im)^\s*(?:revisar|review|next_review|revisión|revision)\s*:\s*['\"]?(" + RX_ISO + r"|" + RX_EU + r")")
RX_REVISAR_TXT = re.compile(r"(?i)revisar(?: el| antes del)?\s+(" + RX_EU + r"|" + RX_ISO + r")")
RX_FUENTE = re.compile(r"(?i)(?:fuentes?|sources?)[^\n]{0,80}?(" + RX_ISO + r"|" + RX_EU + r")")
RX_FUENTE2 = re.compile(
    r"(?i)(?:le[ií]d[oa]s? (?:el|en)|consultad[oa]s?(?: el)?|verificad[oa]s?(?: el)?|"
    r"revisad[oa]s?(?: el)?|actualizad[oa]s?(?: el)?|publicad[oa]s?(?: el)?|"
    r"retrieved|checked(?: on)?|verified(?: on)?|updated(?: on)?|published(?: on)?|"
    r"as of|fechad[oa]s?(?: al)?)[^\n]{0,60}?(" + RX_EU + r"|" + RX_ISO + r")")


def parse_fecha(s: str) -> dt.date | None:
    m = re.fullmatch(RX_ISO, s)
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.fullmatch(RX_EU, s)
        if not m:
            return None
        d, mo, y = map(int, m.groups())
    try:
        return dt.date(y, mo, d)
    except ValueError:
        return None


def fechas(rx: re.Pattern[str], texto: str) -> list[dt.date]:
    out = []
    for m in rx.finditer(texto):
        f = parse_fecha(m.group(1))
        if f:
            out.append(f)
    return out


def analizar(skill_md: Path, hoy: dt.date, dias_aviso: int, fuente_max: int) -> dict[str, Any]:
    t = skill_md.read_text(encoding="utf-8", errors="replace")
    nombre = skill_md.parent.name
    rev = fechas(RX_REVISAR, t) + fechas(RX_REVISAR_TXT, t)
    # Las fuentes fechadas suelen vivir en references/: se leen también, pero la fecha de
    # revisión solo cuenta desde el SKILL.md (es la que manda).
    refs = ""
    ref_dir = skill_md.parent / "references"
    if ref_dir.is_dir():
        refs = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted(ref_dir.glob("*.md")))
    hoy_max = hoy + dt.timedelta(days=1)  # una fecha futura no es una fuente
    fue = [f for f in fechas(RX_FUENTE, t + "\n" + refs) + fechas(RX_FUENTE2, t + "\n" + refs) if f <= hoy_max]
    mtime = dt.date.fromtimestamp(skill_md.stat().st_mtime)
    r: dict[str, Any] = {"skill": nombre, "modificado": mtime.isoformat()}
    if rev:
        prox = min(rev)
        r["revisar"] = prox.isoformat()
        dias = (prox - hoy).days
        r["dias_para_revisar"] = dias
        r["estado"] = "vencida" if dias < 0 else ("por_vencer" if dias <= dias_aviso else "vigente")
    elif fue:
        ult = max(fue)
        r["fuentes_mas_recientes"] = ult.isoformat()
        edad = (hoy - ult).days
        r["edad_fuentes_dias"] = edad
        r["estado"] = "fuentes_viejas" if edad > fuente_max else "vigente_por_fuentes"
    else:
        r["estado"] = "sin_fecha"
    return r


def main(a: argparse.Namespace) -> dict[str, Any]:
    raiz = Path(a.carpeta).expanduser()
    if not raiz.is_dir():
        raise FileNotFoundError(f"No existe la carpeta {raiz}")
    hoy = dt.date.fromisoformat(a.hoy) if a.hoy else dt.date.today()
    filas = []
    for md in sorted(raiz.glob("*/SKILL.md")):
        if md.parent.name.startswith(("_", ".")):
            continue
        filas.append(analizar(md, hoy, a.dias_aviso, a.fuente_max_dias))
    por_estado: dict[str, list[dict[str, Any]]] = {}
    for f in filas:
        por_estado.setdefault(f["estado"], []).append(f)
    orden = ["vencida", "por_vencer", "fuentes_viejas", "sin_fecha", "vigente_por_fuentes", "vigente"]
    return {
        "fecha": hoy.isoformat(),
        "carpeta": str(raiz),
        "total": len(filas),
        "resumen": {k: len(por_estado.get(k, [])) for k in orden},
        "detalle": {k: por_estado.get(k, []) for k in orden if k in por_estado},
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Vigencia del catálogo de skills")
    ap.add_argument("carpeta", nargs="?", default="~/.claude/skills")
    ap.add_argument("--dias-aviso", type=int, default=30, help="Días antes de la fecha de revisión para avisar")
    ap.add_argument("--fuente-max-dias", type=int, default=180, help="Edad máxima de las fuentes sin fecha de revisión")
    ap.add_argument("--hoy", help="Fecha de referencia AAAA-MM-DD (para pruebas)")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        res = main(args)
        txt = json.dumps(res, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(txt, encoding="utf-8")
            print(json.dumps({"guardado": args.output, "resumen": res["resumen"]}, ensure_ascii=False))
        else:
            print(txt)
        sys.exit(1 if res["resumen"].get("vencida") else 0)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
