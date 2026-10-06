# Hướng dẫn chạy Hệ thống Agent Đặt vé máy bay (Flight Booking Agent)

Đây là tài liệu hướng dẫn các lệnh thực thi nhằm tự động hóa việc đánh giá và tạo báo cáo cho Bài thực hành #3. Dự án này được thiết kế riêng với kịch bản vé máy bay đi **Phú Quốc (PQC)** ngày **20/12/2026**.

## Yêu cầu môi trường
- Python 3.9+
- Các thư viện cần thiết:
```bash
pip install -r requirements.txt
```
*(Nếu chưa có requirements.txt, hãy đảm bảo đã cài đặt `langchain`, `langgraph`, `python-docx`)*

---

## Danh sách các lệnh thực thi (Dùng để lấy minh chứng)

### 1. Minh chứng cấu trúc thư mục
In ra cấu trúc thư mục của dự án:
```bash
tree /F
```

### 2. Kiểm thử Unit Test cho Harness (Lớp bảo vệ)
Chạy kịch bản kiểm tra các rào cản (Constraints, Permission Guard) để đảm bảo hệ thống chặn các hành vi sai lệch:
```bash
python test_harness.py
```

### 3. Chạy từng mẫu Agent (ReAct, Plan-then-Execute, Hybrid)
Bạn có thể dùng cờ `--pattern` và `--scenario` để chạy độc lập từng kịch bản. Các lệnh dưới đây dùng để lấy minh chứng cho báo cáo:

- **Chạy ReAct (Kịch bản cần duyệt thanh toán - Permission Guard):**
  ```bash
  python main.py --pattern react --scenario can-duyet
  ```
- **Chạy ReAct (Kịch bản chuẩn):**
  ```bash
  python main.py --pattern react --scenario chuan
  ```
- **Chạy Plan-then-Execute (Kịch bản chuẩn):**
  ```bash
  python main.py --pattern plan-execute --scenario chuan
  ```
- **Chạy Hybrid (Kịch bản chuẩn):**
  ```bash
  python main.py --pattern hybrid --scenario chuan
  ```
*(Ghi chú: Thêm cờ `--real` vào cuối nếu muốn chạy với LLM thật thông qua Gemini API thay vì mô hình giả lập tốc độ cao).*

### 4. Đánh giá toàn diện (Benchmark)
Lệnh này sẽ tự động chạy 4 tình huống kiểm tra trên cả 3 mẫu Agent (ReAct, Plan-then-Execute, Lai) và lưu kết quả vào file `evaluation_results.json`:
```bash
python run_evaluation.py
```
