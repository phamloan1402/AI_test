---
description: Review kịch bản test đã có so với SRS — phân tích coverage theo common_tc_checklist và kiểm tra đủ logic nghiệp vụ + tích hợp liên module. Output là file báo cáo .md liệt kê GAPs và gợi ý bổ sung.
---

# /review_testcases_with_srs

> **Workflow:** Review kịch bản test đã có so với SRS — phân tích coverage theo common_tc_checklist và kiểm tra đủ logic nghiệp vụ + tích hợp liên module. Output là file báo cáo .md liệt kê GAPs và gợi ý bổ sung.

## Hướng dẫn thực thi

Quy trình chi tiết và toàn bộ các bước thực hiện được quản lý tại skill:
👉 **[`wf_review_testcases_with_srs`](../skills/wf_review_testcases_with_srs/SKILL.md)**

### Các bước cho AI Agent:
1. Nạp và đọc kỹ hướng dẫn tại: `.agent/skills/wf_review_testcases_with_srs/SKILL.md`.
2. Kiểm tra và nạp các kỹ năng phụ thuộc (`Dependent skills`) được khai báo trong skill đó.
3. Tuân thủ nghiêm ngặt các điểm dừng xác nhận (Review Gate / Checkpoint) trước khi chuyển bước.
