# Bonk — Agent Reference

## Development Environment

This project uses [devenv](https://devenv.sh) for reproducible development environments.

### Quick Setup

```bash
devenv shell
setup        # runs: install-deps
dev
```

### Commands

| Command | Description |
|---------|-------------|
| `setup` | Initialize repo (runs: install-deps) |
| `dev` | Launch screensaver fullscreen (interactive) |
| `dev-start` | Start screensaver in background (non-interactive) |
| `dev-stop` | Stop background screensaver |
| `dev-status` | Check status of background processes |
| `dev-logs` | View last 50 lines of dev logs |
| `lint` | Run ruff linter |
| `lint-fix` | Run ruff with auto-fix |
| `format` | Run ruff formatter |
| `test` | Run pytest |
| `install-deps` | Install dependencies with uv |
| `build` | Build standalone executable with PyInstaller |

### For AI Agents

**IMPORTANT**: When working in this repository:

1. **Always use devenv scripts** — Run `lint` not `ruff check .`, `test` not `uv run pytest`
2. **Use non-interactive commands** — For automation, use:
   - `dev-start` instead of `dev` (runs in background, returns immediately)
   - `dev-stop` to stop background processes
   - `dev-status` to check if processes are running
   - `dev-logs` to view recent output (non-blocking)
3. **Check process status** — Before starting servers, run `dev-status`
4. **View logs for errors** — After starting, check `dev-logs` for issues

### Project Structure

```
bonk/
├── assets/              # DVD logo images
│   ├── dvd_logo.png
│   └── dvd_logo2.png
├── src/
│   └── dvd_screensaver/
│       ├── __init__.py
│       └── __main__.py  # Main screensaver implementation
├── devenv.nix           # Dev environment config
├── devenv.yaml          # Nix inputs
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
