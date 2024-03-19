import sys
# Data to write
data_to_write = "This is the data from distance-vector."
INFINITY = float("inf")

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
        if next_hop == None: 
            self.routing_table[destination.id] = (None, INFINITY)
        else:
            self.routing_table[destination.id] = (next_hop.id, cost)
    
    def print_routing_table(self):
        routing_table_str = ""
        for destination in sorted(self.routing_table):
            next_hop, cost = self.routing_table[destination]
            routing_table_str += f"{destination} {next_hop} {cost}\n"
        return routing_table_str
        
class Network:
    def __init__(self, topology_file):
        self.routers = {}
        self.initialize_topology(topology_file)
    
    def add_router(self, router_id):
        router = Router(router_id)
        self.routers[router.id] = router
    
    def get_router(self, router_id):
        return self.routers[router_id]
    
    def update_routing_table(self, router, destination, next_hop, cost):
        self.routers[router.id].update_routing_table(destination, next_hop, cost)
    
    
    def add_link(self, router_id1, router_id2, cost):
        if(router_id1 not in self.routers.keys()):
            self.add_router(router_id1)
        if(router_id2 not in self.routers.keys()):
            self.add_router(router_id2)
        
        router1 = self.routers[router_id1]
        router2 = self.routers[router_id2]

        router1.add_neighbor(router2, cost)
        router2.add_neighbor(router1, cost)
    
    def initialize_topology(self, topology_file):
        with open(topology_file, 'r') as file:
            for line in file:
                router1, router2, cost = line.split()
                self.add_link(int(router1), int(router2), int(cost))

    def print_network(self):
        for router in self.routers:
            print(f"Router: {router}")
            print(f"Neighbors: {self.routers[router].neighbors}")
            print(f"Routing Table: {self.routers[router].routing_table}")
    
    def topology_output(self, output_file):
        print(output_file)
        with open(output_file, 'w') as file:
            for router in sorted(self.routers.values(), key=lambda x: x.id):
                routing_table_str = router.print_routing_table()
                file.write(routing_table_str)
                file.write("\n")
            
            
    def process_change(self, router_id1, router_id2, cost):
        if (cost == -999):
            if (router_id1 not in self.routers.keys()):
                self.add_router(router_id1)
            if (router_id2 not in self.routers.keys()):
                self.add_router(router_id2)
            router1 = self.get_router(router_id1)
            router2 = self.get_router(router_id2)

            if router2.id in router1.neighbors:
                del router1.neighbors[router2.id]
                del router2.neighbors[router1.id]

                router1.update_routing_table(router2, None, INFINITY)
                router2.update_routing_table(router1, None, INFINITY)

                # Invalidate the routes that go through the routers that are being removed
                for destination_id in router1.routing_table.keys():
                    destination = self.get_router(destination_id)
                    next_hop, cost = router1.routing_table[destination_id]
                    if next_hop == router2.id:
                        router1.update_routing_table(destination, None, INFINITY)

                for destination_id in router2.routing_table.keys():
                    destination = self.get_router(destination_id)
                    next_hop, cost = router2.routing_table[destination_id]
                    if next_hop == router1.id:
                        router2.update_routing_table(destination, None, INFINITY)
        else:
            self.add_link(router_id1, router_id2, cost)
            pass


def dv_algorithm(network, priority_routers = []):
    # Make all routers send their routing table to their neighbors, except the one that is the destination or the one that is the next hop
    # Update the routing table of the neighbors
    # Repeat until no changes are made
    # Neighbor should not accept changes if it already has a better route. It should always update if it is receiving a message from the router that is its current destination

    # Initialize a flag to keep track of changes
    changes_made = True
    
    while changes_made:
        changes_made = False
        routers = priority_routers + [v for k, v in network.routers.items() if v not in priority_routers]

        # Iterate over each router in the network
        for router in routers:
            # Iterate over each neighbor of the router
            for neighbor in router.neighbors.keys():
                # Get the neighbor router object
                neighbor_router = network.routers[neighbor]
                
                # Iterate over each destination in the routing table of the router
                for destination in router.routing_table.keys():
                    # Get the next hop and cost to reach the destination from the router
                    next_hop_id, cost = router.routing_table[destination]
                    destination_router = network.routers[destination]
                    if should_transmit_message(neighbor_router, destination_router, next_hop_id):
                        if  should_accept_message(neighbor_router, router, destination_router, next_hop_id, cost):
                            # Update the routing table of the neighbor
                            neighbor_router.update_routing_table(destination_router, router, cost + router.neighbors[neighbor])
                            changes_made = True

def should_transmit_message(neigbour_router, destination, next_hop_id):
    if neigbour_router.id == destination.id:
        return False
    if neigbour_router.id == next_hop_id:
        return False
    return True

def should_accept_message(router, advertiser, destination, next_hop_id, cost):
    if destination.id not in router.routing_table.keys():
        return True
    if cost + advertiser.neighbors[router.id] < router.routing_table[destination.id][1]:
        return True
    if cost + advertiser.neighbors[router.id] == router.routing_table[destination.id][1] and router.routing_table[destination.id][0]  and advertiser.id < router.routing_table[destination.id][0]:
        return True
    if router.routing_table[destination.id][0] == advertiser.id and router.routing_table[destination.id][1] < cost + advertiser.neighbors[router.id]:
        return True
    return False

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
    dv_algorithm(network)
    network.topology_output(output_file)
    network.print_network()
    with open(changes_file, 'r') as changes_file:
        for line in changes_file:
            router_id1, router_id2, cost = line.split()
            network.process_change(int(router_id1), int(router_id2), int(cost))
            router_1 = network.get_router(int(router_id1))
            router_2 = network.get_router(int(router_id2))
            dv_algorithm(network, [router_1, router_2])
            pass
    
    # network.print_network()

    pass

if __name__ == "__main__":
    main()