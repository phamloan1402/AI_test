---
name: wf_generate_testcases_from_requirements
description: "Sinh manual test cases nhanh từ requirements (QUICK mode — không qua quy trình AI-RBT 7 bước đầy đủ). Use when the user invokes WF_generate_testcases_from_requirements, /generate_testcases_from_requirements, or asks to run this workflow."
---

# WF_generate_testcases_from_requirements

## Cross-agent compatibility contract

- Run on Codex, Claude, Gemini/Google, or any agent capable of reading Markdown and operating on the repository.
- Resolve relative paths from the repository root. Do not depend on a vendor-specific installation directory.
- Map tool names in this workflow to equivalent available capabilities such as browser, shell, file operations, Jira, and Confluence. Do not skip a step only because a tool has a different name.
- Follow `AGENTS.md` and any agent-specific instruction file. If instructions conflict, prioritize security and repository-level rules.
- Never read `.env` files directly. Only check their existence or invoke a process designed to load environment variables internally.

## Dependent skills

- `.agent/skills/rbt_manual_testing/SKILL.md`

If the workflow below names additional mandatory skills or references, read them before execution. On agents without native skill invocation, open the corresponding `SKILL.md` directly and follow it.

## Original workflow

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`rbt_manual_testing`** (tại `.agent/skills/rbt_manual_testing/SKILL.md`) trước khi bắt đầu thực hiện tác vụ này. Sử dụng **Mode QUICK** của skill.

# Workflow: Sinh Manual Test Cases Nhanh từ Requirements

Workflow này sử dụng **Mode QUICK** của skill `rbt_manual_testing` để sinh test cases nhanh từ requirements đã sẵn có.

## ⚠️ Nguyên tắc

- **Mode:** QUICK (2 lượt: Lượt 1 — sinh TC draft; Lượt 2 — TC Lead Review Gate → xuất final)
- **Dừng 1 lần** tại TC Lead Review Gate (sau Lượt 1) để user confirm trước khi xuất bảng final
- Phù hợp cho module đơn giản, requirements đã rõ ràng
- Nếu phát hiện requirements quá phức tạp hoặc mơ hồ → **tự động chuyển sang FULL RBT** và thông báo user
- Tất cả output bằng **Tiếng Việt**
- **Common TC Checklist BẮT BUỘC:** Sau khi đọc requirements, PHẢI lập Field Inventory và áp dụng checklist tại `.agent/skills/rbt_manual_testing/references/common_tc_checklist.md` — sinh đủ Common TCs cho tất cả nhóm áp dụng trước khi sinh Business TCs

## Các bước thực hiện

1. **Đọc và hiểu requirements** được user cung cấp

2. **Lập Field Inventory & xác định nhóm Common TC** *(bắt buộc)*

   Liệt kê toàn bộ fields/controls trên màn hình, sau đó dùng **Bảng điều phối** trong checklist để tick nhóm áp dụng:

   | Field Name | Field Type | Required? | Constraint |
   |---|---|---|---|
   | ... | TEXT / NUMBER / DATE / ... | Yes/No | maxlength, min/max... |

   Nhóm luôn áp dụng: **A** (giao diện chung), **M** (button action).
   Nhóm còn lại: tick theo field type thực tế.

3. **Xác định các luồng nghiệp vụ:** Happy Path, Negative Path, Boundary Cases

4. **Áp dụng kỹ thuật thiết kế test case:**
   - Equivalence Partitioning (EP)
   - Boundary Value Analysis (BVA)
   - Decision Table (nếu có nhiều rules)
   - State Transition (nếu có workflow)

