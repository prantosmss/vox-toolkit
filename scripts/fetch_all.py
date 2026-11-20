import re, subprocess, sys
from common import *

CUE = re.compile(r"^\[(FOOTAGE|IMAGE|LOGO|PERSON|ARTICLE|NEWSPAPER|SFX):\s*(.+?)\]\s*$")
SCRIPTS = {
    "FOOTAGE": "fetch_stock_video.py",
    "IMAGE": "fetch_stock_image.py",
    "LOGO": "fetch_logo.py",
    "PERSON": "fetch_person.py",
    "SFX": "fetch_audio.py",
    "ARTICLE": "screenshot.py",
    "NEWSPAPER": "screenshot.py",
}


def main():
    script_md = Path(sys.argv[1])
    here = Path(__file__).parent
    failed = []
    for line in script_md.read_text().splitlines():
        m = CUE.match(line.strip())
        if not m:
            continue
        kind, body = m.groups()
        parts = [p.strip() for p in body.split("|")]
        extra = ["sfx"] if kind == "SFX" else []
        cmd = [sys.executable, str(here / SCRIPTS[kind])] + extra + [parts[0]] + parts[1:]
        print("->", kind, parts[0])
        if subprocess.run(cmd).returncode != 0:
            failed.append(line.strip())
    if failed:
        print("\nMissing assets, review these cues:")
        for f in failed:
            print("  " + f)
        sys.exit(1)


if __name__ == "__main__":
    main()
