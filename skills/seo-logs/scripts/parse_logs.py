#!/usr/bin/env python3
"""
Purpose: Analiza logs de acceso de un sitio y resume la actividad de bots
         (buscadores, IA de entrenamiento, IA de búsqueda, IA por pedido de usuario).
Input:   Uno o más archivos de log (texto plano o .gz) en formato Apache/Nginx
         combined, LiteSpeed (mismo formato), JSON/NDJSON de Vercel Log Drains o
         NDJSON de Cloudflare Logpush (dataset http_requests). Opcionalmente un
         sitemap XML local, un CSV exportado de GSC y archivos JSON de rangos IP.
Output:  JSON en stdout (o en --output) con agregados por bot, sección, código
         de respuesta y día, más cruces con sitemap y GSC.
Usage:   py scripts/parse_logs.py access.log [access.log.1.gz ...]
             [--format auto|combined|vercel|cloudflare]
             [--sitemap sitemap.xml] [--gsc cobertura.csv] [--gsc-status "..."]
             [--known-urls urls.txt] [--verify-dns] [--dns-cache cache.json]
             [--ip-ranges GPTBot=gptbot.json] [--section-depth 1] [--top 50]
             [--host example.com] [--output resultado.json]

Solo usa la biblioteca estándar (Python 3.11+). No hace peticiones HTTP.
La verificación DNS solo se ejecuta con --verify-dns y solo para bots cuyo
método en references/bots.json incluye "rdns" (Googlebot, bingbot, Applebot,
CCBot). Las IP de clientes no se incluyen en la salida salvo con --show-ips.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import ipaddress
import json
import re
import socket
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlsplit, parse_qsl

DEFAULT_BOTS = Path(__file__).resolve().parent.parent / "references" / "bots.json"

# Apache/Nginx/LiteSpeed combined, con prefijo opcional de vhost (vhost_combined).
COMBINED_RE = re.compile(
    r'^(?:(?P<vhost>[^\s"]+:\d+)\s+)?(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<req>[^"]*)"\s+(?P<status>\d{3})\s+(?P<size>\S+)'
    r'(?:\s+"(?P<ref>[^"]*)"\s+"(?P<ua>[^"]*)")?'
)

ASSET_EXT = {
    ".css", ".js", ".mjs", ".map", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif",
    ".svg", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".webm", ".mp3",
    ".json", ".txt", ".xml", ".pdf", ".zip",
}
FEED_OR_META = {"/robots.txt", "/sitemap.xml", "/sitemap_index.xml", "/llms.txt", "/favicon.ico"}


# ---------------------------------------------------------------- lectura

def open_text(path: Path) -> Iterator[str]:
    """Itera líneas de un archivo de texto o .gz, tolerando bytes no UTF-8."""
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            yield from fh
    else:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            yield from fh


def detect_format(path: Path) -> str:
    """Detecta el formato mirando la primera línea no vacía."""
    for line in open_text(path):
        s = line.strip()
        if not s:
            continue
        if s.startswith("["):
            return "vercel"
        if s.startswith("{"):
            try:
                obj = json.loads(s)
            except json.JSONDecodeError:
                return "vercel"  # puede ser un array JSON con saltos de línea
            if "ClientRequestUserAgent" in obj or "ClientIP" in obj or "EdgeStartTimestamp" in obj:
                return "cloudflare"
            return "vercel"
        if COMBINED_RE.match(s):
            return "combined"
        raise ValueError(f"No se reconoce el formato de {path.name}; usa --format")
    raise ValueError(f"{path.name} está vacío")


def parse_time_combined(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        return None


def epoch_to_dt(value: Any) -> datetime | None:
    """Acepta segundos, milisegundos, nanosegundos o texto RFC 3339."""
    if value is None:
        return None
    if isinstance(value, str):
        if value.isdigit():
            value = int(value)
        else:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    if num > 1e17:
        num /= 1e9
    elif num > 1e14:
        num /= 1e6
    elif num > 1e11:
        num /= 1e3
    return datetime.fromtimestamp(num, tz=timezone.utc)


def records_combined(path: Path, stats: Counter) -> Iterator[dict[str, Any]]:
    for line in open_text(path):
        line = line.strip()
        if not line:
            continue
        m = COMBINED_RE.match(line)
        if not m:
            stats["lineas_no_reconocidas"] += 1
            continue
        parts = m.group("req").split()
        if len(parts) < 2:
            stats["lineas_no_reconocidas"] += 1
            continue
        host = m.group("vhost").rsplit(":", 1)[0] if m.group("vhost") else None
        yield {
            "ip": m.group("ip"),
            "time": parse_time_combined(m.group("time")),
            "method": parts[0],
            "target": parts[1],
            "status": int(m.group("status")),
            "ua": m.group("ua") or "",
            "host": host,
        }


def iter_json_objects(path: Path) -> Iterator[dict[str, Any]]:
    """Soporta NDJSON y arrays JSON (uno por línea o el archivo completo)."""
    lines = list(open_text(path))
    head = next((l.strip() for l in lines if l.strip()), "")
    if head.startswith("[") and not head.endswith("]"):
        data = json.loads("".join(lines))
        yield from (o for o in data if isinstance(o, dict))
        return
    for line in lines:
        s = line.strip().rstrip(",")
        if not s:
            continue
        try:
            obj = json.loads(s)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, list):
            yield from (o for o in obj if isinstance(o, dict))
        elif isinstance(obj, dict):
            yield obj


def records_vercel(path: Path, stats: Counter) -> Iterator[dict[str, Any]]:
    seen: set[str] = set()
    for obj in iter_json_objects(path):
        proxy = obj.get("proxy")
        if not isinstance(proxy, dict) or not proxy.get("path"):
            stats["registros_sin_proxy"] += 1  # build, stdout de funciones, etc.
            continue
        # Varias líneas de log de una misma petición comparten requestId.
        key = obj.get("requestId") or f'{proxy.get("timestamp")}|{proxy.get("path")}|{proxy.get("clientIp")}'
        if key in seen:
            stats["duplicados_por_requestId"] += 1
            continue
        seen.add(key)
        ua = proxy.get("userAgent") or ""
        if isinstance(ua, list):
            ua = ua[0] if ua else ""
        status = proxy.get("statusCode")
        if status in (None, -1):
            status = obj.get("statusCode")
        if status in (None, -1):
            stats["registros_sin_status"] += 1
            continue
        yield {
            "ip": proxy.get("clientIp") or "",
            "time": epoch_to_dt(proxy.get("timestamp") or obj.get("timestamp")),
            "method": proxy.get("method") or "GET",
            "target": proxy["path"],
            "status": int(status),
            "ua": ua,
            "host": proxy.get("host") or obj.get("host"),
        }


def records_cloudflare(path: Path, stats: Counter) -> Iterator[dict[str, Any]]:
    for obj in iter_json_objects(path):
        target = obj.get("ClientRequestURI") or obj.get("ClientRequestPath")
        status = obj.get("EdgeResponseStatus")
        if not target or status is None:
            stats["registros_incompletos"] += 1
            continue
        yield {
            "ip": obj.get("ClientIP") or "",
            "time": epoch_to_dt(obj.get("EdgeStartTimestamp")),
            "method": obj.get("ClientRequestMethod") or "GET",
            "target": target,
            "status": int(status),
            "ua": obj.get("ClientRequestUserAgent") or "",
            "host": obj.get("ClientRequestHost"),
            "cf_verified_category": obj.get("VerifiedBotCategory") or None,
        }


READERS = {"combined": records_combined, "vercel": records_vercel, "cloudflare": records_cloudflare}


# ---------------------------------------------------------------- clasificación

class BotTable:
    def __init__(self, path: Path):
        data = json.loads(path.read_text(encoding="utf-8"))
        self.bots = data["bots"]
        for b in self.bots:
            b["_re"] = re.compile(b["ua_pattern"], re.IGNORECASE)
        self.generic = re.compile(data.get("generic_bot_pattern", "bot|crawl|spider"), re.IGNORECASE)
        self._cache: dict[str, dict[str, Any] | None] = {}

    def classify(self, ua: str) -> dict[str, Any] | None:
        if ua in self._cache:
            return self._cache[ua]
        result = None
        for b in self.bots:
            if b["_re"].search(ua):
                result = b
                break
        if result is None and ua and self.generic.search(ua):
            result = {"name": "otro_bot", "operator": "?", "category": "otro_bot", "verify": {"method": ["ninguno"]}}
        self._cache[ua] = result
        return result


class Verifier:
    """FCrDNS con caché en disco y rangos IP desde archivos locales."""

    def __init__(self, use_dns: bool, cache_path: Path | None, max_lookups: int, ip_ranges: dict[str, list]):
        self.use_dns = use_dns
        self.cache_path = cache_path
        self.max_lookups = max_lookups
        self.lookups = 0
        self.ip_ranges = ip_ranges
        self.cache: dict[str, Any] = {}
        if cache_path and cache_path.exists():
            try:
                self.cache = json.loads(cache_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.cache = {}
        socket.setdefaulttimeout(3)

    def save(self) -> None:
        if self.cache_path and self.use_dns:
            self.cache_path.write_text(json.dumps(self.cache, indent=1), encoding="utf-8")

    def _fcrdns(self, ip: str, domains: list[str]) -> str:
        key = f"{ip}|{','.join(domains)}"
        if key in self.cache:
            return self.cache[key]
        if self.lookups >= self.max_lookups:
            return "pendiente"
        self.lookups += 1
        try:
            host = socket.gethostbyaddr(ip)[0].rstrip(".").lower()
        except socket.herror:
            result = "falso"  # sin PTR: no es un rastreador del operador
        except OSError:
            result = "pendiente"  # timeout o fallo de red: no concluir
        else:
            if not any(host == d or host.endswith("." + d) for d in domains):
                result = "falso"
            else:
                try:
                    infos = socket.getaddrinfo(host, None)
                    addrs = {i[4][0] for i in infos}
                    result = "verificado" if ip in addrs else "falso"
                except OSError:
                    result = "pendiente"
        if result != "pendiente":
            self.cache[key] = result
        return result

    def check(self, bot: dict[str, Any], ip: str) -> str:
        methods = bot.get("verify", {}).get("method", ["ninguno"])
        ranges = self.ip_ranges.get(bot["name"])
        if ranges and ip:
            try:
                addr = ipaddress.ip_address(ip)
                return "verificado" if any(addr in net for net in ranges) else "falso"
            except ValueError:
                return "pendiente"
        if self.use_dns and "rdns" in methods and ip:
            return self._fcrdns(ip, bot["verify"].get("rdns_domains", []))
        if methods == ["ninguno"]:
            return "no_verificable"
        return "sin_verificar"


def load_ip_ranges(specs: list[str]) -> dict[str, list]:
    """--ip-ranges NombreBot=archivo.json; recoge cualquier valor CIDR del JSON."""
    out: dict[str, list] = {}
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"--ip-ranges espera Bot=archivo.json, recibido: {spec}")
        name, file = spec.split("=", 1)
        data = json.loads(Path(file).read_text(encoding="utf-8"))
        nets: list = []

        def walk(node: Any) -> None:
            if isinstance(node, dict):
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
            elif isinstance(node, str) and "/" in node:
                try:
                    nets.append(ipaddress.ip_network(node, strict=False))
                except ValueError:
                    pass

        walk(data)
        out[name] = nets
    return out


# ---------------------------------------------------------------- URLs

def norm_path(target: str) -> tuple[str, str]:
    """Devuelve (ruta normalizada sin query, query)."""
    parts = urlsplit(target)
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path, parts.query


def section_of(path: str, depth: int) -> str:
    """Primeros `depth` segmentos de carpeta. Las URLs sin carpeta van a '/(raíz)'."""
    segs = [s for s in path.split("/") if s]
    if not segs:
        return "/"
    folders = segs[:-1]  # el último segmento es la página, no la sección
    if not folders:
        return "/(raíz)"
    return "/" + "/".join(folders[:depth]) + "/"


def is_asset(path: str) -> bool:
    if path in FEED_OR_META:
        return False
    return Path(path).suffix.lower() in ASSET_EXT


def load_sitemap_paths(files: list[str]) -> tuple[set[str], list[str]]:
    paths: set[str] = set()
    child_sitemaps: list[str] = []
    for f in files:
        tree = ET.parse(f)
        root = tree.getroot()
        tag = root.tag.split("}")[-1]
        for loc in root.iter():
            if loc.tag.split("}")[-1] != "loc" or not loc.text:
                continue
            if tag == "sitemapindex":
                child_sitemaps.append(loc.text.strip())
            else:
                paths.add(norm_path(loc.text.strip())[0])
    return paths, child_sitemaps


def load_gsc(path: str, fixed_status: str | None) -> dict[str, str]:
    """CSV de GSC (informe Páginas o inspección). Busca la columna de URL y la de estado."""
    raw = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    dialect = csv.Sniffer().sniff(raw.splitlines()[0], delimiters=",;\t")
    rows = list(csv.reader(raw.splitlines(), dialect))
    header = [h.strip().lower() for h in rows[0]]
    url_idx = next((i for i, h in enumerate(header) if "url" in h), None)
    if url_idx is None:
        raise ValueError("El CSV de GSC no tiene una columna con 'URL' en el encabezado")
    status_idx = next((i for i, h in enumerate(header)
                       if any(k in h for k in ("estado", "status", "motivo", "reason", "coverage", "cobertura", "indexación", "indexing"))), None)
    out: dict[str, str] = {}
    for r in rows[1:]:
        if len(r) <= url_idx or not r[url_idx].strip():
            continue
        status = fixed_status or (r[status_idx].strip() if status_idx is not None and len(r) > status_idx else "sin estado")
        out[norm_path(r[url_idx].strip())[0]] = status
    return out


# ---------------------------------------------------------------- agregación

def analyze(args: argparse.Namespace) -> dict[str, Any]:
    table = BotTable(Path(args.bots))
    verifier = Verifier(args.verify_dns, Path(args.dns_cache) if args.dns_cache else None,
                        args.verify_dns_max, load_ip_ranges(args.ip_ranges or []))
    stats: Counter = Counter()
    formats: dict[str, str] = {}

    total = Counter()
    by_bot: dict[str, dict[str, Any]] = {}
    by_cat = Counter()
    by_day_cat: dict[str, Counter] = defaultdict(Counter)
    google_paths: dict[str, dict[str, Any]] = {}
    bing_paths: set[str] = set()
    ai_paths: dict[str, set[str]] = defaultdict(set)
    spoof_ips: Counter = Counter()
    first_dt: datetime | None = None
    last_dt: datetime | None = None

    for f in args.logs:
        path = Path(f)
        fmt = args.format if args.format != "auto" else detect_format(path)
        formats[path.name] = fmt
        for rec in READERS[fmt](path, stats):
            if args.host and rec.get("host") and args.host not in rec["host"]:
                stats["filtrados_por_host"] += 1
                continue
            total["peticiones"] += 1
            dt = rec["time"]
            if dt:
                first_dt = dt if first_dt is None or dt < first_dt else first_dt
                last_dt = dt if last_dt is None or dt > last_dt else last_dt
            day = dt.date().isoformat() if dt else "sin_fecha"
            bot = table.classify(rec["ua"])
            if bot is None:
                total["no_bot"] += 1
                continue
            total["bots"] += 1
            name = bot["name"]
            ver = verifier.check(bot, rec["ip"]) if name != "otro_bot" else "no_verificable"
            if ver == "falso":
                spoof_ips[(name, rec["ip"])] += 1
            p, q = norm_path(rec["target"])
            sec = section_of(p, args.section_depth)
            status = rec["status"]
            b = by_bot.setdefault(name, {
                "operador": bot.get("operator"), "categoria": bot.get("category"),
                "peticiones": 0, "urls": set(), "status": Counter(), "secciones": Counter(),
                "dias": Counter(), "verificacion": Counter(), "con_parametros": 0,
                "parametros": Counter(), "redirecciones": 0, "errores_4xx": 0, "errores_5xx": 0,
                "recursos": 0, "top_urls": Counter(), "urls_404": Counter(), "urls_3xx": Counter(),
                "movil": 0,
            })
            b["peticiones"] += 1
            b["urls"].add(p)
            b["status"][str(status)] += 1
            b["secciones"][sec] += 1
            b["dias"][day] += 1
            b["verificacion"][ver] += 1
            b["top_urls"][p] += 1
            if "Mobile" in rec["ua"]:
                b["movil"] += 1
            if q:
                b["con_parametros"] += 1
                for k, _ in parse_qsl(q, keep_blank_values=True):
                    b["parametros"][k] += 1
            if 300 <= status < 400:
                b["redirecciones"] += 1
                b["urls_3xx"][p] += 1
            elif 400 <= status < 500:
                b["errores_4xx"] += 1
                if status in (404, 410):
                    b["urls_404"][p] += 1
            elif status >= 500:
                b["errores_5xx"] += 1
            if is_asset(p):
                b["recursos"] += 1
            by_cat[bot.get("category", "otro_bot")] += 1
            by_day_cat[day][bot.get("category", "otro_bot")] += 1
            if ver == "falso":
                continue  # no cuenta como rastreo real en los cruces
            if bot.get("operator") == "Google" and bot.get("category") == "buscador" and name != "Google-InspectionTool":
                g = google_paths.setdefault(p, {"hits": 0, "ultimo": None, "status": Counter()})
                g["hits"] += 1
                g["status"][str(status)] += 1
                if dt and (g["ultimo"] is None or dt > g["ultimo"]):
                    g["ultimo"] = dt
            if name == "bingbot":
                bing_paths.add(p)
            if str(bot.get("category", "")).startswith("ia_"):
                ai_paths[bot["category"]].add(p)

    verifier.save()
    top = args.top
    bots_out = {}
    for name, b in sorted(by_bot.items(), key=lambda kv: -kv[1]["peticiones"]):
        n = b["peticiones"]
        bots_out[name] = {
            "operador": b["operador"], "categoria": b["categoria"], "peticiones": n,
            "urls_unicas": len(b["urls"]),
            "verificacion": dict(b["verificacion"]),
            "status": dict(b["status"]),
            "pct_redirecciones": round(100 * b["redirecciones"] / n, 1),
            "pct_4xx": round(100 * b["errores_4xx"] / n, 1),
            "pct_5xx": round(100 * b["errores_5xx"] / n, 1),
            "pct_con_parametros": round(100 * b["con_parametros"] / n, 1),
            "pct_recursos": round(100 * b["recursos"] / n, 1),
            "pct_movil": round(100 * b["movil"] / n, 1),
            "parametros_top": dict(b["parametros"].most_common(10)),
            "secciones": dict(b["secciones"].most_common(top)),
            "por_dia": dict(sorted(b["dias"].items())),
            "top_urls": dict(b["top_urls"].most_common(top)),
            "urls_404_top": dict(b["urls_404"].most_common(top)),
            "urls_3xx_top": dict(b["urls_3xx"].most_common(top)),
        }

    result: dict[str, Any] = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archivos": formats,
        "periodo": {
            "desde": first_dt.isoformat() if first_dt else None,
            "hasta": last_dt.isoformat() if last_dt else None,
            "dias_con_datos": len([d for d in by_day_cat if d != "sin_fecha"]),
        },
        "totales": dict(total),
        "lectura": dict(stats),
        "por_categoria": dict(by_cat),
        "por_dia_y_categoria": {d: dict(c) for d, c in sorted(by_day_cat.items())},
        "bots": bots_out,
        "verificacion_dns": {
            "activada": args.verify_dns,
            "consultas_realizadas": verifier.lookups,
            "limite": args.verify_dns_max,
            "rangos_ip_cargados": {k: len(v) for k, v in verifier.ip_ranges.items()},
        },
        "suplantaciones": {
            "peticiones": sum(spoof_ips.values()),
            "por_bot": dict(sum((Counter({n: c}) for (n, _), c in spoof_ips.items()), Counter())),
        },
        "googlebot_urls_rastreadas": len(google_paths),
    }
    if args.show_ips:
        result["suplantaciones"]["ips_top"] = {f"{n} {ip}": c for (n, ip), c in spoof_ips.most_common(top)}

    known: set[str] = set()
    if args.known_urls:
        for line in Path(args.known_urls).read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                known.add(norm_path(line.strip())[0])

    if args.sitemap:
        sm_paths, children = load_sitemap_paths(args.sitemap)
        never = sorted(p for p in sm_paths if p not in google_paths)
        result["sitemap"] = {
            "urls_en_sitemap": len(sm_paths),
            "rastreadas_por_googlebot": len(sm_paths) - len(never),
            "nunca_rastreadas_por_googlebot": len(never),
            "pct_cobertura_googlebot": round(100 * (len(sm_paths) - len(never)) / len(sm_paths), 1) if sm_paths else None,
            "nunca_rastreadas_por_bingbot": len([p for p in sm_paths if p not in bing_paths]),
            "rastreadas_por_ia": {cat: len(sm_paths & s) for cat, s in ai_paths.items()},
            "lista_nunca_rastreadas_googlebot": never[:top],
            "sitemaps_hijos_no_cargados": children,
        }
        ref = sm_paths | known
        outside = Counter({p: g["hits"] for p, g in google_paths.items()
                           if p not in ref and not is_asset(p) and p not in FEED_OR_META})
        result["googlebot_fuera_de_sitemap"] = {
            "nota": "URLs que Googlebot pide y que no están en el sitemap" + (" ni en --known-urls" if known else "")
                    + ". Si responden 200 y no aparecen en un crawl interno, son candidatas a huérfanas.",
            "total": len(outside),
            "top": dict(outside.most_common(top)),
        }

    if args.gsc:
        gsc = load_gsc(args.gsc, args.gsc_status)
        groups: dict[str, dict[str, Any]] = {}
        for p, st in gsc.items():
            g = groups.setdefault(st, {"urls": 0, "con_googlebot": 0, "sin_googlebot": 0,
                                       "hits_googlebot": 0, "ejemplos_sin_googlebot": [], "ejemplos_con_googlebot": []})
            g["urls"] += 1
            info = google_paths.get(p)
            if info:
                g["con_googlebot"] += 1
                g["hits_googlebot"] += info["hits"]
                if len(g["ejemplos_con_googlebot"]) < top:
                    g["ejemplos_con_googlebot"].append({"url": p, "hits": info["hits"],
                                                        "ultimo": info["ultimo"].isoformat() if info["ultimo"] else None,
                                                        "status": dict(info["status"])})
            else:
                g["sin_googlebot"] += 1
                if len(g["ejemplos_sin_googlebot"]) < top:
                    g["ejemplos_sin_googlebot"].append(p)
        result["cruce_gsc"] = {
            "nota": "Cruce por ruta (sin host ni query). Sin Googlebot en el periodo = problema de descubrimiento o prioridad; "
                    "con Googlebot y sin indexar = problema de calidad, duplicado o canonical.",
            "por_estado": groups,
        }
    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Análisis de logs de acceso para SEO y bots de IA (salida JSON).")
    p.add_argument("logs", nargs="+", help="Archivos de log (.log, .gz, .json, .ndjson)")
    p.add_argument("--format", choices=["auto", "combined", "vercel", "cloudflare"], default="auto")
    p.add_argument("--bots", default=str(DEFAULT_BOTS), help="Tabla de bots (por defecto references/bots.json)")
    p.add_argument("--host", help="Filtra por host (contiene). Útil con logs de varios dominios")
    p.add_argument("--section-depth", type=int, default=1, help="Segmentos de ruta que definen una sección")
    p.add_argument("--top", type=int, default=50, help="Máximo de elementos en cada lista")
    p.add_argument("--sitemap", action="append", help="Sitemap XML local (repetible)")
    p.add_argument("--known-urls", help="TXT con URLs conocidas por crawl interno, una por línea")
    p.add_argument("--gsc", help="CSV exportado de GSC (informe Páginas o inspección)")
    p.add_argument("--gsc-status", help="Estado fijo para todo el CSV, si el export no trae columna de estado")
    p.add_argument("--verify-dns", action="store_true", help="Verifica por DNS inverso y directo los bots con método rdns")
    p.add_argument("--verify-dns-max", type=int, default=300, help="Máximo de IP nuevas a consultar")
    p.add_argument("--dns-cache", help="Archivo JSON de caché de DNS")
    p.add_argument("--ip-ranges", action="append", help="Bot=archivo.json con rangos IP descargados (repetible)")
    p.add_argument("--show-ips", action="store_true", help="Incluye en la salida las IP que suplantan bots")
    p.add_argument("--output", "-o", help="Escribe el JSON en este archivo")
    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = analyze(args)
    except Exception as exc:  # salida de error estructurada
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(json.dumps({"ok": True, "output": args.output, "peticiones": result["totales"].get("peticiones", 0)}))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
