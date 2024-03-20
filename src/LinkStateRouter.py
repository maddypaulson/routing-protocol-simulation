from Router import Router
from utilities import INFINITY
import heapq


class LinkStateRouter(Router):
    """
    This class represents a Link State Router.

    It inherits from the Router class and implements the Link State Routing algorithm.
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
        self.sequence_number_tracker = {router_id: 0 for router_id in network_routers.keys()}
        self.network_routers = network_routers
    
    def generate_lsp(self, network):
        """
        Generates a Link State Packet (LSP) and distributes it to all other routers in the network.

        Args:
            network (Network): The network object representing the network topology.
        """
        self.lsp_sequence_number += 1
        lsp =  {'id': self.id, 'sequence': self.lsp_sequence_number, 'neighbors': self.neighbors}
        self._distribute_lsp(lsp, network)
    
    def _process_lsp(self, lsp, network):
        """
        Processes a received Link State Packet (LSP) and updates the network topology if necessary.

        Args:
            lsp (dict): The received LSP.
            network (Network): The network object representing the network topology.
        """
        if lsp['id'] not in self.sequence_number_tracker.keys() or lsp['sequence'] > self.sequence_number_tracker[lsp['id']]:
            self.sequence_number_tracker[lsp['id']] = lsp['sequence']
            self.network_topology[lsp['id']] = lsp['neighbors']
            self.network_topology[self.id] = self.neighbors
            self._distribute_lsp(lsp, network)

    
    def _distribute_lsp(self, lsp, network):
        """
        Distributes a Link State Packet (LSP) to all other routers in the network.

        Args:
            lsp (dict): The LSP to be distributed.
            network (Network): The network object representing the network topology.
        """
        # send the lsp to all other routers in the network
        for router_id in self.neighbors.keys():
                router = network.routers[router_id]
                router._process_lsp(lsp, network)

    def _ls_algorithm(self):
        """
        Implements the Link State algorithm to calculate the shortest paths and next hops.

        Returns:
            tuple: A tuple containing two dictionaries - shortest_paths and next_hops.
                shortest_paths: A dictionary mapping each node to its shortest path cost from the current router.
                next_hops: A dictionary mapping each node to its next hop router ID.
        """
        shortest_paths = {node: INFINITY for node in self.network_topology}
        previous_nodes = {node: None for node in self.network_topology}
        next_hops = {node: None for node in self.network_topology}
        shortest_paths[self.id] = 0
        pq = [(0, self.id, self.id)]
        
        while pq:
            current_distance, current_node, _ = heapq.heappop(pq)
            
            if current_distance > shortest_paths[current_node]:
                continue
            
            for neighbor, weight in self.network_topology[current_node].items():
                distance = current_distance + weight
                
                if distance < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor, neighbor))
                elif distance == shortest_paths[neighbor] and previous_nodes[neighbor] is not None:
                    # If there's a tie in cost, compare based on the last node's ID before the destination
                    current_last_node = previous_nodes[current_node]
                    existing_last_node = previous_nodes[previous_nodes[neighbor]]
                    if current_last_node is not None and existing_last_node is not None and current_last_node < existing_last_node:
                        previous_nodes[neighbor] = current_node
        
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
