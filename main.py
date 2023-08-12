import numpy as np
from universe import universe_development
from voting import voting_development, Voting
from voting_decision import VotingDecision

PARTICIPANTS = 1000
VOTING_METHOD = 'simple_majority'
VOTING_INCENTIVE = 'none'
WEALTH_DISTRIBUTION = 'uniform'
AVG_VOTING_RATE = 0.5
WEALTH = 1000000
TOKENS_AMOUNT = 1000000
RANDOM_SEED = 42
network_update = [0, 0, 0]

# add a probability of leaving
# fitness network
# block models
# number of clusters/connected components

def main():
    
    np.random.seed(RANDOM_SEED)
    # Create new universe
    universe = universe_development.build_universe()
    print("Participants: ", len(universe.participants))
    proposals = voting_development.define_proposals(num_proposals=50, distrib_per_group=(0.2, 0.2, 0.2), preference_methodology="binary")
    print("Proposals: ", len(proposals))
    simulate_voting(universe, proposals)

RATIO_PARTICIPANTS = [11.4, 1, 18.55, 0.6, 1.6]
ovr_condition = [0, 0, 0]

def simulate_voting(universe, proposals):
    for proposal in proposals:
        voting = Voting.Voting(proposal, universe.participants, voting_mechanism="majority_vote")
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

        universe_development.add_new_participants(universe, "M")
        #print("New memeber: ", len(universe.participants))
        ovr_condition[0]-=thresh
    
    if ovr_condition[0] <= -1*thresh:
        print("REMOVE PARTICIPANT VOTING M") 

        universe_development.remove_participant(universe, "M")
        ovr_condition[0]+=thresh

    if ovr_condition[1] >= thresh:
        print("ADD PARTICIPANT VOTING I") 

        universe_development.add_new_participants(universe, "I")
        #print("New memeber: ", len(universe.participants))
        ovr_condition[1]-=thresh

    if ovr_condition[1] <= -1*thresh:
        print("REMOVE PARTICIPANT VOTING I") 

        universe_development.remove_participant(universe, "I")
        ovr_condition[1]+=thresh

    if ovr_condition[2] >= thresh:
        print("ADD PARTICIPANT VOTING C") 

        universe_development.add_new_participants(universe, "C")
        #print("New memeber: ", len(universe.participants))
        ovr_condition[2]-=thresh

    elif ovr_condition[2] <= -1*thresh:
        print("REMOVE PARTICIPANT VOTING C") 

        universe_development.remove_participant(universe, "C")
        ovr_condition[2]+=thresh

    M_participants = len([p for p in universe.participants if p.type == "M"])
    I_participants = len([p for p in universe.participants if p.type == "I"])
    C_participants = len([p for p in universe.participants if p.type == "C"])

    print("M: ", M_participants, "I: ", I_participants, "C: ", C_participants)

    add_participant_ratio(M_participants, I_participants, C_participants, universe, universe.condition)
    remove_participants_ratio(M_participants, I_participants, C_participants, universe)


def add_participant_ratio(M_participants, I_participants, C_participants, universe, ovr_condition):

    if M_participants < np.ceil(C_participants / RATIO_PARTICIPANTS[0]) - 1 and ovr_condition[0] >= 0:
        print("ADD PARTICIPANT RATIO M") 
        universe_development.add_new_participants(universe, "M")
    
    if I_participants < np.ceil(C_participants / RATIO_PARTICIPANTS[2]) - 1 and ovr_condition[1] >= 0:
        print("ADD PARTICIPANT RATIO I") 
        
        universe_development.add_new_participants(universe, "I")

    if M_participants < np.ceil(I_participants / RATIO_PARTICIPANTS[3]) - 1 and ovr_condition[0] >= 0:
        print("ADD PARTICIPANT RATIO M") 
       
        universe_development.add_new_participants(universe, "M")

    if I_participants < np.ceil(M_participants / RATIO_PARTICIPANTS[4]) - 1 and ovr_condition[1] >= 0:
        print("ADD PARTICIPANT RATIO I") 
        
        universe_development.add_new_participants(universe, "I")

    if C_participants < np.ceil(I_participants * RATIO_PARTICIPANTS[2]) and ovr_condition[2] >= 0:
        print("ADD PARTICIPANT RATIO C") 
        
        universe_development.add_new_participants(universe, "C")

    if C_participants < np.ceil(M_participants * RATIO_PARTICIPANTS[0]) and ovr_condition[2] >= 0:
        print("ADD PARTICIPANT RATIO C") 
        
        universe_development.add_new_participants(universe, "C")

def remove_participants_ratio(M_participants, I_participants, C_participants, universe):


    if I_participants > np.ceil(C_participants / RATIO_PARTICIPANTS[2]):
        print("REMOVE PARTICIPANT RATIO I")         
        universe_development.remove_participant(universe, "I")

    if M_participants > np.ceil(I_participants / RATIO_PARTICIPANTS[3]):
        print("REMOVE PARTICIPANT RATIO M")     
        universe_development.remove_participant(universe, "M")

    if I_participants > np.ceil(M_participants / RATIO_PARTICIPANTS[4]):
        print("REMOVE PARTICIPANT RATIO I")     
        universe_development.remove_participant(universe, "I")

    if C_participants > np.ceil(I_participants * RATIO_PARTICIPANTS[2]):
        print("REMOVE PARTICIPANT RATIO C")     
        universe_development.remove_participant(universe, "C")

    if C_participants > np.ceil(M_participants * RATIO_PARTICIPANTS[0]):
        print("REMOVE PARTICIPANT RATIO C")     
        universe_development.remove_participant(universe, "C")


if __name__ == '__main__':
    main()