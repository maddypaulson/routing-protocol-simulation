from Router import Router
from utilities import INFINITY
import heapq


class LinkStateRouter(Router):
    
    """
    This class represents a Link State Router.

    It inherits from the Router class and implements the Link State Routing algorithm.

    Attributes:
        lsp_sequence_number (int): The sequence number of the Link State Packet (LSP) generated by the router.
        network_topology (dict): A dictionary representing the network topology, where the keys are the router IDs and the values are the neighbor routers.
        sequence_number_tracker (dict): A dictionary tracking the sequence numbers of received LSPs from other routers.
        network_routers (dict): A dictionary representing the network routers, where the keys are the router IDs and the values are the router objects. 
                                This is not used for shared global knowledge, but a way to access the object of other routers, in order to trigger actions on them.
    """

    def __init__(self, id, network_routers):
        """
        Initializes a LinkStateRouter object.

        Args:
            id (int): The ID of the router.
            network_routers (dict): A dictionary representing the network routers, where the keys are the router IDs and the values are the router objects.
        """
        super().__init__(id)
        self.lsp_sequence_number = 0
        self.network_topology = {}
        self.sequence_number_tracker = {}
        self.network_routers = network_routers
    
    def generate_lsp(self):
        """
        Generates a Link State Packet (LSP) and distributes it to all other routers in the network.
        """
        self.lsp_sequence_number += 1
        lsp =  {'id': self.id, 'sequence': self.lsp_sequence_number, 'neighbors': self.neighbors}
        self._distribute_lsp(lsp)
    
    def _process_lsp(self, lsp):
        """
        Processes a received Link State Packet (LSP) and updates the network topology if necessary.

        Args:
            lsp (dict): The received LSP.
        """
        if lsp['id'] not in self.sequence_number_tracker.keys() or lsp['sequence'] > self.sequence_number_tracker[lsp['id']]:
            self.sequence_number_tracker[lsp['id']] = lsp['sequence']
            self.network_topology[lsp['id']] = lsp['neighbors']
            self.network_topology[self.id] = self.neighbors
            self._distribute_lsp(lsp)

    
    def _distribute_lsp(self, lsp):
        """
        Distributes a Link State Packet (LSP) to all other routers in the network.

        Args:
            lsp (dict): The LSP to be distributed.
        """
        # send the lsp to all other routers in the network
        for router_id in self.neighbors.keys():
                router = self.network_routers[router_id]
                router._process_lsp(lsp)

    def _ls_algorithm(self):
        """
        Implements the Link State algorithm to calculate the shortest paths and next hops.

        Returns:
            tuple: A tuple containing two dictionaries - shortest_paths and next_hops.
                shortest_distances: A dictionary mapping each node to its shortest path cost from the current router.
                next_hops: A dictionary mapping each node to its next hop router ID.
        """
        shortest_distances = {node: INFINITY for node in self.network_topology}
        paths = {self.id: [self.id]}   
        shortest_distances[self.id] = 0
        pq = [(0, self.id, [self.id])]
        
        while pq:
            current_distance, current_node, current_path = heapq.heappop(pq)
            
            if current_distance > shortest_distances[current_node]:
                continue
            
            for neighbor, weight in self.network_topology[current_node].items():
                distance = current_distance + weight
                new_path = current_path + [neighbor]
                    
                if distance < shortest_distances.get(neighbor, INFINITY):
                    shortest_distances[neighbor] = distance
                    paths[neighbor] = new_path
                    heapq.heappush(pq, (distance, neighbor, new_path))
                elif distance == shortest_distances[neighbor] and  new_path[-2] < paths[neighbor][-2]:
                    paths[neighbor] = new_path

        # reconstruct shortest path in order to find the next hop
        next_hops = {node: None for node in self.network_topology}

        for node in self.network_topology:
            if node == self.id:
                next_hops[node] = self.id
            else:
                
                if paths.get(node, False) and len(paths[node]) > 1:
                    next_hops[node] = paths[node][1]
                else:
                    next_hops[node] = INFINITY
                        
        return shortest_distances, next_hops
        
    def update_routing_table_dijkstra(self):
        """
        Updates the routing table using Dijkstra's algorithm.

        This method calculates the shortest paths and next hops using the Link State algorithm,
        and updates the routing table accordingly.
        """
        shortest_paths, next_hops = self._ls_algorithm()
        self.routing_table = {}
        
        for destination_id, cost in shortest_paths.items():
            destination_router = self.network_routers[destination_id]
            next_hop_id = next_hops[destination_id]
            
            if next_hop_id not in [None, INFINITY] :
                next_hop_router = self.network_routers[next_hop_id]
            else:
                next_hop_router = None
                
            self.update_routing_table(destination_router, next_hop_router, cost)
