---
name: wf_generate_manual_testcases_rbt
description: "Sinh manual test cases chất lượng cao theo quy trình AI-RBT 7 bước (Risk-Based Testing) từ requirements. Use when the user invokes WF_generate_manual_testcases_rbt, /generate_manual_testcases_rbt, or asks to run this workflow."
---

# WF_generate_manual_testcases_rbt

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

# Workflow: Sinh Manual Test Cases — FULL RBT Mode

> **BẮT BUỘC:** Đọc skill `.agent/skills/rbt_manual_testing/SKILL.md` (Mode FULL RBT) trước khi bắt đầu.

## ⚠️ Nguyên tắc

- **7 bước tuần tự** — KHÔNG gộp bước
- **PHẢI dừng chờ user xác nhận** tại: B1, B2 (Q&A), B4 (Scenarios), B5b (Review Gate)
- **NGHIÊM CẤM tự tiến sang bước tiếp theo** khi chưa có phản hồi rõ ràng từ user tại các checkpoint
- Output bằng **Tiếng Việt có dấu đầy đủ** (Unicode) — NGHIÊM CẤM viết tiếng Anh hoặc bỏ dấu tiếng Việt trong nội dung TC
- **B3b:** Tham chiếu `references/common_tc_checklist.md`
- **Đọc tài liệu:** BẮT BUỘC đọc **toàn bộ** nội dung mỗi tài liệu (Confluence page, PDF, spec) trước khi định nghĩa scope — KHÔNG kết luận dựa trên tiêu đề, TOC, hoặc đọc không đầy đủ

## 💾 State File

**Path:** `practices/testcases/<DU_AN>/<FeatureName>_rbt_state.md`

Tồn tại → đọc + hỏi tiếp tục | Không → tạo mới, bắt đầu B1.

| Sau bước | Nội dung lưu |
|---|---|
| B1 | Context xác nhận |
| B2 | Q&A + assumptions + **file Q&A** (`practices/Q&A/<FeatureName>_QA.md`) |
| B3 | Modules + Field Inventory + Common TC groups |
| **B4** | **Traceability + scenarios APPROVED ← điểm khôi phục** |
| B5 | TC count/module |
| B7 | Script + xlsx path + tc_count final |

### 📝 Work Log & Memory (khi user duyệt checkpoint)

> Nguồn chuẩn: `.agent/rules/worklog_memory_rules.md` — **BẮT BUỘC đọc tại thời điểm trigger**, không ghi theo trí nhớ.

- **Đầu session tiếp nối feature đã có:** đọc `practices/worklog/PROJECT_MEMORY.md` → `memory/<slug>_MEMORY.md` → tối đa 3 bản ghi Work Log gần nhất (§6), cùng với state file.
- **Tại checkpoint (B1, B2, B4, B5b; QUICK: TC Lead Review Gate):** khi user xác nhận **có nêu scope** (VD: *"duyệt B2 Q&A"*, `/pass B4`) → ghi `PASS`/`PARTIAL` vào `practices/worklog/<slug>_WORKLOG.md` + cập nhật Memory. `ok`/`xong` đứng một mình **không** phải trigger → hỏi lại scope.
- **Requirement/spec mới tác động nội dung đã duyệt:** ghi `REOPEN` (chưa duyệt → `Approval: PENDING`, change=`PENDING_REVIEW`, nội dung vào `practices/Q&A/<slug>_QA.md`).
- **Đối soát:** pipeline state trong Memory lấy `<FeatureName>_rbt_state.md` làm chuẩn; **không bao giờ** xóa change state khi đối soát.
- Báo cáo kết quả ghi trong **Tier 3 — Execution & Audit Summary**.

## Các bước

### B1: Context & Role-play

> [!IMPORTANT]
> **PRE-B1 — Đọc tài liệu bắt buộc trước khi viết bất cứ điều gì:**
> Với MỌI tài liệu yêu cầu (Confluence page, PDF, spec file): **ĐỌC TOÀN BỘ NỘI DUNG** từ đầu đến cuối. KHÔNG được:
> - Kết luận "màn hình X không có tab/bảng Y" chỉ từ TOC hoặc đọc lướt
> - Bỏ qua phần nội dung vì "có vẻ" lặp lại phần trước
> - Tóm tắt scope dựa trên tiêu đề section mà chưa đọc body

Xác nhận context, tóm tắt scope đầy đủ đến cấp **màn hình → tab → từng bảng/sub-component**.

