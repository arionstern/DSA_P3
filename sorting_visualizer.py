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
    def merge_sort(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]

            merge_sort(L)
            merge_sort(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i][2] < R[j][2]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
                if k % 5 == 0:
                    draw_bars(screen, data)
                    pygame.display.flip()
                    time.sleep(0.01)

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
                if k % 5 == 0:
                    draw_bars(screen, data)
                    pygame.display.flip()
                    time.sleep(0.01)

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
                if k % 5 == 0:
                    draw_bars(screen, data)
                    pygame.display.flip()
                    time.sleep(0.01)

    merge_sort(data)
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
