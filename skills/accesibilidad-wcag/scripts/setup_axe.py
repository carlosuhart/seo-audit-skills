"""Descarga axe-core en versión fija, verifica su integridad y lo deja en vendor/.

axe-core (Deque, MPL-2.0) no se versiona en el repo: se baja con npm y se comprueba el hash sha512 que
publica el registro. La MPL-2.0 obliga solo por archivo; se usa sin modificar y se conserva su LICENSE.

Uso (PowerShell):
  py scripts/setup_axe.py                 # versión fijada en AXE_VERSION
  py scripts/setup_axe.py --version 4.14.0
  py scripts/setup_axe.py --comprobar     # solo dice si vendor/ está listo y qué versión tiene

Salida: vendor/axe.min.js, vendor/axe-LICENSE.txt, vendor/axe-es.json (textos en español), vendor/axe-version.json
Requiere Node/npm en el PATH. No envía ningún dato del usuario: npm pack es una descarga anónima.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

AXE_VERSION = "4.14.0"  # revisar en cada actualización de fuentes de la skill
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(RAIZ, "vendor")


def npm() -> str:
    exe = shutil.which("npm") or shutil.which("npm.cmd")
    if not exe:
        sys.exit("No encuentro npm en el PATH. Instala Node.js o copia axe.min.js a vendor/ a mano.")
    return exe


def comprobar() -> dict | None:
    meta = os.path.join(VENDOR, "axe-version.json")
    if os.path.exists(meta) and os.path.exists(os.path.join(VENDOR, "axe.min.js")):
        with open(meta, encoding="utf-8") as f:
            return json.load(f)
    return None


def instalar(version: str) -> dict:
    exe = npm()
    integ = subprocess.run([exe, "view", f"axe-core@{version}", "dist.integrity"],
                           capture_output=True, text=True, check=False).stdout.strip()
    if not integ.startswith("sha512-"):
        sys.exit(f"npm no devolvió la integridad de axe-core@{version}. ¿Existe esa versión?")
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([exe, "pack", f"axe-core@{version}", "--silent"], cwd=tmp,
                           capture_output=True, text=True, check=False)
        tgz = os.path.join(tmp, f"axe-core-{version}.tgz")
        if r.returncode != 0 or not os.path.exists(tgz):
            sys.exit(f"npm pack falló: {r.stderr.strip()[:300]}")
        with open(tgz, "rb") as f:
            calc = "sha512-" + base64.b64encode(hashlib.sha512(f.read()).digest()).decode()
        if calc != integ:
            sys.exit("El hash del paquete NO coincide con el del registro npm. No se instala.")
        os.makedirs(VENDOR, exist_ok=True)
        with tarfile.open(tgz, "r:gz") as t:
            for miembro, destino in (("package/axe.min.js", "axe.min.js"), ("package/LICENSE", "axe-LICENSE.txt"),
                                     ("package/locales/es.json", "axe-es.json")):
                src = t.extractfile(miembro)
                if src is None:
                    sys.exit(f"Falta {miembro} en el paquete.")
                with open(os.path.join(VENDOR, destino), "wb") as out:
                    out.write(src.read())
    meta = {"version": version, "integrity": integ, "licencia": "MPL-2.0",
            "fuente": "https://github.com/dequelabs/axe-core"}
    with open(os.path.join(VENDOR, "axe-version.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default=AXE_VERSION)
    ap.add_argument("--comprobar", action="store_true")
    a = ap.parse_args()
    if a.comprobar:
        m = comprobar()
        print(json.dumps(m or {"listo": False}, ensure_ascii=False))
        sys.exit(0 if m else 1)
    m = comprobar()
    if m and m.get("version") == a.version and os.path.exists(os.path.join(VENDOR, "axe-es.json")):
        print(json.dumps({"listo": True, **m, "accion": "ya instalado"}, ensure_ascii=False))
        return
    print(json.dumps({"listo": True, **instalar(a.version), "accion": "instalado"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
