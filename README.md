# 🤖 Robot Giao Hàng - AI Search Algorithms

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.5.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Một ứng dụng minh họa trực quan các thuật toán tìm kiếm cơ bản và nâng cao trong Trí tuệ nhân tạo (AI). Ứng dụng mô phỏng bài toán tìm đường đi cho robot giao hàng trên lưới 2D, giúp người dùng dễ dàng quan sát cách các thuật toán hoạt động, duyệt không gian trạng thái và tìm ra giải pháp tối ưu.

## ✨ Tính năng nổi bật

- **Giao diện Hiện đại (Clean & Modern Minimalist)**: Ứng dụng sở hữu Light Theme cao cấp, hỗ trợ tự động co giãn lưới (Responsive Layout) và font chữ Tiếng Việt sắc nét.
- **Mô phỏng Animation Mượt mà**: Quan sát trực tiếp từng bước thuật toán lan tỏa (Fade-in animation) và dò tìm đường đi (Pulse animation).
- **Tương tác Thời gian thực (Real-time)**: 
  - Thống kê thông số (Độ dài đường đi, số node đã mở, thời gian) tự động cập nhật ngay trong lúc animation đang chạy.
  - Cho phép người dùng trực tiếp dùng chuột vẽ các loại chướng ngại vật: Tường cứng, Đầm lầy (x5 chi phí), Vùng cấm, và kéo thả Start/Goal.
- **Đa dạng thuật toán**: Hoàn thiện 6 nhóm thuật toán AI kinh điển với các bản đồ chuyên dụng đi kèm để mô phỏng chính xác ưu/nhược điểm của từng loại.
- **Ghi chú trực quan**: Hệ thống Tooltips động ngay trên giao diện giúp người dùng mới dễ dàng hiểu được các thao tác và đặc điểm của bản đồ.
- **Tạo Mê Cung Ngẫu Nhiên**: Tính năng sinh chướng ngại vật ngẫu nhiên chỉ bằng một cú click.

## 🧠 Các thuật toán được hỗ trợ

Dự án này bao gồm 6 nhóm thuật toán chính trong lĩnh vực AI:

| Nhóm thuật toán | Các thuật toán được cài đặt |
|-----------------|-----------------------------|
| **Tìm Kiếm Mù** (Uninformed Search) | BFS, DFS, IDS (Iterative Deepening Search) |
| **Có Thông Tin** (Informed Search) | UCS (Uniform-Cost), Greedy Best-First, A* (A-Star) |
| **Tìm Cục Bộ** (Local Search) | Simple Hill Climbing, Steepest Ascent, Local Beam Search |
| **Môi Trường Ẩn** (Complex Environments) | No Observation, Partially Observable (Cảm biến một phần) |
| **Ràng Buộc (CSP)** | Backtracking, Forward Checking, Min-Conflicts |
| **Tìm Đối Kháng** (Adversarial) | Minimax, Alpha-Beta Pruning, Expectimax |

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

## 🎮 Hướng dẫn sử dụng giao diện

1. **Khám phá thuật toán**: Sử dụng Sidebar bên phải để chọn *Nhóm thuật toán* và *Thuật toán cụ thể*. Một bản đồ mẫu chuyên dụng sẽ tự động tải lên để minh hoạ tốt nhất cho thuật toán đó.
2. **Tùy chỉnh bản đồ**: 
   - Click chọn công cụ trong hộp `CÔNG CỤ VẼ BẢN ĐỒ`.
   - Dùng **chuột trái** click/kéo trên lưới để đặt vị trí Bắt đầu (Start), Đích đến (Goal), hoặc vẽ các loại vật cản (Tường, Đầm lầy, Vùng cấm).
   - Có thể nhấn nút **Ngẫu Nhiên** để máy tự động sinh chướng ngại vật.
3. **Thực thi**:
   - Tuỳ chỉnh tốc độ animation ở thanh gạt `Chậm - Nhanh`.
   - Nhấn nút **Chạy** để bắt đầu.
   - Quan sát bảng `THỐNG KÊ THỜI GIAN THỰC` và hiệu ứng lan toả thuật toán trên màn hình.
