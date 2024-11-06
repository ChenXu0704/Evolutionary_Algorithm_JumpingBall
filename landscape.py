"""Create landscape
"""
from obstacles import Obstacle
from obstacles import Obstacle
from constants import GRAVITY, TIME_INTERVAL
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from constants import BALL_COLOR, BALL_RADIUS, BALL_VELOCITY_X, BALL_VELOCITY_Y, BALL_X
from constants import OBSTACLE_GAP, OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_VELOCITY
def create_landscape(n):
    """
    Args:
        n (int): how many obstacles to be generated
    """
    return [Obstacle(BALL_X + OBSTACLE_GAP + OBSTACLE_GAP, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, -BALL_VELOCITY_X) for _ in range(n)]


def reset_obstacles(landscape, id):
    """
    Args:
        landscape (list): a list of obstacles
        id (int): reset the x position of obstacles with range[0, id]
    """
    for i in range(id + 1):
        landscape[i].x = BALL_X + OBSTACLE_GAP