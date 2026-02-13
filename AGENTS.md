# Bonk — Agent Reference

## Development Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and Python 3.14.

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

```
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

- **Language**: Python 3.14
- **Graphics**: pygame-ce
- **Package manager**: uv
- **Linter/Formatter**: ruff
- **Tests**: pytest
- **Build**: PyInstaller (for standalone executables)
