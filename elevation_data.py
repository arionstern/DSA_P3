# sorting_visualizer.py
import pygame
import time

WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 5
FPS = 60

def draw_bars(screen, data, highlight=[]):
    screen.fill((0, 0, 0))
    max_elev = max(e[2] for e in data)
    min_elev = min(e[2] for e in data)

    bar_width = max(1, WIDTH // len(data))

    for i, (_, _, elev) in enumerate(data):
        height = int((elev - min_elev) / (max_elev - min_elev + 1e-6) * HEIGHT)
        x = i * bar_width
        color = (255, 255, 255)
        if i in highlight:
            color = (255, 0, 0)
        pygame.draw.rect(screen, color, (x, HEIGHT - height, bar_width, height))

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



def run_visualizer(data, algo):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elevation Sort Visualizer")
    clock = pygame.time.Clock()

    running = True
    sorted_once = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not sorted_once:
            if algo == "quick":
                quick_sort_visualized(data, screen, clock)
            elif algo == "merge":
                merge_sort_visualized(data, screen, clock)
            sorted_once = True

        draw_bars(screen, data)
        pygame.display.flip()

    pygame.quit()
