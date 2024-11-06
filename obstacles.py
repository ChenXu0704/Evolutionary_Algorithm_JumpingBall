"""Obstacle Object
"""
from constants import TIME_INTERVAL
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, OBSTACLE_COLOR, OBSTACLE_HEIGHT
import random
import pygame

class Obstacle:
    """Create Obstacle object
    """
    def __init__(self, x, width, height, speed):
        """Initialize the Ball

        Args:
            x (int): location of the obstacle at x axis
            y (int): location of the obstacle at y axis
            width (int): the width of the obstacle
            height (int): the height of the obstacle
            speed (int): the moving speed of the obstacle
        """
        self.x = x
        self.width = width
        self.height = random.randint(10, OBSTACLE_HEIGHT)
        self.y = SCREEN_HEIGHT - self.height
        self.speed = speed

    def draw(self, screen):
        """Draw Obstacle as rectangular on Surface

        Args:
            screen (pygame.Surface): the screen to display the game
        """
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height))

    def update(self):
        """Update locations of the obstacle when the obstacle moves out of the screen
        """
        if self.x + self.width < 0:
            self.x = SCREEN_WIDTH - self.width
            self.height = random.randint(10, OBSTACLE_HEIGHT)
            self.y = SCREEN_HEIGHT - self.height
    
    def move(self):
        """Move the obstacle
        """
        self.x += (self.speed * TIME_INTERVAL)