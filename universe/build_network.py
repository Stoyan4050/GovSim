import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Network:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def create_connection(self, node1, node2):
        if node1.compute_fitness(node2) > np.random.uniform(0, 1):
            node1.connections.append(node2)
            node2.connections.append(node1)

    def visualize_network(self):
        G = nx.Graph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                G.add_edge(node, conn)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue")
        plt.title("Network Visualization")
        plt.show()

    def update_connections(self):
        # Iterate over all pairs of nodes
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                node1 = self.nodes[i]
                node2 = self.nodes[j]
                
                # Compute the fitness between the two nodes
                fitness_value = node1.compute_fitness(node2)
                
                # If the nodes are already connected
                if node2 in node1.connections:
                    # If fitness value drops below a threshold, remove the connection
                    if fitness_value < 0.4:  # Threshold can be adjusted
                        node1.connections.remove(node2)
                        node2.connections.remove(node1)
                # If the nodes are not connected
                else:
                    # If fitness value exceeds a threshold, create a connection
                    if fitness_value > 0.6:  # Threshold can be adjusted
                        node1.connections.append(node2)
                        node2.connections.append(node1)
    
    def compute_fitness(self, other_node):
        R = 0.5 if self.group == other_node.group else np.random.uniform(0, 0.5)
        W = other_node.wealth / max([node.wealth for node in self.connections + [self]])
        D = len(other_node.connections) / max([len(node.connections) for node in self.connections + [self]])
        corr = np.corrcoef(self.preferences, other_node.preferences)
        
        return 0.5 * R + 0.5 * (corr + W + D) / 3

    def generate_value(prob_of_1):
        """
        Generate a random value of 1 with a probability of 'prob_of_1' 
        and 0 with a probability of '1 - prob_of_1'.
        """
        return 1 if random.random() < prob_of_1 else 0


# Example usage
# node1 = Node('OC', 100)
# node2 = Node('PT', 150)
# network = Network()
# network.add_node(node1)
# network.add_node(node2)
# network.create_connection(node1, node2)
# network.conduct_voting({'OC': 1, 'PT': 0, 'IP': 0, 'CA': 0})
# network.visualize_network()
