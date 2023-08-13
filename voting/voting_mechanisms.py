import numpy as np

# Compute Majority Vote decision  
def token_based_vote(voter):
    votes = np.floor(voter.wealth)

    return votes

def quadratic_vote(voter):
    votes = np.floor(np.sqrt(voter.wealth))

    return votes
