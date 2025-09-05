# findbot_main.py
import pygame
import math
import time
import os
from supermarket_board import supermarket_layout, PRODUCT_CATEGORIES, get_category_by_key, get_shelf_center
from enhanced_pathfinding import EnhancedPathFinder

# Constants
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)  # Đổi YELLOW thành CYAN để dễ quan sát
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Meters per grid cell for text route generation
METERS_PER_CELL = 1.0

class FinalSupermarketFindBot:
    def __init__(self, screen=None, clock=None):
        self.show_grid = False
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 22)
        self.font_large = pygame.font.Font(None, 28)
        self.font_title = pygame.font.Font(None, 36)
        
        self.layout = supermarket_layout
        self.pathfinder = EnhancedPathFinder(self.layout)
        
        self.shelf_sprite_raw = None
        self._shelf_sprite_cache = {}
        self._sprite_raw_cache = {}
        self.default_sprite_name = 'shelf2_2.png'
        base_dir = os.path.dirname(__file__)
        self.base_dir = base_dir
        self.shelf_image_dirs = [
            os.path.join(base_dir, 'shelfpicture'),
            os.path.join(base_dir, 'assets', 'shelves'),
            base_dir,
        ]
        try:
            sprite_path = os.path.join(base_dir, self.default_sprite_name)
            self.shelf_sprite_raw = pygame.image.load(sprite_path).convert_alpha()
            self._sprite_raw_cache[self.default_sprite_name] = self.shelf_sprite_raw
        except Exception as e:
            print(f"Không thể load sprite kệ: {e}")
            self.shelf_sprite_raw = None
        
        self.shelf_extra_w_cells = 2
        self.shelf_extra_h_cells = 1
        
        self.entrances = [(r, c) for r, row in enumerate(self.layout) for c, val in enumerate(row) if val == 9]
        if self.entrances:
            bottom_row = max(r for r, _ in self.entrances)
            bottom_cells = [pos for pos in self.entrances if pos[0] == bottom_row]
            self.user_pos = min(bottom_cells, key=lambda rc: rc[1])
        else:
            self.user_pos = (0, 0)
        self.target_product = None
        self.current_path = []
        self.path_index = 0
        self.selected_category = None
        self.show_help = True
        self.animation_time = 0
        self.path_animation_index = 0
        self.total_searches = 0
        self.total_distance = 0
        self.last_direction = (0, 0)
        self.last_route_text = ""
        
        self.cell_to_desc = {}
        for _cat, _info in PRODUCT_CATEGORIES.items():
            desc = str(_info.get('description') or '').strip()
            if not desc:
                sid = _info.get('shelf_id')
                desc = str(sid) if sid is not None else ''
            for rc in _info.get('positions', []) or []:
                try:
                    r, c = rc
                    self.cell_to_desc[(int(r), int(c))] = desc
                except Exception:
                    continue
        
        if screen is None:
            self.screen = pygame.display.get_surface()
            if self.screen is None:
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        else:
            self.screen = screen
        print(f"Bot screen: {self.screen}, Size: {self.screen.get_size()}")
        self.clock = clock or pygame.time.Clock()

    def run(self):
        """Main game loop - Không sử dụng vì tích hợp với main.py"""
        pass

    def draw_board(self):
        """Draw the supermarket layout with dark walkways/background"""
        board_width = WIDTH
        board_height = HEIGHT
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                x = j * cell_width
                y = i * cell_height
                cell = self.layout[i][j]
                
                if cell == 0:  # Walkway - DARK_GRAY thay vì WHITE
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, cell_width, cell_height))
                elif cell == 1:  # Product shelf base - DARK_GRAY
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, cell_width, cell_height))
                elif cell == 2:  # Special product
                    pygame.draw.rect(self.screen, PURPLE, (x, y, cell_width, cell_height))
                elif cell == 9:  # Entrance/Exit
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, cell_width, cell_height))
                elif cell >= 3:  # Walls
                    pygame.draw.rect(self.screen, BLACK, (x, y, cell_width, cell_height))
        
        if self.show_grid:
            rows = len(self.layout)
            cols = len(self.layout[0])
            for i in range(rows + 1):
                y = i * cell_height
                pygame.draw.line(self.screen, GRAY, (0, y), (board_width, y), 1)
            for j in range(cols + 1):
                x = j * cell_width
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, board_height), 1)

    def _get_scaled_shelf_sprite(self, width_px, height_px):
        if not self.shelf_sprite_raw:
            return None
        key = (width_px, height_px)
        sprite = self._shelf_sprite_cache.get(key)
        if sprite is None:
            try:
                sprite = pygame.transform.scale(self.shelf_sprite_raw, key)
                self._shelf_sprite_cache[key] = sprite
            except Exception as e:
                print(f"Lỗi scale sprite: {e}")
                return None
        return sprite

    def _load_sprite_raw_by_name(self, name):
        surf = self._sprite_raw_cache.get(name)
        if surf is not None:
            return surf
        dirs = getattr(self, 'shelf_image_dirs', None)
        if not dirs:
            base_dir = os.path.dirname(__file__)
            dirs = [
                os.path.join(base_dir, 'shelfpicture'),
                os.path.join(base_dir, 'assets', 'shelves'),
                base_dir,
            ]
        for d in dirs:
            p = os.path.join(d, name)
            try:
                if os.path.isfile(p):
                    surf = pygame.image.load(p).convert_alpha()
                    self._sprite_raw_cache[name] = surf
                    return surf
            except Exception:
                continue
        self._sprite_raw_cache[name] = None
        return None

    def _get_scaled_sprite(self, name, width_px, height_px):
        raw = self._load_sprite_raw_by_name(name)
        if raw is None:
            raw = self._load_sprite_raw_by_name(self.default_sprite_name) or self.shelf_sprite_raw
            if raw is None:
                return None
            name = self.default_sprite_name
        key = (name, width_px, height_px)
        sprite = self._shelf_sprite_cache.get(key)
        if sprite is None:
            try:
                sprite = pygame.transform.scale(raw, (width_px, height_px))
                self._shelf_sprite_cache[key] = sprite
            except Exception as e:
                print(f"Lỗi scale sprite '{name}': {e}")
                return None
        return sprite

    def _get_scaled_sprite_with_candidates(self, names, width_px, height_px):
        for n in names:
            sp = self._get_scaled_sprite(n, width_px, height_px)
            if sp is not None and n != self.default_sprite_name:
                return sp
        return self._get_scaled_sprite(self.default_sprite_name, width_px, height_px)

    def draw_products(self):
        """Gộp các mục có description cùng số thành kệ đôi lưng"""
        board_width = WIDTH
        board_height = HEIGHT
        rows = len(self.layout)
        cols = len(self.layout[0]) if rows else 0
        if rows == 0 or cols == 0:
            return
        cell_w = board_width // cols
        cell_h = board_height // rows

        shelves_by_id = {}
        for cat, info in PRODUCT_CATEGORIES.items():
            sid = info.get('shelf_id')
            if sid is None:
                continue
            entry = shelves_by_id.setdefault(sid, {'positions': [], 'color': info.get('color', (200, 200, 200))})
            entry['positions'].extend(info.get('positions', []))
        desc_by_sid = {}
        for cat, info in PRODUCT_CATEGORIES.items():
            sid = info.get('shelf_id')
            if sid is None:
                continue
            if sid not in desc_by_sid:
                d = info.get('description')
                desc_by_sid[sid] = str(d).strip().upper() if d is not None else ''

        groups = {}
        for cat, info in PRODUCT_CATEGORIES.items():
            desc = info.get('description')
            if not desc:
                continue
            d = str(desc).strip().upper()
            if len(d) >= 2 and d[-1] in ('A', 'B') and d[:-1].isdigit():
                num = int(d[:-1])
                letter = d[-1]
                grp = groups.setdefault(num, {'A': set(), 'B': set()})
                for rc in info.get('positions', []):
                    grp[letter].add(tuple(rc))

        covered = set()
        for num in sorted(groups.keys()):
            posA = groups[num]['A']
            posB = groups[num]['B']
            if not posA or not posB:
                continue
            rowsA = {r for (r, _) in posA}
            rowsB = {r for (r, _) in posB}
            rAmax = max(rowsA)
            rBmin = min(rowsB)
            if rAmax + 1 != rBmin:
                continue
            colsA_bottom = {c for (r, c) in posA if r == rAmax}
            colsB_top = {c for (r, c) in posB if r == rBmin}
            union_cols = sorted(colsA_bottom | colsB_top)
            if not union_cols:
                continue
            segments = []
            start = None
            prev = None
            for c in union_cols:
                if start is None:
                    start = prev = c
                elif c == prev + 1:
                    prev = c
                else:
                    segments.append((start, prev))
                    start = prev = c
            if start is not None:
                segments.append((start, prev))
            all_rows = rowsA | rowsB
            min_r_all = min(all_rows)
            max_r_all = max(all_rows)
            height_cells_all = max_r_all - min_r_all + 1
            for c1, c2 in segments:
                width_cells = c2 - c1 + 1
                total_w_cells = width_cells + getattr(self, 'shelf_extra_w_cells', 0)
                total_h_cells = height_cells_all + getattr(self, 'shelf_extra_h_cells', 0)
                sprite = self._get_scaled_sprite_with_candidates([f"shelf_{num}.png"], total_w_cells * cell_w, total_h_cells * cell_h)
                if sprite:
                    base_x = c1 * cell_w
                    base_y = min_r_all * cell_h
                    offset_x = - (getattr(self, 'shelf_extra_w_cells', 0) // 2) * cell_w
                    offset_y = - int((getattr(self, 'shelf_extra_h_cells', 0) / 2.0) * cell_h)
                    x = base_x + offset_x
                    y = base_y + offset_y
                    self.screen.blit(sprite, (x, y))
                    for (rr, cc) in posA | posB:
                        if c1 <= cc <= c2:
                            covered.add((rr, cc))
        paired_nums = {num for num, ab in groups.items() if ab['A'] and ab['B']}
        for sid, info in shelves_by_id.items():
            positions = [tuple(rc) for rc in info['positions']]
            if not positions:
                continue
            desc = desc_by_sid.get(sid, '')
            d = desc.strip().upper()
            is_AB = (len(d) >= 2 and d[-1] in ('A', 'B') and d[:-1].isdigit())
            is_in_paired_group = False
            if is_AB:
                try:
                    num = int(d[:-1])
                    is_in_paired_group = num in paired_nums
                except:
                    is_in_paired_group = False
            if is_in_paired_group:
                continue
            rs = [r for (r, _) in positions]
            cs = [c for (_, c) in positions]
            min_r, max_r = min(rs), max(rs)
            min_c, max_c = min(cs), max(cs)
            width_cells = max_c - min_c + 1
            height_cells = max_r - min_r + 1
            total_w_cells = width_cells + getattr(self, 'shelf_extra_w_cells', 0)
            total_h_cells = height_cells + getattr(self, 'shelf_extra_h_cells', 0)
            candidates = []
            if is_AB:
                candidates.append(f"shelf_{d}.png")
                try:
                    candidates.append(f"shelf_{int(d[:-1])}.png")
                except:
                    pass
            else:
                if d.isdigit():
                    candidates.append(f"shelf_{d}.png")
            candidates.append(f"shelf_{sid}.png")
            sprite = self._get_scaled_sprite_with_candidates(candidates, total_w_cells * cell_w, total_h_cells * cell_h)
            if sprite:
                base_x = min_c * cell_w
                base_y = min_r * cell_h
                offset_x = - (getattr(self, 'shelf_extra_w_cells', 0) // 2) * cell_w
                offset_y = - int((getattr(self, 'shelf_extra_h_cells', 0) / 2.0) * cell_h)
                x = base_x + offset_x
                y = base_y + offset_y
                self.screen.blit(sprite, (x, y))
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        covered.add((r, c))
            for sid, info in shelves_by_id.items():
                color = info['color']
                for (r, c) in info['positions']:
                    if 0 <= r < rows and 0 <= c < cols and (r, c) not in covered:
                        x = c * cell_w
                        y = r * cell_h
                        pygame.draw.rect(self.screen, color, (x, y, cell_w, cell_h))
                        shine = tuple(min(255, ch + 30) for ch in color)
                        pygame.draw.rect(self.screen, shine, (x, y, cell_w, 2))
            for sid, info in shelves_by_id.items():
                positions = info['positions']
                if not positions:
                    continue
                rs = [r for (r, _) in positions]
                cs = [c for (_, c) in positions]
                min_r, max_r = min(rs), max(rs)
                min_c, max_c = min(cs), max(cs)
                center_x = (min_c + max_c + 1) // 2 * cell_w
                center_y = (min_r + max_r + 1) // 2 * cell_h
                text = self.font_small.render(str(sid), True, WHITE)
                text_rect = text.get_rect(center=(center_x, center_y))
                bg_rect = pygame.Rect(text_rect.x - 2, text_rect.y - 1, text_rect.width + 4, text_rect.height + 2)
                pygame.draw.rect(self.screen, BLACK, bg_rect)
                self.screen.blit(text, text_rect)

    def draw_user(self):
        board_width = WIDTH
        board_height = HEIGHT
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        x = self.user_pos[1] * cell_width + cell_width // 2
        y = self.user_pos[0] * cell_height + cell_height // 2
        pulse = math.sin(self.animation_time * 5) * 2
        radius = 8 + pulse
        pygame.draw.circle(self.screen, DARK_GRAY, (x + 2, y + 2), int(radius))
        pygame.draw.circle(self.screen, RED, (x, y), int(radius))
        pygame.draw.circle(self.screen, WHITE, (x, y), int(radius), 2)
        fb_text = self.font_small.render("FB", True, WHITE)
        fb_rect = fb_text.get_rect(center=(x, y))
        self.screen.blit(fb_text, fb_rect)
        if hasattr(self, 'last_direction') and self.last_direction != (0, 0):
            dx, dy = self.last_direction
            end_x = x + dx * 12
            end_y = y + dy * 12
            pygame.draw.line(self.screen, WHITE, (x, y), (end_x, end_y), 3)

    def draw_path(self):
        if not self.current_path:
            print("No path to draw")
            return
        board_width = WIDTH
        board_height = HEIGHT
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        print(f"Grid size: {len(self.layout)}x{len(self.layout[0])}, Cell size: {cell_width}x{cell_height}")
        print(f"Drawing path with {len(self.current_path)} points: {self.current_path}")
        visible_path_length = len(self.current_path)  # Tạm bỏ animation để vẽ ngay
        print(f"Visible path length: {visible_path_length}, Animation index: {self.path_animation_index:.2f}")
        points = []
        for i in range(visible_path_length):
            if i >= len(self.current_path):
                print(f"Index {i} out of range for current_path")
                break
            row, col = self.current_path[i]
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2
            if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
                print(f"Invalid pixel coordinates: ({x}, {y}) for path point ({row}, {col})")
            points.append((x, y))
        if len(points) > 1:
            for i in range(len(points) - 1):
                pygame.draw.line(self.screen, CYAN, points[i], points[i + 1], 8)
                print(f"Drawing line from {points[i]} to {points[i + 1]}")
        for i, point in enumerate(points):
            if i < visible_path_length - 1:
                pulse = math.sin(self.animation_time * 3 + i * 0.5) * 2
                radius = 5 + pulse
                pygame.draw.circle(self.screen, CYAN, point, int(radius))
        if self.current_path and visible_path_length == len(self.current_path):
            target_row, target_col = self.current_path[-1]
            x = target_col * cell_width + cell_width // 2
            y = target_row * cell_height + cell_height // 2
            pulse = math.sin(self.animation_time * 4) * 4
            radius = 15 + pulse
            pygame.draw.circle(self.screen, GREEN, (x, y), int(radius))
            pygame.draw.circle(self.screen, WHITE, (x, y), int(radius), 3)
            pygame.draw.line(self.screen, WHITE, (x - 10, y), (x + 10, y), 3)
            pygame.draw.line(self.screen, WHITE, (x, y - 10), (x, y + 10), 3)
            print(f"Drawing target at ({x}, {y})")

    def draw_entrance(self):
        board_width = WIDTH
        board_height = HEIGHT
        cell_width = board_width // len(self.layout[0])
        cell_height = board_height // len(self.layout)
        if not hasattr(self, 'entrances') or not self.entrances:
            return
        bottom_row = max(r for r, _ in self.entrances)
        cols = [c for r, c in self.entrances if r == bottom_row]
        if not cols:
            return
        left_c, right_c = min(cols), max(cols)
        entrance_center_x = int((left_c * cell_width + cell_width // 2 + right_c * cell_width + cell_width // 2) / 2)
        entrance_y = bottom_row * cell_height + cell_height // 2
        entrance_text = self.font_medium.render("LỐI VÀO", True, WHITE)
        entrance_rect = entrance_text.get_rect(center=(entrance_center_x, entrance_y))
        bg_rect = pygame.Rect(entrance_rect.x - 6, entrance_rect.y - 4, entrance_rect.width + 12, entrance_rect.height + 8)
        pygame.draw.rect(self.screen, BLACK, bg_rect)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        self.screen.blit(entrance_text, entrance_rect)

    def handle_keyboard_input(self, key):
        category = get_category_by_key(key)
        if category:
            self.selected_category = category
            self.find_path_to_product(category)
            return True
        elif key in ['w', 'up']:
            self.move_user('up')
        elif key in ['s', 'down']:
            self.move_user('down')
        elif key in ['a', 'left']:
            self.move_user('left')
        elif key in ['d', 'right']:
            self.move_user('right')
        elif key == 'm':
            print(f"Âm thanh: {'Bật' if sound_status else 'Tắt'}")
        elif key == 'g':
            self.show_grid = not getattr(self, 'show_grid', False)
            print(f"Lưới: {'Bật' if self.show_grid else 'Tắt'}")
        elif key == 'escape':
            self.selected_category = None
            self.current_path = []
            self.path_animation_index = 0
        return False

    def move_user(self, direction):
        """Move user in the specified direction"""
        # Implement move_user logic if needed
        pass

    def find_path_to_product(self, category):
        if category not in PRODUCT_CATEGORIES:
            return
        info = PRODUCT_CATEGORIES[category]
        product_positions = info['positions']
        result = self.pathfinder.find_nearest_shelf_access(self.user_pos, product_positions)
        if result:
            target_pos, path, distance = result
            self.current_path = path
            self.path_animation_index = 0
            self.total_searches += 1
            self.total_distance += distance
            print(f"Tìm thấy đường đến Kệ {info['shelf_id']} - {info['name']} - Khoảng cách: {distance:.1f} bước")
            self.last_route_text = self.build_text_route()
            print(f"Chỉ đường: {self.last_route_text}")
            try:
                route_path = os.path.join(self.base_dir, 'route.txt')
                saved = self.save_text_route(route_path)
                if os.path.isfile(route_path):
                    print(f"Đã ghi chỉ đường vào: {route_path}")
                else:
                    print(saved)
            except Exception as e:
                print(f"Không thể ghi file chỉ đường: {e}")
        else:
            self.current_path = []
            print(f"Không tìm thấy đường đến Kệ {info['shelf_id']} - {info['name']}")

    def generate_directions(self):
        if not self.current_path or len(self.current_path) < 2:
            return ["Đã đến nơi!!!"]
        directions = []
        path_directions = []
        for i in range(len(self.current_path) - 1):
            current_pos = self.current_path[i]
            next_pos = self.current_path[i + 1]
            dr = next_pos[0] - current_pos[0]
            dc = next_pos[1] - current_pos[1]
            if dr == 0 and dc == 1:
                path_directions.append("PHẢI")
            elif dr == 0 and dc == -1:
                path_directions.append("TRÁI")
            elif dr == 1 and dc == 0:
                path_directions.append("XUỐNG")
            elif dr == -1 and dc == 0:
                path_directions.append("LÊN")
        if not path_directions:
            return ["Đã đến nơi!!!"]
        i = 0
        while i < len(path_directions):
            current_dir = path_directions[i]
            count = 1
            while i + count < len(path_directions) and path_directions[i + count] == current_dir:
                count += 1
            if i == 0:
                if current_dir == "LÊN":
                    directions.append(f"Đi thẳng {count} bước")
                elif current_dir == "XUỐNG":
                    directions.append(f"Đi thẳng {count} bước")
                elif current_dir == "TRÁI":
                    directions.append(f"Rẽ trái {count} bước")
                elif current_dir == "PHẢI":
                    directions.append(f"Rẽ phải {count} bước")
            else:
                prev_dir = path_directions[i - 1]
                if current_dir != prev_dir:
                    if current_dir == "TRÁI":
                        directions.append(f"Rẽ trái {count} bước")
                    elif current_dir == "PHẢI":
                        directions.append(f"Rẽ phải {count} bước")
                    elif current_dir == "LÊN":
                        directions.append(f"Đi lên {count} bước")
                    elif current_dir == "XUỐNG":
                        directions.append(f"Đi xuống {count} bước")
                else:
                    directions.append(f"Đi thẳng {count} bước")
            i += count
        directions.append("Đã đến nơi!!!")
        return directions

    def _is_ab_desc(self, desc: str) -> bool:
        d = (desc or '').strip().upper()
        return len(d) >= 2 and d[-1] in ('A', 'B') and d[:-1].isdigit()

    def _neighbors4(self, r, c):
        return [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]

    def _find_adjacent_shelf_desc(self, r: int, c: int) -> str | None:
        best_any = None
        for nr, nc in self._neighbors4(r, c):
            if 0 <= nr < len(self.layout) and 0 <= nc < len(self.layout[0]):
                desc = self.cell_to_desc.get((nr, nc))
                if desc:
                    if self._is_ab_desc(desc):
                        return desc
                    if best_any is None:
                        best_any = desc
        return best_any

    def _segments_from_path(self, path):
        if not path or len(path) < 2:
            return []
        segs = []
        i = 0
        r0, c0 = path[0]
        r1, c1 = path[1]
        cur = (r1 - r0, c1 - c0)
        length = 1
        start_idx = 0
        for k in range(1, len(path) - 1):
            ra, ca = path[k]
            rb, cb = path[k + 1]
            d = (rb - ra, cb - ca)
            if d == cur:
                length += 1
            else:
                segs.append((cur, length, start_idx, k))
                cur = d
                length = 1
                start_idx = k
        segs.append((cur, length, start_idx, len(path) - 1))
        return segs

    def _turn_text(self, prev_dir, next_dir) -> str:
        mapping = {
            ((-1, 0), (0, 1)): 'rẽ phải',
            ((-1, 0), (0, -1)): 'rẽ trái',
            ((0, 1), (1, 0)): 'rẽ phải',
            ((0, 1), (-1, 0)): 'rẽ trái',
            ((1, 0), (0, -1)): 'rẽ phải',
            ((1, 0), (0, 1)): 'rẽ trái',
            ((0, -1), (-1, 0)): 'rẽ phải',
            ((0, -1), (1, 0)): 'rẽ trái',
        }
        return mapping.get((prev_dir, next_dir), 'rẽ')

    def build_text_route(self, meters_per_cell: float | None = None) -> str:
        path = self.current_path
        if not path or len(path) < 2:
            return "Bạn đang ở vị trí đích"
        mpc = meters_per_cell if meters_per_cell is not None else METERS_PER_CELL
        segs = self._segments_from_path(path)
        if not segs:
            return "Bạn đang ở vị trí đích"
        parts = []
        dvec, steps, s_idx, e_idx = segs[0]
        dist_m = int(round(steps * mpc))
        if dist_m > 0:
            parts.append(f"Đi thẳng {dist_m} mét")
        for i in range(1, len(segs)):
            prev_vec, _, _, prev_end = segs[i - 1]
            dvec, steps, s_idx, e_idx = segs[i]
            turn = self._turn_text(prev_vec, dvec)
            tr, tc = path[s_idx]
            desc = self._find_adjacent_shelf_desc(tr, tc)
            if desc:
                parts.append(f"{turn} tại kệ {desc}")
            else:
                parts.append(f"{turn}")
            dist_m = int(round(steps * mpc))
            if dist_m > 0:
                parts.append(f"đi thẳng {dist_m} mét")
        parts.append("bạn sẽ đến nơi")
        return ' '.join(parts).strip()

    def save_text_route(self, filepath: str, meters_per_cell: float | None = None) -> str:
        text = self.build_text_route(meters_per_cell)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text + "\n")
        except Exception as e:
            return f"Lỗi ghi file: {e}"
        return filepath

    def _resolve_positions_for_shelf(self, shelf):
        if isinstance(shelf, int) or (isinstance(shelf, str) and shelf.isdigit()):
            sid = int(shelf)
            pos = []
            label = None
            for _k, info in PRODUCT_CATEGORIES.items():
                if info.get('shelf_id') == sid:
                    pos.extend(info.get('positions', []) or [])
                    if label is None:
                        d = str(info.get('description') or '').strip().upper()
                        label = f"kệ {d}" if d else f"kệ {sid}"
            return (pos, label or f"kệ {sid}") if pos else (None, None)
        if isinstance(shelf, str):
            key = shelf.strip()
            key_up = key.upper()
            if key in PRODUCT_CATEGORIES:
                info = PRODUCT_CATEGORIES[key]
                pos = list(info.get('positions', []) or [])
                if pos:
                    d = str(info.get('description') or '').strip().upper()
                    name = str(info.get('name') or '').strip()
                    label = f"kệ {d}" if d else (name or f"mục {key}")
                    return pos, label
            acc = []
            label = None
            for _k, info in PRODUCT_CATEGORIES.items():
                d = str(info.get('description') or '').strip().upper()
                if d == key_up:
                    acc.extend(info.get('positions', []) or [])
                    if label is None:
                        label = f"kệ {d}"
            if acc:
                return acc, (label or f"kệ {key_up}")
            acc = []
            label = None
            for _k, info in PRODUCT_CATEGORIES.items():
                name = str(info.get('name') or '').strip()
                if name and name.lower() == key.lower():
                    acc.extend(info.get('positions', []) or [])
                    if label is None:
                        d = str(info.get('description') or '').strip().upper()
                        label = f"kệ {d}" if d else name
            if acc:
                return acc, (label or key)
        return None, None

    def find_path_to_positions(self, positions, label: str | None = None):
        if not positions:
            print("Đầu vào vị trí rỗng")
            self.current_path = []
            return False
        product_positions = [tuple(p) for p in positions]
        result = self.pathfinder.find_nearest_shelf_access(self.user_pos, product_positions)
        if result:
            target_pos, path, distance = result
            self.current_path = path
            self.path_animation_index = 0
            self.total_searches += 1
            self.total_distance += distance
            label_txt = label or "mục tiêu"
            print(f"Tìm thấy đường đến {label_txt} - Khoảng cách: {distance:.1f} bước")
            self.last_route_text = self.build_text_route()
            print(f"Chỉ đường: {self.last_route_text}")
            try:
                route_path = os.path.join(self.base_dir, 'route.txt')
                saved = self.save_text_route(route_path)
                if os.path.isfile(route_path):
                    print(f"Đã ghi chỉ đường vào: {route_path}")
                else:
                    print(saved)
            except Exception as e:
                print(f"Không thể ghi file chỉ đường: {e}")
            return True
        else:
            self.current_path = []
            print(f"Không tìm thấy đường đến {label or 'mục tiêu'}")
            return False

    def update_animations(self, dt):
        self.animation_time += dt
        if self.current_path and self.path_animation_index < len(self.current_path):
            self.path_animation_index += dt * 50  # Tăng tốc độ animation
            print(f"Updated path_animation_index: {self.path_animation_index:.2f}, Path length: {len(self.current_path)}")

    def update_routing(self, dt):
        self.update_animations(dt)
        print(f"Updating routing with dt: {dt:.4f}")

def open_gui_and_route_to_shelf(shelf, screen=None, clock=None) -> 'FinalSupermarketFindBot':
    bot = FinalSupermarketFindBot(screen=screen, clock=clock)
    pos, label = bot._resolve_positions_for_shelf(shelf)
    print(f"Shelf input: {shelf}, Resolved positions: {pos}, Label: {label}")
    if pos:
        bot.find_path_to_positions(pos, label=label)
    else:
        print("Không xác định được đích đến từ đầu vào")
    return bot
