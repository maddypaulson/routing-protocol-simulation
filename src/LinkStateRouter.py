from Router import Router
from utilities import INFINITY
import heapq

class LinkStateRouter(Router):
    def __init__(self, id, network):
        super().__init__(id)
        self.lsp_sequence_number = 0
        # self.network = network
        self.network_topology = {}
        self.network = network
    
    def generate_lsp(self):
        self.lsp_sequence_number += 1
        return {'id': self.id, 'sequence': self.lsp_sequence_number, 'neighbors': self.neighbors}
    
    def process_lsp(self, lsp):
        self.network_topology[lsp['id']] = lsp['neighbors']
        self.network_topology[self.id] = self.neighbors
    
    def ls_algorithm(self):
        shortest_paths = {node: float('infinity') for node in self.network_topology}
        previous_nodes = {node: None for node in self.network_topology}
        next_hops = {node: None for node in self.network_topology}
        shortest_paths[self.id] = 0
        pq = [(0, self.id)]
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_distance > shortest_paths[current_node]:
                continue
            
            for neighbor, weight in self.network_topology[current_node].items():
                distance = current_distance + weight
                
                if distance < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        # reconstruct shortest path in order to find the next hop
        for node in self.network_topology:
            if node == self.id:
                next_hops[node] = self.id
            else:
                current = node
                path = []
                while current is not None:
                    path.insert(0, current)
                    current = previous_nodes[current]
                    
                if len(path) > 1:
                    next_hops[node] = path[1]    
                else:
                    next_hops[node] = INFINITY
                          
        return shortest_paths, next_hops
        
    # def update_routing_table_dijkstra(self):
    #     print(self.network)
    #     self.network.print_network()       
    
    def update_routing_table_dijkstra(self):
        print(f"network topology: {self.network_topology}\n")
        print(f"router id: {self.id}\n")
        shortest_paths, next_hops = self.ls_algorithm()
        
        for destination_id, cost in shortest_paths.items():
            destination_router = self.network.routers[destination_id]
            next_hop_id = next_hops[destination_id]
            
            if next_hop_id is not None:
                next_hop_router = self.network.routers[next_hop_id]
            else:
                next_hop_router = None
                
            self.update_routing_table(destination_router, next_hop_router, cost)
