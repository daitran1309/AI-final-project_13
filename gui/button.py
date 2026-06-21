"""
Module button: Button widget với hover animation, ripple/scale effect.
"""

import pygame
import math
from gui.colors import Colors


class Button:
    """
    Nút bấm premium với hiệu ứng:
    - Hover: đổi màu mượt + scale nhẹ
    - Click: ripple effect
    - Active: viền glow
    """

    def __init__(self, x, y, width, height, text, callback=None,
                 font_size=14, color=None, hover_color=None, active_color=None,
                 icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_rect = pygame.Rect(x, y, width, height)  # Rect gốc (không scale)
        self.text = text
        self.callback = callback
        self.font_size = font_size
        self.icon = icon  # Emoji/text icon

        # Màu tùy chỉnh
        self.color = color or Colors.BTN_NORMAL
        self.hover_color = hover_color or Colors.BTN_HOVER
        self.active_color = active_color or Colors.BTN_ACTIVE

        self.is_hovered = False
        self.is_active = False
        self.is_enabled = True

        # Animation state
        self._hover_progress = 0.0       # 0→1 hover transition
        self._scale = 1.0                # Scale hiện tại
        self._ripple_alpha = 0           # Ripple opacity
        self._ripple_radius = 0          # Ripple bán kính
        self._ripple_center = (0, 0)     # Ripple tâm
        self._click_time = 0             # Thời gian click

    def draw(self, surface):
        """Vẽ nút với hiệu ứng."""
        now = pygame.time.get_ticks()

        # --- Hover transition ---
        target = 1.0 if self.is_hovered else 0.0
        self._hover_progress += (target - self._hover_progress) * 0.15
        self._hover_progress = max(0, min(1, self._hover_progress))

        # --- Scale animation ---
        target_scale = 1.03 if self.is_hovered else 1.0
        self._scale += (target_scale - self._scale) * 0.12

        # Tính rect scaled
        w = int(self.base_rect.width * self._scale)
        h = int(self.base_rect.height * self._scale)
        cx, cy = self.base_rect.center
        draw_rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)

        # --- Màu nền blend ---
        if not self.is_enabled:
            bg = (30, 25, 50)
        elif self.is_active:
            bg = self.active_color
        else:
            bg = self._blend_color(self.color, self.hover_color, self._hover_progress)

        # --- Đổ bóng nhẹ ---
        shadow_rect = draw_rect.inflate(2, 2)
        shadow_rect.y += 2
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 40), shadow_surf.get_rect(), border_radius=8)
        surface.blit(shadow_surf, shadow_rect.topleft)

        # --- Vẽ nền ---
        pygame.draw.rect(surface, bg, draw_rect, border_radius=8)

        # --- Viền ---
        if self.is_active:
            # Glow viền cho active
            glow_rect = draw_rect.inflate(2, 2)
            pygame.draw.rect(surface, Colors.BTN_ACTIVE_GLOW, glow_rect, width=2, border_radius=9)
        else:
            border_alpha = int(60 + 40 * self._hover_progress)
            border_color = self._blend_color(Colors.PANEL_BORDER, (120, 100, 200), self._hover_progress)
            pygame.draw.rect(surface, border_color, draw_rect, width=1, border_radius=8)

        # --- Ripple effect ---
        if self._ripple_alpha > 0:
            elapsed = now - self._click_time
            self._ripple_radius = min(elapsed * 0.5, max(w, h))
            self._ripple_alpha = max(0, 180 - elapsed * 0.5)
            if self._ripple_alpha > 0:
                ripple_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                local_center = (self._ripple_center[0] - draw_rect.x,
                                self._ripple_center[1] - draw_rect.y)
                pygame.draw.circle(ripple_surf, (255, 255, 255, int(self._ripple_alpha)),
                                   local_center, int(self._ripple_radius))
                # Clip vào rect
                clip_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.rect(clip_surf, (255, 255, 255, 255), clip_surf.get_rect(), border_radius=8)
                ripple_surf.blit(clip_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                surface.blit(ripple_surf, draw_rect.topleft)

        # --- Vẽ text ---
        font = pygame.font.SysFont("arial", self.font_size, bold=True)
        text_color = Colors.BTN_TEXT if self.is_enabled else Colors.TEXT_DIM
        if self.is_active:
            text_color = Colors.TEXT_HIGHLIGHT

        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        text_surface = font.render(display_text, True, text_color)
        text_rect = text_surface.get_rect(center=draw_rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Xử lý sự kiện chuột."""
        if not self.is_enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # Trigger ripple
                self._ripple_center = event.pos
                self._ripple_alpha = 180
                self._ripple_radius = 0
                self._click_time = pygame.time.get_ticks()
                if self.callback:
                    self.callback()
                return True
        return False

    def set_position(self, x, y):
        """Di chuyển nút."""
        self.rect.x = x
        self.rect.y = y
        self.base_rect.x = x
        self.base_rect.y = y

    @staticmethod
    def _blend_color(c1, c2, t):
        """Blend 2 màu RGB theo t (0→1)."""
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
