from voting.Voting import Proposal
import numpy as np

# Count the number of proposals
proposal_counter = 0
def define_proposal(network):
    global proposal_counter

    # Increment the proposal counter
    proposal_counter += 1
    
    # Get the total token holding of each group
    sum_tokens_OC = np.round(np.sum([node.wealth for node in network.nodes if node.group == "OC"]), 4)
    sum_tokens_IP = np.round(np.sum([node.wealth for node in network.nodes if node.group == "IP"]), 4)
    sum_tokens_PT = np.round(np.sum([node.wealth for node in network.nodes if node.group == "PT"]), 4)
    sum_tokens_CA = np.round(np.sum([node.wealth for node in network.nodes if node.group == "CA"]), 4)

    # Get the total token holdings in the network
    total_token_holding = sum_tokens_OC + sum_tokens_IP + sum_tokens_PT + sum_tokens_CA

    # Compute the ratio of token holdings for each group
    # This ratio will be used to determine the probability that a node will benefit particular group
    ratio_OC = np.round(sum_tokens_OC/total_token_holding, 4)
    ratio_IP = np.round(sum_tokens_IP/total_token_holding, 4)
    ratio_PT = np.round(sum_tokens_PT/total_token_holding, 4)
    ratio_CA = 1 - ratio_OC - ratio_IP - ratio_PT   

    # Get the benefiting group
    # The benefiting group will have a value of 1 in the vector, while the others will have a value of 0  
    proposal_preferences = get_benefiting_group([ratio_OC, ratio_IP, ratio_PT, ratio_CA])

    # Create the proposal
    proposal = Proposal(["Y", "N"], OC_preferences=proposal_preferences[0], IP_preferences=proposal_preferences[1], 
                        PT_preferences=proposal_preferences[2], CA_preferences=proposal_preferences[3])

    return proposal

# Determine the benefiting group
# Generate a sequence of length 4 with one 1 and three 0s based on given probabilities
def get_benefiting_group(probs):
    """
    Generate a sequence of length 4 with one 1 and three 0s based on given probabilities.

    Parameters:
    - probs (list): A list of 4 probabilities.

    Returns:
    - list: A list containing one 1 and three 0s.
    """
    print("probs: ", probs)
    if len(probs) != 4:
        raise ValueError("The length of the probabilities list must be 4.")
    
    # Determine the position of the 1 based on the given probabilities
    position_of_one = np.random.choice(4, p=probs)
    
    # Create the sequence
    sequence = [0, 0, 0, 0]
    # Set the benefiting group to 1
    sequence[position_of_one] = 1
    
    print("Proposal: ", sequence)
    return sequence