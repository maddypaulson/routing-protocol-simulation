import sys
INFINITY = float("inf")

def parseArgs():
    """
    Parses the command line arguments and returns them as a list.

    Returns:
        list: A list containing the command line arguments.
    """
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python your_script.py topology_file message_file changes_file [output_file]")
        sys.exit(1)
    
    args = sys.argv[1:]

    if len(sys.argv) == 4:
        args += ["output.txt"]

    return args