# animations/listening.py
import pygame
import math

class ListeningDots:
    def __init__(self, screen, color=(0, 200, 255)):
        self.screen = screen
        self.color = color
        self.center_x = self.screen.get_width() // 2
        self.center_y = self.screen.get_height() // 2
        
        self.dot_radius = 40
        self.spacing = 100
        self.num_dots = 3
        
    def update(self):
        pass # Không cần update liên tục, chỉ cần vẽ theo thời gian thực

    def draw(self):
        start_x = self.center_x - (self.num_dots - 1) * self.spacing // 2
        for i in range(self.num_dots):
            y_offset = int(40 * math.sin(pygame.time.get_ticks() / 150.0 + i * math.pi / 2))
            dot_x = start_x + i * self.spacing
            dot_y = self.center_y + y_offset
            pygame.draw.circle(self.screen, self.color, (dot_x, dot_y), self.dot_radius)
