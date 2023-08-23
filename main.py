import numpy as np
from universe import build_universe
from voting import voting_development, Voting
from voting_decision import VotingDecision
import random
import matplotlib.pyplot as plt
from universe import network_development
import networkx as nx
from community import community_louvain
import community
from voting_incentives import Incentive
from pyvis.network import Network

VOTING_METHOD = 'simple_majority'
AVG_VOTING_RATE = 0.5
WEALTH = 1000000
TOKENS_AMOUNT = 1000000
RANDOM_SEED = 42
network_update = [0, 0, 0]
results = []

num_proposals = 100

GINI_HISTORY = []

def main():
    
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    # Create new universe

    universe, network, total_token_amount_per_group = build_universe.build_universe_network()
    print("Participants: ", len(universe.participants))

    # inc = Incentive.Incentive(network)
    # inc.participation_probability("PT")
    # Print participants per group
    for key, participants in universe.participants_per_group.items():
        print(f"{key}: {len(participants)} participants")    
        
    network.visualize_network()
    #network.visualize_network2()


    simulate_voting(universe, network, num_proposals, total_token_amount_per_group)


def simulate_voting(universe, network, num_proposals, total_token_amount_per_group):
    GINI_HISTORY = []
    satisfaction_level_history = {"OC": [], "IP": [], "PT": [], "CA": []}
    proposal_count = 0
    node_per_group_history = {"OC": [], "IP": [], "PT": [], "CA": []}
    proposal_per_group = {"OC": [], "IP": [], "PT": [], "CA": []}
    WEALTH_GROUP = {"OC": [], "IP": [], "PT": [], "CA": []}
    results = []


    CLUSTERING = {"num_clusters": [], "modularity": [], "avg_clustering": []}
    NAKAMOTO_COEFF = []
    VOTING_RATE_HISTORY = []

    for i in range(num_proposals):
        proposal_count += 1
        proposal = voting_development.define_proposal(network)

        # Voting mechanism can be: token_based_vote, quadratic_vote
        #voting = Voting.Voting(proposal, network, universe, voting_mechanism="token_based_vote")
        voting = Voting.Voting(proposal, network, universe, voting_mechanism="quadratic_vote")
        #voting = Voting.Voting(proposal, network, universe, voting_mechanism="reputation_vote")

        result, GINI, voting_rate = voting.vote()

        GINI_HISTORY.append(GINI)
        VOTING_RATE_HISTORY.append(voting_rate)

        # plt.plot(GINI_HISTORY)
        # plt.show()

        OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS, SATISFACTION_LEVEL = network_development.update_network(
                                                                         universe, network, result, proposal_count, total_token_amount_per_group)
        

        group_counts = {"OC": 0, "IP": 0, "PT": 0, "CA": 0}
        temp_wealth_group = {"OC": 0, "IP": 0, "PT": 0, "CA": 0}
        for node in network.nodes:
            group_counts[node.group] += 1 
            temp_wealth_group[node.group] += node.wealth


        if (group_counts["CA"]) == 0 or (group_counts["PT"]) == 0 or (group_counts["IP"]) == 0 or (group_counts["OC"]) == 0:
            break

        WEALTH_GROUP['OC'].append(temp_wealth_group['OC'])
        WEALTH_GROUP['IP'].append(temp_wealth_group['IP'])
        WEALTH_GROUP['PT'].append(temp_wealth_group['PT'])
        WEALTH_GROUP['CA'].append(temp_wealth_group['CA'])

        node_per_group_history['OC'].append(group_counts['OC'])
        node_per_group_history['IP'].append(group_counts['IP'])
        node_per_group_history['PT'].append(group_counts['PT'])
        node_per_group_history['CA'].append(group_counts['CA'])

        satisfaction_level_history["OC"].append(SATISFACTION_LEVEL["OC"])
        satisfaction_level_history["IP"].append(SATISFACTION_LEVEL["IP"])
        satisfaction_level_history["PT"].append(SATISFACTION_LEVEL["PT"])
        satisfaction_level_history["CA"].append(SATISFACTION_LEVEL["CA"])

        proposal_per_group["OC"].append(proposal.OC_preferences)
        proposal_per_group["IP"].append(proposal.IP_preferences)
        proposal_per_group["PT"].append(proposal.PT_preferences)
        proposal_per_group["CA"].append(proposal.CA_preferences)
        #print("OVERALL SATISFACTION: ", OVERALL_SATISFACTION)
        #print("NUMBER OF PARTICIPANTS: ", NUMNBER_PARTICIPANTS)
        #print("SATISFACTION LEVEL GROUP: ", SATISFACTION_LEVEL)

        #network.visualize_network()

        # Clustering metric
        num_clusters, modularity, avg_clustering_coefficient = compute_clustering_metrics(network)
        CLUSTERING["num_clusters"].append(num_clusters)
        CLUSTERING["modularity"].append(modularity)
        CLUSTERING["avg_clustering"].append(avg_clustering_coefficient)

        # Nakamoto coefficient
        nakamoto_coefficient = calculate_nakamoto_coefficient([node.wealth for node in network.nodes])
        NAKAMOTO_COEFF.append(nakamoto_coefficient)
        results.append(result)

        #print("Result: ", result)
    print("Groups: ", group_counts)

    print("SATISFACTION LEVEL OC FINAL: ", satisfaction_level_history["OC"][-1])
    print("SATISFACTION LEVEL IP FINAL: ", satisfaction_level_history["IP"][-1])
    print("SATISFACTION LEVEL PT FINAL: ", satisfaction_level_history["PT"][-1])
    print("SATISFACTION LEVEL CA FINAL: ", satisfaction_level_history["CA"][-1])

    print("SATISFACTION LEVEL OC AVG: ", np.mean(satisfaction_level_history["OC"]))
    print("SATISFACTION LEVEL IP AVG: ", np.mean(satisfaction_level_history["IP"]))
    print("SATISFACTION LEVEL PT AVG: ", np.mean(satisfaction_level_history["PT"]))
    print("SATISFACTION LEVEL CA AVG: ", np.mean(satisfaction_level_history["CA"]))


    print("WEALTH OC FINAL: ", WEALTH_GROUP['OC'][-1])
    print("WEALTH IP FINAL: ", WEALTH_GROUP['IP'][-1])
    print("WEALTH PT FINAL: ", WEALTH_GROUP['PT'][-1])
    print("WEALTH CA FINAL: ", WEALTH_GROUP['CA'][-1])

    print("WEALTH OC AVG: ", np.mean(WEALTH_GROUP['OC']))
    print("WEALTH IP AVG: ", np.mean(WEALTH_GROUP['IP']))
    print("WEALTH PT AVG: ", np.mean(WEALTH_GROUP['PT']))
    print("WEALTH CA AVG: ", np.mean(WEALTH_GROUP['CA']))

    print("PROPOSAL OC: ", np.sum(proposal_per_group["OC"]))
    print("PROPOSAL IP: ", np.sum(proposal_per_group["IP"]))
    print("PROPOSAL PT: ", np.sum(proposal_per_group["PT"]))
    print("PROPOSAL CA: ", np.sum(proposal_per_group["CA"]))

    print("PROPOSAL Y: ", results.count("Y"))
    print("PROPOSAL N: ", results.count("N"))

    print("NAKAMOTO COEFFICIENT FINAL: ", NAKAMOTO_COEFF[-1])
    print("NAKAMOTO COEFFICIENT AVG: ", np.mean(NAKAMOTO_COEFF))
    print("NAKAMOTO COEFFICIENT INITIAL: ", NAKAMOTO_COEFF[0])

    print("AVG voting rate: ", np.mean(VOTING_RATE_HISTORY))

    print("CLUSTRING NUM CLUSTERS FINAL: ", CLUSTERING["num_clusters"][-1])
    print("CLUSTRING NUM CLUSTERS AVG: ", np.mean(CLUSTERING["num_clusters"]))
    print("CLUSTRING NUM CLUSTERS INITIAL: ", CLUSTERING["num_clusters"][0])

    print("CLUSTRING MODULARITY FINAL: ", CLUSTERING["modularity"][-1])
    print("CLUSTRING MODULARITY AVG: ", np.mean(CLUSTERING["modularity"]))
    print("CLUSTRING MODULARITY INITIAL: ", CLUSTERING["modularity"][0])

    print("CLUSTRING AVG CLUSTERING FINAL: ", CLUSTERING["avg_clustering"][-1])
    print("CLUSTRING AVG CLUSTERING AVG: ", np.mean(CLUSTERING["avg_clustering"]))
    print("CLUSTRING AVG CLUSTERING INITIAL: ", CLUSTERING["avg_clustering"][0])


    plot_benchmark_results(network, OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS, 
                           satisfaction_level_history, node_per_group_history, GINI_HISTORY, CLUSTERING, NAKAMOTO_COEFF, VOTING_RATE_HISTORY)


    #print("GINI HISTORY: ", GINI_HISTORY)

