from Network import Network
from DistanceVectorRouter import DistanceVectorRouter 

## @file DistanceVectorNetwork.py
## @brief Implementation of the Distance Vector Network class for routing simulation.
##
## This module contains the definition and implementation of the DistanceVectorNetwork class,
## which simulates a network using the Distance Vector routing protocol. It inherits from
## the Network base class and integrates the DistanceVectorRouter class to represent individual
## routers within the network. The DistanceVectorNetwork class is responsible for initializing
## the network topology from a given topology file, applying topology changes, executing the
## Distance Vector algorithm to update routing tables across routers, and facilitating the
## transmission of messages based on the updated routing tables. Key operations include network
## initialization, routing table updates, and message handling according to the Distance Vector
## routing principles.
##
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup DVR 
## @{
class DistanceVectorNetwork(Network):
    """
    Represents a network using the Distance Vector routing algorithm.

    Inherits from the Network class.

    """

    def __init__(self, topology_file, output_file):
        super().__init__(topology_file, output_file)
        self._dv_algorithm()


    def _add_router(self, router_id):
        """
        Adds a router to the network.

        Args:
            router_id (int): The ID of the router to add.
        """
        router = DistanceVectorRouter(router_id)
        self.routers[router.id] = router


    def apply_changes_and_output(self, changes_file, message_file):
        """
        Apply changes to the network and output the network state.

        Args:
            changes_file (str): The path to the file containing the changes to be applied.
            message_file (str): The path to the file containing the messages to be sent.

        Returns:
            None
        """
        self.topology_output()
        self.send_messages(message_file)
        with open(changes_file, 'r') as changes_file:
            
            for line in changes_file:
                router_id1, router_id2, cost = line.split()
                self.process_change(int(router_id1), int(router_id2), int(cost))

                router_1 = self.get_router(int(router_id1))
                router_2 = self.get_router(int(router_id2))

                self._notify_neighbors(router_1, router_2)
                self._notify_neighbors(router_2, router_1)

                self._invalidate_expired_routes()

                self._dv_algorithm()
                self.topology_output()
                self.send_messages(message_file)

    def _dv_algorithm(self):
        """
        Distance Vector Algorithm implementation.

        Returns:
            None
        """
        # Initialize a flag to keep track of changes
        changes_made = True
        
        while changes_made:
            changes_made = False

            # Iterate over each router in the network
            for router in self.routers.values():
                # Iterate over each neighbor of the router
                for neighbor in router.neighbors.keys():
                    # Get the neighbor router object
                    neighbor_router = self.routers[neighbor]
                    
                    # Iterate over each destination in the routing table of the router
                    for destination in router.routing_table.keys():
                        # Get the next hop and cost to reach the destination from the router
                        destination_router = self.routers[destination]
                        if router.should_transmit_message(neighbor_router, destination_router):
                            next_hop_id, cost = router.routing_table[destination_router.id]
                            if  neighbor_router.should_accept_message( router, destination_router, cost):
                                # Update the routing table of the neighbor
                                neighbor_router.update_routing_table(destination_router, router, cost + router.neighbors[neighbor])
                                changes_made = True

    def _notify_neighbors(self, router, destination_router):
        """
        Notify the neighbors of a router about a change in the routing table.
        Way to simulate the poison reverse.

        Args:
            router (Router): The router that has a change in its routing table.
            destination_router (Router): The router that is the destination of the change.

        Returns:
            None
        """
        for neighbor in router.neighbors.keys():
            neighbor_router = self.routers[neighbor]
            if router.should_transmit_message(neighbor_router, destination_router):
                next_hop_id, cost = router.get_next_hop_cost(destination_router.id)
                if  neighbor_router.should_accept_message( router, destination_router, cost):
                    # Update the routing table of the neighbor
                    neighbor_router.update_routing_table(destination_router, router, cost + router.neighbors[neighbor])
                    self._notify_neighbors(neighbor_router, destination_router)

    def _invalidate_expired_routes(self):
        """
        Invalidate routes in the routing tables of all routers in the network.
        Except for the neighbors of the routers. 
        Way to simulate the timeout.

        Returns:
            None
        """
        for router in self.routers.values():
            for destination_id in router.routing_table.keys():
                if destination_id not in router.neighbors.keys() and router.id != destination_id:
                    router.routing_table[destination_id] = (None, float('inf'))

## @}