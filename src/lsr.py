from LinkStateNetwork import LinkStateNetwork
from utilities import parseArgs

def main():
    """
    Main function to run the Distance Vector Algorithm.

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
    network.print_network()

if __name__ == "__main__":
    main()