**⏸ DỪNG HOÀN TOÀN — Chờ user xác nhận scope.**
> ❌ NGHIÊM CẤM tự tiến sang B2 khi chưa nhận được phản hồi rõ ràng từ user ("OK", "đúng rồi", "tiếp tục", v.v.)
> ✅ Chỉ được tiến sang B2 khi user reply xác nhận

💾 Tạo `_rbt_state.md` (sau khi user confirm).

### B2: Analysis & QnA
**BẮT BUỘC tái sử dụng skill `srs_qa_architect`:** đọc `.agent/skills/srs_qa_architect/SKILL.md`, `references/checklist-review.md`, `references/Ambiguity.md` và `references/deep-logic-review.md`; dùng skill này làm nguồn chuẩn cho phân tích Happy/Alternate/Exception Paths, Ambiguities, Testability, Q&A Cross-Cutting, Assumption và format artifact.
**Adapter FULL RBT:** lưu Q&A vào `practices/Q&A/<FeatureName>_QA.md`, giữ schema Quality Gate + Q&A có cột `Câu trả lời`, cập nhật state B2=PENDING cùng verdict và Q-ID chưa giải quyết. Áp dụng đầy đủ các lượt phân tích sâu và cơ chế handoff ở B2 của master skill. Không duy trì checklist Q&A riêng trong workflow.

**Quy tắc bảng Q&A findings (schema chung — nguồn duy nhất là `srs_qa_architect`, workflow này chỉ trỏ tới, không mở rộng):**

**0. Truy vết `checklist-review.md` — BẮT BUỘC, theo schema chung của `srs_qa_architect`.**

> ⚠️ **Không nhầm hai checklist:** B2 dùng `srs_qa_architect/references/checklist-review.md` (96 tiêu chí, 19 nhóm review SRS, mã tiền tố `CR-`). **NGHIÊM CẤM** dùng nhóm của `common_tc_checklist.md` (A Giao diện chung, D Textbox, H Dropdown, M Button...) ở B2 — checklist đó chỉ dùng từ B3b.

- Áp dụng nguyên văn schema **Full Review** trong `.agent/skills/srs_qa_architect/SKILL.md` (§4 và §5): mục `1. Coverage và applicability` đủ **19 nhóm `CR-A` → `CR-S`**, cột **`Mã checklist`** cho mọi Q-ID, và **Self-check (a)–(d)** trước khi dừng B2. Không định nghĩa lại schema tại đây.
- Nếu `practices/Q&A/<FeatureName>_QA.md` đã được tạo trước bởi `/analyze_srs_qa`: tái sử dụng file đó (cùng schema), chỉ chạy lại self-check và bổ sung phần thiếu theo trọng tâm FULL RBT.

**1–2. Cột `Vấn đề & Rủi ro` và `Assumption / Options`:** áp dụng đúng quy tắc định dạng tại `.agent/skills/srs_qa_architect/SKILL.md` §4 (4 ý bắt buộc cho `Vấn đề & Rủi ro`; Option A/B/(C) + dòng `>> Chọn Option X vì: <lý do>`, rủi ro cao kèm `⚠️ Cần BA/PO quyết định`). Không định nghĩa lại tại đây.

**Ràng buộc riêng của pipeline:** khi user phản hồi `Dùng assumptions, tiếp tục B3`, phương án ở dòng **>> Chọn Option X vì** của từng Q-ID được dùng làm assumption; ghi rõ vào state B2. Q-ID có `⚠️ Cần BA/PO quyết định` **không** được dùng làm assumption khi chưa có câu trả lời BA/PO.

**⏸ DỪNG — Chờ user trả lời.**

### B3: Decomposition + Field Inventory

**3a — Phân rã:** Chia thành Modules/Sub-modules + Dependencies.

**3b — Field Inventory & Common TC Mapping** *(bắt buộc, tham chiếu `common_tc_checklist.md`)*:
- **3b.1:** Liệt kê fields/controls (tên, loại, required, constraint). Types: `TEXT/NUMBER/DATE/CBB/DROPDOWN/MULTISELECT/MULTISELECT+SEARCH/CHECKBOX/RADIO/TEXTAREA/FILE/LABEL`
- **3b.2:** Tick nhóm Common TC qua Bảng điều phối. **A + M** luôn bắt buộc
- **3b.3:** Lưu nhóm + field cụ thể → dùng ở B5

