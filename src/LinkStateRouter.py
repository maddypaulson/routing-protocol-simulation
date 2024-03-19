from Router import Router
import heapq

class LinkStateRouter(Router):
    def __init__(self, id):
        super().__init__(id)
        self.lsp_sequence_number = 0
        self.network_topology = {}
    
    def generate_lsp(self):
        self.lsp_sequence_number += 1
        return {'id': self.id, 'sequence': self.lsp_sequence_number, 'neighbors': self.neighbors}
    
    def process_lsp(self, lsp):
        self.network_topology[lsp['id']] = lsp['neighbors']
    
    def ls_algorithm(self, network_topology, router_id):
        distances = {node: float('infinity') for node in network_topology}
        distances[router_id] = 0
        
        previous_nodes = {node: None for node in network_topology}
        
        pq = [(0, router_id)]
        
        print(f"Initial distances: {distances}")
        print(f"Initial previous_nodes: {previous_nodes}")
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # Iterate through the neighbors of the current node
            for neighbor, cost in network_topology.get(current_node, {}).items():
                distance = current_distance + cost
                # If a shorter path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
            
            print(f"Current node: {current_node}, Current distance: {current_distance}")
            print(f"Updated distances: {distances}")
            print(f"Updated previous_nodes: {previous_nodes}") 
            
        print(f"Final distances before constructing shortest paths: {distances}")
        print(f"Final previous_nodes before constructing shortest paths: {previous_nodes}")
               
        shortest_paths = {}
        for destination in network_topology:
            if destination == router_id or distances[destination] == float('infinity'):
                continue
            next_hop = destination
            while previous_nodes[next_hop] != router_id:
                print(f"Reconstructing path: Current next_hop for destination {destination}: {next_hop}")
                next_hop = previous_nodes[next_hop]
            shortest_paths[destination] = (next_hop, distances[destination])
        
        print(f"shortest paths for node {self.id}:\n{shortest_paths}")    
        return shortest_paths      
        
    def update_routing_table_dijkstra(self):
        # print(f"network topology: {self.network_topology}\n")
        # print(f"router id: {self.id}\n")
        shortest_paths = self.ls_algorithm(self.network_topology, self.id)
        # print(f"shortest paths for node {self.id}:\n", shortest_paths)
        # for destination, (next_hop, cost) in shortest_paths.items():
        #     self.update_routing_table(destination, next_hop, cost)       
