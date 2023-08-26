import numpy as np
from voting.voting_mechanisms import token_based_vote, quadratic_vote, reputation_vote
from voting_decision import VotingDecision
from collections import Counter
from voting_incentives import Incentive

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

        GINI_VOTERS = []

        # We resset the last preferences of the voters
        voters = self.reset_voters_preferences(voters)

        # Set the last preferences for the benefiting voters
        # Returns list of the voters that have not voted
        voters = VotingDecision.VotingDecision(voters, self.proposal).generate_voting_decision_benefit()

        # Set the last preferences for the neutral voters
        # Returns list of the voters that have not voted
        voters = VotingDecision.VotingDecision(voters, self.proposal).generate_voting_decision_neutral()

        # Set the last preferences for the voters which connections are influenced by the proposal
        # Returns list of the voters that have not voted
        voters = VotingDecision.VotingDecision(voters, self.proposal).generate_voting_decision_connections()

        # Check if all voters have voted
        if len(voters) != 0:
            Exception("Issue with the voting decision")

        incentive = Incentive.Incentive(self.network, self.proposal)
        incentive.get_probability_vote()

        # Each voter votes for a candidate we save the votes in a list
        for voter in self.network.nodes:
            # Get the incentive decision of the voter
            # Determine if the voter will vote or abstain
            incentive_decision = self.get_voting_incentive_decision(voter)
            #print("Incentive decision: ", incentive_decision)

            # Consider the case when voter votes
            if incentive_decision != "abstain":
                # Count the number of voters that voted
                voted+=1

                # Get the number of votes from the voter based on the chosen voting mechanism
                if self.voting_mechanism == "token_based_vote":
                    votes_node = token_based_vote(voter)
                elif self.voting_mechanism == "quadratic_vote":
                    votes_node = quadratic_vote(voter)
                elif self.voting_mechanism == "reputation_vote":
                    votes_node = reputation_vote(voter)
                else:
                    Exception("Voting mechanism not found")
                
                # Get the decision of the voter based on the last preference
                decision = self.get_decision_from_preference_voter(voter)
                GINI_VOTERS.append(np.floor(votes_node))

                for vote in range(int(np.floor(votes_node))):
                    total_votes.append(decision)

            else:
                abstain+=1
                if incentive.incentive_mechanism == "penalty":
                   incentive.penalty_effect_wealth(voter, np.sum([node.wealth for node in self.network.nodes]))


        GINI = self.calculate_GINI(GINI_VOTERS)
        # Get the results of the voting mechanism and the voting decision
        voting_outcome, voting_summary = self.get_results(total_votes)
        voting_rate = voted/len(self.network.nodes)
        # Display the results
        self.display_results(voting_outcome, voting_summary, voting_rate=voting_rate)
        
        return voting_outcome, GINI, voting_rate

    # Determine the decision of the voter based on the last preference
    def get_decision_from_preference_voter(self, voter):

        if voter.last_preference > 0.5:
            decision = "Y"
        else:
            decision = "N"

        #print("Voter: ", voter.group, " - ", voter.last_preference, " Decision: ", decision)

        return decision

    # Reset the last preferences of the voters    
    def reset_voters_preferences(self, voters):
        for voter in voters:
            voter.last_preference = None

        return voters
    
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
        #scale = np.array(range(1, n+1)) / n
        gini = (n + 1 - 2 * np.sum(cum_values) / cum_values[-1]) / n

        print("GINI: ", (n + 1 - 2 * np.sum(cum_values) / cum_values[-1]) / n)

        return gini

    def get_voting_incentive_decision(self, voter):
        #print("Voter: ", voter.group, " - ", voter.probability_vote)
        if voter.probability_vote > VOTING_INCENTIVE_THRESHOLD:
            return "vote"
        else:
            return "abstain"

# candidates list of 2 options
# each perferences is integer 0 or 1 to indicate if a group supports the proposal
class Proposal:
    def __init__(self, candidates, OC_preferences, IP_preferences, PT_preferences, CA_preferences):
        self.candidates = candidates
        self.OC_preferences = OC_preferences
        self.IP_preferences = IP_preferences
        self.PT_preferences = PT_preferences 
        self.CA_preferences = CA_preferences

        