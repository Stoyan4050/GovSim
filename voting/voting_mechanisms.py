from collections import Counter

# Compute Majority Vote decision  
def majority_vote(proposal, votes):
    # Count the votes per candidate
    vote_count = Counter(votes)
    # Decision based on the votes
    decision = vote_count.most_common(2)

    # Check if there is a tie
    if len(decision) > 1 and decision[0][1] == decision[1][1]:
        # It's a tie
        return "Tie", decision

    # Get the majority vote
    majority_vote = decision[0][0]
    if len(decision) == 1:
        if decision[0][0] == "Y":
            decision.append(("N", 0))
        elif decision[0][0] == "N":
            decision.append(("Y", 0))
    return majority_vote, decision