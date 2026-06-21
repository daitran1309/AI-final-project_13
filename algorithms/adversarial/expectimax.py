"""
Expectimax Algorithm - Thuật toán Expectimax.

Đặc điểm:
    - Biến thể Minimax cho đối thủ NGẪU NHIÊN (không tối ưu).
    - MAX player = Robot (chọn nước đi tốt nhất).
    - CHANCE player = Môi trường (hành động ngẫu nhiên với xác suất).
    - CHANCE node: tính giá trị kỳ vọng (expected value) thay vì min.
    
    Áp dụng: Môi trường thêm vật cản ngẫu nhiên (không chủ đích cản robot),
    ví dụ: kẹt xe ngẫu nhiên, thời tiết xấu bất ngờ.
    
    So sánh:
    - Minimax: đối thủ chọn nước đi TỆ NHẤT cho ta (pessimistic).
    - Expectimax: đối thủ chọn NGẪU NHIÊN (realistic hơn).
"""

from algorithms.base import BaseAlgorithm
from utils.helpers import manhattan_distance
import config


class Expectimax(BaseAlgorithm):
    """Thuật toán Expectimax."""

    def __init__(self, problem, max_depth=None):
        super().__init__(problem, name="Expectimax")
        self.max_depth = max_depth or config.ADVERSARIAL_MAX_DEPTH

    def solve(self):
        """Chạy Expectimax."""
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

            for action in robot_actions:
                next_state = {'robot_pos': action, 'grid': current_grid}
                val = self._expectimax(next_state, 1, False)
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
            if env_actions:
                import random
                chosen_action = random.choice(env_actions)
                current_grid.set_cell(chosen_action[0], chosen_action[1], config.CELL_WALL)

        return path

    def _expectimax(self, state, depth, is_maximizing):
        """Hàm đệ quy Expectimax (Không copy grid)."""
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
                val = self._expectimax(next_state, depth + 1, False)
                max_val = max(max_val, val)
            return max_val
        else:
            actions = self._get_env_actions(state)
            if not actions:
                next_state = {'robot_pos': pos, 'grid': grid}
                return self._expectimax(next_state, depth + 1, True)
            total_val = 0.0
            for action in actions:
                # Kỹ thuật Backtracking: Tạm thời thêm tường -> Tính toán kỳ vọng -> Hoàn tác
                grid.set_cell(action[0], action[1], config.CELL_WALL)
                next_state = {'robot_pos': pos, 'grid': grid}

                val = self._expectimax(next_state, depth + 1, True)

                grid.set_cell(action[0], action[1], config.CELL_EMPTY)
                total_val += val
            return total_val / len(actions)

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