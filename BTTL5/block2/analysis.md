# Phân tích kết quả - Bài luyện tập 02

## Block 2: Kiểm tra quá tải theo người (Stage 03 & Stage 04)

### Các thay đổi đã thực hiện
- **Stage 04 (Script & Skill)**:
  - Cập nhật script `scripts/check_csv.py` bổ sung tham số dòng lệnh `--max-hours`, hỗ trợ đọc các dòng hợp lệ để tính `hours_by_owner`, lọc ra `overloaded_owners` dựa trên ngưỡng, và ghi chi tiết lỗi vào `excluded_rows`. Fix lỗi in Unicode ra stdout và stderr.
  - Cập nhật test `test_check_csv.py` bổ sung logic chạy với `--max-hours` và thêm một unit test kiểm tra edge case khi ID xuất hiện lần đầu bị lỗi format hours.
  - Cập nhật `SKILL.md` và `references/report-template.md` của skill `csv-quality` để nhắc nhở Agent hỏi lại ngưỡng, và điền thông tin quá tải vào báo cáo kết quả.
  - Đồng bộ hóa các thay đổi từ thư mục `workspace/` sang `fixtures/`.

### Kết quả các trường hợp kiểm tra
1. **Ngưỡng 8**: `Lan` có tổng số giờ là 9, vượt ngưỡng 8 nên được đưa vào danh sách quá tải. `Minh` có 3 giờ, không quá tải. Dòng 5 bị loại vì sai định dạng giờ, dòng 6 bị loại vì lặp `task_id`, dòng 7 bị loại do thiếu `owner`.
2. **Ngưỡng 9**: Vẫn lọc các dòng trên, tuy nhiên không có ai quá tải vì 9 giờ không lớn hơn ngưỡng 9.
3. **Không cung cấp ngưỡng**: Agent tự động dừng lại và hỏi người dùng để biết giá trị ngưỡng `max-hours` trước khi chạy lệnh.
4. **File không tồn tại**: Script xuất lỗi ra `stderr`, trả về exit code `1`. Agent giải thích cho người dùng là không thể phân tích được do lỗi thực thi và không tạo báo cáo ảo.
5. **Trường hợp đặc biệt (workload-edge.csv)**: ID `E01` của `Lan` dòng đầu có hours bị lỗi, khi lặp lại ở dòng sau, nó bị loại với lý do `duplicate_id`. Tổng cộng `Lan` có 0 giờ. Unit test trong `test_check_csv.py` hoạt động hoàn hảo và pass.

### Câu hỏi cuối bài: Phần nào do script tính, phần nào do model diễn giải?
- **Phần script tính toán**: Script chịu trách nhiệm tính toán logic cứng như đọc file, đếm tổng giờ theo người, so sánh với ngưỡng `max-hours` để tìm người quá tải, lọc loại bỏ các dòng lặp/lỗi, và ném lỗi exit 1 nếu đầu vào không hợp lệ. Kết quả được đóng gói chặt chẽ dưới dạng JSON.
- **Phần model diễn giải**: LLM đóng vai trò như cầu nối. Model diễn giải yêu cầu người dùng để trích xuất `max-hours`, gọi script với các cờ (flags) tương ứng, parse thông tin JSON trả về, và dịch chúng sang định dạng ngôn ngữ tự nhiên thông qua template Markdown. 
- **Nếu sửa script nhưng không cập nhật skill/reference**: Nếu script xuất thêm trường JSON nhưng `SKILL.md` và template không thay đổi, model sẽ không truyền tham số `max-hours`, gây crash script. Cho dù script có chạy thành công, model sẽ tiếp tục dùng mẫu báo cáo cũ, làm mất hoàn toàn giá trị của những thông tin vừa được cập nhật (người bị quá tải, tổng giờ của từng người). Báo cáo đầu ra sẽ sai lệch so với mong đợi hoặc thiếu thông tin trầm trọng.
