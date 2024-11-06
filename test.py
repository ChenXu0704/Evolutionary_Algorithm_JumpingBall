import itertools
import json
import os
import sys
import shutil
import numpy as np
from constants import HYPER_PARAMS, NUMBER_OF_RUNNING
from log import logging

# Generate all combinations of parameter values
param_combinations = list(itertools.product(*HYPER_PARAMS.values()))

# Number of combinations can generated from the parameters
num_combinations = np.prod([len(v) for k,v in HYPER_PARAMS.items()])

# Generate files for each parameter combination
def file_generator(combinations, params, path):
    """ Generate input and output files to each test folders
    Args:
        combinations (list): a list of all possible hyper parameters' combinations
        params (dict): hyper parameters
    """
    for i, param_values in enumerate(combinations):
        # Create a dictionary with parameter names and values
        sample_params = {}
        for j, param_name in enumerate(params.keys()):
            sample_params[param_name] = param_values[j]
        
        # Write files to directory
        if not os.path.exists(path):
            os.makedirs(path)
        new_path = f"{path}/{i+1}"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            print("Directory '% s' created" % new_path)
            src = os.listdir("./")
            for file in src:
                if file[-2:] != "py" or file == "test.py":
                    continue
                des = f"{path}/{i+1}/"
                shutil.copy(file, des)
            print("files copied into % s' created" % new_path)

        input_filename = f"{new_path}/input_params.json"
        with open(input_filename, 'w') as f:
            json.dump(sample_params, f, indent=4)
        logging.info(f"Wrote to the file: {input_filename}")
        

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Please assign test number for this test and run something like: python3 test.py 2.")
    else:
        test_number = sys.argv[1]
        test_path = "./test"
        if not os.path.exists(test_path):
            os.makedirs(test_path)
            print("Directory '% s' created" % test_path)

        test_path = f"{test_path}/test{test_number}"
        if os.path.exists(test_path):
            print(f"Assign different number for this test rather than {test_number}" )
        else:
            os.makedirs(test_path)
            print("Directory '% s' created" % test_path)
            with open(f"{test_path}/hyper_parameters.json", 'w') as f:
                json.dump(HYPER_PARAMS, f, indent = 4)
            for n in range(NUMBER_OF_RUNNING):
                if len(param_combinations) == num_combinations:
                    file_generator(param_combinations, HYPER_PARAMS, f"{test_path}/test_{n+1}")