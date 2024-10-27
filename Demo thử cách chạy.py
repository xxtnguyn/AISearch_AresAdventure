from Algo_AStar import AStar
from Algo_UCS import UCS
from Algo_BFS import BFS
from Algo_DFS import DFS
from State_and_Game import Game
from Metrics_Tracker import MetricsTracker


# Test case is txt file, I put in one folder
testcase_folder = "testcases"

# Test for each testcase in the folder
for i in range(1, 26):
    if i in (3, 9, 10, 20, 21, 22):
        continue
    print("Testcase", i)
    # Read the testcase
    with open(testcase_folder + "/test" + str(i) + ".txt", "r") as f:
        text = f.read()

    # Create the game
    game = Game()
    game.read_map_from_string(text)

    # Create the metrics tracker
    metrics = MetricsTracker()
    
    print("=== DFS ===")
    # Run the DFS algorithm
    dfs = DFS(game, metrics)
    metrics.print_metrics()
    metrics.reset()

    print("=== BFS ===")
    # Run the BFS algorithm
    bfs = BFS(game, metrics)
    metrics.print_metrics()
    metrics.reset()

    print("=== AStar ===")
    # Run the AStar algorithm
    astar = AStar(game, metrics)
    metrics.print_metrics()
    metrics.reset()

    print("=== UCS ===")
    # Run the UCS algorithm
    ucs = UCS(game, metrics)
    metrics.print_metrics()
    metrics.reset()
    print("=====================================")
