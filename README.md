# 🤖 Robot Giao Hàng - AI Search Algorithms

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.5.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Một ứng dụng minh họa trực quan các thuật toán tìm kiếm cơ bản và nâng cao trong Trí tuệ nhân tạo (AI). Ứng dụng mô phỏng bài toán tìm đường đi cho robot giao hàng trên lưới 2D, giúp người dùng dễ dàng quan sát cách các thuật toán hoạt động, duyệt không gian trạng thái và tìm ra giải pháp tối ưu.

Đặc biệt, dự án hỗ trợ minh hoạ các không gian phức tạp như **Trạng thái niềm tin (Belief State)** và **Tìm kiếm đối kháng (Adversarial Search)** một cách sinh động, trực quan nhất.

---

## ✨ Tính năng nổi bật

- **Giao diện Hiện đại (Clean & Modern Minimalist)**: Ứng dụng sở hữu Light Theme cao cấp, hỗ trợ tự động co giãn lưới (Responsive Layout) và font chữ Tiếng Việt sắc nét.
- **Công nghệ Arrow Path Rendering (Mới)**: Hệ thống render quỹ đạo thông minh (đặc biệt cho nhóm Môi trường ẩn) giúp hiển thị đồng thời nhiều quỹ đạo song song. Các mũi tên chỉ hướng được tách rời, có độ lệch tâm (offset) riêng và loại bỏ nền tảng, đảm bảo **100% không đè chéo nét vẽ**, giữ cho lưới bản đồ luôn trong vắt và dễ nhìn.
- **Mô phỏng Animation Mượt mà**: Quan sát trực tiếp từng bước thuật toán lan tỏa (Fade-in animation) và dò tìm đường đi bằng xung nhịp thị giác (Pulse animation).
- **Tương tác Thời gian thực (Real-time)**: 
  - Sidebar hiển thị sống động Thống kê thông số (Độ dài đường, node đã mở, thời gian, số lượng niềm tin) tự động cập nhật ngay trong lúc thuật toán tính toán ngầm.
  - Hỗ trợ công cụ vẽ trực quan: Kéo thả Start/Goal, vẽ Tường cứng, Đầm lầy, Vùng cấm chỉ bằng các click chuột đơn giản.
- **Tùy biến Cảm biến (Sensor)**: Chỉnh sửa trực tiếp bán kính cảm biến robot trong môi trường ẩn để làm "mờ mắt" robot, mô phỏng quá trình Localization trong thực tế.
- **Tạo Mê Cung Ngẫu Nhiên**: Tính năng sinh chướng ngại vật ngẫu nhiên chỉ bằng một nút bấm.

---

## 🧠 Hệ thống thuật toán AI

Dự án này bao quát 6 nhóm thuật toán cốt lõi trong giáo trình Trí tuệ nhân tạo, tự động đổi bản đồ chuyên dụng để người dùng thấy rõ nhất đặc tính của từng nhóm:

| Nhóm thuật toán | Các thuật toán được cài đặt |
|-----------------|-----------------------------|
| **Tìm Kiếm Mù** (Uninformed Search) | BFS, DFS, IDS (Iterative Deepening Search) |
| **Có Thông Tin** (Informed Search) | UCS (Uniform-Cost), Greedy Best-First, A* (A-Star) |
| **Tìm Cục Bộ** (Local Search) | Simple Hill Climbing, Steepest Ascent, Local Beam Search |
| **Môi Trường Ẩn** (Complex Environments) | No Observation (Mù hoàn toàn - Gom trạng thái bằng vách ngăn), Partially Observable (Cảm biến quét góc rộng) |
| **Ràng Buộc (CSP)** | CSP Backtracking, Forward Checking, Min-Conflicts (Giảm thiểu xung đột) |
| **Tìm Đối Kháng** (Adversarial) | Minimax, Alpha-Beta Pruning, Expectimax (Vật cản sinh động theo lượt) |

---

## 🚀 Cài đặt và sử dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Thư viện `pygame` (phiên bản 2.5.0 trở lên)

### Cài đặt môi trường

1. Clone repository về máy:
   ```bash
   git clone https://github.com/daitran1309/python-final-project.git
   cd python-final-project
   ```

