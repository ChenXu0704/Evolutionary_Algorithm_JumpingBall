"""Visualization
"""

import pygame, sys
import math
import numpy as np

from ball import Ball
from nn import Agent
from obstacles import Obstacle
from constants import GRAVITY, TIME_INTERVAL
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from constants import BALL_COLOR, BALL_RADIUS, BALL_VELOCITY_X, BALL_VELOCITY_Y, BALL_X
from constants import OBSTACLE_GAP, OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_VELOCITY
from log import logging


def is_collision(ball, obstacle):
    """Define the condition when the ball and the obstacle have collisions

    Args:
        ball (Object Ball): A moving ball
        obstacle (Object Obstacle): A moving obstacle
    Returns:
        True if the ball hits the obstacle
        False otherwise
    """

    if ball.x >= obstacle.x - ball.radius and ball.x < obstacle.x:
        if ball.y - obstacle.y >= 0:
            logging.debug("collision condition 1 triggered......")
            return True
        else:
            if math.sqrt(math.pow(ball.x - obstacle.x, 2) + math.pow(ball.y - obstacle.y, 2)) <= ball.radius:
                logging.debug("collision condition 2 triggered......")
                return True
    elif ball.x > obstacle.x and ball.x < obstacle.x + obstacle.width:
        if (obstacle.y - ball.y <= ball.radius):
            logging.debug("collision condition 3 triggered......")
            return True
    elif ball.x >= obstacle.x + obstacle.width and ball.x < obstacle.x + obstacle.width + ball.radius:
        if math.sqrt(math.pow(ball.x - (obstacle.x + obstacle.width), 2) + math.pow(ball.y - obstacle.y, 2)) <= ball.radius:
            logging.debug("collision condition 4 triggered......")
            return True
        
    return False


## Controll the ball's movement in NN
def ball_control(ball, obstacles, agent, vx_min = 20, vx_max = 50, vy_max = 80):
    """Control the movement of the ball

    Args:
        ball (Object Ball): Moving the ball in the x and y directions
        obstacles (List<Object Obstacle>): A record of upcoming obstacles that the ball will face in a sorted order
        agent (Object Agent): Neural Network agent to initialize the ball's velocities
    """
    
    #ball.x += (ball.speed_x * TIME_INTERVAL)
    ball.y = min(SCREEN_HEIGHT - ball.radius, ball.y + ball.speed_y * TIME_INTERVAL + 0.5 * GRAVITY * TIME_INTERVAL * TIME_INTERVAL)

    if ball.y < SCREEN_HEIGHT - ball.radius:
        ball.speed_y += (GRAVITY * TIME_INTERVAL)
    else:
        features = []
        features.append((obstacles[0].height - 0.5 * OBSTACLE_HEIGHT) / OBSTACLE_HEIGHT)
        features.append(((obstacles[0].x - ball.x) - 0.5 * OBSTACLE_GAP ) / OBSTACLE_GAP)
        #features.append((-obstacles[0].speed - (vx_max + vx_min) / 2) / (vx_max - vx_min) * 2)
        features.append((-obstacles[0].speed - vx_min) / (vx_max - vx_min) * 2)
        features.append((ball.speed_y - vy_max / 2) / vy_max * 2)
        features.append(1)
        delta_v = agent.prediction(np.array(features))
        ball.speed_y = - delta_v[1] * vy_max / 100
        ball.speed_x = delta_v[0] * (vx_max - vx_min) / 100 + vx_min

def main():
    # Initialize Pygame
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create the ball and obstacle and player
    ball = Ball(BALL_X, SCREEN_HEIGHT - BALL_RADIUS, BALL_RADIUS)
    obstacle1 = Obstacle(SCREEN_WIDTH, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, -ball.speed_x)
    obstacle2 = Obstacle(obstacle1.x-obstacle1.width-OBSTACLE_GAP, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, -ball.speed_x)
    agent = Agent(5, 8, 2)
    obstacles = [obstacle2, obstacle1]
    # Start the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Move the ball
        ball_control(ball, obstacles, agent)
        obstacle1.speed = -ball.speed_x
        obstacle2.speed = -ball.speed_x
        # Move the obstacles
        obstacle1.move()
        obstacle2.move()
        # If obstacle goes out of screen, reset its position
        obstacle1.update()
        obstacle2.update()
        if obstacles[0].x + OBSTACLE_WIDTH <= ball.x - ball.radius:
            tmp = obstacles[0]
            obstacles[0] = obstacles[1]
            obstacles[1] = tmp
        
        # Draw the screen
        screen.fill((0, 0, 0))
        obstacle1.draw(screen)
        obstacle2.draw(screen)
        ball.draw(screen)
        pygame.display.update()
        # Check for collision with obstacle
        if is_collision(ball, obstacle1):
            break
        if is_collision(ball, obstacle2):
            break

if __name__ == '__main__':
    main()