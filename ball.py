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
        # Keep track of screen borders for position calculations
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
        pygame.draw.circle(self.image, color, (size / 2, size / 2), size / 2)
        self.rect = self.image.get_rect()
        self.set_pos(starting_pos)

    def set_pos(self, coords):
        # TODO: set center instead (for all x/y assignments)
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def set_direction(self, new_direction):
        """Set direction angle.

        If new_direction is close to a horizontal angle, it will be tweaked
        to avoid soft locking the game.

        :param new_direction: The new direction of the ball
        """
        # TODO: move % 360 here
        # If the angle would cause a horizontal (or near-horizontal) angle,
        # adjust the new direction to be angled slightly upwards
        if 80 <= new_direction <= 100:
            new_direction -= 30
        elif 260 <= new_direction <= 280:
            new_direction += 30
        self.direction = new_direction

    def h_bounce(self, target_y, diff=0):
        """Bounce off horizontal surface.

        :param target_y: New Y-coordinate to set for ball. Should be 1px
            above/below the object we're bouncing off of
        :param diff: (Default: 0) center of paddle - center of ball. Angle will
            be adjusted based on how far to the left or right of the paddle
            ball hits
        """
        self.set_direction(((180 - self.direction - diff) % 360))
        self.rect.y = target_y

    def v_bounce(self, target_x):
        """Bounce off vertical surface.

        :param target_x: New X-coordinate to set for ball. Should be 1px
            left/right of the object we're bouncing off of
        """
        self.set_direction((360 - self.direction) % 360)
        self.rect.x = target_x

    def handle_brick_collision(self, brick_rect):
        """Bounce the ball based on which side of a brick we've collided with.

        Based on edge calculations from this sketch:
        https://openprocessing.org/sketch/533102/

        :param brick_rect: The Rect object of the brick we've collided with
        """
        # Figure out which edge we've collided with
        is_horizontal_edge = True
        bounce_side_coords = self.rect.y
        if self.rect.centerx <= brick_rect.left:
            is_horizontal_edge = False
            bounce_side_coords = brick_rect.left
        elif self.rect.centerx >= brick_rect.right:
            is_horizontal_edge = False
            bounce_side_coords = brick_rect.right
        if self.rect.centery <= brick_rect.top:
            is_horizontal_edge = True
            bounce_side_coords = brick_rect.top
        elif self.rect.centery >= brick_rect.bottom:
            is_horizontal_edge = True
            bounce_side_coords = brick_rect.bottom
        bounce_method = self.h_bounce if is_horizontal_edge else self.v_bounce
        bounce_method(bounce_side_coords)

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

