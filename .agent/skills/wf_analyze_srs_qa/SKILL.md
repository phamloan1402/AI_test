---
name: wf_analyze_srs_qa
description: "Đọc và phân tích tài liệu SRS để trích xuất danh sách Q&A chuẩn (bao gồm nghiệp vụ và cross-cutting) giúp làm rõ các yêu cầu hệ thống. Use when the user invokes WF_analyze_srs_qa, /analyze_srs_qa, or asks to run this workflow."
---

# WF_analyze_srs_qa

## Cross-agent compatibility contract

- Run on Codex, Claude, Gemini/Google, or any agent capable of reading Markdown and operating on the repository.
- Resolve relative paths from the repository root. Do not depend on a vendor-specific installation directory.
- Map tool names in this workflow to equivalent available capabilities such as browser, shell, file operations, Jira, and Confluence. Do not skip a step only because a tool has a different name.
- Follow `AGENTS.md` and any agent-specific instruction file. If instructions conflict, prioritize security and repository-level rules.
- Never read `.env` files directly. Only check their existence or invoke a process designed to load environment variables internally.

## Dependent skills

- `.agent/skills/srs_qa_architect/SKILL.md`

If the workflow below names additional mandatory skills or references, read them before execution. On agents without native skill invocation, open the corresponding `SKILL.md` directly and follow it.

## Original workflow

# Workflow: Phân tích SRS & Trích xuất Q&A

> **Slash command:** `/analyze_srs_qa` | **Skill:** `srs_qa_architect` | **MCP:** Atlassian (Confluence)

**Kích hoạt khi:** "Đọc SRS và viết Q&A", "Phân tích requirements lấy luồng và questions", "Sinh câu hỏi từ Confluence", "Có mơ hồ không", "Viết lại câu này", `/analyze_srs_qa`

---

## Vai Trò

Đóng vai **Senior Test Architect** — mục tiêu duy nhất: bảo vệ chất lượng kiểm thử bằng cách phát hiện sớm điểm mù, mâu thuẫn, và sự mơ hồ trong spec. 4 trụ cột tư duy: **Testability**, **Defect Prevention**, **State & Data**, **Cross-module Impact**.

---

## Nguyên Tắc

- **DỪNG và CHỜ PHẢN HỒI** sau khi sinh ra file Q&A, không tự ý bước sang các tác vụ khác (như viết TC) khi chưa được duyệt Assumptions.
- File Q&A xuất ra phải tuân thủ nghiêm ngặt chuẩn bảng Markdown trong `SKILL.md`.
- Bắt buộc đánh giá **Cross-Cutting theo applicability**; không hỏi Filter, Pagination, UI hoặc NFR không liên quan tới feature.
- Mỗi câu hỏi có **Assumption** khi tồn tại phương án mặc định ít rủi ro; nếu có nhiều phương án hợp lệ thì dùng Options, và có thể để BA/PO quyết định với vấn đề rủi ro cao.
- Tất cả output bằng **Tiếng Việt**.

---

## Xác Định Output Mode

Trước khi bắt đầu, xác định loại yêu cầu của User để chọn output mode phù hợp:

| Yêu cầu của User | Output Mode |
|---|---|
| Dán 1 câu/đoạn SRS ngắn, hỏi "có mơ hồ không" / "viết lại câu này" | **Inline** — trả lời trực tiếp trong chat: SRS gốc → Vấn đề → Câu hỏi (kèm Assumption) → Viết lại. Không cần sinh file. |
| Đưa cả SRS / 1 feature lớn, muốn chuẩn bị test case | **Full Q&A** — sinh file Q&A đầy đủ → **DỪNG LẠI** chờ xác nhận (Bước 1–4 bên dưới). |
| User xác nhận tiếp tục | **Continue** — ưu tiên câu trả lời BA/PO, chỉ dùng assumption đã được chấp thuận; tính lại verdict rồi handoff sang workflow thiết kế test phù hợp. |

> **Nếu là mode Inline** → không cần chạy qua các bước bên dưới.

---

## Các Bước Thực Hiện (Mode Full Q&A)

### Bước 1 — Lấy Thông Tin Nguồn
- Yêu cầu User cung cấp **Page ID** của tài liệu Confluence (hoặc URL, hoặc dán nội dung trực tiếp).
- Gọi công cụ `mcp__Atlassian__confluence_get_page` để lấy nội dung.
- Nếu tài liệu có trang con, hỏi User xem có cần lấy thêm không.

### Bước 2 — Phân Tích & Xác Định Logic
Đọc tài liệu và thực hiện tuần tự:

1. **Phân loại luồng:**
   - Các **Luồng chính (Happy Path)** — tóm tắt để confirm hiểu đúng nghiệp vụ.
   - Các **Luồng ngoại lệ (Alternate/Exception Paths)** — QA sẽ tập trung test.

