from nodes import Node
from universe import Network
import numpy as np


# Provide initial settings
# Set initila tokens amount
def build_universe_network(tokens_amount = 10000):
    # Get initial participants
    participants, participants_per_group, total_token_amount_per_group = get_network_participants(tokens_amount)

    
    # Build initial network
    network = Network.Network(tokens_amount)
    for participant in participants:
        network.add_node(participant)
    
    # Add initial connections
    network.update_connections()

    return network, total_token_amount_per_group, participants_per_group

# Generate initial memebers/nodes of the network
def get_network_participants(tokens_amount_initial):
    
    # Set initial number of participants per group
    initial_n_type_OC = 15
    initial_n_type_IP = 40
    initial_n_type_PT = 150
    initial_n_type_CA = 12

    # Set initial tokens amount per group
    # Split the tokens evenly among the groups
    tokens_amount_per_group = {"OC": 0.25 * tokens_amount_initial, "IP": 0.25 * tokens_amount_initial, 
                               "PT": 0.25 * tokens_amount_initial, "CA": 0.25 * tokens_amount_initial}
    
    participants_per_group = {"OC": [], "IP": [], "PT": [], "CA": []}

    participants = []

    # Distirbute tokens for each memeber of the OC group using the Pareto distribution (80-20 rule)
    tokens_distribution_OC = distirbute_tokens_Pareto(tokens_amount_per_group["OC"], initial_n_type_OC)
    for i in range(initial_n_type_OC):
        participant_wealth = tokens_distribution_OC[i]
        participant = Node.Node(wealth=participant_wealth, group="OC", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["OC"].append(participant)

    # Distirbute tokens for each memeber of the IP group using the Pareto distribution (80-20 rule)
    tokens_distribution_IP = distirbute_tokens_Pareto(tokens_amount_per_group["IP"], initial_n_type_IP)
    for i in range(initial_n_type_IP):
        participant_wealth = tokens_distribution_IP[i]
        participant = Node.Node(wealth=participant_wealth, group="IP", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["IP"].append(participant)
    
    # Distirbute tokens for each memeber of the PT group using the Pareto distribution (80-20 rule)
    tokens_distribution_PT = distirbute_tokens_Pareto(tokens_amount_per_group["PT"], initial_n_type_PT)
    for i in range(initial_n_type_PT):
        participant_wealth = tokens_distribution_PT[i]
        participant = Node.Node(wealth=participant_wealth, group="PT", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["PT"].append(participant)
    
    # Distirbute tokens for each memeber of the CA group using the Pareto distribution (80-20 rule)
    tokens_distribution_CA = distirbute_tokens_Pareto(tokens_amount_per_group["CA"], initial_n_type_CA)
    for i in range(initial_n_type_CA):
        participant_wealth = tokens_distribution_CA[i]
        participant = Node.Node(wealth=participant_wealth, group="CA", incentive_mechanism="constant")
        participants.append(participant)
        participants_per_group["CA"].append(participant)
    
    total_token_amount_per_group = tokens_amount_per_group.copy()
    
    return participants, participants_per_group, total_token_amount_per_group

# Generate Pareto distributed values
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

