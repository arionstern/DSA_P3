import pygame
import time
import matplotlib.pyplot as plt
import numpy as np
from elevation_data import get_elevation_grid

WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 5
FPS = 60

def draw_bars(screen, data, font, highlight=[], min_elev=None, max_elev=None, hover_index=None):
    screen.fill((0, 0, 0))
    if not data:
        return

    elevations = [e[2] for e in data]
    if min_elev is None or max_elev is None:
        max_elev = max(elevations)
        min_elev = min(elevations)

    elev_range = max_elev - min_elev if max_elev != min_elev else 1
    bar_width = max(1, WIDTH // len(data))

    for i, (lat, lon, elev, _) in enumerate(data):
        height = int((elev - min_elev) / elev_range * HEIGHT)
        x = i * bar_width
        y = HEIGHT - height

        norm = (elev - min_elev) / elev_range
        red = int(255 * norm)
        green = int(255 * (1 - abs(norm - 0.5) * 2))
        blue = int(255 * (1 - norm))
        color = (red, green, blue)

        if i in highlight or i == hover_index:
            color = (255, 255, 255)

        pygame.draw.rect(screen, color, (x, y, bar_width, height))

    draw_color_legend(screen, font)


def draw_color_legend(screen, font):
    legend_rect = pygame.Rect(10, HEIGHT - 30, 200, 10)
    for x in range(legend_rect.width):
        norm = x / legend_rect.width
        red = int(255 * norm)
        green = int(255 * (1 - abs(norm - 0.5) * 2))
        blue = int(255 * (1 - norm))
        color = (red, green, blue)
        screen.set_at((legend_rect.x + x, legend_rect.y), color)

    label_low = font.render("Low", True, (255, 255, 255))
    label_high = font.render("High", True, (255, 255, 255))
    screen.blit(label_low, (legend_rect.x, legend_rect.y - 15))
    screen.blit(label_high, (legend_rect.x + legend_rect.width - 30, legend_rect.y - 15))


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

def show_comparison_heatmap(original_data, sorted_data, rows, cols):
    if not original_data or not sorted_data:
        return

    original_grid = np.array([e[2] for e in original_data]).reshape((rows, cols))
    sorted_grid = np.array([e[2] for e in sorted_data]).reshape((rows, cols))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    im1 = axes[0].imshow(original_grid, cmap='terrain', aspect='auto', origin='lower')
    axes[0].set_title("Original Elevation Grid")
    fig.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

    im2 = axes[1].imshow(sorted_grid, cmap='terrain', aspect='auto', origin='lower')
    axes[1].set_title("Sorted Elevation Grid")
    fig.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

    for ax in axes:
        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")

    plt.tight_layout()
    plt.show()



def reset_visualization_state(_, rows, cols):
    new_data = get_elevation_grid(rows, cols)
    show_elevation_heatmap(new_data, rows, cols)
    new_summary = get_summary_text(new_data)
    indexed = [(lat, lon, elev, idx) for idx, (lat, lon, elev) in enumerate(new_data)]
    return indexed, new_summary


def stable_key(item):
    return (item[2], item[3]) if len(item) > 3 else (item[2], 0)

def bubble_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if stable_key(data[j]) > stable_key(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]
            draw_bars(screen, data, font, highlight=[j, j + 1], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            pygame.time.wait(5)

    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev)
    pygame.display.flip()

def quick_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            draw_bars(screen, arr, font, highlight=[j, high], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            time.sleep(0.01)
            if stable_key(arr[j]) < stable_key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    quick_sort(data, 0, len(data) - 1)
    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev)
    pygame.display.flip()

def merge_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

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
            draw_bars(screen, data, font, highlight=[k], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            time.sleep(0.01)
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            draw_bars(screen, data, font, highlight=[k], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            time.sleep(0.01)
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            draw_bars(screen, data, font, highlight=[k], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            time.sleep(0.01)
            k += 1

    merge_sort(data, 0, len(data) - 1)
    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev)
    pygame.display.flip()

def insertion_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and stable_key(data[j]) > stable_key(key):
            data[j + 1] = data[j]
            j -= 1
            draw_bars(screen, data, font, highlight=[j + 1], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            pygame.time.wait(10)
        data[j + 1] = key
    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev)
    pygame.display.flip()

def selection_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)
    n = len(data)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if stable_key(data[j]) < stable_key(data[min_idx]):
                min_idx = j
            draw_bars(screen, data, font, highlight=[j, min_idx], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            pygame.time.wait(10)
        data[i], data[min_idx] = data[min_idx], data[i]
    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev)
    pygame.display.flip()

def heap_sort_visualized(data, screen, clock):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

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
            draw_bars(screen, data, font, highlight=[i, largest], min_elev=min_elev, max_elev=max_elev)
            pygame.display.flip()
            pygame.time.wait(10)
            heapify(arr, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw_bars(screen, data, font, highlight=[0, i], min_elev=min_elev, max_elev=max_elev)
        pygame.display.flip()
        pygame.time.wait(10)
        heapify(data, i, 0)
    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev)
    pygame.display.flip()

def run_visualizer(data, default_sort_func, rows, cols):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elevation Sort Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 14)

    sort_funcs = {
        "Quick": quick_sort_visualized,
        "Merge": merge_sort_visualized,
        "Insertion": insertion_sort_visualized,
        "Selection": selection_sort_visualized,
        "Heap": heap_sort_visualized,
        "Bubble": bubble_sort_visualized
    }

    # Create button rects
    button_width = 100
    button_height = 25
    buttons = []
    for i, name in enumerate(sort_funcs):
        rect = pygame.Rect(10 + i * (button_width + 10), 10, button_width, button_height)
        buttons.append((rect, name))

    current_sort = None
    sorted_once = False
    running = True

    data, summary_lines = reset_visualization_state(data, rows, cols)
    original_data = data.copy()  # 🔁 Store original unsorted data
    sort_duration = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    data, summary_lines = reset_visualization_state(data, rows, cols)
                    original_data = data.copy()
                    sorted_once = False
                    current_sort = None
                    sort_duration = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, name in buttons:
                    if rect.collidepoint(mx, my):
                        current_sort = sort_funcs[name]
                        data = original_data.copy()  # 🔁 Reset data before each sort
                        sorted_once = False
                        sort_duration = 0
                        print(f"Selected: {name} Sort")

        if current_sort and not sorted_once:
            start_time = time.time()
            current_sort(data, screen, clock)
            sort_duration = time.time() - start_time
            sorted_once = True
            summary_lines = get_summary_text(data)

        draw_bars(screen, data, font)

        # Draw buttons
        for rect, name in buttons:
            color = (200, 50, 50) if sort_funcs[name] == current_sort else (50, 50, 200)
            pygame.draw.rect(screen, color, rect)
            label = font.render(name, True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        # Draw summary + time
        for i, line in enumerate(summary_lines):
            label = font.render(line, True, (255, 255, 255))
            screen.blit(label, (10, 50 + i * 20))

        if current_sort and sorted_once:
            label_time = font.render(f"Sort Time: {sort_duration:.2f}s", True, (255, 255, 255))
            screen.blit(label_time, (10, 50 + len(summary_lines) * 20))

        pygame.display.flip()

    pygame.quit()
