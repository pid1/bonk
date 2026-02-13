"""Bonk - Turning your PC into a 2004 DVD player on standby."""

from __future__ import annotations

import random
import sys
from importlib import resources
from pathlib import Path

import pygame

# Speed in pixels per second
SPEED = 150.0

# Hue rotation range (degrees) applied on each bounce
HUE_ROTATE_MIN = 120
HUE_ROTATE_MAX = 240

ASSET_DIR = Path(__file__).resolve().parent.parent.parent / "assets"


def load_logo(screen_w: int, screen_h: int) -> pygame.Surface:
    """Load the DVD logo and scale it to ~1/6 of the screen width."""
    logo_path = ASSET_DIR / "dvd_logo.png"
    if not logo_path.exists():
        # Fallback: check if bundled via importlib.resources
        ref = resources.files("dvd_screensaver") / "assets" / "dvd_logo.png"
        with resources.as_file(ref) as p:
            logo_path = p

    logo = pygame.image.load(str(logo_path)).convert_alpha()

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


def main() -> None:
    """Run the DVD screensaver."""
    # Handle Windows screensaver flags
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag.startswith("/c") or flag.startswith("/p"):
            print("Configuration menu and in-window preview are not implemented")
            sys.exit(0)

    pygame.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption("bonk")
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    # Load and color the logo
    logo_original = load_logo(screen_w, screen_h)
    logo = tint_surface(logo_original)
    logo_w, logo_h = logo.get_size()

    # Start centered
    x = float((screen_w - logo_w) // 2)
    y = float((screen_h - logo_h) // 2)
    vel_x = SPEED
    vel_y = SPEED

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

        # Update position
        x += vel_x * dt
        y += vel_y * dt

        # Bounce off edges
        bounced = False
        if x <= 0:
            x = 0
            vel_x = abs(vel_x)
            bounced = True
        elif x + logo_w >= screen_w:
            x = float(screen_w - logo_w)
            vel_x = -abs(vel_x)
            bounced = True

        if y <= 0:
            y = 0
            vel_y = abs(vel_y)
            bounced = True
        elif y + logo_h >= screen_h:
            y = float(screen_h - logo_h)
            vel_y = -abs(vel_y)
            bounced = True

        if bounced:
            logo = tint_surface(logo_original)

        # Draw
        screen.fill((0, 0, 0))
        screen.blit(logo, (int(x), int(y)))
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
