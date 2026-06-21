"""
Module renderer: Vẽ grid Clean & Modern Minimalist.
"""

import pygame
import math
import config
from gui.theme import UITheme

class Renderer:
    def __init__(self, surface, offset_x=None, offset_y=None, cell_size=None):
        self.surface = surface
        self.offset_x = offset_x or config.GRID_OFFSET_X
        self.offset_y = offset_y or config.GRID_OFFSET_Y
        self.cell_size = cell_size or config.CELL_SIZE
        self.hover_cell = None
        self._glow_time = 0
        
        self.animation_speed = config.ANIMATION_SPEED_DEFAULT # Sẽ được update từ app

    def draw_grid(self, grid):
        """Vẽ toàn bộ grid."""
        # Nền grid
        grid_w = grid.cols * self.cell_size
        grid_h = grid.rows * self.cell_size
        pygame.draw.rect(self.surface, UITheme.BG_WHITE, (self.offset_x, self.offset_y, grid_w, grid_h))

        # Kẻ lưới mỏng (Border)
        for row in range(grid.rows + 1):
            y = self.offset_y + row * self.cell_size
            pygame.draw.line(self.surface, UITheme.GRID_BORDER, (self.offset_x, y), (self.offset_x + grid_w, y), 1)
        for col in range(grid.cols + 1):
            x = self.offset_x + col * self.cell_size
            pygame.draw.line(self.surface, UITheme.GRID_BORDER, (x, self.offset_y), (x, self.offset_y + grid_h), 1)

        # Vẽ các ô đặc biệt (Wall, Weight, Forbidden)
        for row in range(grid.rows):
            for col in range(grid.cols):
                cell_type = grid.cells[row][col]
                if cell_type in [config.CELL_WALL, config.CELL_WEIGHT, config.CELL_FORBIDDEN]:
                    self._draw_cell(row, col, cell_type)

        # Hover
        if self.hover_cell:
            self._draw_hover(self.hover_cell[0], self.hover_cell[1])

    def _draw_cell(self, row, col, cell_type):
        x = self.offset_x + col * self.cell_size
        y = self.offset_y + row * self.cell_size
        rect = pygame.Rect(x + 1, y + 1, self.cell_size - 1, self.cell_size - 1)

        if cell_type == config.CELL_WALL:
            pygame.draw.rect(self.surface, UITheme.CELL_WALL, rect)
        elif cell_type == config.CELL_WEIGHT:
            pygame.draw.rect(self.surface, UITheme.CELL_WEIGHT, rect)
            self._draw_cell_icon(rect, "~", UITheme.TEXT_MAIN)
        elif cell_type == config.CELL_FORBIDDEN:
            pygame.draw.rect(self.surface, UITheme.CELL_FORBIDDEN, rect)
            self._draw_cell_icon(rect, "✕", UITheme.GOAL)

    def _draw_cell_icon(self, rect, icon, color):
        font = UITheme.font(max(10, self.cell_size // 3))
        text = font.render(icon, True, color)
        self.surface.blit(text, text.get_rect(center=rect.center))

    def _draw_hover(self, row, col):
        x = self.offset_x + col * self.cell_size
        y = self.offset_y + row * self.cell_size
        hover_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        pygame.draw.rect(hover_surf, (0, 0, 0, 10), hover_surf.get_rect())
        self.surface.blit(hover_surf, (x, y))

    def draw_visited(self, visited_list, count):
        """Vẽ visited cells với hiệu ứng fade-in."""
        for i in range(count):
            row, col = visited_list[i]
            # Loại bỏ các vị trí trùng với wall, start, goal cho đẹp
            # Nhưng để đơn giản, vẽ đè lên
            x = self.offset_x + col * self.cell_size + 1
            y = self.offset_y + row * self.cell_size + 1
            rect = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)

            age = count - i
            fade_duration_ms = 150.0
            time_lived = age * self.animation_speed
            t = min(1.0, time_lived / fade_duration_ms)
            
            color = self._blend_color(UITheme.BG_WHITE, UITheme.CELL_VISITED, t)
            
            # Khung viền mờ khi đang fade in
            pygame.draw.rect(self.surface, color, rect)

    def draw_path(self, path, count=None):
        """Vẽ path với hiệu ứng xuất hiện dần (nếu có count) và pulse."""
        if not path: return
        
        self._glow_time += 1
        pulse = 0.5 + 0.5 * math.sin(self._glow_time * 0.1)
        
        limit = count if count is not None else len(path)
        
        for i in range(limit):
            row, col = path[i]
            x = self.offset_x + col * self.cell_size + 1
            y = self.offset_y + row * self.cell_size + 1
            rect = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
            
            # Pulse logic cho path: golden yellow sáng lấp lánh nhẹ
            r = int(UITheme.CELL_PATH[0] + (255 - UITheme.CELL_PATH[0]) * 0.2 * pulse)
            g = int(UITheme.CELL_PATH[1] + (255 - UITheme.CELL_PATH[1]) * 0.2 * pulse)
            b = int(UITheme.CELL_PATH[2] + (255 - UITheme.CELL_PATH[2]) * 0.2 * pulse)
            
            pygame.draw.rect(self.surface, (r, g, b), rect)

    def draw_start_goal(self, grid):
        """Vẽ Start và Goal dưới dạng hình tròn."""
        if grid.start:
            self._draw_circle_icon(grid.start, UITheme.START, is_start=True)
        if grid.goal:
            self._draw_circle_icon(grid.goal, UITheme.GOAL, is_start=False)

    def _draw_circle_icon(self, pos, color, is_start):
        row, col = pos
        cx = self.offset_x + col * self.cell_size + self.cell_size // 2
        cy = self.offset_y + row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        
        # Glow
        glow_surf = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 40), (radius*2, radius*2), radius + 4)
        self.surface.blit(glow_surf, (cx - radius*2, cy - radius*2))
        
        # Circle
        pygame.draw.circle(self.surface, color, (cx, cy), radius)
        
        # Simple Shape
        if is_start: # Robot shape (vuông trắng)
            sw = radius * 0.8
            pygame.draw.rect(self.surface, UITheme.TEXT_WHITE, (cx - sw/2, cy - sw/2, sw, sw), border_radius=2)
            pygame.draw.rect(self.surface, color, (cx - sw/4, cy - sw/4, sw/2, sw/4)) # Mắt
        else: # Package shape (hộp vuông có băng dính)
            bw = radius * 0.8
            pygame.draw.rect(self.surface, UITheme.TEXT_WHITE, (cx - bw/2, cy - bw/2, bw, bw), border_radius=2)
            pygame.draw.line(self.surface, color, (cx - bw/2, cy), (cx + bw/2, cy), 2)

    def get_cell_at_mouse(self, mouse_pos, grid):
        mx, my = mouse_pos
        col = (mx - self.offset_x) // self.cell_size
        row = (my - self.offset_y) // self.cell_size
        if grid.in_bounds(row, col):
            return (row, col)
        return None

    def update_hover(self, mouse_pos, grid):
        self.hover_cell = self.get_cell_at_mouse(mouse_pos, grid)

    @staticmethod
    def _blend_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
