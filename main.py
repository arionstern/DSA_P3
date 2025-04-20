from elevation_data import get_elevation_grid
from sorting_visualizer import show_elevation_heatmap, run_visualizer

def main():
    print("Fetching elevation data using BRIDGES...")

    try:
        rows = int(input("Enter number of grid rows (e.g. 10): "))
        cols = int(input("Enter number of grid columns (e.g. 10): "))
    except ValueError:
        rows, cols = 10, 10
        print("Invalid input. Using 10×10 grid.")

    elevation_list = get_elevation_grid(rows, cols)
    if not elevation_list:
        print("Failed to fetch elevation data.")
        return

    show_elevation_heatmap(elevation_list, rows, cols)

    indexed = [(lat, lon, elev, idx) for idx, (lat, lon, elev) in enumerate(elevation_list)]
    run_visualizer(indexed, default_sort_func=None, rows=rows, cols=cols)

if __name__ == "__main__":
    main()
