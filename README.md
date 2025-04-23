# Elevation Sort Visualizer

This project visualizes the sorting of real-world elevation data fetched from the NOAA ETOPO1 dataset using the BRIDGES API. The user can watch various sorting algorithms transform a grid of elevation data into ordered sequences, with real-time animations, tooltips, and metrics.

## Features

- Retrieves real elevation data using BRIDGES API (NOAA ETOPO1)
- Visualizes elevation as color-coded vertical bars
- Animated sorting with six algorithms:
  - Bubble Sort
  - Insertion Sort
  - Selection Sort
  - Merge Sort
  - Quick Sort
  - Heap Sort
- Interactive GUI with:
  - Sort buttons
  - Keyboard shortcuts (`R = Reset`, `S = Shuffle`, `C = Change Theme`, `ESC = Quit`)
  - Hover tooltips showing latitude, longitude, and elevation
- Displays sorting metrics: time, comparisons, and swaps
- Supports color themes: Terrain, Grayscale, Heatmap
- Pre/post elevation heatmap comparison using Matplotlib

## How to Run

### Requirements

Install Python 3.10 or higher, then install dependencies.

**Option 1 (Recommended via terminal):**
```bash
pip install -r requirements.txt
```

**Option 2 (Manual install):**
```bash
pip install pygame matplotlib numpy bridges
```

**Option 3 (Via IDE like PyCharm or VS Code):**
1. Open the project folder in your IDE.
2. Locate and open the `requirements.txt` file.
3. Right-click the file or use the integrated terminal and select **"Install Requirements"** or click **Install Packages** if prompted.
4. Alternatively, open the terminal inside your IDE and run:
```bash
pip install -r requirements.txt
```

### Run the Program
```bash
python main.py
```

## File Overview

- `main.py`: Entry point. Handles input, sort selection, and visualizer loop.
- `elevation_data.py`: Fetches elevation data using BRIDGES API.
- `sorting_visualizer.py`: Contains sorting algorithms and rendering logic.

## Data Source

NOAA ETOPO1 elevation dataset accessed via:  
https://bridgesuncc.github.io/tutorials/Data_Elevation.html