from Network import Network
from LinkStateRouter import LinkStateRouter 
## @file
## @brief Implementation of the LinkStateNetwork Class.
# This module defines the LinkStateNetwork class, which extends the Network base class to simulate 
# the operation of a network using the Link State routing protocol. It manages the creation and 
# interaction of LinkStateRouter objects to represent individual routers within the network. Key 
# functionalities include the initialization of the network topology from a given file, distribution 
# of Link State Packets (LSPs) to build a complete network topology view at each router, application 
# of Dijkstra's algorithm for routing table calculations, and handling of dynamic network changes and 
# message forwarding. This class demonstrates the core principles of Link State routing, including 
# global topology awareness and shortest-path routing, through the generation, distribution, and 
# processing of LSPs.
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup  LSR 
## @{
class LinkStateNetwork(Network):
    """
    Represents a network using the Link State routing algorithm.

    Inherits from the Network class.
    """

    def __init__(self, topology_file, output_file):
        """
        Initializes a LinkStateNetwork object.

        Args:
            topology_file (str): The file path of the topology file.
            output_file (str): The file path to write the output.
        """
        super().__init__(topology_file, output_file)
        self.distribute_all_lsp()

        for router in self.routers.values():
            router.update_routing_table_dijkstra()

    def _add_router(self, router_id):
        """
        Adds a router to the network.

        Args:
            router_id (int): The ID of the router to add.
        """
        router = LinkStateRouter(router_id, self.routers)
        self.routers[router.id] = router

    def distribute_all_lsp(self):
        """
        Distributes the Link State Packets (LSP) from all routers in the network.
        """
        for router in self.routers.values():
            router.generate_lsp()

    def apply_changes_and_output(self, changes_file, message_file):
        """
        Applies changes to the network and outputs the topology and messages.

        Args:
            changes_file (str): The file path of the changes file.
            message_file (str): The file path to write the messages.
        """

        self.topology_output()
        self.send_messages(message_file)

        with open(changes_file, 'r') as changes_file:
            for line in changes_file:
                router_id1, router_id2, cost = line.split()
               
                self.process_change(int(router_id1), int(router_id2), int(cost))

                router_1 = self.get_router(int(router_id1))
                router_2 = self.get_router(int(router_id2))
                router_1.generate_lsp()
                router_2.generate_lsp()

                for router in self.routers.values():
                    router.update_routing_table_dijkstra()

                self.topology_output()
                self.send_messages(message_file)

    def process_change(self, router_id1, router_id2, cost):
        """
        Processes a change in the network and distribute knowledge for all routers.

        Args:
            router_id1 (int): The ID of the first router.
            router_id2 (int): The ID of the second router.
            cost (int): The cost of the link between the routers.
        """
            
        super().process_change(router_id1, router_id2, cost)
        self.distribute_all_lsp()

## @}