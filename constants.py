# Define some constants
GRAVITY = 10
TIME_INTERVAL = 0.02

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
BALL_X = 100
BALL_VELOCITY_X = 30
BALL_VELOCITY_Y = 5

OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 150
OBSTACLE_COLOR = (0, 255, 0)
OBSTACLE_VELOCITY = 5
OBSTACLE_GAP = 200

NUMBER_OF_RUNNING = 20
HYPER_PARAMS1 = {"hidden_layer_nodes": [8],
    "input_nodes": [5],
    "mut_rate": [0.5],
    "mutation_sigma": [1],
    "mutation_type": ['onestep'],
    "xover_rate": [0.5],
    "xover_exchange_rate": [0.2],
    "xover_type": ['sample'],
    "fitness_mode": ['median'],
    "popsize": [40],
    "tournament_size": [4],
    "parent_selection_type": ["topK"],
    "survival_selection_type": ["mu_plus_lambda"],
    "epoch": [40],
    "obstacle_number": [120],
    "landscape_size": [150],
    "vx_min": [5, 10, 15],
    "vx_max": [20, 30, 40],
    "vy_max": [70, 80, 90]}
HYPER_PARAMS2 = {"hidden_layer_nodes": [8],
    "input_nodes": [5],
    "mut_rate": [0.1, 0.5, 0.8],
    "mutation_sigma": [1, 3],
    "mutation_type": ['onestep', 'nstep'],
    "xover_rate": [0.5],
    "xover_exchange_rate": [0.2],
    "xover_type": ['sample'],
    "fitness_mode": ['median','mean'],
    "popsize": [40],
    "tournament_size": [4],
    "parent_selection_type": ["topK", "MPS", "tournament"],
    "survival_selection_type": ["replacement", "mu_plus_lambda"],
    "epoch": [60],
    "obstacle_number": [120],
    "landscape_size": [150],
    "vx_min": [10],
    "vx_max": [20],
    "vy_max": [90]}
    
HYPER_PARAMS = {"hidden_layer_nodes": [8],
    "input_nodes": [5],
    "mut_rate": [0.1, 0.5],
    "mutation_sigma": [1],
    "mutation_type": ['onestep', 'nstep'],
    "xover_rate": [0],
    "xover_exchange_rate": [0.2],
    "xover_type": ['sample'],
    "fitness_mode": ['median','mean'],
    "popsize": [40],
    "tournament_size": [4],
    "parent_selection_type": ["topK", "MPS"],
    "survival_selection_type": ["replacement", "mu_plus_lambda"],
    "epoch": [60],
    "obstacle_number": [120],
    "landscape_size": [150],
    "vx_min": [10],
    "vx_max": [20],
    "vy_max": [90]}