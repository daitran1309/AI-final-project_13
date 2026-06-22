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
    - Tường tạm thời: biến mất sau N lượt để robot có cơ hội đến goal.
    - Env chỉ hành động mỗi 2 lượt (cooldown) để cân bằng.
"""

from algorithms.adversarial.adversarial_base import AdversarialBase
import config


class Minimax(AdversarialBase):
    """Thuật toán Minimax cho bài toán đối kháng."""

    def __init__(self, problem, max_depth=None):
        super().__init__(problem, name="Minimax", max_depth=max_depth)

    def solve(self):
        """Chạy Minimax để tìm đường đi tốt nhất chống lại môi trường."""
        if not self.problem.is_valid():
            return []

        current_grid = self.problem.grid.copy()
        current_pos = self.problem.start

        path = [current_pos]
        self.visited.append(current_pos)
        visited_set = {current_pos}  # Theo dõi vị trí đã đi qua để tránh lặp

        limit = 200
        step = 0
        stuck_count = 0  # Đếm số lần robot không tiến được

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
                next_state = {'robot_pos': action, 'grid': current_grid}
                val = self._minimax(next_state, 1, False)
                # Ưu tiên ô chưa đi qua
                if action not in visited_set:
                    val += 0.1
                if val > best_val:
                    best_val = val
                    best_action = action

            if best_action is None:
                break

            # Kiểm tra robot có tiến được không
            prev_pos = current_pos
            current_pos = best_action
            path.append(current_pos)
            self.visited.append(current_pos)
            visited_set.add(current_pos)

            if current_pos == prev_pos:
                stuck_count += 1
                if stuck_count > 5:
                    break  # Thoát nếu bị stuck quá lâu
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
                        self._place_wall(current_grid, best_env_action)

        # Trả path (có thể partial)
        if len(path) > 1:
            return path
        return []

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
