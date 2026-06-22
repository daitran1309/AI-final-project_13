"""
Alpha-Beta Pruning - Cắt tỉa Alpha-Beta.

Đặc điểm:
    - Tối ưu hóa Minimax bằng cách cắt bỏ các nhánh không cần thiết.
    - Alpha = giá trị tốt nhất MAX đã tìm được (lower bound).
    - Beta = giá trị tốt nhất MIN đã tìm được (upper bound).
    - Nếu alpha >= beta → cắt tỉa (prune) nhánh đó.
    - Kết quả giống hệt Minimax nhưng nhanh hơn nhiều.
    - Best case: O(b^(d/2)) thay vì O(b^d).
    - Tường tạm thời: biến mất sau N lượt để robot có cơ hội đến goal.
    - Env chỉ hành động mỗi 2 lượt (cooldown) để cân bằng.
"""

from algorithms.adversarial.adversarial_base import AdversarialBase
import config


class AlphaBeta(AdversarialBase):
    """Thuật toán Alpha-Beta Pruning."""

    def __init__(self, problem, max_depth=None):
        super().__init__(problem, name="Alpha-Beta", max_depth=max_depth)
        self.pruned_count = 0  # Đếm số nhánh bị cắt tỉa

    def solve(self):
        """Chạy Alpha-Beta Pruning."""
        if not self.problem.is_valid():
            return []

        current_grid = self.problem.grid.copy()
        current_pos = self.problem.start

        path = [current_pos]
        self.visited.append(current_pos)
        visited_set = {current_pos}  # Theo dõi vị trí đã đi qua

        limit = 200
        step = 0
        stuck_count = 0

        while current_pos != self.problem.goal and step < limit:
            step += 1
            state = {'robot_pos': current_pos, 'grid': current_grid}
            robot_actions = self._get_robot_actions(state)
            if not robot_actions:
                break

            best_action = None
            best_val = -float('inf')

            # Khởi tạo alpha/beta cho vòng lặp gốc của Robot (MAX)
            alpha = -float('inf')
            beta = float('inf')

            for action in robot_actions:
                next_state = {'robot_pos': action, 'grid': current_grid}
                val = self._alpha_beta(next_state, 1, alpha, beta, False)
                # Ưu tiên ô chưa đi qua
                if action not in visited_set:
                    val += 0.1
                if val > best_val:
                    best_val = val
                    best_action = action
                alpha = max(alpha, best_val)

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
                    best_env_action = None
                    best_env_val = float('inf')

                    alpha = -float('inf')
                    beta = float('inf')

                    for action in env_actions:
                        current_grid.set_cell(action[0], action[1], config.CELL_WALL)
                        next_state = {'robot_pos': current_pos, 'grid': current_grid}

                        val = self._alpha_beta(next_state, 1, alpha, beta, True)

                        current_grid.set_cell(action[0], action[1], config.CELL_EMPTY)

                        if val < best_env_val:
                            best_env_val = val
                            best_env_action = action
                        beta = min(beta, best_env_val)

                    if best_env_action:
                        self._place_wall(current_grid, best_env_action)

        # Trả path (có thể partial)
        if len(path) > 1:
            return path
        return []

    def _alpha_beta(self, state, depth, alpha, beta, is_maximizing):
        """Hàm đệ quy Alpha-Beta (Không sao chép ma trận)."""
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
                val = self._alpha_beta(next_state, depth + 1, alpha, beta, False)
                max_val = max(max_val, val)
                alpha = max(alpha, val)
                if alpha >= beta:
                    self.pruned_count += 1
                    break
            return max_val
        else:
            actions = self._get_env_actions(state)
            if not actions:
                next_state = {'robot_pos': pos, 'grid': grid}
                return self._alpha_beta(next_state, depth + 1, alpha, beta, True)
            min_val = float('inf')
            for action in actions:
                # Kỹ thuật Backtracking & Undo
                grid.set_cell(action[0], action[1], config.CELL_WALL)
                next_state = {'robot_pos': pos, 'grid': grid}

                val = self._alpha_beta(next_state, depth + 1, alpha, beta, True)

                grid.set_cell(action[0], action[1], config.CELL_EMPTY)
                min_val = min(min_val, val)
                beta = min(beta, val)
                if alpha >= beta:
                    self.pruned_count += 1
                    break
            return min_val

    def get_metrics(self):
        metrics = super().get_metrics()
        metrics['pruned_branches'] = self.pruned_count
        return metrics
