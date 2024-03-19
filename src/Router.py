from utilities import INFINITY


class Router:
    def __init__(self, id):
        """
        Initializes a Router object.

        Parameters:
        - id (int): The ID of the router.

        Returns:
        - None
        """
        self.id = id
        self.neighbors = {}
        self.routing_table = {}
        self.update_routing_table(self, self, 0)
    
    def add_neighbor(self, neighbor, cost):
        """
        Adds a neighbor to the router.

        Parameters:
        - neighbor (Router): The neighbor router object.
        - cost (int): The cost to reach the neighbor.

        Returns:
        - None
        """
        self.neighbors[neighbor.id] =  cost
        self.update_routing_table(neighbor, neighbor, cost)
    
    def update_routing_table(self, destination, next_hop, cost):
        """
        Updates the routing table of the router.

        Parameters:
        - destination (Router): The destination router object.
        - next_hop (Router): The next hop router object.
        - cost (int): The cost to reach the destination.

        Returns:
        - None
        """
        if cost == INFINITY: 
            self.routing_table[destination.id] = (None, INFINITY)
        else:
            self.routing_table[destination.id] = (next_hop.id, cost)
    
    def print_routing_table(self):
        """
        Prints the routing table of the router.

        Parameters:
        - None

        Returns:
        - str: The routing table as a string.
        """
        routing_table_str = ""
        for destination in sorted(self.routing_table):
            next_hop, cost = self.routing_table[destination]
            if cost != INFINITY:
                routing_table_str += f"{destination} {next_hop} {cost}\n"
        return routing_table_str
        