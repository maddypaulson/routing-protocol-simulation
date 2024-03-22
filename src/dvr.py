from DistanceVectorNetwork import DistanceVectorNetwork
from utilities import parseArgs

## @file
## @brief Main file to run the Distance Vector Routing Algorithm.
##
## This script serves as the entry point for simulating a network utilizing the Distance Vector Routing protocol.
##
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup DVR 
## @{
def main():
    """
    Main function to run the Distance Vector Routing Algorithm.

    Args:
        None

    Returns:
        None
    """
    args = parseArgs()
    topology_file, message_file, changes_file, output_file  = args

    network = DistanceVectorNetwork(topology_file, output_file)
    network.apply_changes_and_output(changes_file, message_file)


if __name__ == "__main__":
    main()

## @}