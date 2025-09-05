import sys
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/animations')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/Manager')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/audio_manager')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/Uart_manager')


import pygame
from happy import draw_happy_face_offset, draw_happy_face_blink, screen
from sleep import draw_sleeping_face
from wakeup import draw_wakeup_face
from listening import draw_listening_dots
from thanks import draw_thanks_face

pygame.init()
clock = pygame.time.Clock()

# Màu nền
DEL_SCREEN = (30, 30, 30)

# ================================
# Trạng thái & thời gian mỗi trạng thái (tính bằng frame)
states = ['happy', 'sleeping', 'wakeup', 'listening', 'thanks']
durations = {
    'happy': 600,       # 10s
    'sleeping': 300,    # 5s
    'wakeup': 60,       # khoảng 1s
    'listening': 300,   # 5s
    'thanks': 300       # 5s
}

# Animation cho trạng thái "happy"
happy_steps = [
    {'start': (0, 0), 'end': (-140, -100), 'pause_after': 60, 'blink': False},
    {'start': (-140, -100), 'end': (0, 0), 'pause_after': 60, 'blink': True},
    {'start': (0, 0), 'end': (-140, 100), 'pause_after': 60, 'blink': False},
    {'start': (-140, 100), 'end': (0, 0), 'pause_after': 60, 'blink': True},
]
happy_duration = 30
happy_step = 0
happy_frame_in_step = 0
happy_state = 'moving'

# ================================
# Điều khiển luồng chính
frame = 0
state_index = 0
current_state = states[state_index]
state_timer = 0
running = True

while running:
    screen.fill(DEL_SCREEN)

    if current_state == 'happy':
        step = happy_steps[happy_step]
        start = step['start']
        end = step['end']
        pause_time = step['pause_after']

        if happy_state == 'moving':
            t = min(happy_frame_in_step / happy_duration, 1.0)
            x = int(start[0] + (end[0] - start[0]) * t)
            y = int(start[1] + (end[1] - start[1]) * t)
            draw_happy_face_offset(x, y)

            if happy_frame_in_step >= happy_duration:
                happy_frame_in_step = 0
                happy_state = "pause"
            else:
                happy_frame_in_step += 1

        elif happy_state == 'pause':
            blink_frames = {
                26: 400,
                27: 200,
                28: 100,
                29: 40,
                30: 100,
                31: 200,
                32: 400
            }

            if step['blink'] and happy_frame_in_step in blink_frames:
                draw_happy_face_blink(end[0], end[1], blink_frames[happy_frame_in_step])
            else:
                draw_happy_face_offset(end[0], end[1])

            if happy_frame_in_step >= pause_time:
                happy_step = (happy_step + 1) % len(happy_steps)
                happy_frame_in_step = 0
                happy_state = "moving"
            else:
                happy_frame_in_step += 1

    elif current_state == 'sleeping':
        z_offset = (frame % 120)
        draw_sleeping_face(z_offset)

    elif current_state == 'wakeup':
        draw_wakeup_face(state_timer)

    elif current_state == 'listening':
        draw_listening_dots(frame)

    elif current_state == 'thanks':
        draw_thanks_face(frame)

    # =====================================
    # Chuyển sang trạng thái tiếp theo nếu đủ thời gian
    state_timer += 1
    if state_timer >= durations[current_state]:
        state_index = (state_index + 1) % len(states)
        current_state = states[state_index]
        state_timer = 0

        # Reset thông số cho "happy"
        if current_state == 'happy':
            happy_step = 0
            happy_frame_in_step = 0
            happy_state = 'moving'

    # =====================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    pygame.display.flip()
    frame += 1
    clock.tick(60)

pygame.quit()

