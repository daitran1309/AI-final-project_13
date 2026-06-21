"""
Module components: UI widgets như Button, PillToggle, Card, StatBadge.
"""

import pygame
from gui.theme import UITheme

def draw_card(surface, rect):
    """Vẽ card nền trắng với shadow 2px."""
    # Vẽ shadow (offset +2px y)
    shadow_rect = pygame.Rect(rect.x, rect.y + 2, rect.width, rect.height)
    pygame.draw.rect(surface, UITheme.SHADOW, shadow_rect, border_radius=UITheme.CARD_RADIUS)
    
    # Vẽ nền card
    pygame.draw.rect(surface, UITheme.BG_WHITE, rect, border_radius=UITheme.CARD_RADIUS)
    # Vẽ viền card
    pygame.draw.rect(surface, UITheme.GRID_BORDER, rect, width=1, border_radius=UITheme.CARD_RADIUS)

class Button:
    """Nút bấm có các style: 'filled', 'outline', 'ghost'."""
    def __init__(self, x, y, width, height, text, style='ghost', color=UITheme.PRIMARY, font_size=13):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.style = style  # 'filled', 'outline', 'ghost'
        self.color = color
        self.font_size = font_size
        self.is_hovered = False
        self.is_active = False

    def draw(self, surface):
        if self.style == 'filled' or self.is_active:
            bg_color = self._darken(self.color) if self.is_hovered else self.color
            pygame.draw.rect(surface, bg_color, self.rect, border_radius=UITheme.BTN_RADIUS)
            text_color = UITheme.TEXT_WHITE
        elif self.style == 'outline':
            bg_color = UITheme.HOVER_BG if self.is_hovered else UITheme.BG_WHITE
            pygame.draw.rect(surface, bg_color, self.rect, border_radius=UITheme.BTN_RADIUS)
            pygame.draw.rect(surface, self.color, self.rect, width=1, border_radius=UITheme.BTN_RADIUS)
            text_color = self.color
        else: # ghost
            bg_color = UITheme.HOVER_BG if self.is_hovered else UITheme.BG_WHITE
            pygame.draw.rect(surface, bg_color, self.rect, border_radius=UITheme.BTN_RADIUS)
            pygame.draw.rect(surface, UITheme.BORDER, self.rect, width=1, border_radius=UITheme.BTN_RADIUS)
            text_color = UITheme.PRIMARY if self.is_hovered else UITheme.TEXT_MAIN
            
        font = UITheme.font(self.font_size, bold=(self.style=='filled' or self.is_active))
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)
            if self.is_hovered != was_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if self.is_hovered else pygame.SYSTEM_CURSOR_ARROW)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
        
    def _darken(self, color, amount=0.1):
        """Làm tối màu đi 10%."""
        return tuple(max(0, int(c * (1 - amount))) for c in color[:3])

class PillToggleGroup:
    """Group các nút dạng pill dính liền nhau."""
    def __init__(self, x, y, width, height, options, font_size=11):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.font_size = font_size
        self.selected = options[0] if options else None
        self.hover_index = -1
        
        # Cấu hình pill
        self.btn_width = width / len(options) if options else 0

    def draw(self, surface):
        # Vẽ viền ngoài cùng bo tròn hoàn toàn
        radius = self.rect.height // 2
        pygame.draw.rect(surface, UITheme.BORDER, self.rect, width=1, border_radius=radius)
        
        font = UITheme.font(self.font_size, bold=True)
        
        for i, opt in enumerate(self.options):
            btn_rect = pygame.Rect(self.rect.x + i * self.btn_width, self.rect.y, self.btn_width, self.rect.height)
            
            # Nếu là nút đang chọn
            if self.selected == opt:
                if i == 0:
                    pygame.draw.rect(surface, UITheme.PRIMARY, btn_rect, border_top_left_radius=radius, border_bottom_left_radius=radius)
                elif i == len(self.options) - 1:
                    pygame.draw.rect(surface, UITheme.PRIMARY, btn_rect, border_top_right_radius=radius, border_bottom_right_radius=radius)
                else:
                    pygame.draw.rect(surface, UITheme.PRIMARY, btn_rect)
                text_color = UITheme.TEXT_WHITE
            else:
                if self.hover_index == i:
                    if i == 0:
                        pygame.draw.rect(surface, UITheme.HOVER_BG, btn_rect, border_top_left_radius=radius, border_bottom_left_radius=radius)
                    elif i == len(self.options) - 1:
                        pygame.draw.rect(surface, UITheme.HOVER_BG, btn_rect, border_top_right_radius=radius, border_bottom_right_radius=radius)
                    else:
                        pygame.draw.rect(surface, UITheme.HOVER_BG, btn_rect)
                text_color = UITheme.TEXT_MAIN
                
            text_surf = font.render(opt, True, text_color)
            text_rect = text_surf.get_rect(center=btn_rect.center)
            surface.blit(text_surf, text_rect)
            
            # Kẻ vạch chia
            if i > 0:
                pygame.draw.line(surface, UITheme.BORDER, (btn_rect.x, self.rect.y), (btn_rect.x, self.rect.bottom))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                idx = int((event.pos[0] - self.rect.x) / self.btn_width)
                if idx >= len(self.options): idx = len(self.options) - 1
                if self.hover_index != idx:
                    self.hover_index = idx
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                if self.hover_index != -1:
                    self.hover_index = -1
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_index != -1:
                self.selected = self.options[self.hover_index]
                return True
        return False
