import pygame
from colors import Colors


class Paddle(pygame.sprite.Sprite):
    """Paddle object"""
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        # TODO: this sets transparency, but if we're not using image files then do we need it?
        self.image.fill(Colors.BLACK)
        self.image.set_colorkey(Colors.BLACK)
        # Draw paddle
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

