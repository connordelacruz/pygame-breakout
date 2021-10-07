#!/usr/bin/env python3
import pygame
pygame.init()
from colors import Colors
from paddle import Paddle
from ball import Ball
from brick import Brick
from score_manager import ScoreManager


# GLOBALS AND CONSTANTS ========================================================
# Window and Rendering ---------------------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
C_BG = Colors.DARK_BLUE
# Paddle -----------------------------------------------------------------------
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
POS_PADDLE_START = ((WINDOW_WIDTH - PADDLE_WIDTH) / 2, WINDOW_HEIGHT - 40)
PADDLE_SPEED = 5
C_PADDLE = Colors.LIGHT_BLUE
# Ball -------------------------------------------------------------------------
C_BALL = Colors.WHITE
# Bricks -----------------------------------------------------------------------
C_BRICK_TOP = Colors.RED
C_BRICK_MID = Colors.ORANGE
C_BRICK_BOT = Colors.YELLOW
# UI ---------------------------------------------------------------------------
POS_SCORE = (20, 10)
POS_LIVES = (650, 10)
UI_LINE_Y = 38
UI_LINE_STROKE = 2
C_UI = Colors.WHITE
ui_font = pygame.font.Font(None, 34)
game_over_font = pygame.font.Font(None, 74)


# PYGAME SETUP =================================================================
# Window -----------------------------------------------------------------------
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Breakout')
# Clock ------------------------------------------------------------------------
clock = pygame.time.Clock()
# Game Objects -----------------------------------------------------------------
# Global sprites list
sprites = pygame.sprite.Group()
# Paddle
paddle = Paddle(C_PADDLE, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle.set_pos(POS_PADDLE_START)
sprites.add(paddle)
# Ball
# TODO constants
ball = Ball(Colors.WHITE, 10, 10)
ball.set_pos((345, 560))
# So ball doesn't pass thru UI
ball.set_playfield_limits(min_y=UI_LINE_Y + UI_LINE_STROKE)
sprites.add(ball)
# Bricks
bricks = pygame.sprite.Group()
# TODO constants
for i in range(7):
    brick = Brick(C_BRICK_TOP, 80, 30)
    brick.set_pos((60 + i * 100, 60))
    bricks.add(brick)
for i in range(7):
    brick = Brick(C_BRICK_MID, 80, 30)
    brick.set_pos((60 + i * 100, 100))
    bricks.add(brick)
for i in range(7):
    brick = Brick(C_BRICK_BOT, 80, 30)
    brick.set_pos((60 + i * 100, 140))
    bricks.add(brick)
sprites.add(bricks)

# Object to keep track of score
score_manager = ScoreManager(3)


# MAIN LOOP ====================================================================
running = True
while running:
    # Event Loop ---------------------------------------------------------------
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False

    # Input Handlers -----------------------------------------------------------
    keys = pygame.key.get_pressed()
    # Quit on ESC
    if keys[pygame.K_ESCAPE]:
        running = False
    # Paddle controls
    if keys[pygame.K_LEFT]:
        paddle.move_left(PADDLE_SPEED)
    if keys[pygame.K_RIGHT]:
        paddle.move_right(PADDLE_SPEED)
    # TODO DEBUG
    if keys[pygame.K_b]:
        bricks.empty()

    # Game Logic ---------------------------------------------------------------
    # Update ball position, determine if ball hit bottom
    lose_life = ball.update()
    if lose_life:
        score_manager.lose_life()
        # TODO: move ball to starting position after pause
    # Paddle/ball collision
    if pygame.sprite.collide_mask(ball, paddle):
        ball.bounce()
    # Brick/ball collision
    for brick in pygame.sprite.spritecollide(ball, bricks, False):
        ball.bounce()
        score_manager.add_points()
        brick.kill()
    if len(bricks) == 0:
        win_text = game_over_font.render("STAGE CLEAR", 1, C_UI)
        # TODO: centering?
        screen.blit(win_text, (200, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        # TODO: reset game instead
        running = False

    # Drawing ------------------------------------------------------------------
    # Background
    screen.fill(C_BG)
    # UI border and text
    # TODO move to sprite class?
    pygame.draw.line(screen, C_UI, [0, UI_LINE_Y], [WINDOW_WIDTH, UI_LINE_Y], UI_LINE_STROKE)
    score_text = ui_font.render(f'Score: {score_manager.score}', 1, C_UI)
    lives_text = ui_font.render(f'Lives: {score_manager.lives}', 1, C_UI)
    screen.blit(score_text, POS_SCORE)
    screen.blit(lives_text, POS_LIVES)
    # Draw sprites
    sprites.draw(screen)
    # Render screen
    pygame.display.flip()

    # Handle game over
    if score_manager.lives <= 0:
        # Show game over then exit
        game_over_text = game_over_font.render('GAME OVER', 1, C_UI)
        # TODO positioning?
        screen.blit(game_over_text, (250, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        # TODO: reset game instead
        running = False

    # Ticks --------------------------------------------------------------------
    clock.tick(FPS)

# End Loop ---------------------------------------------------------------------
pygame.quit()


