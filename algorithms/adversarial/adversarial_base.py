"""
Adversarial Base - Class cơ sở chung cho các thuật toán đối kháng.

Chứa các method dùng chung: đánh giá trạng thái, lấy actions của robot và môi trường.
Hỗ trợ tường tạm thời (biến mất sau N lượt) để cân bằng game.
"""

from algorithms.base import BaseAlgorithm
from utils.helpers import manhattan_distance
import config


class AdversarialBase(BaseAlgorithm):
    """Class cơ sở cho các thuật toán đối kháng (Minimax, Alpha-Beta, Expectimax)."""

    def __init__(self, problem, name, max_depth=None):
        super().__init__(problem, name=name)
        self.max_depth = max_depth or config.ADVERSARIAL_MAX_DEPTH
        self.total_walls_placed = 0  # Tổng số tường đã đặt
        self.max_walls = config.ADVERSARIAL_MAX_WALLS  # Giới hạn tổng tường
        self.wall_lifetime = config.ADVERSARIAL_WALL_LIFETIME  # Số lượt tường tồn tại
        # Danh sách tường tạm: [(row, col, remaining_turns), ...]
        self.temp_walls = []
        self.game_history = []  # Lưu lịch sử vị trí tường qua mỗi bước

    def _evaluate(self, state):
        """Hàm đánh giá trạng thái: +100 nếu đến goal, ngược lại trả -Manhattan distance."""
        pos = state['robot_pos']
        goal = self.problem.goal
        if pos == goal:
            return 100.0
        return -float(manhattan_distance(pos, goal))

    def _get_robot_actions(self, state):
        """Lấy danh sách nước đi hợp lệ của robot (các ô kề đi được)."""
        pos = state['robot_pos']
        grid = state['grid']
        return grid.get_neighbors(pos[0], pos[1])

    def _get_env_actions(self, state):
        """
        Lấy danh sách nước đi của môi trường (đặt vật cản).
        
        Chọn các ô trống trong bán kính 3 quanh robot, nhưng bảo vệ
        ô gần robot (distance <= 2) để robot không bị nhốt ngay.
        Giới hạn số lượng theo ADVERSARIAL_NUM_OBSTACLES.
        """
        # Nếu đã đạt giới hạn tổng tường → không đặt thêm
        if self.total_walls_placed >= self.max_walls:
            return []
            
        r, c = state['robot_pos']
        grid = state['grid']
        
        candidates = []
        for dr in range(-3, 4):
            for dc in range(-3, 4):
                if dr == 0 and dc == 0:
                    continue
                dist = abs(dr) + abs(dc)
                # Chỉ đặt tường ở distance > 1 (cho phép đặt sát robot hơn, giảm vùng an toàn)
                if dist <= 1:
                    continue
                nr, nc = r + dr, c + dc
                if grid.in_bounds(nr, nc):
                    if grid.get_cell(nr, nc) == config.CELL_EMPTY:
                        if (nr, nc) != self.problem.goal and (nr, nc) != self.problem.start:
                            candidates.append((nr, nc))
        candidates.sort(key=lambda p: manhattan_distance(p, (r, c)))
        return candidates[:config.ADVERSARIAL_NUM_OBSTACLES]

    def _place_wall(self, grid, pos):
        """Đặt tường tạm thời và theo dõi lifetime."""
        grid.set_cell(pos[0], pos[1], config.CELL_WALL)
        self.temp_walls.append((pos[0], pos[1], self.wall_lifetime))
        self.total_walls_placed += 1

    def _decay_walls(self, grid):
        """Giảm lifetime tường tạm. Xóa tường hết hạn."""
        new_walls = []
        for r, c, remaining in self.temp_walls:
            if remaining <= 1:
                # Tường hết hạn → xóa
                grid.set_cell(r, c, config.CELL_EMPTY)
                self.total_walls_placed -= 1
            else:
                new_walls.append((r, c, remaining - 1))
        self.temp_walls = new_walls
