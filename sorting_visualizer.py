# sorting_visualizer.py
import pygame
import time

WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 5
FPS = 60

def draw_bars(screen, data, highlight=[]):
    screen.fill((0, 0, 0))
    if not data:
        return

    elevations = [e[2] for e in data]
    max_elev = max(elevations)
    min_elev = min(elevations)
    elev_range = max_elev - min_elev if max_elev != min_elev else 1

    bar_width = max(1, WIDTH // len(data))

    for i, (_, _, elev) in enumerate(data):
        height = int((elev - min_elev) / elev_range * HEIGHT)
        x = i * bar_width
        y = HEIGHT - height

        # Elevation gradient: blue (low) → green (mid) → red (high)
        norm = (elev - min_elev) / elev_range
        red = int(255 * norm)
        green = int(255 * (1 - abs(norm - 0.5) * 2))
        blue = int(255 * (1 - norm))
        color = (red, green, blue)

        if i in highlight:
            color = (255, 255, 255)

        pygame.draw.rect(screen, color, (x, y, bar_width, height))


def quick_sort_visualized(data, screen, clock):
    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high][2]
        i = low - 1
        for j in range(low, high):
            draw_bars(screen, arr, highlight=[j, high])
            pygame.display.flip()
            time.sleep(0.01)
            if arr[j][2] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    quick_sort(data, 0, len(data) - 1)
    draw_bars(screen, data)
    pygame.display.flip()

def merge_sort_visualized(data, screen, clock):
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
            if left[i][2] <= right[j][2]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            draw_bars(screen, data, highlight=[k])
            pygame.display.flip()
            time.sleep(0.01)
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            draw_bars(screen, data, highlight=[k])
            pygame.display.flip()
            time.sleep(0.01)
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            draw_bars(screen, data, highlight=[k])
            pygame.display.flip()
            time.sleep(0.01)
            k += 1

    merge_sort(data, 0, len(data) - 1)
    draw_bars(screen, data)
    pygame.display.flip()

def insertion_sort_visualized(data, screen, clock):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j][2] > key[2]:
            data[j + 1] = data[j]
            j -= 1
            draw_bars(screen, data, highlight=[j + 1])
            pygame.display.flip()
            pygame.time.wait(10)
        data[j + 1] = key
    draw_bars(screen, data)
    pygame.display.flip()


def selection_sort_visualized(data, screen, clock):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j][2] < data[min_idx][2]:
                min_idx = j
            draw_bars(screen, data, highlight=[j, min_idx])
            pygame.display.flip()
            pygame.time.wait(10)
        data[i], data[min_idx] = data[min_idx], data[i]
    draw_bars(screen, data)
    pygame.display.flip()

def heap_sort_visualized(data, screen, clock):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l][2] > arr[largest][2]:
            largest = l
        if r < n and arr[r][2] > arr[largest][2]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            draw_bars(screen, data, highlight=[i, largest])
            pygame.display.flip()
            pygame.time.wait(10)
            heapify(arr, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw_bars(screen, data, highlight=[0, i])
        pygame.display.flip()
        pygame.time.wait(10)
        heapify(data, i, 0)

    draw_bars(screen, data)
    pygame.display.flip()



def run_visualizer(data, sort_func):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elevation Sort Visualizer")
    clock = pygame.time.Clock()

    original_data = data.copy()
    sorted_once = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Press R to replay sort
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                data = original_data.copy()
                sorted_once = False

        if not sorted_once:
            sort_func(data, screen, clock)
            sorted_once = True

        draw_bars(screen, data)
        pygame.display.flip()

    pygame.quit()
