"""
Steepest Ascent Hill Climbing - Leo đồi dốc nhất.

Đặc điểm:
    - So sánh TẤT CẢ neighbors, chọn neighbor TỐT NHẤT.
    - Tốt hơn Simple Hill Climbing vì xét toàn bộ lân cận.
    - Vẫn có thể bị kẹt ở local minimum.
    - Hàm đánh giá: h(n) = Manhattan distance đến goal.
    - Cho phép sideways move (đi ngang khi h bằng nhau) để vượt plateau.
"""

from algorithms.base import BaseAlgorithm
from core.node import Node
from utils.helpers import manhattan_distance


class SteepestHillClimbing(BaseAlgorithm):
    """Thuật toán Steepest Ascent Hill Climbing (Leo đồi dốc nhất)."""

    def __init__(self, problem, max_sideways=50):
        super().__init__(problem, name="Steepest Hill Climbing")
        self.max_sideways = max_sideways  # Giới hạn sideways move liên tiếp

    def solve(self):
        """
        Chạy Steepest Ascent Hill Climbing.

        Returns:
            list[tuple]: Đường đi tìm được hoặc partial path nếu bị kẹt.
        """
        if not self.problem.is_valid():
            return []

        start_pos = self.problem.start
        goal_pos = self.problem.goal

        current_h = manhattan_distance(start_pos, goal_pos)
        current_node = Node(start_pos[0], start_pos[1], cost=0, heuristic=current_h)

        visited_set = {start_pos}  # Tránh vòng lặp
        self.visited.append(start_pos)
        self.steps += 1

        if self.problem.is_goal(start_pos):
            return [start_pos]

        sideways_count = 0  # Đếm số sideways move liên tiếp

        while True:
            pos = current_node.position
            best_neighbor = None
            best_h = current_h
            best_cost = 0
            is_sideways = False

            for next_pos, cost in self.problem.get_successors(pos):
                if next_pos in visited_set:
                    continue
                next_h = manhattan_distance(next_pos, goal_pos)
                if next_h < best_h:
                    best_h = next_h
                    best_neighbor = next_pos
                    best_cost = cost
                    is_sideways = False
                elif next_h == best_h and best_neighbor is None and sideways_count < self.max_sideways:
                    # Sideways move: chọn nếu chưa tìm được cải thiện
                    best_neighbor = next_pos
                    best_cost = cost
                    is_sideways = True

            if best_neighbor is None:
                break

            if is_sideways:
                sideways_count += 1
            else:
                sideways_count = 0  # Reset khi tìm được cải thiện thực sự

            current_h = best_h
            current_node = Node(best_neighbor[0], best_neighbor[1], cost=current_node.cost + best_cost, heuristic=best_h, parent=current_node)
            visited_set.add(best_neighbor)
            self.visited.append(best_neighbor)
            self.steps += 1

            if self.problem.is_goal(best_neighbor):
                return [n.position for n in current_node.trace_path()]

        # Trả partial path thay vì [] để hiển thị nơi bị kẹt
        return [n.position for n in current_node.trace_path()]
