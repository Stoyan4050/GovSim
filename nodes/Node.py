import numpy as np
from voting_incentives import Incentive

# Node class
# Defines the nodes in the network
class Node:
    def __init__(self, wealth, group, incentive_mechanism):
        self.wealth = wealth
        self.group = group
        self.incentive_mechanism = incentive_mechanism
        self.connections = []
        self.preferences = []
        self.last_preference = None
        self.probability_vote = 0
        self.total_pen_rep = 0
    
    # Compute the fitness between 2 nodes
    def compute_fitness(self, other_node, all_nodes):
        
        R = self.get_fitness_relation_value(other_node)
        
        W = other_node.wealth / np.max([node.wealth for node in all_nodes])

        if max([len(node.connections) for node in all_nodes]) == 0:
            D = 0
        else:
            D = len(other_node.connections) / np.max([len(node.connections) for node in all_nodes])

        if len(self.preferences) < 10 or len(other_node.preferences) < 10:
            corr = 0
        else:
            corr = np.corrcoef(self.preferences[-10:], other_node.preferences[-10:])[0, 1]
            if corr < 0:
                corr = 0
                        
        return 0.5 * R + 0.5 * (corr + W + D) / 3

    # Compute the business relation value for the fitness based on node's group
    def get_fitness_relation_value(self, other_node):
        if self.group == "PT":
            if other_node.group == "PT":
                R = np.random.uniform(0, 0.5)
            else:
                R = np.random.uniform(0.5, 1)
        elif self.group == "IP":
            if other_node.group == "PT":
                R = np.random.uniform(0.5, 1)
            else:
                R = np.random.uniform(0, 0.5)
        elif self.group == "OC":
            if other_node.group == "PT":
                R = np.random.uniform(0.5, 1)
            else:
                R = np.random.uniform(0, 0.5)
        elif self.group == "CA":
            if other_node.group == "PT":
                R = np.random.uniform(0.5, 1)
            else:
                R = np.random.uniform(0, 0.5)
        else:
            Exception("Invalid group")

        return R