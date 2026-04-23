from __future__ import annotations

import json
import ssl
import urllib.parse
import urllib.request
from typing import Any, Dict, Tuple


def get_json(url: str, params: Dict[str, Any], headers: Dict[str, str] | None = None, timeout: int = 20) -> Tuple[Any, str | None]:
    query = urllib.parse.urlencode(params, doseq=True)
    full = f"{url}?{query}" if query else url
    req = urllib.request.Request(full, headers=headers or {}, method="GET")
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
