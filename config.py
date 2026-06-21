"""
Cấu hình toàn cục cho project Robot Giao Hàng.
"""

# ============================================================
# CỬA SỔ & HIỂN THỊ
# ============================================================
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 800
FPS = 60
TITLE = "Delivery Robot Pathfinding"

# ============================================================
# GRID
# ============================================================
GRID_ROWS = 20
GRID_COLS = 30
CELL_SIZE = 30       # px mỗi ô
GRID_OFFSET_X = 10   # Khoảng cách grid với cạnh trái
GRID_OFFSET_Y = 10   # Khoảng cách grid với cạnh trên

# ============================================================
# GIÁ TRỊ Ô (Cell Types)
# ============================================================
CELL_EMPTY = 0       # Ô trống (đi được)
CELL_WALL = 1        # Vật cản (tường)
CELL_START = 2       # Điểm bắt đầu
CELL_GOAL = 3        # Điểm đích
CELL_WEIGHT = 4      # Ô có trọng số cao (terrain khó đi)
CELL_FORBIDDEN = 5   # Vùng cấm (dùng cho CSP)

# ============================================================
# TRỌNG SỐ
# ============================================================
DEFAULT_WEIGHT = 1       # Trọng số mặc định ô trống
HEAVY_WEIGHT = 5         # Trọng số ô nặng (terrain khó)

# ============================================================
# ANIMATION
# ============================================================
ANIMATION_SPEED_DEFAULT = 50   # ms giữa mỗi bước animation
ANIMATION_SPEED_MIN = 5
ANIMATION_SPEED_MAX = 500

# ============================================================
# SIDEBAR
# ============================================================
SIDEBAR_WIDTH = 420
SIDEBAR_X = WINDOW_WIDTH - SIDEBAR_WIDTH

# ============================================================
# NHÓM THUẬT TOÁN
# ============================================================
ALGORITHM_GROUPS = {
    "Tìm Kiếm Mù": ["BFS", "DFS", "IDS"],
    "Có Thông Tin": ["UCS", "Greedy", "A*"],
    "Tìm Cục Bộ": ["Simple Hill Climbing", "Steepest Hill Climbing", "Local Beam Search"],
    "Môi Trường Ẩn": ["No Observation (BFS)", "No Observation (DFS)", "Partially Observable (Greedy)"],
    "Ràng Buộc CSP": ["CSP Backtracking", "Forward Checking", "Min-Conflicts"],
    "Tìm Đối Kháng": ["Minimax", "Alpha-Beta", "Expectimax"],
}

# ============================================================
# ĐỐI KHÁNG (Adversarial)
# ============================================================
ADVERSARIAL_MAX_DEPTH = 4        # Độ sâu tối đa cây game
ADVERSARIAL_NUM_OBSTACLES = 3    # Số vật cản môi trường thêm mỗi lượt

# ============================================================
# BELIEF STATE (Complex Environments)
# ============================================================
SENSOR_RANGE = 2                 # Tầm cảm biến (partially observable)

# ============================================================
# CSP
# ============================================================
CSP_MAX_STEPS = 100              # Giới hạn bước đi cho CSP
