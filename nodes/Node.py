from voting_incentives import Incentive
class Node:
    def __init__(self, type, community, incentive_mechanism, wealth, reputation, incentive_decision):
        self.type = type
        self.community = community
        self.incentive_mechanism = incentive_mechanism
        self.wealth = wealth
        self.reputation = reputation
        self.incentive_decision = incentive_decision
    
    def get_voting_incentive(self):
        return Incentive.Incentive(self).get_voting_incentive()