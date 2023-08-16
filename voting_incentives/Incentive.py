import numpy as np
from scipy.stats import truncnorm

# constants:
AVG_PARTICIPATION_RATE = 0.245

class Incentive:
    def __init__(self, network, proposal, incentive_mechanism=None):
        self.incentive_mechanism = incentive_mechanism
        self.network = network
        self.proposal = proposal

    def get_probability_vote(self):
        self.participation_probability()

        if self.incentive_mechanism == "wealth":
            self.wealth_based_prize()
        elif self.incentive_mechanism == "reputations":
            self.reputation_based_prize()
        elif self.incentive_mechanism == "penalty":
            self.non_voting_penalty()

        
    def wealth_based_prize(self):
        max_wealth = np.max([node.wealth for node in self.network.nodes])

        for node in self.network.nodes:
            node.probability_vote =+ (node.wealth / max_wealth)
            if node.probability_vote > 1:
                node.probability_vote = 1
    

    def participation_probability(self):
        """
        Calculate the participation probability for each participant.
        
        Parameters:
        - group_benefit (str): The group with a higher participation rate.
        
        """ 

        for node in self.network.nodes:
            if node.last_preference <= 0.6 and node.last_preference >= 0.4:
                # Calculate alpha based on the desired mean
                node.probability_vote = self.generate_truncated_normal(0.25)

            else:
                node.probability_vote = self.generate_truncated_normal(0.75)
    


    def generate_truncated_normal(self, mean, sd=0.1, low=0, upp=1):
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
        