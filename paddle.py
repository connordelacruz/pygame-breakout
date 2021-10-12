import pygame
from colors import Colors


class Paddle(pygame.sprite.Sprite):
    """Paddle object"""

    def __init__(self, color, width, height):
        super().__init__()

        # Keep track of screen borders for position calulations
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.max_x = self.screen_width - width

        # Initialize self.image
        self.image = pygame.Surface([width, height])
        # Set transparency
        self.image.fill(Colors.BLACK)
        self.image.set_colorkey(Colors.BLACK)

        # Draw paddle
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def set_pos(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def move_left(self, amount):
        self.rect.x -= amount
        # Don't go past screen border
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, amount):
        self.rect.x += amount
        # Don't go past screen border
        if self.rect.x > self.max_x:
            self.rect.x = self.max_x

