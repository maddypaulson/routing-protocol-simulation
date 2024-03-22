import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from LinkStateNetwork import LinkStateNetwork
from LinkStateRouter import LinkStateRouter
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
        output_path = Path(__file__).resolve().parent / "testfiles/output_file1.txt"

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
        output_path = Path(__file__).resolve().parent / "testfiles/output_file1.txt"

        network = LinkStateNetwork(str(topology_path), str(output_path))

        network.distribute_all_lsp()
        
        # Check the network topology of the routers
        self.assertDictEqual(network.routers[1].network_topology, network.routers[2].network_topology)
        self.assertDictEqual(network.routers[3].network_topology, network.routers[4].network_topology)
        self.assertNotEqual(network.routers[1].network_topology, network.routers[3].network_topology)
        self.assertEqual(network.routers[1].network_topology, network.routers[2].network_topology)
## @}

if __name__ == "__main__":
    unittest.main()
