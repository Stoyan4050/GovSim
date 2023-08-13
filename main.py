import numpy as np
from universe import build_universe
from voting import voting_development, Voting
from voting_decision import VotingDecision
import random

PARTICIPANTS = 1000
VOTING_METHOD = 'simple_majority'
VOTING_INCENTIVE = 'none'
AVG_VOTING_RATE = 0.5
WEALTH = 1000000
TOKENS_AMOUNT = 1000000
RANDOM_SEED = 42
network_update = [0, 0, 0]

num_proposals = 5
# add a probability of leaving
# fitness network
# block models
# number of clusters/connected components

def main():
    
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    # Create new universe
    universe, network = build_universe.build_universe_network()
    print("Participants: ", len(universe.participants))
    print("Network Connections: ", )
    #print("Participants per group:", universe.participants_per_group)

    network.visualize_network()

    simulate_voting(universe, network, num_proposals)

def simulate_voting(universe, network, num_proposals):

    for i in range(num_proposals):

        proposal = voting_development.define_proposal(network)
        print("Proposals: ", (proposal))

        # Voting mechanism can be: token_based_vote, quadratic_vote
        voting = Voting.Voting(proposal, network, voting_mechanism="token_based_vote")

        result = voting.vote()
        if result == "Y":
            if proposal.M_preferences[0] == 1:
                universe.condition[0]+=0.1
                ovr_condition[0]+=0.1
            if proposal.I_preferences[0] == 1:
                universe.condition[1]+=0.1
                ovr_condition[1]+=0.1
            if proposal.C_preferences[0] == 1:
                universe.condition[2]+=0.1
                ovr_condition[2]+=0.1
        else:
            if proposal.M_preferences[0] == 1:
                universe.condition[0]-=0.1
                ovr_condition[0]-=0.1
            if proposal.I_preferences[0] == 1:
                universe.condition[1]-=0.1
                ovr_condition[1]-=0.1
            if proposal.C_preferences[0] == 1:
                universe.condition[2]-=0.1
                ovr_condition[2]-=0.1

        print("Universe status: ", universe.condition)
        print("Universe status2: ", ovr_condition)

        update_network(universe, universe.condition)


def update_network(universe, condition):
    global ovr_condition
    thresh = 0.2

    if ovr_condition[0] >= thresh:
        print("ADD PARTICIPANT VOTING M") 

        build_universe.add_new_participants(universe, "M")
        #print("New memeber: ", len(universe.participants))
        ovr_condition[0]-=thresh
    
    if ovr_condition[0] <= -1*thresh:
        print("REMOVE PARTICIPANT VOTING M") 

        build_universe.remove_participant(universe, "M")
        ovr_condition[0]+=thresh

    if ovr_condition[1] >= thresh:
        print("ADD PARTICIPANT VOTING I") 

        build_universe.add_new_participants(universe, "I")
        #print("New memeber: ", len(universe.participants))
        ovr_condition[1]-=thresh

    if ovr_condition[1] <= -1*thresh:
        print("REMOVE PARTICIPANT VOTING I") 

        build_universe.remove_participant(universe, "I")
        ovr_condition[1]+=thresh

    if ovr_condition[2] >= thresh:
        print("ADD PARTICIPANT VOTING C") 

        build_universe.add_new_participants(universe, "C")
        #print("New memeber: ", len(universe.participants))
        ovr_condition[2]-=thresh

    elif ovr_condition[2] <= -1*thresh:
        print("REMOVE PARTICIPANT VOTING C") 

        build_universe.remove_participant(universe, "C")
        ovr_condition[2]+=thresh

    M_participants = len([p for p in universe.participants if p.type == "M"])
    I_participants = len([p for p in universe.participants if p.type == "I"])
    C_participants = len([p for p in universe.participants if p.type == "C"])

    print("M: ", M_participants, "I: ", I_participants, "C: ", C_participants)

    add_participant_ratio(M_participants, I_participants, C_participants, universe, universe.condition)
    remove_participants_ratio(M_participants, I_participants, C_participants, universe)



if __name__ == '__main__':
    main()