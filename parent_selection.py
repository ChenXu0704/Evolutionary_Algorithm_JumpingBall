"""_description_
"""
import random


def MPS(fitness, mating_pool_size):
    """Multi-pointer selection (MPS)
    Args:
        fitness (list): a list that stores the fitness value for all parents
        mating_pool_size (int): number of offspring generated
    
    """

    selected_to_mate = []
    fitness_sum = sum(fitness)
    prefix_sum = []
    prefix_sum.append(0)
    
    for i in range(len(fitness)):
        cdf = prefix_sum[len(prefix_sum) - 1]
        prefix_sum.append(cdf + fitness[i] / fitness_sum)
    
    interval = 1 / mating_pool_size
    starting_point = random.uniform(0, interval)
    pointer_positions = [starting_point + i * interval for i in range(mating_pool_size)]
    
    index_cdf = 0
    index_mp = 0
    while index_mp < mating_pool_size:
        while (prefix_sum[index_cdf] < pointer_positions[index_mp]):
            index_cdf += 1
        selected_to_mate.append(index_cdf - 1)
        index_mp += 1
    return selected_to_mate


def tournament(fitness, mating_pool_size, tournament_size):
    """Tournament selection without replacement
    Args:
        fitness (list): a list that stores the fitness value for all parents
        mating_pool_size (int): number of offspring generated
        tournament_size (int): size of tournament for each round of parent selection
    """

    selected_to_mate = []

    # student code starts
    for _ in range(mating_pool_size):
        selected = set()
        max_fitness = -1
        max_fitness_index = -1
        while len(selected) < tournament_size:
            ind = random.randint(0, len(fitness) - 1)
            while ind in selected:
                ind = random.randint(0, len(fitness) - 1)
            selected.add(ind)
            if max_fitness < fitness[ind]:
                max_fitness = fitness[ind]
                max_fitness_index = ind
        selected_to_mate.append(max_fitness_index)
    
    return selected_to_mate


def random_uniform (population_size, mating_pool_size):
    """Random uniform selection
    Args:
        population_size (int): number of population
        mating_pool_size (int): number of offspring
    """
    selected_to_mate = []
    for _ in range(mating_pool_size):
        selected_to_mate.append(int(random.uniform(0, 1) * population_size))
    
    return selected_to_mate

def topK(fitness, mating_pool_size):
    """Select parents with highest fitness score
    Args:
        fitness (list): a list that stores the fitness value for all parents
        mating_pool_size (int): number of offspring generated
    """
    ind_list = [(fitness[i], i)for i in range(len(fitness))]
    ind_list.sort(key = lambda x:x[0], reverse=True)
    
    return [ind_list[i][1] for i in range(0, mating_pool_size)]

class ParentSelection:
    """ Class to choose parent selection based on type
    """
    def __init__(self, type, mating_pool_size, population_size, tournament_size, fitness):
        self.type=type
        self.mating_pool_size=mating_pool_size
        self.fitness=fitness
        self.population_size=population_size
        self.tournament_size=tournament_size

    def selection(self):
        method_name=self.type+"_selection"
        method=getattr(self, method_name, lambda :'Invalid')
        return method()
  
    def MPS_selection(self):
        return MPS(self.fitness, self.mating_pool_size)

    def tournament_selection(self):
        return tournament(self.fitness, self.mating_pool_size, self.tournament_size)
 
    def random_uniform_selection(self):
        return random_uniform(self.population_size, self.mating_pool_size)
    
    def topK_selection(self):
        return topK(self.fitness, self.mating_pool_size)