5. **Sinh test cases theo 2 luồng:**

   **5a — Common TCs** (từ checklist, sinh trước):
   - Chỉ đọc các nhóm đã tick ở Bước 2
   - Nhóm D — TEXT: bắt buộc đủ **38 cases** = D01–D21 (Nhập keyboard) + D05cp–D21cp (Copy-paste Ctrl+V) cho mỗi trường Textbox. **QUY TẮC CỐT LÕI: Textbox TUYỆT ĐỐI KHÔNG CÓ case "Kiểm tra nhập tìm kiếm"** (nghiệp vụ tìm kiếm thuộc Section Chức năng hoặc Button Tìm kiếm; D22–D28 chỉ áp dụng cho Dropdown/Combobox searchable popup); ID Copy-paste dùng range 500+
   - Nhóm H — Dropdown: **MỌI trường đều PHẢI có đủ H01–H12** (bao gồm H03 placeholder, H04 bỏ trống, H05 options, H06 keyboard focus, scroll 3 TH, chọn giá trị 3 sub, search nếu có). **NGHIÊM CẤM** cắt bớt case cho dropdown thứ 2 trở đi
   - TC có `(tùy spec)` → xác định expected result từ requirements
   - **Format ID:** `[FEATURE]_[SỐ]` (VD: `M1_001`)

   **5b — Business TCs** (nghiệp vụ đặc thù, sinh sau):
   - Happy Path, Alternate Paths, Exception Paths
   - Các kịch bản đặc thù không được bao phủ bởi Common TCs
   - **Format ID:** `[FEATURE]_[SỐ]` (VD: `M1_001`)

   **⚠️ Self-check bắt buộc sau mỗi module:**
   - **CHECK 1 — Dropdown đủ case:** MỌI dropdown đều có đủ H01-H06 + scroll 3 TH + chọn giá trị 3 sub + search nếu có
   - **CHECK 2 — Button Xuất Excel:** Nếu màn hình có nút Xuất Excel → phải có subsection button 3 TC
   - **CHECK 3 — tc_sub tên unique:** Không có 2 tc_sub trùng tên trong cùng tc_group

   Đảm bảo đủ fields cho mỗi TC:
   - TC ID, Module, Test Scenario / Title, Pre-conditions
   - Test Steps (đánh số), Expected Results (đánh số tương ứng)
   - Test Data (**phải cụ thể**, không placeholder), Priority

6. **TC Lead Review Gate (BẮT BUỘC trước khi xuất bảng final)**

   > Xem chi tiết tại SKILL.md → mục **Bước 5b: TC Lead Review Gate**.

   Agent tự rà soát bộ TC vừa sinh theo 6 tiêu chí: **Coverage, Clarity, Accuracy, Feasibility, Organization, Traceability & RBT**.
   - Xuất file `practices/testcases/<DU_AN>/tc_review_<module>.md` liệt kê GAP + đề xuất hành động
   - ⚠️ **DỪNG — Chờ user tích chọn** cho từng GAP (Bổ sung / Sửa / Bỏ qua + lý do)
   - Sau khi user confirm → xử lý hành động → merge thành **bộ TC final**

7. **Xuất bảng Markdown chuẩn (final)**

   Đóng gói bộ TC final (đã qua Review Gate) vào bảng Markdown chuẩn. Sắp xếp: UI → CMN → BIZ. Không bỏ sót TC nào.

