import numpy as np
from universe import build_universe
from voting import voting_development, Voting
from voting_decision import VotingDecision
import random
import matplotlib.pyplot as plt
from universe import network_development

VOTING_METHOD = 'simple_majority'
AVG_VOTING_RATE = 0.5
WEALTH = 1000000
TOKENS_AMOUNT = 1000000
RANDOM_SEED = 30
network_update = [0, 0, 0]

num_proposals = 100

GINI_HISTORY = []

def main():
    
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    # Create new universe

    universe, network = build_universe.build_universe_network()
    print("Participants: ", len(universe.participants))

    # Print participants per group
    for key, participants in universe.participants_per_group.items():
        print(f"{key}: {len(participants)} participants")    
        
    network.visualize_network()

    simulate_voting(universe, network, num_proposals)


def simulate_voting(universe, network, num_proposals):
    GINI_HISTORY = []
    satisfaction_level_history = {"OC": [], "IP": [], "PT": [], "CA": []}
    proposal_count = 0
    for i in range(num_proposals):
        proposal_count += 1
        proposal = voting_development.define_proposal(network)

        # Voting mechanism can be: token_based_vote, quadratic_vote
        voting = Voting.Voting(proposal, network, universe, voting_mechanism="token_based_vote")

        result, GINI = voting.vote()

        GINI_HISTORY.append(GINI)

        # plt.plot(GINI_HISTORY)
        # plt.show()

        OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS, SATISFACTION_LEVEL = network_development.update_network(
                                                                         universe, network, result, proposal_count)

        satisfaction_level_history["OC"].append(SATISFACTION_LEVEL["OC"])
        satisfaction_level_history["IP"].append(SATISFACTION_LEVEL["IP"])
        satisfaction_level_history["PT"].append(SATISFACTION_LEVEL["PT"])
        satisfaction_level_history["CA"].append(SATISFACTION_LEVEL["CA"])
        #print("OVERALL SATISFACTION: ", OVERALL_SATISFACTION)
        #print("NUMBER OF PARTICIPANTS: ", NUMNBER_PARTICIPANTS)
        #print("SATISFACTION LEVEL GROUP: ", SATISFACTION_LEVEL)
        #network.visualize_network()

        print("Result: ", result)

        #update_network(universe, universe.condition)
    network.visualize_network()
    plt.plot(GINI_HISTORY)
    plt.title("GINI")
    plt.show()

    plt.plot(OVERALL_SATISFACTION)
    plt.title("Overall satisfaction")
    plt.show()

    plt.plot(NUMNBER_PARTICIPANTS)
    plt.title("Number of participants")
    plt.show()

    plt.plot(satisfaction_level_history["OC"])
    plt.plot(satisfaction_level_history["IP"])
    plt.plot(satisfaction_level_history["PT"])
    plt.plot(satisfaction_level_history["CA"])
    plt.title("Satisfaction level Group")
    plt.legend(["OC", "IP", "PT", "CA"])
    plt.show()
    
    #print("GINI HISTORY: ", GINI_HISTORY)



if __name__ == '__main__':
    main()