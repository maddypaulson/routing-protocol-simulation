from LinkStateNetwork import LinkStateNetwork
from utilities import parseArgs

## @file
## @brief Main file to run the Link State Routing Algorithm.
## This script serves as the entry point for simulating a network utilizing the Link State Routing protocol.
##
## @author Maddy Paulson (maddypaulson)
## @author Leonardo Kamino Barros (LeonardoKamino)
## @bug No known bugs.
## @addtogroup LSR
def main():
    """
    Main function to run the Link State Routing Algorithm.

    Args:
        topology_file (str): The file containing the network topology.
        message_file (str): The file containing the messages to be sent.
        changes_file (str): The file containing the changes to be applied to the network.
        [output_file] (str): The file to output the results to.

    Returns:
        None
    """
    args = parseArgs()
    topology_file, message_file, changes_file, output_file  = args

    network = LinkStateNetwork(topology_file, output_file)
    network.apply_changes_and_output(changes_file, message_file)

if __name__ == "__main__":
    main()

## @}