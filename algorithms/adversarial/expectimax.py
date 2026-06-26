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
    - Tường tạm thời + env cooldown để cân bằng.
"""

from algorithms.adversarial.adversarial_base import AdversarialBase
import config
import random


class Expectimax(AdversarialBase):
    """Thuật toán Expectimax."""

    def __init__(self, problem, max_depth=None):
        super().__init__(problem, name="Expectimax", max_depth=max_depth)

    def solve(self):
        """Chạy Expectimax."""
        if not self.problem.is_valid():
            return []

        current_grid = self.problem.grid.copy()
        current_pos = self.problem.start

        path = [current_pos]
        self.visited.append(current_pos)
        visited_set = {current_pos}

        limit = 200
        step = 0
        stuck_count = 0

        # Lưu trạng thái ban đầu
        self.game_history.append([(r, c) for r, c, _ in self.temp_walls])

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
                if action not in visited_set:
                    val += 0.1
                if val > best_val:
                    best_val = val
                    best_action = action

            if best_action is None:
                break

            prev_pos = current_pos
            current_pos = best_action
            path.append(current_pos)
            self.visited.append(current_pos)
            visited_set.add(current_pos)

            if current_pos == prev_pos:
                stuck_count += 1
                if stuck_count > 5:
                    break
            else:
                stuck_count = 0

            if current_pos == self.problem.goal:
                break

            # Giảm lifetime tường tạm trước lượt env
            self._decay_walls(current_grid)

            # Env chỉ hành động mỗi 2 lượt (cooldown)
            if step % 2 == 0:
                state = {'robot_pos': current_pos, 'grid': current_grid}
                env_actions = self._get_env_actions(state)
                if env_actions:
                    chosen_action = random.choice(env_actions)
                    self._place_wall(current_grid, chosen_action)

            # Lưu lại trạng thái tường sau lượt này
            self.game_history.append([(r, c) for r, c, _ in self.temp_walls])

        # Trả path (có thể partial)
        if len(path) > 1:
            return path
        return []

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