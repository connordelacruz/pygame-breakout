import math
from random import randint
import pygame
from colors import Colors


class Ball(pygame.sprite.Sprite):
    """Ball object."""

    # TODO take min/max x/y, starting position here
    def __init__(self, color, size, starting_pos,
                 min_x=0, max_x=None, min_y=0, max_y=None):
        super().__init__()
        self.color = color
        self.size = size
        self.starting_pos = starting_pos

        # Keep track of screen borders for position calulations
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.min_x = min_x
        self.max_x = self.screen_width - size if max_x is None else max_x
        self.min_y = min_y
        self.max_y = self.screen_height - size if max_y is None else max_y

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
        # TODO: set center instead?
        self.rect.x = starting_pos[0]
        self.rect.y = starting_pos[1]

    def set_pos(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def h_bounce(self, target_y, diff=0):
        """Bounce off horizontal surface"""
        # TODO doc params
        # TODO: don't allow for horizontal lines
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
        self.rect.y = target_y

    def v_bounce(self, target_x):
        """Bounce off vertical surface"""
        # TODO doc params
        # TODO: don't allow for horizontal lines
        self.direction = (360 - self.direction) % 360
        self.rect.x = target_x

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