> **Nhóm D (TEXT):** 38 cases/field = D01–D04 + D05–D21 (keyboard) + D05cp–D21cp (paste). **QUY TẮC CỐT LÕI: Textbox TUYỆT ĐỐI KHÔNG CÓ case "Kiểm tra nhập tìm kiếm"** (nghiệp vụ tìm kiếm thuộc Section Chức năng hoặc Button Tìm kiếm; D22–D28 chỉ áp dụng cho Dropdown/Combobox searchable popup). ID: keyboard liền mạch, copy-paste 500+.
> **Nhóm G (TEXTAREA):** 41 cases/field = D01–D04 (4) + tc_group D05–D21 keyboard **17 item** (bao gồm 3 BVA) + tc_group D05cp–D21cp paste **17 item** + G07 + G11 + G12 (3). KHÔNG được chỉ cộng +3 mà bỏ tc_group. NGHIÊM CẤM tách Nhóm G ra sheet riêng.

### B4: Traceability & High-Level Scenarios

**BẮT BUỘC xây dựng Ma trận truy vết 4 tầng (4-Layer Traceability Matrix) — KHÔNG được tóm tắt sơ sài:**

1. **Tầng 1 — Functional & Use Cases:** Map 100% Use Cases (`UC-xxx`) / Features với Module và Tiêu chí nghiệm thu (Acceptance Criteria).
2. **Tầng 2 — 100% Business Rules & Mã thông báo (QUAN TRỌNG):**
   - Mỗi Business Rule (`BR-xxx`) là 1 dòng độc lập. **NGHIÊM CẤM gộp dải `BR-001→008`**.
   - Ánh xạ 100% mã thông báo (`ERR_xxx`, `WAR_xxx`, `SUC_xxx`, `CONF_xxx`) sang kịch bản test tương ứng.
3. **Tầng 3 — Ma trận phân quyền RBAC:**
   - Đủ 100% thao tác × toàn bộ các vai trò (Roles) trong tài liệu.
   - Bắt buộc kiểm tra hành vi UI khi không có quyền (ẩn nút hay disabled control).
4. **Tầng 4 — Non-Functional, State Machine & Shared Components:**
   - Sơ đồ chuyển trạng thái đối tượng nghiệp vụ (hợp lệ và bất hợp lệ).
   - Yêu cầu phi chức năng: Hiệu năng (SLA), Bất đồng bộ (non-blocking UI), Responsive UI.
   - Component dùng chung: Popover ẩn/hiện cột, Xuất Excel, Lịch sử audit.

**High-Level Scenarios:** Liệt kê đầy đủ các kịch bản theo từng Module (Happy, Alternate, Exception, Concurrency).

**Anti-patterns B4 (NGHIÊM CẤM):**
- ❌ Gộp dải BR (`BR-001→008`) thay vì liệt kê từng dòng đối chiếu 1-1.
- ❌ Bỏ sót mã thông báo hệ thống / mã lỗi chưa có scenario kiểm thử.
- ❌ Bỏ qua ma trận phân quyền (RBAC) hoặc chỉ kiểm tra vai trò có quyền mà bỏ qua vai trò bị chặn.
- ❌ Bỏ qua sơ đồ chuyển trạng thái (State Machine) và yêu cầu phi chức năng (NFR).

**⏸ DỪNG HOÀN TOÀN — Chờ user review và phê duyệt 4 tầng Traceability Matrix + Scenarios.**
💾 B4 = APPROVED (sau khi user confirm).

### B5: RBT & TC Generation

> **Chế độ:** ≤2 modules + ≤80 TC → **FULL** (Markdown → B6 → B7) | Ngược lại → **COMPACT** (summary + ghi thẳng script Python, bỏ B6)

Đánh giá Risk Level. Áp dụng EP, BVA, Decision Table, State Transition (định nghĩa & cách áp dụng: `.agent/skills/rbt_manual_testing/references/test_design_techniques.md`). Test Data cụ thể.

**5a — Common TCs:** Sinh theo nhóm đã tick ở B3b. Format ID: `[FEATURE]_[SỐ]`.
- Mỗi field cùng loại → subsection riêng, BVA độc lập
- Nhóm D: D01–D21 keyboard trước → D05cp–D21cp paste sau. D07cp = truncate (không block)

