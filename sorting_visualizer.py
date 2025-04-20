import pygame
import time
import matplotlib.pyplot as plt
import numpy as np
from elevation_data import get_elevation_grid

WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 5
FPS = 60

def draw_bars(screen, data, font, highlight=[], min_elev=None, max_elev=None, hover_index=None, color_theme="terrain"):
    # Clear the screen
    screen.fill((0, 0, 0))
    if not data:
        return

    # Calculate elevation range if not provided
    elevations = [e[2] for e in data]
    if min_elev is None or max_elev is None:
        max_elev = max(elevations)
        min_elev = min(elevations)

    # Set bar width
    elev_range = max_elev - min_elev if max_elev != min_elev else 1
    bar_width = max(1, WIDTH // len(data))


    for i, (lat, lon, elev, _) in enumerate(data):
        # Normalize elevation to bar height
        height = int((elev - min_elev) / elev_range * HEIGHT)
        x = i * bar_width
        y = HEIGHT - height

        norm = (elev - min_elev) / elev_range

        #Apply selected color theme
        if color_theme == "terrain":
            red = int(255 * norm)
            green = int(255 * (1 - abs(norm - 0.5) * 2))
            blue = int(255 * (1 - norm))
            color = (red, green, blue)
        elif color_theme == "grayscale":
            shade = int(255 * norm)
            color = (shade, shade, shade)
        elif color_theme == "heat":
            color = plt.cm.inferno(norm)
            color = tuple(int(c * 255) for c in color[:3])
        else:
            color = (255, 255, 255)

        # Highlight hovered bar
        if i in highlight or i == hover_index:
            color = (255, 255, 255)

        # Draw vertical bar
        pygame.draw.rect(screen, color, (x, y, bar_width, height))

    # Draw elevation legend matching the theme
    draw_color_legend(screen, font, color_theme)


def draw_color_legend(screen, font, color_theme):
    # Define rectangle area
    legend_rect = pygame.Rect(10, HEIGHT - 30, 200, 10)

    # Draw gradient bar from left to right
    for x in range(legend_rect.width):
        norm = x / legend_rect.width

        # Match color theme
        if color_theme == "terrain":
            red = int(255 * norm)
            green = int(255 * (1 - abs(norm - 0.5) * 2))
            blue = int(255 * (1 - norm))
            color = (red, green, blue)
        elif color_theme == "grayscale":
            shade = int(255 * norm)
            color = (shade, shade, shade)
        elif color_theme == "heat":
            import matplotlib.pyplot as plt
            cmap_color = plt.cm.inferno(norm)
            color = tuple(int(c * 255) for c in cmap_color[:3])
        else:
            color = (255, 255, 255)

        screen.set_at((legend_rect.x + x, legend_rect.y), color)

    # Add labels
    label_low = font.render("Low", True, (255, 255, 255))
    label_high = font.render("High", True, (255, 255, 255))
    screen.blit(label_low, (legend_rect.x, legend_rect.y - 15))
    screen.blit(label_high, (legend_rect.x + legend_rect.width - 30, legend_rect.y - 15))


def get_summary_text(data):
    if not data:
        return []

    # Sort data by elevation
    sorted_data = sorted(data, key=lambda x: x[2])
    n = len(sorted_data)

    #get points
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

    # Convert flat elevation list into 2D grid
    elevations = [e[2] for e in data]
    grid = np.array(elevations).reshape((rows, cols))

    # Plot using matplotlib
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

    # Extract elevation values and reshape into 2D grids
    original_grid = np.array([e[2] for e in original_data]).reshape((rows, cols))
    sorted_grid = np.array([e[2] for e in sorted_data]).reshape((rows, cols))

    #side-by-side plots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    #original
    im1 = axes[0].imshow(original_grid, cmap='terrain', aspect='auto', origin='lower')
    axes[0].set_title("Original Elevation Grid")
    fig.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

    #sorted
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

def bubble_sort_visualized(data, screen, clock, metrics, color_theme):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            metrics["comparisons"] += 1
            if stable_key(data[j]) > stable_key(data[j + 1]):
                if data[j] != data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    metrics["swaps"] += 1
            draw_bars(screen, data, font, highlight=[j, j + 1], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            pygame.time.wait(5)



def quick_sort_visualized(data, screen, clock, metrics, color_theme):
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
            metrics["comparisons"] += 1
            draw_bars(screen, arr, font, highlight=[j, high], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            time.sleep(0.01)
            if stable_key(arr[j]) < stable_key(pivot):
                i += 1
                if arr[i] != arr[j]:
                    arr[i], arr[j] = arr[j], arr[i]
                    metrics["swaps"] += 1
        if arr[i + 1] != arr[high]:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            metrics["swaps"] += 1
        return i + 1

    quick_sort(data, 0, len(data) - 1)

    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
    pygame.display.flip()

def merge_sort_visualized(data, screen, clock, metrics, color_theme):
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
            metrics["comparisons"] += 1
            new_val = left[i] if stable_key(left[i]) <= stable_key(right[j]) else right[j]
            if arr[k] != new_val:
                arr[k] = new_val
                metrics["swaps"] += 1
            else:
                arr[k] = new_val
            draw_bars(screen, data, font, highlight=[k], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            time.sleep(0.01)
            k += 1
            if stable_key(left[i]) <= stable_key(right[j]):
                i += 1
            else:
                j += 1
        while i < len(left):
            if arr[k] != left[i]:
                arr[k] = left[i]
                metrics["swaps"] += 1
            else:
                arr[k] = left[i]
            draw_bars(screen, data, font, highlight=[k], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            time.sleep(0.01)
            i += 1
            k += 1
        while j < len(right):
            if arr[k] != right[j]:
                arr[k] = right[j]
                metrics["swaps"] += 1
            else:
                arr[k] = right[j]
            draw_bars(screen, data, font, highlight=[k], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            time.sleep(0.01)
            j += 1
            k += 1

    merge_sort(data, 0, len(data) - 1)

    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
    pygame.display.flip()



def insertion_sort_visualized(data, screen, clock, metrics, color_theme):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            metrics["comparisons"] += 1
            if stable_key(data[j]) > stable_key(key):
                if data[j + 1] != data[j]:
                    data[j + 1] = data[j]
                    metrics["swaps"] += 1
                else:
                    data[j + 1] = data[j]
                j -= 1
                draw_bars(screen, data, font, highlight=[j + 1], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
                pygame.display.flip()
                pygame.time.wait(10)
            else:
                break
        if data[j + 1] != key:
            data[j + 1] = key
            metrics["swaps"] += 1



    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
    pygame.display.flip()


def selection_sort_visualized(data, screen, clock, metrics, color_theme):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)
    n = len(data)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            metrics["comparisons"] += 1
            if stable_key(data[j]) < stable_key(data[min_idx]):
                min_idx = j
            draw_bars(screen, data, font, highlight=[j, min_idx], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            pygame.time.wait(10)
        if i != min_idx and data[i] != data[min_idx]:
            data[i], data[min_idx] = data[min_idx], data[i]
            metrics["swaps"] += 1


    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
    pygame.display.flip()


def heap_sort_visualized(data, screen, clock, metrics, color_theme):
    font = pygame.font.SysFont("Arial", 14)
    min_elev = min(e[2] for e in data)
    max_elev = max(e[2] for e in data)

    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n:
            metrics["comparisons"] += 1
            if stable_key(arr[l]) > stable_key(arr[largest]):
                largest = l
        if r < n:
            metrics["comparisons"] += 1
            if stable_key(arr[r]) > stable_key(arr[largest]):
                largest = r
        if largest != i:
            if arr[i] != arr[largest]:
                arr[i], arr[largest] = arr[largest], arr[i]
                metrics["swaps"] += 1
            draw_bars(screen, data, font, highlight=[i, largest], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
            pygame.display.flip()
            pygame.time.wait(10)
            heapify(arr, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)
    for i in range(n - 1, 0, -1):
        if data[i] != data[0]:
            data[i], data[0] = data[0], data[i]
            metrics["swaps"] += 1
        draw_bars(screen, data, font, highlight=[0, i], min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
        pygame.display.flip()
        pygame.time.wait(10)
        heapify(data, i, 0)



    draw_bars(screen, data, font, min_elev=min_elev, max_elev=max_elev, color_theme=color_theme)
    pygame.display.flip()


def run_visualizer(data, default_sort_func, rows, cols):
    import random
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elevation Sort Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 14)

    # Available sorting algorithms and color themes
    sort_funcs = {
        "Quick": quick_sort_visualized,
        "Merge": merge_sort_visualized,
        "Insertion": insertion_sort_visualized,
        "Selection": selection_sort_visualized,
        "Heap": heap_sort_visualized,
        "Bubble": bubble_sort_visualized
    }

    color_themes = ["terrain", "grayscale", "heat"]
    current_theme_index = 0

    # Create buttons
    button_width = 100
    button_height = 25
    buttons = []
    for i, name in enumerate(sort_funcs):
        rect = pygame.Rect(10 + i * (button_width + 10), 10, button_width, button_height)
        buttons.append((rect, name))

    current_sort = None
    sorted_once = False
    running = True

    # Initial data and summary setup
    data, summary_lines = reset_visualization_state(data, rows, cols)
    original_data = data.copy()
    working_data = original_data.copy()
    sort_duration = 0
    metrics = {"comparisons": 0, "swaps": 0}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #Reset
                    data, summary_lines = reset_visualization_state(data, rows, cols)
                    original_data = data.copy()
                    working_data = original_data.copy()
                    sorted_once = False
                    current_sort = None
                    sort_duration = 0
                    metrics = {"comparisons": 0, "swaps": 0}
                elif event.key == pygame.K_s: # Shuffle
                    random.shuffle(working_data)
                    sorted_once = False
                    current_sort = None
                    sort_duration = 0
                    metrics = {"comparisons": 0, "swaps": 0}
                    summary_lines = get_summary_text(working_data)
                elif event.key == pygame.K_c:  # Switch color theme
                    current_theme_index = (current_theme_index + 1) % len(color_themes)
                elif event.key == pygame.K_ESCAPE:  # Quit
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, name in buttons:
                    if rect.collidepoint(mx, my):
                        current_sort = sort_funcs[name]
                        working_data = working_data.copy()
                        sorted_once = False
                        sort_duration = 0
                        metrics = {"comparisons": 0, "swaps": 0}

        if current_sort and not sorted_once:
            original_copy = working_data.copy()
            start_time = time.time()
            # Run selected sort
            current_sort(working_data, screen, clock, metrics, color_themes[current_theme_index])
            sort_duration = time.time() - start_time
            sorted_once = True
            summary_lines = get_summary_text(working_data)
            show_comparison_heatmap(original_copy, working_data, rows, cols)

        # Hover
        mouse_x, _ = pygame.mouse.get_pos()
        bar_width = max(1, WIDTH // len(working_data))
        hover_index = mouse_x // bar_width if bar_width else None

        draw_bars(screen, working_data, font, hover_index=hover_index, color_theme=color_themes[current_theme_index])

        # Draw buttons
        for rect, name in buttons:
            color = (200, 50, 50) if sort_funcs[name] == current_sort else (50, 50, 200)
            pygame.draw.rect(screen, color, rect)
            label = font.render(name, True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=rect.center))

        # Draw summary text
        for i, line in enumerate(summary_lines):
            label = font.render(line, True, (255, 255, 255))
            screen.blit(label, (10, 50 + i * 20))

        # Show sorting metrics
        if current_sort and sorted_once:
            label_time = font.render(f"Sort Time: {sort_duration:.2f}s", True, (255, 255, 255))
            screen.blit(label_time, (10, 50 + len(summary_lines) * 20))
            label_comp = font.render(f"Comparisons: {metrics['comparisons']}", True, (255, 255, 255))
            screen.blit(label_comp, (10, 50 + len(summary_lines) * 20 + 20))
            label_swaps = font.render(f"Swaps: {metrics['swaps']}", True, (255, 255, 255))
            screen.blit(label_swaps, (10, 50 + len(summary_lines) * 20 + 40))

        # Show hover info
        if hover_index is not None and 0 <= hover_index < len(working_data):
            lat, lon, elev, _ = working_data[hover_index]
            hover_label = font.render(f"{lat:.2f}, {lon:.2f} → {elev:.2f} m", True, (255, 255, 0))
            screen.blit(hover_label, (WIDTH - 260, HEIGHT - 40))

        # Footer text
        footer = font.render("R = Reset | S = Shuffle | C = Theme | ESC = Quit | Click a sort", True, (180, 180, 180))
        screen.blit(footer, (10, HEIGHT - 20))

        pygame.display.flip()

    pygame.quit()


