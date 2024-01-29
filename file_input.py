"""
When loading from a file in Pyzo you have to run the script from the file
system. If you don't do that, it won't be able to find your file.

From the Run menu choose "Run File as Script" or hit CTRL-SHIFT-E

Poojan Patel, Mohawk college, January 2024
"""
def file_input(filename):
    """Loads each line of the file into a list and returns it."""
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip())
    return lines

