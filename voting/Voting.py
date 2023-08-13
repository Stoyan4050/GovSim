import numpy as np
from voting.voting_mechanisms import token_based_vote, quadratic_vote
from voting_decision import VotingDecision
from collections import Counter


# constants:
VOTING_INCENTIVE_THRESHOLD = 0.5

# Voting simulation class
# Candidates: list of candidates with wights, for voters to select the preferred candidate
class Voting:
    def __init__(self, proposal, network, voting_mechanism):
        self.proposal = proposal
        self.network = network
        self.voting_mechanism = voting_mechanism

    def vote(self):
        # Each voter votes for a candidate we save the votes in a list
        total_votes = []
        voted = 0
        abstain = 0
        voters = self.network.nodes
        # Each voter votes for a candidate
        for voter in voters:

            decision = self.get_decision_voter(voter)
            
            
            if decision != "abstain":
                voted+=1
                if self.voting_mechanism == "token_based_vote":
                    votes_node = token_based_vote(voter)
                elif self.voting_mechanism == "quadratic_vote":
                    votes_node = token_based_vote(voter)
                else:
                    Exception("Voting mechanism not found")
            else:
                abstain+=1
            
            for vote in range(int(votes_node)):
                total_votes.append(decision)

        GINI = self.calculate_GINI([p.wealth for p in self.voters])
        # Get the results of the voting mechanism and the voting decision
        voting_outcome, voting_summary = self.get_results(total_votes)
        voting_rate = voted/len(voters)
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
    
    # Determines the result of the voting
    def get_results(self, votes):
        # Count the votes per candidate
        vote_count = Counter(votes)
        # Decision based on the votes
        decision = vote_count.most_common(2)

        # Check if there is a tie
        if len(decision) > 1 and decision[0][1] == decision[1][1]:
            # It's a tie
            return "Tie", decision

        # Get the majority vote
        majority_vote = decision[0][0]
        if len(decision) == 1:
            if decision[0][0] == "Y":
                decision.append(("N", 0))
            elif decision[0][0] == "N":
                decision.append(("Y", 0))

        return majority_vote, decision

    
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
# each perferences is integer 0 or 1 to indicate if a group supports the proposal
class Proposal:
    def __init__(self, candidates, OC_preferences, IP_preferences, PT_preferences, CA_preferences):
        self.candidates = candidates
        self.OC_preferences = OC_preferences
        self.IP_preferences = IP_preferences
        self.PT_preferences = PT_preferences 
        self.CA_preferences = CA_preferences

        