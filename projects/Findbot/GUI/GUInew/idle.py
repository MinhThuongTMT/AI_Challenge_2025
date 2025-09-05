import pygame
import random
import math

class IdleFace:
    def __init__(self, screen, color=(0, 200, 255)):
        self.screen = screen
        self.base_color = color
        self.color = color
        self.center_x = self.screen.get_width() // 2
        self.center_y = self.screen.get_height() // 2
        
        self.eye_size = 300
        self.eye_radius = 70
        self.eye_spacing = 120
        self.eye_height = self.eye_size
        self.x_offset, self.y_offset = 0, 0
        self.left_y_offset, self.right_y_offset = 0, 0
        self.rotation_angle = 0
        
        self.state = "sleeping"
        self.state_timer = 0
        self.awake_duration = 6000  # 10 giây
        self.sleep_duration = 600  # 10 giây
        
        self.sub_state = None
        self.sub_state_timer = 0
        self.is_waiting = False
        self.wait_duration = 600
        
        self.blink_duration = 30
        self.is_blinking = False
        self.bubbles = []
        self.bubble_timer = 0
        self.color_shift_timer = 0
        self.color_shift_speed = 0.02
        self.droop_duration = 45
        self.is_drooping = False
        self.target_y_offset = 100
        self.up_offset = -50
        self.look_duration = 15
        self.look_wait_duration = 180
        self.look_amplitude = 70
        self.diagonal_amplitude = 50
        self.squint_duration = 60
        self.is_squinting = False
        self.squint_scale = 1.0
        self.slam_duration = 12
        self.slam_down_offset = 84
        self.slam_up_offset = -50
        self.tilt_offset = 20
        self.tilt_angle = 13
        self.is_slamming = False
        self.slam_wait_duration = 150
        self.left_eye_scale = 1.0
        self.right_eye_scale = 1.0
        self.bob_duration = 180
        self.bob_amplitude = 10
        self.bob_period = 120
        self.noise_y = 0
        self.noise_period = 180
        self.noise_speed = self.screen.get_height() / self.noise_period

    def slam(self):
        self.state = "looking_around"  # Chuyển ngay sang looking_around
        self.eye_height = self.eye_size  # Đặt mắt mở hoàn toàn
        self.state_timer = 0
        self.bubbles = []  # Xóa bong bóng nếu đang sleeping
        self.noise_y = 0
        self.sub_state = "slam"
        self.sub_state_timer = 0
        self.is_slamming = True
        self.is_waiting = False

    def update(self):
        self.state_timer += 1
        self.color_shift_timer += 1

        if self.state == "looking_around":
            self.noise_y += self.noise_speed
            if self.noise_y >= self.screen.get_height():
                self.noise_y = 0

        r = int(self.base_color[0] + 20 * math.sin(self.color_shift_timer * self.color_shift_speed))
        g = int(self.base_color[1] + 20 * math.sin(self.color_shift_timer * self.color_shift_speed + 2))
        b = int(self.base_color[2] + 20 * math.sin(self.color_shift_timer * self.color_shift_speed + 4))
        self.color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

        if self.state == "sleeping":
            self.eye_height = 40
            self.x_offset, self.y_offset = 0, 0
            self.left_y_offset, self.right_y_offset = 0, 0
            self.rotation_angle = 0
            self.squint_scale = 1.0
            self.left_eye_scale = 1.0
            self.right_eye_scale = 1.0
            self.sub_state = None
            self.sub_state_timer = 0
            self.is_waiting = False
            self.bubble_timer += 1
            if self.bubble_timer > 30:
                self.bubbles.append({
                    'x': self.center_x + random.randint(-100, 100),
                    'y': self.center_y,
                    'speed': random.uniform(1, 3),
                    'radius': random.randint(10, 20)
                })
                self.bubble_timer = 0
            for bubble in self.bubbles[:]:
                bubble['y'] -= bubble['speed']
                bubble['radius'] -= 0.1
                if bubble['y'] < self.center_y - 200 or bubble['radius'] <= 0:
                    self.bubbles.remove(bubble)
            if self.state_timer >= self.sleep_duration:
                self.state = "wakeup"
                self.state_timer = 0
                self.bubbles = []
                self.noise_y = 0
        
        elif self.state == "wakeup":
            self.eye_height = min(self.eye_size, self.eye_height + 20)
            self.x_offset, self.y_offset = 0, 0
            self.left_y_offset, self.right_y_offset = 0, 0
            self.rotation_angle = 0
            self.squint_scale = 1.0
            self.left_eye_scale = 1.0
            self.right_eye_scale = 1.0
            self.sub_state = None
            self.sub_state_timer = 0
            self.is_waiting = False
            if self.eye_height >= self.eye_size:
                self.state = "looking_around"
                self.state_timer = 0
                self.noise_y = 0
                
        elif self.state == "looking_around":
            self.eye_height = self.eye_size
            self.sub_state_timer += 1

            if self.sub_state is None and not self.is_waiting:
                rand = random.random()
                if rand < 0.002:
                    self.sub_state = "blink"
                    self.sub_state_timer = 0
                    self.is_blinking = True
                elif rand < 0.005:
                    self.sub_state = "droop"
                    self.sub_state_timer = 0
                    self.is_drooping = True
                elif rand < 0.008:
                    self.sub_state = "look_left"
                    self.sub_state_timer = 0
                elif rand < 0.011:
                    self.sub_state = "look_right"
                    self.sub_state_timer = 0
                elif rand < 0.014:
                    self.sub_state = "squint"
                    self.sub_state_timer = 0
                    self.is_squinting = True
                elif rand < 0.017:
                    self.sub_state = "look_up_left_to_right"
                    self.sub_state_timer = 0
                elif rand < 0.020:
                    self.sub_state = "look_up_right_to_left"
                    self.sub_state_timer = 0
                elif rand < 0.023:
                    self.sub_state = "look_left_squint"
                    self.sub_state_timer = 0
                elif rand < 0.026:
                    self.sub_state = "look_right_squint"
                    self.sub_state_timer = 0

            if self.sub_state == "blink":
                t = self.sub_state_timer / self.blink_duration
                self.eye_height = int(self.eye_size * (1 - abs(math.cos(t * math.pi)))) + 20
                if self.sub_state_timer >= self.blink_duration:
                    self.sub_state = None
                    self.is_blinking = False
                    self.eye_height = self.eye_size
                    self.is_waiting = True
                    self.sub_state_timer = 0

            elif self.sub_state == "droop":
                if self.sub_state_timer <= self.droop_duration:
                    t = self.sub_state_timer / self.droop_duration
                    self.y_offset = self.target_y_offset * t
                    self.eye_height = int(self.eye_size * (1 - 0.9 * t))
                elif self.sub_state_timer <= self.droop_duration + self.droop_duration:
                    t = (self.sub_state_timer - self.droop_duration) / self.droop_duration
                    self.y_offset = self.target_y_offset * (1 - t) + self.up_offset * t
                    self.eye_height = int(self.eye_size * (0.1 + 0.9 * t))
                elif self.sub_state_timer <= self.droop_duration * 2 + self.wait_duration:
                    self.y_offset = self.up_offset
                    self.eye_height = self.eye_size
                else:
                    t = (self.sub_state_timer - (self.droop_duration * 2 + self.wait_duration)) / self.droop_duration
                    self.y_offset = self.up_offset * (1 - t)
                    self.eye_height = self.eye_size
                    if self.sub_state_timer >= self.droop_duration * 3 + self.wait_duration:
                        self.sub_state = None
                        self.is_drooping = False
                        self.y_offset = 0
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "look_left":
                if self.sub_state_timer <= self.look_duration:
                    t = self.sub_state_timer / self.look_duration
                    self.x_offset = -self.look_amplitude * t
                    self.left_eye_scale = 0.85 + 0.15 * t
                    self.right_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                    self.y_offset = self.eye_size * 0.15 / 2
                elif self.sub_state_timer <= self.look_duration + self.look_wait_duration:
                    self.x_offset = -self.look_amplitude
                    self.left_eye_scale = 1.0
                    self.right_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                    self.y_offset = self.eye_size * 0.15 / 2
                else:
                    t = (self.sub_state_timer - (self.look_duration + self.look_wait_duration)) / self.look_duration
                    self.x_offset = -self.look_amplitude * (1 - t)
                    self.left_eye_scale = 1.0
                    self.right_eye_scale = 0.85 + 0.15 * t
                    self.squint_scale = 0.85 + 0.15 * t
                    self.eye_height = int(self.eye_size * (0.85 + 0.15 * t))
                    self.y_offset = self.eye_size * 0.15 * (1 - t) / 2
                    if self.sub_state_timer >= self.look_duration * 2 + self.look_wait_duration:
                        self.sub_state = None
                        self.x_offset = 0
                        self.left_eye_scale = 1.0
                        self.right_eye_scale = 1.0
                        self.squint_scale = 1.0
                        self.eye_height = self.eye_size
                        self.y_offset = 0
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "look_right":
                if self.sub_state_timer <= self.look_duration:
                    t = self.sub_state_timer / self.look_duration
                    self.x_offset = self.look_amplitude * t
                    self.right_eye_scale = 0.85 + 0.15 * t
                    self.left_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                    self.y_offset = self.eye_size * 0.15 / 2
                elif self.sub_state_timer <= self.look_duration + self.look_wait_duration:
                    self.x_offset = self.look_amplitude
                    self.right_eye_scale = 1.0
                    self.left_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                    self.y_offset = self.eye_size * 0.15 / 2
                else:
                    t = (self.sub_state_timer - (self.look_duration + self.look_wait_duration)) / self.look_duration
                    self.x_offset = self.look_amplitude * (1 - t)
                    self.left_eye_scale = 0.85 + 0.15 * t
                    self.right_eye_scale = 1.0
                    self.squint_scale = 0.85 + 0.15 * t
                    self.eye_height = int(self.eye_size * (0.85 + 0.15 * t))
                    self.y_offset = self.eye_size * 0.15 * (1 - t) / 2
                    if self.sub_state_timer >= self.look_duration * 2 + self.look_wait_duration:
                        self.sub_state = None
                        self.x_offset = 0
                        self.left_eye_scale = 1.0
                        self.right_eye_scale = 1.0
                        self.squint_scale = 1.0
                        self.eye_height = self.eye_size
                        self.y_offset = 0
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "look_up_left_to_right":
                if self.sub_state_timer <= self.look_duration:
                    t = self.sub_state_timer / self.look_duration
                    self.x_offset = -self.diagonal_amplitude * t
                    self.y_offset = -self.diagonal_amplitude * t + self.eye_size * 0.15 / 2
                    self.left_eye_scale = 0.85 + 0.15 * t
                    self.right_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                elif self.sub_state_timer <= self.look_duration + self.look_wait_duration:
                    self.x_offset = -self.diagonal_amplitude
                    self.y_offset = -self.diagonal_amplitude + self.eye_size * 0.15 / 2
                    self.left_eye_scale = 1.0
                    self.right_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                else:
                    t = (self.sub_state_timer - (self.look_duration + self.look_wait_duration)) / self.look_duration
                    self.x_offset = -self.diagonal_amplitude * (1 - t)
                    self.y_offset = (-self.diagonal_amplitude + self.eye_size * 0.15 / 2) * (1 - t)
                    self.left_eye_scale = 1.0
                    self.right_eye_scale = 0.85 + 0.15 * t
                    self.squint_scale = 0.85 + 0.15 * t
                    self.eye_height = int(self.eye_size * (0.85 + 0.15 * t))
                    if self.sub_state_timer >= self.look_duration * 2 + self.look_wait_duration:
                        self.sub_state = None
                        self.x_offset = 0
                        self.y_offset = 0
                        self.left_eye_scale = 1.0
                        self.right_eye_scale = 1.0
                        self.squint_scale = 1.0
                        self.eye_height = self.eye_size
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "look_up_right_to_left":
                if self.sub_state_timer <= self.look_duration:
                    t = self.sub_state_timer / self.look_duration
                    self.x_offset = self.diagonal_amplitude * t
                    self.y_offset = -self.diagonal_amplitude * t + self.eye_size * 0.15 / 2
                    self.right_eye_scale = 0.85 + 0.15 * t
                    self.left_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                elif self.sub_state_timer <= self.look_duration + self.look_wait_duration:
                    self.x_offset = self.diagonal_amplitude
                    self.y_offset = -self.diagonal_amplitude + self.eye_size * 0.15 / 2
                    self.right_eye_scale = 1.0
                    self.left_eye_scale = 0.85
                    self.squint_scale = 0.85
                    self.eye_height = int(self.eye_size * 0.85)
                else:
                    t = (self.sub_state_timer - (self.look_duration + self.look_wait_duration)) / self.look_duration
                    self.x_offset = self.diagonal_amplitude * (1 - t)
                    self.y_offset = (-self.diagonal_amplitude + self.eye_size * 0.15 / 2) * (1 - t)
                    self.left_eye_scale = 0.85 + 0.15 * t
                    self.right_eye_scale = 1.0
                    self.squint_scale = 0.85 + 0.15 * t
                    self.eye_height = int(self.eye_size * (0.85 + 0.15 * t))
                    if self.sub_state_timer >= self.look_duration * 2 + self.look_wait_duration:
                        self.sub_state = None
                        self.x_offset = 0
                        self.y_offset = 0
                        self.left_eye_scale = 1.0
                        self.right_eye_scale = 1.0
                        self.squint_scale = 1.0
                        self.eye_height = self.eye_size
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "slam":
                if self.sub_state_timer <= self.slam_duration:
                    t = self.sub_state_timer / self.slam_duration
                    self.y_offset = self.slam_down_offset * t
                    self.eye_height = int(self.eye_size * (1 - 0.9 * t))
                    self.rotation_angle = 0
                    self.right_eye_scale = 1.0
                elif self.sub_state_timer <= self.slam_duration * 2:
                    t = (self.sub_state_timer - self.slam_duration) / self.slam_duration
                    self.y_offset = self.slam_down_offset * (1 - t) + self.slam_up_offset * t
                    self.eye_height = int(self.eye_size * (0.1 * (1 - t) + t))
                    self.rotation_angle = 0
                    self.right_eye_scale = 1.0
                elif self.sub_state_timer <= self.slam_duration * 3:
                    t = (self.sub_state_timer - self.slam_duration * 2) / self.slam_duration
                    self.y_offset = self.slam_up_offset * (1 - t)
                    self.left_y_offset = self.tilt_offset * t
                    self.right_y_offset = -self.tilt_offset * 1.8 * t
                    self.rotation_angle = self.tilt_angle * t
                    self.eye_height = self.eye_size
                    self.right_eye_scale = 1.0 - 0.1 * t
                else:
                    self.y_offset = 0
                    self.left_y_offset = self.tilt_offset
                    self.right_y_offset = -self.tilt_offset * 1.8
                    self.rotation_angle = self.tilt_angle
                    self.eye_height = self.eye_size
                    self.right_eye_scale = 0.9
                    if self.sub_state_timer >= self.slam_duration * 3 + self.slam_wait_duration:
                        self.sub_state = "waiting_after_slam"
                        self.is_slamming = False
                        self.y_offset = 0
                        self.left_y_offset = 0
                        self.right_y_offset = 0
                        self.rotation_angle = 0
                        self.eye_height = self.eye_size
                        self.right_eye_scale = 1.0
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "squint":
                if self.sub_state_timer <= self.squint_duration / 2:
                    t = self.sub_state_timer / (self.squint_duration / 2)
                    self.squint_scale = 1.0 - 0.2 * t
                    self.eye_height = int(self.eye_size * (1.0 - 0.2 * t))
                    self.y_offset = self.eye_size * 0.2 * t / 2
                    self.left_eye_scale = self.squint_scale
                    self.right_eye_scale = self.squint_scale
                else:
                    t = (self.sub_state_timer - (self.squint_duration / 2)) / (self.squint_duration / 2)
                    self.squint_scale = 0.8 + 0.2 * t
                    self.eye_height = int(self.eye_size * (0.8 + 0.2 * t))
                    self.y_offset = self.eye_size * 0.2 * (1 - t) / 2
                    self.left_eye_scale = self.squint_scale
                    self.right_eye_scale = self.squint_scale
                if self.sub_state_timer >= self.squint_duration:
                    self.sub_state = None
                    self.is_squinting = False
                    self.squint_scale = 1.0
                    self.eye_height = self.eye_size
                    self.y_offset = 0
                    self.left_eye_scale = 1.0
                    self.right_eye_scale = 1.0
                    self.is_waiting = True
                    self.sub_state_timer = 0

            elif self.sub_state == "look_left_squint":
                if self.sub_state_timer <= self.look_duration:
                    t = self.sub_state_timer / self.look_duration
                    self.x_offset = -self.look_amplitude * t
                    self.squint_scale = 1.0 - 0.2 * t
                    self.left_eye_scale = self.squint_scale
                    self.right_eye_scale = self.squint_scale
                    self.eye_height = int(self.eye_size * self.squint_scale)
                    self.y_offset = self.eye_size * 0.2 * t / 2
                elif self.sub_state_timer <= self.look_duration + self.look_wait_duration:
                    self.x_offset = -self.look_amplitude
                    self.squint_scale = 0.8
                    self.left_eye_scale = 0.8
                    self.right_eye_scale = 0.8
                    self.eye_height = int(self.eye_size * 0.8)
                    self.y_offset = self.eye_size * 0.2 / 2
                else:
                    t = (self.sub_state_timer - (self.look_duration + self.look_wait_duration)) / self.look_duration
                    self.x_offset = -self.look_amplitude * (1 - t)
                    self.squint_scale = 0.8 + 0.2 * t
                    self.left_eye_scale = self.squint_scale
                    self.right_eye_scale = self.squint_scale
                    self.eye_height = int(self.eye_size * self.squint_scale)
                    self.y_offset = self.eye_size * 0.2 * (1 - t) / 2
                    if self.sub_state_timer >= self.look_duration * 2 + self.look_wait_duration:
                        self.sub_state = None
                        self.x_offset = 0
                        self.squint_scale = 1.0
                        self.left_eye_scale = 1.0
                        self.right_eye_scale = 1.0
                        self.eye_height = self.eye_size
                        self.y_offset = 0
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "look_right_squint":
                if self.sub_state_timer <= self.look_duration:
                    t = self.sub_state_timer / self.look_duration
                    self.x_offset = self.look_amplitude * t
                    self.squint_scale = 1.0 - 0.2 * t
                    self.left_eye_scale = self.squint_scale
                    self.right_eye_scale = self.squint_scale
                    self.eye_height = int(self.eye_size * self.squint_scale)
                    self.y_offset = self.eye_size * 0.2 * t / 2
                elif self.sub_state_timer <= self.look_duration + self.look_wait_duration:
                    self.x_offset = self.look_amplitude
                    self.squint_scale = 0.8
                    self.left_eye_scale = 0.8
                    self.right_eye_scale = 0.8
                    self.eye_height = int(self.eye_size * 0.8)
                    self.y_offset = self.eye_size * 0.2 / 2
                else:
                    t = (self.sub_state_timer - (self.look_duration + self.look_wait_duration)) / self.look_duration
                    self.x_offset = self.look_amplitude * (1 - t)
                    self.squint_scale = 0.8 + 0.2 * t
                    self.left_eye_scale = self.squint_scale
                    self.right_eye_scale = self.squint_scale
                    self.eye_height = int(self.eye_size * self.squint_scale)
                    self.y_offset = self.eye_size * 0.2 * (1 - t) / 2
                    if self.sub_state_timer >= self.look_duration * 2 + self.look_wait_duration:
                        self.sub_state = None
                        self.x_offset = 0
                        self.squint_scale = 1.0
                        self.left_eye_scale = 1.0
                        self.right_eye_scale = 1.0
                        self.eye_height = self.eye_size
                        self.y_offset = 0
                        self.is_waiting = True
                        self.sub_state_timer = 0

            elif self.sub_state == "waiting_after_slam":
                self.y_offset = 0
                self.left_y_offset = 0
                self.right_y_offset = 0
                self.rotation_angle = 0
                self.eye_height = self.eye_size
                self.right_eye_scale = 1.0
                self.left_eye_scale = 1.0
                self.squint_scale = 1.0
                self.is_waiting = True

            if self.is_waiting and self.sub_state is None:
                if self.sub_state_timer >= self.wait_duration:
                    self.sub_state = "idle_bob"
                    self.sub_state_timer = 0
                    self.is_waiting = False

            if self.sub_state == "idle_bob":
                t = self.sub_state_timer / self.bob_period
                self.y_offset = self.bob_amplitude * 0.2 * math.sin(2 * math.pi * t)
                self.x_offset = 0
                self.squint_scale = 1.0
                self.left_eye_scale = 1.0
                self.right_eye_scale = 1.0
                self.eye_height = self.eye_size
                self.left_y_offset = 0
                self.right_y_offset = 0
                self.rotation_angle = 0
                if self.sub_state_timer >= self.bob_duration:
                    self.sub_state = None
                    self.y_offset = 0
                    self.is_waiting = False
                    rand = random.random()
                    if rand < 0.002:
                        self.sub_state = "blink"
                        self.sub_state_timer = 0
                        self.is_blinking = True
                    elif rand < 0.005:
                        self.sub_state = "droop"
                        self.sub_state_timer = 0
                        self.is_drooping = True
                    elif rand < 0.008:
                        self.sub_state = "look_left"
                        self.sub_state_timer = 0
                    elif rand < 0.011:
                        self.sub_state = "look_right"
                        self.sub_state_timer = 0
                    elif rand < 0.014:
                        self.sub_state = "squint"
                        self.sub_state_timer = 0
                        self.is_squinting = True
                    elif rand < 0.017:
                        self.sub_state = "look_up_left_to_right"
                        self.sub_state_timer = 0
                    elif rand < 0.020:
                        self.sub_state = "look_up_right_to_left"
                        self.sub_state_timer = 0
                    elif rand < 0.023:
                        self.sub_state = "look_left_squint"
                        self.sub_state_timer = 0
                    elif rand < 0.026:
                        self.sub_state = "look_right_squint"
                        self.sub_state_timer = 0

            if self.state_timer >= self.awake_duration:
                self.state = "sleeping"
                self.state_timer = 0
                self.sub_state = None
                self.sub_state_timer = 0
                self.is_waiting = False
                self.noise_y = 0

    def draw(self):
        for bubble in self.bubbles:
            pygame.draw.circle(self.screen, (*self.color, 100), 
                             (int(bubble['x']), int(bubble['y'])), 
                             int(bubble['radius']))

        left_eye_size = int(self.eye_size * self.left_eye_scale)
        left_eye_height = int(self.eye_height * self.left_eye_scale)
        left_eye_spacing = int(self.eye_spacing * self.left_eye_scale)
        left_eye_radius = int(self.eye_radius * self.left_eye_scale)

        right_eye_size = int(self.eye_size * self.right_eye_scale)
        right_eye_height = int(self.eye_height * self.right_eye_scale)
        right_eye_spacing = int(self.eye_spacing * self.right_eye_scale)
        right_eye_radius = int(self.eye_radius * self.right_eye_scale)

        left_eye_x = self.center_x - left_eye_size - left_eye_spacing // 2 + self.x_offset
        left_eye_y = self.center_y - left_eye_height // 2 + self.y_offset + self.left_y_offset
        right_eye_x = self.center_x + right_eye_spacing // 2 + self.x_offset
        right_eye_y = self.center_y - right_eye_height // 2 + self.y_offset + self.right_y_offset

        left_eye_surface = pygame.Surface((left_eye_size * 2, left_eye_height * 2), pygame.SRCALPHA)
        left_eye_rect = pygame.Rect(left_eye_size // 2, left_eye_height // 2, left_eye_size, left_eye_height)
        pygame.draw.rect(left_eye_surface, self.color, left_eye_rect, border_radius=left_eye_radius)
        left_eye_rotated = pygame.transform.rotate(left_eye_surface, self.rotation_angle)
        left_eye_rotated_rect = left_eye_rotated.get_rect(center=(left_eye_x + left_eye_size // 2, left_eye_y + left_eye_height // 2))
        self.screen.blit(left_eye_rotated, left_eye_rotated_rect)

        right_eye_surface = pygame.Surface((right_eye_size * 2, right_eye_height * 2), pygame.SRCALPHA)
        right_eye_rect = pygame.Rect(right_eye_size // 2, right_eye_height // 2, right_eye_size, right_eye_height)
        pygame.draw.rect(right_eye_surface, self.color, right_eye_rect, border_radius=right_eye_radius)
        right_eye_rotated = pygame.transform.rotate(right_eye_surface, self.rotation_angle)
        right_eye_rotated_rect = right_eye_rotated.get_rect(center=(right_eye_x + right_eye_size // 2, right_eye_y + right_eye_height // 2))
        self.screen.blit(right_eye_rotated, right_eye_rotated_rect)

        if self.state == "looking_around":
            noise_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            y = int(self.noise_y)
            pygame.draw.line(noise_surface, (255, 255, 255, 100), (0, y), (self.screen.get_width(), y), 2)
            self.screen.blit(noise_surface, (0, 0))
