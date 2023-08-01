from universe import Universe as un
from nodes import Node
# provide initial settings
def build_universe():
    
    avg_voting_rate=0.5
    wealth=0
    tokens_amount=10000
    wealth_dis_method="normal"
    participants = get_network_participants(tokens_amount, wealth_dis_method)
    universe = un.Universe(participants=participants, avg_voting_rate=avg_voting_rate, 
                           wealth=wealth, tokens_amount=tokens_amount, wealth_dis_method=wealth_dis_method, condition=[0, 0, 0])
    return universe

# add initial number of network participants
def get_network_participants(tokens_amount, wealth_dis_method):
    initial_n_type_M = 26
    initial_n_type_I = 16
    initial_n_type_C = 297

    participants = []

    for i in range(initial_n_type_M):
        participant_wealth = 0.057 * tokens_amount
        participant = Node.Node(type="M", community="M", incentive_mechanism="constant", 
                                wealth= participant_wealth, reputation=None, incentive_decision="best_interest")
        participants.append(participant)

    for i in range(initial_n_type_I):
        participant_wealth = 0.093 * tokens_amount
        participant = Node.Node(type="I", community="I", incentive_mechanism="constant", 
                                wealth= participant_wealth, reputation=None, incentive_decision="best_interest")
        participants.append(participant)
    
    for i in range(initial_n_type_C):
        participant_wealth = 0.005 * tokens_amount
        participant = Node.Node(type="C", community="C", incentive_mechanism="constant", 
                                wealth= participant_wealth, reputation=None, incentive_decision="best_interest")
        participants.append(participant)
        
    return participants

# add new participant to the network
def add_new_participants(universe, new_participant_type):
    if new_participant_type == "M":
        new_participant_wealth = 0.057 * universe.tokens_amount
    elif new_participant_type == "I":
        new_participant_wealth = 0.093 * universe.tokens_amount
    elif new_participant_type == "C":
        new_participant_wealth = 0.005 * universe.tokens_amount
    else:
        raise Exception("Invalid participant type")
    
    new_participant = Node.Node(type=new_participant_type, community=new_participant_type, incentive_mechanism="constant", 
                                wealth= new_participant_wealth, reputation=None, incentive_decision="best_interest")
    universe.participants.append(new_participant)
    
    return universe

def remove_participant(universe, type_participant):
    if type_participant == "M":
        M_type_participants = [p for p in universe.participants if p.type == "M"]
        to_be_removed = M_type_participants[0]
    elif type_participant == "I":
        I_type_participants = [p for p in universe.participants if p.type == "I"]
        to_be_removed = I_type_participants[0]
    elif type_participant == "C":
        C_type_participants = [p for p in universe.participants if p.type == "C"]
        to_be_removed = C_type_participants[0]
    else:
        raise Exception("Invalid participant type")
    
    # remove participant
    universe.participants.remove(to_be_removed)
    
    return universe