from nodes import Node
from universe import Network
import numpy as np


# provide initial settings
def build_universe_network():
    tokens_amount = 1000
    participants, participants_per_group, total_token_amount_per_group = get_network_participants(tokens_amount)
    # universe = un.Universe(participants=participants, avg_voting_rate=avg_voting_rate, 
    #                        tokens_amount=tokens_amount, participants_per_group=participants_per_group)
    
    #build initila network
    network = Network.Network(tokens_amount)
    for participant in participants:
        network.add_node(participant)
    
    # add initial connections
    network.update_connections()

    return network, total_token_amount_per_group, participants_per_group

# generate initial memebers/nodes of the network
def get_network_participants(tokens_amount_initial):
    
    initial_n_type_OC = 15 #15
    initial_n_type_IP = 40 #40
    initial_n_type_PT = 15 #150
    initial_n_type_CA = 12 #12

    tokens_amount_per_group = {"OC": 0.25 * tokens_amount_initial, "IP": 0.25 * tokens_amount_initial, 
                               "PT": 0.25 * tokens_amount_initial, "CA": 0.25 * tokens_amount_initial}
    
    participants_per_group = {"OC": [], "IP": [], "PT": [], "CA": []}

    participants = []

    tokens_distribution_OC = distirbute_tokens_Pareto(tokens_amount_per_group["OC"], initial_n_type_OC)
    for i in range(initial_n_type_OC):
        participant_wealth = tokens_distribution_OC[i]
        participant = Node.Node(wealth=participant_wealth, group="OC", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["OC"].append(participant)

    tokens_distribution_IP = distirbute_tokens_Pareto(tokens_amount_per_group["IP"], initial_n_type_IP)
    for i in range(initial_n_type_IP):
        participant_wealth = tokens_distribution_IP[i]
        participant = Node.Node(wealth=participant_wealth, group="IP", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["IP"].append(participant)
    
    tokens_distribution_PT = distirbute_tokens_Pareto(tokens_amount_per_group["PT"], initial_n_type_PT)
    for i in range(initial_n_type_PT):
        participant_wealth = tokens_distribution_PT[i]
        participant = Node.Node(wealth=participant_wealth, group="PT", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["PT"].append(participant)

    tokens_distribution_CA = distirbute_tokens_Pareto(tokens_amount_per_group["CA"], initial_n_type_CA)
    for i in range(initial_n_type_CA):
        participant_wealth = tokens_distribution_CA[i]
        participant = Node.Node(wealth=participant_wealth, group="CA", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["CA"].append(participant)
    
    total_token_amount_per_group = tokens_amount_per_group.copy()
    
    return participants, participants_per_group, total_token_amount_per_group


def distirbute_tokens_Pareto(tokens_amount, num_participants):
    """
    Distribute tokens among participants following the Pareto distribution.

    Parameters:
    - tokens_amount (int): Total number of tokens to be distributed.
    - num_participants (int): Number of participants.
    - alpha (float): Pareto distribution parameter. Default is 1.16.

    Returns:
    - list: List of tokens for each participant.
    """
    alpha = 1.16

    # Generate Pareto distributed values
    pareto_values = np.random.pareto(alpha, num_participants)
    
    # Normalize the values so that they sum up to total_tokens
    normalized_values = pareto_values / pareto_values.sum() * tokens_amount
    
    # Round the values to 4 decimal places
    token_distribution = np.round(normalized_values, 4)
    
    return token_distribution.tolist()

