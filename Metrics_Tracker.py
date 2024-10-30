import time
import tracemalloc

class MetricsTracker:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.start_memory = 0
        self.end_memory = 0
        self.new_state_count = 0
        self.weight_pushed = 0
        self.step_count = 0
        self.time_taken = 0
        self.memory_taken = 0

    def start(self):
        self.start_time = time.time()
        tracemalloc.start()
        self.start_memory = tracemalloc.take_snapshot()

    def end(self):
        self.end_time = time.time()
        self.end_memory = tracemalloc.take_snapshot()
        self.time_taken = self.end_time - self.start_time

        # Calculate total memory taken in MB
        memory_diff = self.end_memory.compare_to(self.start_memory, 'lineno')
        self.memory_taken = sum(stat.size_diff for stat in memory_diff) / 10**6

    def reset(self):
        self.start_time = 0
        self.end_time = 0
        self.start_memory = 0
        self.end_memory = 0
        self.new_state_count = 0
        self.weight_pushed = 0
        self.step_count = 0
        self.time_taken = 0
        self.memory_taken = 0

    def print_metrics(self):
        print(f"Time taken: {self.time_taken:.4f} seconds")
        print(f"Memory taken: {self.memory_taken:.4f} MB")
        print(f"New state count: {self.new_state_count}")
        print(f"Weight pushed: {self.weight_pushed}")
        print(f"Step count: {self.step_count}")
