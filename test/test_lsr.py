import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from LinkStateNetwork import LinkStateNetwork
from LinkStateRouter import LinkStateRouter
## @file
## Test file for LinkSateRouting.
## @addtogroup Tests
## @{

class TestLinkState(unittest.TestCase):
    def test_distribute_all_lsp_connected_graph(self):
        """
        \test
        Test case to verify the functionality of the distribute_all_lsp method.

        This test case creates a LinkStateNetwork object, representing a fully connected network and calls the distribute_all_lsp method.
        It then checks that all nodes have knowledge about all other nodes in the network.

        Test Steps:
        1. Create a LinkStateNetwork object with the given topology and output file paths.
        2. Call the distribute_all_lsp method to cdistribute knowledge in network.
        3. Check the nodes have correct knowledge of network.

        Expected Results:
        - All network topologies are equal.
        """

        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_distribute_all_lsp_connected.txt"

        network = LinkStateNetwork(str(topology_path), str(output_path))

        network.distribute_all_lsp()

        # Check the network topology of the routers
        self.assertDictEqual(network.routers[1].network_topology, network.routers[2].network_topology)
        self.assertDictEqual(network.routers[2].network_topology, network.routers[3].network_topology)
        self.assertDictEqual(network.routers[3].network_topology, network.routers[4].network_topology)

    def test_distribute_all_lsp_disconnected_graph(self):
        """
        Test case to verify the functionality of the distribute_all_lsp method.

        This test case creates a LinkStateNetwork object, representing a disconnected network and calls the distribute_all_lsp method.
        It then checks that  nodes have knowledge about all other nodes in their own network.

        Test Steps:
        1. Create a LinkStateNetwork object with the given topology and output file paths.
        2. Call the distribute_all_lsp method to cdistribute knowledge in network.
        3. Check the nodes have correct knowledge of network.

        Expected Results:
        - Nodes in same network have the same network topology.
        - Nodes in different networks have different network topologies.
        """

        topology_path = Path(__file__).resolve().parent / "testfiles/topology_disconnected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_distribute_all_lsp_disconnected.txt"

        network = LinkStateNetwork(str(topology_path), str(output_path))

        network.distribute_all_lsp()
        
        # Check the network topology of the routers
        self.assertDictEqual(network.routers[1].network_topology, network.routers[2].network_topology)
        self.assertDictEqual(network.routers[3].network_topology, network.routers[4].network_topology)
        self.assertNotEqual(network.routers[1].network_topology, network.routers[3].network_topology)
        self.assertEqual(network.routers[1].network_topology, network.routers[2].network_topology)
    
    def test_tie_break(self):
        """
        Test case for the tie breaking in the Link State Routing.

        This test case verifies the functionality of the tie breaking in the Link State Routing.
        It creates a LinkStateNetwork object, runs the distribute_all_lsp() method, and checks the routing tables.

        The test checks that the path with the lowest lexigraphuc is chosen in case of a time.
        The testfile topology_tie_break.txt contains the following topology with all edges equal to 1:
            3 - 4 - 5 - 6
              \    /
                2 
        Therefore routing table from 3 to 6 should have 2 as next hop. Since the path 3-4-5-6 and 3-2-5-6 have the same cost, the path 3-2-5-6 should be chosen as 2 < 4.

        Test Steps:
        1. Create a LinkStateNetwork object.
        2. Call the distribute_all_lsp method to spread info between router.
        3. Call the update_routing_table_dijkstra method to update the routing table of router 3.
        4. Check the routing table of the router 3.

        Expected Results:
        - The routing table router 3 has next hop as 2, not 4.
        """
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_tie_break.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))
        
        network.distribute_all_lsp()
        network.routers[3].update_routing_table_dijkstra()
        self.assertEqual(network.routers[3].routing_table[6], (2, 3))

    def test_tie_break_2(self):
        """
        Test case for the tie breaking in the Link State Routing.

        This test case verifies the functionality of the tie breaking in the Link State Routing after changes.
        It creates a LinkStateNetwork object, runs the distribute_all_lsp() method,apply changes, and checks the routing tables.

        The test checks that the lowest lexigraphic path is selected.
        The testfile topology_tie_break_2.txt contains the following topology (the number of lines is the cost of the edge):
            1 - 4 - 12 -- 9
                \        /
                  5     11 
        And the changes_tie_break_2.txt contains the following changes:
            5 11 1

        Therefore routing table from 4 to 9 should have 5 as next hop. Since the path 4-5-11-9 and 4-12-9 have the same cost, the path 4-5-11-9 should be chosen as 11 < 12.

        Test Steps:
        1. Create a LinkStateNetwork object.
        2. Call the distribute_all_lsp method to spread info between router.
        3. Call the update_routing_table_dijkstra method to update the routing table of router 4.
        4. Check the routing table of the router 4.
        5. Apply the changes.
        
        

        Expected Results:
        - The routing table router 3 has next hop as 2, not 4.
        """
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break_2.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_tie_break_2.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))
        
        network.distribute_all_lsp()
        network.routers[4].update_routing_table_dijkstra()
        self.assertEqual(network.routers[4].routing_table[9], (12, 3))

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_tie_break_2.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_tie_break_2.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        self.assertEqual(network.routers[4].routing_table[9], (5, 3))
        self.assertEqual(network.routers[5].routing_table[9], (11, 2))
## @}

if __name__ == "__main__":
    unittest.main()
