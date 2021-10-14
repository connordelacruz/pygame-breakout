import math
from random import randint
import pygame
from colors import Colors


class Ball(pygame.sprite.Sprite):
    """Ball object."""

    def __init__(self, color, size, starting_pos, starting_direction, speed,
                 min_x=0, max_x=None, min_y=0, max_y=None):
        super().__init__()
        self.color = color
        self.size = size
        self.starting_pos = starting_pos
        self.direction = starting_direction
        self.speed = speed
        # Keep track of screen borders for position calulations
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.min_x = min_x
        self.max_x = max_x or self.screen_width - size
        self.min_y = min_y
        self.max_y = max_y or self.screen_height - size
        # Initialize self.image
        self.image = pygame.Surface([size, size])
        self.image.fill(Colors.BLACK)
        self.image.set_colorkey(Colors.BLACK)
        # Initialize rect
        pygame.draw.rect(self.image, color, [0, 0, size, size])
        self.rect = self.image.get_rect()
        self.set_pos(starting_pos)

    def set_pos(self, coords):
        # TODO: set center instead?
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def h_bounce(self, target_y, diff=0):
        """Bounce off horizontal surface.

        :param target_y: New Y-coordinate to set for ball. Should be 1px
            above/below the object we're bouncing off of
        :param diff: (Default: 0) center of paddle - center of ball. Angle will
            be adjusted based on how far to the left or right of the paddle
            ball hits
        """
        # TODO: don't allow for horizontal lines
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
        self.rect.y = target_y

    def v_bounce(self, target_x):
        """Bounce off vertical surface.

        :param target_x: New X-coordinate to set for ball. Should be 1px
            left/right of the object we're bouncing off of
        """
        # TODO: don't allow for horizontal lines
        self.direction = (360 - self.direction) % 360
        self.rect.x = target_x

    def update(self):
        """Update ball position and direction.

        :return: True if ball hit the bottom
        """
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

