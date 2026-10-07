# Phân tích kết quả - Bài luyện tập 02

## Block 1: Tra cứu chính sách đúng phiên bản (Stage 01 & Stage 02)

### Các thay đổi đã thực hiện
- **Stage 01**:
  - Tạo 2 file `policy-before-oct.md` (chính sách trước 1/10/2023) và `policy-from-oct.md` (chính sách từ 1/10/2023) trong `workspace/data/policies/`.
  - Cập nhật thư viện công cụ bằng cách cài đặt `list_files` trong `tools/files.py`, `tools/__init__.py`, và `agent.py`.
- **Stage 02**:
  - Tạo `SKILL.md` cho skill `refund-policy` hướng dẫn Agent chọn chính sách dựa trên ngày mua và yêu cầu người dùng cung cấp thông tin nếu thiếu.
  - Tạo template báo cáo `references/answer-template.md`.

### Kết quả các trường hợp kiểm tra
1. **Trường hợp A (Khách mua ngày 2/9, yêu cầu ngày 10/9)**: Áp dụng chính sách `policy-before-oct.md` do ngày mua trước tháng 10. Khoảng cách là 8 ngày (dưới 14 ngày), tài khoản đã kích hoạt -> Kết luận **Đủ điều kiện**, phí hoàn: **0đ**.
2. **Trường hợp B (Khách mua ngày 25/10, yêu cầu ngày 1/11)**: Áp dụng chính sách `policy-from-oct.md` do ngày mua từ tháng 10. Khoảng cách là 7 ngày (dưới 15 ngày), tài khoản đã kích hoạt -> Kết luận **Đủ điều kiện**, phí hoàn: **10%**.
3. **Trường hợp thiếu thông tin (Không có ngày mua)**: Agent không tự suy đoán mà đặt câu hỏi yêu cầu khách hàng bổ sung ngày mua để có thể xác định chính sách áp dụng, đáp ứng đúng hướng dẫn trong `SKILL.md`.

### Câu hỏi cuối bài:
- **Vì sao cần tool để tìm file và skill để hướng dẫn chọn chính sách?**
  - **Tool tìm file (`list_files`)**: Giúp agent linh hoạt tìm kiếm, quét các thư mục để tìm file chính sách một cách tự động, ngay cả khi tên file thay đổi hoặc bị di chuyển. Agent không cần phải biết trước đường dẫn cứng (hardcoded path).
  - **Skill hướng dẫn**: Cung cấp quy trình rõ ràng (workflow), cung cấp cho model các quy tắc logic như cách tính số ngày, so sánh với mốc thời gian 1/10/2026, phí phần trăm, và lúc nào cần dừng lại để hỏi thêm thông tin từ người dùng.
- **Nếu agent chưa có tool tìm file, việc sửa prompt có giải quyết được yêu cầu đổi tên file không?**
  - **Không**. Nếu không có tool tìm file, cách duy nhất để agent đọc file là cung cấp chính xác đường dẫn trong prompt. Nếu đổi tên file mà chỉ sửa prompt, chúng ta đang biến đổi agent thành một chương trình tĩnh (static). Mỗi lần thay đổi tên file, lập trình viên phải can thiệp thủ công vào code để cập nhật system prompt. Việc này đi ngược lại với nguyên lý tự chủ (autonomous) của Agentic AI. Tool tìm file cho phép agent thích ứng tự động với những thay đổi về mặt cấu trúc thư mục mà không cần sửa đổi mã nguồn.
