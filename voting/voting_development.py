from voting.Voting import Proposal
import numpy as np

# num_proposals: number of proposals
proposal_counter = 0
def define_proposal(network):
    global proposal_counter

    proposal_counter += 1

    sum_tokens_OC = np.round(np.sum([node.wealth for node in network.nodes if node.group == "OC"]), 4)
    sum_tokens_IP = np.round(np.sum([node.wealth for node in network.nodes if node.group == "IP"]), 4)
    sum_tokens_PT = np.round(np.sum([node.wealth for node in network.nodes if node.group == "PT"]), 4)
    sum_tokens_CA = np.round(np.sum([node.wealth for node in network.nodes if node.group == "CA"]), 4)

    total_token_holding = sum_tokens_OC + sum_tokens_IP + sum_tokens_PT + sum_tokens_CA

    # compute ratios:
    ratio_OC = np.round(sum_tokens_OC/total_token_holding, 4)
    ratio_IP = np.round(sum_tokens_IP/total_token_holding, 4)
    ratio_PT = np.round(sum_tokens_PT/total_token_holding, 4)
    ratio_CA = 1 - ratio_OC - ratio_IP - ratio_PT        
    proposal_preferences = get_benefiting_group([ratio_OC, ratio_IP, ratio_PT, ratio_CA])

    #print("Proposal preferences: ", proposal_preferences)


    proposal = Proposal(["Y", "N"], OC_preferences=proposal_preferences[0], IP_preferences=proposal_preferences[1], 
                        PT_preferences=proposal_preferences[2], CA_preferences=proposal_preferences[3])

    return proposal


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
    sequence[position_of_one] = 1
    
    print("Proposal: ", sequence)
    return sequence