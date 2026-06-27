import pygame
from gui.theme import UITheme
import config

class BenchmarkUI:
    """Component hiển thị bảng so sánh (Benchmark) dưới dạng Popup (Modal)."""

    def __init__(self, surface):
        self.surface = surface
        self.font_title = UITheme.font(24, bold=True)
        self.font_header = UITheme.font(14, bold=True)
        self.font_row = UITheme.font(13)
        self.scroll_y = 0
        self.close_rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, results):
        """
        Vẽ bảng xếp hạng.
        results: list các dict chứa metrics của từng thuật toán.
        """
        # Làm tối màn hình nền (Overlay)
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.surface.blit(overlay, (0, 0))

        # Kích thước popup
        width = 800
        height = 450
        x = (self.surface.get_width() - width) // 2
        y = (self.surface.get_height() - height) // 2
        
        rect = pygame.Rect(x, y, width, height)
        
        # Vẽ thẻ trắng (Card)
        pygame.draw.rect(self.surface, UITheme.BG_WHITE, rect, border_radius=12)
        pygame.draw.rect(self.surface, UITheme.BORDER, rect, width=2, border_radius=12)

        # Tiêu đề
        title_surf = self.font_title.render("BẢNG SO SÁNH THUẬT TOÁN", True, UITheme.TEXT_MAIN)
        self.surface.blit(title_surf, (x + (width - title_surf.get_width())//2, y + 20))

        # Nếu không có kết quả
        if not results:
            msg = self.font_row.render("Đang chạy hoặc không có dữ liệu...", True, UITheme.TEXT_LIGHT)
            self.surface.blit(msg, (x + 20, y + 80))
            return

        # Sắp xếp kết quả: Tốt nhất lên đầu. 
        # Tiêu chí: Thời gian chạy (càng nhỏ càng tốt), sau đó là số bước (càng ngắn càng tốt)
        sorted_results = sorted(results, key=lambda r: (not r['found'], r['execution_time'], r['path_length']))

        # Tọa độ cột
        col_x = [x + 30, x + 230, x + 400, x + 530, x + 650]
        headers = ["Tên Thuật Toán", "Nhóm", "Độ dài đường", "Số ô duyệt", "Thời gian (ms)"]

        # Vẽ Header
        hy = y + 80
        pygame.draw.rect(self.surface, UITheme.BG_LIGHT, (x + 20, hy - 5, width - 40, 30), border_radius=6)
        for i, header in enumerate(headers):
            h_surf = self.font_header.render(header, True, UITheme.TEXT_MAIN)
            self.surface.blit(h_surf, (col_x[i], hy))

        # Vùng danh sách (Clipping)
        list_rect = pygame.Rect(x + 20, hy + 35, width - 40, height - 180)
        self.surface.set_clip(list_rect)

        # Vẽ các hàng (Rows)
        ry = hy + 40 - self.scroll_y
        for idx, res in enumerate(sorted_results):
            # Chỉ vẽ nếu nằm trong list_rect
            if ry + 30 > list_rect.top and ry < list_rect.bottom:
                # Highlight hàng top 1 (Màu vàng nhạt)
                if idx == 0 and res['found']:
                    pygame.draw.rect(self.surface, (255, 250, 205), (x + 20, ry - 5, width - 40, 30), border_radius=6)
                
                # Tên
                name_color = UITheme.TEXT_MAIN if res['found'] else UITheme.BTN_RESET
                name_surf = self.font_row.render(res['algorithm'], True, name_color)
                self.surface.blit(name_surf, (col_x[0], ry))

                # Nhóm
                group_surf = self.font_row.render(res.get('group', 'Unknown'), True, UITheme.TEXT_LIGHT)
                self.surface.blit(group_surf, (col_x[1], ry))

                # Độ dài
                path_str = str(res['path_length']) if res['found'] else "Thất bại"
                path_surf = self.font_row.render(path_str, True, UITheme.TEXT_MAIN)
                self.surface.blit(path_surf, (col_x[2], ry))

                # Số ô duyệt
                visited_surf = self.font_row.render(str(res['visited_count']), True, UITheme.TEXT_MAIN)
                self.surface.blit(visited_surf, (col_x[3], ry))

                # Thời gian (Quy đổi ra ms)
                time_ms = res['execution_time'] * 1000
                time_str = f"{time_ms:.2f} ms"
                time_surf = self.font_row.render(time_str, True, UITheme.PRIMARY)
                self.surface.blit(time_surf, (col_x[4], ry))

            ry += 30

        self.surface.set_clip(None) # Reset clip

        # Nút ĐÓNG
        btn_width = 120
        btn_height = 36
        self.close_rect = pygame.Rect(x + (width - btn_width)//2, y + height - 55, btn_width, btn_height)
        pygame.draw.rect(self.surface, UITheme.BTN_RESET, self.close_rect, border_radius=6)
        
        close_surf = self.font_header.render("ĐÓNG", True, UITheme.TEXT_WHITE)
        self.surface.blit(close_surf, (self.close_rect.centerx - close_surf.get_width()//2, self.close_rect.centery - close_surf.get_height()//2))
        
        # Hướng dẫn cuộn
        hint_surf = self.font_row.render("Sử dụng con lăn chuột để cuộn danh sách", True, UITheme.TEXT_LIGHT)
        self.surface.blit(hint_surf, (x + (width - hint_surf.get_width())//2, y + height - 85))
