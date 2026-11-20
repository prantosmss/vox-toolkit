import json, os, re, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "manifest.json"


def load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def slug(text, n=50):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:n] or "asset"


def http_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "VoxToolkit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "VoxToolkit/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def log_asset(path, source, source_url, license_name, query):
    ASSETS.mkdir(exist_ok=True)
    data = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    data.append({
        "file": str(Path(path).relative_to(ROOT)),
        "source": source,
        "source_url": source_url,
        "license": license_name,
        "query": query,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    })
    MANIFEST.write_text(json.dumps(data, indent=2))


def parse_options(parts):
    opts = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            opts[k.strip()] = v.strip().strip('"')
    return opts
