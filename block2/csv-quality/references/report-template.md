# Báo cáo quá tải và chất lượng dữ liệu: `{đường dẫn CSV}`

Ngưỡng quá tải: {max_hours} giờ

## Người vượt ngưỡng (Quá tải)
- {owner}: {total_hours} giờ

## Tổng giờ theo người
- {owner}: {total_hours} giờ

## Dòng bị loại
| Line | task_id | Lý do loại |
|---|---|---|
| {line} | {task_id} | {reasons} |

## Chi tiết chất lượng
- Số dòng dữ liệu (không header): {row_count}
- Dòng thiếu owner: {missing_owner_count}
- Dòng hours không hợp lệ: {invalid_hours_count}
- Số task_id bị lặp: {duplicate_id_count} ({duplicate_ids})

## Đánh giá & Khuyến nghị
- Dữ liệu có dùng được để tính tổng giờ/KPI chưa? Nếu còn lỗi: chưa, nêu lý do.
- Cách sửa đề xuất cho từng nhóm lỗi.
