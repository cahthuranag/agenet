import random
from agenet import maincom

class Node:
    def __init__(self, id, active_prob):
        self.id = id
        self.AoI = 0
        self.active_prob = active_prob
    

    
    def calaoi_AoI(self):
     self.AoI = maincom.main()
     

num_nodes = 1
active_prob = 0.5

nodes = [Node(i, active_prob) for i in range(num_nodes)]


for j in range(num_nodes):
        nodes[j].calaoi_AoI()

for i in range(num_nodes):
    print(f"Node {i} AoI: {nodes[i].AoI}")
    
