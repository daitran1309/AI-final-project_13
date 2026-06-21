# 🤖 Project Context cho AI Agent (Antigravity)

Chào AI Agent! Khi bạn được yêu cầu làm việc với dự án này, hãy đọc kỹ toàn bộ file này. Đây là file lưu trữ ngữ cảnh (context), trạng thái dự án, kiến trúc và định hướng tiếp theo. 

**Quy tắc:** Bất cứ khi nào bạn (Agent) hoàn thành một tính năng lớn hoặc thay đổi kiến trúc, hãy tự động cập nhật lại file này để các Agent ở phiên làm việc sau (hoặc trên máy khác) có thể hiểu được dự án đang ở giai đoạn nào.

---

## 1. Tổng quan dự án (Project Overview)
- **Tên dự án**: Robot Giao Hàng - AI Search Algorithms.
- **Mục tiêu**: Xây dựng một ứng dụng Python sử dụng thư viện `pygame` để mô phỏng trực quan các thuật toán tìm kiếm trong Trí tuệ nhân tạo (AI). Ứng dụng giải quyết bài toán tìm đường cho robot giao hàng trên một không gian lưới (Grid 2D).
- **Ngôn ngữ & Thư viện**: Python 3.8+, Pygame 2.5.0+.
- **Ngôn ngữ giao tiếp (Prompting & Comment)**: Ưu tiên dùng **tiếng Việt** cho code comment, docstring và commit messages.

## 2. Kiến trúc hệ thống (Architecture)
Dự án được chia thành các module độc lập:
- **`core/`**: Cốt lõi hệ thống. `Grid` (Môi trường lưới 2D), `Node` (Đỉnh đồ thị tìm kiếm), `Problem` (Định nghĩa bài toán theo chuẩn AI), `Robot` (Quản lý vị trí, hành động của agent).
- **`algorithms/`**: Triển khai logic thuật toán. Các thuật toán kế thừa từ một `BaseAlgorithm` chung. Gồm 6 nhóm chính:
  - `uninformed/`: Tìm kiếm mù (BFS, DFS, IDS).
  - `informed/`: Tìm kiếm kinh nghiệm (A*, Greedy, UCS).
  - `local_search/`: Tìm kiếm cục bộ (Hill Climbing, Local Beam).
  - `adversarial/`: Tìm kiếm đối kháng (Minimax, Alpha-beta, Expectimax).
  - `csp/`: Thỏa mãn ràng buộc (Backtracking, Forward Checking).
  - `complex_env/`: Môi trường phức tạp (Partially Observable).
- **`gui/`**: Xử lý giao diện bằng Pygame theo phong cách Clean & Modern Minimalist. `app.py` là controller chính, `renderer.py` lo việc vẽ lưới và hiệu ứng animation (fade-in, pulse), `sidebar.py` chứa toàn bộ UI dạng Card, `theme.py` định nghĩa màu sắc/font, và `components.py` chứa các widget dùng chung (Button, PillToggleGroup).
- **`maps/`**: Quản lý bản đồ, chứa `presets.py` phân bổ map chuyên dụng cho từng nhóm thuật toán để minh hoạ trực quan điểm mạnh/yếu của chúng.
- **`utils/`**: Các file tiện ích `helpers.py` và `metrics.py` (đo đạc thời gian, memory, số lượng node đã mở rộng).

## 3. Trạng thái hiện tại (Current State)
- **Hoàn thiện 100% Logic Thuật Toán**: Đã tích hợp đầy đủ 6 nhóm thuật toán AI (Mù, Heuristic, Cục bộ, Môi trường ẩn, CSP, Đối kháng).
- **Giao diện (UI/UX)**: Đã thiết kế lại toàn bộ UI theo phong cách **Clean & Modern Minimalist (Light Theme)**. Hỗ trợ responsive (co giãn lưới tự động), sử dụng hệ font Segoe UI sắc nét, Việt hoá 100%.
- **Tính năng mở rộng**: 
  - Animation mượt mà bằng cơ chế Queue (không block UI).
  - Thống kê thông số (Thời gian, Độ dài đường đi, Bộ nhớ) theo thời gian thực (Real-time update) ngay trong lúc đang vẽ animation.
  - Tích hợp công cụ vẽ bản đồ chuyên nghiệp (Tường, Đầm lầy, Vùng cấm, Điểm bắt đầu, Đích) kèm Tooltips (Ghi chú động) giải thích trực tiếp trên màn hình.
  - Tính năng sinh Mê cung ngẫu nhiên (Random Maze).

## 4. Công việc tiếp theo (TODO / Roadmap)
*(Tất cả công việc nền tảng đã hoàn tất)*

- [x] Cài đặt chi tiết logic của BaseAlgorithm và kết nối nó vào luồng của `gui/app.py`.
- [x] Xử lý thuật toán tìm kiếm mù (BFS, DFS, IDS): Trả về từng step để `gui/renderer.py` vẽ hiệu ứng animation thay vì chỉ vẽ kết quả cuối cùng.
- [x] Cài đặt hệ thống ghi nhận metrics (thời gian chạy, số node sinh ra, số bước đi) và hiển thị lên Sidebar khi thuật toán chạy xong (đã nâng cấp thành Real-time).
- [x] Thêm logic tương tác cho phép người dùng dùng chuột vẽ chướng ngại vật (wall) và kéo thả điểm Start / Goal.
- [x] Hoàn thiện các nhóm thuật toán còn lại (Informed, Local Search, Adversarial...).
- [x] Nâng cấp UI/UX: Light Theme, Việt hóa, Tooltips, Random Maze, Scale Grid.

## 5. Quy tắc dành cho Agent (AI Guidelines)
1. **Tránh Block UI**: Vì dùng Pygame, các thuật toán không được phép dùng vòng lặp `while/for` chặn event loop. Khuyến khích sử dụng generator `yield` trạng thái ở mỗi bước lặp của thuật toán, hoặc chạy thuật toán ở luồng (thread) riêng để `app.py` update UI mượt mà.
2. **Type Hinting**: Code mới sinh ra cần tuân thủ Type Hinting của Python.
3. **Mở rộng dễ dàng**: Khi thêm tính năng mới, hãy tuân thủ nguyên tắc SOLID. Tránh hardcode trong `gui/app.py`, hãy truyền data qua cấu trúc `config.py` hoặc các biến môi trường.
