import pygame
import random
import math

class HappyFace:
    def __init__(self, screen, color=(0, 200, 255)):
        self.screen = screen
        self.color = color
        self.center_x = self.screen.get_width() // 2
        self.center_y = self.screen.get_height() // 2
        
        self.eye_size = 300
        self.eye_radius = 70
        self.eye_spacing = 120
        self.eye_height = self.eye_size
        self.right_eye_height = self.eye_size  # Chiều cao riêng cho mắt phải
        self.x_offset, self.y_offset = 0, 0
        
        self.last_blink = pygame.time.get_ticks()
        self.blink_interval = random.randint(2000, 5000)
        self.is_blinking = False
        self.blink_timer = 0
        self.blink_duration = 30
        
        # Biến cho hiệu ứng nháy một mắt bên phải
        self.is_winking = False
        self.wink_timer = 0
        self.wink_duration = 20  # 20 frame cho nháy một mắt
        self.target_right_eye_height = int(self.eye_size * 0.05)  # Thu còn 5%

        # Biến cho hiệu ứng nhắm mắt, gập thành mái nhà và nhích lên xuống
        self.is_closing = False
        self.is_folded = False
        self.close_timer = 0
        self.close_duration = 60  # Thời gian để nhắm mắt
        self.fold_duration = 180  # Thời gian giữ hình mái nhà
        self.bounce_timer = 0
        self.target_eye_height = self.eye_size

        # Biến cho hiệu ứng nhấp nhô
        self.bob_duration = 180  # 3 giây
        self.bob_amplitude = 10  # Biên độ nhấp nhô
        self.bob_period = 120  # Chu kỳ nhấp nhô (2 giây)
        self.is_bobbing = False  # Trạng thái nhấp nhô

        # Biến cho trạng thái chờ
        self.is_waiting = False
        self.wait_duration = 600  # 10 giây chờ trước idle_bob

        # Biến cho hiệu ứng nhiễu TV
        self.noise_y = 0  # Vị trí y của đường nhiễu
        self.noise_period = 180  # Chu kỳ 3 giây
        self.noise_speed = self.screen.get_height() / self.noise_period  # Tốc độ di chuyển

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Cập nhật vị trí đường nhiễu, chỉ khi không gập mắt
        if not self.is_folded:
            self.noise_y += self.noise_speed
            if self.noise_y >= self.screen.get_height():
                self.noise_y = 0  # Quay lại đỉnh khi chạm đáy

        # Logic nháy mắt ngẫu nhiên, chỉ khi không nhắm, không gập, không chờ, không nhấp nhô, không nháy một mắt
        if not self.is_blinking and not self.is_closing and not self.is_folded and not self.is_waiting and not self.is_bobbing and not self.is_winking and current_time - self.last_blink > self.blink_interval:
            self.is_blinking = True
            self.blink_timer = 0
        
        if self.is_blinking:
            self.blink_timer += 1
            t = self.blink_timer / self.blink_duration
            self.eye_height = int(self.eye_size * (1 - abs(math.cos(t * math.pi)))) + 20
            self.right_eye_height = self.eye_height  # Đồng bộ mắt phải
            if self.blink_timer >= self.blink_duration:
                self.is_blinking = False
                self.eye_height = self.eye_size
                self.right_eye_height = self.eye_size
                self.last_blink = current_time
                self.blink_interval = random.randint(2000, 5000)
                self.is_waiting = True
                self.close_timer = 0
        
        # Logic nháy một mắt bên phải
        if not self.is_blinking and not self.is_closing and not self.is_folded and not self.is_waiting and not self.is_bobbing and not self.is_winking and random.random() < 0.0025:
            self.is_winking = True
            self.wink_timer = 0
        
        if self.is_winking:
            self.wink_timer += 1
            if self.wink_timer <= self.wink_duration / 2:
                # Thu nhỏ mắt phải
                t = self.wink_timer / (self.wink_duration / 2)
                self.right_eye_height = int(self.eye_size * (1 - t) + self.target_right_eye_height * t)
                self.eye_height = self.eye_size  # Mắt trái giữ nguyên
            else:
                # Mở mắt phải
                t = (self.wink_timer - self.wink_duration / 2) / (self.wink_duration / 2)
                self.right_eye_height = int(self.target_right_eye_height * (1 - t) + self.eye_size * t)
                self.eye_height = self.eye_size  # Mắt trái giữ nguyên
            if self.wink_timer >= self.wink_duration:
                self.is_winking = False
                self.right_eye_height = self.eye_size
                self.eye_height = self.eye_size
                self.is_waiting = True
                self.close_timer = 0
        
        # Logic hiệu ứng nhắm mắt, gập thành mái nhà và nhích lên xuống
        if not self.is_blinking and not self.is_folded and not self.is_waiting and not self.is_bobbing and not self.is_winking and random.random() < 0.0025:
            self.is_closing = True
            self.close_timer = 0
            self.target_eye_height = int(self.eye_size * 0.2)
        
        if self.is_closing:
            self.close_timer += 1
            if self.close_timer <= self.close_duration:
                t = self.close_timer / self.close_duration
                self.eye_height = int(self.eye_size * (1 - t) + self.target_eye_height * t)
                self.right_eye_height = self.eye_height  # Đồng bộ mắt phải
            else:
                self.is_closing = False
                self.is_folded = True
                self.close_timer = 0
        
        if self.is_folded:
            self.close_timer += 1
            if self.close_timer <= self.fold_duration:
                self.bounce_timer += 0.1
                self.y_offset = math.sin(self.bounce_timer) * 20
                self.right_eye_height = self.eye_height  # Đồng bộ mắt phải
            else:
                self.is_folded = False
                self.eye_height = self.eye_size
                self.right_eye_height = self.eye_size
                self.y_offset = 0
                self.bounce_timer = 0
                self.close_timer = 0
                self.is_waiting = True
        
        # Logic chờ 10 giây trước khi nhấp nhô
        if self.is_waiting:
            self.close_timer += 1
            if self.close_timer >= self.wait_duration:
                self.is_waiting = False
                self.is_bobbing = True
                self.close_timer = 0
        
        # Logic nhấp nhô
        if self.is_bobbing:
            self.close_timer += 1
            t = self.close_timer / self.bob_period
            self.y_offset = self.bob_amplitude * math.sin(2 * math.pi * t)
            self.eye_height = self.eye_size
            self.right_eye_height = self.eye_size
            if self.close_timer >= self.bob_duration:
                self.is_bobbing = False
                self.y_offset = 0
                self.close_timer = 0
                # Chọn hành động ngẫu nhiên mới
                rand = random.random()
                if rand < 0.33:  # 33% nháy cả hai mắt
                    self.is_blinking = True
                    self.blink_timer = 0
                elif rand < 0.66:  # 33% nháy một mắt
                    self.is_winking = True
                    self.wink_timer = 0
                else:  # 33% nhắm mắt/gập
                    self.is_closing = True
                    self.close_timer = 0
                    self.target_eye_height = int(self.eye_size * 0.2)

    def draw(self):
        if self.is_folded:
            # Vẽ mắt gập thành hình mái nhà (^ ^) bằng tam giác
            half_eye_size = self.eye_size // 2
            inner_color = (0, 0, 0)
            inner_scale = 0.5
            inner_eye_size = half_eye_size * inner_scale
            inner_eye_height = self.eye_height * inner_scale
            
            left_eye_center_x = self.center_x - self.eye_spacing // 2 - half_eye_size
            left_eye_points = [
                (left_eye_center_x - half_eye_size, self.center_y + self.y_offset),
                (left_eye_center_x + half_eye_size, self.center_y + self.y_offset),
                (left_eye_center_x, self.center_y - self.eye_height + self.y_offset)
            ]
            left_inner_points = [
                (left_eye_center_x - inner_eye_size, self.center_y + self.y_offset),
                (left_eye_center_x + inner_eye_size, self.center_y + self.y_offset),
                (left_eye_center_x, self.center_y - inner_eye_height + self.y_offset)
            ]
            
            right_eye_center_x = self.center_x + self.eye_spacing // 2 + half_eye_size
            right_eye_points = [
                (right_eye_center_x - half_eye_size, self.center_y + self.y_offset),
                (right_eye_center_x + half_eye_size, self.center_y + self.y_offset),
                (right_eye_center_x, self.center_y - self.eye_height + self.y_offset)
            ]
            right_inner_points = [
                (right_eye_center_x - inner_eye_size, self.center_y + self.y_offset),
                (right_eye_center_x + inner_eye_size, self.center_y + self.y_offset),
                (right_eye_center_x, self.center_y - inner_eye_height + self.y_offset)
            ]
            
            pygame.draw.polygon(self.screen, self.color, left_eye_points)
            pygame.draw.polygon(self.screen, self.color, right_eye_points)
            pygame.draw.polygon(self.screen, inner_color, left_inner_points)
            pygame.draw.polygon(self.screen, inner_color, right_inner_points)
        else:
            # Vẽ mắt bình thường bằng hình chữ nhật
            left_eye_x = self.center_x - self.eye_size - self.eye_spacing // 2 + self.x_offset
            left_eye_y = self.center_y - self.eye_height // 2 + self.y_offset
            left_eye_rect = pygame.Rect(left_eye_x, left_eye_y, self.eye_size, self.eye_height)

            right_eye_x = self.center_x + self.eye_spacing // 2 + self.x_offset
            right_eye_y = self.center_y - self.right_eye_height // 2 + self.y_offset
            right_eye_rect = pygame.Rect(right_eye_x, right_eye_y, self.eye_size, self.right_eye_height)

            pygame.draw.rect(self.screen, self.color, left_eye_rect, border_radius=self.eye_radius)
            pygame.draw.rect(self.screen, self.color, right_eye_rect, border_radius=self.eye_radius)

        # Hiệu ứng nhiễu TV: đường ngang di chuyển từ trên xuống, chỉ khi không gập mắt
        if not self.is_folded:
            noise_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            y = int(self.noise_y)
            pygame.draw.line(noise_surface, (255, 255, 255, 100), (0, y), (self.screen.get_width(), y), 2)
            self.screen.blit(noise_surface, (0, 0))
