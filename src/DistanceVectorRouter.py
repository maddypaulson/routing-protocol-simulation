from Router import Router

## @file DistanceVectorRouter.py
## @brief Implementation of the DistanceVectorRouter Class.
##
## This file defines the DistanceVectorRouter class, which extends the Router base class to implement
## router functionalities specific to the Distance Vector routing protocol. Key responsibilities include
## deciding whether to transmit or accept routing information based on the protocol's rules, enabling
## the iterative process of distance vector routing. The class plays a crucial role in the simulation of 
## Distance Vector networks by facilitating the update and updating of routing tables among neighboring 
## routers, adhering to the principles of distance vector routing for path determination and message forwarding.
##
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup DVR 
## @{
class DistanceVectorRouter(Router):
    """
    This class represents a Distance Vector Router.

    Inherits from the Router class.
    """

    def __init__(self, id):
        super().__init__(id)

    def should_transmit_message(self, neigbour_router, destination):
        """
        Check if a neighbor router should transmit a message to a destination router.

        Parameters:
        - neigbour_router (Router): The neighbor router.
        - destination (Router): The destination router.

        Returns:
        - bool: True if the message should be transmitted, False otherwise.
        """
        next_hop_id, cost = self.get_next_hop_cost(destination.id)
        if neigbour_router.id == destination.id:
            return False
        if neigbour_router.id == next_hop_id:
            return False
        return True
    
    def should_accept_message(self, advertiser_router, destination, cost):
        """
        Check if a router should accept a message from an advertiser router.
        
        Args:
            advertiser_router (Router): The advertiser router.
            destination (Router): The destination router.
            cost (int): The cost to reach the destination from the advertiser router.
        Returns:
            bool: True if the message should be accepted, False otherwise.
        """
        if destination.id not in self.routing_table.keys():
            return True
        if cost + advertiser_router.neighbors[self.id] < self.routing_table[destination.id][1]:
            return True
        elif cost + advertiser_router.neighbors[self.id] == self.routing_table[destination.id][1] and self.routing_table[destination.id][0]  and advertiser_router.id < self.routing_table[destination.id][0]:
            return True
        elif self.routing_table[destination.id][0] == advertiser_router.id and self.routing_table[destination.id][1] < cost + advertiser_router.neighbors[self.id]:
            return True 
        return False
    
## @}