import numpy as np
import random
from scipy.stats import truncnorm

# Generate a voting decision
class VotingDecision:
    def __init__(self, voters, proposal):
        self.voters = voters
        self.proposal = proposal

    # Returns the voting decision of a voter if the proposal benefits him
    def generate_voting_decision_benefit(self):
        left_to_vote = [] 
        for voter in self.voters:
            # Check if the voter is benefiting from the proposal
            # If benefiting, generate voting decision with mean 0.75
            preference_continuos = compute_preferences_benefit(self.proposal, voter)
            # Update the last preference of the voter
            # Add the last preference to the list of preferences of the voter
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                voter.preferences.append(preference_continuos)
            # If not benefiting from the proposal, add the voter to the list of voters that still do not have a voting decision
            else:
                left_to_vote.append(voter)
        # Return the list of voters that still do not have a voting decision
        return left_to_vote
    
    # Generate the voting decision of a voter if the proposal is neutral
    def generate_voting_decision_neutral(self):
        left_to_vote = [] 
        for voter in self.voters:
            # Check if the voter is neutral to the proposal
            # If neutral, generate voting decision with mean 0.25
            preference_continuos = compute_preferences_neutral(self.proposal, voter)
            # Update the last preference of the voter
            # Add the last preference to the list of preferences of the voter
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                voter.preferences.append(preference_continuos)
            # If not neutral to the proposal, add the voter to the list of voters that still do not have a voting decision
            else:
                left_to_vote.append(voter)
        # Return the list of voters that still do not have a voting decision
        return left_to_vote
    
    # Generate the voting decision of a voter if the proposal influences the connections of the voter
    def generate_voting_decision_connections(self):
        left_to_vote = [] 
        for voter in self.voters:
            # Check if the voter's connections are influenced by the proposal
            # If connections are influenced, generate voting decision that is equal to the mean of the last preferences of the connections
            preference_continuos = compute_preferences_connections(voter)
            # Update the last preference of the voter
            # Add the last preference to the list of preferences of the voter
            if preference_continuos != None:
                voter.last_preference = preference_continuos
                voter.preferences.append(preference_continuos)
            # If the voter's connections are not influenced by the proposal, 
            # add the voter to the list of voters that still do not have a voting decision
            else:
                left_to_vote.append(voter)
        # Return the list of voters that still do not have a voting decision
        # After this function, all voters should have a voting decision
        # Thus the list should be empty
        return left_to_vote
    
# Compute the preferences of a voter if the proposal benefits him
def compute_preferences_benefit(proposal, voter):
    
    if voter.group == "OC" and proposal.OC_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)

    elif voter.group == "IP" and proposal.IP_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
            
    elif voter.group == "PT" and proposal.PT_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)
  
    elif voter.group == "CA" and proposal.CA_preferences == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.75)

    else:
        return None

    return preference_continuos

def compute_preferences_neutral(proposal, voter):
    
    neutral_flag = 1

    # Check if the voter is neutral
    for node in voter.connections:
        if node.group == "OC" and proposal.OC_preferences == 1:
            neutral_flag = 0
        
        elif node.group == "IP" and proposal.IP_preferences == 1:
            neutral_flag = 0
        
        elif node.group == "CA" and proposal.CA_preferences == 1:
            neutral_flag = 0

        elif node.group == "PT" and proposal.PT_preferences == 1:
            neutral_flag = 0
    
    # If the flag is still 1, none of the connections of the voter are influenced by the proposal
    # Thus the voter is neutral
    # If the voter is neutral, generate voting decision with mean 0.25
    if neutral_flag == 1:
        # Randomly select preference from truncated normal distribution with mean 0.75, interval [0,1]
        preference_continuos = generate_truncated_normal(mean=0.25)

        return preference_continuos
    
    else:
        return None

# Compute the preferences of a voter if the proposal influences the connections of the voter
def compute_preferences_connections(voter):
    sum_preferences = 0
    connection_with_preferences = 0
    # Iterate through all connections of the voter
    for node in voter.connections:
        # Check if the node has preference
        if node.last_preference != None:
            # Add the last preference of the node to the sum of preferences
            sum_preferences += node.last_preference
            connection_with_preferences += 1
        else:
            # If a connection does not have a preference, generate a random preference with mean 0.5
            # This value represents neutral behavior
            preference_continuos = generate_truncated_normal(mean=0.5)
            sum_preferences += preference_continuos
            connection_with_preferences += 1

    # Return the mean of the preferences of the connections of the voter  
    return sum_preferences / connection_with_preferences


# Get values from truncated normal distribution with given mean
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

