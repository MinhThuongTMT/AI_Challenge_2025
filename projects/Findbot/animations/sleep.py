import pygame

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
DARK_GRAY = (30, 30, 30)
BLUE = (0, 200, 255)
WHITE = (240, 240, 240)

def draw_sleeping_face(z_offset=0):
    screen.fill(DARK_GRAY)

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Mắt
    eye_width = 400
    eye_height = 40
    eye_radius = 20
    spacing = 120

    # Hai mắt nhắm (hình chữ nhật dẹt)
    left_eye_x = center_x - eye_width - spacing // 2
    left_eye_y = center_y - eye_height // 2
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_width, eye_height)

    right_eye_x = center_x + spacing // 2
    right_eye_y = center_y - eye_height // 2
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_width, eye_height)

    pygame.draw.rect(screen, BLUE, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, BLUE, right_eye_rect, border_radius=eye_radius)

    # Vẽ các chữ "Z" đang bay lên
    font = pygame.font.SysFont(None, 100)
    for i in range(3):
        text = font.render("Z", True, WHITE)
        x = center_x + 300 + i * 50
        y = center_y - 150 - z_offset + i * -60  # bay lên cao dần
        screen.blit(text, (x, y))
