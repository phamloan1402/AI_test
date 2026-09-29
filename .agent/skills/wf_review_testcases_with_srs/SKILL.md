---
name: wf_review_testcases_with_srs
description: "Review kịch bản test đã có so với SRS — phân tích coverage theo common_tc_checklist và kiểm tra đủ logic nghiệp vụ + tích hợp liên module. Output là file báo cáo .md liệt kê GAPs và gợi ý bổ sung. Use when the user invokes WF_review_testcases_with_srs, /review_testcases_with_srs, or asks to run this workflow."
---

# WF_review_testcases_with_srs

## Cross-agent compatibility contract

- Run on Codex, Claude, Gemini/Google, or any agent capable of reading Markdown and operating on the repository.
- Resolve relative paths from the repository root. Do not depend on a vendor-specific installation directory.
- Map tool names in this workflow to equivalent available capabilities such as browser, shell, file operations, Jira, and Confluence. Do not skip a step only because a tool has a different name.
- Follow `AGENTS.md` and any agent-specific instruction file. If instructions conflict, prioritize security and repository-level rules.
- Never read `.env` files directly. Only check their existence or invoke a process designed to load environment variables internally.

## Dependent skills

- `.agent/skills/rbt_manual_testing/SKILL.md`
- `.agent/skills/srs_qa_architect/SKILL.md`

If the workflow below names additional mandatory skills or references, read them before execution. On agents without native skill invocation, open the corresponding `SKILL.md` directly and follow it.

## Original workflow

# Workflow: Review Test Cases so với SRS

Workflow này giúp **rà soát bộ test cases đã có** (file `.md` hoặc `.xlsx`) đối chiếu với SRS (Confluence), phát hiện các gaps về:
1. **Coverage theo common_tc_checklist** — kiểm tra đủ các case validate UI, field types (Nhóm A–W)
2. **Logic nghiệp vụ và tích hợp** — kiểm tra các luồng BIZ, ràng buộc DB, tích hợp liên module

---

## ⚠️ Nguyên tắc

- **Không tự ý sửa file test case gốc** — chỉ sinh báo cáo review, chờ user confirm trước khi merge
- **Dừng 1 lần** tại Review Checkpoint (Bước 4) để user confirm từng GAP
- **Input từ Confluence** — lấy SRS qua `confluence_get_page` với Page ID do user cung cấp
- **Test case nguồn** — có thể là file `.md` hoặc `.xlsx` trong workspace
- Tất cả output bằng **Tiếng Việt**

---

## Các bước thực hiện

### Bước 1 — Thu thập đầu vào

1. **Lấy SRS từ Confluence:**
   - Yêu cầu user cung cấp **Page ID hoặc URL** của tài liệu SRS
   - Gọi `mcp_Atlassian_confluence_get_page` với page ID đó
   - Nếu SRS có nhiều trang con → hỏi user cần lấy những trang nào (dùng `confluence_get_page_children` để liệt kê)
   - Lưu nội dung SRS vào biến nội bộ (KHÔNG lưu ra file temp)

2. **Xác định file test case cần review:**
   - Hỏi user: file test case hiện có ở đâu? (path file `.md` hoặc `.xlsx`)
   - Đọc file test case đó (dùng `view_file` hoặc `read_file`)
   - Nếu là `.xlsx` → đọc bằng script Python để parse nội dung

3. **Xác định scope review:**
   - Hỏi user: Review toàn bộ module hay chỉ một số module cụ thể?
   - Xác nhận tên feature/module để đặt tên file output

---

### Bước 2 — Phân tích SRS → Field Inventory

Đọc SRS và lập **Field Inventory** — danh sách toàn bộ fields/controls/chức năng trên màn hình:

| Tên Field / Control | Loại | Bắt buộc? | Ràng buộc | Nhóm TC áp dụng |
|---|---|---|---|---|
| *(từ SRS)* | TEXT / NUMBER / DATE / DROPDOWN / CHECKBOX / ... | Yes/No | maxlength, min/max, format... | D / E / H / K / ... |