def compute_clustering_metrics(network):

    G = network.get_networkx_graph_noDi()

    partition = community_louvain.best_partition(G)
    num_clusters = max(partition.values()) + 1

    #print("Number of Clusters:", num_clusters)

    modularity = community.modularity(partition, G)
    #print("Modularity:", modularity)

    avg_clustering_coefficient = nx.average_clustering(G)
    #print("Average Clustering Coefficient:", avg_clustering_coefficient)

    return num_clusters, modularity, avg_clustering_coefficient

def calculate_nakamoto_coefficient(entity_powers):
    """
    Calculate the Nakamoto Coefficient.
    
    Parameters:
    - entity_powers (list): A list of the power of each entity in the network.
    
    Returns:
    - int: The Nakamoto Coefficient.
    """
    # Step 1: Sort the entities in descending order based on their power
    sorted_powers = sorted(entity_powers, reverse=True)
    
    # Step 2: Calculate the total power of the network
    total_power = sum(sorted_powers)
    
    # Step 3: Find the minimum number of entities to gain control
    cumulative_power = 0
    for i, power in enumerate(sorted_powers):
        cumulative_power += power
        if cumulative_power > total_power / 2:
            return i + 1  # We add 1 because list indices are 0-based
    
    return None

def plot_benchmark_results(network, OVERALL_SATISFACTION, NUMNBER_PARTICIPANTS, 
                           satisfaction_level_history, node_per_group_history, GINI_HISTORY, CLUSTERING, NAKAMOTO_COEFF, VOTING_RATE_HISTORY):
    network.visualize_network()
    plt.plot(GINI_HISTORY)
    plt.title("GINI")
    plt.show()

    plt.plot(OVERALL_SATISFACTION[10:])
    plt.title("Overall satisfaction")
    plt.show()

    plt.plot(NUMNBER_PARTICIPANTS[10:])
    plt.title("Number of participants")
    plt.show()

    plt.plot(satisfaction_level_history["OC"][10:])
    plt.plot(satisfaction_level_history["IP"][10:])
    plt.plot(satisfaction_level_history["PT"][10:])
    plt.plot(satisfaction_level_history["CA"][10:])
    plt.title("Satisfaction level Group")
    plt.legend(["OC", "IP", "PT", "CA"])
    plt.show()

    plt.plot(node_per_group_history["OC"][10:])
    plt.plot(node_per_group_history["PT"][10:])
    plt.plot(node_per_group_history["CA"][10:])
    plt.title("Number of Participants per Group")
    plt.legend(["OC", "PT", "CA"])
    plt.show()

    plt.plot(node_per_group_history["IP"])[10:]
    plt.title("Number of Participants IP")
    plt.show()

    plt.plot(CLUSTERING["num_clusters"])
    plt.title("Number of Clusters")
    plt.show()

    plt.plot(CLUSTERING["modularity"])
    plt.title("Modularity")
    plt.show()

    plt.plot(CLUSTERING["avg_clustering"])
    plt.title("Average Clustering Coefficient")
    plt.show()

    # plt.plot(NAKAMOTO_COEFF)
    # plt.title("Nakamoto Coefficient")
    # plt.show()
    
    # plt.plot(VOTING_RATE_HISTORY)
    # plt.title("Voting Rate")
    # plt.show()

if __name__ == '__main__':
    main()