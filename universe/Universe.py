#import wealth_distribution as wd

# Universe Class

class Universe:
  def __init__(self, participants, avg_voting_rate, tokens_amount, participants_per_group):
    self.participants = participants
    self.avg_voting_rate = avg_voting_rate
    self.tokens_amount = tokens_amount
    self.participants_per_group = participants_per_group

  def get_avg_voting_rate(self):
    return self.avg_voting_rate
  
  def get_participants(self):
    return self.participants
  
  def get_wealth(self):
    return self.wealth
  
  def tokens_amount(self):
    return self.tokens_amount
  
    