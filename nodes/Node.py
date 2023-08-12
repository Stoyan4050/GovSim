import numpy as np
from voting_incentives import Incentive

class Node:
    def __init__(self, wealth, group, incentive_mechanism):
        self.wealth = wealth
        self.group = group
        self.incentive_mechanism = incentive_mechanism
        self.connections = []
        self.preferences = []
    
    def get_voting_incentive(self):
        return Incentive.Incentive(self).get_voting_incentive()

    def update_preferences(self, proposal):
        # Update the preferences of the node based on the proposal
        if proposal[self.group] == 1:
            preference = np.random.normal(0.75, 0.05)
        elif any([conn.preferences[-1] > 0.5 for conn in self.connections]):
            preference = sum([conn.preferences[-1] for conn in self.connections]) / len(self.connections)
        else:
            preference = np.random.normal(0.5, 0.05)
        
        # Remove the oldest preference and add the new preference
        self.preferences.pop(0)
        self.preferences.append(preference)

