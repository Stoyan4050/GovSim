import numpy as np
from scipy.stats import truncnorm
from voting.voting_mechanisms import token_based_vote, quadratic_vote, reputation_vote

# Incentive class
class Incentive:
    def __init__(self, network, proposal, incentive_mechanism=None):
        self.incentive_mechanism = incentive_mechanism
        self.network = network
        self.proposal = proposal
    
    # Get the probability to vote based on the incentive mechanism
    # If incentive mechanism is not specified, no incentive is applied
    def get_probability_vote(self):
        self.participation_probability()

        if self.incentive_mechanism == "wealth":
            self.wealth_based_prize()
        elif self.incentive_mechanism == "reputation":
            self.reputation_based_prize()
        elif self.incentive_mechanism == "penalty":
            self.non_voting_penalty()

    # Increase the probability to vote based on the token holdings of the voter
    def wealth_based_prize(self):
        # Calculate the minimum and maximum wealth in the network
        max_wealth = np.max([node.wealth for node in self.network.nodes])
        min_wealth = np.min([node.wealth for node in self.network.nodes])

        for node in self.network.nodes:
            # Get the current probability to vote
            prob_vote = node.probability_vote
            # Increase the probability to vote based on the wealth of the voter
            node.probability_vote = prob_vote + ((node.wealth - min_wealth) / (max_wealth - min_wealth))
            
            # If the probability to vote is greater than 1, set it to 1
            if node.probability_vote > 1:
                node.probability_vote = 1

    def non_voting_penalty(self):
        # Calculate the minimum and maximum wealth in the network
        max_wealth = np.max([node.wealth for node in self.network.nodes])
        min_wealth = np.min([node.wealth for node in self.network.nodes])

        for node in self.network.nodes:
            # Get the current probability to vote
            prob_vote = node.probability_vote
            # Increase the probability to vote based on the wealth of the voter
            node.probability_vote = prob_vote + ((node.wealth - min_wealth) / (max_wealth - min_wealth))
            # If the probability to vote is greater than 1, set it to 1
            if node.probability_vote > 1:
                node.probability_vote = 1

    # Increase the probability to vote based on the reputation of the voter
    def reputation_based_prize(self):
        # Calculate the minimum and maximum reputation in the network
        max_reputation = np.max([len(node.connections) for node in self.network.nodes])
        min_reputation = np.min([len(node.connections) for node in self.network.nodes])

        for node in self.network.nodes:
            prob_vote = node.probability_vote
            # Increase the probability to vote based on the reputation of the voter
            node.probability_vote = prob_vote + (len(node.connections) - min_reputation) / (max_reputation - min_reputation)
            # If the probability to vote is greater than 1, set it to 1
            if node.probability_vote > 1:
                node.probability_vote = 1

    # Calculate the effect of the penalty incentive mechanism on the nodes
    # Token holdings are reduced by 10% if the node does not vote
    def penalty_effect_wealth(self, node):
        # Set the penalty rate
        pen = 0.1
        # Calculate the penalty and update the wealth of the node based on the penalty
        if node.wealth >pen*node.wealth:
            w = node.wealth
            node.wealth = w - pen*w
            self.network.tokens_amount -= pen*w


    # Calculate the effect of the penalty incentive mechanism on the nodes
    # Reputation is reduced by 10% if the node does not vote
    def penalty_effect_reputation(self, node):
        # Set the penalty rate
        pen = 0.1
        # Calculate the penalty and update the reputation of the node based on the penalty
        penalty_rep = (len(node.connections) - node.total_pen_rep)*pen
        node.total_pen_rep += penalty_rep


    # Get the initial probability to vote for each node
    def participation_probability(self):
        """
        Calculate the participation probability for each participant.

        """ 

        for node in self.network.nodes:
            # If a node has a weak preference that is below 0.6 and above 0.4, 
            # this indicates that the node is not bery interested in the proposal
            # and therefore the probability to vote is sampled from a truncated normal distribution with mean 0.25
            if node.last_preference <= 0.6 and node.last_preference >= 0.4:
                node.probability_vote = self.generate_truncated_normal(0.25)

            else:
                # If a node has a strong preference that is above 0.6 or below 0.4,
                # this indicates that the node is interested in the proposal
                # and therefore the probability to vote is sampled from a truncated normal distribution with mean 0.75
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
        