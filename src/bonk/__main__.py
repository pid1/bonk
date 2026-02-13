"""Bonk - Turning your PC into a 2004 DVD player on standby."""

from __future__ import annotations

import ctypes
import os
import random
import sys
from pathlib import Path

import pygame

# Speed in pixels per second
SPEED = 150.0

# Hue rotation range (degrees) applied on each bounce
HUE_ROTATE_MIN = 120
HUE_ROTATE_MAX = 240

# When bundled by PyInstaller, assets live under sys._MEIPASS
if getattr(sys, "frozen", False):
    ASSET_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSET_DIR = Path(__file__).resolve().parent.parent.parent / "assets"


def load_logo(screen_w: int, screen_h: int) -> pygame.Surface:
    """Load the DVD logo and scale it to ~1/6 of the screen width."""
    logo_path = ASSET_DIR / "dvd_logo.png"

    logo = pygame.image.load(str(logo_path)).convert_alpha()

    # Convert to white preserving alpha so the multiply-blend tint works on any source color
    logo.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)

    target_w = screen_w // 6
    scale = target_w / logo.get_width()
    target_h = int(logo.get_height() * scale)

    return pygame.transform.smoothscale(logo, (target_w, target_h))


def hue_rotate_surface(surface: pygame.Surface) -> pygame.Surface:
    """Apply a random hue rotation to a surface by shifting pixel colors in HSV space."""
    rotation = random.randint(HUE_ROTATE_MIN, HUE_ROTATE_MAX)
    width, height = surface.get_size()
    rotated = surface.copy()

    for x in range(width):
        for y in range(height):
            r, g, b, a = surface.get_at((x, y))
            if a == 0:
                continue
            color = pygame.Color(r, g, b, a)
            h, s, lightness, ca = color.hsla
            color.hsla = ((h + rotation) % 360, s, lightness, ca)
            rotated.set_at((x, y), color)

    return rotated


def tint_surface(surface: pygame.Surface) -> pygame.Surface:
    """Fast hue-shift by tinting with a random bright color. Much faster than per-pixel HSV."""
    hue = random.randint(HUE_ROTATE_MIN, HUE_ROTATE_MAX)
    tint_color = pygame.Color(0)
    tint_color.hsla = (hue, 100, 50, 100)

    tinted = surface.copy()
    tint_overlay = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
    tint_overlay.fill((tint_color.r, tint_color.g, tint_color.b, 255))

    # Multiply blend: keeps the shape from alpha, shifts color
    tinted.blit(tint_overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
    return tinted


def _get_monitors_win32(offset_x: int, offset_y: int) -> list[tuple[int, int, int, int]]:
    """Return monitor rects as (x, y, w, h) in window-relative coordinates."""
    from ctypes import wintypes

    monitors: list[tuple[int, int, int, int]] = []

    def callback(hmon, hdc, lprect, lparam):
        r = lprect.contents
        monitors.append((
            r.left - offset_x,
            r.top - offset_y,
            r.right - r.left,
            r.bottom - r.top,
        ))
        return True

    proc = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
        ctypes.POINTER(wintypes.RECT), wintypes.LPARAM,
    )(callback)
    ctypes.windll.user32.EnumDisplayMonitors(None, None, proc, 0)
    return monitors


def main() -> None:
    """Run the DVD screensaver."""
    # Handle Windows screensaver flags
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag.startswith("/c") or flag.startswith("/p"):
            print("Configuration menu and in-window preview are not implemented")
            sys.exit(0)

    # Enable per-monitor DPI awareness on Windows so we get real pixel dimensions
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
        except (AttributeError, OSError):
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows

    pygame.init()

    if sys.platform == "win32":
        user32 = ctypes.windll.user32
        # Primary monitor width (for logo scaling)
        primary_w = user32.GetSystemMetrics(0)  # SM_CXSCREEN
        # Virtual screen spans all monitors
        virt_x = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
        virt_y = user32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN
        screen_w = user32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
        screen_h = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN

        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{virt_x},{virt_y}"
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.NOFRAME)

        # Place window above taskbar
        hwnd = pygame.display.get_wm_info()["window"]
        user32.SetWindowPos(hwnd, -1, virt_x, virt_y, screen_w, screen_h, 0x0040)

        # Per-monitor rects in window-relative coordinates
        monitor_rects = _get_monitors_win32(virt_x, virt_y)
    else:
        info = pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        primary_w = screen_w
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
        monitor_rects = [(0, 0, screen_w, screen_h)]

    pygame.display.set_caption("bonk")
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    # Load logo scaled relative to primary monitor
    logo_original = load_logo(primary_w, screen_h)
    logo_w, logo_h = logo_original.get_size()

    # Create an independent bouncing instance for each monitor
    instances = []
    for mx, my, mw, mh in monitor_rects:
        instances.append({
            "mx": mx, "my": my, "mw": mw, "mh": mh,
            "x": float(mx + (mw - logo_w) // 2),
            "y": float(my + (mh - logo_h) // 2),
            "vel_x": SPEED * random.choice([-1, 1]),
            "vel_y": SPEED * random.choice([-1, 1]),
            "logo": tint_surface(logo_original),
        })

    # Track initial mouse position for screensaver-style quit behavior
    initial_mouse_pos: tuple[int, int] | None = None
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL):
                # Grace period to avoid quitting from initial input events
                if pygame.time.get_ticks() - start_ticks > 100:
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                if pygame.time.get_ticks() - start_ticks > 100:
                    if initial_mouse_pos is None:
                        initial_mouse_pos = event.pos
                    elif event.pos != initial_mouse_pos:
                        running = False

        screen.fill((0, 0, 0))

        for inst in instances:
            # Update position
            inst["x"] += inst["vel_x"] * dt
            inst["y"] += inst["vel_y"] * dt

            # Bounce within this monitor's bounds
            bounced = False
            if inst["x"] <= inst["mx"]:
                inst["x"] = float(inst["mx"])
                inst["vel_x"] = abs(inst["vel_x"])
                bounced = True
            elif inst["x"] + logo_w >= inst["mx"] + inst["mw"]:
                inst["x"] = float(inst["mx"] + inst["mw"] - logo_w)
                inst["vel_x"] = -abs(inst["vel_x"])
                bounced = True

            if inst["y"] <= inst["my"]:
                inst["y"] = float(inst["my"])
                inst["vel_y"] = abs(inst["vel_y"])
                bounced = True
            elif inst["y"] + logo_h >= inst["my"] + inst["mh"]:
                inst["y"] = float(inst["my"] + inst["mh"] - logo_h)
                inst["vel_y"] = -abs(inst["vel_y"])
                bounced = True

            if bounced:
                inst["logo"] = tint_surface(logo_original)

            screen.blit(inst["logo"], (int(inst["x"]), int(inst["y"])))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
