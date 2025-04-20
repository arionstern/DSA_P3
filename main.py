# main.py
import pygame
from elevation_data import get_elevation_grid
from sorting_visualizer import (
    run_visualizer,
    quick_sort_visualized,
    merge_sort_visualized,
    insertion_sort_visualized,
    selection_sort_visualized,
    heap_sort_visualized,
)

def main():
    print("Fetching elevation data...")
    elevation_list = get_elevation_grid(10, 10)  # ~100 points

    print("\nChoose a sorting algorithm to visualize:")
    print("1. Quick Sort")
    print("2. Merge Sort")
    print("3. Insertion Sort")
    print("4. Selection Sort")
    print("5. Heap Sort")

    choice = input("Enter 1–5: ").strip()

    algo_map = {
        '1': ("Quick Sort", quick_sort_visualized),
        '2': ("Merge Sort", merge_sort_visualized),
        '3': ("Insertion Sort", insertion_sort_visualized),
        '4': ("Selection Sort", selection_sort_visualized),
        '5': ("Heap Sort", heap_sort_visualized),
    }

    algo_name, algo_func = algo_map.get(choice, ("Quick Sort (default)", quick_sort_visualized))
    print(f"\nRunning: {algo_name}...\n")

    run_visualizer(elevation_list, algo_func)


if __name__ == "__main__":
    main()
