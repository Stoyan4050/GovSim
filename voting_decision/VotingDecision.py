import numpy as np
import random

# Generate a voting decision
class VotingDecision:
    def __init__(self, voter, proposal):
        self.voter = voter
        self.proposal = proposal
    # Returns the voting decision of voter
    # TODO: Implement more complex voting decision
    def generate_voting_decision(self):

        if self.voter.incentive_decision == "best_interest":
            return best_interest_vote(self.proposal, self.voter)
    

#constants
#RANDOM_INFORMED  = 0.6

def best_interest_vote(proposal, voter):
    
    if voter.type == "C":
        preference = np.max(proposal.C_preferences)
        
        if preference == 0:
            # Randomly select from the list of choices
            chosen_option = proposal.candidates[random.choice([0, 1])]
        else:
            chosen_option = proposal.candidates[np.argmax(proposal.C_preferences)]

    elif voter.type == "I":
        preference = np.max(proposal.I_preferences)
        
        if preference == 0:
            # Randomly select from the list of choices
            chosen_option = proposal.candidates[random.choice([0, 1])]
        else:
            chosen_option = proposal.candidates[np.argmax(proposal.I_preferences)]
    elif voter.type == "M":
        preference = np.max(proposal.M_preferences)

        if preference == 0:
            # Randomly select from the list of choices
            chosen_option = proposal.candidates[random.choice([0, 1])]
        else:
            chosen_option = proposal.candidates[np.argmax(proposal.M_preferences)]
    else:
        raise Exception("Invalid voter type")

    #print("Voter type: ", voter.type, " Chosen option: ", chosen_option)
    return chosen_option

