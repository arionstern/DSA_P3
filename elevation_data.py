# elevation_data.py
from bridges.bridges import Bridges
from bridges.data_src_dependent import data_source
import random

def get_elevation_grid(rows=10, cols=10):
    bridges = Bridges(0, "your_username", "your_api_key")  # Replace with your actual credentials

    lat = round(random.uniform(-89.0, 88.0), 2)
    lon = round(random.uniform(-179.0, 178.0), 2)

    min_lat = lat
    max_lat = lat + (rows * 0.1)
    min_lon = lon
    max_lon = lon + (cols * 0.1)

    try:
        elevation_obj = data_source.get_elevation_data([min_lat, min_lon, max_lat, max_lon])
        grid = elevation_obj.data

        result = []
        for i in range(min(rows, len(grid))):
            for j in range(min(cols, len(grid[0]))):
                result.append((lat + i * 0.1, lon + j * 0.1, grid[i][j]))
        return result
    except Exception as e:
        print(f"Failed to fetch elevation grid: {e}")
        return []