2. (Tùy chọn) Tạo môi trường ảo (Virtual Environment):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Đối với Linux/macOS
   venv\Scripts\activate     # Đối với Windows
   ```

3. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

### Chạy ứng dụng

Mở terminal/command prompt và chạy lệnh sau từ thư mục gốc của project:
```bash
python main.py
```

---

## 🎮 Hướng dẫn sử dụng giao diện

1. **Khám phá thuật toán**: Sử dụng Sidebar bên phải để chọn *Nhóm thuật toán* và *Thuật toán cụ thể*. Một bản đồ mẫu chuyên dụng sẽ tự động tải lên để minh hoạ tốt nhất cho thuật toán đó.
2. **Tùy chỉnh bản đồ**: 
   - Click chọn công cụ trong hộp `CÔNG CỤ VẼ BẢN ĐỒ`.
   - Dùng **chuột trái** click/kéo trên lưới để đặt vị trí Bắt đầu (Start), Đích đến (Goal), hoặc vẽ các loại vật cản (Tường, Đầm lầy, Vùng cấm).
   - Có thể nhấn nút **Ngẫu Nhiên** để máy tự động sinh chướng ngại vật.
3. **Thực thi**:
   - Tuỳ chỉnh tốc độ animation ở thanh gạt `Chậm - Nhanh`.
   - Nhấn nút **Chạy** để bắt đầu.
   - Quan sát bảng `THỐNG KÊ THỜI GIAN THỰC` và hiệu ứng mũi tên/quỹ đạo trên màn hình.
4. **Tùy chỉnh kỹ thuật nâng cao**: Thay đổi các thông số cấu hình cốt lõi (như Tầm nhìn cảm biến `SENSOR_RANGE`, trọng số đầm lầy, giới hạn Minimax) ngay trong tệp `config.py`.
5. **Làm mới**: Nhấn nút **Làm Mới** để khôi phục bản đồ về trạng thái gốc.

---

## 📂 Cấu trúc thư mục (Project Structure)

Toàn bộ mã nguồn dự án được thiết kế theo hướng Modularity (mô-đun hóa) nghiêm ngặt để đảm bảo khả năng mở rộng. Dưới đây là cây thư mục chi tiết:

```text
final-ai/
├── .vscode/             # Cấu hình workspace của VSCode cho môi trường lập trình
├── algorithms/          # Thư mục cốt lõi chứa 6 nhóm thuật toán AI
│   ├── adversarial/     # Nhóm thuật toán đối kháng (Game Theory)
│   │   ├── alpha_beta.py        # Alpha-Beta Pruning
│   │   ├── expectimax.py        # Expectimax Search
│   │   ├── minimax.py           # Thuật toán Minimax cơ bản
│   │   └── __init__.py
│   ├── complex_env/     # Môi trường phức tạp (Sensorless / Partially Observable)
│   │   ├── no_observation.py    # Mù hoàn toàn - Quản lý niềm tin (Belief State)
│   │   ├── partially_observable.py # Có cảm biến định vị - Cập nhật Bayes
│   │   └── __init__.py
│   ├── csp/             # Thỏa mãn ràng buộc (Constraint Satisfaction Problem)
│   │   ├── csp_solver.py        # Framework CSP cốt lõi
│   │   ├── forward_checking.py  # CSP với Forward Checking
│   │   ├── min_conflicts.py     # Local Search cho CSP (Min-Conflicts)
│   │   └── __init__.py
│   ├── informed/        # Nhóm thuật toán tìm kiếm có thông tin (Heuristic)
│   │   ├── astar.py             # Thuật toán A* tối ưu
│   │   ├── greedy.py            # Greedy Best-First Search
│   │   ├── ucs.py               # Uniform Cost Search (Chi phí đều)
│   │   └── __init__.py
│   ├── local_search/    # Nhóm thuật toán tìm kiếm cục bộ (Tối ưu hóa)
│   │   ├── local_beam_search.py # Cải tiến giữ lại k trạng thái tốt nhất
│   │   ├── simple_hill_climbing.py  # Leo đồi cơ bản
│   │   ├── steepest_hill_climbing.py# Leo đồi dốc nhất
│   │   └── __init__.py
│   ├── uninformed/      # Nhóm thuật toán tìm kiếm mù (Blind Search)
│   │   ├── bfs.py               # Tìm kiếm theo chiều rộng
│   │   ├── dfs.py               # Tìm kiếm theo chiều sâu
│   │   ├── ids.py               # Tìm kiếm sâu dần lặp lại (Iterative Deepening)
│   │   └── __init__.py
│   ├── base.py          # Abstract Base Class chứa bộ khung chung cho mọi thuật toán
│   └── __init__.py
├── core/                # Core logic môi trường vật lý của Robot
│   ├── grid.py          # Quản lý không gian lưới 2D và logic va chạm (collision)
│   ├── node.py          # Lớp Node dùng để biểu diễn trạng thái duyệt cây
│   ├── problem.py       # Lớp Problem đóng gói bài toán cho hàm AI
│   ├── robot.py         # Quản lý vị trí của Agent
│   └── __init__.py
├── gui/                 # Hệ thống Giao diện đồ họa (Pygame)
│   ├── app.py           # Vòng lặp Event-loop chính, kết nối UI và Logic
│   ├── components.py    # Các Custom Widgets: Buttons, Cards, Toggles (UI UI Component)
│   ├── renderer.py      # Xử lý đồ hoạ nâng cao (Arrow Rendering, Pulse Animation)
│   ├── sidebar.py       # Quản lý hiển thị thanh trạng thái và điều khiển bên phải
│   └── theme.py         # Quy định Palette Màu sắc, Font chữ chuẩn
├── maps/                # Quản lý dữ liệu Bản đồ
│   ├── samples/         # Chứa các file dữ liệu thô (.txt) dùng để parse
│   │   ├── complex.txt          # Bản đồ Môi trường ẩn / CSP
│   │   ├── maze.txt             # Mê cung dành cho Tìm kiếm mù
│   │   └── simple.txt           # Môi trường cơ bản
│   ├── map_loader.py    # Trình đọc và parse cấu hình từ file txt
│   ├── presets.py       # Quản lý việc tự động load các Preset chuẩn cho từng thuật toán
│   └── __init__.py
├── utils/               # Công cụ bổ trợ
│   ├── helpers.py       # Các hàm tính toán khoảng cách (Manhattan, Euclidean)
│   ├── metrics.py       # Bắt (tracking) dung lượng RAM, thời gian ms, số node duyệt
│   └── __init__.py
├── config.py            # Nơi tập trung toàn bộ cấu hình, hệ số, biến cục bộ dự án
├── main.py              # File chạy (Entry point) duy nhất của chương trình
├── README.md            # Tài liệu dự án bạn đang đọc
└── requirements.txt     # Danh sách Dependency Python (pygame)
```

## 🤝 Đóng góp (Contributing)

Mọi đóng góp nhằm cải thiện giao diện, tối ưu hóa thuật toán hoặc thêm các thuật toán mới đều được hoan nghênh.
Vui lòng tạo Pull Request hoặc mở Issue để thảo luận trước khi đóng góp.
