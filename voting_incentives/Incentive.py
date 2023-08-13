import numpy as np

# constants:
VOTING_INCENTIVE_THRESHOLD = 0.5


class Incentive:
    def __init__(self, voter, universe):
        self.incentive_mechanism = voter.incentive_mechanism
        self.voter = voter
        self.universe = universe

    def get_incentive_decision(self):
        incentive_rate = self.get_voting_incentive()
        if incentive_rate > VOTING_INCENTIVE_THRESHOLD:
            return "vote"
        else:
            return "abstain"

    def get_voting_incentive(self):

        if self.incentive_mechanism == "wealth":
            return self.wealth_incentive()
        elif self.incentive_mechanism == "constant":
            return 1
        else:
            Exception("Incentive mechanism not found")
        
    # TODO: Implement wealth incentive
    def wealth_incentive(self):
        return 0
    
