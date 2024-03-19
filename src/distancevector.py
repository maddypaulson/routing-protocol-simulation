from network import Network, parseArgs

def dv_algorithm(network, priority_routers = []):
    # Make all routers send their routing table to their neighbors, except the one that is the destination or the one that is the next hop
    # Update the routing table of the neighbors
    # Repeat until no changes are made
    # Neighbor should not accept changes if it already has a better route. It should always update if it is receiving a message from the router that is its current destination

    # Initialize a flag to keep track of changes
    changes_made = True
    
    while changes_made:
        changes_made = False
        routers = priority_routers + [v for k, v in network.routers.items() if v not in priority_routers]

        # Iterate over each router in the network
        for router in routers:
            # Iterate over each neighbor of the router
            for neighbor in router.neighbors.keys():
                # Get the neighbor router object
                neighbor_router = network.routers[neighbor]
                
                # Iterate over each destination in the routing table of the router
                for destination in router.routing_table.keys():
                    # Get the next hop and cost to reach the destination from the router
                    next_hop_id, cost = router.routing_table[destination]
                    destination_router = network.routers[destination]
                    if should_transmit_message(neighbor_router, destination_router, next_hop_id):
                        if  should_accept_message(neighbor_router, router, destination_router, next_hop_id, cost):
                            # Update the routing table of the neighbor
                            neighbor_router.update_routing_table(destination_router, router, cost + router.neighbors[neighbor])
                            changes_made = True

def should_transmit_message(neigbour_router, destination, next_hop_id):
    if neigbour_router.id == destination.id:
        return False
    if neigbour_router.id == next_hop_id:
        return False
    return True

def should_accept_message(router, advertiser, destination, next_hop_id, cost):
    if destination.id not in router.routing_table.keys():
        return True
    if cost + advertiser.neighbors[router.id] < router.routing_table[destination.id][1]:
        return True
    if cost + advertiser.neighbors[router.id] == router.routing_table[destination.id][1] and router.routing_table[destination.id][0]  and advertiser.id < router.routing_table[destination.id][0]:
        return True
    if router.routing_table[destination.id][0] == advertiser.id and router.routing_table[destination.id][1] < cost + advertiser.neighbors[router.id]:
        return True
    return False

def main():
    args = parseArgs()
    topology_file, message_file, changes_file, output_file  = args

    network = Network(topology_file)
    dv_algorithm(network)
    network.topology_output(output_file)
    network.print_network()
    with open(message_file, 'r') as message_file_iterator:
                for line in message_file_iterator:
                    router_id_from, router_id_to, message = line.split(" ", 2)
                    network.send_message(int(router_id_from), int(router_id_to),message, output_file)
    # with open(changes_file, 'r') as changes_file:
    #     for line in changes_file:
    #         router_id1, router_id2, cost = line.split()
    #         network.process_change(int(router_id1), int(router_id2), int(cost))
    #         router_1 = network.get_router(int(router_id1))
    #         router_2 = network.get_router(int(router_id2))
    #         dv_algorithm(network, [router_1, router_2])
    #         pass
    

    pass

if __name__ == "__main__":
    main()