**Nhóm luôn áp dụng (mọi màn hình):** A (Giao diện chung), M (Button action)

**Nhóm áp dụng theo field type** — dùng Bảng điều phối trong `common_tc_checklist.md`:

| Loại field | Nhóm TC |
|---|---|
| TEXT input | D |
| NUMBER input | E |
| EMAIL field | F |
| TEXTAREA | G |
| DROPDOWN / COMBOBOX | H |
| CHECKBOX | I |
| MULTISELECT | J |
| DATE / DATETIME | K |
| PASSWORD | L |
| RADIO | N |
| IP Address | O |
| Chức năng Xóa | P |
| File Upload | Q |
| Import | R |
| Phân quyền | S |
| Tìm kiếm nhiều trường | T |
| Grid có edit + thao tác | U |
| Grid + Paging | C |
| Panel collapse/expand | B |

---

### Bước 3 — Review Coverage (2 chiều)

#### 3A — Đối chiếu Common TC Checklist

Tham chiếu file: `.agent/skills/rbt_manual_testing/references/common_tc_checklist.md`

Với **từng nhóm TC đã xác định** ở Bước 2, kiểm tra bộ TC hiện có đã cover đủ chưa:

**Nhóm A — Giao diện chung** (6 TC bắt buộc):
- [ ] A01 — Màn hình mặc định
- [ ] A02 — Tổng thể giao diện (bố cục, font, dấu *, chính tả)
- [ ] A03 — Tab order tiến ⚠️ *thường bị thiếu*
- [ ] A04 — Tab order lùi (Shift+Tab) ⚠️ *thường bị thiếu*
- [ ] A05 — Phím Enter ⚠️ *thường bị thiếu*
- [ ] A06 — Responsive (Ctrl+−, Ctrl+=)

**Nhóm D — TEXT** (38 cases/field):
- 4 TC tĩnh: D01–D04
- 17 tc_item nhập keyboard: D05–D21 (gộp trong `tc_group`, bắt đầu bằng `tc_sub("Kiểm tra nhập maxlength")` 3 items BVA)
- 17 tc_item copy-paste: D05cp–D21cp (gộp trong `tc_group`, bắt đầu bằng `tc_sub("Kiểm tra copy/paste maxlength")` 3 items)
- *Dropdown/Combobox có ô search popup thêm:* D22–D28 (7 cases). Textbox KHÔNG có search cases.

**Nhóm E — NUMBER** (42 cases/field):
- 4 TC tĩnh: E01–E04
- 19 tc_item nhập keyboard: E05–E23 (gộp trong `tc_group`, bắt đầu bằng `tc_sub("Kiểm tra nhập maxlength")` 3 items BVA)
- 19 tc_item copy-paste: E05cp–E23cp (gộp trong `tc_group`, bắt đầu bằng `tc_sub("Kiểm tra copy/paste maxlength")` 3 items)

**Nhóm H — Dropdown** (15+ cases/field):
- H01–H06 (tĩnh), scroll 3 TH (H07-H09), chọn giá trị 3 sub (H10-H12), API states 4 sub (H13-H16)
- ⚠️ **MỌI dropdown đều phải đủ** — không được cắt bớt từ dropdown thứ 2 trở đi

**Nhóm C — Grid + Paging**:
- C01–C03, C05, C07, C09–C10 (tĩnh) + 3 tc_group phân trang + C11–C16 (QT component)

**Nhóm K — Date/DateTime**:
- K01–K17 (tùy spec — check case K01, K02, K08, K17 thường bị thiếu)

*(Lặp tương tự cho tất cả nhóm đã tick ở Field Inventory)*

**Khi phát hiện thiếu → ghi nhận GAP với format:**
```
GAP-CMN-[STT]: [Tên nhóm] — [Field/Control] thiếu [case ID]: [mô tả case]
Mức độ: HIGH / MEDIUM / LOW
Gợi ý: Bổ sung [N] TC theo mẫu checklist nhóm [X]
```

---

#### 3B — Đối chiếu Logic Nghiệp vụ và Tích hợp

Đọc SRS để xác định:

