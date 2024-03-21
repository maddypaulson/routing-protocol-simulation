import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from DistanceVectorNetwork import DistanceVectorNetwork
from DistanceVectorRouter import DistanceVectorRouter
## @file
## Test file for Distance Vector Routing.
## @addtogroup Tests
## @{
class TestDistanceVectorRouter(unittest.TestCase):
    def test_update_routing_table(self):
        """
        Test case for the update_routing_table method of the DistanceVectorRouter class.

        This test case verifies the functionality of the update_routing_table method.
        It creates three DistanceVectorRouter objects and checks that the routing table is updated correctly.

        Test Steps:
        1. Create three DistanceVectorRouter objects.
        2. Call the update_routing_table method on one of the routers.
        3. Check that the routing table of  routers is updated correctly.

        Expected Results:
        - The routing table of routers is updated correctly.
        """
        router1 = DistanceVectorRouter(1)
        router2 = DistanceVectorRouter(2)
        router3 = DistanceVectorRouter(3)
        router1.update_routing_table(router2, router3, 10)
        self.assertEqual(router1.routing_table[router2.id], (router3.id, 10))
    
    def test_should_accept_message(self):
        """
        Test case for the should_accept_message method of the DistanceVectorRouter class.

        This test case verifies the functionality of the should_accept_message method.
        It creates three DistanceVectorRouter objects and checks that the message acceptance is determined correctly.

        Test Steps:
        1. Create three DistanceVectorRouter objects.
        2. Call the update_routing_table method on one of the routers.
        3. Check that the should_accept_message method returns the expected result.

        Expected Results:
        - The should_accept_message method returns the expected result.
        """
        router1 = DistanceVectorRouter(1)
        router2 = DistanceVectorRouter(2)
        router3 = DistanceVectorRouter(3)
        router1.update_routing_table(router2, router3, 10)
        self.assertTrue(router2.should_accept_message(router1, router3, 10))

class TestDistanceVectorNetwork(unittest.TestCase):
    def test_add_router(self):
        """
        Test case for the _add_router method of the DistanceVectorNetwork class.

        This test case verifies the functionality of the _add_router method.
        It creates a DistanceVectorNetwork object, adds a router, and checks that the router is added correctly.

        Test Steps:
        1. Create a DistanceVectorNetwork object.
        2. Call the _add_router method to add a non existing router.
        3. Check that the router is added to the network.

        Expected Results:
        - The router is added to the network.
        """
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/output_file1.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        network._add_router(22)
        self.assertIn(22, network.routers)

    def test_dv_algorithm(self):
        """
        Test case for the _dv_algorithm method of the DistanceVectorNetwork class.

        This test case verifies the functionality of the _dv_algorithm method.
        It creates a DistanceVectorNetwork object, runs the distance vector algorithm, and checks the routing tables.

        Test Steps:
        1. Create a DistanceVectorNetwork object.
        2. Call the _dv_algorithm method to run the distance vector algorithm.
        3. Check the routing tables of the routers.

        Expected Results:
        - The routing tables of the routers are updated correctly.
        """
        topology_path = Path(__file__).resolve().parent / "testfiles/topology_connected.txt"
        output_path = Path(__file__).resolve().parent / "testfiles/output_file1.txt"
        network = DistanceVectorNetwork(str(topology_path), str(output_path))
        
        network._dv_algorithm()
        print(network.routers[1].routing_table)
        self.assertEqual(network.routers[1].routing_table[3], (4, 9))
        self.assertEqual(network.routers[2].routing_table[1], (5, 6))
        self.assertEqual(network.routers[3].routing_table[4], (2, 8))
## @}

if __name__ == '__main__':
    unittest.main()

