from utilities import INFINITY

class Router:
    def __init__(self, id):
        self.id = id
        self.neighbors = {}
        self.routing_table = {}
        self.update_routing_table(self, self, 0)
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor.id] =  cost
        self.update_routing_table(neighbor, neighbor, cost)
    
    def update_routing_table(self, destination, next_hop, cost):
        if cost == INFINITY: 
            self.routing_table[destination.id] = (None, INFINITY)
        else:
            self.routing_table[destination.id] = (next_hop.id, cost)
    
    def print_routing_table(self):
        routing_table_str = ""
        for destination in sorted(self.routing_table):
            next_hop, cost = self.routing_table[destination]
            if cost != INFINITY:
                routing_table_str += f"{destination} {next_hop} {cost}\n"
        return routing_table_str
        