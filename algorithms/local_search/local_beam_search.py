"""
Local Beam Search - Tìm kiếm chùm cục bộ.

Đặc điểm:
    - Duy trì k trạng thái song song (thay vì 1 như Hill Climbing).
    - Mỗi bước: sinh tất cả successors của k trạng thái, chọn k tốt nhất.
    - Giảm nguy cơ bị kẹt local minimum nhờ đa dạng trạng thái.
    - k = 1 → tương đương Steepest Hill Climbing.
"""

from algorithms.base import BaseAlgorithm
from core.node import Node
from utils.helpers import manhattan_distance


class LocalBeamSearch(BaseAlgorithm):
    """Thuật toán Local Beam Search."""

    def __init__(self, problem, k=3):
        """
        Args:
            problem (Problem): Bài toán.
            k (int): Số lượng trạng thái duy trì song song.
        """
        super().__init__(problem, name="Local Beam Search")
        self.k = k  # Số beam (trạng thái song song)

    def solve(self):
        """
        Chạy Local Beam Search với k beams.
        
        Returns:
            list[tuple]: Đường đi tìm được hoặc [] nếu thất bại.
        """
        if not self.problem.is_valid():
            return []
            
        start_pos = self.problem.start
        goal_pos = self.problem.goal
        
        start_h = manhattan_distance(start_pos, goal_pos)
        start_node = Node(start_pos[0], start_pos[1], cost=0, heuristic=start_h)
        
        beams = [start_node]
        self.visited.append(start_pos)
        self.steps += 1
        
        if self.problem.is_goal(start_pos):
            return [start_pos]
            
        visited_set = {start_pos}
        
        while True:
            successors = []
            for node in beams:
                pos = node.position
                for next_pos, cost in self.problem.get_successors(pos):
                    if next_pos not in visited_set:
                        next_h = manhattan_distance(next_pos, goal_pos)
                        child = Node(next_pos[0], next_pos[1], cost=node.cost + cost, heuristic=next_h, parent=node)
                        successors.append(child)
            
            if not successors:
                break
                
            for child in successors:
                if self.problem.is_goal(child.position):
                    self.visited.append(child.position)
                    self.steps += 1
                    return [n.position for n in child.trace_path()]
                    
            successors.sort(key=lambda node: node.heuristic)
            next_beams = successors[:self.k]
            
            # best_curr_h = min(node.heuristic for node in beams)
            # best_next_h = next_beams[0].heuristic
            #
            # Nếu giữ nguyên check này, Beam Search sẽ dừng khi h tăng (giống hệt Hill Climbing)
            # if best_next_h >= best_curr_h:
            #     break
                
            beams = next_beams
            for node in beams:
                visited_set.add(node.position)
                self.visited.append(node.position)
                self.steps += 1
                
        if beams:
            beams.sort(key=lambda node: node.heuristic)
            return [n.position for n in beams[0].trace_path()]
        return []
