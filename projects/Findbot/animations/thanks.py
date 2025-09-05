import pygame
import math  # Dùng math.sin thay vì pygame.math.sin

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)

DARK_GRAY = (30, 30, 30)
BLUE = (0, 200, 255)
WHITE = (255, 255, 255)

def draw_thanks_face(frame):
    screen.fill(DARK_GRAY)

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Sáng tối nhẹ theo sóng sin (hiệu ứng nhấp nháy)
    intensity = int(100 + 100 * abs(math.sin(frame * 0.1)))  # Giá trị từ 100 -> 200
    blink_blue = (0, intensity, 255)

    # Mắt robot
    eye_width = 300
    eye_height = 200
    eye_radius = 70
    spacing = 120

    left_eye_x = center_x - eye_width - spacing // 2
    left_eye_y = center_y - eye_height // 2
    left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, eye_width, eye_height)

    right_eye_x = center_x + spacing // 2
    right_eye_y = center_y - eye_height // 2
    right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, eye_width, eye_height)

    pygame.draw.rect(screen, blink_blue, left_eye_rect, border_radius=eye_radius)
    pygame.draw.rect(screen, blink_blue, right_eye_rect, border_radius=eye_radius)

    # Vẽ chữ "Thank You 😊"
    font = pygame.font.SysFont(None, 120)
    text = font.render("Thank You", True, WHITE)
    text_rect = text.get_rect(center=(center_x, center_y + 250))
    screen.blit(text, text_rect)