**Self-check bắt buộc (CHECK 1–12):**
1. **Dropdown đủ case:** MỌI dropdown có H01–H06 + scroll 3 Trường hợp + chọn giá trị 3 sub + search nếu có + **H13–H16 API states dùng `tc_group`** (3 tc_sub: Trường hợp call API thành công/2 item, thất bại, timeout)
2. **Button Xuất Excel:** Có nút → phải có subsection 3 TC; nếu popup có nhiều action con → mỗi action con là 1 subsection riêng
3. **tc_sub tên unique:** Không trùng trong cùng tc_group
4. **Grid U02:** MỌI cột có U01–U04 đủ; U02 **BẮT BUỘC** kể cả cột readonly ("không mở edit mode")
5. **Phân trang tc_group:** Đã dùng 3 tc_group → KHÔNG có tc() riêng C04/C06/C08
6. **Nhóm A đủ 6 TC:** MỌI module/màn hình (kể cả popup) có đủ A01–A06 — A03 (Tab tiến), A04 (Shift+Tab), A05 (Enter) thường bị thiếu nhất
7. **Grid (C) đủ case:** Có C02 (STT tăng dần), C03 (ẩn paging ≤10), C05 (format chuỗi), C07 (header ổn định), C09 (action trang N → quay trang 1), C10 (xóa cuối trang cuối → quay N−1) + QT: C11–C16
8. **Multi-select (J) đủ case:** MỌI J có đủ J01–J06 (tĩnh) + J14 (bàn phím) + tc_group chọn (4 sub, bao gồm J10b bỏ chọn bằng dấu x nếu QT component) + tc_group scroll (3 sub) + tc_group API states (3 sub); NGHIÊM CẤM cắt bớt cho field 2+
9. **DatePicker (K) đủ case:** Có K01 (focus trống), K02 (focus có giá trị), K08 (29/02 năm nhuận), K17 (<01/01/1900) + K15–K16 (QT); RangePicker thêm K12–K14; Nếu SRS giới hạn khoảng ngày tối đa → thêm 3 TC BVA khoảng ngày
10. **Không tách thành phần chung (M0):** Nếu màn hình có nhiều file/tab độc lập (VD: D10, D12, D31...), mỗi sheet phải chứa đầy đủ các thành phần chung (button, Nhóm G, Nhóm S). NGHIÊM CẤM tạo sheet/module riêng chứa thành phần chung.
11. **Giới hạn ký tự (BVA):** Các case kiểm tra biên nhập/max length (D05, D06, D07, E05, E06, E07) **BẮT BUỘC** nằm trong `tc_group("Kiểm tra khi nhập giá trị")` (sử dụng `tc_sub`), KHÔNG được khai báo tĩnh bằng `tc()` riêng lẻ bên ngoài.
12. **Checkbox Mandatory disabled:** Nếu có checkbox luôn checked+disabled (không thể bỏ tick), PHẢI có `tc()` riêng kiểm tra 3 điểm: hiển thị đúng trạng thái, không bỏ được tick, giá trị vẫn submit khi save. Tham chiếu I10 từ Nhóm I (`common_tc_checklist.md`).
13. **Button trên Hộp thoại xác nhận (CONF_*):** Khi một thao tác (Huỷ form khi đã có dữ liệu `ALT-01`, Xoá bản ghi, Phê duyệt, Từ chối, Tiếp nhận...) kích hoạt mở popup xác nhận `CONF_*` → **BẮT BUỘC** tạo riêng subsection cho từng nút và icon: Nút Đồng ý (3 TC), Nút Huỷ bỏ (3 TC), icon đóng X (2 TC).
14. **Cột Trường hợp kiểm thử (Col C) của Button:** BẮT BUỘC bắt đầu bằng `"Kiểm tra "`, TUYỆT ĐỐI KHÔNG để tiền tố mã `M01 — `, `M02 — `, `M03 — ` (VD: `Kiểm tra hiển thị nút Gửi yêu cầu`, `Kiểm tra trạng thái enable/disable của nút Gửi yêu cầu`, `Kiểm tra click nút Gửi yêu cầu`).
15. **Dropdown H06 (Sử dụng bàn phím):** BẮT BUỘC có đủ 5 bước phím chi tiết: (1) Tab/Shift-Tab focus vào dropdown, (2) Enter mở danh sách option, (3) Phím Up/Down di chuyển con trỏ, (4) Enter chọn giá trị, (5) Tab/Shift-Tab chuyển sang control tiếp theo.
16. **File Upload (Nhóm Q):** BẮT BUỘC chia thành 3 nhóm rõ rệt: (1) Kéo thả file vào dropzone, (2) Click button 'Chọn file' mở File Dialog, (3) Hiển thị danh sách file sau tải lên và các thao tác trên file (xem, tải về, xóa file, popup xác nhận xóa).
17. **Bám sát SRS trên Confluence — CẤM TỰ SUY DIỄN (Zero Invented Fields):** 100% chỉ đưa vào Field Inventory và kịch bản test các trường có trong spec. Tuyệt đối KHÔNG mang thói quen/logic sản phẩm khác áp đặt thêm trường (Upload file, checkbox cam kết). Nếu nghi ngờ thiếu -> đưa vào Q&A Bước 2.
18. **Bắt buộc qua Bước 5b (QA Lead Review Gate):** Đánh giá 6 tiêu chí chất lượng và xuất báo cáo `tc_review_<module>.md`, dừng tại checkpoint để User/Lead duyệt trước khi bàn giao.

