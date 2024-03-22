from utilities import INFINITY
from Router import Router

## @file
## @brief Implementation of the Network Class, that is the parent of the DistanceVectorNetwork and LinkStateNetwork classes.
# This file defines the Network class, which serves as a foundatio for simulating 
# various routing protocols, including both Distance Vector and Link State routing. The Network 
# class is responsible for maintaining a collection of Router objects, initializing the network 
# topology from a specified topology file, and providing core functionalities such as adding or 
# removing links between routers, updating routing tables, and handling message transmissions 
# across the network.
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup Super
## @{
class Network:
    """
    Represents a network of routers.

    Attributes:
        routers (dict): A dictionary of routers in the network.
        output_file (str): The path to the output file.
        output_file_iterator (file): The file iterator for writing output.
    """

    def __init__(self, topology_file, output_file):
        """
        Initializes a Network object.

        Args:
            topology_file (str): The path to the topology file.
            output_file (str): The path to the output file.
        """
        self.routers = {}
        self.initialize_topology(topology_file)
        self.output_file = output_file
        self.output_file_iterator = open(output_file, 'w')  # Open output file

    def initialize_topology(self, topology_file):
        """
        Initializes the network topology based on the given topology file.

        Args:
            topology_file (str): The path to the topology file.
        """
        with open(topology_file, 'r') as file:
            for line in file:
                router1, router2, cost = line.split()
                self.add_link(int(router1), int(router2), int(cost))

    def _add_router(self, router_id):
        """
        Adds a router to the network.

        Args:
            router_id (int): The ID of the router to add.
        """
        router = Router(router_id)
        self.routers[router.id] = router

    def get_router(self, router_id):
        """
        Retrieves a router from the network.

        Args:
            router_id (int): The ID of the router to retrieve.

        Returns:
            Router: The router object, or None if not found.
        """
        if router_id not in self.routers.keys():
            return None
        return self.routers[router_id]

    def update_routing_table(self, router, destination, next_hop, cost):
        """
        Updates the routing table of a router in the network.

        Args:
            router (Router): The router to update.
            destination (Router): The destination router.
            next_hop (int): The ID of the next hop router.
            cost (int): The cost to reach the destination.
        """
        self.routers[router.id].update_routing_table(destination, next_hop, cost)

    def add_link(self, router_id1, router_id2, cost):
        """
        Adds a link between two routers in the network.
        Add routers if they don't exist.

        Args:
            router_id1 (int): The ID of the first router.
            router_id2 (int): The ID of the second router.
            cost (int): The cost of the link.
        """
        if router_id1 not in self.routers.keys():
            self._add_router(router_id1)
        if router_id2 not in self.routers.keys():
            self._add_router(router_id2)

        router1 = self.routers[router_id1]
        router2 = self.routers[router_id2]

        router1.add_neighbor(router2, cost)
        router2.add_neighbor(router1, cost)

    def remove_link(self, router1, router2):
        """
        Removes a link between two routers in the network.

        Args:
            router1 (Router): The first router.
            router2 (Router): The second router.
        """
        if router2.id in router1.neighbors:
            del router1.neighbors[router2.id]
            del router2.neighbors[router1.id]

            router1.update_routing_table(router2, None, INFINITY)
            router2.update_routing_table(router1, None, INFINITY)

            self.invalidate_routes_for_removed_link(router1, router2)

    def invalidate_routes_for_removed_link(self, router1, router2):
        """
        Invalidates routes in the routing tables that depend on a removed link.

        Args:
            router1 (Router): The first router.
            router2 (Router): The second router.
        """
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
        """
        Prints the network information.
        """
        for router in self.routers:
            print(f"Router: {router}")
            print(f"Neighbors: {self.routers[router].neighbors}")
            print(f"Routing Table: {self.routers[router].routing_table}")

    def topology_output(self):
        """
        Writes the routing tables to the output file.
        """
        for router in sorted(self.routers.values(), key=lambda x: x.id):
            routing_table_str = router.get_routing_table_string()
            self.output_file_iterator.write(routing_table_str)
            self.output_file_iterator.write("\n")
    
    def send_messages(self, message_file):
        """
        Send messages between routers in the network.

        Args:
            network (Network): The network object representing the routers and their connections.
            message_file (str): The path to the file containing the messages to be sent.

        Returns:
            None
        """
        with open(message_file, 'r') as message_file_iterator:
            for line in message_file_iterator:
                router_id_from, router_id_to, message = line.split(" ", 2)
                self.send_message(int(router_id_from), int(router_id_to),message)
            self.output_file_iterator.write("\n\n")

    def send_message(self, router_id_from, router_id_to, message):
        """
        Sends a message from one router to another in the network.
        Writes the message to the output file.

        Args:
            router_id_from (int): The ID of the source router.
            router_id_to (int): The ID of the destination router.
            message (str): The message to send.
        
        """
        formatted_message = self._generate_message_string(router_id_from, router_id_to, message)
        self.output_file_iterator.write(formatted_message)
    
    def _generate_message_string(self, router_id_from, router_id_to, message):
        """
        Generates a message string formatted to be written to the output file.

        Args:
            router_id_from (int): The ID of the source router.
            router_id_to (int): The ID of the destination router.
            message (str): The message to send.

        Returns:
            str: The formatted message.
        """
        router_from = self.get_router(router_id_from)
        router_to = self.get_router(router_id_to)

        if self.check_impossible_to_reach(router_from, router_to):
            # impossible to reach
            formatted_message = f"from {router_id_from} to {router_id_to} cost infinite hops unreachable message {message}"
        else:
            hops, total_cost = self.get_hops_and_cost_from_to(router_from, router_to)
            hops_str = ' '.join(map(str, hops))
            formatted_message = f"from {router_id_from} to {router_id_to} cost {total_cost} hops {hops_str} message {message}"

        return formatted_message

    def get_hops_and_cost_from_to(self, router_from, router_to):
        """
        Calculates the hops and total cost to reach a destination router.

        Args:
            router_from (Router): The source router.
            router_to (Router): The destination router.

        Returns:
            tuple: A tuple containing the list of hops and the total cost.
        """
        next_hop, cost = router_from.routing_table[router_to.id]
        hops = [str(router_from.id)]
        total_cost = cost

        while next_hop != router_to.id:
            hops.append(str(next_hop))
            next_router = self.get_router(next_hop)
            next_hop, cost = next_router.routing_table[router_to.id]

        return hops, total_cost

    def check_impossible_to_reach(self, router_from, router_to):
        """
        Checks if it is impossible to reach a destination router from a source router.

        Args:
            router_from (Router): The source router.
            router_to (Router): The destination router.

        Returns:
            bool: True if it is impossible to reach, False otherwise.
        """
        if router_from is None or router_to is None:
            return True
        if router_to.id not in router_from.routing_table.keys() or router_from.routing_table[router_to.id][1] == INFINITY:
            return True
        return False

    def process_change(self, router_id1, router_id2, cost):
        """
        Processes a change in the network topology.

        Args:
            router_id1 (int): The ID of the first router.
            router_id2 (int): The ID of the second router.
            cost (int): The new cost of the link, or -999 to remove the link.
        """
        if cost == -999:
            if router_id1 not in self.routers.keys():
                self._add_router(router_id1)
            if router_id2 not in self.routers.keys():
                self._add_router(router_id2)
            router1 = self.get_router(router_id1)
            router2 = self.get_router(router_id2)

            self.remove_link(router1, router2)

        else:
            self.add_link(router_id1, router_id2, cost)
    
    def __del__(self):
        """
        Closes the output file when the Network object is deleted.
        """
        self.output_file_iterator.close()

## @}