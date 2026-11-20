# Vox-style documentary toolkit

In any project folder, use:

    npx github:prantosmss/vox-toolkit

This copies the toolkit in (never overwriting existing files) and runs init.py, which creates a .venv, installs the packages there, and creates .env from .env.example. Then paste your API keys into .env and tell the agent to read instructions.md.

Alternative: `npx degit prantosmss/vox-toolkit` then `python init.py`.

Run scripts with the venv Python, for example `.venv/bin/python scripts/fetch_all.py script.md`.

## Landing page

The landing page lives in `docs/` (publish it with GitHub Pages: Settings > Pages > Deploy from branch > `/docs`). It is not part of the npm package and `npx` never copies it into your project.
