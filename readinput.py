def load_grid_from_file(filename):
    """Load the game grid from a file"""
    grid = []
    with open(filename, 'r') as file:
        file.readline()  # Skip dimensions line
        for line in file:
            line = line[:-1]
            grid.append(list(line))  # Convert each line into a list of characters
    return grid