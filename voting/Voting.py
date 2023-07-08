import numpy as np
from voting_mechanisms import majority_vote
from voting_decision import VotingDecision

# constants:
VOTING_INCENTIVE_THRESHOLD = 0.5

# Voting simulation class
# Candidates: list of candidates, for voters to select the preferred candidate
class Voting:
    def __init__(self, candidates, voters, voting_mechanism):
        self.candidates = candidates
        self.voters = voters
        self.voting_mechanism = voting_mechanism

    def vote(self):
        # Each voter votes for a candidate we save the votes in a list
        votes = []
        # Each voter votes for a candidate
        for voter in self.voters:
            decision = self.get_decision_voter(self, voter)
            if decision != "abstain":
                votes.append(decision)
        
        # Get the results of the voting mechanism and the voting decision
        voting_outcome, voting_summary = self.get_results(votes, self.voting_mechanism)

        # Display the results
        self.display_results(voting_outcome, voting_summary)

    # TODO: Implement more complex voting decision
    def get_decision_voter(self, voter):
        # Get the decision of the voting mechanism
        if voter.get_voting_incentive() < VOTING_INCENTIVE_THRESHOLD:
            return "abstain"
        else:
            voter_decision = VotingDecision(voter, self.candidates).generate_voting_decision()
        
        return voter_decision
        
    def get_results(self, votes, voting_mechanism):
        if voting_mechanism == "majority_vote":
            return majority_vote(self.candidates, votes)
        else:
            Exception("Voting mechanism not found")

    
    # Display the results
    def display_results(results, voting_results, voting_rate):
        print("Participation rate: ", voting_rate)
        print(voting_results[0][0] + ": " + str(voting_results[0][1])) 
        print(voting_results[1][0] + ": " + str(voting_results[1][1]))
        print("Winner: ", results)
        return results
    
        

        