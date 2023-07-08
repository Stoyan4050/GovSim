import numpy as np

# Generate a voting decision
class VotingDecision:
    def __init__(self, voter, candidates):
        self.voter = voter
        self.candidates = candidates

    # Returns the voting decision of voter
    # TODO: Implement more complex voting decision
    def generate_voting_decision(self):

        if self.voter.deincentive_decision == "random_informed_vote":
            return random_informed_vote(self.candidates, self.voter)
    

#constants
RANDOM_INFORMED  = 0.6

def random_informed_vote(candidates, voter):
    
    # We assume the first option in the candidate list is the optimal one
    probabilities = [RANDOM_INFORMED, 1 - RANDOM_INFORMED]

    # Simulate the selection process
    chosen_option = np.random.choice(candidates, p=probabilities)

    return chosen_option

