# This file contains the wealth distribution class
class WealthDistribution:
    def __init__(self, method, participants, wealth):
        self.method = method
        self.wealth = wealth
    
    def get_wealth_distribution(self):
        if self.method == "uniform":
            return self.get_uniform_distribution()
        elif self.method == "normal":
            return self.get_normal_distribution()
        else:
            raise Exception("Invalid wealth distribution method")

    # TODO: Implement uniform distribution
    def get_uniform_distribution(self):
        return self.wealth / self.participants
    
    # TODO: Implement normal distribution
    def get_normal_distribution(self):
        return self.wealth / self.participants
    
