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
            
        path = [start_pos]
        path_set = {start_pos}
        self.visited.append(start_pos)
        self.steps += 1
        
        def backtrack():
            if self.problem.is_goal(path[-1]):
                return list(path)
                
            last_pos = path[-1]
            neighbors = self.problem.grid.get_neighbors(last_pos[0], last_pos[1])
            
            # Forward checking: lọc các neighbor hợp lệ cho bước đi tiếp theo
            valid_neighbors = []
            for neighbor in neighbors:
                if self._is_consistent(neighbor, path_set):
                    if self.problem.is_goal(neighbor):
                        valid_neighbors.append(neighbor)
                        continue
                    # Check future domain: thêm neighbor tạm vào path_set để kiểm tra
                    path_set.add(neighbor)
                    future_neighbors = self.problem.grid.get_neighbors(neighbor[0], neighbor[1])
                    has_future_domain = any(
                        self._is_consistent(f_nb, path_set) for f_nb in future_neighbors
                    )
                    path_set.discard(neighbor)
                    if has_future_domain:
                        valid_neighbors.append(neighbor)
                    
            # Nếu không có nước đi tiếp theo hợp lệ nào (domain trống) → quay lui ngay (Prune)
            if not valid_neighbors:
                return None
                
            for neighbor in valid_neighbors:
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
        Lưu ý: in_bounds và is_walkable đã được lọc bởi grid.get_neighbors().
        Chỉ cần kiểm tra vùng cấm và trùng lặp.
        """
        if self.problem.grid.is_forbidden(position[0], position[1]):
            return False
        if position in path_set:
            return False
        return True
