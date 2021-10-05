from random import randint
import pygame
from colors import Colors


# TODO extract common to class
class Ball(pygame.sprite.Sprite):
    """Ball object."""

    def __init__(self, color, width, height):
        super().__init__()

        # Keep track of screen borders for position calulations
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.min_x = 0
        self.max_x = self.screen_width - width
        self.min_y = 0
        self.max_y = self.screen_height - height

        # Randomize initial velocity
        # TODO: i think there's some odd behavior with randomness like this, play around with it
        self.velocity = [randint(4, 8), randint(-8, 8)]

        # Initialize self.image
        self.image = pygame.Surface([width, height])
        self.image.fill(Colors.BLACK)
        self.image.set_colorkey(Colors.BLACK)

        # Draw ball
        pygame.draw.rect(self.image, color, [0, 0, width, height])
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

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # Bounce off the walls
        if self.rect.x >= self.max_x or self.rect.x <= self.min_x:
            self.velocity[0] *= -1
        if self.rect.y >= self.max_y or self.rect.y <= self.min_y:
            self.velocity[1] *= -1

    def bounce(self):
        # Back it up TODO: necessary?
        self.rect.x -= self.velocity[0]
        self.rect.y -= self.velocity[1]
        # Flip y velocity n randomize x
        self.velocity[0] = randint(-8, 8)
        self.velocity[1] *= -1

