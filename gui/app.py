"""
Module app: Ứng dụng chính Pygame - Clean & Modern UI.
"""

import pygame
import sys
import random
import config
from core.grid import Grid
from core.problem import Problem
from gui.renderer import Renderer
from gui.sidebar import Sidebar
from gui.benchmark import BenchmarkUI
from gui.theme import UITheme
from maps.presets import load_preset, DEFAULT_GROUP

# Import tất cả thuật toán
from algorithms.uninformed.bfs import BFS
from algorithms.uninformed.dfs import DFS
from algorithms.uninformed.ids import IDS
from algorithms.informed.ucs import UCS
from algorithms.informed.greedy import Greedy
from algorithms.informed.astar import AStar
from algorithms.local_search.simple_hill_climbing import SimpleHillClimbing
from algorithms.local_search.steepest_hill_climbing import SteepestHillClimbing
from algorithms.local_search.local_beam_search import LocalBeamSearch
from algorithms.complex_env.no_observation import NoObservationSearch
from algorithms.complex_env.partially_observable import PartiallyObservableSearch
from algorithms.csp.csp_solver import CSPSolver
from algorithms.csp.forward_checking import ForwardCheckingCSP
from algorithms.csp.min_conflicts import MinConflicts
from algorithms.adversarial.minimax import Minimax
from algorithms.adversarial.alpha_beta import AlphaBeta
from algorithms.adversarial.expectimax import Expectimax

