import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from nodes import Node

class Network:
    def __init__(self):
        self.nodes = []

    # def add_new_node(self, group, incentive_mechanism, min_wealth_group, max_wealth_group):
    #     node_wealth = self.random_wealth_value(min_wealth_group, max_wealth_group)
    #     new_node = Node.Node(node_wealth, group, incentive_mechanism)
    #     self.nodes.append(new_node)

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def update_connections(self):
        # Iterate over all pairs of nodes
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                node1 = self.nodes[i]
                node2 = self.nodes[j]
                
                # Compute the fitness between the two nodes
                fitness_value = node1.compute_fitness(node2)
                print("Fitness: ", fitness_value)
                
                connection_decision = self.generate_value_from_fitness(fitness_value)
                print("Obtain value: ", connection_decision)

                # If the nodes are already connected, check if the connection should be removed
                if node2 in node1.connections:
                    if connection_decision == 0:
                        node1.connections.remove(node2)
                        print("Connection removed")
                # If the nodes are not connected, check if a connection should be created
                elif connection_decision == 1:
                    node1.connections.append(node2)
                    print("Connection created")

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

    def generate_value_from_fitness(prob_of_1):
        """
        Generate a random value of 1 with a probability of 'prob_of_1' 
        and 0 with a probability of '1 - prob_of_1'.
        """
        return 1 if random.random() < prob_of_1 else 0

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