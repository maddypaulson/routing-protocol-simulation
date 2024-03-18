import sys
# Data to write
data_to_write = "This is the data from distance-vector."

class Router:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.routing_table = {}
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor.name] =  cost
    
    def update_routing_table(self, destination, next_hop, cost):
        self.routing_table[destination.name] = (next_hop.name, cost)

class Network:
    def __init__(self, topology_file):
        self.routers = {}
        self.initialize_topology(topology_file)
    
    def add_router(self, router):
        self.routers[router.name] = router
    
    def update_routing_table(self, router, destination, next_hop, cost):
        self.routers[router.name].update_routing_table(destination, next_hop, cost)

    
    def add_link(self, router_name1, router_name2, cost):
        if(router_name1 not in self.routers):
            router1 = Router(router_name1)
            self.add_router(router1)
        if(router_name2 not in self.routers):
            router2 = Router(router_name2)
            self.add_router(router2)
        
        router1 = self.routers[router_name1]
        router2 = self.routers[router_name2]

        router1.add_neighbor(router2, cost)
        router2.add_neighbor(router1, cost)
    
    def initialize_topology(self, topology_file):
        with open(topology_file, 'r') as file:
            for line in file:
                router1, router2, cost = line.split()
                self.add_link(router1, router2, int(cost))
    
    def print_network(self):
        for router in self.routers:
            transformed_dict = {str(key): value for key, value in self.routers[router].neighbors.items()}
            
            print(f"Router: {router}")
            print(f"Neighbors: {transformed_dict}")
            print(f"Routing Table: {self.routers[router].routing_table}")

# Open file and create if it doesn't exist
with open('output.txt', 'w') as file:
    file.write(data_to_write)

def parseArgs():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python your_script.py topology_file message_file changes_file [output_file]")
        sys.exit(1)
    
    args = sys.argv[1:]

    if len(sys.argv) == 4:
        args += ["output.txt"]

    return args


def main():
    args = parseArgs()
    topology_file, message_file, changes_file, output_file  = args

    network = Network(topology_file)
    network.update_routing_table(network.routers['1'], network.routers['2'], network.routers['2'], 1)
    network.print_network()
    pass

if __name__ == "__main__":
    main()