import sys
import networkx as nx
import heapq

## @file
## File for a custom Dijkstra's algorithm to compare output with the Link State Routing algorithm.
## @addtogroup Tests
## @{

def parseArgs():
    """
    Parses the command line arguments and returns them as a list.

    Returns:
        list: A list containing the command line arguments.
    """
    if len(sys.argv) != 4:
        print("Usage: python your_script.py topology_file  message_file changes_file   ")
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

def print_messages_from_file(filename, graph, output_iterator):
    """
    Read and parse messages from a file.
    Each line of the file should be "from to message".
    """
    with open(filename,'r') as file:
        for line in file:
            from_node, to_node, message = line.split(" ", 2)
            lengths, paths = custom_dijkstra(graph, from_node)
            if paths[to_node]:
                path = paths[to_node]
                path_cost = lengths[to_node]
                hops = ' '.join(path[0:-1])
                output_iterator.write(f"from {from_node} to {to_node} cost {path_cost} hops {hops} message {message}")
            else:
                output_iterator.write(f"from {from_node} to {to_node} cost infinite hops unreachable message {message}")
        output_iterator.write(f"\n\n")
            


def apply_changes_from_file(graph, changes_filename, message_filename, output_iterator):
    """
    Apply changes to the graph based on a file.
    Each line of the file should be "node1 node2 cost",
    where a cost of -999 indicates the removal of a link.
    """
    with open(changes_filename, 'r') as file:
        for line in file:
            node1, node2, cost = line.split()
            cost = int(cost)
            if cost == -999:
                
                if graph.has_edge(node1, node2):
                    graph.remove_edge(node1, node2)
            else:
                graph.add_edge(node1, node2, weight=cost)

            print_routing_tables(graph, output_iterator)
            print_messages_from_file(message_filename, graph, output_iterator)

def custom_dijkstra(graph, source):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[source] = 0
    pq = [(0, source, [source])]  # (distance, node, path)
    paths = {source: [source]}

    while pq:
        current_distance, current_node, current_path = heapq.heappop(pq)
        if current_distance > distances[current_node]:
            continue

        for neighbor, edge_attrs in graph[current_node].items():
            new_distance = current_distance + edge_attrs.get('weight', 1)
            new_path = current_path + [neighbor]
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = new_path
                heapq.heappush(pq, (new_distance, neighbor, new_path))
            elif new_distance == distances[neighbor] and new_path[-2] < paths[neighbor][-2]:
                # If new path has the same distance but a lower penultimate node ID, update the path
                paths[neighbor] = new_path

    return distances, paths   


def print_routing_tables(graph, output_iterator):
    """
    Compute and print the routing table for each router.
    """
    for node in sorted(graph.nodes, key=lambda x: int(x)):
        lengths, paths = custom_dijkstra(graph, node)
        for target in sorted(graph.nodes, key=lambda x: int(x)):
            if target == node:
                next_hop = node
                cost = 0
            elif target in paths:
                next_hop = paths[target][1] if len(paths[target]) > 1 else target
                cost = lengths[target]
            else:
                continue
            output_iterator.write(f"{target} {next_hop} {cost}\n")
        output_iterator.write("\n")


# Main function to run the script
def main():
    args = parseArgs()
    topology_filename = args[0]
    changes_filename = args[2]
    message_filename = args[1]
    output_filename = 'output_test.txt'

    output_iterator = open(output_filename, 'w')
    

    graph = read_topology_from_file(topology_filename)
    print_routing_tables(graph, output_iterator)
    print_messages_from_file(message_filename, graph, output_iterator)
    apply_changes_from_file(graph, changes_filename, message_filename, output_iterator)
    
    output_iterator.close()

if __name__ == "__main__":
    main()

## @}