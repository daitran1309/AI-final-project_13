"""
Minimax Algorithm - Thuật toán Minimax.

Mô hình đối kháng cho robot giao hàng:
    - MAX player = Robot: muốn đến Goal nhanh nhất (tối đa điểm)
    - MIN player = Môi trường: thêm vật cản cản đường robot (kẹt xe, thời tiết xấu)
    - Turn-based: Robot đi 1 bước → Môi trường thêm/thay đổi vật cản → Robot đi tiếp...
    
    Hàm đánh giá (utility):
    - Nếu robot đến goal: +100
    - Nếu hết depth: -(Manhattan distance đến goal)
    - Môi trường muốn minimize (làm robot xa goal nhất)

Đặc điểm:
    - Duyệt toàn bộ cây game đến depth limit.
    - Đảm bảo chọn nước đi tốt nhất trong trường hợp xấu nhất.
    - Độ phức tạp: O(b^d) — rất tốn kém.
"""

from algorithms.base import BaseAlgorithm
from utils.helpers import manhattan_distance
import config


class Minimax(BaseAlgorithm):
    """Thuật toán Minimax cho bài toán đối kháng."""

    def __init__(self, problem, max_depth=None):
        super().__init__(problem, name="Minimax")
        self.max_depth = max_depth or config.ADVERSARIAL_MAX_DEPTH

    def solve(self):
        """Chạy Minimax để tìm đường đi tốt nhất chống lại môi trường."""
        if not self.problem.is_valid():
            return []

        current_grid = self.problem.grid.copy()
        current_pos = self.problem.start

        path = [current_pos]
        self.visited.append(current_pos)

        limit = 100
        step = 0

        while current_pos != self.problem.goal and step < limit:
            step += 1
            state = {'robot_pos': current_pos, 'grid': current_grid}
            robot_actions = self._get_robot_actions(state)
            if not robot_actions:
                break

            best_action = None
            best_val = -float('inf')

            # Robot chọn nước đi tốt nhất (MAX)
            for action in robot_actions:
                # Robot di chuyển không làm thay đổi bản đồ -> Không cần sao chép grid
                next_state = {'robot_pos': action, 'grid': current_grid}
                val = self._minimax(next_state, 1, False)
                if val > best_val:
                    best_val = val
                    best_action = action

            if best_action is None:
                break

            current_pos = best_action
            path.append(current_pos)
            self.visited.append(current_pos)

            if current_pos == self.problem.goal:
                break

            state = {'robot_pos': current_pos, 'grid': current_grid}
            env_actions = self._get_env_actions(state)

            # Môi trường chọn nước đi cản trở nhất (MIN)
            if env_actions:
                best_env_action = None
                best_env_val = float('inf')
                for action in env_actions:
                    # Đặt tường tạm thời (Do)
                    current_grid.set_cell(action[0], action[1], config.CELL_WALL)
                    next_state = {'robot_pos': current_pos, 'grid': current_grid}

                    val = self._minimax(next_state, 1, True)

                    # Khôi phục trạng thái cũ (Undo)
                    current_grid.set_cell(action[0], action[1], config.CELL_EMPTY)

                    if val < best_env_val:
                        best_env_val = val
                        best_env_action = action

                if best_env_action:
                    current_grid.set_cell(best_env_action[0], best_env_action[1], config.CELL_WALL)

        return path

    def _minimax(self, state, depth, is_maximizing):
        """Hàm đệ quy Minimax (Không copy grid)."""
        self.steps += 1
        pos = state['robot_pos']
        grid = state['grid']

        if pos == self.problem.goal or depth >= self.max_depth:
            return self._evaluate(state)

        if is_maximizing:
            actions = self._get_robot_actions(state)
            if not actions:
                return -100.0
            max_val = -float('inf')
            for action in actions:
                next_state = {'robot_pos': action, 'grid': grid}
                val = self._minimax(next_state, depth + 1, False)
                max_val = max(max_val, val)
            return max_val
        else:
            actions = self._get_env_actions(state)
            if not actions:
                next_state = {'robot_pos': pos, 'grid': grid}
                return self._minimax(next_state, depth + 1, True)
            min_val = float('inf')
            for action in actions:
                # Kỹ thuật Backtracking: Đặt tường tạm thời -> Đệ quy -> Hoàn tác
                grid.set_cell(action[0], action[1], config.CELL_WALL)
                next_state = {'robot_pos': pos, 'grid': grid}

                val = self._minimax(next_state, depth + 1, True)

                grid.set_cell(action[0], action[1], config.CELL_EMPTY)
                min_val = min(min_val, val)
            return min_val

    def _evaluate(self, state):
        pos = state['robot_pos']
        goal = self.problem.goal
        if pos == goal:
            return 100.0
        return -float(manhattan_distance(pos, goal))

    def _get_robot_actions(self, state):
        pos = state['robot_pos']
        grid = state['grid']
        return grid.get_neighbors(pos[0], pos[1])

    def _get_env_actions(self, state):
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
        # Thay thế hardcode bằng cấu hình hệ thống
        return candidates[:config.ADVERSARIAL_NUM_OBSTACLES]