import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from DistanceVectorNetwork import DistanceVectorNetwork
from DistanceVectorRouter import DistanceVectorRouter
from utilities import INFINITY
## @file
## @brief Test file for Distance Vector Routing.
# Contains tests for the DistanceVectorRouting simulation, focusing on routing table updates, 
# message handling, and network changes. Ensures the DistanceVectorNetwork and DistanceVectorRouter 
# classes operate correctly, adhering to DVR principles. A key tool for validating DVR simulation 
# accuracy and reliability.
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup Tests
## @{
class TestDistanceVectorRouter(unittest.TestCase):
    ## @brief Test case for the update_routing_table method of the DistanceVectorRouter class.
    #
    # This test case verifies the functionality of the update_routing_table method.
    # It creates three DistanceVectorRouter objects and checks that the routing table is updated correctly.
    #
    # Test Steps:
    # 1. Create three DistanceVectorRouter objects.
    # 2. Call the update_routing_table method on one of the routers.
    # 3. Check that the routing table of  routers is updated correctly.
    #
    # Expected Results:
    # - The routing table of routers is updated correctly.
    # @test This test case verifies updating the routing table of a router.
    def test_update_routing_table(self):
        
        router1 = DistanceVectorRouter(1)
        router2 = DistanceVectorRouter(2)
        router3 = DistanceVectorRouter(3)
        router1.update_routing_table(router2, router3, 10)
        self.assertEqual(router1.routing_table[router2.id], (router3.id, 10))
    
    ## @brief Test case for the should_accept_message method of the DistanceVectorRouter class.
    #
    # This test case verifies the functionality of the should_accept_message method.
    # It creates three DistanceVectorRouter objects and checks that the message acceptance is determined correctly.
    #
    # Test Steps:
    # 1. Create three DistanceVectorRouter objects.
    # 2. Call the update_routing_table method on one of the routers.
    # 3. Check that the should_accept_message method returns the expected result.
    #
    # Expected Results:
    # - The should_accept_message method returns the expected result.
    # @test This test case verifies the decision of router in accepting or not a message it receives.
    def test_should_accept_message(self):
        router1 = DistanceVectorRouter(1)
        router2 = DistanceVectorRouter(2)
        router3 = DistanceVectorRouter(3)
        router1.update_routing_table(router2, router3, 10)
        self.assertTrue(router2.should_accept_message(router1, router3, 10))

