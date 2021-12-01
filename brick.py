import pygame
from colors import Colors


class Brick(pygame.sprite.Sprite):
    """Brick object."""

    def __init__(self, color, width, height, starting_pos):
        super().__init__()
        # Initialize self.image
        self.image = pygame.Surface([width, height])
        self.image.fill(Colors.BLACK)
        self.image.set_colorkey(Colors.BLACK)
        # Initialize rect
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.set_pos(starting_pos)

    def set_pos(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]
