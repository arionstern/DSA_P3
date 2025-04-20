from bridges.bridges import Bridges
from bridges.data_src_dependent import data_source
import random

def get_random_elevation_data(count=100):
    bridges = Bridges(0, "your_username", "your_api_key")  # Replace with your actual credentials

    data = []

    for _ in range(count):
        # Generate a small random box (1° area)
        lat = round(random.uniform(-89.0, 89.0), 2)
        lon = round(random.uniform(-179.0, 179.0), 2)

        min_lat = lat
        max_lat = lat + 1
        min_lon = lon
        max_lon = lon + 1

        try:
            elevation_obj = data_source.get_elevation_data([min_lat, min_lon, max_lat, max_lon])
            # Sample a single point from the top-left corner of the elevation grid
            elevation = elevation_obj.data[0][0]
            data.append((lat, lon, elevation))
        except Exception as e:
            print(f"Failed at ({lat}, {lon}): {e}")

    return data
