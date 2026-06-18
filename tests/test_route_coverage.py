from __future__ import annotations

import json
import re
from pathlib import Path

_COVERS = re.compile(r"#\s*v2:covers\s+(GET|POST|PUT|PATCH|DELETE)\s+(\S+)")
_RESOURCES = Path(__file__).resolve().parent.parent / "src" / "textql" / "resources"
_MANIFEST = Path(__file__).resolve().parent / "routes.manifest.json"


def _declared() -> set[str]:
    out: set[str] = set()
    for f in _RESOURCES.glob("*.py"):
        for method, path in _COVERS.findall(f.read_text()):
            out.add(f"{method} {path}")
    return out


def test_sdk_covers_every_backend_route() -> None:
    declared = _declared()
    manifest = set(json.loads(_MANIFEST.read_text()))
    assert declared == manifest, {
        "missing_in_sdk": sorted(manifest - declared),
        "stale_in_sdk": sorted(declared - manifest),
    }
