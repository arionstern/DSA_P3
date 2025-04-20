from elevation_data import get_elevation_grid
from sorting_visualizer import show_elevation_heatmap, run_visualizer

def main():
    print("Fetching elevation data using BRIDGES...")

    try:
        # Prompt user for dataset size
        rows = int(input("Enter number of grid rows: "))
        cols = int(input("Enter number of grid columns: "))
    except ValueError:
        # Fallback to 10x10 if invalid input
        rows, cols = 10, 10
        print("Invalid input. Using 10×10 grid.")


    # Fetch and visualize elevation data
    elevation_list = get_elevation_grid(rows, cols)
    if not elevation_list:
        print("Failed to fetch elevation data.")
        return
    show_elevation_heatmap(elevation_list, rows, cols)

    indexed = [(lat, lon, elev, idx) for idx, (lat, lon, elev) in enumerate(elevation_list)]

    # Launch Pygame visualizer
    run_visualizer(indexed, default_sort_func=None, rows=rows, cols=cols)

if __name__ == "__main__":
    main()
