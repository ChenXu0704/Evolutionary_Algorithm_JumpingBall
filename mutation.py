"""_description_
"""
from nn import Agent
import numpy as np


def uncorr_onestep(agent, sigma, rate):
    """
    Apply uncorrelated update on genes of agent
    Args:
        agent (nn): An agent
        sigma (float): step size
        rate (float): mutation rate
    """
    mask_ih = np.random.rand(agent.n_feature, agent.n_hidden) < rate
    mask_ho = np.random.rand(agent.n_hidden, agent.n_out) < rate
    delta_ih = np.random.normal(0, sigma, (agent.n_feature, agent.n_hidden))
    delta_ho = np.random.normal(0, sigma, (agent.n_hidden, agent.n_out))
    agent.w_ih = agent.w_ih + np.multiply(delta_ih, mask_ih)
    agent.w_ho = agent.w_ho + np.multiply(delta_ho, mask_ho)
    
def uncorr_nstep(agent, sigma, rate):
    """
    Apply uncorrelated update on genes of agent
    Args:
        agent (nn): An agent
        sigma (float): a scale that applied on n-step vector
        rate (float): mutation rate
    """
    delta_ih = np.multiply(np.random.normal(0, 1, (agent.n_feature, agent.n_hidden)), agent. sigma_ih) * sigma
    delta_ho = np.multiply(np.random.normal(0, 1, (agent.n_hidden, agent.n_out)), agent.sigma_ho) * sigma
    mask_ih = np.random.rand(agent.n_feature, agent.n_hidden) < rate
    mask_ho = np.random.rand(agent.n_hidden, agent.n_out) < rate
    agent.w_ih = agent.w_ih + np.multiply(delta_ih, mask_ih)
    agent.w_ho = agent.w_ho + np.multiply(delta_ho, mask_ho)

mutation = {"onestep": uncorr_onestep,
          "nstep": uncorr_nstep}