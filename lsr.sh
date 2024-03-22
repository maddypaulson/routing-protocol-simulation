#!/bin/bash

# Check if Python is installed
if command -v python &> /dev/null; then
    python_cmd="python"
elif command -v python3 &> /dev/null; then
    python_cmd="python3"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi
# Check if at least 3 arguments are passed
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <topologyFile> <messageFile> <changesFile> [outputFile]"
    exit 1
fi

# Assign inputs to variables
topology_file=$1
message_file=$2
changes_file=$3
output_file=${4:-output.txt} # Default to output.txt if not provided

# Placeholder for the main logic
# Here, you would include the commands or calls to other scripts/programs that process the inputs
echo "Running Link State Simulation with the following inputs:"
echo "Topology file: $topology_file"
echo "Message file: $message_file"
echo "Changes file: $changes_file"
echo "Output will be written to: $output_file"


$python_cmd "src/lsr.py" "$topology_file" "$message_file" "$changes_file" "$output_file"