class TestDistanceVectorNetwork(unittest.TestCase):
    ## @brief Test case for the _add_router method of the DistanceVectorNetwork class.
    #
    # This test case verifies the functionality of the _add_router method.
    # It creates a DistanceVectorNetwork object, adds a router, and checks that the router is added correctly.
    #
    # Test Steps:
    # 1. Create a DistanceVectorNetwork object.
    # 2. Call the _add_router method to add a non existing router.
    # 3. Check that the router is added to the network.
    #
    # Expected Results:
    # - The router is added to the network.
    # @test This test case verifies the functionality of the adding a router to network.
    def test_add_router(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_add_router.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        network._add_router(22)
        self.assertIn(22, network.routers)

    ## @brief Test case for the DistanceVectorNetwork object initializations.
    #
    # This test case verifies the functionality of the _dv_algorithm method.
    # It creates a DistanceVectorNetwork object, and checks if the routing tables are initialized correctly.
    #
    # Test Steps:
    # 1. Create a DistanceVectorNetwork object.
    # 2. Check the routing tables of the routers.
    #
    # Expected Results:
    # - The routing tables of the routers are updated correctly.
    # @test This test case verifies the functionality of the _dv_algorithm method.
    def test_initialize_dv_network(self):
        
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_test_dv_algorithm.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        network._dv_algorithm()
        self.assertEqual(network.routers[1].routing_table[3], (4, 9))
        self.assertEqual(network.routers[2].routing_table[1], (5, 6))
        self.assertEqual(network.routers[3].routing_table[4], (2, 8))
    
    ## @brief Test case for the tie breaking in the _dv_algorithm method of the DistanceVectorNetwork class.
    #
    # This test case verifies the functionality of the tie breaking in the _dv_algorithm method.
    # It creates a DistanceVectorNetwork object, and checks the routing tables looking for specifics results due to tie-break.
    #
    # The test checks that the router with the lowest ID is chosen as the next hop in case of a tie.
    # The testfile topology_tie_break.txt contains the following topology with all edges equal to 1:
    #     3 - 4 - 5 - 6
    #       \    /
    #         2 
    # Therefore routing table from 3 to 6 should have 2 as next hop.
    #
    # Test Steps:
    # 1. Create a DistanceVectorNetwork object.
    # 2. Check the routing table of the router 3.
    #
    # Expected Results:
    # - The routing table router 3 has next hop as 2, not 4.
    # @test This test case verifies the functionality of the tie breaking in DistanceVectorNetwork class if 2 routes has same cost.
    def test_tie_break(self):
        
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_tie_break.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        self.assertEqual(network.routers[3].routing_table[6], (2, 3))

    ##@brief Test case for changing topology and tie breaking in the _dv_algorithm method of the DistanceVectorNetwork class.
    #
    # This test case verifies the functionality of the tie breaking in the _dv_algorithm method.
    # It creates a DistanceVectorNetwork object, and checks the routing tables.
    #
    # The test checks that the router with the lowest ID is chosen as the next hop in case of a tie.
    # The testfile topology_tie_break.txt contains the following topology with all edges equal to 1:
    #     3 - 4 - 5 - 6
    #       \    /
    #         2 
    # Therefore routing table from 3 to 6 should have 2 as next hop.
    #
    # Test Steps:
    # 1. Create a DistanceVectorNetwork object.
    # 2. Check the routing table of the router 3.
    #
    # Expected Results:
    # - The routing table router 3 has next hop as 2, not 4.
    # @test This test case verifies the functionality of updating topology and the tie breaking of the DistanceVectorNetwork class when a new path has same cost as the previous selected path.
    def test_tie_break_after_change(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break_2.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_tie_break_2.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        self.assertEqual(network.routers[4].routing_table[9], (12, 3))

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_tie_break_2.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_tie_break_2.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        self.assertEqual(network.routers[4].routing_table[9], (5, 3))

    ## @brief Test case for sending messages between disconnected nodes that are later connected.
    #
    # This test case verifies the functionality of sending messages between disconnected nodes that are later connected.
    # It creates a DistanceVectorNetwork object, applies changes, and checks the messages.
    #
    # The testfile topology_disconnected_to_connected.txt contains the following topology:
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
    # 1. Create a DistanceVectorNetwork object.
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
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_disconnected_to_connected.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
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
    # It creates a DistanceVectorNetwork object, update router routing table, applies changes, and checks the messages.
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
    # 1. Create a DistanceVectorNetwork object.
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
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_connected_to_disconnected.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        message_str = network._generate_message_string(1, 5, "hello")
        self.assertEqual("from 1 to 5 cost 3 hops 1 3 4 message hello", message_str)

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_connected_to_disconnected.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_connected_to_disconnected.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        message_str = network._generate_message_string(1, 5, "hello")
        self.assertEqual("from 1 to 5 cost infinite hops unreachable message hello", message_str)
    ## @brief Test case for verifying routing and messaging in Distance Vector Routing after topology changes.
    #
    # This test case examines the Distance Vector Routing (DVR) algorithm's adaptability to changes in the network topology, especially focusing on how routing tables and message delivery are affected when a link becomes unreachable.
    #
    # The initial network setup involves a straightforward connection between two routers. This setup tests the basic routing capabilities and message delivery based on the initial topology. Subsequently, a change simulates the disconnection of a link between these routers, and the test evaluates how well the subsequent routing tables and message deliveries reflect this topology alteration.
    #
    # Initial Setup:
    # - A direct link connects routers 1 and 2 with a cost of 6.
    #
    # Applied Change:
    # - The direct link between routers 1 and 2 is removed, represented by a cost value of `-999` in `changes_single.txt`, effectively making the destination unreachable through the previous direct path.
    #
    # Test Steps:
    # 1. Instantiate a `DistanceVectorNetwork` object with the predefined topology.
    # 2. Confirm the initial routing table for router 1 accurately reflects the direct connection to router 2.
    # 3. Verify that a message from router 2 to router 1 correctly shows the cost and path based on the initial topology setup.
    # 4. Implement the network change to sever the link between routers 1 and 2.
    # 5. Check that router 1's routing table updates to mark router 2 as unreachable following the disconnection.
    # 6. Attempt to send a message post-change and validate that it accurately indicates the unreachability of router 1 from router 2.
    #
    # Expected Results:
    # - Prior to applying the topology change, messages sent between routers 1 and 2 should correctly reflect the initial cost and direct path.
    # - Following the change, the routing table entry for router 2 in router 1's table should be updated to show an infinite cost, signifying it's unreachable.
    # - Subsequent message attempts should correctly identify the destination as unreachable, highlighted by an "infinite cost" and "unreachable" status for the path.
    #@test Validates that DVR efficiently updates routing tables and manages message routing in light of topology changes.
    def test_dv_algorithm_single_router(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_single.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_single.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        network._dv_algorithm()
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
    ## @brief Test case for DVR in a circular network topology with specific topology changes.
    #
    # This test scrutinizes the DVR algorithm within a 5-node circular topology, focusing on accurate shortest path determination and routing table/message path updates following specific topology changes. The setup and changes provide a nuanced view of DVR's response to complex network dynamics.
    #
    # Initial Setup:
    # - A 5-node network forms a circular topology, with links established between adjacent nodes and specified costs: 1-2 (cost 4), 2-3 (cost 6), 3-4 (cost 8), 4-5 (cost 2), and 5-1 (cost 10).
    #
    # Test Objectives:
    # 1. Confirm initial shortest path computations match expectations: 1 to 4 should route via 5 with a total cost of 12, underscoring DVR's initial path optimization.
    # 2. Check initial message routing accuracy, such as a message from 1 to 5 should ideally follow the direct path with a cost of 10.
    # 3. Apply predefined topology changes, potentially including both link removals and additions, to challenge the network's existing routing decisions.
    # 4. Assess how DVR algorithm updates the routing tables and message routing in light of the network alterations, ensuring changes yield correct new shortest paths and costs.
    #
    # Expected Outcomes:
    # - Before applying changes, routing tables and message delivery paths should align with DVR's optimization for the circular setup.
    # - Subsequent to the changes, expect DVR to recalibrate routing tables and message paths to reflect the most efficient routes given the new topology, such as adjusting the path and cost from 1 to 5 since there is now a direct path for a cost of 3.
    #@test Validates DVR's effectiveness and dynamic adjustment capability in a circular network subjected to specific topology alterations.
    def test_dvr_circular(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_circular.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/lsr/output_circular.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))

        network._dv_algorithm()
        
        # First check that the correct shortest paths were found
        self.assertEqual(network.routers[1].routing_table[4], (5,12))
        self.assertEqual(network.routers[4].routing_table[3], (3,8))
        self.assertEqual(network.routers[2].routing_table[2], (2,0))
        
        # Verify message before change
        expectedBefore = "from 1 to 5 cost 10 hops 1 message Testing"
        resultBefore = network._generate_message_string(1, 5, "Testing")
        self.assertEqual(expectedBefore, resultBefore)

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_circular.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_circular.txt"
        network.apply_changes_and_output(changes_path, message_path)
        
        # Check routing tables after changes
        self.assertEqual(network.routers[1].routing_table[5], (2,7))
        self.assertEqual(network.routers[3].routing_table[4], (2,11))
        self.assertEqual(network.routers[2].routing_table[5], (5,3))
        
        # Verify message and correct path 
        expectedAfter = "from 1 to 5 cost 7 hops 1 2 message Testing"
        resultAfter = network._generate_message_string(1, 5, "Testing")
        self.assertEqual(expectedAfter, resultAfter)
        
## @}

if __name__ == '__main__':
    unittest.main()

