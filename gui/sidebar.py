"""
Module sidebar: Bảng điều khiển với giao diện Clean & Modern Minimalist.
"""

import pygame
import config
from gui.theme import UITheme
from gui.components import Button, PillToggleGroup, draw_card

LEGEND_ITEMS = [
    ("Bắt đầu", UITheme.START),
    ("Đích", UITheme.GOAL),
    ("Tường", UITheme.CELL_WALL),
    ("Đầm lầy", UITheme.CELL_WEIGHT),
    ("Vùng cấm", UITheme.CELL_FORBIDDEN),
    ("Đã duyệt", UITheme.CELL_VISITED),
    ("Đường đi", UITheme.CELL_PATH),
]

DRAW_MODE_MAP = {
    "Tường": "wall",
    "Bắt Đầu": "start",
    "Đích": "goal",
    "Đầm Lầy": "weight",
    "Cấm": "forbid",
    "Xoá": "erase"
}

class Sidebar:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.selected_group = None
        self.selected_algorithm = None
        self.draw_mode = "wall"
        self.animation_speed = config.ANIMATION_SPEED_DEFAULT
        self.metrics = None
        
        self.speed_min = config.ANIMATION_SPEED_MIN
        self.speed_max = config.ANIMATION_SPEED_MAX
        self.is_dragging_slider = False

        self._create_components()

    def _create_components(self):
        """Khởi tạo các UI components."""
        pad = UITheme.PADDING
        inner_w = self.width - 2 * pad
        
        # 1. Action Buttons
        # Chúng ta khởi tạo trước để có rect cố định khi vẽ
        btn_w = (inner_w - 2 * pad - 10) // 3
        y_actions = 0 # Sẽ được tính lại trong draw
        self.btn_run = Button(0, 0, btn_w, UITheme.BTN_HEIGHT, "Chạy", style='filled', color=UITheme.BTN_RUN, font_size=14)
        self.btn_reset = Button(0, 0, btn_w, UITheme.BTN_HEIGHT, "Làm Mới", style='outline', color=UITheme.BTN_RESET, font_size=14)
        self.btn_random = Button(0, 0, btn_w, UITheme.BTN_HEIGHT, "Ngẫu Nhiên", style='outline', color=UITheme.BTN_RANDOM, font_size=14)
        
        # 2. Draw Mode Pill
        draw_options = list(DRAW_MODE_MAP.keys())
        self.draw_mode_group = PillToggleGroup(0, 0, inner_w - 2 * pad, UITheme.BTN_HEIGHT, draw_options, font_size=11)
        self.draw_mode_group.selected = "Tường"
        
        # 3. Algorithm Group Pills (2x3 grid)
        # Sẽ được tạo ở _update_algo_buttons dựa trên config
        self.group_options_1 = list(config.ALGORITHM_GROUPS.keys())[:3]
        self.group_options_2 = list(config.ALGORITHM_GROUPS.keys())[3:]
        self.group_pill_1 = PillToggleGroup(0, 0, inner_w - 2 * pad, 28, self.group_options_1, font_size=10)
        self.group_pill_2 = PillToggleGroup(0, 0, inner_w - 2 * pad, 28, self.group_options_2, font_size=10)
        
        self.algo_buttons = []
        
        self.slider_rect = pygame.Rect(0, 0, inner_w - 2 * pad, 6)

    def update_algo_buttons(self, y_offset=0):
        """Tạo danh sách các nút chọn thuật toán."""
        self.algo_buttons = []
        if self.selected_group and self.selected_group in config.ALGORITHM_GROUPS:
            pad = UITheme.PADDING
            inner_w = self.width - 2 * pad
            btn_w = inner_w - 2 * pad
            btn_h = 32
            
            algos = config.ALGORITHM_GROUPS[self.selected_group]
            if self.selected_algorithm not in algos:
                self.selected_algorithm = algos[0]
                
            for algo_name in algos:
                btn = Button(0, 0, btn_w, btn_h, algo_name, style='ghost', color=UITheme.PRIMARY, font_size=12)
                self.algo_buttons.append((algo_name, btn))

    def set_position(self, x, y, height):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.height = height

    def draw(self, surface):
        # Background Sidebar
        pygame.draw.rect(surface, UITheme.BG_LIGHT, self.rect)
        # Border chia cách grid
        pygame.draw.line(surface, UITheme.GRID_BORDER, (self.x, self.y), (self.x, self.y + self.height), 2)
        
        pad = UITheme.PADDING
        inner_w = self.width - 2 * pad
        current_y = self.y + pad
        
        # --- 1. Header Card ---
        header_h = 50
        header_rect = pygame.Rect(self.x + pad, current_y, inner_w, header_h)
        draw_card(surface, header_rect)
        self._draw_header_content(surface, header_rect)
        current_y += header_h + 10

        # --- 2. Algorithm Groups Card ---
        group_h = 90
        group_rect = pygame.Rect(self.x + pad, current_y, inner_w, group_h)
        draw_card(surface, group_rect)
        self._draw_section_title(surface, "NHÓM THUẬT TOÁN", group_rect.x + pad, group_rect.y + 10)
        
        self.group_pill_1.rect.topleft = (group_rect.x + pad, group_rect.y + 30)
        self.group_pill_2.rect.topleft = (group_rect.x + pad, group_rect.y + 30 + 28 + 4)
        
        # Update selected in pills
        if self.selected_group in self.group_options_1:
            self.group_pill_1.selected = self.selected_group
            self.group_pill_2.selected = None
        else:
            self.group_pill_2.selected = self.selected_group
            self.group_pill_1.selected = None
            
        self.group_pill_1.draw(surface)
        self.group_pill_2.draw(surface)
        
        current_y += group_h + 10

        # --- 3. Select Algorithm Card ---
        if self.algo_buttons:
            algo_h = 36 + len(self.algo_buttons) * 36
            algo_rect = pygame.Rect(self.x + pad, current_y, inner_w, algo_h)
            draw_card(surface, algo_rect)
            self._draw_section_title(surface, "CHỌN THUẬT TOÁN", algo_rect.x + pad, algo_rect.y + 10)
            
            by = algo_rect.y + 30
            for algo_name, btn in self.algo_buttons:
                btn.rect.topleft = (algo_rect.x + pad, by)
                btn.is_active = (algo_name == self.selected_algorithm)
                btn.draw(surface)
                by += 36
            current_y += algo_h + 10

        # --- 4. Statistics Card ---
        stat_h = 130
        stat_rect = pygame.Rect(self.x + pad, current_y, inner_w, stat_h)
        draw_card(surface, stat_rect)
        self._draw_section_title(surface, "THỐNG KÊ THỜI GIAN THỰC", stat_rect.x + pad, stat_rect.y + 10)
        self._draw_statistics(surface, stat_rect)
        current_y += stat_h + 10

        # --- 5 & 6. Controls & Actions Card ---
        ctrl_h = 120
        ctrl_rect = pygame.Rect(self.x + pad, current_y, inner_w, ctrl_h)
        draw_card(surface, ctrl_rect)
        self._draw_section_title(surface, "ĐIỀU KHIỂN & TỐC ĐỘ", ctrl_rect.x + pad, ctrl_rect.y + 10)
        
        self.slider_rect.topleft = (ctrl_rect.x + pad, ctrl_rect.y + 45)
        self._draw_speed_slider(surface, self.slider_rect)
        
        act_y = ctrl_rect.y + 70
        btn_w = (inner_w - 2 * pad - 10) // 3
        
        self.btn_run.rect.topleft = (ctrl_rect.x + pad, act_y)
        self.btn_run.rect.width = btn_w
        self.btn_reset.rect.topleft = (self.btn_run.rect.right + 5, act_y)
        self.btn_reset.rect.width = btn_w
        self.btn_random.rect.topleft = (self.btn_reset.rect.right + 5, act_y)
        self.btn_random.rect.width = btn_w
        
        self.btn_run.draw(surface)
        self.btn_reset.draw(surface)
        self.btn_random.draw(surface)
        
        current_y += ctrl_h + 10

        # --- 7. Draw Mode Card ---
        draw_h = 95
        draw_rect = pygame.Rect(self.x + pad, current_y, inner_w, draw_h)
        draw_card(surface, draw_rect)
        self._draw_section_title(surface, "CÔNG CỤ VẼ BẢN ĐỒ", draw_rect.x + pad, draw_rect.y + 10)
        self.draw_mode_group.rect.topleft = (draw_rect.x + pad, draw_rect.y + 25)
        selected_vi = self.draw_mode_group.selected
        self.draw_mode = DRAW_MODE_MAP[selected_vi] if selected_vi else "wall"
        self.draw_mode_group.draw(surface)
        
        # Ghi chú trực quan cho người dùng
        note_text = ""
        if self.draw_mode == "wall": note_text = "* Tường cứng: Chướng ngại vật không thể đi qua."
        elif self.draw_mode == "weight": note_text = "* Vùng lầy: Đi qua tốn x5 chi phí (chỉ A*/UCS biết né)."
        elif self.draw_mode == "forbid": note_text = "* Vùng cấm: Khu vực giới hạn (dùng cho mô hình CSP)."
        elif self.draw_mode == "start": note_text = "* Điểm bắt đầu: Vị trí xuất phát của Robot."
        elif self.draw_mode == "goal": note_text = "* Đích đến: Vị trí gói hàng cần giao."
        elif self.draw_mode == "erase": note_text = "* Cục tẩy: Click/Kéo chuột để xoá chướng ngại vật."
        
        font_note = UITheme.font(11, italic=True)
        surf_note = font_note.render(note_text, True, UITheme.TEXT_MAIN)
        surface.blit(surf_note, (draw_rect.x + pad, draw_rect.y + 70))

        current_y += draw_h + 10

        # --- 8. Legend ---
        self._draw_legend(surface, self.x + pad, current_y, inner_w)

    def _draw_header_content(self, surface, rect):
        """Vẽ title và icon robot đơn giản."""
        # Icon robot (hình chữ nhật có mắt)
        rx, ry = rect.x + 20, rect.y + 12
        pygame.draw.rect(surface, UITheme.PRIMARY, (rx, ry, 24, 24), border_radius=6)
        pygame.draw.rect(surface, UITheme.TEXT_WHITE, (rx + 4, ry + 6, 6, 6), border_radius=2)
        pygame.draw.rect(surface, UITheme.TEXT_WHITE, (rx + 14, ry + 6, 6, 6), border_radius=2)
        pygame.draw.rect(surface, UITheme.TEXT_WHITE, (rx + 6, ry + 16, 12, 4), border_radius=2)
        
        font = UITheme.font(16, bold=True)
        title = font.render("Robot Giao Hàng", True, UITheme.TEXT_MAIN)
        surface.blit(title, (rx + 35, ry - 2))
        
        font_sub = UITheme.font(11)
        sub = font_sub.render("Mô phỏng Tìm đường AI", True, UITheme.TEXT_LIGHT)
        surface.blit(sub, (rx + 35, ry + 16))

    def _draw_section_title(self, surface, text, x, y):
        """Vẽ tiêu đề section (chữ HOA, letter-spacing nhỏ)."""
        font = UITheme.font(10, bold=True)
        # Pygame không có letter-spacing dễ, ta tự render từng chữ nếu cần, nhưng tạm dùng render thường
        label = font.render(text, True, UITheme.TEXT_LIGHT)
        surface.blit(label, (x, y))

    def _draw_statistics(self, surface, rect):
        """Vẽ Stats Card."""
        font_label = UITheme.font(11, bold=True)
        font_val = UITheme.font(12, bold=True)
        
        pad = UITheme.PADDING
        x = rect.x + pad
        y = rect.y + 30
        
        nodes = self.metrics.get('steps', 0) if self.metrics else 0
        path_len = self.metrics.get('path_length', 0) if self.metrics else 0
        time_ms = self.metrics.get('execution_time', 0)*1000 if self.metrics else 0
        frontier = self.metrics.get('visited_count', 0) if self.metrics else 0
        
        stats = [
            ("Số ô đã duyệt", str(nodes), UITheme.PRIMARY),
            ("Độ dài đường đi", f"{path_len} ô", UITheme.CELL_PATH),
            ("Thời gian chạy", f"{time_ms:.1f} ms", UITheme.START),
            ("Ô chờ (Frontier)", str(frontier), UITheme.GOAL),
        ]
        
        for lbl, val, color in stats:
            # Thin colored left-border accent
            accent_rect = pygame.Rect(x, y, 4, 14)
            pygame.draw.rect(surface, color, accent_rect, border_radius=2)
            
            # Label
            surf_lbl = font_label.render(lbl, True, UITheme.TEXT_MAIN)
            surface.blit(surf_lbl, (x + 10, y))
            
            # Badge
            surf_val = font_val.render(val, True, color)
            val_rect = surf_val.get_rect()
            
            # Badge background (màu nhạt hơn)
            badge_bg = (color[0], color[1], color[2], 30)
            badge_surf = pygame.Surface((val_rect.width + 12, 20), pygame.SRCALPHA)
            pygame.draw.rect(badge_surf, badge_bg, badge_surf.get_rect(), border_radius=10)
            
            bx = rect.right - pad - badge_surf.get_width()
            by = y - 2
            surface.blit(badge_surf, (bx, by))
            surface.blit(surf_val, (bx + 6, by + 2))
            
            y += 24

    def _draw_speed_slider(self, surface, rect):
        """Vẽ speed slider."""
        # Label
        font = UITheme.font(11, bold=True)
        label_left = font.render("Chậm", True, UITheme.TEXT_LIGHT)
        label_right = font.render("Nhanh", True, UITheme.TEXT_LIGHT)
        
        surface.blit(label_left, (rect.x, rect.y - 18))
        surface.blit(label_right, (rect.right - label_right.get_width(), rect.y - 18))
        
        # Track
        pygame.draw.rect(surface, UITheme.BORDER, rect, border_radius=3)
        
        # Fill (tỉ lệ ngược: max_speed (500) là bên trái, min_speed (5) là bên phải)
        t = 1.0 - (self.animation_speed - self.speed_min) / max(1, self.speed_max - self.speed_min)
        fill_w = int(rect.width * t)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_w, rect.height)
        pygame.draw.rect(surface, UITheme.PRIMARY, fill_rect, border_radius=3)
        
        # Knob
        knob_x = rect.x + fill_w
        pygame.draw.circle(surface, UITheme.BG_WHITE, (knob_x, rect.centery), 8)
        pygame.draw.circle(surface, UITheme.PRIMARY, (knob_x, rect.centery), 8, 2)

    def _draw_legend(self, surface, x, y, width):
        """Vẽ legend (ngang compact)."""
        font = UITheme.font(11)
        col_w = width // 3
        
        for i, (label, color) in enumerate(LEGEND_ITEMS):
            r = i // 3
            c = i % 3
            cx = x + c * col_w
            cy = y + r * 18
            
            pygame.draw.rect(surface, color, (cx, cy, 10, 10), border_radius=2)
            pygame.draw.rect(surface, UITheme.BORDER, (cx, cy, 10, 10), width=1, border_radius=2)
            
            lbl_surf = font.render(label, True, UITheme.TEXT_MAIN)
            surface.blit(lbl_surf, (cx + 16, cy - 2))

    def handle_event(self, event):
        # 1. Action buttons
        if self.btn_run.handle_event(event): return {'type': 'run'}
        if self.btn_reset.handle_event(event): return {'type': 'reset'}
        if self.btn_random.handle_event(event): return {'type': 'random_maze'}
        
        # 2. Slider
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect.inflate(10, 20).collidepoint(event.pos):
                self.is_dragging_slider = True
                self._update_slider_value(event.pos[0])
                return {'type': 'speed_change', 'speed': self.animation_speed}
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging_slider = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging_slider:
            self._update_slider_value(event.pos[0])
            return {'type': 'speed_change', 'speed': self.animation_speed}
            
        # 3. Pill groups
        if self.group_pill_1.handle_event(event):
            self.selected_group = self.group_pill_1.selected
            self.update_algo_buttons()
            return {'type': 'select_group', 'group': self.selected_group}
        if self.group_pill_2.handle_event(event):
            self.selected_group = self.group_pill_2.selected
            self.update_algo_buttons()
            return {'type': 'select_group', 'group': self.selected_group}
            
        if self.draw_mode_group.handle_event(event):
            self.draw_mode = self.draw_mode_group.selected.lower()
            return {'type': 'draw_mode', 'mode': self.draw_mode}
            
        # 4. Algo buttons
        for algo_name, btn in self.algo_buttons:
            if btn.handle_event(event):
                self.selected_algorithm = algo_name
                return {'type': 'select_algorithm', 'algorithm': algo_name}
                
        return None

    def _update_slider_value(self, mouse_x):
        t = (mouse_x - self.slider_rect.x) / self.slider_rect.width
        t = max(0, min(1, t))
        # Kéo phải (t=1) = Fast (speed thấp)
        self.animation_speed = int(self.speed_max - t * (self.speed_max - self.speed_min))
        self.animation_speed = max(self.speed_min, min(self.speed_max, self.animation_speed))
