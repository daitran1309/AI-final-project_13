"""
Min-Conflicts Algorithm - Thuật toán giảm xung đột.

Đặc điểm:
    - Local search cho CSP: bắt đầu từ 1 lời giải ngẫu nhiên (có thể vi phạm ràng buộc).
    - Lặp: chọn biến vi phạm ràng buộc, gán giá trị giảm số xung đột nhất.
    - Không đảm bảo tìm được lời giải nhưng rất nhanh trong thực tế.
    - Thường dùng cho bài toán lớn.

Áp dụng cho tìm đường:
    - Tạo đường đi ban đầu hợp lệ (dùng random walk)
    - Sửa các vị trí vi phạm bằng cách chọn ô giảm conflicts nhất
"""

import random
from collections import deque
from algorithms.base import BaseAlgorithm
import config


class MinConflicts(BaseAlgorithm):
    """Thuật toán Min-Conflicts cho CSP."""

    def __init__(self, problem, max_iterations=2000):
        """
        Args:
            problem (Problem): Bài toán.
            max_iterations (int): Số vòng lặp tối đa.
        """
        super().__init__(problem, name="Min-Conflicts")
        self.max_iterations = max_iterations

    def solve(self):
        """
        Giải CSP bằng Min-Conflicts.
        
        Returns:
            list[tuple]: Đường đi hoặc [].
        """
        if not self.problem.is_valid():
            return []
            
        path = self._generate_initial_assignment()
        if not path:
            return []
            
        N = len(path)
        if N <= 1:
            return path
        
        # Nếu path ban đầu đã hợp lệ → trả luôn
        if self._is_valid_path(path):
            return path
            
        for iteration in range(self.max_iterations):
            # Tìm các index vi phạm ràng buộc
            conflicting_indices = []
            for i in range(1, N - 1):
                if self._count_conflicts(path, i) > 0:
                    conflicting_indices.append(i)
                    
            if not conflicting_indices:
                if self._is_valid_path(path):
                    return path
                break
                    
            # Chọn ngẫu nhiên 1 index vi phạm
            idx = random.choice(conflicting_indices)
            prev_pos = path[idx - 1]
            
            # Mở rộng candidates: neighbors của cả prev VÀ next
            candidates_set = set()
            for nb in self.problem.grid.get_neighbors(prev_pos[0], prev_pos[1]):
                if not self.problem.grid.is_forbidden(nb[0], nb[1]):
                    candidates_set.add(nb)
            
            if idx < N - 1:
                next_pos = path[idx + 1]
                for nb in self.problem.grid.get_neighbors(next_pos[0], next_pos[1]):
                    if not self.problem.grid.is_forbidden(nb[0], nb[1]):
                        candidates_set.add(nb)
            
            candidates = list(candidates_set)
            if not candidates:
                continue
                
            # Chọn candidate giảm conflicts nhất
            best_val = path[idx]
            min_conf = self._count_conflicts(path, idx, best_val)
            
            random.shuffle(candidates)
            for cand in candidates:
                conf = self._count_conflicts(path, idx, cand)
                if conf < min_conf:
                    min_conf = conf
                    best_val = cand
                    
            path[idx] = best_val
            self.visited.append(best_val)
            self.steps += 1
            
        # Kiểm tra kết quả cuối cùng
        if self._is_valid_path(path):
            return path
        return []

    def _is_valid_path(self, path):
        """Kiểm tra path có hợp lệ hoàn toàn không."""
        for i in range(len(path)):
            r, c = path[i]
            if not self.problem.grid.is_walkable(r, c):
                return False
            if self.problem.grid.is_forbidden(r, c):
                return False
            if i > 0:
                pr, pc = path[i - 1]
                if abs(r - pr) + abs(c - pc) != 1:
                    return False
        # Kiểm tra không trùng lặp
        if len(set(path)) != len(path):
            return False
        return True

    def _count_conflicts(self, path, index, val=None):
        """
        Đếm số ràng buộc bị vi phạm tại bước index.
        """
        if val is None:
            val = path[index]
            
        conflicts = 0
        r, c = val
        
        # Ràng buộc 1: phải nằm trong grid và đi được
        if not self.problem.grid.in_bounds(r, c):
            conflicts += 2
        else:
            if not self.problem.grid.is_walkable(r, c):
                conflicts += 2
            if self.problem.grid.is_forbidden(r, c):
                conflicts += 2
                
        # Ràng buộc 2: kề với bước trước
        if index > 0:
            pr, pc = path[index - 1]
            if abs(r - pr) + abs(c - pc) != 1:
                conflicts += 1
                
        # Ràng buộc 3: kề với bước sau
        if index < len(path) - 1:
            nr, nc = path[index + 1]
            if abs(r - nr) + abs(c - nc) != 1:
                conflicts += 1
                
        # Ràng buộc 4: không trùng lặp
        for i, p in enumerate(path):
            if i != index and p == val:
                conflicts += 1
                break
            
        return conflicts

    def _generate_initial_assignment(self):
        """
        Tạo đường đi ban đầu hợp lệ bằng random BFS.
        Nếu random BFS thất bại, dùng đường L-shaped cơ bản.
        """
        start_pos = self.problem.start
        goal_pos = self.problem.goal
        
        # Thử tạo path hợp lệ bằng random BFS
        path = self._random_bfs_path(start_pos, goal_pos)
        if path:
            return path
        
        # Fallback: đường L-shaped (có thể vi phạm)
        path = [start_pos]
        r, c = start_pos
        gr, gc = goal_pos
        
        while r != gr:
            r += 1 if gr > r else -1
            path.append((r, c))
        while c != gc:
            c += 1 if gc > c else -1
            path.append((r, c))
            
        return path

    def _random_bfs_path(self, start, goal):
        """
        Tìm đường đi hợp lệ bằng BFS với thứ tự ngẫu nhiên.
        Trả về path hoặc None nếu không tìm được.
        """
        queue = deque([(start, [start])])
        visited = {start}
        max_steps = config.CSP_MAX_STEPS
        
        while queue:
            pos, path = queue.popleft()
            
            if pos == goal:
                return path
                
            if len(path) > max_steps:
                continue
                
            neighbors = self.problem.grid.get_neighbors(pos[0], pos[1])
            # Lọc forbidden zones
            neighbors = [n for n in neighbors if not self.problem.grid.is_forbidden(n[0], n[1])]
            random.shuffle(neighbors)  # Random để tạo path đa dạng
            
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, path + [nb]))
                    
        return None
