"""
Module base: Class trừu tượng chung cho tất cả thuật toán tìm kiếm.
"""

from abc import ABC, abstractmethod
import time


class BaseAlgorithm(ABC):
    """
    Class trừu tượng chung cho tất cả thuật toán tìm kiếm.
    
    Mỗi thuật toán cụ thể kế thừa class này và override method solve().
    
    Attributes:
        problem (Problem): Bài toán cần giải.
        visited (list[tuple]): Danh sách các ô đã duyệt (theo thứ tự) — dùng cho animation.
        path (list[tuple]): Đường đi tìm được (start → goal).
        steps (int): Số node đã mở rộng (expanded).
        execution_time (float): Thời gian chạy thuật toán (giây).
        name (str): Tên thuật toán (hiển thị trên GUI).
    """

    def __init__(self, problem, name="Unknown"):
        self.problem = problem
        self.name = name
        self.visited = []           # Thứ tự các ô đã duyệt (để vẽ animation)
        self.path = []              # Đường đi kết quả
        self.steps = 0              # Số node mở rộng
        self.execution_time = 0.0   # Thời gian chạy (giây)

    @abstractmethod
    def solve(self):
        """
        Chạy thuật toán tìm đường.
        
        Returns:
            list[tuple[int, int]]: Đường đi [(row, col), ...] từ start → goal.
                                   Trả về list rỗng [] nếu không tìm được.
        
        Lưu ý:
            - Phải cập nhật self.visited theo thứ tự duyệt (dùng cho animation).
            - Phải cập nhật self.steps mỗi khi mở rộng node.
        """
        pass

    def run(self):
        """
        Chạy thuật toán và đo thời gian.
        
        Returns:
            list[tuple]: Đường đi tìm được.
        """
        start_time = time.time()
        self.path = self.solve()
        self.execution_time = time.time() - start_time
        return self.path

    def get_metrics(self):
        """
        Lấy thống kê hiệu suất thuật toán.
        
        Returns:
            dict: {
                'algorithm': str - Tên thuật toán,
                'path_length': int - Độ dài đường đi,
                'steps': int - Số node mở rộng,
                'visited_count': int - Số node đã duyệt,
                'execution_time': float - Thời gian (giây),
                'found': bool - Có tìm được đường không,
            }
        """
        return {
            'algorithm': self.name,
            'path_length': len(self.path) if self.path else 0,
            'steps': self.steps,
            'visited_count': len(self.visited),
            'execution_time': round(self.execution_time, 6),
            'found': bool(self.path) and len(self.path) > 0,
        }

    def reset(self):
        """Reset trạng thái thuật toán để chạy lại."""
        self.visited = []
        self.path = []
        self.steps = 0
        self.execution_time = 0.0

    def __repr__(self):
        metrics = self.get_metrics()
        return (f"{self.name}: found={metrics['found']}, "
                f"path_len={metrics['path_length']}, "
                f"steps={metrics['steps']}, "
                f"time={metrics['execution_time']}s")
