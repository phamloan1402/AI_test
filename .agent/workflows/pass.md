---
description: Ghi nhận user duyệt (PASS/PARTIAL) một scope cụ thể vào Work Log & Memory theo worklog_memory_rules.
---

# /pass <scope>

> **Workflow:** Ghi sự kiện `PASS` (hoặc `PARTIAL` nếu chỉ duyệt một phần) cho scope user nêu — VD: `/pass B2 Q&A DeNghiDieuChinhTCTD`, `/pass B4`.

## Hướng dẫn thực thi

Quy tắc duy nhất: 👉 **[`worklog_memory_rules.md`](../rules/worklog_memory_rules.md)** — BẮT BUỘC đọc lại toàn bộ trước khi ghi.

### Các bước cho AI Agent:
1. Thiếu `<scope>` hoặc scope mơ hồ → hỏi lại *"Bạn xác nhận PASS cho phạm vi nào?"* (tối đa 1 lần nữa, §2.3). Vẫn không rõ → không ghi.
2. Xác định feature + `<slug>` (§1.1). Kiểm tra blocking open issue trong `practices/Q&A/<slug>_QA.md` → còn blocking thì **không ghi** PASS/PARTIAL, báo lý do.
3. Lấy timestamp `+07:00` (§3.3), re-read Work Log + `archive/`, kiểm tra trùng Event ID (§3.2).
4. Append bản ghi vào `practices/worklog/<slug>_WORKLOG.md` (§3.4); cập nhật `PROJECT_MEMORY.md` và `memory/<slug>_MEMORY.md` (§4), đối soát với `<FeatureName>_rbt_state.md` (§4.4).
5. Áp dụng redaction (§7), rotate nếu vượt ngưỡng (§8), báo cáo theo §10.