8. **Excel Export (tùy chọn)**

   Nếu user yêu cầu xuất Excel, tạo file `scripts/gen_tc_<ten_chuc_nang>.py` dùng module `scripts/tc_excel_writer.py` (xem rule `manual_tc_excel_export.md`).

    **Convention bắt buộc khi viết script:**
   - Import: `from tc_excel_writer import section, subsection, tc, tc_group, tc_sub, tc_item, FeatureSpec, generate_excel`
   - **Nhóm D TEXT field → BẮT BUỘC dùng `tc_group()` (MẶC ĐỊNH, không cần user yêu cầu):**
     - D01-D04 (tĩnh): dùng `tc()` riêng lẻ bình thường
     - D05-D21 (nhập keyboard): dùng `tc_group("Kiểm tra khi nhập giá trị", [tc_sub("Kiểm tra nhập maxlength", [...]), ...])` — **17 tc_item**
     - D05cp-D21cp (copy-paste): dùng `tc_group("Kiểm tra khi copy/paste giá trị", [...])` — **17 tc_item**
   - **Nhóm E (Number field) → BẮT BUỘC dùng `tc_group()` (MẶC ĐỊNH):**
     - E01-E04 (tĩnh): dùng `tc()` riêng lẻ bình thường
     - E05-E23 (nhập keyboard): dùng `tc_group("Kiểm tra khi nhập giá trị", [tc_sub("Kiểm tra nhập maxlength", [...]), ...])` — **19 tc_item**
     - E05cp-E23cp (copy-paste): dùng `tc_group("Kiểm tra khi copy/paste giá trị", [...])` — **19 tc_item**
   - **Nhóm H (Dropdown) / J (Multiselect) → BẮT BUỘC dùng `tc_group()` (MẶC ĐỊNH):**
     - H07-H09 / J11-J13 (scroll): dùng `tc_group("Kiểm tra hiển thị scroll", [tc_sub("TH số bản ghi < 5"), ...])`
     - H10-H12 / J07-J10 (chọn giá trị): dùng `tc_group("Kiểm tra chọn giá trị", [...])`
     - H13-H16 (API states): dùng `tc_group("Kiểm tra options hiển thị đúng", [...])` (Áp dụng cho CẢ Dropdown và Multiselect)
     - D24-D28 (nhập tìm kiếm trong dropdown): dùng `tc_group("Kiểm tra nhập tìm kiếm", [...])`
   - Section BIZ: `section("Chức năng (Phần này viết các trường hợp kiểm thử kiểm tra các ràng buộc trong cơ sở dữ liệu và cho các luồng nghiệp vụ trong tài liệu giải pháp, tích hợp với các chức năng khác)")`
   - Subsection BIZ (tạo khi có TC): `"Kiểm tra <tên> thành công"` / `"Kiểm tra <tên> không thành công"` / `"Kiểm tra phân quyền"`
   - **Subsection button** — mỗi button action có 1 subsection riêng `"Kiểm tra button <Tên Button>"`, bên trong **ít nhất 3 TC chuẩn**: `hiển thị` / `trạng thái` / `onclick` (có thể thêm M04, M05). Xem cấu trúc đầy đủ tại `.agent/rules/manual_tc_excel_export.md`
   - `subsection()` control: dùng `"Nhóm X — Tên field (constraints)"` — writer tự strip prefix và constraints, hiển thị `"Kiểm tra tên field"`
   - `muc_dich` trong `tc()`: dùng `"Mx_NNN - mô tả chữ thường"` — writer tự strip ID, thêm `"Kiểm tra "`. **KHÔNG** viết `"Kiểm tra ..."` trong code. **KHÔNG** dùng `→` — thay bằng `/` (nhiều mục đích) hoặc `"khi"` (điều kiện)

## Bảng Output

```
| TC ID | Mục đích kiểm thử | Trường hợp kiểm thử | Điều kiện tiên quyết | Test Data | Các bước thực hiện | Kết quả mong đợi | Priority |
```

- **Format TC ID:** `[FEATURE]_[SỐ]` (VD: `M1_001`, `Login_001`)
- **Phân loại TC (tổ chức nội bộ, không phải cột):** `UI` (Giao diện) / `CMN` (Common) / `BIZ` (Business)
- Sắp xếp: Giao diện (UI) → Common TCs (CMN) → Business TCs (BIZ)

## Quy tắc quan trọng

- Test Data phải cụ thể: `test_login_01@domain.com`, không phải "email hợp lệ"
- Phải bao gồm cả Positive, Negative, và Boundary cases
- TC ID theo format thống nhất do user quy ước hoặc mặc định
- Nếu quá nhiều TCs → chia thành Part 1, Part 2 và hỏi user
- **KHÔNG bỏ qua Common TC Checklist** dù là QUICK mode — đây là tiêu chuẩn bắt buộc
- **KHÔNG bỏ qua TC Lead Review Gate** — NGHIÊM CẤM xuất file khi chưa có xác nhận user

## Khi nào chuyển sang FULL RBT

Agent **tự động đề xuất chuyển mode** nếu phát hiện:
- Requirements mơ hồ, cần hỏi Q&A
- Scope lớn (>3 modules)
- Logic nghiệp vụ phức tạp, nhiều điều kiện chồng chéo
- User yêu cầu Traceability Matrix hoặc Risk Assessment