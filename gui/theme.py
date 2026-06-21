"""
Module theme: Định nghĩa màu sắc, kích thước và style cho Light Theme (Clean & Modern Minimalist).
"""

import pygame

class UITheme:
    # === Colors ===
    BG_LIGHT = (248, 249, 250)      # #F8F9FA
    BG_WHITE = (255, 255, 255)      # #FFFFFF
    
    PRIMARY = (74, 144, 217)        # #4A90D9 Soft blue
    PRIMARY_HOVER = (91, 141, 239)  # #5B8DEF Soft blue
    
    START = (0, 200, 150)           # #00C896
    GOAL = (255, 107, 107)          # #FF6B6B
    
    GRID_BORDER = (232, 236, 242)   # #E8ECF2
    CELL_WALL = (45, 53, 97)        # #2D3561
    CELL_VISITED = (200, 222, 255)  # #C8DEFF
    CELL_PATH = (255, 217, 61)      # #FFD93D
    CELL_FORBIDDEN = (255, 179, 179)# #FFB3B3
    CELL_WEIGHT = (212, 245, 233)   # #D4F5E9
    
    TEXT_MAIN = (30, 36, 48)        # Darker contrast
    TEXT_LIGHT = (110, 118, 138)    # Darker contrast
    TEXT_WHITE = (255, 255, 255)
    
    BORDER = (209, 216, 232)        # #D1D8E8
    HOVER_BG = (238, 243, 255)      # #EEF3FF
    
    SHADOW = (224, 228, 237)        # #E0E4ED

    BTN_RUN = (0, 200, 150)         # Green
    BTN_RESET = (255, 107, 107)     # Red
    BTN_RANDOM = (74, 144, 217)     # Blue

    # === Dimensions ===
    CARD_RADIUS = 12
    BTN_RADIUS = 8
    BTN_HEIGHT = 36
    PADDING = 12
    
    @staticmethod
    def font(size, bold=False, italic=False):
        # Sử dụng segoeui làm font mặc định để hiển thị Tiếng Việt sắc nét nhất trên Windows
        return pygame.font.SysFont("segoe ui, tahoma, arial", size, bold=bold, italic=italic)
