import pygame

# Constants
WIDTH = 800
HEIGHT = 600
BAR_WIDTH = 5
FPS = 60

def bubble_sort_visualized(data, screen, clock):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_bars(screen, data, highlight=[j, j+1])
            pygame.display.flip()
            clock.tick(FPS)

            if data[j][2] > data[j + 1][2]:
                data[j], data[j + 1] = data[j + 1], data[j]

    draw_bars(screen, data)
    pygame.display.flip()

def draw_bars(screen, data, highlight=[]):
    screen.fill((0, 0, 0))  # Clear screen
    max_elev = max(e[2] for e in data)
    min_elev = min(e[2] for e in data)

    for i, (_, _, elev) in enumerate(data):
        height = int((elev - min_elev) / (max_elev - min_elev + 1e-6) * HEIGHT)
        x = i * BAR_WIDTH
        color = (255, 255, 255)

        if i in highlight:
            color = (255, 0, 0)  # Red for elements being compared

        pygame.draw.rect(screen, color, (x, HEIGHT - height, BAR_WIDTH, height))

# Optional test run
if __name__ == "__main__":
    import random
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bubble Sort - Elevation Visualizer")
    clock = pygame.time.Clock()

    # Fake data for testing: 100 bars with random elevation
    test_data = [(0, 0, random.randint(-6000, 8000)) for _ in range(WIDTH // BAR_WIDTH)]

    running = True
    sorted_once = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not sorted_once:
            bubble_sort_visualized(test_data, screen, clock)
            sorted_once = True

    pygame.quit()