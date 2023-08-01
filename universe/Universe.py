#import wealth_distribution as wd

# Universe Class

class Universe:
  def __init__(self, participants, avg_voting_rate, wealth, tokens_amount, wealth_dis_method, condition):
    self.participants = participants
    self.avg_voting_rate = avg_voting_rate
    self.wealth = wealth
    self.tokens_amount = tokens_amount
    self.wealth_dis_method = wealth_dis_method
    self.condition = condition

  # Returns the wealth distribution of the universe, tokens per participant
  def get_wealth_distribtuion_universe(self):
    return wd.WealthDistribution(self.wealth_dis_method, self.participants, self.wealth).get_wealth_distribution()

  def get_avg_voting_rate(self):
    return self.avg_voting_rate
  
  def get_participants(self):
    return self.participants
  
  def get_wealth(self):
    return self.wealth
  
  def tokens_amount(self):
    return self.tokens_amount
  
  def get_token_value(self):
    return self.wealth / self.tokens_amount
    