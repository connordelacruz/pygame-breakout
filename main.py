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
BG_COLOR = Colors.BLACK
# Paddle -----------------------------------------------------------------------
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_STARTING_POS = ((WINDOW_WIDTH - PADDLE_WIDTH) / 2, WINDOW_HEIGHT - 40)
# TODO: parameterize (or remove and use mouse 1:1)
PADDLE_SPEED = 5
PADDLE_COLOR = Colors.LIGHT_BLUE
# Ball -------------------------------------------------------------------------
BALL_SIZE = 10
BALL_STARTING_POS = ((WINDOW_WIDTH - BALL_SIZE) / 2, PADDLE_STARTING_POS[1] - BALL_SIZE)
BALL_STARTING_DIRECTION = 200
BALL_SPEED = 6
BALL_COLOR = Colors.WHITE
# Bricks -----------------------------------------------------------------------
BRICK_ROWS = 5
BRICKS_PER_ROW = 8
BRICK_PADDING_X = 2
BRICK_PADDING_TOP = 5
BRICK_WIDTH = (WINDOW_WIDTH / BRICKS_PER_ROW) - 2 * BRICK_PADDING_X
BRICK_HEIGHT = 30
# Colors for each row, top to bottom
BRICK_ROW_COLORS = [
    Colors.RED,
    Colors.ORANGE,
    Colors.YELLOW,
    Colors.GREEN,
    Colors.BLUE,
]
# UI ---------------------------------------------------------------------------
UI_SCORE_POS = (20, 10)
UI_LIVES_POS = (650, 10)
UI_LINE_Y = 38
UI_LINE_STROKE = 2
UI_COLOR = Colors.WHITE
UI_FONT = pygame.font.Font(None, 34)
GAME_OVER_FONT = pygame.font.Font(None, 74)
# Playfield --------------------------------------------------------------------
# Set top of playfield to just below UI
PLAYFIELD_TOP_Y = UI_LINE_Y + UI_LINE_STROKE

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
paddle = Paddle(PADDLE_COLOR, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_STARTING_POS)
sprites.add(paddle)
# Ball
ball = Ball(BALL_COLOR, BALL_SIZE, BALL_STARTING_POS, BALL_STARTING_DIRECTION, BALL_SPEED,
            min_y=PLAYFIELD_TOP_Y)
sprites.add(ball)
# Bricks
bricks = pygame.sprite.Group()
for r in range(BRICK_ROWS):
    for b in range(BRICKS_PER_ROW):
        brick = Brick(BRICK_ROW_COLORS[r], BRICK_WIDTH, BRICK_HEIGHT)
        # x = b * (l_pad + r_pad + width) + l_pad
        brick_x = b * (2 * BRICK_PADDING_X + BRICK_WIDTH) + BRICK_PADDING_X
        # y = top_y + r * (t_pad + height) + t_pad
        brick_y = PLAYFIELD_TOP_Y + r * (BRICK_PADDING_TOP + BRICK_HEIGHT) + BRICK_PADDING_TOP
        brick.set_pos((brick_x, brick_y))
        bricks.add(brick)
sprites.add(bricks)

# Object to keep track of score
score_manager = ScoreManager(5)

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
    # Game Logic ---------------------------------------------------------------
    # TODO: once objects store props, try to use those instead of constants whenever possible (e.g. paddle.width)
    # Update ball position, determine if ball hit bottom
    lose_life = ball.update()
    if lose_life:
        score_manager.lose_life()
        # TODO: move ball to starting position after pause
    # Paddle/ball collision
    if pygame.sprite.collide_mask(ball, paddle):
        diff = paddle.rect.centerx - ball.rect.centerx
        ball.h_bounce(paddle.rect.y - ball.size - 1, diff)
    # Brick/ball collision
    for brick in pygame.sprite.spritecollide(ball, bricks, False):
        ball.handle_brick_collision(brick.rect)
        score_manager.add_points()
        brick.kill()
    if len(bricks) == 0:
        win_text = GAME_OVER_FONT.render("STAGE CLEAR", 1, UI_COLOR)
        # TODO: centering?
        screen.blit(win_text, (200, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        # TODO: reset game instead
        running = False

    # Drawing ------------------------------------------------------------------
    # Background
    screen.fill(BG_COLOR)
    # UI border and text
    pygame.draw.line(screen, UI_COLOR, [0, UI_LINE_Y], [WINDOW_WIDTH, UI_LINE_Y], UI_LINE_STROKE)
    score_text = UI_FONT.render(f'Score: {score_manager.score}', 1, UI_COLOR)
    lives_text = UI_FONT.render(f'Lives: {score_manager.lives}', 1, UI_COLOR)
    screen.blit(score_text, UI_SCORE_POS)
    screen.blit(lives_text, UI_LIVES_POS)
    # Draw sprites
    sprites.draw(screen)
    # Render screen
    pygame.display.flip()

    # Handle game over
    if score_manager.lives <= 0:
        # Show game over then exit
        game_over_text = GAME_OVER_FONT.render('GAME OVER', 1, UI_COLOR)
        # TODO positioning?
        screen.blit(game_over_text, (250, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        # TODO: reset game instead
        running = False

    # Ticks --------------------------------------------------------------------
    clock.tick(FPS)

pygame.quit()