4. **Làm mới**: Nhấn nút **Làm Mới** để khôi phục bản đồ về trạng thái gốc.

## 📂 Cấu trúc thư mục (Project Structure)

```text
final-ai/
├── .vscode/             # Cấu hình workspace của VSCode
│   └── settings.json
├── algorithms/          # Mã nguồn các thuật toán tìm kiếm (được chia theo 6 nhóm)
│   ├── adversarial/     # Nhóm thuật toán đối kháng
│   │   ├── alpha_beta.py
│   │   ├── expectimax.py
│   │   ├── minimax.py
│   │   └── __init__.py
│   ├── complex_env/     # Môi trường phức tạp (không quan sát/cảm biến một phần)
│   │   ├── no_observation.py
│   │   ├── partially_observable.py
│   │   └── __init__.py
│   ├── csp/             # Thỏa mãn ràng buộc (Constraint Satisfaction Problem)
│   │   ├── csp_solver.py
│   │   ├── forward_checking.py
│   │   ├── min_conflicts.py
│   │   └── __init__.py
│   ├── informed/        # Nhóm thuật toán tìm kiếm có kinh nghiệm (Heuristic)
│   │   ├── astar.py
│   │   ├── greedy.py
│   │   ├── ucs.py
│   │   └── __init__.py
│   ├── local_search/    # Nhóm thuật toán tìm kiếm cục bộ
│   │   ├── local_beam_search.py
│   │   ├── simple_hill_climbing.py
│   │   ├── steepest_hill_climbing.py
│   │   └── __init__.py
│   ├── uninformed/      # Nhóm thuật toán tìm kiếm mù (Blind Search)
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── ids.py
│   │   └── __init__.py
│   ├── base.py          # Lớp cơ sở (Base Class) cho các thuật toán
│   └── __init__.py
├── core/                # Các thành phần cốt lõi của bài toán
│   ├── grid.py          # Quản lý không gian lưới (môi trường mô phỏng)
│   ├── node.py          # Cấu trúc dữ liệu Node dùng để duyệt cây
│   ├── problem.py       # Định nghĩa bài toán tìm kiếm
│   ├── robot.py         # Quản lý trạng thái và hành động của Robot (Agent)
│   └── __init__.py
├── gui/                 # Giao diện người dùng (Pygame) - Clean & Modern Minimalist
│   ├── app.py           # Vòng lặp chính, xử lý sự kiện và tích hợp logic
│   ├── components.py    # UI Widgets tái sử dụng (Button, PillToggleGroup, Card)
│   ├── renderer.py      # Xử lý đồ hoạ vẽ Lưới, Icon, Hiệu ứng Animation
│   ├── sidebar.py       # Thanh điều khiển trung tâm
│   └── theme.py         # Quản lý hệ màu sắc (Light Theme) và Font chữ
├── maps/                # Quản lý hệ thống bản đồ
│   ├── samples/         # Chứa các file bản đồ mẫu dạng text (.txt)
│   │   ├── complex.txt
│   │   ├── maze.txt
│   │   └── simple.txt
│   ├── map_loader.py    # Logic đọc và parse bản đồ từ file
│   ├── presets.py       # Dữ liệu và hàm tiện ích tải bản đồ dựng sẵn
│   └── __init__.py
├── utils/               # Các hàm tiện ích bổ trợ
│   ├── helpers.py       # Các hàm helper chung
│   ├── metrics.py       # Module đo lường và theo dõi thuật toán (time, memory, nodes)
│   └── __init__.py
├── config.py            # Chứa các hằng số và cấu hình toàn cục
├── main.py              # File entry point chạy ứng dụng
├── README.md            # Tài liệu của dự án
└── requirements.txt     # Danh sách các thư viện Python cần thiết
```

## 🤝 Đóng góp (Contributing)

Mọi đóng góp nhằm cải thiện giao diện, tối ưu hóa thuật toán hoặc thêm các thuật toán mới đều được hoan nghênh.
Vui lòng tạo Pull Request hoặc mở Issue để thảo luận trước khi đóng góp.


