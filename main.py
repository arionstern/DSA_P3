import pygame
from elevation_data import get_elevation_grid
from sorting_visualizer import show_elevation_heatmap
from sorting_visualizer import (
    run_visualizer,
    quick_sort_visualized,
    merge_sort_visualized,
    insertion_sort_visualized,
    selection_sort_visualized,
    heap_sort_visualized
)

def main():
    print("Fetching elevation data using BRIDGES...")

    # Get user-defined grid size
    try:
        rows = int(input("Enter number of grid rows (e.g. 10): "))
        cols = int(input("Enter number of grid columns (e.g. 10): "))
    except ValueError:
        rows, cols = 10, 10
        print("Invalid input. Defaulting to 10x10 grid.")

    # Fetch the elevation data
    elevation_list = get_elevation_grid(rows, cols)
    if not elevation_list:
        print("Failed to retrieve elevation data. Exiting.")
        return

    # Show the elevation heatmap
    show_elevation_heatmap(elevation_list, rows, cols)

    # Sorting algorithm selection menu
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
        '5': ("Heap Sort", heap_sort_visualized)
    }

    algo_name, algo_func = algo_map.get(choice, ("Quick Sort (default)", quick_sort_visualized))
    print(f"\nRunning: {algo_name}...\n")

    # Run the visualization with full context
    run_visualizer(elevation_list, algo_func, rows, cols)

if __name__ == "__main__":
    main()
