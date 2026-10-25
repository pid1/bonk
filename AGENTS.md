# Bonk — Agent Reference

## Development Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and Python 3.15.

### Quick Setup

```bash
uv sync
uv run bonk
```

### Commands

- `uv sync` — Install dependencies
- `uv run bonk` — Launch screensaver fullscreen
- `uv run ruff check .` — Run ruff linter
- `uv run ruff check . --fix` — Run ruff with auto-fix
- `uv run ruff format .` — Run ruff formatter
- `uv run pytest` — Run tests
- `uv sync --extra build && uv run pyinstaller --name bonk --onefile --windowed --add-data "assets:assets" src/bonk/__main__.py` — Build standalone executable

### For AI Agents

**IMPORTANT**: When working in this repository:

1. **Use `uv run`** to run all Python tools and scripts
2. **Run `uv sync`** before running anything if dependencies may have changed
3. **Lint before committing** — Run `uv run ruff check .`

### Project Structure

```text
bonk/
├── assets/              # DVD logo images
│   ├── dvd_logo.png
│   └── dvd_logo2.png
├── src/
│   └── bonk/
│       ├── __init__.py
│       └── __main__.py  # Main screensaver implementation
├── pyproject.toml       # Python project config (uv)
└── README.md
```

### Tech Stack

- **Language**: Python 3.15
- **Graphics**: pygame-ce
- **Package manager**: uv
- **Linter/Formatter**: ruff
- **Tests**: pytest
- **Build**: PyInstaller (for standalone executables)

## Sadr

### Build and test

- `uv sync --locked --extra dev`, then `uv run ruff check .` and `uv run ruff format --check .`. Both pass on a clean tree.
- `uv run pytest` exits 5 because the repo has no tests and `tests/` does not exist. Exit 5 counts as passing.
- Smoke test on a headless host: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 5 uv run bonk`. Exit 124 (killed by `timeout`) means the app started and kept running.
- Build check: `uv sync --locked --extra build`, then the PyInstaller command above. With `--specpath DIR`, pass `--add-data "$PWD/assets:assets"`, because PyInstaller reads a relative data path from the spec folder.
- CI runs only Semgrep (`.github/workflows/semgrep.yml`). It runs no lint, test or build job.
