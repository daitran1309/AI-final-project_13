"""
CSP Solver (Backtracking) - Giải CSP bằng quay lui.

Mô hình CSP cho bài toán tìm đường:
    - Variables: X_0, X_1, ..., X_n (mỗi bước đi trên đường)
      X_0 = start, X_n = goal
    - Domain: Mỗi X_i có domain = các ô walkable trên grid
    - Constraints:
      1. X_0 = start, X_n = goal
      2. X_i và X_{i+1} phải kề nhau (4 hướng) — ràng buộc liên tục
      3. X_i không nằm trong vùng cấm (forbidden zones)
      4. Tổng số bước <= max_steps (giới hạn)
      5. Không lặp lại (X_i != X_j nếu i != j) — tùy chọn

Đặc điểm:
    - Backtracking: thử từng giá trị cho biến, quay lui nếu vi phạm ràng buộc.
    - Cơ bản nhất, không có tối ưu.
"""

from algorithms.base import BaseAlgorithm
import config


class CSPSolver(BaseAlgorithm):
    """Thuật toán CSP Backtracking cơ bản."""

    def __init__(self, problem):
        super().__init__(problem, name="CSP Backtracking")

    def solve(self):
        """
        Giải bài toán tìm đường dạng CSP bằng Backtracking.
        
        Returns:
            list[tuple]: Đường đi [(row, col), ...] hoặc [] nếu không tìm được.
        """
        if not self.problem.is_valid():
            return []
            
        start_pos = self.problem.start
            
        path = [start_pos]
        path_set = {start_pos}
        self.visited.append(start_pos)
        self.steps += 1
        
        def backtrack():
            if self.problem.is_goal(path[-1]):
                return list(path)
                
            last_pos = path[-1]
            for neighbor in self.problem.grid.get_neighbors(last_pos[0], last_pos[1]):
                if self._is_consistent(neighbor, path_set):
                    self.visited.append(neighbor)
                    self.steps += 1
                    path.append(neighbor)
                    path_set.add(neighbor)
                    res = backtrack()
                    if res is not None:
                        return res
                    path.pop()
                    path_set.discard(neighbor)
                    self.visited.append((neighbor[0], neighbor[1], 'remove'))
            return None
            
        res = backtrack()
        return res or []

    def _is_consistent(self, position, path_set):
        """
        Kiểm tra position có thỏa mãn tất cả ràng buộc không.
        
        Lưu ý: in_bounds và is_walkable đã được lọc bởi grid.get_neighbors().
        Chỉ cần kiểm tra vùng cấm và trùng lặp.
        """
        if self.problem.grid.is_forbidden(position[0], position[1]):
            return False
        if position in path_set:
            return False
        return True
