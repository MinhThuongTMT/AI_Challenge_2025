import pygame


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
DARK_GRAY = (30, 30, 30)
BLUE = (0, 200, 255)

def draw_listening_dots(frame):
    screen.fill(DARK_GRAY)

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    dot_radius = 80
    spacing = 300

    active_dot = (frame // 15) % 4

    for i in range(3):
        x = center_x + (i - 1) * spacing
        y = center_y
        color = BLUE if i < active_dot else (80, 80, 80)  # sáng dần
        pygame.draw.circle(screen, color, (x, y), dot_radius)
