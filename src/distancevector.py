import sys
# Data to write
data_to_write = "This is the data from distance-vector."
INFINITY = float("inf")

class Router:
    def __init__(self, id):
        self.id = id
        self.neighbors = {}
        self.routing_table = {}
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor.id] =  cost
    
    def update_routing_table(self, destination, next_hop, cost):
        self.routing_table[destination.id] = (next_hop.id, cost)

class Network:
    def __init__(self, topology_file):
        self.routers = {}
        self.initialize_topology(topology_file)
    
    def add_router(self, router):
        self.routers[router.id] = router
    
    def update_routing_table(self, router, destination, next_hop, cost):
        self.routers[router.id].update_routing_table(destination, next_hop, cost)

    
    def add_link(self, router_id1, router_id2, cost):
        if(router_id1 not in self.routers.keys()):
            router1 = Router(router_id1)
            self.add_router(router1)
        if(router_id2 not in self.routers.keys()):
            router2 = Router(router_id2)
            self.add_router(router2)
        
        router1 = self.routers[router_id1]
        router2 = self.routers[router_id2]

        router1.add_neighbor(router2, cost)
        router2.add_neighbor(router1, cost)
    
    def initialize_topology(self, topology_file):
        with open(topology_file, 'r') as file:
            for line in file:
                router1, router2, cost = line.split()
                self.add_link(int(router1), int(router2), int(cost))

    def initialize_routing_table(self):
        for router in self.routers.values():
            # Initialize entry for self
            router.update_routing_table(router, router, 0)
            # Initialize cost for neighbours
            for neighbor in router.neighbors.keys():
                router.update_routing_table(self.routers[neighbor], self.routers[neighbor], router.neighbors[neighbor])
            # Initialize cost of infinity for all other routers
            for other_router in self.routers.keys():
                if other_router != router.id and other_router not in router.neighbors:
                    router.routing_table[other_router] = (None, INFINITY)
    
    def print_network(self):
        for router in self.routers:
            print(f"Router: {router}")
            print(f"Neighbors: {self.routers[router].neighbors}")
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
    network.initialize_routing_table()
    network.print_network()

    pass

if __name__ == "__main__":
    main()