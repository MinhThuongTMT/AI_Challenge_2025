# main.py
import pygame
import socket
import threading
import queue
import time  # Chỉ nhập module time
from idle import IdleFace
from happy import HappyFace
from listening import ListeningDots
import sys
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/Map')
from findbot_main import open_gui_and_route_to_shelf, FinalSupermarketFindBot

# Khởi tạo Pygame
pygame.init()
clock = pygame.time.Clock()

# Định nghĩa kích thước màn hình
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Khởi tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DARK_GRAY = (30, 30, 30)
BLACK = (0, 0, 0)

class RobotManager:
    def __init__(self, screen):
        self.screen = screen
        self.states = {
            'idle': IdleFace(screen),
            'happy': HappyFace(screen),
            'listening': ListeningDots(screen)
        }
        self.current_state_name = 'idle'
        self.current_animation = self.states[self.current_state_name]
        self.last_interaction_time = pygame.time.get_ticks()
        self.timeout_duration = 15000
        self.waiting_after_slam = False
        self.command_queue = queue.Queue(maxsize=2)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(1)
        self.running = True
        self.thread = threading.Thread(target=self.handle_commands)
        self.thread.daemon = True
        self.thread.start()
        self.is_routing = False
        self.bot = None
        self.dt = 0

    def _reset_main_display(self):
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = screen
        for st in self.states.values():
            if hasattr(st, 'screen'):
                st.screen = screen
        self.bot = None
        self.is_routing = False

    def run_route_to_shelf(self, target_desc: str, screen=None, clock=None):
        self.is_routing = True
        print(f"Running route to shelf: {target_desc}")
        try:
            self.bot = open_gui_and_route_to_shelf(target_desc, screen or self.screen, clock or pygame.time.Clock())
            txt = self.bot.last_route_text
            if txt:
                print(f"Route text: {txt}")
        except Exception as e:
            print(f"Route error: {e}")
            self.bot = None
            self.is_routing = False

    def handle_commands(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                data = client_socket.recv(1024).decode().strip()
                if data:
                    print(f"Received command from {addr}: {data}")
                    self.command_queue.put(data)
                client_socket.close()
            except Exception as e:
                print(f"Socket error: {e}")

    def process_commands(self):
        try:
            while not self.command_queue.empty():
                print("Bắt đầu xử lý hàng đợi")
                command = self.command_queue.get()
                print(f"Processing command: {command}")
                if command in self.states:
                    self.set_state(command)
                    self.waiting_after_slam = False
                    self.is_routing = False
                    self.bot = None
                elif command == "starthello":
                    if self.current_state_name != 'idle':
                        self.set_state('idle')
                    if isinstance(self.current_animation, IdleFace):
                        print("Triggering slam action")
                        self.current_animation.slam()
                        self.waiting_after_slam = True
                        self.last_interaction_time = pygame.time.get_ticks()
                    self.is_routing = False
                    self.bot = None
                elif command == "listen":
                    self.set_state('listening')
                    self.waiting_after_slam = False
                    self.is_routing = False
                    self.bot = None
                elif command == "startconfirm":
                    self.set_state('happy')
                    self.current_animation.is_bobbing = True
                    self.current_animation.is_folded = False
                    self.current_animation.is_winking = False
                    self.current_animation.is_closing = False
                    self.current_animation.close_timer = 0
                    self.waiting_after_slam = False
                    self.is_routing = False
                    self.bot = None
                elif command == "confirmyes" and self.current_state_name == 'happy':
                    self.current_animation.is_winking = True
                    self.current_animation.wink_timer = 0
                    self.current_animation.is_folded = False
                    self.current_animation.is_closing = False
                    self.last_interaction_time = pygame.time.get_ticks()
                    self.waiting_after_slam = False
                    self.is_routing = False
                    self.bot = None
                elif command == "confirmno":
                    self.set_state('happy')
                    self.current_animation.is_bobbing = True
                    self.current_animation.is_folded = False
                    self.current_animation.is_winking = False
                    self.current_animation.is_closing = False
                    self.current_animation.close_timer = 0
                    self.waiting_after_slam = False
                    self.is_routing = False
                    self.bot = None
                elif command == "smile":
                    self.set_state('happy')
                    self.current_animation.is_folded = True
                    self.current_animation.is_bobbing = True
                    self.current_animation.is_winking = False
                    self.current_animation.is_closing = False
                    self.current_animation.close_timer = 0
                    self.waiting_after_slam = False
                    self.is_routing = False
                    self.bot = None
                else:
                    self.run_route_to_shelf(command, screen=self.screen, clock=clock)
                self.command_queue.task_done()
        except queue.Empty:
            pass

    def set_state(self, new_state):
        if new_state in self.states:
            self.current_state_name = new_state
            self.current_animation = self.states[new_state]
            self.last_interaction_time = pygame.time.get_ticks()
            self.is_routing = False
            self.bot = None

    def update(self):
        if self.is_routing and self.bot:
            self.bot.update_routing(self.dt)
            print(f"Updating routing with dt: {self.dt:.4f}")
        else:
            if not self.waiting_after_slam and self.current_state_name not in ['idle'] and \
               pygame.time.get_ticks() - self.last_interaction_time > self.timeout_duration:
                self.set_state('idle')
            self.current_animation.update()
        self.process_commands()

    def draw(self):
        self.screen.fill(BLACK)  # Xóa màn hình trước khi vẽ
        if self.is_routing and self.bot:
            self.bot.draw_board()
            self.bot.draw_products()
            self.bot.draw_entrance()
            self.bot.draw_path()  # Vẽ draw_path sau cùng để tránh bị ghi đè
            self.bot.draw_user()
        else:
            self.current_animation.draw()

    def stop(self):
        self.running = False
        self.server_socket.close()
        self.command_queue.join()

def main():
    robot_manager = RobotManager(screen)
    running = True
    last_time = time.time()

    while running:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if robot_manager.is_routing:
                    robot_manager.is_routing = False
                    robot_manager.bot = None
                    robot_manager._reset_main_display()
                    print("Quay lại giao diện chính")
                else:
                    running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not robot_manager.is_routing:
                robot_manager.set_state('happy')
                robot_manager.current_animation.is_bobbing = True
                robot_manager.current_animation.is_folded = False
                robot_manager.current_animation.is_winking = False
                robot_manager.current_animation.is_closing = False
                robot_manager.current_animation.close_timer = 0
                print("Chuyển sang trạng thái Vui Vẻ")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and not robot_manager.is_routing:
                robot_manager.set_state('listening')
                print("Chuyển sang trạng thái Lắng Nghe")
            if event.type == pygame.KEYDOWN and robot_manager.is_routing and robot_manager.bot:
                key_name = pygame.key.name(event.key)
                robot_manager.bot.handle_keyboard_input(key_name)

        robot_manager.dt = dt
        robot_manager.update()
        robot_manager.draw()
        pygame.display.flip()  # Đảm bảo làm mới màn hình
        clock.tick(60)

    robot_manager.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
