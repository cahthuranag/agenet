import random
import maincom

class Node:
    def __init__(self, id, active_prob):
        self.id = id
        
        #self.collision_count = 0
        #self.rate = rate
        #self.next_update_time = random.expovariate(rate)
        self.active_prob = active_prob
        self.AoI,_ = maincom.main()
        _,self.AoIth = maincom.main()
    

num_nodes = 4
num_slots = 100
channel_error_prob = 1
update_rate = 2
active_prob = 0.5

nodes = [Node(i, active_prob) for i in range(num_nodes)]



for i in range(num_nodes):
    print(f"Node {i} AoI: {nodes[i].AoI}")
    print(f"Node {i} AoIth: {nodes[i].AoIth}")
    