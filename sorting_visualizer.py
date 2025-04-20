import pygame
import time
import matplotlib.pyplot as plt
import numpy as np
from elevation_data import get_elevation_grid

WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 5
FPS = 60

def draw_bars(screen, data, font, highlight=[]):
    screen.fill((0, 0, 0))
    if not data:
        return

    elevations = [e[2] for e in data]
    max_elev = max(elevations)
    min_elev = min(elevations)
    elev_range = max_elev - min_elev if max_elev != min_elev else 1
    bar_width = max(1, WIDTH // len(data))

    for i, (_, _, elev, _) in enumerate(data):
        height = int((elev - min_elev) / elev_range * HEIGHT)
        x = i * bar_width
        y = HEIGHT - height

        norm = (elev - min_elev) / elev_range
        red = int(255 * norm)
        green = int(255 * (1 - abs(norm - 0.5) * 2))
        blue = int(255 * (1 - norm))
        color = (red, green, blue)

        if i in highlight:
            color = (255, 255, 255)

        pygame.draw.rect(screen, color, (x, y, bar_width, height))

def get_summary_text(data):
    if not data:
        return []

    sorted_data = sorted(data, key=lambda x: x[2])
    n = len(sorted_data)

    low = sorted_data[0]
    high = sorted_data[-1]
    median = sorted_data[n // 2]

    return [
        f"Lowest:  ({low[0]:.2f}, {low[1]:.2f}) → {low[2]:.2f} m",
        f"Median:  ({median[0]:.2f}, {median[1]:.2f}) → {median[2]:.2f} m",
        f"Highest: ({high[0]:.2f}, {high[1]:.2f}) → {high[2]:.2f} m"
    ]

def show_elevation_heatmap(data, rows, cols):
    if not data or len(data) != rows * cols:
        print("Data size mismatch or missing.")
        return

    elevations = [e[2] for e in data]
    grid = np.array(elevations).reshape((rows, cols))

    plt.figure(figsize=(8, 6))
    plt.imshow(grid, cmap='terrain', aspect='auto', origin='lower')
    plt.colorbar(label='Elevation (m)')
    plt.title("Elevation Grid Visualization")
    plt.xlabel("Columns (Longitude)")
    plt.ylabel("Rows (Latitude)")
    plt.tight_layout()
    plt.show()

def reset_visualization_state(_, rows, cols):
    new_data = get_elevation_grid(rows, cols)
    show_elevation_heatmap(new_data, rows, cols)
    new_summary = get_summary_text(new_data)
    return new_data, new_summary

def stable_key(item):
    return (item[2], item[3])

def quick_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            draw_bars(screen, arr, font, highlight=[j, high])
            pygame.display.flip()
            time.sleep(0.01)
            if stable_key(arr[j]) < stable_key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    quick_sort(data, 0, len(data) - 1)
    draw_bars(screen, data, font)
    pygame.display.flip()

def merge_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    def merge_sort(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort(arr, l, m)
            merge_sort(arr, m + 1, r)
            merge(arr, l, m, r)

    def merge(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if stable_key(left[i]) <= stable_key(right[j]):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            draw_bars(screen, data, font, highlight=[k])
            pygame.display.flip()
            time.sleep(0.01)
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            draw_bars(screen, data, font, highlight=[k])
            pygame.display.flip()
            time.sleep(0.01)
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            draw_bars(screen, data, font, highlight=[k])
            pygame.display.flip()
            time.sleep(0.01)
            k += 1

    merge_sort(data, 0, len(data) - 1)
    draw_bars(screen, data, font)
    pygame.display.flip()

def insertion_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and stable_key(data[j]) > stable_key(key):
            data[j + 1] = data[j]
            j -= 1
            draw_bars(screen, data, font, highlight=[j + 1])
            pygame.display.flip()
            pygame.time.wait(10)
        data[j + 1] = key
    draw_bars(screen, data, font)
    pygame.display.flip()

def selection_sort_visualized(data, screen, clock):
    n = len(data)
    font = pygame.font.SysFont("Arial", 14)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if stable_key(data[j]) < stable_key(data[min_idx]):
                min_idx = j
            draw_bars(screen, data, font, highlight=[j, min_idx])
            pygame.display.flip()
            pygame.time.wait(10)
        data[i], data[min_idx] = data[min_idx], data[i]
    draw_bars(screen, data, font)
    pygame.display.flip()

def heap_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and stable_key(arr[l]) > stable_key(arr[largest]):
            largest = l
        if r < n and stable_key(arr[r]) > stable_key(arr[largest]):
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            draw_bars(screen, data, font, highlight=[i, largest])
            pygame.display.flip()
            pygame.time.wait(10)
            heapify(arr, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw_bars(screen, data, font, highlight=[0, i])
        pygame.display.flip()
        pygame.time.wait(10)
        heapify(data, i, 0)
    draw_bars(screen, data, font)
    pygame.display.flip()

def run_visualizer(data, sort_func, rows, cols):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elevation Sort Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 14)

    original_data = data.copy()
    sorted_once = False
    running = True

    summary_lines = get_summary_text(data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                data, summary_lines = reset_visualization_state(original_data, rows, cols)
                sorted_once = False

        if not sorted_once:
            sort_func(data, screen, clock)
            sorted_once = True
            summary_lines = get_summary_text(data)

        draw_bars(screen, data, font)

        for i, line in enumerate(summary_lines):
            label = font.render(line, True, (255, 255, 255))
            screen.blit(label, (10, 10 + i * 20))

        pygame.display.flip()

    pygame.quit()
