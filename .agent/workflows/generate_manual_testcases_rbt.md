---
description: Sinh manual test cases chất lượng cao theo quy trình AI-RBT 7 bước (Risk-Based Testing) từ requirements.
---

# /generate_manual_testcases_rbt

> **Workflow:** Sinh manual test cases chất lượng cao theo quy trình AI-RBT 7 bước (Risk-Based Testing) từ requirements.

## Hướng dẫn thực thi

Quy trình chi tiết và toàn bộ các bước thực hiện được quản lý tại skill:
👉 **[`wf_generate_manual_testcases_rbt`](../skills/wf_generate_manual_testcases_rbt/SKILL.md)**

### Các bước cho AI Agent:
1. Nạp và đọc kỹ hướng dẫn tại: `.agent/skills/wf_generate_manual_testcases_rbt/SKILL.md`.
2. Kiểm tra và nạp các kỹ năng phụ thuộc (`Dependent skills`) được khai báo trong skill đó.
3. Tuân thủ nghiêm ngặt các điểm dừng xác nhận (Review Gate / Checkpoint) trước khi chuyển bước.
4. Tại **B2 (Analysis & QnA)**, áp dụng schema Q&A chung của `srs_qa_architect` (nguồn duy nhất, §4–§5):
   - Truy vết `srs_qa_architect/references/checklist-review.md` (**không** dùng `common_tc_checklist.md` ở B2) theo schema Full Review của `srs_qa_architect`: Coverage đủ 19 nhóm `CR-A`…`CR-S`, cột `Mã checklist` cho mọi Q-ID, chạy Self-check.
   - Cột `Vấn đề & Rủi ro` (4 ý) và `Assumption / Options` (Option A/B/(C) + **>> Chọn Option X vì: <lý do>**; rủi ro cao kèm `⚠️ Cần BA/PO quyết định`) theo `srs_qa_architect` §4. Cột `Câu trả lời` để trống cho BA/PO.