1. **Luồng chức năng chính (Happy Path)**
   - Hệ thống có ghi nhận đủ test case cho từng bước trong luồng chính chưa?
   - Ví dụ: Tạo → Duyệt → Phê duyệt → Kết thúc — mỗi bước phải có TC

2. **Luồng ngoại lệ (Exception Path)**
   - Các trường hợp lỗi theo rule nghiệp vụ: trùng mã, vượt hạn mức, sai trạng thái...
   - Các ràng buộc DB: unique constraint, foreign key, not null theo SRS

3. **Ràng buộc nghiệp vụ (Business Rules)**
   - Mỗi Business Rule trong SRS (thường ký hiệu BUS-XXX hoặc BR-XXX) → phải có ít nhất 1 TC positive + 1 TC negative
   - Kiểm tra TC nào chưa map với BR nào

4. **Tích hợp liên module**
   - SRS đề cập module nào liên quan? (VD: A phụ thuộc B, C trigger D...)
   - TC tích hợp: thay đổi ở module X → kiểm tra ảnh hưởng module Y
   - Kiểm tra: bộ TC hiện có đã có TC integration chưa?

5. **Phân quyền (nếu SRS đề cập)**
   - Nhóm S — mỗi chức năng có quyền → phải có S01 (có quyền) + S02 (không có quyền)

6. **Workflow / State Machine**
   - Nếu chức năng có trạng thái (draft/pending/approved/rejected...) → đủ TC chuyển trạng thái hợp lệ và bất hợp lệ

**Khi phát hiện thiếu → ghi nhận GAP với format:**
```
GAP-BIZ-[STT]: [Loại gap] — [Mô tả ngắn]
Business Rule tham chiếu: BUS-XXX / BR-XXX (nếu có)
Module liên quan: M1, M3...
Mức độ: HIGH / MEDIUM / LOW
Gợi ý: [Hành động cụ thể để bổ sung]
```

---

### Bước 4 — Review Checkpoint *(DỪNG — Chờ user confirm)*

Sau khi phân tích xong, AI xuất **Báo cáo Review Draft** ra file:

```
practices/testcases/<DU_AN>/tc_review_<FeatureName>_srs_gap.md
```

**Cấu trúc file báo cáo:**

```markdown
# TC Review Report — [Tên chức năng]

> **SRS Source:** Confluence Page ID [XXXX]
> **Test Case file:** [đường dẫn file TC]
> **Reviewer:** AI TC Lead
> **Ngày review:** YYYY-MM-DD

---

## Tóm tắt

| Hạng mục | Tổng GAP | HIGH | MEDIUM | LOW |
|---|---|---|---|---|
| Common TC Coverage | N | N | N | N |
| Logic Nghiệp vụ | N | N | N | N |
| Tích hợp liên module | N | N | N | N |
| **TỔNG** | **N** | **N** | **N** | **N** |

---

## GAPs — Common TC Coverage

| GAP ID | Nhóm | Field/Control | Cases thiếu | Mức độ | Gợi ý |
|---|---|---|---|---|---|
| GAP-CMN-001 | D | Trường Tên | D11, D12, D13, D14, D16, D20, D21 (thiếu 7 cases nhập) | HIGH | Bổ sung vào tc_group "Kiểm tra khi nhập giá trị" |
| ... | | | | | |

### Hành động đề xuất cho từng GAP-CMN

Với mỗi GAP, user chọn 1 trong:
- [ ] **Bổ sung** — AI sẽ sinh TC bổ sung vào bộ TC
- [ ] **Bỏ qua** — Ghi N/A + lý do
- [ ] **Hỏi thêm** — Cần làm rõ với BA/PO

---

## GAPs — Logic Nghiệp vụ và Tích hợp

| GAP ID | Loại | Mô tả | BR tham chiếu | Module | Mức độ | Gợi ý |
|---|---|---|---|---|---|---|
| GAP-BIZ-001 | Happy Path | Thiếu TC luồng phê duyệt 2 cấp | BUS-045 | M3, M5 | HIGH | Bổ sung 3 TC: phê duyệt cấp 1, cấp 2, đủ 2 cấp |
| ... | | | | | | |

### Hành động đề xuất cho từng GAP-BIZ

Với mỗi GAP, user chọn 1 trong:
- [ ] **Bổ sung** — AI sẽ sinh TC bổ sung
- [ ] **Sửa TC hiện có** — AI sẽ cập nhật nội dung TC đang có
- [ ] **Bỏ qua** — Ghi lý do
- [ ] **Cần làm rõ** — Cần hỏi BA/PO thêm
```

