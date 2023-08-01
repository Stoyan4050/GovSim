import numpy as np
from voting.voting_mechanisms import majority_vote
from voting_decision import VotingDecision

# constants:
VOTING_INCENTIVE_THRESHOLD = 0.5

# Voting simulation class
# Candidates: list of candidates with wights, for voters to select the preferred candidate
class Voting:
    def __init__(self, proposal, voters, voting_mechanism):
        self.proposal = proposal
        self.voters = voters
        self.voting_mechanism = voting_mechanism

    def vote(self):
        # Each voter votes for a candidate we save the votes in a list
        votes = []
        voted = 0
        abstain = 0
        # Each voter votes for a candidate
        for voter in self.voters:

            decision = self.get_decision_voter(voter)
            if decision != "abstain":
                voted+=1
                for i in range(int(voter.wealth)):
                    votes.append(decision)
            else:
                abstain+=1

        GINI = self.calculate_GINI([p.wealth for p in self.voters])
        # Get the results of the voting mechanism and the voting decision
        voting_outcome, voting_summary = self.get_results(votes, self.voting_mechanism)
        voting_rate = voted/len(self.voters)
        # Display the results
        self.display_results(voting_outcome, voting_summary, voting_rate=voting_rate)
        return voting_outcome


    # TODO: Implement more complex voting decision
    def get_decision_voter(self, voter):
        # Get the decision of the voting mechanism

        if voter.get_voting_incentive() < VOTING_INCENTIVE_THRESHOLD:
            return "abstain"
        else:
            voter_decision = VotingDecision.VotingDecision(voter, self.proposal).generate_voting_decision()
        
        return voter_decision
        
    def get_results(self, votes, voting_mechanism):
        outcome = None
        results = None
        if voting_mechanism == "majority_vote":
            outcome, results = majority_vote(self.proposal, votes)
        else:
            Exception("Voting mechanism not found")
        
        return outcome, results 

    
    # Display the results
    def display_results(self, result, voting_results, voting_rate):
        print("Participation rate: ", voting_rate)
        print(voting_results)
        print(voting_results[0][0] + ": " + str(voting_results[0][1])) 
        print(voting_results[1][0] + ": " + str(voting_results[1][1]))
        print("Winner: ", result)

    def calculate_GINI(self, x):
        sorted_x = sorted(x)
        n = len(sorted_x)
        cum_values = np.cumsum(sorted_x)
        scale = np.array(range(1, n+1)) / n
        print("GINI1: ", (n + 1 - 2 * np.sum(cum_values) / cum_values[-1]) / n)

        mad = np.abs(np.subtract.outer(x, x)).mean()
        # Relative mean absolute difference
        rmad = mad/np.mean(x)
        # Gini coefficient
        g = 0.5 * rmad
        print("GINI2: ", g)


# candidates list of 2 options
# each perferences is lift of 2 values indication the preference
class Proposal:
    def __init__(self, candidates, C_preferences, I_preferences, M_preferences):
        self.candidates = candidates
        self.C_preferences = C_preferences
        self.I_preferences = I_preferences
        self.M_preferences = M_preferences
        

        