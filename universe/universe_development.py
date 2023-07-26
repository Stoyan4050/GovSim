import Universe as un
from nodes import Node
# provide initial settings
def build_universe():
    
    avg_voting_rate=0.5
    wealth=0
    tokens_amount=1000
    wealth_dis_method="normal"
    participants = get_network_participants(wealth, wealth_dis_method)
    universe = un.Universe(participants=participants, avg_voting_rate=avg_voting_rate, 
                           wealth=wealth, tokens_amount=tokens_amount, wealth_dis_method=wealth_dis_method)
    return universe

# add initial number of network participants
def get_network_participants(tokens_amount, wealth_dis_method):
    initial_n_type_M = 100
    initial_n_type_I = 200
    initial_n_type_C = 600

    participants = []

    for i in range(initial_n_type_M):
        participant_wealth = 0.003 * tokens_amount
        participant = Node.Node(type="M", community="M", incentive_mechanism=None, 
                                wealth= participant_wealth, reputation=None, incentive_decision="best_interest")
        participants.append(participant)

    for i in range(initial_n_type_I):
        participant_wealth = 0.001 * tokens_amount
        participant = Node.Node(type="I", community="I", incentive_mechanism=None, 
                                wealth= participant_wealth, reputation=None, incentive_decision="best_interest")
        participants.append(participant)
    
    for i in range(initial_n_type_C):
        participant_wealth = 0.0005 * tokens_amount
        participant = Node.Node(type="C", community="C", incentive_mechanism=None, 
                                wealth= participant_wealth, reputation=None, incentive_decision="best_interest")
        participants.append(participant)
    
    return participants