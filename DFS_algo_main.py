import copy
import time

# Game map symbols and directions
RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

DIRECTION_MAP = {
    RIGHT: 'R',
    LEFT: 'L',
    UP: 'U',
    DOWN: 'D'
}

DIRECTIONS = [RIGHT, LEFT, UP, DOWN]

grid = []

nodes = 0

def load_grid_from_file(filename):
    """Load the game grid from a file"""
    grid = []
    with open(filename, 'r') as file:
        file.readline()  # Skip dimensions line
        for line in file:
            line = line[:-1]
            grid.append(list(line))  # Convert each line into a list of characters
    return grid

def is_valid_move(position, is_player):
    """Check if a move is valid for the player or a box"""
    x, y = position
    rows, cols = len(grid), len(grid[0])
    if 0 <= x < rows and 0 <= y < cols:
        if is_player:
            return grid[x][y] != '#'
        else:
            return grid[x][y] not in ['#', '$', '*']
    return False

def can_push_box(player_pos, box_pos):
    """Check if the box can be pushed to the new position"""
    new_box_pos = (box_pos[0] + (box_pos[0] - player_pos[0]), box_pos[1] + (box_pos[1] - player_pos[1]))
    return is_valid_move(new_box_pos, False)

def overGame():
    """Check if all boxes are on goal positions"""
    for row in grid:
        if '$' in row:
            return False
    return True

def dfs_to_goal_iterative(player_pos, nodes):
    global grid
    
    stack = [(player_pos, [], copy.deepcopy(grid))]
    visited = set()  # Using a set for faster lookup
    
    while stack:
        current_pos, path, current_grid = stack.pop()
        
        # Restore grid to the current state
        grid = copy.deepcopy(current_grid)
        
        # Check if all boxes are on goal positions
        if overGame():
            return path  # Found solution path
        
        for direction in DIRECTIONS:
            player_push_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            is_box_move = False
            
            if grid[player_push_pos[0]][player_push_pos[1]] in ('$','*'):
                is_box_move = True
                # Check if the box can be pushed
                if not can_push_box(current_pos, player_push_pos):
                    continue  # Skip if the box can't be pushed
                new_box_pos = (player_push_pos[0] + direction[0], player_push_pos[1] + direction[1])

            # Validate move
            if is_valid_move(player_push_pos, True):
                # Save the original states before making a move
                original_grid_state = copy.deepcopy(grid)  # Store the original grid state
                
                nodes += 1
                
                # Handle box movement if applicable
                if is_box_move:
                    if grid[new_box_pos[0]][new_box_pos[1]] == '.':
                        grid[new_box_pos[0]][new_box_pos[1]] = '*'
                    else:
                        grid[new_box_pos[0]][new_box_pos[1]] = '$'
                    
                    last_box_pos = player_push_pos
                    if grid[last_box_pos[0]][last_box_pos[1]] == '*':
                        grid[last_box_pos[0]][last_box_pos[1]] = '.'
                    else:
                        grid[last_box_pos[0]][last_box_pos[1]] = ' '


                # Move player
                if grid[player_push_pos[0]][player_push_pos[1]] == '.':
                    grid[player_push_pos[0]][player_push_pos[1]] = '+'
                else:
                    grid[player_push_pos[0]][player_push_pos[1]] = '@'

                # Nếu Ares rời khỏi vị trí switch (Ares đã đứng ở vị trí switch)
                if (grid[current_pos[0]][current_pos[1]] == '+'):
                    grid[current_pos[0]][current_pos[1]] = '.'
                # Nếu Ares rời khỏi vị trí rỗng
                else:
                    grid[current_pos[0]][current_pos[1]] = ' '  

                # Check if this state has been visited
                state = (str(player_push_pos), str(grid))
                if state not in visited:
                    visited.add(state)
                    if is_box_move:
                        stack.append((player_push_pos, path + [DIRECTION_MAP[direction]], grid))
                    else:
                        stack.append((player_push_pos, path + [DIRECTION_MAP[direction].lower()], grid))
                # Restore the grid to the original state after exploring
                grid = original_grid_state

    return None  # No path found

# Load grid and set initial player position
grid = load_grid_from_file(r'D:\Artificial Intelligent Foudation\Project 1 - Search\test_cases\input-01.txt')

player_pos = ()
for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x][y] == '@':
            player_pos = (x, y)  # Initial player position

# Run DFS to find the solution path
start_time = time.time()
path = dfs_to_goal_iterative(player_pos, nodes)
end_time = time.time()
if path:
    print("Finish!")
    print(len(path))
    for ele in path:
        print(ele, end='')
    execution_time = (end_time - start_time) * 1000  # chuyển đổi sang ms

    print(f"Time: {execution_time:.2f} ms")
else:
    print("No finding path!")
