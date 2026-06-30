"""
Simple Hill Climbing - Leo đồi đơn giản.

Đặc điểm:
    - Chọn neighbor ĐẦU TIÊN tốt hơn trạng thái hiện tại.
    - Không so sánh tất cả neighbors, chọn ngay khi tìm được cải thiện.
    - Có thể bị kẹt ở local minimum.

    - Cho phép sideways move (đi ngang khi h bằng nhau) để vượt plateau.
"""

from algorithms.base import BaseAlgorithm
from core.node import Node
from utils.helpers import euclidean_distance


class SimpleHillClimbing(BaseAlgorithm):
    """Thuật toán Simple Hill Climbing (Leo đồi đơn giản)."""

    def __init__(self, problem, max_sideways=50, max_worse_moves=100):
        super().__init__(problem, name="Simple Hill Climbing")
        self.max_sideways = max_sideways  # Giới hạn sideways move liên tiếp
        self.max_worse_moves = max_worse_moves  # Giới hạn bước đi xấu hơn liên tiếp khi bị kẹt tường

    def solve(self):
        """
        Chạy Simple Hill Climbing.

        Returns:
            list[tuple]: Đường đi tìm được hoặc partial path nếu bị kẹt.
        """
        if not self.problem.is_valid():
            return []

        start_pos = self.problem.start
        goal_pos = self.problem.goal

        current_h = euclidean_distance(start_pos, goal_pos)
        current_node = Node(start_pos[0], start_pos[1], cost=0, heuristic=current_h)

        visited_set = {start_pos}  # Tránh vòng lặp
        self.visited.append(start_pos)
        self.steps += 1

        if self.problem.is_goal(start_pos):
            return [start_pos]

        sideways_count = 0  # Đếm số sideways move liên tiếp
        worse_count = 0     # Đếm số bước đi lùi/rẽ hướng xấu hơn liên tiếp

        while True:
            pos = current_node.position
            found_better = False
            for next_pos, cost in self.problem.get_successors(pos):
                if next_pos in visited_set:
                    continue
                next_h = euclidean_distance(next_pos, goal_pos)
                # Cho phép sideways move (<=) nhưng giới hạn số lần liên tiếp
                if next_h < current_h or (next_h == current_h and sideways_count < self.max_sideways):
                    if next_h == current_h:
                        sideways_count += 1
                    else:
                        sideways_count = 0  # Reset khi tìm được cải thiện thực sự
                    worse_count = 0  # Reset khi tìm thấy bước tốt
                    current_h = next_h
                    current_node = Node(next_pos[0], next_pos[1], cost=current_node.cost + cost, heuristic=next_h, parent=current_node)
                    visited_set.add(next_pos)
                    self.visited.append(next_pos)
                    self.steps += 1
                    found_better = True
                    break

            if not found_better:
                # Fallback: Nếu gặp tường (không có ô kề nào tốt hơn hoặc bằng),
                # bỏ qua hướng bị chặn, chấp nhận đi hướng khác (rẽ) dù h xấu hơn
                if worse_count < self.max_worse_moves:
                    for next_pos, cost in self.problem.get_successors(pos):
                        if next_pos in visited_set:
                            continue
                        # Chọn ngay hướng rẽ chưa đi qua đầu tiên
                        next_h = euclidean_distance(next_pos, goal_pos)
                        worse_count += 1
                        sideways_count = 0
                        current_h = next_h
                        current_node = Node(next_pos[0], next_pos[1], cost=current_node.cost + cost, heuristic=next_h, parent=current_node)
                        visited_set.add(next_pos)
                        self.visited.append(next_pos)
                        self.steps += 1
                        found_better = True
                        break

            if not found_better:
                break

            if self.problem.is_goal(current_node.position):
                return [n.position for n in current_node.trace_path()]

        # Trả partial path thay vì [] để hiển thị nơi bị kẹt
        return [n.position for n in current_node.trace_path()]
