# Bonk 

Turning your PC into a 2004 DVD player on standby.

A bouncing DVD logo screensaver written in Python. It changes color every time it hits an edge, and yes it could hit the corner if you look at it long enough.

## Features

- Bouncing DVD logo on a black fullscreen background
- Random hue shift on every wall bounce
- Exits on any mouse movement, click, or keypress (screensaver behavior)
- Windows screensaver (.scr) support

## Development

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Getting Started

```bash
# Install dependencies
uv sync

# Launch the screensaver
uv run bonk
```

### Available Commands

- `uv sync` — Install dependencies
- `uv run bonk` — Launch screensaver fullscreen
- `uv run ruff check .` — Run linter
- `uv run pytest` — Run tests

See `AGENTS.md` for the complete command reference.

## Building a Standalone Executable

Build a single-file executable using PyInstaller:

```bash
uv sync --extra build
uv run pyinstaller --name bonk --onefile --windowed --add-data "assets:assets" src/bonk/__main__.py
```

The executable will be at `dist/bonk.exe`.

## Installing as a Windows Screensaver

1. **Build the executable:**
   ```bash
   build
   ```

2. **Rename and install:**
   ```powershell
   # Rename to .scr
   Rename-Item dist\bonk.exe bonk.scr

   # Copy to system directory
   Copy-Item bonk.scr C:\Windows\System32\

   # Or right-click bonk.scr → "Install"
   ```

3. In **Settings → Personalization → Lock Screen → Screen saver settings**, select `bonk`.
