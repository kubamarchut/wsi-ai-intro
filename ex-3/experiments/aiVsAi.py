import sys
import time
import statistics
import matplotlib
import numpy as np
from tqdm import tqdm

sys.path.append("..")
from MiniMax import minmax, alpha_pruning, possible_moves
from plot_time import plot_time_per_step
from gameSimulation import game_simulation


def print_statistics(method, statistics_dict):
    print(f"AI vs AI Game Duration Statistics - {method}:")
    print("-------------------------------------" + "-" * len(method))
    print(f'Average Duration: {statistics_dict["average"]:.3f}')
    print(f'Minimum Duration: {statistics_dict["minimum"]:.3f}')
    print(f'Maximum Duration: {statistics_dict["maximum"]:.3f}')
    print(f'Standard Deviation: {statistics_dict["stddev"]:.3f}')
    # print("All Durations:", statistics_dict["results"])
    print("\n")


def test_solution_single(opt_function, time_per_step, starting_board):
    start_time = time.time()
    game_simulation(opt_function, time_per_step, starting_board)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def test_solution_multiple(opt_function, n_tests=10):
    results = []
    time_per_step = {}
    progress_bar = tqdm(
        total=n_tests,
        desc=f"Testing {opt_function.__name__}",
        position=0,
        leave=True,
    )

    def run_test():
        starting_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        results.append(
            test_solution_single(opt_function, time_per_step, starting_board)
        )
        starting_board = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
        results.append(
            test_solution_single(opt_function, time_per_step, starting_board)
        )
        starting_board = np.array([[-1, 0, 0], [0, 1, 1], [0, 0, 0]])
        results.append(
            test_solution_single(opt_function, time_per_step, starting_board)
        )

    for _ in range(n_tests):
        progress_bar.update(1)
        run_test()

    progress_bar.close()

    avg = statistics.mean(results)
    minimum = min(results)
    maximum = max(results)
    stddev = statistics.stdev(results)

    return {
        "average": avg,
        "minimum": minimum,
        "maximum": maximum,
        "stddev": stddev,
        "results": results,
        "per_step": time_per_step,
    }


if __name__ == "__main__":
    font = {"weight": "bold", "size": 12}

    matplotlib.rc("font", **font)
    print("Testing alpha pruning algorithm:")
    stats_data = test_solution_multiple(alpha_pruning)
    # print_statistics("AlphaBeta", stats_data)

    print("Testing minmax algorithm:")
    stats_data_2 = test_solution_multiple(minmax)
    # print_statistics("MiniMax", stats_data_2)

    plot_time_per_step(
        [{"alpha": stats_data["per_step"]}, {"minmax": stats_data_2["per_step"]}],
        "simulation-data.csv",
    )
