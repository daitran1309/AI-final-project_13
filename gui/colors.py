"""
Module colors: Bảng màu premium SÁNG MÀU cho giao diện Pygame.
"""


class Colors:
    """Bảng màu giao diện - sáng, rực rỡ, dễ nhìn."""

    # === Gradient nền ===
    BG_TOP = (20, 22, 48)
    BG_BOTTOM = (35, 30, 65)

    # === Sidebar ===
    SIDEBAR_BG = (25, 22, 52)
    SIDEBAR_ACCENT = (50, 42, 85)

    # === Grid ===
    GRID_LINE = (60, 55, 100)
    CELL_EMPTY = (42, 38, 75)
    CELL_WALL = (18, 15, 35)
    CELL_WEIGHT = (180, 140, 40)
    CELL_FORBIDDEN = (200, 50, 70)

    # === Robot & Điểm đầu/cuối ===
    START = (0, 255, 130)
    START_GLOW = (0, 255, 130, 80)
    GOAL = (255, 80, 100)
    GOAL_GLOW = (255, 80, 100, 80)
    ROBOT = (30, 200, 255)

    # === Đường đi & Duyệt ===
    PATH = (255, 230, 30)
    PATH_GLOW = (255, 230, 30, 100)
    VISITED = (130, 110, 240)
    VISITED_FADE = (90, 70, 180)
    FRONTIER = (0, 240, 230)
    CURRENT = (255, 170, 20)
    CURRENT_GLOW = (255, 170, 20, 120)

    # === Text ===
    TEXT = (250, 250, 255)
    TEXT_DIM = (180, 180, 200)
    TEXT_HIGHLIGHT = (255, 255, 255)
    TEXT_ACCENT = (200, 180, 255)

    # === Buttons ===
    BTN_NORMAL = (55, 48, 95)
    BTN_HOVER = (75, 65, 130)
    BTN_ACTIVE = (100, 75, 230)
    BTN_ACTIVE_GLOW = (130, 100, 255)
    BTN_TEXT = (255, 255, 255)
    BTN_RUN = (0, 220, 120)
    BTN_RUN_HOVER = (20, 255, 145)
    BTN_RESET = (220, 75, 95)
    BTN_RESET_HOVER = (250, 100, 115)

    # === Panel / Card ===
    PANEL_BG = (38, 34, 68)
    PANEL_BORDER = (80, 68, 135)
    CARD_BG = (48, 42, 85)
    CARD_BORDER = (95, 80, 160)

    # === Header ===
    HEADER_BG = (30, 26, 58)
    HEADER_ACCENT = (130, 100, 255)

    # === Metrics ===
    SUCCESS = (0, 255, 130)
    FAILURE = (255, 80, 100)
    WARNING = (255, 220, 30)

    # === Legend ===
    LEGEND_BG = (32, 28, 58)

    # === Speed Slider ===
    SLIDER_TRACK = (65, 58, 110)
    SLIDER_FILL = (130, 100, 255)
    SLIDER_KNOB = (180, 160, 255)

    # === Belief State ===
    BELIEF = (200, 130, 255)

    # === Hover highlight ===
    HOVER_HIGHLIGHT = (255, 255, 255, 40)

    # === Đổ bóng ===
    SHADOW = (8, 5, 20, 140)
