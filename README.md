# Routing Protocol Simulation

## Overview
This project is a simulation of routing protocols implemented in Java. It includes two major routing protocols:

1. **Distance Vector Routing (DVR)** - Uses the Bellman-Ford algorithm to update routing tables based on information shared with immediate neighbors.
2. **Link State Routing (LSR)** - Uses Dijkstra’s algorithm to construct the shortest path tree from a global view of the network.

### Distance Vector Routing

The Distance Vector Routing (DVR) module implements the core principles of the Distance Vector routing protocol. Routers exchange information only with their immediate neighbors, gradually propagating knowledge of the network's topology. The DistanceVectorNetwork class manages network-wide operations and initializes routers as DistanceVectorRouter objects. Each DistanceVectorRouter maintains a routing table that records destinations, next hops, and costs, using iterative updates to compute the shortest paths.

### Link State Routing

The Link State Routing (LSR) module enables routers to maintain a complete and up-to-date view of the network. The LinkStateNetwork class initializes the network from a topology file and manages LinkStateRouter objects, which generate and distribute Link State Packets (LSPs). These packets contain information about directly connected neighbors and their link costs, allowing routers to build a comprehensive map of the network.

Each LinkStateRouter processes incoming LSPs, ensuring freshness through sequence numbers, and updates its routing table using Dijkstra's algorithm to compute the shortest paths. The implementation dynamically adjusts to network changes, such as link failures or cost modifications, redistributing LSPs and recalculating routes accordingly.

## Features
- Implementation of DVR and LSR algorithms.
- Simulated network topology for testing routing behavior.
- Support for adding routers dynamically.
- Handles topology changes and updates routes accordingly.
- Test suite ensuring protocol correctness and stability.

## Tech Stack
- **Language:** Python
- **Version Control:** Git
- **Algorithms:** Bellman-Ford, Dijkstra

## Running the Application

### bash_scripts 
Bash Scripts - `dvr.sh` and `lsr.sh`

We have created a bash script which allows running our project with the following commands
```
./dvr.sh <topologyFile> <messageFile> <changesFile> [outputFile]
```
```
./lsr.sh <topologyFile> <messageFile> <changesFile> [outputFile]
```

### make_bash 
Executable Files - make.sh

We also created bash scripts to compile the code into executable binaries

The script is used as follows:
```
./make.sh
```

The executable files will be present in the dist folder. The executable binaries are named dvr and lsr and are executed from the project source folder using:

```
./dist/dvr <topologyFile> <messageFile> <changesFile> [outputFile]
./dist/lsr <topologyFile> <messageFile> <changesFile> [outputFile]
```

## Contributions
- Maddy Paulson
- Leonardo Kamino Barros