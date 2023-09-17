import numpy as np

# Return number of votes based on the token holdings of the voter
# One token = one vote mechanism 
def token_based_vote(voter):
    votes = np.floor(voter.wealth)

    return votes

# Return number of votes based on the token holdings of the voter
# Quadratic voting mechanism - one vote = square root of tokens 
def quadratic_vote(voter):
    votes = np.floor(np.sqrt(voter.wealth))
    return votes

# Return number of votes based on the reputation of the voter
def reputation_vote(voter):
    # Get the reputation of the voter based on the number of connections
    # Subtract the penalty (if any) from the reputation
    votes = np.floor(len(voter.connections) - voter.total_pen_rep)
    if votes < 0:
        votes = 0

    return votes
