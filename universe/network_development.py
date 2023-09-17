import numpy as np
from nodes import Node
import random

# Variables to store the overall satisfaction level and the number of participants
OVERALL_SATISFACTION = []
NUMNBER_PARTICIPANTS = []

# Update network after every iteration
def update_network(network, voting_result, num_proposals, total_token_amount_per_group):
    # Variable to store the satisfaction level of the group
    SATISFACTION_LEVEL = {"OC": 0, "IP": 0, "PT": 0, "CA": 0}

    global OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS


    # We update the preferences of the nodes based on the last voting outcome
    # If outcome is "N" then the preeferences of the nodes are the opposite of the computed one
    network = update_preferences_for_voting_decision(network, voting_result)

    # Update the satisfaction level of the group
    SATISFACTION_LEVEL["OC"] = compute_satisfaction_level_group(network, "OC")
    SATISFACTION_LEVEL["IP"] = compute_satisfaction_level_group(network, "IP")
    SATISFACTION_LEVEL["PT"] = compute_satisfaction_level_group(network, "PT")
    SATISFACTION_LEVEL["CA"] = compute_satisfaction_level_group(network, "CA")

    # Update the network based on the satisfaction level of the group
    network = add_nodes_to_network_satisfaction(network, num_proposals, SATISFACTION_LEVEL, total_token_amount_per_group)
    # Remove nodes from the network if they are not satisfied
    network = remove_nodes_network_satisfaction(network)
    # Update the connections of the network
    network.update_connections()
    # Remove nodes from the network if they have no connections
    network = remove_nodes_from_network_conn(network)

    # Compute the overall satisfaction level in the network
    overall_satisfaction = 0
    for node in network.nodes:
        if len(node.preferences) >= 10:
            overall_satisfaction += np.mean(node.preferences[-10:])
            #print(node.group, node.preferences[-10:])


    overall_satisfaction = overall_satisfaction / len(network.nodes)

    OVERALL_SATISFACTION.append(overall_satisfaction)
    NUMNBER_PARTICIPANTS.append(len(network.nodes))

    return OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS, SATISFACTION_LEVEL

# Update the preferences of the nodes based on the last voting outcome
# If the proposal passed with "Y" then leave the preferences as they are
# If the proposal failed with "N" then the preferences of the nodes are the opposite of the computed one
def update_preferences_for_voting_decision(network, voting_result):
    if voting_result == "N":
        for node in network.nodes:
            node.last_preference = 1 - node.last_preference
            node.preferences[-1] = node.last_preference

    return network      


# Determine the overall satisfaction level of the group.
def compute_satisfaction_level_group(network, group):
    # Get nodes for particular group
    nodes_in_group = [node for node in network.nodes if node.group == group]
    
    M = len(nodes_in_group)
    total_preference = 0

    # Compute the total sum of preferences for the group
    for node in nodes_in_group:
        if len(node.preferences) >= 10:
            total_preference += np.sum(node.preferences[-10:])  # Sum the last 10 votes for the node

    # Compute the average preference for the group
    P_group = total_preference / (10 * M)

    return P_group


# We add a new node to the network if the satisfaction level of the group is above 0.6
def add_nodes_to_network_satisfaction(network, num_proposals, SATISFACTION_LEVEL, total_token_amount_per_group): 
    if num_proposals >= 10:
        # We add a new participant if the satisfaction level of the group is above 0.6

        if SATISFACTION_LEVEL["OC"] > 0.6:
            network = add_new_node_network(network, "OC", total_token_amount_per_group)
        if SATISFACTION_LEVEL["IP"] > 0.6:
            network = add_new_node_network(network, "IP", total_token_amount_per_group)
        if SATISFACTION_LEVEL["PT"] > 0.6:
            network = add_new_node_network(network, "PT", total_token_amount_per_group)
        if SATISFACTION_LEVEL["CA"] > 0.6:
            network = add_new_node_network(network, "CA", total_token_amount_per_group)   

    return network

# Generate and add node to network
def add_new_node_network(network, group, total_token_amount_per_group):
    """
    Add a new node to the network.

    Parameters:
    - network (Network): The network object.
    - group (str): The group of the new node.
    """
    # Generate a random wealth value for the new node based on the Pareto distribution
    # Similar to the initial distribution of the tokens per nodes
    node_wealth = generate_scaled_pareto_value() * total_token_amount_per_group[group]

    # Add a new node to the network
    new_node = Node.Node(wealth=node_wealth, group=group, incentive_mechanism="constant")
    
    # Add the new node to the universe
    network.add_node(new_node)
    network.tokens_amount += node_wealth

    print("Added: ", group, " - ", node_wealth, " - ", len(network.nodes))
    return network

# Remove nodes when not satisfied
def remove_nodes_network_satisfaction(network):
    all_nodes = network.nodes
    for node in all_nodes:
        if len(node.preferences) >= 10:
            # If the average of the last 10 preferences is below 0.4 then remove the node
            if np.mean(node.preferences[-10:]) < 0.4:
                print("Remove node: ", node.group)
                network.remove_node(node)
                network.tokens_amount -= node.wealth
    return network

# Remove nodes from the network if they have no connections
def remove_nodes_from_network_conn(network):
    all_nodes = network.nodes
    for node in all_nodes:
        # If node does not have connection, remove the node
        if len(node.connections) == 0:
            print("Node removed no connections: ", node.group)

            network.remove_node(node)
            network.tokens_amount -= node.wealth
   
    return network


def generate_scaled_pareto_value(alpha=1.16):
    """
    Generate random values from the Pareto distribution,
    and scale the first value based on the sum of all values to be in [0, 1].
    
    Parameters:
    - alpha (float): The shape parameter of the Pareto distribution.
    - num_values (int): The number of random values to generate from the Pareto distribution.
    
    Returns:
    - float: The first value from the Pareto distribution, scaled to [0, 1].
    - list: The list of all generated Pareto values, scaled to sum up to 1.
    """
    # Generate random values from the Pareto distribution
    pareto_values = np.random.pareto(alpha, 100)
    
    # Normalize the values so that they sum up to 1
    normalized_values = pareto_values / np.max(pareto_values)
    
    # Take the first normalized value
    scaled_first_value = normalized_values[0]
    
    return scaled_first_value