2. **Rà theo checklist đầy đủ** — đọc `.agent/skills/srs_qa_architect/references/checklist-review.md` (96 tiêu chí / 19 nhóm A–S), xác định Applicable/N/A trước khi tạo finding:
   - Nội dung nghiệp vụ, business rule & validation (BVA, state machine, RBAC)
   - Exception handling (timeout, concurrent edit, data edge case)
   - Kiểm tra chéo UI theo capability thực tế của màn hình
   - Chất lượng viết IEEE 830, luồng liên chức năng (nhóm S)

3. **Soi từng câu phát hiện mơ hồ** — đọc `.agent/skills/srs_qa_architect/references/Ambiguity.md` (6 nhóm từ khóa cờ đỏ VN+EN):
   - Định tính/chủ quan, định lượng mơ hồ, so sánh chưa có mốc
   - Mơ hồ thời gian, hiệu năng, bảo mật

4. **Kiểm tra chéo theo capability** — chỉ hỏi mục thực sự xuất hiện trong phạm vi:
   - Tìm kiếm đa trường có AND/OR không?
   - Filter dùng control gì (dropdown/multi-select/autocomplete), data động hay hardcode?
   - Pagination mặc định bao nhiêu dòng/trang, cuộn vô hạn hay click số trang?
   - Export/Import: format tên file, format ngày tháng, giới hạn số dòng?
   - Validate onBlur (từng field) hay onSubmit (gom lại)?

Đọc và áp dụng `.agent/skills/srs_qa_architect/references/deep-logic-review.md`: dựng các mô hình áp dụng, đối chiếu rule/flow/permission/state/data và dùng tình huống phản biện để tìm logic chưa hợp lý, mâu thuẫn. Giữ vai trò Senior Test Architect / QA Lead; lưu bảng đối chiếu gọn cùng Q-ID trong artifact.

5. **Với mỗi vấn đề phát hiện** → ghi `Vấn đề & Rủi ro` (4 ý) và `Assumption / Options` (Option A/B/(C) + `>> Chọn Option X vì: <lý do>`; rủi ro cao kèm `⚠️ Cần BA/PO quyết định`) theo `srs_qa_architect` §4.

### Bước 3 — Sinh File Q&A (CHECKPOINT)
- Tạo file Q&A tại: `practices/Q&A/<FeatureName>_QA.md` theo format mẫu trong `SKILL.md`.
- File phải dùng schema Quality Gate + Q&A **Full Review** của `srs_qa_architect` (mục 1 Coverage đủ 19 nhóm `CR-A`…`CR-S`, cột `Mã checklist` cho mọi Q-ID); phần không áp dụng ghi N/A thay vì tạo finding giả.
- Chạy **Self-check (a)–(d)** của `srs_qa_architect` §5 trước khi báo user — nhờ đó file này dùng lại được trực tiếp ở B2 của FULL RBT.
- Có phần **Phân tích luồng nghiệp vụ** (Happy Paths + Alternate/Exception Paths).
- Có bảng **Tổng kết** phân loại rủi ro theo nhóm.
- Báo cáo với User rằng đã hoàn thành và **DỪNG LẠI** chờ phản hồi.
- Cung cấp đường dẫn tới file Q&A và hướng dẫn cách phản hồi (OK / ghi nội dung đúng / N/A).

### Bước 4 — Cập Nhật Lại (Sau Khi Có Feedback)
- Khi User phản hồi (trả lời các câu hỏi Q&A hoặc duyệt Assumptions).
- AI cập nhật file Q&A tương ứng với các quyết định đã chốt.
- Nếu User xác nhận tiếp tục → đọc lại toàn bộ Q&A, ưu tiên câu trả lời BA/PO, chỉ dùng assumption đã được chấp thuận, đánh dấu câu chưa giải quyết và tính lại verdict trước khi handoff.

---

## Khi Nào KHÔNG Cần Review Đầy Đủ

- Câu hỏi khái niệm chung (VD: "IEEE 830 là gì", "SRS là gì") → trả lời trực tiếp, không chạy checklist.
- User chỉ đưa 1 câu và hỏi có mơ hồ không → chỉ áp dụng `Ambiguity.md`, không cần rà cả 19 nhóm (chế độ Inline, vẫn ghi `Mã checklist`).
- User đã tự xác nhận rule nghiệp vụ / đã trả lời câu hỏi làm rõ trước đó → không hỏi lại, dùng thẳng thông tin đó.

---

## Tài Liệu Tham Khảo

| Tài liệu | Mô tả |
|---|---|
| `srs_qa_architect/SKILL.md` | Nguồn chuẩn cho vai trò, quy trình, severity, verdict và format output |
| `srs_qa_architect/references/checklist-review.md` | 96 tiêu chí / 19 nhóm A–S, mỗi tiêu chí kèm ví dụ |
| `srs_qa_architect/references/Ambiguity.md` | 6 nhóm từ khóa cờ đỏ VN+EN + 5 ví dụ minh họa chi tiết |
