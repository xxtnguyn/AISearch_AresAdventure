from State_and_Game import Game, State
from Utils import *
from Metrics_Tracker import MetricsTracker
import numpy as np
import heapq


def AStar(game: Game, tracker: MetricsTracker):
    # Start the metrics tracker
    tracker.start()

    # Create a starting state
    start_state = State(
        ares_pos=game.ares_start_pos,
        board=np.copy(game.board),
        cost=0
    )
    start_state.heuristic = find_heuristic(game, start_state)

    # Search's trackers
    tie_breaker = 0 # For the pri-queue, in case the score is the same
    frontier = [(start_state.heuristic + start_state.cost, tie_breaker, start_state)] # Priority queue, rank by cost + heuristic
    closed_set = set() # Visited - Banned forever
    parrents = dict() # Track the parrent, for routing
    found_solution = False
    

    # Start search
    while frontier:
        # Pop the front 
        _, _, front_state = heapq.heappop(frontier)
        if front_state in closed_set:
            continue
        if is_goal(game, front_state):
            found_solution = True
            break 
        closed_set.add(front_state)

        # Check the neighbor of that front state
        for neighbor_state, direction, pushed_a_rock, weight_pushed in find_neighbors(game, front_state, tracker, Astart_mode=True):
            if neighbor_state not in closed_set:
                # Push neighbor into the queue
                heapq.heappush(frontier, (neighbor_state.heuristic + neighbor_state.cost, tie_breaker, neighbor_state))
                # Update parrents
                parrents[neighbor_state] = (front_state, direction, pushed_a_rock, weight_pushed)
                tie_breaker += 1
                    
    # If we cant find a solutions
    if not found_solution:
        return None
    
    # Trace back the route
    route_weight = get_route(parrents, final_state=front_state, start_state=start_state)

    # End the metrics tracker
    tracker.end()
    tracker.weight_pushed = sum(weight for _, weight in route_weight)
    tracker.step_count = len(route_weight)
    return route_weight
