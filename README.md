# Bonk 

Turning your PC into a 2004 DVD player on standby.

A bouncing DVD logo screensaver written in Python. It changes color every time it hits an edge, and yes it could hit the corner if you look at it long enough.

![dvdlogo](../assets/dvd_logo.png)

## Features

- Bouncing DVD logo on a black fullscreen background
- Random hue shift on every wall bounce
- Exits on any mouse movement, click, or keypress (screensaver behavior)
- Windows screensaver (.scr) support

## Development

### Prerequisites

- [Nix](https://nixos.org/download.html) with flakes enabled
- [devenv](https://devenv.sh/getting-started/)

### Getting Started

```bash
# Enter development environment
devenv shell

# Install dependencies
setup

# Launch the screensaver
dev
```

### Available Commands

Run these commands inside `devenv shell`:

- `setup` — Install dependencies
- `dev` — Launch screensaver fullscreen
- `build` — Build standalone executable with PyInstaller
- `lint` — Run linter
- `test` — Run tests

See `AGENTS.md` for the complete command reference.

### Without devenv

```bash
# Requires Python 3.14+ and uv
uv sync
uv run bonk
```

## Building a Standalone Executable

Build a single-file executable using PyInstaller:

```bash
# Inside devenv shell
build

# Or manually
uv sync --extra build
uv run pyinstaller --name bonk --onefile --windowed --add-data "assets:assets" src/dvd_screensaver/__main__.py
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

## License

[MIT License](../license.txt)
