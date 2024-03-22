#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check if Python is installed
if command -v python &> /dev/null; then
    python_cmd="python"
elif command -v python3 &> /dev/null; then
    python_cmd="python3"
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Check if correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 topology_file message_file change_file"
    exit 1
fi

# Assigning arguments to variables
topology_file="$1"
message_file="$2"
change_file="$3"


# Run the first Python script
$python_cmd "$script_dir/custom_dijkstra_lsr_test.py" "$topology_file" "$message_file" "$change_file"

# Run the second Python script
$python_cmd "src/lsr.py" "$topology_file" "$message_file" "$change_file"

# Compare the contents of output.txt and output_test.txt
if cmp -s output.txt output_test.txt; then
    echo "Outputs are equal."
else
    echo "Outputs are different."
fi
