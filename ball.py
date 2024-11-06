"""Create ball class
"""
from constants import BALL_COLOR, BALL_RADIUS, BALL_VELOCITY_X, BALL_VELOCITY_Y, BALL_X
import pygame


class Ball:
    """Create Ball object
    """
    def __init__(self, x, y, radius):
        """Initialize the Ball

        Args:
            x (int): location of the ball at x axis
            y (int): location of the ball at y axis
            radius (int): the radius of the ball
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = BALL_VELOCITY_X
        self.speed_y = BALL_VELOCITY_Y

    def draw(self, screen):
        """Draw the ball as a circle on Surface

        Args:
            screen (pygame.Surface): the screen to display the game
        """
        pygame.draw.circle(screen, BALL_COLOR, (self.x, self.y), self.radius)