> ⚠️ **DỪNG TẠI ĐÂY — Chờ user tích chọn hành động cho từng GAP**
>
> AI không được tự ý bổ sung hoặc sửa TC khi chưa có xác nhận.

---

### Bước 5 — Xử lý GAPs theo xác nhận của user

Sau khi user confirm từng GAP:

1. **GAP được chọn "Bổ sung":**
   - Sinh TC mới theo format bảng Markdown chuẩn
   - Đặt ID tiếp theo từ ID lớn nhất hiện có trong module
   - Ghi rõ TC mới là bổ sung cho GAP nào

2. **GAP được chọn "Sửa TC hiện có":**
   - Chỉ ra TC ID cần sửa, field nào thay đổi, expected result mới

3. **GAP được chọn "Bỏ qua":**
   - Ghi `N/A` vào cột ghi chú + lý do user cung cấp

4. **GAP được chọn "Cần làm rõ":**
   - Ghi vào danh sách câu hỏi mở, để user follow-up với BA/PO

---

### Bước 6 — Xuất báo cáo final

Cập nhật file báo cáo review với kết quả xử lý:

```markdown
## Kết quả Review Gate

| Tiêu chí | Trạng thái | GAPs đã xử lý |
|---|---|---|
| Common TC Coverage | ✅ / ⚠️ Còn mở | X/Y |
| Logic Nghiệp vụ | ✅ / ⚠️ Còn mở | X/Y |
| Tích hợp liên module | ✅ / ⚠️ Còn mở | X/Y |

## Số liệu TC trước/sau review

| Module | TC trước | TC sau | Chênh lệch |
|---|---|---|---|
| M1 | N | N | +N |
| ...| | | |
| **TỔNG** | **N** | **N** | **+N** |

## GAPs chưa xử lý (cần theo dõi)

| GAP ID | Lý do chưa xử lý | Người theo dõi |
|---|---|---|
| ... | | |
```

---

## Quy tắc quan trọng

- **NGHIÊM CẤM** đọc trực tiếp file `.env` để lấy credentials
- **NGHIÊM CẤM** tự ý sửa file TC gốc khi chưa có xác nhận user tại Bước 4
- Nếu SRS thiếu thông tin để đánh giá GAP → ghi `"Cần làm rõ"` thay vì đoán
- Nếu file test case quá lớn (>1000 TC) → hỏi user muốn review module nào trước
- Mỗi GAP phải có **mức độ** rõ ràng: HIGH (ảnh hưởng nghiệp vụ chính), MEDIUM (ảnh hưởng một phần), LOW (tối ưu thêm)
- **Tích hợp liên module** → ưu tiên HIGH khi dữ liệu từ module A là input bắt buộc của module B

---

## File output

```
practices/testcases/<DU_AN>/tc_review_<FeatureName>_srs_gap.md
```

**Đặt tên:** `tc_review_<FeatureName>_srs_gap.md` — phân biệt với file `tc_review_<FeatureName>.md` (là review gate sau khi sinh TC mới)

---

## Khi nào dùng workflow này

| Tình huống | Dùng workflow này? |
|---|---|
| Vừa sinh TC xong, muốn review nhanh trước khi submit | ✅ Có |
| Có SRS mới/cập nhật, cần kiểm tra TC cũ còn phù hợp không | ✅ Có |
| Muốn sinh TC mới từ đầu | ❌ Dùng `/generate_testcases_from_requirements` |
| Muốn review TC không có SRS (chỉ dựa trên giao diện) | ❌ Ngoài phạm vi project AI_test |
