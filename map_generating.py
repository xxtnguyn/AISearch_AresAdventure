import random

# Define the symbols for the game
PLAYER = '@'
BOX = '$'
GOAL = '.'
WALL = '#'
EMPTY = ' '

# Function to randomly generate a map
def generate_random_map(width, height, num_boxes, num_goals, num_walls):
    # Initialize an empty map
    game_map = [[EMPTY for _ in range(width)] for _ in range(height)]
    
    # Add walls around the map border
    for i in range(width):
        game_map[0][i] = WALL
        game_map[height - 1][i] = WALL
    for i in range(height):
        game_map[i][0] = WALL
        game_map[i][width - 1] = WALL
    
    # Place random internal walls
    for _ in range(num_walls):
        while True:
            wall_x = random.randint(1, height - 2)
            wall_y = random.randint(1, width - 2)
            if game_map[wall_x][wall_y] == EMPTY:
                game_map[wall_x][wall_y] = WALL
                break
    
    # Place player in a random empty spot
    while True:
        player_x = random.randint(1, height - 2)
        player_y = random.randint(1, width - 2)
        if game_map[player_x][player_y] == EMPTY:
            game_map[player_x][player_y] = PLAYER
            break
    
    # Place boxes in random spots
    for _ in range(num_boxes):
        while True:
            box_x = random.randint(1, height - 2)
            box_y = random.randint(1, width - 2)
            if game_map[box_x][box_y] == EMPTY:
                game_map[box_x][box_y] = BOX
                break
    
    # Place goals in random spots
    for _ in range(num_goals):
        while True:
            goal_x = random.randint(1, height - 2)
            goal_y = random.randint(1, width - 2)
            if game_map[goal_x][goal_y] == EMPTY:
                game_map[goal_x][goal_y] = GOAL
                break
    
    return game_map

# Function to print the map
def print_map(map_data):
    for row in map_data:
        print(' '.join(row))
    print()

# Generate a random map with specific dimensions and object counts
random_map = generate_random_map(width=8, height=6, num_boxes=3, num_goals=3, num_walls=4)

# Print the generated random map
print_map(random_map)
