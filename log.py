import logging
import os
import time

# Configuration variable to define log level, can be modified 
# Log level with numeric representation: 
#   NOTSET: 0, DEBUG 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50
log_level = logging.INFO


date_time = time.strftime("%Y%m%d-%H%M%S")

def log_config(log_level, new_path="./log"):
    """ Define log configuration and log store location
    parameters:
        log_level (constant): set up the log level
        new_path (string): log path, default is ./log
    """
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        print("Directory '% s' created" % new_path)
    logging.basicConfig(filename=f"{new_path}/log-{date_time}", filemode='w', format='%(asctime)s[%(levelname)s]-%(message)s', level = log_level)

log_config(log_level)

logging.info(f"Log level:{log_level}, log starts...")