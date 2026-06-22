"""
Adversarial Base - Class cơ sở chung cho các thuật toán đối kháng.

Chứa các method dùng chung: đánh giá trạng thái, lấy actions của robot và môi trường.
"""

from algorithms.base import BaseAlgorithm
from utils.helpers import manhattan_distance
import config


class AdversarialBase(BaseAlgorithm):
    """Class cơ sở cho các thuật toán đối kháng (Minimax, Alpha-Beta, Expectimax)."""

    def __init__(self, problem, name, max_depth=None):
        super().__init__(problem, name=name)
        self.max_depth = max_depth or config.ADVERSARIAL_MAX_DEPTH

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
        
        Chọn các ô trống trong bán kính 2 quanh robot, sắp xếp theo khoảng cách,
        giới hạn số lượng theo cấu hình ADVERSARIAL_NUM_OBSTACLES.
        """
        r, c = state['robot_pos']
        grid = state['grid']
        candidates = []
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if grid.in_bounds(nr, nc):
                    if grid.get_cell(nr, nc) == config.CELL_EMPTY and (nr, nc) != self.problem.goal:
                        candidates.append((nr, nc))
        candidates.sort(key=lambda p: manhattan_distance(p, (r, c)))
        return candidates[:config.ADVERSARIAL_NUM_OBSTACLES]
