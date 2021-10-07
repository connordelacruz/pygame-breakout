import math
from random import randint
import pygame
from colors import Colors


class Ball(pygame.sprite.Sprite):
    """Ball object."""

    # TODO take min/max x/y, starting position here
    def __init__(self, color, size):
        super().__init__()

        # Keep track of screen borders for position calulations
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.min_x = 0
        self.max_x = self.screen_width - size
        self.min_y = 0
        self.max_y = self.screen_height - size

        # TODO: parameterize
        # Speed and direction
        self.speed = 8
        self.direction = 200

        # Initialize self.image
        self.image = pygame.Surface([size, size])
        self.image.fill(Colors.BLACK)
        self.image.set_colorkey(Colors.BLACK)

        # Draw ball
        pygame.draw.rect(self.image, color, [0, 0, size, size])
        self.rect = self.image.get_rect()

    def set_pos(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def set_playfield_limits(self, min_x=None, max_x=None, min_y=None, max_y=None):
        # TODO: doc, rename?
        if min_x is not None:
            self.min_x = min_x
        if max_x is not None:
            self.max_x = max_x
        if min_y is not None:
            self.min_y = min_y
        if max_y is not None:
            self.max_y = max_y

    def h_bounce(self, target_y, diff=0):
        """Bounce off horizontal surface"""
        # TODO doc params
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
        # TODO: self.rect.y = target_y

    def v_bounce(self, target_x):
        """Bounce off vertical surface"""
        # TODO doc params
        self.direction = (360 - self.direction) % 360
        # TODO: self.rect.x = target_x

    def update(self):
        """Returns True if we hit the bottom"""
        hit_bottom = False
        rad = math.radians(self.direction)
        # Calculate new position
        self.rect.x += self.speed * math.sin(rad)
        self.rect.y -= self.speed * math.cos(rad)
        # Bounce off the walls
        if self.rect.x >= self.max_x:
            self.v_bounce(self.max_x - 1)
        if self.rect.x <= self.min_x:
            self.v_bounce(self.min_x + 1)
        if self.rect.y >= self.max_y:
            self.h_bounce(self.max_y - 1)
            hit_bottom = True
        if self.rect.y <= self.min_y:
            self.h_bounce(self.min_y + 1)
        return hit_bottom

