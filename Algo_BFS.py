from State_and_Game import Game, State
from Utils import *
from collections import deque
from Metrics_Tracker import MetricsTracker
import numpy as np


def BFS(game: Game, tracker: MetricsTracker):
    # Start the metrics tracker
    tracker.start()

    # Create a starting state
    start_state = State(
        ares_pos=game.ares_start_pos,
        board=np.copy(game.board),
        cost=0
    )

    # Search's trackers
    frontier = deque([start_state])
    frontier_set = set([start_state]) # For quick check if state in frontier
    closed_set = set() # Visited - Banned forever
    parrents = dict() # Track the parrent, for routing
    found_solution = False

    # Start search
    while frontier:
        # Pop the front 
        front_state = frontier.popleft()
        frontier_set.remove(front_state)
        if is_goal(game, front_state):
            found_solution = True
            break 
        closed_set.add(front_state)

        # Check the neighbor of that front state
        for neighbor_state, direction, pushed_a_rock, weight_pushed in find_neighbors(game, front_state, tracker):
            if neighbor_state not in closed_set and neighbor_state not in frontier_set:
                frontier.append(neighbor_state)
                frontier_set.add(neighbor_state)
                parrents[neighbor_state] = (front_state, direction, pushed_a_rock, weight_pushed)

    # If we cant find a solution
    if not found_solution:
        return None
    
    # Trace back the route
    route_weight = get_route(parrents, final_state=front_state, start_state=start_state)

    # End the metrics tracker
    tracker.end()
    tracker.weight_pushed = sum(weight for _, weight in route_weight)
    tracker.step_count = len(route_weight)
    return route_weight
