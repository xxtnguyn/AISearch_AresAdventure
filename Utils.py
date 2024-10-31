from State_and_Game import Game, State
import numpy as np
from CONSTAINTS import *
from Metrics_Tracker import MetricsTracker


# Print the board
def print_board(board):
    print(np.array_str(board, precision=0, suppress_small=True))

# Check if a box position is deadlock
def is_deadlock(game: Game, box_pos): # 2 adjacent walls, 2 opposite walls is not deadlock
    x, y = box_pos
    # Note: If we push the box to deadlock, but if the box is in the goal, it's not deadlock
    if box_pos in game.goals:
        return False
    if game.board[(x-1, y)] == WALL_NUM and game.board[(x, y-1)] == WALL_NUM:
        return True
    if game.board[(x-1, y)] == WALL_NUM and game.board[(x, y+1)] == WALL_NUM:
        return True
    if game.board[(x+1, y)] == WALL_NUM and game.board[(x, y-1)] == WALL_NUM:
        return True
    if game.board[(x+1, y)] == WALL_NUM and game.board[(x, y+1)] == WALL_NUM:
        return True
    return False

# Find neighbors of a state
# For future sake, we return (neighbor, direction, pushed a box or not, weight pushed)
# Parameter:
#   - AStar_mode: If False then we dont compute the heuristic of the neighbor state
def find_neighbors(game: Game, state: State, tracker: MetricsTracker, Astart_mode=False):
    neighbors = []
    directions = [('u', -1, 0), ('d', 1, 0), ('l', 0, -1), ('r', 0, 1)]
    
    for direction, dx, dy in directions:
        ares_new_pos = (state.ares_pos[0] + dx, state.ares_pos[1] + dy)

        # If Ares hit a wall 
        if game.board[ares_new_pos] == WALL_NUM:
            continue

        # If Ares meet a rock
        if state.board[ares_new_pos] > 0:
            weight = state.board[ares_new_pos]
            rock_old_pos = ares_new_pos
            rock_new_pos = (rock_old_pos[0] + dx, rock_old_pos[1] + dy)

            # If Ares push the rock into a wall or another rock or a deadlock
            if game.board[rock_new_pos] == WALL_NUM or state.board[rock_new_pos] > 0 or is_deadlock(game, rock_new_pos):
                continue

            # We can push freely now
            pushed_a_rock = True
            new_board = np.copy(state.board)
            new_board[rock_old_pos] = ARES_NUM
            new_board[rock_new_pos] = weight
            new_board[state.ares_pos] = SPACE_NUM
            
            new_state = State(
                ares_pos=ares_new_pos,
                board=new_board,
                cost=state.cost + weight
            )

            # We only deal with heuristic of Astar_mode is ON
            if Astart_mode:
                new_heuristic = find_heuristic(game, new_state)
                new_state.heuristic = new_heuristic

            neighbors.append((new_state, direction, pushed_a_rock, weight))

        else: # Just walk
            pushed_a_rock = False
            new_board = np.copy(state.board)
            new_board[state.ares_pos] = SPACE_NUM
            new_board[ares_new_pos] = ARES_NUM

            new_state = State(
                ares_pos=ares_new_pos,
                board=new_board,
                cost=state.cost + WALK_COST
            )

            # We only deal with heuristic of Astar_mode is ON
            if Astart_mode:
                new_state.heuristic = state.heuristic # If no box pushed then heuristic dont change

            neighbors.append((new_state, direction, pushed_a_rock, 0))

    # Update metrics
    tracker.new_state_count += len(neighbors)
    return neighbors        
            

# Check if a state is goal state
def is_goal(game: Game, state: State):
    for goal in game.goals:
        if state.board[goal] <= 0:
            return False
    return True


# Trace back the route using parrents dict
def get_route(parrents, final_state, start_state):
    route = []
    current_state = final_state

    while current_state != start_state:
        parrent_stage, direction, pushed_a_rock, weight_pushed = parrents[current_state]
        route.append((direction.upper() if pushed_a_rock else direction, weight_pushed))
        current_state = parrent_stage

    return route[::-1]


# Given a state, find heuristic score of that state
def find_heuristic(game: Game, state: State):
    goals = game.goals # List
    rocks = [] # Each element is tuple of position and weight

    # First we scan thought the state board to find the position and weight of the rocks
    # Each State object only store a matrix represent the board so we have to do this
    # This of course take time, but I dont find any better way yet
    nrow, ncol = state.board.shape
    for row in range(nrow):
        for col in range(ncol):
            value = state.board[row, col]
            if value > 0: # This is a rock 
                rocks.append(((row, col), value))

    # The heuristic should be sum manhattan distance from all rocks to the goals.
    # One rock only has one goal, we priority the heaviest rock to go to its nearest goal 

    # Sort the rocks by weight, heaviest go first
    sorted_rocks = sorted(rocks, key=lambda x:x[1], reverse=True)

    empty_goals = set(goals) # Keep track of which goal is unassigned
    total_heuristic = 0

    for (row, col), weight in sorted_rocks:
        # Find the nearest goal for the current rock
        nearest_goal = min(empty_goals, key=lambda goal: manhattan_dist(goal, (row, col)))
        dist_to_nearest_goal = manhattan_dist(nearest_goal, (row, col))

        # Update the total heuristic
        total_heuristic += dist_to_nearest_goal * weight

        # Update the empty_goals
        empty_goals.remove(nearest_goal)

        # Log
        # print(f"Current rock is: ({row}, {col}), weight: {weight}")
        # print(f"The goal for this rock is: ({nearest_goal})")
        # print(f"Weighted dist is: {dist_to_nearest_goal}")

    return total_heuristic


# Compute the manhattan distance between 2 positions
def manhattan_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
