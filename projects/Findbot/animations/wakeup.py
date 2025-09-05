import pygame

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

screen_wk = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)

DARK_GRAY = (30, 30, 30)
BLUE = (0, 200, 255)

def draw_wakeup_face(frame):
    screen_wk.fill(DARK_GRAY)

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    eye_width = 300
    eye_spacing = 120
    eye_radius = 20

    # Mắt mở dần theo frame
    max_eye_height = 300
    eye_height = min(max_eye_height, int(frame * 10))  # mỗi frame mở thêm 10px

    left_eye_x = center_x - eye_width - eye_spacing // 2
    left_eye_y = center_y - eye_height // 2
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_width, eye_height)

    right_eye_x = center_x + eye_spacing // 2
    right_eye_y = center_y - eye_height // 2
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_width, eye_height)

    pygame.draw.rect(screen_wk, BLUE, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen_wk, BLUE, right_eye_rect, border_radius=eye_radius)
