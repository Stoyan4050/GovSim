import numpy as np
import random
from scipy.stats import truncnorm

# Generate a voting decision
class VotingDecision:
    def __init__(self, voter, proposal):
        self.voter = voter
        self.proposal = proposal
    # Returns the voting decision of voter
    # TODO: Implement more complex voting decision
    def generate_voting_decision(self):
        
        return compute_preferences(self.proposal, self.voter)
    

#constants
#RANDOM_INFORMED  = 0.6

def compute_preferences(proposal, voter):
    
    if voter.group == "OC":
        if proposal.OC_preferences == 1:
            # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
            preference_continuos = generate_truncated_normal(mean=0.75)


    elif voter.type == "IP":
        if proposal.IP_preferences == 1:
            # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
            preference_continuos = generate_truncated_normal(mean=0.75)
            
    elif voter.type == "PT":
        if proposal.PT_preferences == 1:
            # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
            preference_continuos = generate_truncated_normal(mean=0.75)
            
    elif voter.type == "CA":
        if proposal.CA_preferences == 1:
            # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
            preference_continuos = generate_truncated_normal(mean=0.75)
            
    else:
        raise Exception("Invalid voter type")

    #print("Voter type: ", voter.type, " Chosen option: ", chosen_option)
    return chosen_option

def get_mean_connections(voter):
    sum_preferences = 0
    for node in voter.connections:
        # could lead to error
        sum_preferences += node.last_preference[-1]

def generate_truncated_normal(mean, sd=0.1, low=0, upp=1):
    """
    Generate a random number from a truncated normal distribution.

    Parameters:
    - mean (float): Mean of the distribution.
    - sd (float): Standard deviation.
    - low (float): Lower bound of the truncation.
    - upp (float): Upper bound of the truncation.

    Returns:
    - float: A random number from the truncated normal distribution.
    """
    a, b = (low - mean) / sd, (upp - mean) / sd
    return truncnorm.rvs(a, b, loc=mean, scale=sd)