"""
Simple Hill Climbing - Leo đồi đơn giản.

Đặc điểm:
    - Chọn neighbor ĐẦU TIÊN tốt hơn trạng thái hiện tại.
    - Không so sánh tất cả neighbors, chọn ngay khi tìm được cải thiện.
    - Có thể bị kẹt ở local minimum.
    - Hàm đánh giá: h(n) = Manhattan distance đến goal (càng nhỏ càng tốt).
"""

from algorithms.base import BaseAlgorithm
from core.node import Node
from utils.helpers import manhattan_distance


class SimpleHillClimbing(BaseAlgorithm):
    """Thuật toán Simple Hill Climbing (Leo đồi đơn giản)."""

    def __init__(self, problem):
        super().__init__(problem, name="Simple Hill Climbing")

    def solve(self):
        """
        Chạy Simple Hill Climbing.
        
        Returns:
            list[tuple]: Đường đi tìm được hoặc [] nếu bị kẹt.
        """
        if not self.problem.is_valid():
            return []
            
        start_pos = self.problem.start
        goal_pos = self.problem.goal
        
        current_h = manhattan_distance(start_pos, goal_pos)
        current_node = Node(start_pos[0], start_pos[1], cost=0, heuristic=current_h)
        
        self.visited.append(start_pos)
        self.steps += 1
        
        if self.problem.is_goal(start_pos):
            return [start_pos]
            
        while True:
            pos = current_node.position
            found_better = False
            for next_pos, cost in self.problem.get_successors(pos):
                next_h = manhattan_distance(next_pos, goal_pos)
                if next_h < current_h:
                    current_h = next_h
                    current_node = Node(next_pos[0], next_pos[1], cost=current_node.cost + cost, heuristic=next_h, parent=current_node)
                    self.visited.append(next_pos)
                    self.steps += 1
                    found_better = True
                    break
            
            if not found_better:
                break
                
            if self.problem.is_goal(current_node.position):
                return [n.position for n in current_node.trace_path()]
                
        return []
