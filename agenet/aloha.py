import random

class Node:
    def __init__(self, id, rate, active_prob):
        self.id = id
        self.AoI = 0
        self.collision_count = 0
        self.rate = rate
        self.next_update_time = random.expovariate(rate)
        self.active_prob = active_prob
    
    def generate_update(self):
        self.next_update_time += random.expovariate(self.rate)
    
    def increment_AoI(self):
        self.AoI += 1
    
    def reset_AoI(self):
        self.AoI = 0
    
    def increment_collision(self):
        self.collision_count += 1

num_nodes = 10
num_slots = 100
channel_error_prob = 1
update_rate = 2
active_prob = 0.5

nodes = [Node(i, update_rate, active_prob) for i in range(num_nodes)]

for i in range(num_slots):
    updates = []
    for j in range(num_nodes):
        if random.random() < nodes[j].active_prob:
            if i >= nodes[j].next_update_time:
                if random.random() > channel_error_prob:
                    updates.append(j)
    for j in updates:
        if channel_error_prob == 1:
            nodes[j].increment_AoI()
        else:
            is_collision = len(updates) > 1
            if is_collision:
                nodes[j].increment_collision()
            else:
                nodes[j].generate_update()
                nodes[j].reset_AoI()
    for j in range(num_nodes):
        nodes[j].increment_AoI()

for i in range(num_nodes):
    print(f"Node {i} AoI: {nodes[i].AoI}")
    print(f"Node {i} Collision Count: {nodes[i].collision_count}")
