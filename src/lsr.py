from LinkStateNetwork import LinkStateNetwork
from utilities import parseArgs

## @file
## Main file to run the Link State Routing Algorithm.
## @addtogroup LSR
def main():
    """
    Main function to run the Link State Routing Algorithm.

    Args:
        None

    Returns:
        None
    """
    args = parseArgs()
    topology_file, message_file, changes_file, output_file  = args

    network = LinkStateNetwork(topology_file, output_file)
    network.apply_changes_and_output(changes_file, message_file)
    
    # network.distribute_all_lsp()
    # network.apply_ls_all_routers()

if __name__ == "__main__":
    main()

## @}