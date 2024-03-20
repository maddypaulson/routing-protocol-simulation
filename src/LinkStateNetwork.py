from Network import Network
from LinkStateRouter import LinkStateRouter 

class LinkStateNetwork(Network):
    def __init__(self, topology_file, output_file):
        super().__init__(topology_file, output_file)

    def add_router(self, router_id):
        """
        Adds a router to the network.

        Args:
            router_id (int): The ID of the router to add.
        """
        router = LinkStateRouter(router_id, self)
        self.routers[router.id] = router

    def distribute_all_lsp(self):
        # send the lsp to all other routers in the network
        for  router in self.routers.values():
            router.generate_lsp(self)
    

    # def apply_ls_all_routers(self):
    #     for router_id, router in self.routers.items():
    #         router.update_routing_table_dijkstra()           
            
    def apply_changes_and_output(self, changes_file, message_file):
        
        self.distribute_all_lsp()
        
        for router in self.routers.values():
            router.update_routing_table_dijkstra() 
            
        self.topology_output()
        self.send_messages(message_file)
        with open(changes_file, 'r') as changes_file:
            
            for line in changes_file:
                router_id1, router_id2, cost = line.split()
                self.process_change(int(router_id1), int(router_id2), int(cost))

                router_1 = self.get_router(int(router_id1))
                router_2 = self.get_router(int(router_id2))
                router_1.generate_lsp(self)
                router_2.generate_lsp(self)

                for router in self.routers.values():
                    router.update_routing_table_dijkstra() 
                self.topology_output()
                self.send_messages(message_file)