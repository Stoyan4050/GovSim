import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from nodes import Node
import math
from scipy.stats import truncnorm
from pyvis.network import Network as net

class Network:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node_remove):
        # remove all ocnnection to the node that is leaving
        for node in self.nodes:
            if node_remove in node.connections:
                node.connections.remove(node_remove)

        self.nodes.remove(node)

    def update_connections(self):
        # Iterate over all pairs of nodes
        for node1 in self.nodes:
            other_nodes = [node for node in self.nodes if node != node1]
            for node2 in other_nodes:
                
                #print("Node 1: ", node1.group, "Node 2: ", node2.group)
                # Compute the fitness between the two nodes
                #fitness_value = node1.compute_fitness(node2, self.nodes)
                fitness_value1 = node1.compute_fitness(node2, self.nodes)
                fitness_value2 = node2.compute_fitness(node1, self.nodes)

                # print("Fitness: ", fitness_value)
                
                # if fitness_value < 0.5:
                #     connection_decision = 0
                # else:
                #     connection_decision = 1

                #connection_decision = self.generate_value_from_fitness(fitness_value)
                connection_decision1 = self.generate_value_from_fitness(fitness_value1)
                connection_decision2 = self.generate_value_from_fitness(fitness_value2)

                #connection_decision = self.generate_value_from_fitness(self.gaussian_probability(fitness_value))

                # print("Obtain value: ", connection_decision)

                # If the nodes are already connected, check if the connection should be removed
                # if node2 in node1.connections:
                #     if connection_decision == 0:
                #         node1.connections.remove(node2)
                #         #print("Connection removed")
                # # If the nodes are not connected, check if a connection should be created
                # elif connection_decision == 1:
                #     node1.connections.append(node2)
                    #print("Connection created")

                if node2 in node1.connections and node1 in node2.connections:
                    if connection_decision1 == 0 or connection_decision2 == 0:
                        node1.connections.remove(node2)
                        node2.connections.remove(node1)

                        #print("Connection removed")
                # If the nodes are not connected, check if a connection should be created
                elif connection_decision1 == 1 and connection_decision2 == 1:
                    node1.connections.append(node2)
                    node2.connections.append(node1)
                    #print("Connection created")

    def visualize_network(self):
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                G.add_edge(node, conn)
        


        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=False, node_size=700, node_color="skyblue")
        
        # Assuming each node has an attribute called 'label'
        labels = {node: node.group for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels)

        G1 = G.copy()
        # Convert node IDs to strings
        G1 = nx.relabel_nodes(G1, lambda x: str(x))

        # Assuming each node has an attribute 'group', set it as the label
        labels = {node: node_data['group'] for node, node_data in G1.nodes(data=True)}
        nx.set_node_attributes(G1, labels, 'label')

        g = net(notebook=True)
        g.from_nx(G1)

        # Display the interactive network
        g.show('network.html')


        all_edges = G.edges()
        print("Number of connections: ", len(all_edges))
        
        plt.title("Network Visualization")
        plt.show()
    
    def get_networkx_graph_noDi(self):
        G = nx.Graph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                G.add_edge(node, conn)
        
        return G
    
    def visualize_network2(self):
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                if node in conn.connections:
                    G.add_edge(node, conn)
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=False, node_size=700, node_color="skyblue")
        
        # Assuming each node has an attribute called 'label'
        labels = {node: node.group for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels)

        all_edges = G.edges()
        print("Number of connections: ", len(all_edges))
        
        plt.title("Network Visualization")
        plt.show()
    
    def get_networkx_graph_noDi(self):
        G = nx.Graph()
        for node in self.nodes:
            G.add_node(node)
            for conn in node.connections:
                G.add_edge(node, conn)
        
        return G
    
    def get_networkx_graph_Di(self):
        G = nx.DiGraph()
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
        #return 1 if self.generate_truncated_normal(0.5) < prob_of_1 else 0
    
    def gaussian_probability(self, fitness_value, mean=0.5, sigma=0.1):
        return math.exp(-((fitness_value - mean) ** 2) / (2 * sigma ** 2))
    
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
