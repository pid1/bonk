{ pkgs, lib, config, inputs, ... }:

let
  setupCommands = [
    "install-deps"
  ];
in
{
  # Packages
  packages = with pkgs; [
    uv
    ruff
    git
  ];

  # Python 3.14
  languages.python = {
    enable = true;
    package = pkgs.python314;
    uv.enable = true;
  };

  # Scripts
  scripts = {
    # Setup
    setup.exec = lib.concatStringsSep " && " setupCommands;

    # Interactive dev
    dev.exec = "uv run bonk";

    # Background dev
    dev-start.exec = ''
      mkdir -p .devenv/logs .devenv/pids
      nohup uv run bonk > .devenv/logs/dev.log 2>&1 &
      echo $! > .devenv/pids/dev.pid
      echo "✓ Screensaver started in background (PID: $!)"
      echo "  Logs: .devenv/logs/dev.log"
      echo "  Stop: dev-stop"
    '';
    dev-stop.exec = ''
      if [ -f .devenv/pids/dev.pid ]; then
        pid=$(cat .devenv/pids/dev.pid)
        if kill -0 $pid 2>/dev/null; then
          kill $pid && echo "✓ Stopped screensaver (PID: $pid)"
        else
          echo "Screensaver not running"
        fi
        rm -f .devenv/pids/dev.pid
      else
        echo "No PID file found"
      fi
    '';
    dev-status.exec = ''
      echo "=== Dev Process Status ==="
      for name in dev; do
        pidfile=".devenv/pids/$name.pid"
        if [ -f "$pidfile" ]; then
          pid=$(cat "$pidfile")
          if kill -0 $pid 2>/dev/null; then
            echo "$name: Running (PID: $pid)"
          else
            echo "$name: Stopped (stale PID file)"
          fi
        else
          echo "$name: Not started"
        fi
      done
    '';
    dev-logs.exec = "tail -50 .devenv/logs/dev.log 2>/dev/null || echo 'No dev logs found'";

    # Quality
    lint.exec = "ruff check .";
    lint-fix.exec = "ruff check . --fix";
    format.exec = "ruff format .";
    test.exec = "uv run pytest";
    install-deps.exec = "uv sync";

    # Build
    build.exec = ''
      uv sync --extra build
      uv run pyinstaller \
        --name bonk \
        --onefile \
        --windowed \
        --add-data "assets:assets" \
        src/dvd_screensaver/__main__.py
      echo "✓ Built: dist/bonk"
    '';
  };

  enterShell = ''
    echo "📀 Bonk — DVD Screensaver Development Environment"
    echo ""
    echo "Python: $(python --version)"
    echo "uv: $(uv --version)"
    echo ""
    echo "Setup:"
    echo "  setup            - Initialize repo (runs: ${lib.concatStringsSep ", " setupCommands})"
    echo ""
    echo "Interactive commands (block until killed):"
    echo "  dev              - Launch screensaver fullscreen"
    echo ""
    echo "Background commands (for agents/scripts):"
    echo "  dev-start        - Start in background"
    echo "  dev-stop         - Stop background processes"
    echo "  dev-status       - Check process status"
    echo "  dev-logs         - View recent logs"
    echo ""
    echo "Quality commands:"
    echo "  lint             - Run ruff linter"
    echo "  lint-fix         - Run ruff with auto-fix"
    echo "  format           - Run ruff formatter"
    echo "  test             - Run pytest"
    echo ""
    echo "Build commands:"
    echo "  build            - Build standalone executable with PyInstaller"
    echo ""
    echo "Other commands:"
    echo "  install-deps     - Install dependencies with uv"
    echo ""
  '';
}
