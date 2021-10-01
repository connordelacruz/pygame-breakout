#!/usr/bin/env python3
import pygame
pygame.init()
from colors import Colors
from paddle import Paddle


# CONSTANTS ====================================================================
# Derived Colors ---------------------------------------------------------------
C_BG = Colors.DARK_BLUE
C_PADDLE = Colors.LIGHT_BLUE
C_BALL = Colors.WHITE
# Brick colors, from top row to bottom
BRICK_ROW_COLORS = [
    Colors.RED,
    Colors.ORANGE,
    Colors.YELLOW,
]
# UI
C_UI = Colors.WHITE

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

# Sprites ----------------------------------------------------------------------
# Global sprites list
sprites = pygame.sprite.Group()


# PYGAME SETUP =================================================================

# Window -----------------------------------------------------------------------
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Breakout')

# Clock ------------------------------------------------------------------------
clock = pygame.time.Clock()

# Game Objects -----------------------------------------------------------------
# Paddle
paddle = Paddle(C_PADDLE, 100, 10)
# TODO: create Paddle.set_pos()
paddle.rect.x = 350
paddle.rect.y = 560
sprites.add(paddle)


# MAIN LOOP ====================================================================
running = True
while running:
    # Event Loop ---------------------------------------------------------------
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False

    # Game Logic ---------------------------------------------------------------
    sprites.update()

    # Drawing ------------------------------------------------------------------
    # Background
    screen.fill(C_BG)
    # UI border and text
    pygame.draw.line(screen, C_UI, [0, 38], [800, 38], 2)
    score_text = ui_font.render(f'Score: {score}', 1, C_UI)
    lives_text = ui_font.render(f'Lives: {lives}', 1, C_UI)
    screen.blit(score_text, POS_SCORE)
    screen.blit(lives_text, POS_LIVES)
    # Draw sprites
    sprites.draw(screen)
    # Render screen
    pygame.display.flip()

    # Ticks --------------------------------------------------------------------
    clock.tick(FPS)

# End Loop ---------------------------------------------------------------------
pygame.quit()


