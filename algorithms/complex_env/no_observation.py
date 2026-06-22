"""
Searching with No Observation (Sensorless Search) - Tìm kiếm không quan sát.

Đặc điểm:
    - Robot biết bản đồ nhưng KHÔNG biết vị trí hiện tại của mình.
    - Duy trì belief state = tập hợp tất cả vị trí khả dĩ.
    - Mục tiêu: tìm chuỗi actions sao cho bất kể robot ở đâu, cuối cùng sẽ đến goal.
    - Tìm kiếm trên không gian belief state (BFS/DFS).
    - Một action áp dụng cho TẤT CẢ vị trí trong belief state.

Mô hình:
    - State: frozenset các vị trí khả dĩ (belief state)
    - Action: di chuyển 1 hướng (UP, DOWN, LEFT, RIGHT)
    - Transition: áp dụng action cho tất cả vị trí trong belief state
      (nếu vị trí không đi được theo hướng đó → giữ nguyên)
    - Goal test: belief state chỉ chứa goal position
"""

import heapq
from collections import deque
from algorithms.base import BaseAlgorithm
from core.grid import Grid
from utils.helpers import manhattan_distance


class NoObservationSearch(BaseAlgorithm):
    """Thuật toán tìm kiếm không quan sát (Sensorless) trên belief state."""

    def __init__(self, problem, method="bfs"):
        """
        Args:
            problem (Problem): Bài toán.
            method (str): Phương pháp tìm kiếm trên belief space: 'bfs' hoặc 'dfs'.
        """
        name = f"No Observation ({method.upper()})"
        super().__init__(problem, name=name)
        self.method = method

    def solve(self):
        """
        Tìm chuỗi actions trên không gian belief state.
        
        Returns:
            list[tuple]: Chuỗi tọa độ path từ start → goal.
        """
        grid = self.problem.grid
        start_pos = self.problem.start
        goal_pos = self.problem.goal
        
        if not self.problem.is_valid():
            return []
            
        # Khởi tạo belief state ban đầu là tất cả các ô đi được
        initial_belief = []
        for r in range(grid.rows):
            for c in range(grid.cols):
                if grid.is_walkable(r, c):
                    initial_belief.append((r, c))
        initial_belief = frozenset(initial_belief)
        
        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # UP, DOWN, LEFT, RIGHT
        
        # Tăng max_iterations đáng kể để đủ cho belief state space
        max_iterations = 50000
        
        # Sử dụng heuristic-guided search (Greedy) để tìm nhanh hơn
        # Heuristic: ưu tiên belief state nhỏ (ít vị trí khả dĩ hơn)
        # + khoảng cách trung bình đến goal
        counter = 0
        h = self._belief_heuristic(initial_belief, goal_pos)
        
        if self.method == "bfs":
            # BFS với heuristic (trở thành Greedy best-first search trên belief space)
            heap = [(h, counter, (initial_belief, []))]
            use_heap = True
        else:
            # DFS vẫn dùng stack
            queue = [(initial_belief, [])]
            use_heap = False
            
        visited_beliefs = {initial_belief}
        found_actions = None
        
        while (heap if use_heap else queue):
            if self.steps >= max_iterations:
                break
            self.steps += 1
            
            if use_heap:
                _, _, (current_belief, action_path) = heapq.heappop(heap)
            else:
                current_belief, action_path = queue.pop()
            
            # Thêm một vị trí đại diện vào visited để GUI hiển thị animation
            if current_belief:
                # Chọn vị trí gần goal nhất trong belief để visualize
                representative = min(current_belief, 
                                     key=lambda p: manhattan_distance(p, goal_pos))
                if representative not in set(self.visited):
                    self.visited.append(representative)
                
            if len(current_belief) == 1 and goal_pos in current_belief:
                found_actions = action_path
                break
                
            for action in actions:
                next_belief = self._apply_action_to_belief(current_belief, action, grid)
                if next_belief not in visited_beliefs:
                    visited_beliefs.add(next_belief)
                    if use_heap:
                        counter += 1
                        h_val = self._belief_heuristic(next_belief, goal_pos)
                        heapq.heappush(heap, (h_val, counter, (next_belief, action_path + [action])))
                    else:
                        queue.append((next_belief, action_path + [action]))
                        
        if found_actions is None:
            return []
            
        # Mô phỏng từ start để lấy tọa độ di chuyển
        coordinate_path = [start_pos]
        curr = start_pos
        for act in found_actions:
            curr = self._apply_action(curr, act, grid)
            coordinate_path.append(curr)
            
        return coordinate_path

    def _apply_action(self, position, action, grid):
        """
        Áp dụng action cho 1 vị trí.
        Nếu không đi được → giữ nguyên vị trí.
        """
        row, col = position
        dr, dc = action
        nr, nc = row + dr, col + dc
        if grid.is_walkable(nr, nc):
            return (nr, nc)
        return (row, col)

    def _apply_action_to_belief(self, belief_state, action, grid):
        """
        Áp dụng action cho TẤT CẢ vị trí trong belief state.
        """
        return frozenset(self._apply_action(pos, action, grid) for pos in belief_state)

    def _belief_heuristic(self, belief_state, goal):
        """
        Heuristic cho belief state:
        Ưu tiên belief nhỏ hơn (ít vị trí → gần xác định được vị trí)
        + min distance đến goal.
        """
        if not belief_state:
            return float('inf')
        # Kết hợp: kích thước belief state + khoảng cách tối thiểu đến goal
        min_dist = min(manhattan_distance(pos, goal) for pos in belief_state)
        return len(belief_state) * 2 + min_dist
