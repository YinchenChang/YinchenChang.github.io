"""Copy the latest published HTML of each model from a local clone of
YinchenChang/company-models into models/<slug>.html (stable URLs for the map).

The authoritative files stay in company-models (<company>/dist/). This site only
mirrors the newest version. Run:  python3 tools/sync_models.py /path/to/company-models
"""
import json, re, shutil, sys
from pathlib import Path

# company-models folder -> stable slug on this site
MODELS = {
    "openai": "openai", "anthropic": "anthropic", "minimax": "minimax", "zhipu": "zhipu",
    "microsoft": "microsoft", "alphabet": "alphabet", "amazon": "amazon", "oracle": "oracle",
    "coreweave": "coreweave", "nebius": "nebius", "whitefiber": "whitefiber",
    "nvidia": "nvidia", "skhynix": "skhynix", "micron": "micron", "samsung": "samsung",
    "arista": "arista", "quanta": "quanta", "delta": "delta", "tsmc": "tsmc",
    "advantest": "advantest", "disco": "disco", "ibiden": "ibiden",
    "innolight": "innolight",
}

def version_key(name: str):
    # files are named YYYYMMDD_<name>_v<ver>.html; sort by date, then version numbers
    date = re.match(r"(\d{8})", name)
    ver = re.findall(r"\d+", name.split("_v")[-1]) if "_v" in name else []
    return (date.group(1) if date else "", [int(x) for x in ver])

def main(src: Path, dst: Path):
    manifest = {}
    for folder, slug in MODELS.items():
        dist = src / folder / "dist"
        files = [p for p in dist.glob("*.html")] if dist.exists() else []
        if not files:
            print(f"skip {folder}: no dist/*.html"); continue
        latest = max(files, key=lambda p: version_key(p.name))
        shutil.copyfile(latest, dst / f"{slug}.html")
        manifest[slug] = f"{folder}/dist/{latest.name}"
        print(f"{slug:12s} <- {manifest[slug]}")
    (dst / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(__file__).resolve().parent.parent / "models")
