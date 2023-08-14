import numpy as np
from nodes import Node
import random

OVERALL_SATISFACTION = []
NUMNBER_PARTICIPANTS = []

def update_network(universe, network, voting_result, num_proposals):
    SATISFACTION_LEVEL = {"OC": 0, "IP": 0, "PT": 0, "CA": 0}

    global OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS
    """
    Update the network after voting.

    Parameters:
    - universe (Universe): The universe object.
    - network (Network): The network object.
    - voting_result (str): The voting result, either "Y" or "N".
    """

    # We update the preferences of the nodes based on the last voting outcome
    # If outcome is "N" then the preeferences of the nodes are the opposite of the computed one
    network = update_preferences_for_voting_decision(network, voting_result)

    # Update the satisfaction level of the group
    SATISFACTION_LEVEL["OC"] = compute_satisfaction_level_group(network, "OC")
    SATISFACTION_LEVEL["IP"] = compute_satisfaction_level_group(network, "IP")
    SATISFACTION_LEVEL["PT"] = compute_satisfaction_level_group(network, "PT")
    SATISFACTION_LEVEL["CA"] = compute_satisfaction_level_group(network, "CA")

    network, universe = add_nodes_to_network_satisfaction(universe, network, num_proposals, SATISFACTION_LEVEL)
    network, universe = remove_nodes_network_satisfaction(network, universe)
    network.update_connections()
    network, universe = remove_nodes_from_network_conn(network, universe)

    overall_satisfaction = 0
    for node in network.nodes:
        if len(node.preferences) >= 10:
            overall_satisfaction += np.mean(node.preferences[-10:])


    overall_satisfaction = overall_satisfaction / len(network.nodes)

    OVERALL_SATISFACTION.append(overall_satisfaction)
    NUMNBER_PARTICIPANTS.append(len(network.nodes))

    return OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS, SATISFACTION_LEVEL

def update_preferences_for_voting_decision(network, voting_result):
    if voting_result == "N":
        for node in network.nodes:
            node.last_preference = 1 - node.last_preference
            node.preferences[-1] = node.last_preference

    return network      


# Determine the overall satisfaction level of the group.
def compute_satisfaction_level_group(network, group):
    nodes_in_group = [node for node in network.nodes if node.group == group]
    
    M = len(nodes_in_group)
    total_preference = 0

    for node in nodes_in_group:
        if len(node.preferences) >= 10:
            total_preference += np.sum(node.preferences[-10:])  # Sum the last 10 votes for the node

    P_group = total_preference / (10 * M)

    #print("Satisfaction level ", group, ": ", P_group)
    return P_group

# We add a new node to the network if the satisfaction level of the group is above 0.6
def add_nodes_to_network_satisfaction(universe, network, num_proposals, SATISFACTION_LEVEL): 
    if num_proposals >= 10:
        # We add a new participant if the satisfaction level of the group is above 0.6

        if SATISFACTION_LEVEL["OC"] > 0.6:
            network, universe = add_new_node_network(network, universe, "OC")
        elif SATISFACTION_LEVEL["IP"] > 0.6:
            network, universe = add_new_node_network(network, universe, "IP")
        elif SATISFACTION_LEVEL["PT"] > 0.6:
            network, universe = add_new_node_network(network, universe, "PT")
        elif SATISFACTION_LEVEL["CA"] > 0.6:
            network, universe = add_new_node_network(network, universe, "CA")   

    return network, universe

# Generate and add node to network
def add_new_node_network(network, universe, group):
    """
    Add a new node to the network.

    Parameters:
    - network (Network): The network object.
    - universe (Universe): The universe object.
    - group (str): The group of the new node.
    """
    # def add_new_node(self, group, incentive_mechanism, min_wealth_group, max_wealth_group):
    node_wealth = random_wealth_value(np.min([node.wealth for node in network.nodes if node.group == group]), 
                                      np.max([node.wealth for node in network.nodes if node.group == group]))

    # Add a new node to the network
    new_node = Node.Node(wealth=node_wealth, group=group, incentive_mechanism="constant")
    
    # Add the new node to the universe
    network.add_node(new_node)
    universe.tokens_amount += node_wealth

    print("Added: ", group, " - ", node_wealth, " - ", len(network.nodes))
    return network, universe

# Remove nodes when not satisfied
def remove_nodes_network_satisfaction(network, universe):
    all_nodes = network.nodes
    for node in all_nodes:
        if len(node.preferences) >= 10:
            if np.mean(node.preferences[-10:]) < 0.4:
                print("Remove node")
                network.remove_node(node)
                universe.tokens_amount -= node.wealth
    return network, universe

# Remove nodes from the network if they have no connections
def remove_nodes_from_network_conn(network, universe):
    all_nodes = network.nodes
    for node in all_nodes:
        if len(node.connections) == 0:
            print("Node removed no connections")

            network.remove_node(node)
            universe.tokens_amount -= node.wealth
   
    return network, universe

def random_wealth_value(min_wealth, max_wealth):
    """
    Generate a random float between min_wealth and max_wealth.

    Parameters:
    - min_wealth (float): Lower bound.
    - max_wealth (float): Upper bound.

    Returns:
    - float: A random float between a and b.
    """
    return random.uniform(min_wealth, max_wealth)