from voting.Voting import Proposal
import random

# num_proposals: number of proposals
# distrib_per_group: tuple of 3 values indicating the distribution of the proposals per group
# preference_methodology: String indicating the preference methodology per group
def define_proposals(num_proposals, distrib_per_group, preference_methodology):
    all_proposals = []
    
    proposals_benefit_group_C = int(num_proposals * distrib_per_group[2])
    proposals_benefit_group_I = int(num_proposals * distrib_per_group[1])
    proposals_benefit_group_M = int(num_proposals * distrib_per_group[0])
    
    for i in range(proposals_benefit_group_C):
        C_preferences, I_preferences, M_preferences = binary_preferences("C")
        proposal = Proposal([1, 0], C_preferences, I_preferences, M_preferences)
        all_proposals.append(proposal)
    
    for i in range(proposals_benefit_group_I):
        C_preferences, I_preferences, M_preferences = binary_preferences("I")
        proposal = Proposal([1, 0], C_preferences, I_preferences, M_preferences)
        all_proposals.append(proposal)

    for i in range(proposals_benefit_group_M):
        C_preferences, I_preferences, M_preferences = binary_preferences("M")
        proposal = Proposal([1, 0], C_preferences, I_preferences, M_preferences)
        all_proposals.append(proposal)
    
    return all_proposals

def binary_preferences(proposals_benefit_group):
    if proposals_benefit_group == "C":
        C_preferences = [1, 0]
        # Randomly select from the list of choices
        I_preferences = random.choice([0, 1])
        M_preferences = [0, 1]
    elif proposals_benefit_group == "I":
        C_preferences = random.choice([0, 1])
        I_preferences = [1, 0]
        M_preferences = random.choice([0, 1])
    elif proposals_benefit_group == "M":
        C_preferences = [0, 1]
        I_preferences = random.choice([0, 1])
        M_preferences = [1, 0]
    else:
        raise Exception("Invalid group")
         

    return C_preferences, I_preferences, M_preferences
