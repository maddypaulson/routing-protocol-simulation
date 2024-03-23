import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from LinkStateNetwork import LinkStateNetwork
from LinkStateRouter import LinkStateRouter
from utilities import INFINITY
## @file
## @brief Test file for LinkStateRouting.
# This script includes unit tests for the Link State Routing (LSR) simulation, specifically testing the 
# distribution of Link State Packets (LSPs) across a network and verifying correct network topology knowledge 
# among routers. Tests cover scenarios with both fully connected and disconnected graphs, ensuring the 
# LinkStateNetwork and LinkStateRouter classes accurately implement LSR functionalities. Essential for validating 
# the integrity and correctness of LSR implementations in simulated network environments.
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup Tests
## @{

class TestLinkState(unittest.TestCase):
    ## @brief Test case to verify the verify the initialization of LinkStateNetwork.
    #
    # This test case creates a LinkStateNetwork object, representing a fully connected network.
    # It then checks that all nodes have knowledge about all other nodes in the network.
    #
    # Test Steps:
    # 1. Create a LinkStateNetwork object with the given topology and output file paths.
    # 2. Check the nodes have correct knowledge of network.
    #
    # Expected Results:
    # - All network topologies are equal.
    # @test Verifies the functionality of routers in networking distributing knowledge in network in a connected graph.

    def test_distribute_all_lsp_connected_graph(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_distribute_all_lsp_connected.txt"

        network = LinkStateNetwork(str(topology_path), str(output_path))

        network.distribute_all_lsp()

        # Check the network topology of the routers
        self.assertDictEqual(network.routers[1].network_topology, network.routers[2].network_topology)
        self.assertDictEqual(network.routers[2].network_topology, network.routers[3].network_topology)
        self.assertDictEqual(network.routers[3].network_topology, network.routers[4].network_topology)
     
    ## @brief Test case to verify the initialization of LinkStateNetwork in a disconnected graphs.
    #
    # This test case creates a LinkStateNetwork object, representing a disconnected network.
    # It then checks that  nodes have knowledge about all other nodes in their own network.
    #
    # Test Steps:
    # 1. Create a LinkStateNetwork object with the given topology and output file paths.
    # 2. Check the nodes have correct knowledge of network.
    #
    # Expected Results:
    # - Nodes in same network have the same network topology.
    # - Nodes in different networks have different network topologies.
    # @test Verifies the functionality of routers in networking distributing knowledge in network in a disconnected graph.
    def test_distribute_all_lsp_disconnected_graph(self):
       

        topology_path = Path(__file__).resolve().parent / "testfiles/topology_disconnected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_distribute_all_lsp_disconnected.txt"

        network = LinkStateNetwork(str(topology_path), str(output_path))
        
        # Check the network topology of the routers
        self.assertDictEqual(network.routers[1].network_topology, network.routers[2].network_topology)
        self.assertDictEqual(network.routers[3].network_topology, network.routers[4].network_topology)
        self.assertNotEqual(network.routers[1].network_topology, network.routers[3].network_topology)
        self.assertEqual(network.routers[1].network_topology, network.routers[2].network_topology)
     
    ## @brief Test case for the tie breaking in the Link State Routing.
    #
    # This test case verifies the functionality of the tie breaking in the Link State Routing.
    # It creates a LinkStateNetwork object, and checks the routing tables making sure correct tie break happened.
    #
    # The test checks that the path with the lowest lexigraphuc is chosen in case of a time.
    # The testfile topology_tie_break.txt contains the following topology with all edges equal to 1:
    #     3 - 4 - 5 - 6
    #         \    /
    #         2 
    # Therefore routing table from 3 to 6 should have 2 as next hop. Since the path 3-4-5-6 and 3-2-5-6 have the same cost, the path 3-2-5-6 should be chosen as 2 < 4.
    #
    # Test Steps:
    # 1. Create a LinkStateNetwork object.
    # 2. Check the routing table of the router 3.
    #
    # Expected Results:
    # - The routing table router 3 has next hop as 2, not 4.
    #@test Verifies the functionality of the tie breaking in the Link State Routing when 2 paths has same cost.
    def test_tie_break(self):
       
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_tie_break.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))

        self.assertEqual(network.routers[3].routing_table[6], (2, 3))

    ## @brief Test case for the tie breaking in the Link State Routing.
    #
    # This test case verifies the functionality of the tie breaking in the Link State Routing after changes.
    # It creates a LinkStateNetwork object, apply changes, and checks the routing tables.
    #
    # The test checks that the lowest lexigraphic path is selected.
    # The testfile topology_tie_break_2.txt contains the following topology (the number of lines is the cost of the edge):
    #     1 - 4 - 12 -- 9
    #         \        /
    #           5     11 
    # And the changes_tie_break_2.txt contains the following changes:
    #     5 11 1
    #
    # Therefore routing table from 4 to 9 should have 5 as next hop. Since the path 4-5-11-9 and 4-12-9 have the same cost, the path 4-5-11-9 should be chosen as 11 < 12.
    #
    # Test Steps:
    # 1. Create a LinkStateNetwork object.
    # 2. Check the routing table of the router 4.
    # 3. Apply the changes.
    #
    # Expected Results:
    # - The routing table router 3 has next hop as 2, not 4.
    #@test Verifies the functionality of updating topology and the tie breaking in the Link State Routing when new route has same cost as old path.
    def test_tie_break_after_changes(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break_2.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_tie_break_2.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))
        
        self.assertEqual(network.routers[4].routing_table[9], (12, 3))

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_tie_break_2.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_tie_break_2.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        self.assertEqual(network.routers[4].routing_table[9], (5, 3))
        self.assertEqual(network.routers[5].routing_table[9], (11, 2))
    
    ## @brief Test case for verifying routing and messaging in Link State Routing after topology changes.
    #
    # This test case assesses the Link State Routing (LSR) algorithm's response to topology changes, specifically focusing on the accuracy of routing table updates and message handling when a link becomes unreachable.
    #
    # Initially, a simple network topology is set up where router 1 is directly connected to router 2. The test verifies that messages are correctly routed based on the initial topology. 
    # Then, a change is applied to simulate the removal of the link between routers 1 and 2, and the test checks that subsequent routing tables and messages reflect this disconnection appropriately.
    #
    # The initial setup:
    # - A direct link between routers 1 and 2 with a cost of 6.
    #
    # The change applied:
    # - The link between routers 1 and 2 is removed, denoted by a special cost value of `-999` in `changes_single.txt`.
    #
    # Test Steps:
    # 1. Create a `LinkStateNetwork` object with the initial topology.
    # 2. Verify the initial routing table for router 1 entry.
    # 3. Verify that a message sent from router 2 to router 1 correctly indicates the cost and hops based on the initial topology.
    # 4. Apply the topology change to remove the link between routers 1 and 2.
    # 5. Verify that the routing table for router 1 reflects the disconnection by marking router 2 as unreachable.
    # 6. Verify that a message attempted after the link removal correctly indicates that router 1 is unreachable from router 2.
    #
    # Expected Results:
    # - Before applying the change, messages between routers 1 and 2 indicate the correct cost and hop based on the initial topology.
    # - After the change, the routing table entry for router 2 in router 1's routing table is marked with an infinite cost, indicating it's unreachable.
    # - Messages attempted after the link removal correctly report the destination as unreachable, with an "infinite cost" and "unreachable" hops.
    #@test Ensures LSR accurately updates routing tables and handles messages in response to topology changes.    
    def test_ls_algorithm_single_router(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_single.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_single.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))
        
        self.assertEqual(network.routers[1].routing_table[2], (2,6))
        
        # Verify that the message is correct before changes
        expectedAfter = "from 2 to 1 cost 6 hops 2 message How are you?"
        resultAfter = network._generate_message_string(2, 1, "How are you?")
        self.assertEqual(expectedAfter, resultAfter)
        
        changes_path = Path(__file__).resolve().parent / "testfiles/changes_single.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_single.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        # Verify that the link is no longer there, stored as infinity in our routing table
        self.assertTrue(network.routers[1].routing_table.get(2, (None, INFINITY))[1] == INFINITY)
        
        # Verify that the message is correct after the link is removed
        expectedAfter = "from 2 to 1 cost infinite hops unreachable message How are you?"
        resultAfter = network._generate_message_string(2, 1, "How are you?")
        self.assertEqual(expectedAfter, resultAfter)

    ## @brief Test case for sending messages between disconnected nodes that are later connected.
    #
    # This test case verifies the functionality of sending messages between disconnected nodes that are later connected.
    # It creates a LinkStateNetwork object, applies changes, and checks the messages.
    #
    # The testfile topology_disconnected_to_connected.txt contains the following topology (the number of lines is the cost of the edge):
    #   1 - 2--4   5 - 6
    #     \ | /
    #       3
    # The testfile changes_disconnected_to_connected.txt contains the following changes:
    #   4 5 1
    #
    # The resultiing topology would be
    #   1 - 2--4 - 5 - 6
    #     \ | /
    #       3    
    # 
    # Test Steps:
    # 1. Create a LinkStateNetwork object.
    # 2. Check message from 1 - 6 to show it is impossible to reach.
    # 3. Apply the changes.
    # 4. Check message from 1 - 6 to show it is possible to reach and has hops 1 - 3 - 4 - 5.
    #
    # Expected Results:
    # - Before changes, the message from 1 to 6 shows it is impossible to reach.
    # - After messages, the message from 1 to 6 shows it is possible to reach and has hops 1 3 4 5.  
    # @test Testing creating messages string between nodes before and after they are connected.  
    def test_disconnected_to_connected_messages(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_disconnected_to_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_disconnected_to_connected.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))

        message_str = network._generate_message_string(1, 6, "hello")
        self.assertEqual("from 1 to 6 cost infinite hops unreachable message hello", message_str)

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_disconnected_to_connected.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_disconnected_to_connected.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        message_str = network._generate_message_string(1, 6, "hello")
        self.assertEqual("from 1 to 6 cost 4 hops 1 3 4 5 message hello", message_str)
    
    ## @brief Test case for sending messages between connected nodes that are later disconnected.
    #
    # This test case verifies the functionality of sending messages between connected nodes that are later disconnected.
    # It creates a LinkStateNetwork object, update router routing table, applies changes, and checks the messages.
    #
    # The testfile topology_connected_to_disconnected.txt contains the following topology (the number of lines is the cost of the edge):
    #   1 - 2--4 - 5
    #     \ | /
    #       3
    # The testfile changes_connected_to_disconnected.txt contains the following changes:
    #   3 4 -999
    #   4 5 -999
    #   
    #   
    # The resulting topology would be
    #   1 - 2--4  5
    #     \ |
    #       3
    #
    # Test Steps:
    # 1. Create a LinkStateNetwork object.
    # 2. Check message from 1 - 5 to show it is possible to reach through hops 1 3 4.
    # 3. Apply the changes.
    # 4. Check message from 1 - 5 to show it is impossible to reach.
    #
    # Expected Results:
    # - Before changes, the message from 1 to 6 shows it is possible to reach.
    # - After messages, the message from 1 to 6 shows it is impossible to reach.
    # @test Testing creating messages string between nodes before and after they are disconnected.
    def test_connected_to_disconnected(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected_to_disconnected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_connected_to_disconnected.txt"
        network = LinkStateNetwork(str(topology_path), str(output_path))
        
        message_str = network._generate_message_string(1, 5, "hello")
        self.assertEqual("from 1 to 5 cost 3 hops 1 3 4 message hello", message_str)

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_connected_to_disconnected.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_connected_to_disconnected.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        message_str = network._generate_message_string(1, 5, "hello")
        self.assertEqual("from 1 to 5 cost infinite hops unreachable message hello", message_str)
## @}

if __name__ == "__main__":
    unittest.main()
