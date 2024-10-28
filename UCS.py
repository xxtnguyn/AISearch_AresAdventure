from State_and_Game import Game, State
from Utils import *
from MetricsTracker import MetricsTracker
import numpy as np
import heapq


def UCS(game: Game, tracker: MetricsTracker):
    # Start the metrics tracker
    tracker.start()

    # Create a starting state
    start_state = State(
        ares_pos=game.ares_start_pos,
        board=np.copy(game.board),
        cost=0
    )

    # Search's trackers
    frontier = [start_state] # Priority queue, rank by cost
    closed_set = set() # Visited - Banned forever
    parrents = dict() # Track the parrent, for routing
    found_solution = False

    # Start search
    while frontier:
        # Pop the front 
        front_state = heapq.heappop(frontier)
        if front_state in closed_set:
            continue
        if is_goal(game, front_state):
            found_solution = True
            break 
        closed_set.add(front_state)

        # Check the neighbor of that front state
        for neighbor_state, direction, pushed_a_rock, weight_pushed in find_neighbors(game, front_state, tracker):
            if neighbor_state not in closed_set:
                heapq.heappush(frontier, neighbor_state)
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
