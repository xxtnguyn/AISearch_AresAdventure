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

    def start(self):
        self.start_time = time.time()
        tracemalloc.start()
        self.start_memory = tracemalloc.take_snapshot()

    def end(self):
        self.end_time = time.time()
        self.end_memory = tracemalloc.take_snapshot()

    def reset(self):
        self.start_time = 0
        self.end_time = 0
        self.start_memory = 0
        self.end_memory = 0
        self.new_state_count = 0
        self.weight_pushed = 0
        self.step_count = 0

    def print_metrics(self):
        elapsed_time = self.end_time - self.start_time
        top_stats = self.end_memory.compare_to(self.start_memory, 'lineno')
        total_memory = sum(stat.size for stat in top_stats)

        # Print metrics
        print(f"New states created: {self.new_state_count}")
        print(f"Steps taken: {self.step_count}")
        print(f"Weight pushed: {self.weight_pushed}")
        print(f"Time taken: {elapsed_time:.4f} seconds")
        # Print total memory allocated
        print(f"Total memory allocated: {total_memory / 1024:.2f} KiB")  # Convert to KiB