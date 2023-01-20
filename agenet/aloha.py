import random
import maincom

class Node:
    def __init__(self, id, num_nodes, active_prob):
        self.id = id
        self.num_nodes = num_nodes
        self.active_prob = active_prob
        self.AoIth,_ = maincom.main(num_nodes, active_prob)
        _,self.AoI = maincom.main(num_nodes, active_prob)
    

num_nodes = 4
active_prob = 0.5

nodes = [Node(i, num_nodes , active_prob) for i in range(num_nodes)]



for i in range(num_nodes):
    print(f"Node {i} AoI: {nodes[i].AoI}")
    print(f"Node {i} AoIth: {nodes[i].AoIth}")
    