ALGORITHM_MAP = {
    "BFS": BFS,
    "DFS": DFS,
    "IDS": IDS,
    "UCS": UCS,
    "Greedy": Greedy,
    "A*": AStar,
    "Simple Hill Climbing": SimpleHillClimbing,
    "Steepest Hill Climbing": SteepestHillClimbing,
    "Local Beam Search": LocalBeamSearch,
    "No Observation (BFS)": lambda p: NoObservationSearch(p, method="bfs"),
    "No Observation (DFS)": lambda p: NoObservationSearch(p, method="dfs"),
    "Partially Observable (Greedy)": PartiallyObservableSearch,
    "CSP Backtracking": CSPSolver,
    "Forward Checking": ForwardCheckingCSP,
    "Min-Conflicts": MinConflicts,
    "Minimax": Minimax,
    "Alpha-Beta": AlphaBeta,
    "Expectimax": Expectimax,
}

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.TITLE)
        
        # Enable Resizing
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.current_group = DEFAULT_GROUP
        self.grid = load_preset(self.current_group)

        self.renderer = Renderer(self.screen)
        self.benchmark_ui = BenchmarkUI(self.screen)
        
        # Trạng thái so sánh
        self.show_benchmark = False
        self.benchmark_results = []
        
        self.sidebar = Sidebar(config.WINDOW_WIDTH - config.SIDEBAR_WIDTH, 0, config.SIDEBAR_WIDTH, config.WINDOW_HEIGHT)
        self.sidebar.selected_group = self.current_group
        self.sidebar.update_algo_buttons()

        self._update_layout(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.running = True
        self.is_animating = False
        self.is_animating_path = False
        self.animation_index = 0
        self.path_animation_index = 0
        self.last_animation_time = 0
        
        self.current_algorithm = None
        self.result_path = []
        self.visited_list = []
        self.is_drawing = False

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(config.FPS)
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Đóng popup benchmark nếu đang mở
            if self.show_benchmark:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.show_benchmark = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.benchmark_ui.close_rect.collidepoint(event.pos):
                        self.show_benchmark = False
                    elif event.button == 4: # Scroll up
                        self.benchmark_ui.scroll_y = max(0, self.benchmark_ui.scroll_y - 40)
                    elif event.button == 5: # Scroll down
                        # Tối đa scroll là số lượng item * 30 trừ đi chiều cao vùng hiển thị
                        max_scroll = max(0, len(self.benchmark_results) * 30 - 250)
                        self.benchmark_ui.scroll_y = min(max_scroll, self.benchmark_ui.scroll_y + 40)
                continue

            if event.type == pygame.VIDEORESIZE:
                self._update_layout(event.w, event.h)
                continue

            action = self.sidebar.handle_event(event)
            if action:
                self._handle_sidebar_action(action)
                continue

            if event.type == pygame.MOUSEMOTION:
                self.renderer.update_hover(event.pos, self.grid)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Chỉ vẽ nếu click trong grid
                if event.pos[0] < self.sidebar.x:
                    self.is_drawing = True
                    self._handle_grid_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_drawing = False
            elif event.type == pygame.MOUSEMOTION and self.is_drawing:
                if event.pos[0] < self.sidebar.x:
                    self._handle_grid_click(event.pos)

    def _update_layout(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        sb_width = config.SIDEBAR_WIDTH
        sb_x = width - sb_width
        self.sidebar.set_position(sb_x, 0, height)
        
        # Grid area is 70% roughly (or whatever is left)
        available_width = sb_x - 2 * config.GRID_OFFSET_X
        available_height = height - 2 * config.GRID_OFFSET_Y
        if available_width > 0 and available_height > 0:
            cell_w = available_width // self.grid.cols
            cell_h = available_height // self.grid.rows
            self.renderer.cell_size = min(cell_w, cell_h, 50)
            
            # Center grid
            actual_grid_w = self.renderer.cell_size * self.grid.cols
            actual_grid_h = self.renderer.cell_size * self.grid.rows
            self.renderer.offset_x = (sb_x - actual_grid_w) // 2
            self.renderer.offset_y = (height - actual_grid_h) // 2

    def _handle_sidebar_action(self, action):
        if action['type'] == 'run':
            self._run_algorithm()
        elif action['type'] == 'benchmark':
            self._run_benchmark()
        elif action['type'] == 'reset':
            self._reset()
        elif action['type'] == 'random_maze':
            self._generate_random_maze()
        elif action['type'] == 'select_group':
            self._load_group_map(action['group'])
        elif action['type'] == 'select_algorithm':
            self._clear_animation()
        elif action['type'] == 'speed_change':
            self.renderer.animation_speed = action['speed']
            self.sidebar.animation_speed = action['speed']

    def _handle_grid_click(self, mouse_pos):
        cell = self.renderer.get_cell_at_mouse(mouse_pos, self.grid)
        if cell is None: return
        row, col = cell
        mode = self.sidebar.draw_mode
        if mode == "wall": self.grid.set_cell(row, col, config.CELL_WALL)
        elif mode == "start": self.grid.set_cell(row, col, config.CELL_START)
        elif mode == "goal": self.grid.set_cell(row, col, config.CELL_GOAL)
        elif mode == "weight": 
            self.grid.set_cell(row, col, config.CELL_WEIGHT)
            self.grid.set_weight(row, col, config.HEAVY_WEIGHT)
        elif mode == "forbid": self.grid.set_cell(row, col, config.CELL_FORBIDDEN)
        elif mode == "erase": 
            self.grid.set_cell(row, col, config.CELL_EMPTY)
            self.grid.set_weight(row, col, config.DEFAULT_WEIGHT)

    def _generate_random_maze(self):
        # Giữ nguyên Start/Goal, xoá các ô còn lại
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                if self.grid.cells[r][c] not in [config.CELL_START, config.CELL_GOAL]:
                    self.grid.set_cell(r, c, config.CELL_EMPTY)
                    
        # Khởi tạo các toà nhà 2x2 ngẫu nhiên cách nhau bởi đường phố
        # Bắt đầu từ 2 và kết thúc ở cols-2 để chừa ít nhất 1 ô trống quanh viền map, tránh tạo ngõ cụt.
        for r in range(2, self.grid.rows - 2, 3):
            for c in range(2, self.grid.cols - 2, 4):
                if random.random() < 0.7:  # 70% xác suất xây toà nhà tại vị trí này
                    for dr in range(2):
                        for dc in range(2):
                            nr, nc = r + dr, c + dc
                            if self.grid.in_bounds(nr, nc) and self.grid.cells[nr][nc] not in [config.CELL_START, config.CELL_GOAL]:
                                self.grid.set_cell(nr, nc, config.CELL_WALL)
                                
        self._clear_animation()

    def _run_algorithm(self):
        algo_name = self.sidebar.selected_algorithm
        if algo_name is None: return
        if self.grid.start is None or self.grid.goal is None: return

        problem = Problem(self.grid)
        if not problem.is_valid(): return

        algo_class = ALGORITHM_MAP.get(algo_name)
        if algo_class is None: return

        self._clear_animation()

        algorithm = algo_class(problem)
        result = algorithm.run()

        self.current_algorithm = algorithm
        self.result_path = result or []
        self.visited_list = algorithm.visited
        
        # Save full metrics for final
        self.final_metrics = algorithm.get_metrics()
        
        # Setup animation
        if self.visited_list:
            self.is_animating = True
            self.animation_index = 0
            self.last_animation_time = pygame.time.get_ticks()
        elif self.result_path:
            self.is_animating_path = True
            self.path_animation_index = 0
            self.last_animation_time = pygame.time.get_ticks()
        else:
            self.sidebar.metrics = self.final_metrics

    def _run_benchmark(self):
        if self.grid.start is None or self.grid.goal is None: return

        problem = Problem(self.grid)
        if not problem.is_valid(): return

        self._clear_animation()
        self.benchmark_results = []
        # Lấy danh sách TOÀN BỘ thuật toán của TẤT CẢ các nhóm
        
        for group_name, group_algos in config.ALGORITHM_GROUPS.items():
            for algo_name in group_algos:
                algo_class = ALGORITHM_MAP.get(algo_name)
                if algo_class:
                    # Dùng bản sao của problem/grid để tránh thuật toán sửa trực tiếp
                    prob_copy = Problem(self.grid.copy())
                    algo = algo_class(prob_copy)
                    algo.run()
                    metrics = algo.get_metrics()
                    metrics['group'] = group_name
                    self.benchmark_results.append(metrics)
                
        self.show_benchmark = True

    def _load_group_map(self, group_name):
        self.current_group = group_name
        self.grid = load_preset(group_name)
        self._update_layout(self.screen.get_width(), self.screen.get_height())
        self._clear_animation()

    def _clear_animation(self):
        self.is_animating = False
        self.is_animating_path = False
        self.animation_index = 0
        self.path_animation_index = 0
        self.current_algorithm = None
        self.result_path = []
        self.visited_list = []
        self.sidebar.metrics = None
        self.final_metrics = None

    def _reset(self):
        self.grid = load_preset(self.current_group)
        self._update_layout(self.screen.get_width(), self.screen.get_height())
        self._clear_animation()

    def _update(self):
        current_time = pygame.time.get_ticks()
        
        if self.is_animating:
            if current_time - self.last_animation_time >= self.sidebar.animation_speed:
                self.animation_index += 1
                self.last_animation_time = current_time
                if self.animation_index >= len(self.visited_list):
                    self.is_animating = False
                    if self.result_path:
                        self.is_animating_path = True
                        self.path_animation_index = 0
                    else:
                        self.sidebar.metrics = self.final_metrics
            
            # Real-time metrics update
            if self.final_metrics:
                ratio = self.animation_index / max(1, len(self.visited_list))
                self.sidebar.metrics = {
                    'steps': int(self.final_metrics['steps'] * ratio),
                    'path_length': 0,
                    'execution_time': self.final_metrics['execution_time'] * ratio,
                    'visited_count': self.animation_index
                }
                
        elif self.is_animating_path:
            path_speed = 30 # Cố định tốc độ path trace 30ms theo yêu cầu
            if current_time - self.last_animation_time >= path_speed:
                self.path_animation_index += 1
                self.last_animation_time = current_time
                if self.path_animation_index >= len(self.result_path):
                    self.is_animating_path = False
                    self.sidebar.metrics = self.final_metrics
            
            if self.final_metrics:
                self.sidebar.metrics = {
                    'steps': self.final_metrics['steps'],
                    'path_length': self.path_animation_index,
                    'execution_time': self.final_metrics['execution_time'],
                    'visited_count': self.final_metrics['visited_count']
                }

    def _draw(self):
        self.screen.fill(UITheme.BG_LIGHT)

        # 1. Grid
        self.renderer.draw_grid(self.grid)
        
        # 2. Visited
        if self.visited_list:
            count = self.animation_index if self.is_animating else len(self.visited_list)
            self.renderer.draw_visited(self.visited_list, count)
            
            # Vẽ tường động đồng bộ với animation
            if hasattr(self.current_algorithm, 'game_history') and self.current_algorithm.game_history:
                # Đảm bảo index hợp lệ
                idx = min(count - 1, len(self.current_algorithm.game_history) - 1)
                if idx >= 0:
                    self.renderer.draw_dynamic_walls(self.current_algorithm.game_history[idx])
            
        # 3. Path
        if self.result_path and not self.is_animating:
            count = self.path_animation_index if self.is_animating_path else len(self.result_path)
            self.renderer.draw_path(self.result_path, count)

        # 4. Start/Goal
        self.renderer.draw_start_goal(self.grid)
        
        # 5. Sidebar
        self.sidebar.draw(self.screen)

        # 6. Benchmark Modal Overlay (Nếu bật)
        if self.show_benchmark:
            self.benchmark_ui.draw(self.benchmark_results)

        pygame.display.flip()

if __name__ == "__main__":
    app = App()
    app.run()
