import numpy as np
import random
from scipy.stats import truncnorm

# Generate a voting decision
class VotingDecision:
    def __init__(self, voters, proposal):
        self.voters = voters
        self.proposal = proposal
    # Returns the voting decision of voter
    def generate_voting_decision_benefit(self):
        left_to_vote = [] 
        for voter in self.voters:
            preference_continuos = compute_preferences_benefit(self.proposal, voter)
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                voter.preferences.append(preference_continuos)
            else:
                left_to_vote.append(voter)
        #print("Voters1: ", len(left_to_vote))
        return left_to_vote
    
    def generate_voting_decision_neutral(self):
        left_to_vote = [] 
        for voter in self.voters:
            preference_continuos = compute_preferences_neutral(self.proposal, voter)
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                voter.preferences.append(preference_continuos)
            else:
                left_to_vote.append(voter)
        #print("Voters2: ", len(left_to_vote))

        return left_to_vote
    
    def generate_voting_decision_connections(self):
        left_to_vote = [] 
        for voter in self.voters:
            preference_continuos = compute_preferences_connections(voter)
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                voter.preferences.append(preference_continuos)
            else:
                left_to_vote.append(voter)
        #print("Voters3: ", len(left_to_vote))

        return left_to_vote
    

def compute_preferences_benefit(proposal, voter):
    
    if voter.group == "OC" and proposal.OC_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
        #print("A1 ", voter.group, preference_continuos)

    elif voter.group == "IP" and proposal.IP_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
        #print("A1 ", voter.group, preference_continuos)

            
    elif voter.group == "PT" and proposal.PT_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
        #print("A1 ", voter.group, preference_continuos)
  
    elif voter.group == "CA" and proposal.CA_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
        #print("A1 ", voter.group, preference_continuos)


    else:
        return None

    return preference_continuos

def compute_preferences_neutral(proposal, voter):
    
    neutral_flag = 1

    # Check if the voter is actually neutral
    for node in voter.connections:
        if node.group == "OC" and proposal.OC_preferences == 1:
            neutral_flag = 0
        
        elif node.group == "IP" and proposal.IP_preferences == 1:
            neutral_flag = 0
        
        elif node.group == "CA" and proposal.CA_preferences == 1:
            neutral_flag = 0

        elif node.group == "PT" and proposal.PT_preferences == 1:
            neutral_flag = 0

    if neutral_flag == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.25)
        #print("A2 ", voter.group, preference_continuos)

        return preference_continuos
    
    else:
        return None

def compute_preferences_connections(voter):
    sum_preferences = 0
    connection_with_preferences = 0
    # Iterate through all connections of the voter
    for node in voter.connections:
        # Check if the node has preference
        if node.last_preference != None:
            sum_preferences += node.last_preference
            connection_with_preferences += 1
        # else:
        #     preference_continuos = generate_truncated_normal(mean=0.25)
        #     sum_preferences += preference_continuos
        #     connection_with_preferences += 1
            #print("NONE")
    
    #print("A3 ", voter.group, sum_preferences / connection_with_preferences)

    return sum_preferences / connection_with_preferences

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