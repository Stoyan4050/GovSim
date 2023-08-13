import numpy as np
import random
from scipy.stats import truncnorm

# Generate a voting decision
class VotingDecision:
    def __init__(self, voters, proposal):
        self.voters = voters
        self.proposal = proposal
    # Returns the voting decision of voter
    # TODO: Implement more complex voting decision
    def generate_voting_decision_benefit(self):
        
        for voter in self.voters:
            preference_continuos = compute_preferences_benefit(self.proposal, self.voter)
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                self.voters.remove(voter)

        return self.voters
    
    def generate_voting_decision_neutral(self):

        for voter in self.voters:
            preference_continuos = compute_preferences_neutral(self.proposal, self.voter)
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                self.voters.remove(voter)

        return self.voters
    
    def generate_voting_decision_connections(self):
        
        for voter in self.voters:
            preference_continuos = compute_preferences_neutral(self.proposal, self.voter)
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                self.voters.remove(voter)

        return self.voters
    

def compute_preferences_benefit(proposal, voter):
    
    if voter.group == "OC" and proposal.OC_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)

    elif voter.type == "IP" and proposal.IP_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
            
    elif voter.type == "PT" and proposal.PT_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
            
    elif voter.type == "CA" and proposal.CA_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)

    else:
        return None

    return preference_continuos

def compute_preferences_neutral(proposal, voter):
    
    neutral_flag = 1

    # Check if the voter is actually neutral
    for node in voter.connections:
        if node.group == "OC" and proposal.OC_preferences == 1:
            neutral_flag = 0
        
        elif voter.group == "IP" and proposal.IP_preferences == 1:
            neutral_flag = 0
        
        elif voter.group == "CA" and proposal.CA_preferences == 1:
            neutral_flag = 0

        elif voter.group == "PT" and proposal.PT_preferences == 1:
            neutral_flag = 0

    if neutral_flag == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.5)
        return preference_continuos
    
    else:
        return None



def get_mean_connections(voter):
    sum_preferences = 0
    for node in voter.connections:
        if node.last_preference != None:
            sum_preferences += node.last_preference
        else:
            print("NONE")


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