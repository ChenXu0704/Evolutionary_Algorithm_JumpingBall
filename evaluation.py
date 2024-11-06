"""Result evaluation
"""
import os, json
import itertools
import numpy as np
import sys
import statistics
import math
import matplotlib.pyplot as plt

from landscape import create_landscape
from fitness import fitness_calculation, pop_fitness_calculation
from nn import Agent
import pandas as pd

from constants import NUMBER_OF_RUNNING
    
def read_file(path, name):
    """Read hyper parameters on current test
    
    Args:
        path (String): location of json file.
        name (String): name of the json file.
    """
    f = open(f"{path}/{name}")
    return json.load(f)

    
def convert_dict_to_string(dic1, val_is_lst = False):
    """
    Args:
        dic1 (dictionary): parameter or hyper parameter value
    """
    res = ""
    for key, val in dic1.items():
        if val_is_lst:
            for v in val:
                res = res + str(v)
        else:
            res = res + str(val)
    return res
    
    
    
def final_model_fitness_analysis(main_path):
    """
    Args:
        main_path (string): path of current test
    """
    hyper_param = read_file(main_path, "hyper_parameters.json")
    param_combinations = list(itertools.product(*hyper_param.values()))
    num_combinations = len(param_combinations)
    epoch = hyper_param['epoch'][0]
    fitness_max = [[] for i in range(num_combinations)]
    fitness_mean = [[] for i in range(num_combinations)]
    for i in range(1, NUMBER_OF_RUNNING + 1, 1):
        base_path = f"{main_path}/test_{i}"
        for j in range(1, num_combinations + 1, 1):
            path = f"{base_path}/{j}"
            file_name = "output.json"
            if not os.path.exists(f"{path}/{file_name}"):
                print(f"Can not find output.json file in {path}.......")
                fitness_max[j - 1].append(120)
                fitness_mean[j - 1].append(120)
                continue
            data = read_file(path, file_name)
            fitness_max[j - 1].append(data["generated"][epoch - 1]["best fitness"])
            fitness_mean[j - 1].append(data["generated"][epoch - 1]["average fitness"])
    fitnessmax_mean = np.array([statistics.mean(i) for i in fitness_max])
    fitnessmax_std = np.array([math.sqrt(np.var(i)) for i in fitness_max])
    
    fitnessmean_mean = np.array([statistics.mean(i) for i in fitness_mean])
    fitnessmean_std = np.array([math.sqrt(np.var(i)) for i in fitness_mean])
    # Plot the data with error bars
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.errorbar(np.arange(1, num_combinations + 1), fitnessmax_mean, yerr=fitnessmax_std, fmt='o', capsize=4)

    # Add labels and title
    ax1.set_xlabel('Test set number')
    ax1.set_ylabel('Best fitness')
    ax1.set_title('Max fitness with Error Bars')

    ax2.errorbar(np.arange(1, num_combinations + 1), fitnessmean_mean, yerr=fitnessmean_std, fmt='o', capsize=4)

    # Add labels and title
    ax2.set_xlabel('Test set number')
    ax2.set_ylabel('Mean fitness')
    ax2.set_title('Mean fitness with Error Bars')
    fig.suptitle('Max and Mean fitness plots')
    plt.show()

def print_input_param(main_path, test_list):
    """
    Args:
        main_path (string): path of current test
        tset_list (list): list that contains all the test number to be evaluate
    """
    file_name = "input_params.json"
    for t_num in test_list:
        path = f"{main_path}/test_1/{t_num}"
        data = read_file(path, file_name)
        print(data)
        
def find_test_number(main_path, input_par):
    hyper_param = read_file(main_path, "hyper_parameters.json")
    param_combinations = list(itertools.product(*hyper_param.values()))
    num_combinations = len(param_combinations)
    target_input = convert_dict_to_string(input_par)
    file_name = "input_params.json"
    for i in range(1, num_combinations + 1, 1):
        path = f"{main_path}/test_1/{i}"
        cur_input = convert_dict_to_string(read_file(path, file_name))
        if cur_input == target_input:
            return i

def check_test_num_for_given_par(main_path, par_name, par_val):
    """
    Args:
        main_path (string): path of current test
        par_name (string): name of the parameter
        par_val (type of par_name): value of par_name
    """
    hyper_param = read_file(main_path, "hyper_parameters.json")
    param_combinations = list(itertools.product(*hyper_param.values()))
    num_combinations = len(param_combinations)
    file_name = "input_params.json"
    for i in range(1, num_combinations + 1, 1):
        path = f"{main_path}/test_1/{i}"
        data = read_file(path, file_name)
        if data[par_name] == par_val:
            print(i)
    


def model_evolution_analysis(main_path, test_lst, test_name_lst):
    """
    Args:
        main_path (string): path of current test
        tset_list (list): list that contains all the test number to be evaluate
    """
    hyper_param = read_file(main_path, "hyper_parameters.json")
    num_combinations = len(test_lst)
    epoch = hyper_param['epoch'][0]
    fitness_max = [[[]for j in range(epoch)] for i in range(num_combinations)]
    fitness_mean = [[[]for j in range(epoch)] for i in range(num_combinations)]
    
    for i in range(1, 20 + 1, 1):
        base_path = f"{main_path}/test_{i}"
        for j in range(len(test_lst)):
            test_id = test_lst[j]
            path = f"{base_path}/{test_id}"
            file_name = "output.json"
            if not os.path.exists(f"{path}/{file_name}"):
                print(f"Can not find output.json file in {path}.......")
                continue
            data = read_file(path, file_name)
            for k in range(len(data['generated'])):
                fitness_max[j - 1][k].append(data['generated'][k]['best fitness'])
                fitness_mean[j - 1][k].append(data['generated'][k]['average fitness'])
            
    fitness_max_mean = [[] for i in range(num_combinations)]
    fitness_mean_mean = [[] for i in range(num_combinations)]
    for i in range(num_combinations):
        for j in range(epoch):
            fitness_max_mean[i].append(statistics.mean(fitness_max[i][j]))
            fitness_mean_mean[i].append(statistics.mean(fitness_mean[i][j]))


    x = np.linspace(0, 60, 60)
    y = []
    for i in range(num_combinations):
        y.append(fitness_max_mean[i])

    # create a figure and axes object
    fig, ax1 = plt.subplots()

    for i in range(num_combinations):
    # plot the first line on the axes object
        ax1.plot(x, y[i], label= f"test {i}: {test_name_lst[i]}")

    # add a legend to the plot
    ax1.legend()

    # set the title and axis labels
    ax1.set_title('Fitness vs generation (maximum fitness)')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Maximum fitness')
    
    
    y = []
    for i in range(num_combinations):
        y.append(fitness_mean_mean[i])
    
    fig, ax2 = plt.subplots()

    for i in range(num_combinations):
    # plot the first line on the axes object
        ax2.plot(x, y[i], label= f"test {i}: {test_name_lst[i]}")

    # add a legend to the plot
    ax2.legend()

    # set the title and axis labels
    ax2.set_title('Fitness vs generation (mean fitness)')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Mean fitness')

    # show the plot
    plt.show()
  
if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Please assign test number for this test and run something like: python3 evaluation.py test1.")
        
    cur_dir = os.getcwd()
    main_path = f"{cur_dir}/test/{sys.argv[1]}"
    #model_evolution_analysis(main_path, [74, 86, 80, 73, 76, 78],["Benchmark", "nstep", "fitness got by mean", "replacement", "MPS","tournament"])
    #model_evolution_analysis(main_path,[i for i in range(1, 33)], [i for i in range(1, 33)])
    final_model_fitness_analysis(main_path)
