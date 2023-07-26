import numpy as np

# Generate a voting decision
class VotingDecision:
    def __init__(self, voter, proposals):
        self.voter = voter
        self.proposals = proposals
    # Returns the voting decision of voter
    # TODO: Implement more complex voting decision
    def generate_voting_decision(self):

        if self.voter.incentive_decision == "best_interest":
            return best_interest_vote(self.proposals, self.voter)
    

#constants
#RANDOM_INFORMED  = 0.6

def best_interest_vote(proposals, voter):
    
    if voter.type == "C":
        chosen_option = proposals.candidates[np.argmax(proposals.C_preferences)]
    elif voter.type == "I":
        chosen_option = proposals.candidates[np.argmax(proposals.I_preferences)]
    elif voter.type == "R":
        chosen_option = proposals.candidates[np.argmax(proposals.R_preferences)]
    else:
        raise Exception("Invalid voter type")

    print("Voter type: ", voter.type, " Chosen option: ", chosen_option)
    return chosen_option

