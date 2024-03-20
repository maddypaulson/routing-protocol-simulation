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

    def distribute_lsp(self):
        # send the lsp to all other routers in the network
        for router1_id, router1 in self.routers.items():
            lsp = router1.generate_lsp()
            for router2_id, router2 in self.routers.items():
                if router1_id != router2_id:
                    router2.process_lsp(lsp)
                    # print(f"lsp sent from {router1_id} to {router2_id}\n")
                    # print(f"lsp:", lsp)
                    # print(f"\n")
    
    def apply_ls_all_routers(self):
        for router_id, router in self.routers.items():
            router.update_routing_table_dijkstra()