import pygame
import matplotlib.pyplot as plt
from bridges.bridges import Bridges

print("✅ All libraries imported successfully!")

# Optional: open a blank pygame window just to confirm it runs
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame Test")
screen.fill((255, 255, 255))
pygame.display.flip()

# Wait a couple seconds and quit
pygame.time.wait(2000)
pygame.quit()