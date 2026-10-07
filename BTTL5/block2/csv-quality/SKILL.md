---
name: csv-quality
description: Kiểm tra quá tải, tổng giờ theo người và chất lượng file CSV danh sách công việc. Dùng khi người dùng yêu cầu tính tổng giờ, kiểm tra quá tải hoặc kiểm tra dữ liệu.
---

# CSV quality

Kiểm tra chất lượng và tình trạng quá tải trong CSV công việc bằng script.

## Chạy script

Dùng tool `bash` (cwd là workspace). Lệnh đầy đủ:

```
python skills/csv-quality/scripts/check_csv.py --input <đường dẫn CSV> --max-hours <ngưỡng>
```

Nếu yêu cầu kiểm tra quá tải **thiếu ngưỡng** thì **phải hỏi lại** người dùng. Nếu có, truyền đúng giá trị vào lệnh (ví dụ `--max-hours 8`).
Không dùng ngưỡng từ cuộc trò chuyện cũ.

## Kiểm tra kết quả

- `exit_code` 0: phân tích thành công. `stdout` là JSON. Dữ liệu có lỗi chất lượng vẫn là exit 0.
- `exit_code` khác 0: **lỗi thực thi** (thiếu tham số, giá trị không hợp lệ, file không tồn tại). Đọc `stderr`, báo không phân tích được cho người dùng. Không đưa ra tổng giờ hay báo cáo.

## Viết báo cáo

1. Đọc template `references/report-template.md` trong thư mục skill này.
2. Lấy số liệu từ JSON của script, gồm ngưỡng, tổng giờ theo người, người vượt ngưỡng, và các dòng bị loại kèm lý do.
3. Không tự sửa file CSV.
4. Ghi báo cáo bằng công cụ tạo file vào đường dẫn yêu cầu (vd: `output/workload.md`).
