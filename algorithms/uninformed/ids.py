"""
Iterative Deepening Search (IDS) - Tìm kiếm sâu dần.

Đặc điểm:
    - Kết hợp ưu điểm BFS (đầy đủ, tối ưu) và DFS (bộ nhớ thấp).
    - Chạy DFS giới hạn độ sâu, tăng dần depth limit.
    - Đảm bảo tìm đường ngắn nhất (theo số bước).
    - Độ phức tạp: O(b^d) thời gian, O(bd) bộ nhớ.
"""

from algorithms.base import BaseAlgorithm
from core.node import Node


class IDS(BaseAlgorithm):
    """Thuật toán Iterative Deepening Search."""

    def __init__(self, problem):
        super().__init__(problem, name="IDS")

    def solve(self):
        """
        Chạy IDS tìm đường từ start → goal.
        
        Returns:
            list[tuple]: Đường đi [(row, col), ...] hoặc [] nếu không tìm được.
        """
        if not self.problem.is_valid():
            return []
            
        depth_limit = 0
        max_depth = self.problem.grid.rows * self.problem.grid.cols

        while depth_limit <= max_depth:
            result = self._depth_limited_search(depth_limit)
            if result != 'cutoff':
                if result is None:
                    return []
                return result
            depth_limit += 1
        
        return []

    def _depth_limited_search(self, limit):
        """
        DFS giới hạn độ sâu.
        
        Args:
            limit (int): Giới hạn độ sâu.
            
        Returns:
            list[tuple] | 'cutoff' | None:
                - list[tuple]: Đường đi nếu tìm được goal.
                - 'cutoff': Nếu có node bị cắt do giới hạn.
                - None: Nếu không có lời giải trong giới hạn.
        """
        start_pos = self.problem.start
        start_node = Node(start_pos[0], start_pos[1])
        path_set = set()
        
        def dls(node, depth):
            pos = node.position
            self.visited.append(pos)
            self.steps += 1
            
            if self.problem.is_goal(pos):
                return [n.position for n in node.trace_path()]
            
            if depth >= limit:
                return 'cutoff'
                
            path_set.add(pos)
            any_cutoff = False
            
            for next_pos, cost in self.problem.get_successors(pos):
                if next_pos not in path_set:
                    child = Node(next_pos[0], next_pos[1], cost=node.cost + cost, parent=node)
                    result = dls(child, depth + 1)
                    if result == 'cutoff':
                        any_cutoff = True
                    elif result is not None:
                        return result
            
            path_set.remove(pos)
            return 'cutoff' if any_cutoff else None

        return dls(start_node, 0)
