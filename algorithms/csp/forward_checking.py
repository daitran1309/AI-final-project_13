"""
CSP + Forward Checking - CSP với kiểm tra trước.

Đặc điểm:
    - Mở rộng Backtracking: sau khi gán giá trị cho biến X_i,
      loại bỏ ngay các giá trị không hợp lệ từ domain của biến chưa gán.
    - Phát hiện thất bại sớm hơn (nếu domain nào trống → quay lui ngay).
    - Giảm đáng kể số node cần duyệt.
"""

from algorithms.base import BaseAlgorithm
import config


class ForwardCheckingCSP(BaseAlgorithm):
    """Thuật toán CSP + Forward Checking."""

    def __init__(self, problem):
        super().__init__(problem, name="Forward Checking CSP")

    def solve(self):
        """
        Giải CSP bằng Backtracking + Forward Checking.
        
        Returns:
            list[tuple]: Đường đi hoặc [].
        """
        if not self.problem.is_valid():
            return []
            
        start_pos = self.problem.start
        max_steps = self.problem.get_max_steps()
        if max_steps == float('inf'):
            max_steps = config.CSP_MAX_STEPS
            
        path = [start_pos]
        self.visited.append(start_pos)
        self.steps += 1
        
        def backtrack(current_path):
            current_node = current_path[-1]

            if self.problem.is_goal(current_path[-1]):
                return current_path
                
            if len(current_path) > max_steps:
                return None
                
            last_pos = current_path[-1]
            neighbors = self.problem.grid.get_neighbors(last_pos[0], last_pos[1])
            
            # Forward checking: lọc các neighbor hợp lệ cho bước đi tiếp theo
            valid_neighbors = []
            for neighbor in neighbors:
                if self._is_consistent(neighbor, current_path):
                    if self.problem.is_goal(neighbor):
                        valid_neighbors.append(neighbor)
                        continue
                    future_path = current_path + [neighbor]
                    future_neighbors = self.problem.grid.get_neighbors(neighbor[0], neighbor[1])
                    has_future_domain = any(
                        self._is_consistent(f_nb, future_path) for f_nb in future_neighbors
                    )
                    if has_future_domain:
                        valid_neighbors.append(neighbor)
                    
            # Nếu không có nước đi tiếp theo hợp lệ nào (domain trống) → quay lui ngay (Prune)
            if not valid_neighbors:
                return None
                
            for neighbor in valid_neighbors:
                self.visited.append(neighbor)
                self.steps += 1
                res = backtrack(current_path + [neighbor])
                if res is not None:
                    return res
            return None
            
        res = backtrack(path)
        return res or []

    def _is_consistent(self, position, path):
        row, col = position
        if not self.problem.grid.in_bounds(row, col):
            return False
        if not self.problem.grid.is_walkable(row, col):
            return False
        if self.problem.grid.is_forbidden(row, col):
            return False
        if position in path:
            return False
        return True
