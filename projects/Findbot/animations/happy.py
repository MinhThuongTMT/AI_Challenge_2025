import pygame

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
# 001
DARK_GRAY_001 = (30, 30, 30)
BLUE_001 = (0, 200, 255)

def draw_happy_face0():
    screen.fill(DARK_GRAY_001)

    # R
    center_x = SCREEN_WIDTH // 2  # 900
    center_y = SCREEN_HEIGHT // 2  # 500

    # Eye Config
    eye_size = 300
    eye_radius = 70
    eye_spacing = 120

    # Left eye
    left_eye_x = center_x - eye_size - eye_spacing // 2
    left_eye_y = center_y - eye_size // 2
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_size, eye_size)

    # Right eye
    right_eye_x = center_x + eye_spacing // 2
    right_eye_y = center_y - eye_size // 2
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_size, eye_size)

    # Vẽ 2 mắt
    pygame.draw.rect(screen, BLUE_001, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, BLUE_001, right_eye_rect, border_radius=eye_radius)

def draw_happy_face1():
    screen.fill(DARK_GRAY_001)

    # R
    center_x = SCREEN_WIDTH // 2  # 900
    center_y = SCREEN_HEIGHT // 2  # 500

    # Eye Config
    eye_size = 300
    eye_radius = 70
    eye_spacing = 120

    # Left eye
    left_eye_x = center_x - eye_size - eye_spacing // 2 - 140
    left_eye_y = center_y - eye_size // 2 - 100
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_size, eye_size)

    # Right eye
    right_eye_x = center_x + eye_spacing // 2 - 140
    right_eye_y = center_y - eye_size // 2 - 100
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_size, eye_size)

    # Vẽ 2 mắt
    pygame.draw.rect(screen, BLUE_001, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, BLUE_001, right_eye_rect, border_radius=eye_radius)

def draw_happy_face2():
    screen.fill(DARK_GRAY_001)

    # R
    center_x = SCREEN_WIDTH // 2  # 900
    center_y = SCREEN_HEIGHT // 2  # 500

    # Eye Config
    eye_size = 300
    eye_radius = 70
    eye_spacing = 120

    # Left eye
    left_eye_x = center_x - eye_size - eye_spacing // 2 - 140
    left_eye_y = center_y - eye_size // 2 + 100
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_size, eye_size)

    # Right eye
    right_eye_x = center_x + eye_spacing // 2 - 140
    right_eye_y = center_y - eye_size // 2 + 100
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_size, eye_size)

    # Vẽ 2 mắt
    pygame.draw.rect(screen, BLUE_001, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, BLUE_001, right_eye_rect, border_radius=eye_radius)

def draw_happy_face_offset(x_offset=0, y_offset=0):
    center_x = SCREEN_WIDTH // 2 + x_offset
    center_y = SCREEN_HEIGHT // 2 + y_offset

    eye_size = 300
    eye_radius = 70
    eye_spacing = 120

    left_eye_x = center_x - eye_size - eye_spacing // 2
    left_eye_y = center_y - eye_size // 2
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_size, eye_size)

    right_eye_x = center_x + eye_spacing // 2
    right_eye_y = center_y - eye_size // 2
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_size, eye_size)

    pygame.draw.rect(screen, BLUE_001, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, BLUE_001, right_eye_rect, border_radius=eye_radius)

def draw_happy_face_blink(x_offset=0, y_offset=0, eye_height=40):
    screen.fill(DARK_GRAY_001)

    center_x = SCREEN_WIDTH // 2 + x_offset
    center_y = SCREEN_HEIGHT // 2 + y_offset

    eye_width = 300
    eye_radius = 20
    eye_spacing = 120

    left_eye_x = center_x - eye_width - eye_spacing // 2
    left_eye_y = center_y - eye_height // 2
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_width, eye_height)

    right_eye_x = center_x + eye_spacing // 2
    right_eye_y = center_y - eye_height // 2
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_width, eye_height)

    pygame.draw.rect(screen, BLUE_001, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, BLUE_001, right_eye_rect, border_radius=eye_radius)
