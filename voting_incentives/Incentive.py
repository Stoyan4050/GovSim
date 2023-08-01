import numpy as np

class Incentive:
    def __init__(self, voter):
        self.incentive_mechanism = voter.incentive_mechanism
        self.voter = voter
    
    def get_voting_incentive(self):
        if self.incentive_mechanism == "normal_distribution":
            return self.normal_distribution_incentive()
        elif self.incentive_mechanism == "wealth":
            return self.wealth_incentive()
        elif self.incentive_mechanism == "reputation":
            return self.reputation_incentive()
        elif self.incentive_mechanism == "constant":
            return 1
        else:
            Exception("Incentive mechanism not found")
        
    
    def normal_distribution_incentive(self):
        # Define the parameters for the normal distribution
        # For mean we use the average voting rate of the universe
        mean = self.voter.get_avg_voting_rate()
        std_dev = 1.0  # standard deviation

        # Generate a sample of 1000 values from the distribution
        incentive = np.random.normal(mean, std_dev, 1)

        return incentive

    # TODO: Implement wealth incentive
    def wealth_incentive(self):
        return 0
    
    # TODO: Implement reputation incentive
    def normal_distribution_incentive(self):
        return 0
