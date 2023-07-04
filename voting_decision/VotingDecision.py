# Generate a voting decision

class VotingDecision:
    def __init__(self, votes_number, votes_positive, votes_negative, votes_abstain):
        self.votes_number = votes_number
        self.votes_positive = votes_positive
        self.votes_negative = votes_negative
        self.votes_abstain = votes_abstain

    # Returns the voting decision
    # TODO: Implement voting decision
    def generate_voting_decision(self):
        return self.evaluate_decision()
    
    # Evaluates various factors to determine the voting decision
    # TODO: Implement voting decision evaluation
    def evaluate_decision(self):
        return self.votes_positive / self.votes_number 

