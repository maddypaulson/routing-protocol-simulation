import sys
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
            
    def send_message(self, router_id_from, router_id_to, message):
        router_from = self.get_router(router_id_from)
        router_to = self.get_router(router_id_to)

        if router_id_to not in router_from.routing_table.keys() or router_from.routing_table[router_id_to][1] == INFINITY:
            #impossible to reach
            print(f"from {router_id_from} to {router_id_to} cost infinite hops unreachable message message {message}")
            return
        
        next_hop, cost = router_from.routing_table[router_to.id]
        hops = [str(router_id_from)]
        total_cost = cost

        while next_hop != router_to.id:
            hops.append(str(next_hop))
            next_router = self.get_router(next_hop)
            next_hop, cost = next_router.routing_table[router_to.id]
            total_cost += cost
            
        hops_str = ' '.join(map(str, hops))
        print(f"from {router_id_from} to {router_id_to} cost {total_cost} hops {hops_str} message {message}")
                
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

def parseArgs():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python your_script.py topology_file message_file changes_file [output_file]")
        sys.exit(1)
    
    args = sys.argv[1:]

    if len(sys.argv) == 4:
        args += ["output.txt"]

    return args