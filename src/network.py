from utilities import INFINITY
from Router import Router

class Network:
    def __init__(self, topology_file, output_file):
        self.routers = {}
        self.initialize_topology(topology_file)
        self.output_file = output_file
        self.output_file_iterator = open(output_file, 'w')  # Open output file
        
    def initialize_topology(self, topology_file):
        with open(topology_file, 'r') as file:
            for line in file:
                router1, router2, cost = line.split()
                self.add_link(int(router1), int(router2), int(cost))
    
    def add_router(self, router_id):
        router = Router(router_id)
        self.routers[router.id] = router
    
    def get_router(self, router_id):
        if router_id not in self.routers.keys():
            return None
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
    
    def remove_link(self, router1, router2):
        if router2.id in router1.neighbors:
            del router1.neighbors[router2.id]
            del router2.neighbors[router1.id]

            router1.update_routing_table(router2, None, INFINITY)
            router2.update_routing_table(router1, None, INFINITY)

            self.invalidate_routes_for_removed_link(router1, router2)
            
    def invalidate_routes_for_removed_link(self, router1, router2):
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

    def print_network(self):
        for router in self.routers:
            print(f"Router: {router}")
            print(f"Neighbors: {self.routers[router].neighbors}")
            print(f"Routing Table: {self.routers[router].routing_table}")
    
    def topology_output(self):
        for router in sorted(self.routers.values(), key=lambda x: x.id):
            routing_table_str = router.print_routing_table()
            self.output_file_iterator.write(routing_table_str)
            self.output_file_iterator.write("\n")

    def send_message(self, router_id_from, router_id_to, message):
        router_from = self.get_router(router_id_from)
        router_to = self.get_router(router_id_to)

        if self.check_impossible_to_reach(router_from, router_to):
            #impossible to reach
            self.output_file_iterator.write(f"from {router_id_from} to {router_id_to} cost infinite hops unreachable message message {message}")
            return
        else: 
            hops, total_cost = self.get_hops_and_cost(router_from, router_to)
            hops_str = ' '.join(map(str, hops))
            self.output_file_iterator.write(f"from {router_id_from} to {router_id_to} cost {total_cost} hops {hops_str} message {message}")
    
    def get_hops_and_cost(self, router_from, router_to):
        next_hop, cost = router_from.routing_table[router_to.id]
        hops = [str(router_from.id)]
        total_cost = cost

        while next_hop != router_to.id:
            hops.append(str(next_hop))
            next_router = self.get_router(next_hop)
            next_hop, cost = next_router.routing_table[router_to.id]
        
        return hops, total_cost
    
    def check_impossible_to_reach(self, router_from, router_to):
        if router_from == None or router_to == None:
            return True
        if router_to.id not in router_from.routing_table.keys() or router_from.routing_table[router_to.id][1] == INFINITY:
            return True
        return False

    def process_change(self, router_id1, router_id2, cost):
        if (cost == -999):
            if (router_id1 not in self.routers.keys()):
                self.add_router(router_id1)
            if (router_id2 not in self.routers.keys()):
                self.add_router(router_id2)
            router1 = self.get_router(router_id1)
            router2 = self.get_router(router_id2)

            self.remove_link(router1, router2)

        else:
            self.add_link(router_id1, router_id2, cost)
            

    def __del__(self):
        self.output_file_iterator.close()