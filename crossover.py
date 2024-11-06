"""_description_
"""
from nn import Agent
import numpy as np

def bulk_crossover(agent1, agent2):
    """
    Apply bulk crossover on the chromosome of two agents
    Args:
        agent1, agent2 (nn): nn objects
    """
    offspring1 = Agent(agent1.n_feature, agent1.n_hidden, agent1.n_out)
    offspring2 = Agent(agent1.n_feature, agent1.n_hidden, agent1.n_out)
    
    offspring1.w_ih = agent1.w_ih
    offspring1.w_ho = agent2.w_ho
    
    offspring2.w_ih = agent2.w_ih
    offspring2.w_ho = agent1.w_ho

    return offspring1, offspring2
    
def sample_crossover(agent1, agent2, rate):
    """
    Apply sampled crossover on the chronosome of two agents
    Args:
        agent1, agent2 (nn): nn objects
        rate (float): probability that one gene would be switched
    """
    mask_ih = np.random.rand(agent1.n_feature, agent1.n_hidden) <= rate
    mask_ho = np.random.rand(agent1.n_hidden, agent1.n_out) <= rate
    
    offspring1 = Agent(agent1.n_feature, agent1.n_hidden, agent1.n_out)
    offspring2 = Agent(agent1.n_feature, agent1.n_hidden, agent1.n_out)

    offspring1.w_ih = np.multiply(agent1.w_ih, 1 - mask_ih) + np.multiply(agent2.w_ih, mask_ih)
    offspring1.w_ho = np.multiply(agent1.w_ho, 1 - mask_ho) + np.multiply(agent2.w_ho, mask_ho)
    
    offspring2.w_ih = np.multiply(agent1.w_ih, mask_ih) + np.multiply(agent2.w_ih, 1 - mask_ih)
    offspring2.w_ho = np.multiply(agent1.w_ho, mask_ho) + np.multiply(agent2.w_ho, 1 - mask_ho)
    
    return offspring1, offspring2

def _bulk_crossover(agent1, agent2, rate):
    return bulk_crossover(agent1, agent2)

crossover = {"bulk": _bulk_crossover, 
             "sample": sample_crossover}