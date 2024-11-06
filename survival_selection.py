"""_description
"""
import random

def mu_plus_lambda(current_pop, current_fitness, offspring, offspring_fitness):
    """mu+lambda selection
    Args:
        current_pop (list): chromosomes of current population
        current_fitness (list): fitness value corresponding to the current_pop list
        offspring (list): chromosomes of offspring
        offspring_fitness (list): fitness value corresponding to the offspring list
    """
    population = []
    fitness = []
    mu = len(current_pop)
    fitness_to_pop = dict()
    for val in current_fitness:
        fitness_to_pop[val] = []
    for val in offspring_fitness:
        fitness_to_pop[val] = []
        
    for seq, fit_val in zip(current_pop, current_fitness):
        fitness_to_pop[fit_val].append(seq)
    for seq, fit_val in zip(offspring, offspring_fitness):
        fitness_to_pop[fit_val].append(seq)
    current_fitness.sort(reverse = True)
    offspring_fitness.sort(reverse = True)
    id_cur = 0
    id_off = 0
    while mu > 0:
        if id_off == len(offspring_fitness) or current_fitness[id_cur] >= offspring_fitness[id_off]:
            fitness.append(current_fitness[id_cur])
            population.append(fitness_to_pop[current_fitness[id_cur]].pop())
            id_cur += 1
        else:
            fitness.append(offspring_fitness[id_off])
            population.append(fitness_to_pop[offspring_fitness[id_off]].pop())
            id_off += 1
        mu -= 1
        
    return population, fitness
    
def replacement(current_pop, current_fitness, offspring, offspring_fitness):
    """replacement selection
    Args:
        current_pop (list): chromosomes of current population
        current_fitness (list): fitness value corresponding to the current_pop list
        offspring (list): chromosomes of offspring
        offspring_fitness (list): fitness value corresponding to the offspring list
    """

    population = []
    fitness = []
    pop_off = len(offspring)
    left = 0
    right = len(current_fitness) - 1
    pivot = -1
    while pivot != pop_off:
        pivot = left + (right - left) // 2
        swap(current_pop, pivot, right)
        swap(current_fitness, pivot, right)
        pivot = right
        right -= 1
        cur_left = left
        cur_right = right
        while left <= right:
            if current_fitness[left] <= current_fitness[pivot]:
                left += 1
            else:
                swap(current_pop, left, right)
                swap(current_fitness, left, right)
                right -= 1
        swap(current_pop, pivot, left)
        swap(current_fitness, pivot, left)
        pivot = left
        if pivot > pop_off:
            left = cur_left
            right = pivot - 1
        if pivot < pop_off:
            left = pivot + 1
            right = cur_right
            
    population = current_pop[pop_off:] + offspring
    fitness = current_fitness[pop_off:] + offspring_fitness

    return population, fitness
   
def swap(lst, index1, index2):
    """
    swap two elements in a list
    Args:
        lst (list): list that swap operation is applied on
        index1, index2 (int): two indeces the value of which will be swapped
    """
    tmp = lst[index1]
    lst[index1] = lst[index2]
    lst[index2] = tmp

def random_uniform(current_pop, current_fitness, offspring, offspring_fitness):
    """random uniform selection
    Args:
        current_pop (list): chromosomes of current population
        current_fitness (list): fitness value corresponding to the current_pop list
        offspring (list): chromosomes of offspring
        offspring_fitness (list): fitness value corresponding to the offspring list
    """
    population = []
    fitness = []
    merge_pop = current_pop + offspring
    merge_fit = current_fitness + offspring_fitness
    remaining = len(current_pop)
    while remaining > 0:
        cur_id = random.randint(0, len(merge_pop) - 1)
        swap(merge_pop, cur_id, len(merge_pop) - 1)
        swap(merge_fit, cur_id, len(merge_pop) - 1)
        population.append(merge_pop.pop())
        fitness.append(merge_fit.pop())
        remaining -= 1

    return population, fitness

survival_selection = {"mu_plus_lambda": mu_plus_lambda,
                      "replacement": replacement,
                      "random_uniform": random_uniform}