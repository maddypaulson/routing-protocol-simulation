import sys
import networkx as nx

def parseArgs():
    """
    Parses the command line arguments and returns them as a list.

    Returns:
        list: A list containing the command line arguments.
    """
    if len(sys.argv) != 3:
        print("Usage: python your_script.py topology_file  changes_file")
        sys.exit(1)
    
    args = sys.argv[1:]

    return args

def read_topology_from_file(filename):
    """
    Read and parse a topology from a file.
    Each line of the file should be "node1 node2 cost".
    """
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            node1, node2, cost = line.split()
            graph.add_edge(node1, node2, weight=int(cost))
    return graph

def apply_changes_from_file(graph, filename):
    """
    Apply changes to the graph based on a file.
    Each line of the file should be "node1 node2 cost",
    where a cost of -999 indicates the removal of a link.
    """
    with open(filename, 'r') as file:
        for line in file:
            node1, node2, cost = line.split()
            cost = int(cost)
            if cost == -999:
                if graph.has_edge(node1, node2):
                    graph.remove_edge(node1, node2)
            else:
                graph.add_edge(node1, node2, weight=cost)
            print("Change applied \n")
            print_routing_tables(graph)
        

def print_routing_tables(graph):
    """
    Compute and print the routing table for each router.
    """
    for node in sorted(graph.nodes, key=lambda x: int(x)):
        lengths, paths = nx.single_source_dijkstra(graph, node)
        for target in sorted(graph.nodes, key=lambda x: int(x)):
            if target == node:
                next_hop = node
                cost = 0
            elif target in paths:
                next_hop = paths[target][1] if len(paths[target]) > 1 else target
                cost = lengths[target]
            else:
                pass
            print(f"{target} {next_hop} {cost}")
        print("")

# Main function to run the script
def main():
    args = parseArgs()
    topology_filename = args[0]
    changes_filename = args[1]

    graph = read_topology_from_file(topology_filename)
    print_routing_tables(graph)
    apply_changes_from_file(graph, changes_filename)
    

if __name__ == "__main__":
    main()
