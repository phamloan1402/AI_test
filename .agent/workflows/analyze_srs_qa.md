---
description: Đọc và phân tích tài liệu SRS để trích xuất danh sách Q&A chuẩn (bao gồm nghiệp vụ và cross-cutting) giúp làm rõ các yêu cầu hệ thống.
---

# /analyze_srs_qa

> **Workflow:** Đọc và phân tích tài liệu SRS để trích xuất danh sách Q&A chuẩn (bao gồm nghiệp vụ và cross-cutting) giúp làm rõ các yêu cầu hệ thống.

## Hướng dẫn thực thi

Quy trình chi tiết và toàn bộ các bước thực hiện được quản lý tại skill:
👉 **[`wf_analyze_srs_qa`](../skills/wf_analyze_srs_qa/SKILL.md)**

### Các bước cho AI Agent:
1. Nạp và đọc kỹ hướng dẫn tại: `.agent/skills/wf_analyze_srs_qa/SKILL.md`.
2. Kiểm tra và nạp các kỹ năng phụ thuộc (`Dependent skills`) được khai báo trong skill đó.
3. Tuân thủ nghiêm ngặt các điểm dừng xác nhận (Review Gate / Checkpoint) trước khi chuyển bước.
