"""
Searching for Partially Observable Problems - Tìm kiếm với quan sát một phần.

Đặc điểm:
    - Robot biết bản đồ nhưng KHÔNG CHẮC CHẮN vị trí chính xác.
    - Robot có cảm biến (sensor) phát hiện vật cản trong tầm nhất định.
    - Sau mỗi bước, cảm biến cung cấp observation → thu hẹp belief state.
    - Dùng Greedy search trên belief state.

Mô hình:
    - State: frozenset các vị trí khả dĩ (belief state)
    - Action: di chuyển 1 hướng
    - Observation: thông tin cảm biến (vật cản xung quanh)
    - Transition: áp dụng action → lọc belief state theo observation
    - Goal test: belief state chỉ chứa goal position
"""

import heapq
import config
from algorithms.base import BaseAlgorithm
from core.grid import Grid
from utils.helpers import manhattan_distance


class PartiallyObservableSearch(BaseAlgorithm):
    """Thuật toán tìm kiếm với quan sát một phần (Partially Observable)."""

    def __init__(self, problem):
        super().__init__(problem, name="Partially Observable (Greedy)")

    def solve(self):
        """
        Tìm đường trên belief state với cảm biến (Greedy).

        Returns:
            list[tuple]: Chuỗi tọa độ path từ start → goal.
        """
        grid = self.problem.grid
        start_pos = self.problem.start
        goal_pos = self.problem.goal

        if not self.problem.is_valid():
            return []

        initial_belief = []
        for r in range(grid.rows):
            for c in range(grid.cols):
                if grid.is_walkable(r, c):
                    initial_belief.append((r, c))

        # Lọc belief state ban đầu bằng observation tại start
        start_obs = self._get_observation(start_pos, grid)
        initial_belief = self._filter_belief_by_observation(frozenset(initial_belief), start_obs, grid)

        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        heap = []
        counter = 0
        h = self._belief_heuristic(initial_belief, goal_pos)
        heapq.heappush(heap, (h, counter, (initial_belief, start_pos, [])))

        visited_beliefs = {initial_belief}
        found_actions = None

        max_iterations = grid.rows * grid.cols * 100
        
        while heap:
            if self.steps >= max_iterations:
                break
            _, _, (current_belief, actual_pos, action_path) = heapq.heappop(heap)
            self.steps += 1
            self.visited.append(actual_pos)

            if len(current_belief) == 1 and goal_pos in current_belief:
                found_actions = action_path
                break

            for action in actions:
                next_belief_unfiltered = frozenset(
                    self._apply_action(pos, action, grid) for pos in current_belief
                )
                next_actual_pos = self._apply_action(actual_pos, action, grid)
                obs = self._get_observation(next_actual_pos, grid)
                next_belief = self._filter_belief_by_observation(next_belief_unfiltered, obs, grid)

                if next_belief and next_belief not in visited_beliefs:
                    visited_beliefs.add(next_belief)
                    h_val = self._belief_heuristic(next_belief, goal_pos)
                    counter += 1
                    heapq.heappush(heap, (h_val, counter, (next_belief, next_actual_pos, action_path + [action])))

        if found_actions is None:
            return []

        coordinate_path = [start_pos]
        curr = start_pos
        for act in found_actions:
            curr = self._apply_action(curr, act, grid)
            coordinate_path.append(curr)

        return coordinate_path

    def _apply_action(self, position, action, grid):
        row, col = position
        dr, dc = action
        nr, nc = row + dr, col + dc
        if grid.is_walkable(nr, nc):
            return (nr, nc)
        return (row, col)

    def _get_observation(self, position, grid):
        """
        Lấy observation (dữ liệu cảm biến) tại 1 vị trí dựa trên cấu hình hệ thống.
        """
        row, col = position
        obs = []

        # Đọc tầm xa cảm biến từ file cấu hình config
        sensor_range = getattr(config, 'SENSOR_RANGE', 2)
        cell_wall = getattr(config, 'CELL_WALL', 1)

        r_range = range(-sensor_range, sensor_range + 1)
        for dr in r_range:
            for dc in r_range:
                # Kiểm tra bán kính Manhattan của tầm quét cảm biến
                if abs(dr) + abs(dc) <= sensor_range:
                    nr, nc = row + dr, col + dc
                    # Nếu ô vượt biên hoặc gặp tường thì ghi nhận vào observation
                    if not grid.in_bounds(nr, nc) or grid.get_cell(nr, nc) == cell_wall:
                        obs.append((dr, dc))
        return frozenset(obs)

    def _filter_belief_by_observation(self, belief_state, observation, grid):
        """
        Lọc belief state: chỉ giữ vị trí có observation trùng khớp.
        """
        filtered = []
        for pos in belief_state:
            if self._get_observation(pos, grid) == observation:
                filtered.append(pos)
        return frozenset(filtered)

    def _belief_heuristic(self, belief_state, goal):
        """
        Heuristic cho belief state: min Manhattan distance đến goal.
        """
        if not belief_state:
            return float('inf')
        return min(manhattan_distance(pos, goal) for pos in belief_state)
