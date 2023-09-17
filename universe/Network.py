import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from nodes import Node
import math
from scipy.stats import truncnorm
from pyvis.network import Network as net

# Network class
class Network:
    def __init__(self, tokens_amount):
        self.nodes = []
        self.avg_voting_rate = []
        self.tokens_amount = tokens_amount
    
    # Add node
    def add_node(self, node):
        self.nodes.append(node)

    # Remove node
    def remove_node(self, node_remove):
        # remove all connections to the node that is leaving
        for node in self.nodes:
            if node_remove in node.connections:
                node.connections.remove(node_remove)

        self.nodes.remove(node)

    def update_connections(self):
        # Iterate over all pairs of nodes
        for node1 in self.nodes:
            other_nodes = [node for node in self.nodes if node != node1]
            for node2 in other_nodes:
                
                # Compute the fitness value of two nodes
                # The fitness values is probability to connect
                fitness_value1 = node1.compute_fitness(node2, self.nodes)
                fitness_value2 = node2.compute_fitness(node1, self.nodes)

                # Genrate decision to connect or not, based on the fitness value
                # If connection decision is 1, add connection
                # If connection decision is 0, remove connection, if such exists
                connection_decision1 = self.generate_value_from_fitness(fitness_value1)
                connection_decision2 = self.generate_value_from_fitness(fitness_value2)

                # Remove connection if one of the nodes do not want to connect
                if node2 in node1.connections and node1 in node2.connections:
                    if connection_decision1 == 0 or connection_decision2 == 0:
                        node1.connections.remove(node2)
                        node2.connections.remove(node1)

                # Add connection if both nodes want to connect
                elif connection_decision1 == 1 and connection_decision2 == 1:
                    node1.connections.append(node2)
                    node2.connections.append(node1)

    # Visualize the network
    def visualize_network(self):
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                G.add_edge(node, conn)
        

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=False, node_size=700, node_color="skyblue")
        
        # Labels for nodes
        labels = {node: node.group for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels)

        G1 = G.copy()
        # Convert node IDs to strings
        G1 = nx.relabel_nodes(G1, lambda x: str(x))

        # Set nodes labels
        nx.set_node_attributes(G1, labels, 'label')

        g = net(notebook=True)
        g.from_nx(G1)

        # Display the interactive network
        g.show('network.html')

        all_edges = G.edges()
        print("Number of connections: ", len(all_edges))
        
        plt.title("Network Visualization")
        plt.show()

    
    # Get no-directional networkx graph
    def get_networkx_graph_noDi(self):
        G = nx.Graph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                G.add_edge(node, conn)
        
        return G
    

    def generate_value_from_fitness(self, prob_of_1):
        """
        Generate a random value of 1 with a probability of 'prob_of_1' 
        and 0 with a probability of '1 - prob_of_1'.
        """
        return 1 if random.random() < prob_of_1 else 0
    
    
    def generate_truncated_normal(self, mean, sd=0.1, low=0, upp=1):
        """
        Generate a random number from a truncated normal distribution.

        Parameters:
        - mean (float): Mean of the distribution.
        - sd (float): Standard deviation.
        - low (float): Lower bound of the truncation.
        - upp (float): Upper bound of the truncation.

        Returns:
        - float: A random number from the truncated normal distribution.
        """
        a, b = (low - mean) / sd, (upp - mean) / sd
        return truncnorm.rvs(a, b, loc=mean, scale=sd)
