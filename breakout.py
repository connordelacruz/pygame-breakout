#!/usr/bin/env python3
import pygame
pygame.init()

# CONSTANTS ====================================================================
# Color Palette ----------------------------------------------------------------
C_WHITE = '#ffffff'
C_DARK_BLUE = '#1c77c3'
C_LIGHT_BLUE = '#40bcd8'
C_YELLOW = '#f6ee51'
C_ORANGE = '#f39237'
C_RED = '#d63230'

# Derived Colors ---------------------------------------------------------------
C_BG = C_DARK_BLUE
C_PADDLE = C_LIGHT_BLUE
C_BALL = C_WHITE
# Brick colors, from top row to bottom
BRICK_ROW_COLORS = [
    C_RED,
    C_ORANGE,
    C_YELLOW,
]
# UI
C_UI = C_WHITE

# Coordinates ------------------------------------------------------------------
POS_SCORE = (20, 10)
POS_LIVES = (650, 10)

# Misc -------------------------------------------------------------------------
FPS = 60

# GLOBALS ======================================================================
# Game Stats -------------------------------------------------------------------
score = 0
lives = 3

# UI ---------------------------------------------------------------------------
ui_font = pygame.font.Font(None, 34)

# PYGAME SETUP =================================================================

# Window -----------------------------------------------------------------------
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Breakout')

# Clock ------------------------------------------------------------------------
clock = pygame.time.Clock()

# MAIN LOOP ====================================================================
running = True
while running:
    # Event Loop ---------------------------------------------------------------
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False

    # Game Logic ---------------------------------------------------------------

    # Drawing ------------------------------------------------------------------
    # Background
    screen.fill(C_BG)
    # UI
    pygame.draw.line(screen, C_UI, [0, 38], [800, 38], 2)
    score_text = ui_font.render(f'Score: {score}', 1, C_UI)
    lives_text = ui_font.render(f'Lives: {lives}', 1, C_UI)
    screen.blit(score_text, POS_SCORE)
    screen.blit(lives_text, POS_LIVES)
    # Render screen
    pygame.display.flip()

    # Ticks --------------------------------------------------------------------
    clock.tick(FPS)

# End Loop ---------------------------------------------------------------------
pygame.quit()


