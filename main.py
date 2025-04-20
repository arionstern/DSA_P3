# main.py
import pygame
from elevation_data import get_elevation_grid
from sorting_visualizer import run_visualizer


def main():
    print("Fetching elevation data...")
    elevation_list = get_elevation_grid(10, 10)  # Fast grid-based fetch (~100 points)

    print("Choose a sorting algorithm to visualize:")
    print("1. Quick Sort (implemented from scratch)")
    print("2. Merge Sort (library-style visualization)")

    choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        algo = "quick"
    elif choice == '2':
        algo = "merge"
    else:
        print("Invalid choice. Defaulting to Quick Sort.")
        algo = "quick"

    run_visualizer(elevation_list, algo)


if __name__ == "__main__":
    main()
