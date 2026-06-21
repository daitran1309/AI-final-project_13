"""
Module presets: Bản đồ cố định cho từng nhóm thuật toán.

Mỗi nhóm có bản đồ riêng thiết kế để minh họa đặc điểm thuật toán.
    0 = ô trống
    1 = vật cản (tường)
    S = start
    G = goal
    W = ô trọng số cao (weight=5)
    F = vùng cấm (forbidden - CSP)
"""

import config
from core.grid import Grid


# ============================================================
# Nhóm 1: UNINFORMED SEARCH (BFS, DFS, IDS)
# Bản đồ mê cung đơn giản - thể hiện rõ cách duyệt khác nhau
# BFS duyệt theo tầng, DFS đi sâu, IDS kết hợp
# ============================================================
UNINFORMED_MAP = [
    "S 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 1 1 0 1 0 1 1 1 1 0 1 1 1 0 1 1 1 1 0",
    "0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 1 0",
    "1 0 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 0 0 0",
    "0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 1 0",
    "0 1 1 1 1 1 0 1 0 1 1 1 1 1 1 0 1 0 1 0",
    "0 0 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 1 0",
    "1 1 1 1 0 1 1 1 0 1 0 1 1 0 1 1 1 0 1 0",
    "0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0",
    "0 1 1 1 1 1 0 0 0 1 1 1 0 1 1 1 1 1 1 0",
    "0 0 0 0 0 1 0 1 0 0 0 0 0 1 0 0 0 0 0 0",
    "1 1 1 1 0 1 0 1 1 1 1 1 0 1 0 1 1 1 1 1",
    "0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 G",
]

# ============================================================
# Nhóm 2: INFORMED SEARCH (UCS, Greedy, A*)
# Bản đồ có trọng số - Greedy có thể chọn sai đường
# UCS và A* tìm đường chi phí thấp nhất (tránh ô nặng W)
# Có 2 đường: đường ngắn nhưng qua vùng nặng, đường xa nhưng nhẹ
# ============================================================
INFORMED_MAP = [
    "S 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 1 1 1 1 0 1 0 1 1 1 1 1 0 0 0 0 0 0",
    "0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0",
    "0 0 1 0 W W W W W W W 0 0 1 0 0 1 1 1 0",
    "0 0 1 0 W W W W W W W 0 0 0 0 0 1 0 0 0",
    "0 0 0 0 W W W W W W W 0 0 0 0 0 1 0 0 0",
    "0 0 0 0 W W W W W W W 0 0 1 0 0 0 0 1 0",
    "0 0 1 0 W W W W W W W 0 0 1 0 0 0 0 1 0",
    "0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0",
    "0 0 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 G",
]

# ============================================================
# Nhóm 3: LOCAL SEARCH (Hill Climbing, Beam Search)
# Bản đồ có local minimum (ngõ cụt dẫn gần goal nhưng không đến được)
# Hill climbing sẽ bị kẹt, Beam search có thể thoát
# ============================================================
LOCAL_SEARCH_MAP = [
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 S 0 0 0 1 0 0 0 0 0 0 G 0 0 0 0 0 0",
    "0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
]


# ============================================================
# Nhóm 4: COMPLEX ENVIRONMENTS (No Observation, Partially Observable)
# Bản đồ nhỏ hơn (belief state tăng theo cấp số mũ)
# Robot không biết vị trí → cần đi vào góc/tường để xác định
# ============================================================
COMPLEX_ENV_MAP = [
    "0 0 0 1 0 0 0",
    "0 1 0 1 0 1 0",
    "0 1 0 0 0 1 0",
    "0 0 0 1 0 0 0",
    "1 1 0 1 0 1 1",
    "0 0 0 0 0 0 0",
    "S 0 1 0 1 0 G",
]

