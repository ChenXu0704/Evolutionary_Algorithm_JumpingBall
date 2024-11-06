# imports
import random

from fitness import fitness_calculation, pop_fitness_calculation
from crossover import crossover
from mutation import mutation
from parent_selection import ParentSelection
from survival_selection import survival_selection

from nn import Agent
from landscape import create_landscape
from constants import GRAVITY, TIME_INTERVAL
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from constants import BALL_COLOR, BALL_RADIUS, BALL_VELOCITY_X, BALL_VELOCITY_Y, BALL_X
from constants import OBSTACLE_GAP, OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_VELOCITY

import json
from log import logging

# Sample parameters
f = open("./input_params.json")
params = json.load(f)

def main(args):
    """Design the evolutionary algorithm
    Returns:
        np.ndarray: two np arrays which are the weights of the agent
    """
    hidden_layer_nodes, input_nodes, \
        mut_rate, mutation_sigma, mutation_type, \
            xover_rate, xover_exchange_rate, xover_type, \
                fitness_mode, popsize, tournament_size, \
                    parent_selection_type, survival_selection_type, \
                        epoch, obstacle_number, landscape_size, \
                             vx_min, vx_max, vy_max = [v for k,v in args.items()]

    mating_pool_size = int(popsize*0.5)
    
    population = [Agent(input_nodes, hidden_layer_nodes, 2) for _ in range(popsize)]
    landscapes = [create_landscape(obstacle_number) for _ in range(landscape_size)]
    output = {}
    
    pop_fitness = []
    for agent in population:
        agent.fitness = []
        for landscape in landscapes:
            agent.fitness.append(fitness_calculation(landscape, agent, vx_min, vx_max, vy_max))
        pop_fitness.append(pop_fitness_calculation(fitness_mode, agent.fitness))
    
    output["initial"] = {"fitness": pop_fitness}
    output["generated"] = []
    output["best_result"] = {"best_fitness": 0}

    for gen in range(epoch):
        
        # pick parents
        parents_index= ParentSelection(parent_selection_type, mating_pool_size, popsize, tournament_size, pop_fitness).selection()

        random.shuffle(parents_index)
        # reproduction
        offspring =[]
        offspring_fitness = []
        i = 0
        while len(offspring) < mating_pool_size:
        
            if random.random() < xover_rate:
                off1,off2 = crossover[xover_type](population[parents_index[i]], population[parents_index[i+1]], xover_exchange_rate)
            else:
                off1 = Agent(population[parents_index[i]].n_feature, population[parents_index[i]].n_hidden, population[parents_index[i]].n_out)
                off1.w_ih = population[parents_index[i]].w_ih
                off1.w_ho = population[parents_index[i]].w_ho
                off1.sigma_ih = population[parents_index[i]].sigma_ih
                off1.sigma_ho = population[parents_index[i]].sigma_ho
                off2 = Agent(population[parents_index[i]].n_feature, population[parents_index[i]].n_hidden, population[parents_index[i]].n_out)
                off2.w_ih = population[parents_index[i + 1]].w_ih
                off2.w_ho = population[parents_index[i + 1]].w_ho
                off2.sigma_ih = population[parents_index[i + 1]].sigma_ih
                off2.sigma_ho = population[parents_index[i + 1]].sigma_ho
            sigma = mutation_sigma
            off1.update_sigma(mut_rate)
            off2.update_sigma(mut_rate)
            mutation[mutation_type](off1, sigma, mut_rate)
            mutation[mutation_type](off2, sigma, mut_rate)

            off1.fitness = []
            off2.fitness = []
            for landscape in landscapes:
                off1.fitness.append(fitness_calculation(landscape, off1, vx_min, vx_max, vy_max))
                off2.fitness.append(fitness_calculation(landscape, off2, vx_min, vx_max, vy_max))
            offspring.append(off1)
            offspring.append(off2)
            offspring_fitness.append(pop_fitness_calculation(fitness_mode, off1.fitness))
            offspring_fitness.append(pop_fitness_calculation(fitness_mode, off2.fitness))
            i += 2

        population, pop_fitness = survival_selection[survival_selection_type](population, pop_fitness, offspring, offspring_fitness)
        
        max_fitness = max(pop_fitness)
        output["generated"].append({"generation": gen, "fitness": pop_fitness, "best fitness": max_fitness, "average fitness": sum(pop_fitness)/len(pop_fitness)})
        #logging.info(output["generated"])

        if output["best_result"]["best_fitness"] < max_fitness:
            output["best_result"]["best_fitness"] = max_fitness
            output["best_result"]["best_pops"] = find_max(population, pop_fitness, max_fitness)
        if output["best_result"]["best_fitness"] == max_fitness:
            output["best_result"]["best_pops"].extend(find_max(population, pop_fitness, max_fitness))

    logging.info("ea done..............")
    return output

def find_max(population, pop_fitness, max_val):
    """ Find information for the target max value
    Args:
        population (list(Agent)): a sequence of population
        pop_fitness (list(float)): a sequence of population fitness
        max_val (float): the target max value to search
    Returns:
        (list(dict)) a list of dictionary of weights and sigmas information based on the max value
    """
    max_indices = [index for index in range(len(pop_fitness)) if pop_fitness[index] == max_val]
    values = [{"w_ih": population[i].w_ih.tolist(), "w_ho": population[i].w_ho.tolist(), \
                                                  "sigma_ih": population[i].sigma_ih.tolist(), "sigma_ho": population[i].sigma_ho.tolist(), "fitness_list": population[i].fitness} for i in max_indices]
    return values

# Comment this out for system testing
result = main(params)
output_filename = "output.json"
with open(output_filename, 'w') as f:
    json.dump(result, f, indent=4)