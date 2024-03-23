import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from DistanceVectorNetwork import DistanceVectorNetwork
from DistanceVectorRouter import DistanceVectorRouter
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

    ## @brief Test case for the _dv_algorithm method of the DistanceVectorNetwork class.
    #
    # This test case verifies the functionality of the _dv_algorithm method.
    # It creates a DistanceVectorNetwork object, runs the distance vector algorithm, and checks the routing tables.
    #
    # Test Steps:
    # 1. Create a DistanceVectorNetwork object.
    # 2. Call the _dv_algorithm method to run the distance vector algorithm.
    # 3. Check the routing tables of the routers.
    #
    # Expected Results:
    # - The routing tables of the routers are updated correctly.
    # @test This test case verifies the functionality of the _dv_algorithm method.
    def test_dv_algorithm(self):
        
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
    # It creates a DistanceVectorNetwork object, runs the distance vector algorithm, and checks the routing tables.
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
    # 2. Call the _dv_algorithm method to run the distance vector algorithm.
    # 3. Check the routing table of the router 3.
    #
    # Expected Results:
    # - The routing table router 3 has next hop as 2, not 4.
    # @test This test case verifies the functionality of the tie breaking in DistanceVectorNetwork class if 2 routes has same cost.
    def test_tie_break(self):
        
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_tie_break.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        network._dv_algorithm()
        self.assertEqual(network.routers[3].routing_table[6], (2, 3))

    ##@brief Test case for changing topology and tie breaking in the _dv_algorithm method of the DistanceVectorNetwork class.
    #
    # This test case verifies the functionality of the tie breaking in the _dv_algorithm method.
    # It creates a DistanceVectorNetwork object, runs the distance vector algorithm, and checks the routing tables.
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
    # 2. Call the _dv_algorithm method to run the distance vector algorithm.
    # 3. Check the routing table of the router 3.
    #
    # Expected Results:
    # - The routing table router 3 has next hop as 2, not 4.
    # @test This test case verifies the functionality of updating topology and the tie breaking of the DistanceVectorNetwork class when a new path has same cost as the previous selected path.
    def test_tie_break_after_change(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_tie_break_2.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_tie_break_2.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        network._dv_algorithm()
        self.assertEqual(network.routers[4].routing_table[9], (12, 3))

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_tie_break_2.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_tie_break_2.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        self.assertEqual(network.routers[4].routing_table[9], (5, 3))

    ## @brief Test case for sending messages between disconnected nodes that are later connected.
    #
    # This test case verifies the functionality of sending messages between disconnected nodes that are later connected.
    # It creates a DistanceVectorNetwork object, runs the distance vector algorithm, applies changes, and checks the messages.
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
    # 2. Call the _dv_algorithm method to run the distance vector algorithm.
    # 3. Check message from 1 - 6 to show it is impossible to reach.
    # 4. Apply the changes.
    # 5. Check message from 1 - 6 to show it is possible to reach and has hops 1 - 3 - 4 - 5.
    #
    # Expected Results:
    # - Before changes, the message from 1 to 6 shows it is impossible to reach.
    # - After messages, the message from 1 to 6 shows it is possible to reach and has hops 1 3 4 5.  
    # @test Testing creating messages string between nodes before and after they are connected.  
    def test_disconnected_to_connected_messages(self):
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_disconnected_to_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/outputs/dvr/output_disconnected_to_connected.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        network._dv_algorithm()
        message_str = network._generate_message_string(1, 6, "hello")
        self.assertEqual("from 1 to 6 cost infinite hops unreachable message hello", message_str)

        changes_path = Path(__file__).resolve().parent / "testfiles/changes_disconnected_to_connected.txt"
        message_path = Path(__file__).resolve().parent / "testfiles/message_disconnected_to_connected.txt"

        network.apply_changes_and_output(str(changes_path), str(message_path))

        message_str = network._generate_message_string(1, 6, "hello")
        self.assertEqual("from 1 to 6 cost 4 hops 1 3 4 5 message hello", message_str)

        
## @}

if __name__ == '__main__':
    unittest.main()