# ============================================================
# Nhóm 5: CSP (Backtracking, Forward Checking, Min-Conflicts)
# Bản đồ có vùng cấm (F) - đường đi phải tránh vùng cấm
# Có giới hạn bước đi → ràng buộc thêm
# ============================================================
CSP_MAP = [
    "S 0 0 0 F F 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 1 0 F F 0 1 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 1 0 0 0 0 1 0 0 F F F 0 0 0 0 0 0 0",
    "0 0 1 1 1 1 0 1 0 0 F F F 0 1 1 1 1 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0",
    "0 1 1 1 1 0 F F F 0 1 1 1 1 1 0 0 1 0 0",
    "0 0 0 0 1 0 F F F 0 0 0 0 0 1 0 0 0 0 0",
    "0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0",
    "0 0 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 0 0",
    "0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0",
    "0 0 0 0 F F 0 0 0 0 0 0 0 F F 0 0 0 0 G",
]

# ============================================================
# Nhóm 6: ADVERSARIAL SEARCH (Minimax, Alpha-Beta, Expectimax)
# Bản đồ có nhiều ngã rẽ - môi trường có thể chặn đường
# Có nhiều đường đi thay thế để robot phản ứng
# ============================================================
ADVERSARIAL_MAP = [
    "S 0 0 0 0 1 0 0 0 0 0 0 0 0 0",
    "1 1 1 1 0 1 0 1 1 0 1 1 1 1 0",
    "0 0 0 0 0 0 0 0 1 0 0 0 0 0 0",
    "0 1 1 1 1 1 1 0 1 0 1 1 1 1 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 1 0",
    "0 1 0 1 1 1 1 1 1 1 1 1 0 1 0",
    "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 1 1 1 1 0 1 1 1 1 1 0 1 1 0",
    "0 0 0 0 0 0 0 0 0 0 1 0 0 0 0",
    "0 1 1 1 1 1 1 1 1 0 1 1 1 0 1",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 G",
]

# ============================================================
# MAPPING: Nhóm thuật toán → bản đồ tương ứng
# ============================================================
GROUP_MAPS = {
    "Tìm Kiếm Mù": UNINFORMED_MAP,
    "Có Thông Tin": INFORMED_MAP,
    "Tìm Cục Bộ": LOCAL_SEARCH_MAP,
    "Môi Trường Ẩn": COMPLEX_ENV_MAP,
    "Ràng Buộc CSP": CSP_MAP,
    "Tìm Đối Kháng": ADVERSARIAL_MAP,
}

# Bản đồ mặc định khi mở ứng dụng
DEFAULT_GROUP = "Tìm Kiếm Mù"


def parse_map_data(map_data):
    """
    Chuyển đổi dữ liệu bản đồ (list[str]) thành Grid object.
    
    Args:
        map_data (list[str]): Danh sách hàng dạng chuỗi.
        
    Returns:
        Grid: Đối tượng Grid đã khởi tạo.
    """
    rows_data = []
    for line in map_data:
        row = line.strip().split()
        rows_data.append(row)

    rows = len(rows_data)
    cols = len(rows_data[0]) if rows_data else 0

    grid = Grid(rows, cols)

    char_map = {
        '0': config.CELL_EMPTY,
        '1': config.CELL_WALL,
        'S': config.CELL_START,
        'G': config.CELL_GOAL,
        'W': config.CELL_WEIGHT,
        'F': config.CELL_FORBIDDEN,
    }

    for r, row_data in enumerate(rows_data):
        for c, val in enumerate(row_data):
            cell_type = char_map.get(val.upper(), config.CELL_EMPTY)
            grid.set_cell(r, c, cell_type)
            if cell_type == config.CELL_WEIGHT:
                grid.set_weight(r, c, config.HEAVY_WEIGHT)

    return grid


def load_preset(group_name):
    """
    Load bản đồ preset cho nhóm thuật toán.
    
    Args:
        group_name (str): Tên nhóm thuật toán.
        
    Returns:
        Grid: Bản đồ tương ứng, hoặc bản đồ mặc định nếu không tìm thấy.
    """
    map_data = GROUP_MAPS.get(group_name, GROUP_MAPS[DEFAULT_GROUP])
    return parse_map_data(map_data)