**5b — Business TCs:** Happy/Alternate/Exception chưa bao phủ bởi Common.

### B5b: TC Lead Review Gate ⭐

> ⚠️ **CHECKPOINT BẮT BUỘC** — KHÔNG tự chuyển B6.

1. AI rà soát 6 tiêu chí: Coverage, Clarity, Accuracy, Feasibility, Organization, Traceability&RBT
2. Xuất `practices/testcases/<DU_AN>/tc_review_<module>.md` liệt kê GAP + đề xuất
3. **⏸ DỪNG — Chờ user xử lý GAP** (Bổ sung/Sửa/Bỏ qua+lý do)
4. User confirm → merge TC final

### B6: Template Mapping
> Bỏ qua khi COMPACT mode.

Đóng gói TC vào bảng Markdown chuẩn. Sắp xếp: UI → CMN → BIZ.

### B7: Excel Export

> **BẮT BUỘC dùng `scripts/tc_excel_writer.py`.** Xem rule `manual_tc_excel_export.md`.

Tạo `scripts/gen_tc_<name>.py`:

**Quy tắc tc_group (MẶC ĐỊNH):**

| Nhóm | Tĩnh (`tc()`) | Hành vi (`tc_group()`) |
|---|---|---|
| D TEXT | D01–D04 (`tc()` riêng) | D05–D21 keyboard (**17 item**, bắt đầu sub BVA maxlength) + D05cp–D21cp paste (**17 item**) |
| E NUMBER | E01–E04 (`tc()` riêng) | E05–E23 keyboard (**19 item**, bắt đầu sub BVA maxlength) + E05cp–E23cp paste (**19 item**) |
| H Dropdown | H01–H06 | H07–H09 scroll, H10–H12 chọn, H13–H16 API states, D22–D28 search |
| J Multiselect | J01–J06 + J14 | J07–J10 chọn, J11–J13 scroll, H13–H16 API states, D22–D28 search |
| C Paging | C01–C03,C05,C07,C09–C16 | 3 tc_group: phân trang/combobox/nhập số trang |

**Quy tắc section/subsection:**
- Section UI: `section("Giao diện (Phần này viết...)")` — **PHẢI có** `subsection("Nhóm A — Giao diện chung")` đủ 6 TC A01–A06
- Section BIZ: `section("Chức năng (Phần này viết các trường hợp kiểm thử...tích hợp với các chức năng khác)")`
- Subsection BIZ: `"Kiểm tra <tên> thành công"` / `"...không thành công"` / `"Kiểm tra phân quyền"`
- Subsection button: `"Kiểm tra button <Tên>"` — **ít nhất 3 TC chuẩn**: hiển thị / trạng thái / onclick (có thể thêm M04, M05)
- Subsection control: `"Nhóm X — Tên field (constraints)"` — writer auto-strip
- **`muc_dich`**: viết **mô tả thuần chữ thường** — writer tự thêm `"Kiểm tra "` và strip bất kỳ prefix dạng `WORD_WORD - `. NGHIÊM CẤM viết `"Kiểm tra ..."` (lặp), hoa chữ đầu, dùng `→`, chèn ID vào `muc_dich` (mã biến sẽ lộ ra cột B)
- Grid U02 BẮT BUỘC cho mọi cột kể cả readonly

Chạy script → xuất `.xlsx`. 💾 B7 COMPLETED.

> **Tham khảo:** `manual_tc_excel_export.md` (rules + ví dụ), `scripts/gen_tc_quanlychucnang.py` (COMPACT example)

## Output

| Mode | Output |
|---|---|
| FULL | Markdown table + `.xlsx` + Traceability + state file |
| COMPACT | `.xlsx` + summary + state file |

File `.xlsx` → `practices/testcases/<DU_AN>/` | State → `<FeatureName>_rbt_state.md` | Q&A → `practices/Q&A/<FeatureName>_QA.md`
