"""_description_
"""
import numpy as np

class Agent:
    """
        Create Agent (player) object
    """
    
    def __init__(self, n_feature, n_hidden, n_out):
        """
        Initialization the Agent
        
        Args:
            n_feature (int): number of features that fed into neural network
            n_hidden (int): number of nodes at hidden layer
            n_out (int): number of nodes at output layer
        """
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.n_out = n_out
        self.w_ih = np.random.rand(self.n_feature, self.n_hidden)
        self.w_ho = np.random.rand(self.n_hidden, self.n_out)
        self.sigma_ih = np.random.rand(self.n_feature, self.n_hidden) * 0.4 + 0.8
        self.sigma_ho = np.random.rand(self.n_hidden, self.n_out) * 0.4 + 0.8
        self.fitness = []
        
    def update_sigma(self, rate):
        mask_ih = np.random.rand(self.n_feature, self.n_hidden) < rate
        mask_ho = np.random.rand(self.n_hidden, self.n_out) < rate
        newsigma_ih = np.random.rand(self.n_feature, self.n_hidden) * 0.4 + 0.8
        newsigma_ho = np.random.rand(self.n_hidden, self.n_out) * 0.4 + 0.8
        self.sigma_ih = (1 - mask_ih) * self.sigma_ih + mask_ih * newsigma_ih
        self.sigma_ho = (1 - mask_ho) * self.sigma_ho + mask_ho * newsigma_ho
        
    def prediction(self, input_features, activation = "relu"):
        """
        Define prediction function that predicts the x, y components of acceleration
        Args:
            input_features (np.ndarray): feature values of the ball object
            activation (String): activation function that is used at hidden layer
        """
        if activation == "sigmoid":
            return self.relu(np.dot(self.sigmoid(np.dot(input_features, self.w_ih)), self.w_ho))
        
        elif activation == "relu":
            
            return self.relu(np.dot(self.relu(np.dot(input_features, self.w_ih)), self.w_ho))
            
        else:
            raise Exception("use 'sigmoid' or 'relu' for second arg")
    
    
    def sigmoid(self, x):
        """
        Define sigmoid function
        Args:
            x (numpy.ndarray): output scores at certain layer
        """
        return np.array(1. / (1. + np.exp(-x)))
    
    def relu(self, x):
        """
        Define relu funciton
        Args:
            x (numpy.ndarray): output scores at certain layer
        """
        return np.maximum(0, np.minimum(100, x))