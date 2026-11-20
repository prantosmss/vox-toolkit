import os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
PY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run(cmd):
    print("->", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    if not VENV.exists():
        run([sys.executable, "-m", "venv", VENV])
    run([PY, "-m", "pip", "install", "--upgrade", "pip"])
    run([PY, "-m", "pip", "install", "-r", ROOT / "requirements.txt"])
    run([PY, "-m", "playwright", "install", "chromium"])

    env, example = ROOT / ".env", ROOT / ".env.example"
    if not env.exists() and example.exists():
        shutil.copy(example, env)
        print("Created .env. Open it and paste your API keys.")

    gitignore = ROOT / ".gitignore"
    lines = gitignore.read_text().splitlines() if gitignore.exists() else []
    for entry in (".env", ".venv/", "assets/", "__pycache__/"):
        if entry not in lines:
            lines.append(entry)
    gitignore.write_text("\n".join(lines) + "\n")

    print("\nDone. Run scripts with: " + str(PY))


if __name__ == "__main__":
    main()
