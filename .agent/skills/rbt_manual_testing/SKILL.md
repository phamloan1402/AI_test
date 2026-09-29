---
name: RBT Manual Testing
description: Skill sinh manual test cases với 2 modes — QUICK (sinh nhanh từ requirements) và FULL RBT (quy trình AI-RBT 7 bước có đánh giá rủi ro + TC Lead Review Gate). Master skill cho mọi tác vụ manual test case.
---

# RBT Manual Testing

## Description

Đây là **Master Skill** cho mọi tác vụ sinh manual test cases. Skill cung cấp **2 chế độ hoạt động** (modes) để phù hợp với mọi quy mô yêu cầu:

| Mode | Khi nào dùng | Thời gian |
|------|-------------|-----------|
| **QUICK** | Sinh nhanh từ requirements rõ ràng | (2 bước)
| **FULL RBT** | Module phức tạp, cần phân tích rủi ro, hệ thống lớn | 7 bước tuần tự (có checkpoint) |

**Nguyên tắc cốt lõi:**
- **Human Strategy:** quyết định strategy, risk và tiêu chuẩn
- **AI Execution:** AI thực hiện phân tích, sinh TCs và rà soát lỗ hổng
- **AI Review (TC Lead Role):** AI đóng vai Test Lead, tự rà soát bộ TC vừa sinh trước khi xuất
- **Human Verification:** Con người xác nhận gap, chốt trước khi AI sinh bản final

---

## When to Use

Sử dụng skill này khi:

- Sinh manual test cases từ requirements
- Phân tích requirements để phát hiện ambiguity
- Phân rã hệ thống thành modules / features
- Xây dựng traceability matrix
- Áp dụng Risk-Based Testing (đánh giá rủi ro cho test cases)
- Chuẩn hóa test cases sang bảng Excel

**KHÔNG** sử dụng skill này khi:

- Cần sinh automation code, inspect DOM / sinh locator, hoặc chỉ sinh test data → **ngoài phạm vi project AI_test** (không có skill tương ứng)

---

## Mode Routing — Cách chọn mode

Agent tự động chọn mode dựa trên **trigger keywords** và **ngữ cảnh**:

### → Mode QUICK

Kích hoạt khi:
- User dùng workflow `/generate_testcases_from_requirements`
- User nói: "sinh test cases nhanh", "tạo TC nhanh từ requirement này"
- Requirements đã rõ ràng, scope nhỏ (1 module / 1 tính năng)
- User không yêu cầu phân tích rủi ro hay quy trình bài bản

### → Mode FULL RBT

Kích hoạt khi:
- User dùng workflow `/generate_manual_testcases_rbt`
- User nói: "quy trình 7 bước", "phân tích RBT", "sinh test cases đầy đủ", "sinh bộ TC bài bản"
- Scope lớn (nhiều modules, hệ thống phức tạp)
- User yêu cầu Traceability Matrix hoặc đánh giá Risk Level
- Requirements chưa rõ ràng, cần phân tích Ambiguity

### → Khi không rõ

Nếu không xác định được mode, agent **hỏi user**:
```
Bạn muốn sinh test cases theo chế độ nào?
1. QUICK — Sinh nhanh từ requirements (không qua bước phân tích)
2. FULL RBT — Quy trình 7 bước đầy đủ (phân tích → phân rã → RBT → sinh TC → review → xuất)
```

# Mode 1: QUICK — Sinh Test Cases Nhanh

## Mục đích

Sinh test cases **nhanh, đủ chất lượng** từ requirements đã rõ ràng, phù hợp cho module đơn giản hoặc khi cần kết quả ngay. Bắt buộc có **bước review trước khi xuất file**.

> **Lưu ý:** Mode QUICK **không dùng State File**. Nếu session bị ngắt giữa chừng, cần chạy lại từ đầu. Để có khả năng khôi phục xuyên session, hãy dùng Mode FULL RBT.

## Quy trình (2 lượt)

**Lượt 1 — Sinh TC:**

1. **Đọc và hiểu requirements** được cung cấp

2. **Lập Field Inventory & áp dụng Common TC Checklist** *(bắt buộc)*

   > Tham chiếu: `.agent/skills/rbt_manual_testing/references/common_tc_checklist.md`

   - Liệt kê toàn bộ fields/controls trên màn hình (tên field, loại, required, constraint)
   - Dùng **Bảng điều phối** trong checklist để xác định nhóm áp dụng
   - **Nhóm A, M:** Luôn áp dụng
   - **Nhóm D — TEXT:** Bắt buộc đủ **38 cases** (D01–D21 Nhập keyboard + D05cp–D21cp Copy-paste) cho mỗi trường. **Textbox KHÔNG có case tìm kiếm** — D22–D28 chỉ dành cho ô search trong popup Dropdown/Combobox
   - Các nhóm còn lại: áp dụng khi màn hình có field/chức năng tương ứng

3. **Xác định các luồng nghiệp vụ:**
   - Happy Path (luồng chính)
   - Negative Path (dữ liệu sai, thiếu)
   - Boundary Cases (giá trị biên)

4. **Áp dụng kỹ thuật thiết kế test case** tự động:
   - **Equivalence Partitioning (EP):** Chia input thành nhóm tương đương
   - **Boundary Value Analysis (BVA):** Test giá trị tại ranh giới
   - **Decision Table:** Liệt kê tổ hợp điều kiện (nếu có nhiều rules)
   - **State Transition:** Test chuyển đổi trạng thái (nếu có workflow)

5. **Sinh test cases draft theo 2 luồng:**

   **5a — Common TCs** (từ checklist — sinh trước):
   - Chỉ sinh các nhóm đã xác định ở Bước 2
   - TC có `(tùy spec)` → xác định expected result từ requirements trước khi sinh
   - **Format ID:** `[FEATURE]_[SỐ]` (VD: `M1_001`)
   - **Nhiều field cùng loại → MỌI field đều PHẢI có đủ toàn bộ checklist riêng.** NGHIÊM CẤM cắt bớt case cho field thứ 2 trở đi. VD: 4 dropdown → cả 4 đều phải có H01-H12 đầy đủ.

   **5b — Business TCs** (nghiệp vụ đặc thù — sinh sau):
   - Các kịch bản chưa được bao phủ bởi Common TCs
   - **Format ID:** `[FEATURE]_[SỐ]` (VD: `M1_001`)

   **⚠️ Self-check bắt buộc sau khi sinh xong mỗi module:**
   - **CHECK 1 — Dropdown đủ case:** Kiểm tra MỌI dropdown đều có đủ H01-H06 + scroll 3 Trường hợp + chọn giá trị 3 sub + search nếu có + **H13-H16 dùng `tc_group("Kiểm tra options hiển thị đúng")`** (3 tc_sub: Trường hợp call API thành công/2 item, thất bại, timeout)
   - **CHECK 1b — Grid column đủ U02:** Kiểm tra MỌI column subsection trong Nhóm U đều có U02 — kể cả cột readonly (expected result = không mở edit mode)
   - **CHECK 1c — Phân trang dùng tc_group:** Nếu đã sinh `tc_group("Kiểm tra phân trang")` → **không có** `tc()` riêng lẻ C04/C06/C08 (trùng lặp)
   - **CHECK 2 — Button Xuất Excel:** Nếu màn hình Tra cứu có nút Xuất Excel → phải có subsection button 3 TC
   - **CHECK 3 — tc_sub tên unique:** Không có 2 tc_sub trùng tên trong cùng tc_group
   - **CHECK 4 — Nhóm A đủ 6 TC (A01–A06):** Đếm TC trong subsection "Nhóm A" của **MỌI module/màn hình**. Phải có đủ: A01 (mặc định), A02 (tổng thể giao diện), A03 (Tab tiến), A04 (Shift+Tab lùi), A05 (phím Enter), A06 (Responsive zoom). Nếu module không áp dụng A05 → phải ghi `N/A + lý do`, KHÔNG được bỏ trống.
   - **CHECK 5 — TEXT field đủ 38 cases:** Với **MỌI trường TEXT/TEXTAREA**, đếm TC đủ **3 nhóm bắt buộc**:
      + Tĩnh: D01 (mặc định), D02 (hiển thị UI), D03 (placeholder), D04 (required) = **4 TC**
      + Nhập keyboard tc_group: D05–D07 BVA (sub `Kiểm tra nhập maxlength` 3 TH) + D08–D11 (whitespace 4 TH) + D12–D17 (loại ký tự 6 TH) + D18–D21 (bảo mật 4 TH) = **17 tc_item** (trong 1 tc_group "Kiểm tra khi nhập giá trị")
      + Copy-paste tc_group: D05cp–D07cp (BVA 3 TH) + D08cp–D11cp (whitespace 4 TH) + D12cp–D17cp (loại ký tự 6 TH) + D18cp–D21cp (bảo mật 4 TH) = **17 tc_item** (trong 1 tc_group "Kiểm tra khi copy/paste giá trị")
      + **Tổng tối thiểu: 4 tc + 1 tc_group(17 item) + 1 tc_group(17 item) = 38 cases**
      + ⚠️ **LƯU Ý:** Textbox TUYỆT ĐỐI KHÔNG CÓ case "Kiểm tra nhập tìm kiếm" (nghiệp vụ tìm kiếm thuộc Section Chức năng hoặc Button Tìm kiếm). D22–D28 chỉ dùng cho Dropdown/Combobox searchable popup.
   - **CHECK 5b — NUMBER field đủ 42 cases:** Với **MỌI trường NUMBER**, đếm TC đủ **3 nhóm bắt buộc**:
      + Tĩnh: E01–E04 = **4 TC** riêng lẻ
      + Nhập keyboard tc_group: E05–E07 BVA (sub `Kiểm tra nhập maxlength` 3 TH) + E08–E23 (whitespace + chars + security + số đặc thù) = **19 tc_item** (trong 1 tc_group "Kiểm tra khi nhập giá trị")
      + Copy-paste tc_group: E05cp–E23cp = **19 tc_item** (trong 1 tc_group "Kiểm tra khi copy/paste giá trị")
      + **Tổng tối thiểu: 4 + 19 + 19 = 42 cases**
      + ⚠️ Case hay bị thiếu: E05–E07 (BVA maxlength), E08 (toàn space), E11 (nhiều space), E12 (ký tự chữ), E15 (hỗn hợp), E18 (URL bị chặn), E20 (số thập phân), E21 (số âm), E22 (số thập phân vượt quy định)
   - **CHECK 6 — Nhóm C Grid đủ cases cơ bản:** Nếu module có grid, kiểm tra có đủ: C01 (format), C02 (STT tăng dần), C03 (ẩn paging ≤10), C05 (style paging format chuỗi), C07 (header/footer ổn định), C09 (thêm/sửa/xóa từ trang N), C10 (xóa bản ghi cuối trang cuối) + 3 tc_group phân trang + QT: C11 (skeleton), C12 (grid trống), C13 (fullscreen icon), C14 (filter cột), C15 (cột ngày hover), C16 (cột người hover)
   - **CHECK 7 — Multi-select (J) đủ case:** Kiểm tra MỌI multi-select đều có đủ: J01 (hiển thị), J02 (mặc định), J03 (placeholder), J04 (required), J05 (sắp xếp), J06 (căn lề), J07–J10 (chọn giá trị tc_group 4 sub), J11–J13 (scroll tc_group 3 sub), J14 (focus bàn phím) + **API states tc_group** (H13-H16 pattern). NGHIÊM CẤM cắt bớt cho field thứ 2+.
   - **CHECK 8 — Date/DateTime (K) đủ case:** Kiểm tra DatePicker có đủ: K01 (focus trống), K02 (focus có giá trị), K03 (chọn ngày), K05 (required), K06 (sai format), K07 (ngày không tồn tại), K08 (ngày biên 29/02), K15 (nhập tay QT), K16 (ký tự không hợp lệ QT), K17 (ngày <01/01/1900 QT). RangePicker thêm K12–K14 (Từ > Đến, =, <). **Nếu SRS giới hạn khoảng ngày tối đa** (VD: ≤31 ngày) → thêm 3 TC: TK_DATERANGE_01 (bằng giới hạn), TK_DATERANGE_02 (giới hạn −1 ngày), TK_DATERANGE_03 (vượt giới hạn → lỗi).
    - **CHECK 9 — TextArea (G) đủ 41 cases bắt buộc:** Nếu field là **TEXTAREA**, PHẢI áp dụng đầy đủ **Nhóm G = 41 TC** (không phải Nhóm D thường):
       + D01–D04 tĩnh: **4 TC** riêng lẻ
       + tc_group "Kiểm tra khi nhập giá trị" D05–D21: **17 tc_item** (BVA 3 + whitespace 4 + ký tự 6 + bảo mật 4)
       + tc_group "Kiểm tra khi copy/paste giá trị" D05cp–D21cp: **17 tc_item** (BVA 3 + whitespace 4 + ký tự 6 + bảo mật 4)
       + G07 (nhập nhiều dòng Enter), G11 (bộ đếm ký tự realtime), G12 (auto resize chiều cao): **3 TC** riêng lẻ
       + **Tổng: 4 + 17 + 17 + 3 = 41 TC/field**
       + Nếu field không dùng QT component → G11, G12 = N/A + ghi lý do. KHÔNG được bỏ trống.
   - **CHECK 10 — Không tách thành phần chung (rule QUAN TRỌNG):** Nếu màn hình có nhiều file/tab (VD: D10, D12, D31...), NGHIÊM CẤM tách các thành phần chung (button Chạy lại, Chấp nhận, Từ chối, Xuất Excel, Cài đặt, Quay lại, Nhóm G textarea, Nhóm S phân quyền) ra thành 1 module/sheet riêng (VD: "M0 Thành phần chung"). Mỗi file/tab PHẢI có đầy đủ các thành phần chung được lặp lại trong sheet riêng của nó. Lý do: reviewer cần đọc 1 sheet đầy đủ không phụ thuộc sheet khác.
   - **CHECK 11 — Checkbox Mandatory disabled đủ TC:** Nếu màn hình/popup có checkbox luôn ở trạng thái checked và disabled (không thể bỏ tick — VD: checkbox mặc định trong popup Thêm bộ lọc, Cài đặt hiển thị), PHẢI có `tc()` riêng kiểm tra: (1) checkbox hiển thị đúng trạng thái checked+disabled theo thiết kế, (2) người dùng không thể bỏ tick, (3) giá trị vẫn được gửi lên server trong form submit. Tham chiếu case I10 từ Nhóm I (`common_tc_checklist.md`). KHÔNG được bỏ qua hoặc gộp vào TC hiển thị chung (A02).
   - **CHECK 12 — Màn hình Chỉnh sửa (Edit Form) bám sát spec & đủ 5 case đặc thù:** Tùy từng màn hình có nghiệp vụ cho phép sửa trường nào hoặc không cho phép sửa trường nào => BẮT BUỘC đọc spec để phân loại chính xác danh mục trường được sửa và trường bị khóa (readonly). Với các trường cho phép sửa, nhiều nhất PHẢI có số lượng test case tương đương màn hình Tạo mới (đủ D, E, H, J, K...). BẮT BUỘC có 5 case đặc thù: (1) Nạp dữ liệu cũ chính xác, (2) Khóa các trường ID/Mã không cho sửa (readonly/disabled), (3) Sửa 1 hoặc nhiều trường hợp lệ và lưu thành công, (4) Giữ nguyên không đổi và Lưu (không lỗi), (5) Hủy bỏ (Cancel) khôi phục giá trị ban đầu.
   - **CHECK 13 — Grid Column Nhóm U bắt buộc mọi cột:** Đối với mọi màn hình có Gridview/Table, BẮT BUỘC áp dụng Nhóm U cho từng cột dữ liệu (U01 hiển thị, U02 chỉnh sửa - kể cả readonly, U03 search column nếu có, U04 căn lề/format). Không gộp chung các cột vào 1 case.
   - **CHECK 14 — Tra cứu BIZ đính kèm câu lệnh SQL Database:** Các kịch bản tìm kiếm (1 điều kiện, nhiều điều kiện, không có dữ liệu) trong mục Chức năng (BIZ) BẮT BUỘC đính kèm câu lệnh SQL mẫu tương ứng trong kết quả mong đợi (`SELECT ... FROM ... WHERE ...`) để tester đối soát tầng DB.
   - **CHECK 15 — Action hàng loạt (Batch Action) phân tách $N=1$ vs $N>1$:** Khi thao tác trên nhiều dòng (Batch run/delete/approve), BẮT BUỘC phân tách rõ: $N=1$ (popup hiển thị chi tiết bản ghi + câu hỏi đơn lẻ kèm mã `CONF_001`) vs $N>1$ (popup tổng thể kèm câu hỏi tập hợp `CONF_002`); đính kèm đúng các mã Message (`CONF_*`, `SUC_*`, `ERR_*`) từ SRS.
   - **CHECK 16 — Nút Xuất Excel đủ 7 test case chuẩn:** Màn hình có nút Xuất Excel BẮT BUỘC có đủ 7 case: (1) Xuất trang hiện tại, (2) Xuất theo bộ lọc, (3) Tên file `<tên>-ddmmyyyyhhmmss.xlsx`, (4) Chia file zip >1M bản ghi, (5) Dữ liệu rỗng chỉ có Header, (6) Lỗi API hệ thống/timeout, (7) Hết token điều hướng về Login.
   - **CHECK 17 — Button trên Hộp thoại xác nhận (CONF_*):** Khi một thao tác (Huỷ form khi đã có dữ liệu `ALT-01`, Xoá bản ghi, Phê duyệt, Từ chối, Tiếp nhận...) kích hoạt mở popup xác nhận `CONF_*` → **BẮT BUỘC** tạo riêng subsection cho từng nút và icon:
      + Nút **[Đồng ý] / [Xác nhận]:** `subsection("Kiểm tra button Đồng ý trên Hộp thoại xác nhận <Mã popup>")` — Đủ 3 TC (hiển thị, trạng thái, click xác nhận hành động).
      + Nút **[Huỷ bỏ] / [Không]:** `subsection("Kiểm tra button Huỷ bỏ trên Hộp thoại xác nhận <Mã popup>")` — Đủ 3 TC (hiển thị, trạng thái, click hủy bỏ thao tác đóng, bảo toàn 100% dữ liệu đang nhập dở).
      + Icon đóng **[X]:** `subsection("Kiểm tra icon đóng (X) trên Hộp thoại xác nhận <Mã popup>")` — Đủ 2 TC (hiển thị góc trên phải, click đóng popup).
   - **CHECK 18 — Cột Trường hợp kiểm thử (Col C) của Button:** BẮT BUỘC bắt đầu bằng `"Kiểm tra "`, TUYỆT ĐỐI KHÔNG để tiền tố mã `M01 — `, `M02 — `, `M03 — ` (VD: `Kiểm tra hiển thị nút Gửi yêu cầu`, `Kiểm tra trạng thái enable/disable của nút Gửi yêu cầu`, `Kiểm tra click nút Gửi yêu cầu`).
   - **CHECK 19 — Dropdown H06 (Sử dụng bàn phím):** BẮT BUỘC có đủ 5 bước phím chi tiết: (1) Tab/Shift-Tab focus vào dropdown, (2) Enter mở danh sách option, (3) Phím Up/Down di chuyển con trỏ, (4) Enter chọn giá trị, (5) Tab/Shift-Tab chuyển sang control tiếp theo.
   - **CHECK 20 — File Upload (Nhóm Q):** BẮT BUỘC chia thành 3 nhóm rõ rệt: (1) Kéo thả file vào dropzone, (2) Click button 'Chọn file' mở File Dialog, (3) Hiển thị danh sách file sau tải lên và các thao tác trên file (xem, tải về, xóa file, popup xác nhận xóa).
   - **CHECK 21 — Bám sát SRS trên Confluence — CẤM TỰ SUY DIỄN (Zero Invented Fields):** 100% chỉ đưa vào Field Inventory và kịch bản test các trường có trong spec. Tuyệt đối KHÔNG mang thói quen/logic sản phẩm khác áp đặt thêm trường (Upload file, checkbox cam kết). Nếu nghi ngờ thiếu -> đưa vào Q&A Bước 2.
   - **CHECK 22 — Bắt buộc qua Bước 5b (QA Lead Review Gate):** Đánh giá 6 tiêu chí chất lượng và xuất báo cáo `tc_review_<module>.md`, dừng tại checkpoint để User/Lead duyệt trước khi bàn giao.

   Đảm bảo mỗi TC đủ fields:
   - TC ID, Loại TC (Common/Business), Module, Test Case Title / Test Scenario
   - Pre-conditions, Test Steps (đánh số), Expected Results (đánh số tương ứng)
   - Test Data (**phải cụ thể**, không placeholder), Priority (Critical / High / Medium / Low)

**Lượt 2 — TC Lead Review Gate (BẮT BUỘC trước khi xuất):**

> Xem chi tiết tại mục **[TC Lead Review Gate]** bên dưới.

Agent thực hiện tự review bộ TC vừa sinh → xuất Artifact gap list → chờ user confirm → mới xuất bảng Markdown final.

## Bảng Output

```
| TC ID | Mục đích kiểm thử | Trường hợp kiểm thử | Điều kiện tiên quyết | Test Data | Các bước thực hiện | Kết quả mong đợi | Priority |
```

- **Format TC ID:** `[FEATURE]_[SỐ]` (VD: `M1_001`, `Login_001`)
- **Phân loại TC (tổ chức nội bộ, không phải cột):** `UI` (Giao diện) / `CMN` (Common) / `BIZ` (Business)
- Sắp xếp: Giao diện (UI) → Common TCs (CMN) → Business TCs (BIZ)

### Excel Export (tùy chọn)

Nếu user yêu cầu xuất Excel, áp dụng Bước 7 (Excel Export) của FULL RBT — tạo file `scripts/gen_tc_<ten_chuc_nang>.py` dùng module `scripts/tc_excel_writer.py`. Xem rule `manual_tc_excel_export.md`.

## Quy tắc Test Data (áp dụng cho cả 2 modes)

```
❌ Sai: "Nhập mã số hợp lệ"
✅ Đúng: "Nhập mã: KH-2026-0012"

❌ Sai: "Nhập email hợp lệ"
✅ Đúng: "Nhập email: test_khachhang_01@domain.com"

❌ Sai: "Nhập giá trị vượt giới hạn"
✅ Đúng: "Nhập 256 ký tự vào trường Name (max: 255)"
```

## Tiêu chuẩn Kiểm thử Trường Text (Text Field Validation Standard)

> **Nguồn chính thức:** Danh sách đầy đủ cases nằm tại **Nhóm D** trong `.agent/skills/rbt_manual_testing/references/common_tc_checklist.md`.
> Khi sinh TC cho bất kỳ trường TEXT nào, **BẮT BUỘC** áp dụng toàn bộ **38 cases** (D01–D21 Nhập keyboard + D05cp–D21cp Copy-paste) — không được bỏ sót, không được gộp nhiều trường vào 1 case.

**Các nhóm cases bắt buộc (tóm tắt):**

| Nhóm | Cases | Áp dụng | Nội dung |
|---|---|---|---|
| Mặc định & UI | D01–D04 | Mọi TEXT field | Default value, hiển thị, placeholder, required |
| Maxlength BVA (Nhập) | D05–D07 | Mọi TEXT field | Max−1, Max, Max+1 (3 cases độc lập — nhập bằng bàn phím) |
| Whitespace (Nhập) | D08–D11 | Mọi TEXT field | Toàn space, đầu/cuối, giữa, nhiều space giữa (4 cases độc lập) |
| Loại ký tự (Nhập) | D12–D17 | Mọi TEXT field | In hoa, in thường, số, đặc biệt, hỗn hợp, tiếng Việt |
| Bảo mật (Nhập) | D18–D21 | Mọi TEXT field | XSS/HTML, SQL injection, URL, CSRF |
| **Copy-paste** | **D05cp–D21cp** | **Mọi TEXT field** | **Lặp lại D05–D21 bằng Ctrl+V. D07cp: QT component luôn truncate khi paste (khác keyboard). Ký tự bị chặn theo charset vẫn bị lọc khi paste.** |
| Search — case/dấu | D22–D23 | Ô tìm kiếm | Không phân biệt hoa/thường, có dấu/không dấu |
| Search — kết quả | D24–D26 | Ô tìm kiếm | Tương đối (contains), tuyệt đối (exact), không có kết quả |
| Search — maxlength | D27–D28 | Ô tìm kiếm | Nhập ≤ max, nhập > max |

**Quy tắc áp dụng:**
- Mỗi trường TEXT → 1 bộ cases riêng (không gộp)
- Expected Result phải dựa trên logic/SRS thực tế, không dùng placeholder chung
- Ô tìm kiếm của Combobox, Dropdown có search, Multi-select có search cũng áp dụng D22–D28
- **ID range trong script:** Nhập keyboard = ID liền mạch sau D04; Copy-paste = ID 500+ (tránh đụng nhau); D22–D28 search (chỉ ô search trong popup Dropdown/Combobox) = ID 600+

**Ví dụ Test Data cụ thể (bắt buộc):**
```
❌ Sai: "Nhập ký tự đặc biệt"
✅ Đúng: Nhập "!@#$%^&*()_+" vào trường Tên khách hàng (maxlength: 100)

❌ Sai: "Nhập vượt giới hạn"
✅ Đúng: Nhập 256 ký tự vào trường Ghi chú (max: 255) bằng cách paste chuỗi "A"×256
```

## Anti-Patterns (Mode QUICK)

- ❌ **Viết TC bằng tiếng Anh hoặc thiếu dấu tiếng Việt** — Toàn bộ nội dung TC (mô tả, bước thực hiện, kết quả mong đợi) PHẢI viết bằng tiếng Việt có dấu đầy đủ (Unicode TCVN 6909:2001)
- ❌ **Tách thành phần chung (M0)** — NGHIÊM CẤM tách buttons, textarea lý do (Nhóm G), phân quyền (Nhóm S) ra thành sheet/module riêng (VD: "M0 Thành phần chung"). Phải lặp lại đầy đủ trong mỗi sheet.

- ❌ **Bỏ qua Common TC Checklist** — NGHIÊM CẤM sinh TC mà không lập Field Inventory và áp dụng checklist
- ❌ Bỏ qua nhóm A (giao diện chung) hoặc nhóm M (button) — 2 nhóm này luôn bắt buộc
- ❌ **Nhóm A chỉ có 3–5 TC** — phải đủ **6 TC** (A01–A06) cho **MỌI module/màn hình**, kể cả popup. Thiếu A03/A04/A05 là lỗi phổ biến nhất.
- ❌ Sinh Group D không đủ 38 cases (D01–D04 tĩnh + D05–D21 tc_group keyboard 17 item + D05cp–D21cp tc_group copy-paste 17 item) cho mỗi trường TEXT
- ❌ **TEXT tc_group chỉ có vài item** — tc_group "Kiểm tra khi nhập giá trị" PHẢI có **17 tc_item** (D05–D21, bắt đầu bằng sub "Kiểm tra nhập maxlength" 3 items); tc_group copy-paste PHẢI có **17 tc_item** (D05cp–D21cp). Thiếu D05–D07 (BVA maxlength), D11 (nhiều space), D12–D14 (hoa/thường/số), D16 (hỗn hợp), D20 (URL), D21 (CSRF) là lỗi phổ biến.
- ❌ Sinh Group E không đủ 42 cases (E01–E04 tĩnh + E05–E23 tc_group keyboard **19 item** + E05cp–E23cp tc_group copy-paste **19 item**) cho mỗi trường NUMBER
- ❌ **NUMBER tc_group chỉ có vài item** — tc_group "Kiểm tra khi nhập giá trị" PHẢI có **19 tc_item** (E05–E23, bắt đầu bằng sub "Kiểm tra nhập maxlength" 3 items). Thiếu E05–E07 (BVA maxlength), E08 (toàn space), E11 (nhiều space), E12 (ký tự chữ), E15 (hỗn hợp), E18 (URL), E20 (số thập phân), E21 (số âm), E22 (số thập phân vượt quy định) là lỗi phổ biến.
- ❌ Gộp nhiều trường TEXT/NUMBER vào 1 TC
- ❌ Sinh test data chung chung / placeholder
- ❌ Chỉ có Happy Path, thiếu Negative/Boundary
- ❌ Bỏ qua validation rules trong requirements
- ❌ Test Steps mơ hồ ("nhập dữ liệu" → phải ghi rõ nhập gì, ở đâu)
- ❌ Bỏ qua TC Lead Review Gate — NGHIÊM CẤM xuất file khi chưa qua review
- ❌ **Grid (C) chỉ có C01 + phân trang** — PHẢI có thêm C02 (STT), C03 (ẩn paging ≤10), C05 (style format chuỗi), C07 (header ổn định), C09 (action từ trang N), C10 (xóa cuối trang cuối), QT: C11–C16
- ❌ **Multi-select (J) thiếu J02–J06, J14** — MỌI multi-select phải có đủ 14 cases (J01–J14) + API states
- ❌ **DatePicker (K) thiếu K01, K02, K08, K17** — không được bỏ K01 (focus trống), K02 (focus có giá trị), K08 (29/02 năm nhuận), K17 (<01/01/1900)
- ❌ **TEXTAREA dùng Nhóm D nhưng thiếu Nhóm G** — nếu field là TextArea thì PHẢI áp dụng Nhóm G = **41 TC** đầy đủ (D01-D04 + tc_group D05-D21 keyboard 17 item + tc_group D05cp-D21cp paste 17 item + G07 + G11 + G12). Không được chỉ cộng thêm G07+G11+G12 mà bỏ qua tc_group keyboard/copypaste.

## Bảng đếm TC tối thiểu — Tra nhanh khi Self-check

> Agent PHẢI tra bảng này sau khi sinh xong mỗi module, so sánh số TC thực tế với yêu cầu tối thiểu.

| Field Type | TC tĩnh (tc riêng) | tc_group Nhập | tc_group Copy-paste | Phụ trợ | **Tổng tối thiểu** |
|---|---|---|---|---|---|
| **TEXT thường** | D01–D04 (4) = **4** | 1 group × 17 item (D05–D21) | 1 group × 17 item (D05cp–D21cp) | — | **38** |
| **NUMBER** | E01–E04 (4) = **4** | 1 group × 19 item (E05–E23) | 1 group × 19 item (E05cp–E23cp) | — | **42** |
| **TEXTAREA (Nhóm G)** | D01–D04 (4) = **4** | 1 group × 17 item (D05–D21) | 1 group × 17 item (D05cp–D21cp) | G07 + G11 + G12 = **3** | **41** |
| **Dropdown (H)** | H01–H06 (6) | scroll (1 group × 3 sub) + chọn (1 group × 3 sub) + API (1 group × 3 sub) | — | D22–D28 nếu search | **≥15** (không search) / **≥22** (có search) |
| **Multi-select (J)** | J01–J06 (6) + J14 (1) = **7** | chọn (1 group × 4 sub) + scroll (1 group × 3 sub) + API (1 group × 3 sub) | — | D22–D28 nếu MULTISELECT+SEARCH | **≥17** (không search) / **≥24** (có search) |
| **Date (K)** | K01–K03, K05–K09 = **8** | — | — | K12–K14 (RangePicker) + K15–K17 (QT) | **≥8** (DatePicker) / **≥14** (RangePicker QT) |
| **Nhóm A** (mọi module) | A01–A06 = **6** | — | — | A07–A08 (QT) | **≥6** |
| **Grid (C)** | C01–C03, C05, C07, C09–C10 = **7** | 3 tc_group phân trang | — | C11–C16 (QT) = 6 | **≥13** (không QT) / **≥19** (QT) |
| **Grid Columns (Nhóm U)** | U01–U04 = **4** / cột | — | — | U05–U07 = 3 / thao tác | **4 × N_cột** |
| **Chỉnh sửa (Nhóm V)** | 5 case đặc thù Edit (V01–V05) | Tương đương Tạo mới cho trường được sửa | Tương đương Tạo mới | — | **5 + Số TC trường được sửa** |
| **Xuất Excel (Nhóm M)** | 7 cases chuẩn (xuất trang, theo lọc, zip >1M, rỗng, lỗi...) | — | — | — | **7** |

---

# Mode 2: FULL RBT — Quy Trình AI-RBT 7 Bước

## Mục đích

Quy trình bài bản, tuần tự cho module phức tạp. Bao gồm phân tích Ambiguity, phân rã hệ thống, Traceability Matrix, đánh giá Risk Level, sinh test cases chi tiết, **TC Lead Review Gate**, và chuẩn hóa format.

> ⚠️ **QUAN TRỌNG:** Quy trình này **BẮT BUỘC chạy tuần tự** từng bước. KHÔNG được gộp nhiều bước chạy 1 lần. Mỗi bước phải hoàn thành và được user xác nhận trước khi sang bước tiếp.

---

## 💾 State File — Cơ chế ghi nhớ xuyên session

> Work Log & Memory (audit trail khi user duyệt checkpoint) đi kèm state file — xem mục **📝 Work Log & Memory** bên dưới và `.agent/rules/worklog_memory_rules.md`.

**Mục đích:** Sau mỗi checkpoint, AI ghi trạng thái vào file để session mới (sau auto-compact) có thể tiếp tục đúng bước, không mất Q&A decisions và scenarios đã được user approve.

**Path:** `practices/testcases/<DU_AN>/<FeatureName>_rbt_state.md`

### Khi bắt đầu FULL RBT

**BẮT BUỘC** kiểm tra state file trước:
```
Tồn tại → Đọc file → Báo "Phát hiện session trước ở Bước X. Tiếp tục?"
Không tồn tại → Tạo file mới, bắt đầu Bước 1
```

### Format state file

```markdown
---
feature: <Tên tính năng>
project: <Tên dự án>
started: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
current_step: B1|B2|B3|B4|B5|B5b|B6|B7
mode: FULL|COMPACT
output_script: scripts/gen_tc_<name>.py
output_xlsx: practices/testcases/<DU_AN>/<Name>_TestCases.xlsx
qa_file: practices/Q&A/<FeatureName>_QA.md
tc_count: 0
---


## ✅ Bước 1 — Context
## ✅ Bước 2 — Q&A Resolved
## ✅ Bước 3 — Modules & Field Inventory
## ⏳ Bước 4 — Traceability [PENDING / APPROVED]
## ✅ Bước 5 — TC Summary
## ⏳ Bước 5b — TC Lead Review Gate [PENDING / CONFIRMED]
## ⏳ Bước 6 — Template Mapping [SKIP-COMPACT / DONE]
## ✅ Bước 7 — Output
```

### Lịch lưu

| Sau bước | Nội dung cập nhật |
|---|---|
| Bước 1 | Context đã xác nhận |
| Bước 2 | Toàn bộ Q&A + assumptions + **file Q&A path** (`practices/Q&A/<FeatureName>_QA.md`) |
| Bước 3 | Module list + Field Inventory + Common TC groups |
| **Bước 4** | **Traceability Matrix + scenarios APPROVED — quan trọng nhất** |
| Bước 5 | TC count per module |
| **Bước 5b** | **Trạng thái Review Gate (PENDING / CONFIRMED) + danh sách GAP đã xử lý** |
| Bước 6 | SKIP-COMPACT (nếu COMPACT mode) hoặc DONE (FULL mode) |
| Bước 7 | Script path + xlsx path + tc_count final |

---


### Bước 1: Context & Role-play (Khởi tạo ngữ cảnh)

**Mục đích:** Thiết lập vai trò Senior QA Engineer và nạp bối cảnh dự án.

> [!IMPORTANT]
> **PRE-B1 — Đọc toàn bộ tài liệu trước khi định nghĩa scope:**
> - **ĐỌC TOÀN BỘ NỘI DUNG** mỗi tài liệu (Confluence page, PDF, spec file) từ đầu đến cuối trước khi viết scope
> - **KHÔNG** kết luận "màn hình X không có tab/bảng Y" chỉ dựa trên TOC, tiêu đề section hoặc đọc lướt
> - **KHÔNG** bỏ qua phần nội dung vì "ücó vẻ lặp lại" mà chưa kiểm tra
> - Scope phải mô tả đầy đủ đến cấp: **Màn hình → Tab → Từng bảng/sub-component**

**Agent phải:**
1. Yêu cầu user cung cấp (nếu chưa có):
   - Tên dự án / tính năng
   - Mô tả hệ thống hiện tại
   - Mục tiêu kiểm thử MVP
   - Tài liệu yêu cầu (Requirements, User Stories, Figma link, PDF...)
2. **Đọc kỹ toàn bộ từng tài liệu** — NGHIÊM CẤM tóm tắt scope khi chưa đọc hết
3. Tóm tắt scope kiểm thử đầy đủ đến cấp **màn hình → tab → từng bảng**
4. **Dừng và chờ user xác nhận** trước khi sang Bước 2

> [!CAUTION]
> **CHECKPOINT BẮT BUỘC:** Agent phải dừng hoàn toàn sau khi xuất scope B1.
> - ❌ NGHIÊM CẤM tự ý sang B2, bất kể scope có vẻ đầy đủ
> - ✅ Chỉ tiếp tục khi user reply rõ ràng ("OK", "đúng rồi", "tiếp tục B2", v.v.)
> - Nếu user chỉ ra thiếu sót: bổ sung scope, cập nhật lại và chờ xác nhận lần nữa

**Output:** Xác nhận hiểu bối cảnh + tóm tắt scope kiểm thử (màn hình → tab → bảng).

---

### Bước 2: Analysis & QnA (Phân tích yêu cầu)

**Vai trò:** Senior Test Architect / QA Lead. Kết hợp phân tích SRS chuyên sâu với trọng tâm thiết kế testcase của FULL RBT để tìm điểm mờ, logic chưa hợp lý và mâu thuẫn.

1. Đọc và áp dụng `.agent/skills/srs_qa_architect/SKILL.md` cùng các references bắt buộc: `checklist-review.md`, `Ambiguity.md`, `deep-logic-review.md`. Đây là nguồn chuẩn duy nhất cho phân tích và schema Q&A; không rút gọn vì đang chạy trong FULL RBT.
2. Rà từng requirement, dựng Happy/Alternate/Exception Paths; dùng decision table, state transition, role × action × state và field/data dependency khi áp dụng. Đối chiếu giữa các phần/module rồi phản biện bằng tình huống cụ thể.
3. Bao phủ trọng tâm FULL RBT trong reference: search nhiều trường, filter ở trang chi tiết/read-only, loại control, form/button theo trạng thái, phân quyền, concurrency, pagination từng danh sách, export/import và batch. Chỉ hỏi phần chưa rõ thuộc capability thực tế.
4. Lưu **Quality Gate + Q&A** theo schema chung vào `practices/Q&A/<FeatureName>_QA.md`: có nguồn, vấn đề/tác động, câu hỏi, Assumption/Options và cột `Câu trả lời`. Cập nhật state B2=PENDING cùng verdict và các Q-ID chưa giải quyết.
5. **Dừng tại review gate**, chờ BA/user phản hồi. Khi được xác nhận tiếp tục, ưu tiên câu trả lời BA, chỉ dùng assumption đã được chấp thuận; kiểm tra tác động lên rule liên quan và tính lại verdict. BLOCKING chưa giải quyết phải được làm rõ hoặc loại khỏi scope được user xác nhận trước khi thiết kế TC cho phần đó.
6. Cập nhật `Q&A Resolved` khi các vấn đề cần chốt của scope đã được xử lý và trả quyền điều phối về **B3**, không nhảy thẳng sang sinh testcase. Nếu còn vấn đề trong phần hoãn, ghi rõ Q-ID và scope hoãn trong state.

**Output:** Luồng + bảng đối chiếu áp dụng + tình huống phản biện + file Quality Gate/Q&A; không duy trì mẫu Q&A riêng trong skill này.

---

### Bước 3: Decomposition (Phân rã)

**Mục đích:** Chia tính năng phức tạp thành các Module / Sub-module nhỏ, dễ quản lý.

**Agent phải:**
1. Phân rã theo 1 trong 2 cách:
   - **Theo UI:** Header, Data Table, Form popup, Sidebar...
   - **Theo luồng:** Flow tạo mới, Flow chỉnh sửa, Flow xóa...
2. Mô tả ngắn gọn chức năng từng Module
3. Chỉ ra Dependencies giữa các Module

**Output:** Danh sách Modules/Sub-modules + Dependencies.

---

### Bước 3b: Field Inventory & Common TC Mapping *(bắt buộc)*

> **Tham chiếu:**
> - `.agent/skills/rbt_manual_testing/references/common_tc_checklist.md` — Checklist Common TC theo field type
> - `Template/Quy+tắc+component.md` — Quy tắc FE chung cho CUCI (hành vi cụ thể của từng component)
>
> **Nguyên tắc kết hợp:** Checklist cung cấp danh sách TC cần sinh. Quy tắc component cung cấp **expected result chính xác** (VD: textbox chặn ký tự tại input, trim khi blur, textarea hiện bộ đếm ký tự). SRS quy định ràng buộc cụ thể cho từng trường. Khi có mâu thuẫn: **SRS > Quy tắc component > Checklist**.

Thực hiện cho **mỗi màn hình / module** vừa phân rã:

**3b.1 — Lập Field Inventory:**

| Field Name | Field Type | Required? | Constraint |
|---|---|---|---|
| Tên field | TEXT / NUMBER / DATE / CBB / DROPDOWN / MULTISELECT / **MULTISELECT+SEARCH** / CHECKBOX / RADIO / TEXTAREA / FILE / LABEL(readonly) | Yes/No | maxlength, min, max, format... |

> **MULTISELECT+SEARCH** = multi-select có ô tìm kiếm tích hợp (phổ biến trong AntD). Nhóm TC áp dụng: **J + D** (ô search). Phân biệt với MULTISELECT thuần (chỉ nhóm J) và CBB/DROPDOWN có search (nhóm H + D22).

**3b.2 — Xác định nhóm Common TC áp dụng** (dùng Bảng điều phối trong checklist):

| Nhóm | Áp dụng? | Field áp dụng |
|---|---|---|
| A — Giao diện chung | ✅ Luôn có | Mọi màn hình — **bắt buộc đủ 6 TC (A01–A06)**; A07–A08 áp dụng khi hệ thống dùng QT component |
| C — Grid + Paging | ✅/❌ | Nếu có danh sách bảng |
| D — TEXT | ✅/❌ | Tên field: ... |
| H — CBB/DROPDOWN | ✅/❌ | Tên field: ... |
| K — DATE | ✅/❌ | Tên field: ... |
| M — Button | ✅ Luôn có | Nếu có button action |
| P — Xóa | ✅/❌ | Nếu có chức năng xóa |
| S — Phân quyền chức năng | ✅/❌ | Nếu chức năng có kiểm soát quyền truy cập |
| T — Tra cứu kết hợp | ✅/❌ | Nếu màn hình có khu vực tìm kiếm ≥ 2 trường |
| *(các nhóm còn lại A→T)* | ✅/❌ | Xem đầy đủ trong `common_tc_checklist.md` |

**3b.3 — Ghi nhận để dùng ở Bước 5:** lưu danh sách nhóm đã tick + tên field cụ thể cho từng nhóm.

---

### Bước 4: Traceability (Đảm bảo độ bao phủ)

**Mục đích:** Thiết lập ma trận truy vết để đảm bảo 100% requirements được phủ test scenarios.

**Agent phải:**
1. Map mỗi Module/Rule với mã Yêu cầu (REQ-01, REQ-02...)
2. Cross-check xem có yêu cầu nào bị thiếu trong danh sách phân rã (Gap Analysis)
3. Liệt kê High-Level Test Scenarios cho từng Module, tập trung:
   - Security / phân quyền
   - UI Validation
   - Business Logic
   - Data Integrity
   - Error Handling
4. **Chờ user review** danh sách scenarios trước khi sinh test case chi tiết

**Output:** Traceability Matrix + High-Level Test Scenarios.

> [!WARNING]
> **Human Checkpoint:** User cần review danh sách scenarios để bổ sung các trường hợp đặc thù mà AI có thể bỏ sót. Đây là bước đánh giá rủi ro do con người thực hiện.

---

### Bước 5: RBT & TC Generation (Sinh Test Case chi tiết)

**Mục đích:** Sinh test cases chi tiết theo chiến lược Risk-Based Testing.

> **⚡ CHỌN CHẾ ĐỘ OUTPUT TRƯỚC KHI SINH:**
>
> | Điều kiện | Chế độ |
> |---|---|
> | ≤ 2 modules, ≤ 80 TC tổng | **FULL** — sinh bảng Markdown đầy đủ trong chat → Bước 6 → Bước 7 |
> | ≥ 3 modules **hoặc** ≥ 80 TC tổng | **COMPACT** — chỉ in summary trong chat, ghi chi tiết thẳng vào script Python (gộp Bước 5+6+7) |
>
> **COMPACT mode** (mặc định cho tính năng lớn):
> - Trong chat: chỉ in bảng tóm tắt TC ID + Test Title (1 dòng/TC)
> - Chi tiết `buoc`/`ket_qua`/`data` → viết thẳng vào `tc()` calls trong file `.py`
> - **Lợi ích:** tiết kiệm ~70% context, không bị auto-compact giữa chừng
> - **Bỏ qua Bước 6** khi dùng COMPACT — chi tiết đã được ghi vào script Python ở Bước 7
> - **Bước 5b (TC Lead Review Gate) vẫn BẮT BUỘC** — AI rà soát trên bảng summary trước khi ghi vào file Python ở Bước 7
>
> **Fallback khi COMPACT thất bại:**
> - Nếu file `.py` quá lớn (>100 TC) vượt context window → chia file thành nhiều module functions, mỗi function cho 1 module/màn hình
> - Nếu agent mất context giữa chừng → đọc lại state file (`_rbt_state.md`) để khôi phục tại Bước 4 (APPROVED), sau đó sinh lại từ Bước 5
> - Nếu script Python bị lỗi giữa chừng → agent đọc lại file `.py` đã ghi, xác định module cuối cùng hoàn thành, tiếp tục từ module tiếp theo

**Agent phải:**
1. Đánh giá Risk Level cho mỗi Module:
   - **High Risk:** Test kỹ, nhiều cases (nghiệp vụ quan trọng, liên quan tiền, bảo mật)
   - **Medium Risk:** Test vừa phải
   - **Low Risk:** Test cơ bản, happy path
2. Sinh test case với đầy đủ fields:
   - TC ID (format: `[FEATURE]_[SỐ]` VD: `M1_001`)
   - Mục đích kiểm thử — trong `tc()` viết **mô tả thuần chữ thường** (writer tự thêm `"Kiểm tra "` và strip bất kỳ prefix ID-like nào trước ` - `). Cột B Excel chỉ hiển thị `"Kiểm tra [mô tả]"`, KHÔNG có mã ID.
   - Trường hợp kiểm thử
   - Điều kiện tiên quyết
   - Test Data (**phải cụ thể**, không dùng placeholder chung chung)
   - Các bước thực hiện (đánh số)
   - Kết quả mong đợi (đánh số tương ứng)
   - Priority
3. Bao phủ đa dạng:
   - Happy Path
   - Negative Path (giá trị biên, vượt ký tự)
   - Edge Cases (timeout, mất kết nối...)
4. Áp dụng **kỹ thuật thiết kế test case** phù hợp (định nghĩa & ví dụ: `.agent/skills/rbt_manual_testing/references/test_design_techniques.md`):
   - **Equivalence Partitioning:** Chia input thành nhóm tương đương, test đại diện mỗi nhóm
   - **Boundary Value Analysis (BVA):** Test giá trị tại ranh giới (min, min+1, max-1, max)
   - **Decision Table:** Liệt kê tổ hợp điều kiện → kết quả (cho logic nhiều điều kiện)
   - **State Transition:** Test chuyển đổi trạng thái hợp lệ + không hợp lệ (cho workflow)
5. Nếu scenarios quá nhiều → sinh từng Module một, hỏi user để tiếp tục
6. **Self-check bắt buộc (CHECK 1–9 + 5b):** Sau khi sinh xong mỗi module, thực hiện **toàn bộ CHECK 1–9 và CHECK 5b** giống Mode QUICK (xem mục "Self-check bắt buộc" ở trên). Đặc biệt chú ý:
   - Tra **Bảng đếm TC tối thiểu** (mục "Bảng đếm TC tối thiểu — Tra nhanh khi Self-check") và so sánh với số TC thực tế đã sinh cho mỗi field type
   - Nếu phát hiện thiếu → bổ sung ngay trước khi chuyển sang Bước 5b

**Output:** Danh sách Test Cases chi tiết (dạng draft, chưa xuất file).

> [!IMPORTANT]
> Sau khi sinh xong Bước 5, agent **KHÔNG được xuất file ngay**. Phải chuyển sang **Bước 5b: TC Lead Review Gate** trước.

---

### Bước 5b: TC Lead Review Gate ⭐

**Mục đích:** AI đóng vai Test Lead khắt khe, tự rà soát toàn bộ bộ TC vừa sinh theo 6 tiêu chí chất lượng. Phát hiện gap, case thiếu, case sai → xuất báo cáo để user chỉnh sửa → chốt trước khi xuất file.

> ⚠️ **ĐÂY LÀ CHECKPOINT BẮT BUỘC.** Agent KHÔNG được bỏ qua hoặc tự động chuyển sang Bước 6 khi chưa có xác nhận của user tại bước này.

#### Quy trình thực hiện

**Giai đoạn 1 — AI tự rà soát (không cần user):**

Agent đọc lại toàn bộ bộ TC vừa sinh ở Bước 5 và đánh giá theo 6 tiêu chí sau:

**Tiêu chí 1 — Coverage (Tính đầy đủ):**
- Bộ TC có bao phủ đủ các requirement (functional + non-functional) trong scope không?
- Có đủ Positive cases, Negative cases, Boundary values, Edge cases không?
- Có bao phủ đủ Happy path, Alternative flow, Exception flow không?
- Có bao quát Business rules, Invalid data, Permission, Security, Performance không?

**Tiêu chí 2 — Clarity (Tính rõ ràng):**
- Title có mô tả đúng mục đích, không mơ hồ? (Ví dụ: "Verify login with valid credentials" thay vì "Test login")
- Pre-conditions và Post-conditions có đầy đủ, rõ ràng không?
- Test Steps có logic, ngắn gọn, dễ thực hiện không?
- Expected Result có cụ thể, đo lường được không? (Tránh "hiển thị đúng", "hoạt động bình thường")
- Ngôn ngữ có nhất quán, không lỗi chính tả không?

**Tiêu chí 3 — Accuracy (Tính chính xác):**
- TC có phản ánh đúng Requirement/Specification không? Có bị lệch yêu cầu không?
- Expected Result có khớp với logic nghiệp vụ đã xác định ở Bước 2 không?
- Có TC nào bị thừa hoặc thiếu do hiểu sai requirement không?

**Tiêu chí 4 — Feasibility & Efficiency (Tính khả thi):**
- Test Steps có thực tế, dễ execute, không quá phụ thuộc không?
- Có TC nào bị duplicate (trùng lặp hoàn toàn hoặc gần giống) không?

**Tiêu chí 5 — Organization (Tính tổ chức):**
- TC có được nhóm theo module/feature rõ ràng không?
- Priority và Risk Level có được gán phù hợp không?
- Có liên kết Requirement ID / User Story không?

**Tiêu chí 6 — Traceability & RBT:**
- Có TC nào thiếu traceability ngược về requirement không?
- Các TC có tập trung đúng mức vào phần rủi ro cao (High Risk) không?
- Bộ TC có hỗ trợ tốt cho regression testing không?

---

**Giai đoạn 2 — Xuất Artifact báo cáo review:**

Agent xuất file `practices/testcases/<DU_AN>/tc_review_<module>.md` gồm 3 phần:

```markdown
# TC Lead Review Report — [Tên Module]

## Tóm tắt đánh giá
| Tiêu chí | Trạng thái | Số lượng vấn đề |
|----------|-----------|----------------|
| Coverage | ⚠️ Cần bổ sung | 3 |
| Clarity | ✅ Đạt | 0 |
| Accuracy | ⚠️ Cần sửa | 1 |
| Feasibility | ✅ Đạt | 0 |
| Organization | ⚠️ Cần sửa | 2 |
| Traceability & RBT | ⚠️ Cần bổ sung | 2 |

## Danh sách vấn đề phát hiện
<!-- Agent điền vào theo format bên dưới -->

### [GAP-01] — Thiếu coverage: [Mô tả ngắn]
- **Tiêu chí:** Coverage
- **TC liên quan:** (không có / TC_005, TC_006)
- **Vấn đề:** [Mô tả cụ thể vấn đề]
- **Đề xuất:** [Gợi ý cụ thể cần làm]
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-02] — TC không chính xác: [Mô tả ngắn]
- **Tiêu chí:** Accuracy
- **TC liên quan:** TC_003
- **Vấn đề:** Expected Result không khớp với business rule đã xác nhận ở Bước 2
- **Đề xuất:** Sửa Expected Result thành: "..."
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

<!-- Liệt kê tất cả GAP theo format trên -->

## Hướng dẫn xác nhận
1. Đọc từng GAP trong danh sách trên
2. Tích vào checkbox [x] cho hành động bạn muốn thực hiện
3. Với hành động "Bỏ qua": điền lý do vào dòng đó
4. Với hành động "Bổ sung TC mới": có thể ghi thêm gợi ý nội dung TC cần sinh
5. Khi đã xử lý xong toàn bộ GAP, reply: **"Đã review xong, tiến hành sinh bộ TC final"**
```

---

**Giai đoạn 3 — Chờ user xác nhận:**

> ⚠️ Agent **DỪNG HOÀN TOÀN** tại đây. KHÔNG tự động tiếp tục Bước 6.

Agent in thông báo:
```
📋 **TC Lead Review Report đã được xuất.**

Bộ TC vừa sinh có [X] vấn đề cần xem xét.
Vui lòng:
1. Mở file `tc_review_<module>.md`
2. Tích chọn hành động cho từng GAP (Bổ sung / Sửa / Bỏ qua + lý do)
3. Reply "Đã review xong" để tôi tiến hành sinh bộ TC final theo quyết định của bạn.
```

---

**Giai đoạn 4 — AI đọc quyết định và xử lý:**

Sau khi user reply xác nhận, agent:
1. Đọc lại file `tc_review_<module>.md` đã được user chỉnh sửa
2. Tổng hợp danh sách hành động:
   - GAP đánh dấu **"Bổ sung TC mới"** → sinh TC mới tương ứng
   - GAP đánh dấu **"Sửa TC hiện có"** → cập nhật TC theo đề xuất
   - GAP đánh dấu **"Bỏ qua"** → ghi chú lý do, không thay đổi
3. Merge bộ TC gốc + TC mới + TC đã sửa thành **bộ TC final**
4. Chuyển sang Bước 6

**Output:** Bộ TC final đã được review và chốt bởi user.

---

### Bước 6: Template Mapping (Chuẩn hóa Format)

**Mục đích:** Đóng gói bộ TC final (đã qua Review Gate) thành bảng Markdown chuẩn, sẵn sàng copy sang Excel.

**Agent phải:**
1. Chuẩn hóa toàn bộ test cases vào bảng Markdown:

```
| TC ID | Mục đích kiểm thử | Trường hợp kiểm thử | Điều kiện tiên quyết | Test Data | Các bước thực hiện | Kết quả mong đợi | Priority |
```

2. Quy tắc bảng:
   - TC ID theo format thống nhất (ví dụ: `CRM_CUST_001`)
   - Test Steps và Expected Result đánh số, dùng `<br>` xuống dòng trong cell
   - **TUYỆT ĐỐI không được bỏ sót** bất kỳ test case nào đã chốt sau Review Gate
   - Nếu quá dài → chia thành Part 1, Part 2... và hỏi user để tiếp tục
3. Xuất output dưới dạng Artifact (`test_cases_<module>.md`)

**Output:** Bảng Test Cases Markdown hoàn chỉnh (đã qua Review Gate).

---

### Bước 7: Excel Export (Xuất file Excel theo template CIC)

**Mục đích:** Tự động tạo file `.xlsx` đúng định dạng template CIC từ bộ TC đã chuẩn hóa ở Bước 6.

> ⚠️ **BẮT BUỘC dùng module `scripts/tc_excel_writer.py`.**
> KHÔNG viết lại logic `openpyxl` từ đầu. Xem rule `.agent/rules/manual_tc_excel_export.md`.

**Agent phải:**
1. Tạo file `scripts/gen_tc_<ten_chuc_nang>.py` với cấu trúc:
   - Import: `from tc_excel_writer import section, subsection, tc, tc_group, tc_sub, tc_item, FeatureSpec, generate_excel`
   - `PRECOND`: chuỗi pre-condition
   - `ROWS`: list các `section()` / `subsection()` / `tc()` / `tc_group()` call từ bộ TC ở Bước 6
   - `FEATURE = FeatureSpec(sheet_title, feature_name, feature_code, precondition, rows)`
   - Gọi `generate_excel([FEATURE], output_path)` trong `if __name__ == '__main__':`
2. **Nhóm D TEXT field → BẮT BUỘC dùng `tc_group()` (MẶC ĐỊNH, không cần user yêu cầu):**
   - D01-D04 (tĩnh): dùng `tc()` bình thường
   - D05-D21 (nhập keyboard): dùng `tc_group("Kiểm tra khi nhập giá trị", [tc_sub("Kiểm tra nhập maxlength", [tc_item("Max−1"), tc_item("Max"), tc_item("Max+1")]), tc_sub(...), ...])` — **17 tc_item** (BVA 3 + whitespace 4 + ký tự 6 + bảo mật 4)
   - D05cp-D21cp (copy-paste): dùng `tc_group("Kiểm tra khi copy/paste giá trị", [tc_sub("Kiểm tra copy/paste maxlength", [tc_item("Max−1"), tc_item("Max"), tc_item("Max+1")]), ...])` — **17 tc_item**
3. **Nhóm E NUMBER field → BẮT BUỘC dùng `tc_group()` (MẶC ĐỊNH):**
   - E01-E04 (tĩnh): dùng `tc()` bình thường
   - E05-E23 (nhập keyboard): dùng `tc_group("Kiểm tra khi nhập giá trị", [tc_sub("Kiểm tra nhập maxlength", [tc_item("Max−1"), tc_item("Max"), tc_item("Max+1")]), tc_sub(...), ...])` — **19 tc_item** (BVA 3 + whitespace + chars + security + số đặc thù)
   - E05cp-E23cp (copy-paste): dùng `tc_group("Kiểm tra khi copy/paste giá trị", [tc_sub("Kiểm tra copy/paste maxlength", [tc_item("Max−1"), tc_item("Max"), tc_item("Max+1")]), ...])` — **19 tc_item**
4. **Nhóm H (Dropdown) / J (Multiselect) → BẮT BUỘC dùng `tc_group()` (MẶC ĐỊNH):**
   - H01-H06 / J01-J04 (tĩnh): dùng `tc()` bình thường
   - H07-H09 / J11-J13 (scroll): dùng `tc_group("Kiểm tra hiển thị scroll", [tc_sub("TH số bản ghi < 5"), ...])`
   - H10-H12 (chọn giá trị): dùng `tc_group("Kiểm tra chọn giá trị", [tc_sub("Chọn 1 giá trị"), tc_sub("Không cho phép chọn nhiều"), tc_sub("Bỏ chọn")])`
   - J07-J10 (chọn giá trị): dùng `tc_group("Kiểm tra chọn giá trị", [tc_sub("Chọn 1"), tc_sub("Chọn nhiều"), tc_sub("Bỏ chọn 1"), tc_sub("Bỏ chọn nhiều")])`
   - D22-D23 (search case): dùng `tc()` bình thường
   - D24-D28 (nhập tìm kiếm): dùng `tc_group("Kiểm tra nhập tìm kiếm", [tc_sub("Nhập tìm kiếm giá trị có trong danh sách", [tc_item("Tìm kiếm tương đối"), tc_item("Tìm kiếm tuyệt đối")]), ...])`
   - Xem chi tiết format tại `.agent/rules/manual_tc_excel_export.md`
5. Chạy script: `python scripts/gen_tc_<ten_chuc_nang>.py`
6. Báo cáo đường dẫn file `.xlsx` đã tạo và tổng số TC

**Quy tắc section/subsection trong ROWS:**

| Loại | Code trong script | Excel hiển thị |
|------|-------------------|----------------|
| Section UI | `section("Giao diện (Phần này viết...)")` | header màu xanh |
| Section BIZ | `section("Chức năng (Phần này viết các trường hợp kiểm thử kiểm tra các ràng buộc trong cơ sở dữ liệu và cho các luồng nghiệp vụ trong tài liệu giải pháp, tích hợp với các chức năng khác)")` | header màu xanh |
| Subsection control | `subsection("Nhóm X — Tên field (constraints)")` | "Kiểm tra tên field" (writer strip "Nhóm X — " + constraints) |
| Subsection BIZ | `subsection("Kiểm tra <tên> thành công")` | giữ nguyên (không match "Nhóm X —") |
| Subsection BIZ | `subsection("Kiểm tra <tên> không thành công")` | giữ nguyên |
| Subsection BIZ | `subsection("Kiểm tra phân quyền")` | giữ nguyên |
| Subsection button | `subsection("Kiểm tra button <Tên Button>")` | giữ nguyên — **ít nhất 3 TC chuẩn** (có thể thêm M04, M05) |

**Subsection BIZ — quy tắc tổ chức:**
- **"Kiểm tra X thành công"**: happy paths, alternate paths thành công, TCs nghiệp vụ tích cực
- **"Kiểm tra X không thành công"**: validation failures, constraint violations, exception paths
- **"Kiểm tra phân quyền"**: access control, button ẩn/hiện theo quyền
- Chỉ tạo subsection nào có TC — không bắt buộc đủ 3

**Subsection button — 3 TC chuẩn bắt buộc theo thứ tự:**
```python
subsection("Kiểm tra button <Tên Button>"),
tc(muc_dich="Mx_NNN - hiển thị button <tên>",   ket_qua="Button hiển thị giống như trong SRS", ...),
tc(muc_dich="Mx_NNN - trạng thái button <tên>", ket_qua="Trạng thái: Enable", ...),
tc(muc_dich="Mx_NNN - onclick button <tên>",    ket_qua='Onclick hệ thống thực hiện validate dữ liệu. Hệ thống lưu thông tin với trạng thái "<theo SRS>", chuyển về màn hình Danh sách.', ...),
```
> Chi tiết đầy đủ tại `.agent/rules/manual_tc_excel_export.md` → mục "Cấu trúc chuẩn subsection Kiểm tra button".

**Quy tắc mapping từ Bước 6 → `tc()` call:**

| Bảng Markdown (Bước 6) | Tham số `tc()` | Ghi chú |
|------------------------|----------------|---------|
| Test Title / Mục đích  | `muc_dich`     | Viết dạng `"Mx_NNN - mô tả chữ thường"` — writer tự strip ID, thêm "Kiểm tra ", lowercase |
| Test Scenario          | `truong_hop`   | |
| Test Data              | `data`         | |
| Test Steps             | `buoc`         | |
| Expected Result        | `ket_qua`      | |
| Priority               | `priority`     | `"Cao"` \| `"Trung bình"` \| `"Thấp"` |

> ⚠️ **KHÔNG** viết `muc_dich = "Kiểm tra ..."` — writer tự thêm tiền tố, sẽ bị lặp.
> ⚠️ **KHÔNG** dùng tên section `"Nghiệp vụ (...)"` cho BIZ — phải dùng `"Chức năng (Phần này viết...)"`.
> `subsection("Nhóm X — Tên field")` giữ format đó trong code — writer tự strip `"Nhóm X — "` trong Excel.

**Output:** File `.xlsx` tại `practices/testcases/<DU_AN>/<TenChucNang>_TestCases.xlsx`

---

## 📝 Work Log & Memory (khi user duyệt checkpoint)

> Nguồn chuẩn: `.agent/rules/worklog_memory_rules.md` — **BẮT BUỘC đọc tại thời điểm trigger**, không ghi theo trí nhớ.

- **Đầu session tiếp nối feature đã có:** đọc `practices/worklog/PROJECT_MEMORY.md` → `memory/<slug>_MEMORY.md` → tối đa 3 bản ghi Work Log gần nhất (§6), cùng với state file.
- **Tại checkpoint (B1, B2, B4, B5b; QUICK: TC Lead Review Gate):** khi user xác nhận **có nêu scope** (VD: *"duyệt B2 Q&A"*, `/pass B4`) → ghi `PASS`/`PARTIAL` vào `practices/worklog/<slug>_WORKLOG.md` + cập nhật Memory. `ok`/`xong` đứng một mình **không** phải trigger → hỏi lại scope.
- **Requirement/spec mới tác động nội dung đã duyệt:** ghi `REOPEN` (chưa duyệt → `Approval: PENDING`, change=`PENDING_REVIEW`, nội dung vào `practices/Q&A/<slug>_QA.md`).
- **Đối soát:** pipeline state trong Memory lấy `<FeatureName>_rbt_state.md` làm chuẩn; **không bao giờ** xóa change state khi đối soát.
- Báo cáo kết quả ghi trong **Tier 3 — Execution & Audit Summary**.

## Anti-Patterns (NGHIÊM CẤM — áp dụng cho cả 2 modes)

- ❌ **[B1-CRITICAL] Tự ý sang B2 khi chưa có xác nhận của user tại B1** — BẤT KỂ scope B1 có vẻ đầy đủ; PHẢI dừng và chờ user reply
- ❌ **[B1-CRITICAL] Đọc tài liệu không đầy đủ trước khi định nghĩa scope** — NGHIÊM CẤM kết luận \"không có tab/bảng X\" chỉ dựa trên TOC, tiêu đề section, hoặc đọc lướt. PHẢI đọc toàn bộ nội dung từng trang tài liệu
- ❌ **Bỏ qua Common TC Checklist** khi sinh TC (dù QUICK hay FULL RBT)
- ❌ Bỏ qua nhóm A (giao diện chung) hoặc nhóm M (button) — 2 nhóm luôn bắt buộc
- ❌ Sinh Group D thiếu cases cho trường TEXT (phải đủ **38 cases** = D01–D21 Nhập keyboard + D05cp–D21cp Copy-paste) — **Textbox KHÔNG có case tìm kiếm**; D22–D28 chỉ dành cho ô search trong popup Dropdown/Combobox
- ❌ Gộp nhiều trường TEXT vào 1 TC
- ❌ Gộp nhiều bước chạy 1 lần trong FULL RBT (PHẢI tuần tự)
- ❌ Tự đoán business logic khi chưa hỏi user (Bước 2 - FULL RBT)
- ❌ Bỏ qua bước phân tích Ambiguity (FULL RBT)
- ❌ Sinh test data chung chung / placeholder
- ❌ Rút gọn hoặc bỏ sót test case khi mapping sang bảng
- ❌ Sinh tất cả test cases 1 lần cho hệ thống lớn (phải chia module)
- ❌ Chỉ có Happy Path, thiếu Negative/Boundary cases
- ❌ Test Steps mơ hồ, không ghi rõ dữ liệu nhập
- ❌ **Bỏ qua TC Lead Review Gate (Bước 5b) — NGHIÊM CẤM xuất file khi chưa có xác nhận user**
- ❌ **Tự ý chuyển sang Bước 6 khi user chưa reply xác nhận sau Review Gate**
- ❌ **Tự đánh dấu "Đạt" cho tất cả tiêu chí để bỏ qua review — PHẢI review thực chất**
- ❌ Dùng `→` trong `muc_dich` để nối điều kiện hoặc flow — thay bằng `/` (nhiều mục đích) hoặc `"khi"` (điều kiện):
  - Sai: `"đổi chức năng cha → cập nhật vị trí trong tree"`
  - Đúng: `"đổi chức năng cha/ cập nhật vị trí trong tree"`
  - Sai: `"đổi hành động thường → khác → lưu ok"`
  - Đúng: `"chỉnh sửa khi đổi hành động từ hành động thường sang khác"`
- ❌ Subsection button thiếu 3 TC chuẩn — mỗi subsection "Kiểm tra button \<tên\>" **bắt buộc** có đủ: **hiển thị** ("Button hiển thị giống như trong SRS") / **trạng thái** ("Trạng thái: Enable") / **onclick** ("Onclick hệ thống thực hiện validate dữ liệu. Hệ thống lưu thông tin với trạng thái \<theo SRS\>, chuyển về màn hình Danh sách."). Xem cấu trúc đầy đủ trong `manual_tc_excel_export.md`.

---


## Output Format

### Mode QUICK

| Output | Mô tả |
|--------|--------|
| Draft TC (inline) | Test Cases draft, chưa xuất file |
| `tc_review_<module>.md` | Artifact báo cáo review — user chỉnh sửa trực tiếp |
| Bảng TC Markdown final | Xuất sau khi user confirm Review Gate |

### Mode FULL RBT

| Bước | Output |
|------|--------|
| 1 | Xác nhận bối cảnh |
| 2 | Luồng + Ambiguities + Câu hỏi Q&A |
| 3 | Module Decomposition + Dependencies |
| 4 | Traceability Matrix + High-Level Scenarios |
| 5 | Test Cases draft (Risk Level + Test Data) |
| **5b** | **`tc_review_<module>.md` — Báo cáo review (user chỉnh sửa + confirm)** |
| 6 | Bảng Markdown chuẩn (Jira/Excel ready) — chỉ xuất sau khi Bước 5b được confirm |
| **7** | **File `.xlsx` đúng template CIC — tạo bằng `scripts/tc_excel_writer.py`** |

Tất cả output phải bằng **Tiếng Việt**, format **Markdown**, xuất file **Excel**,sử dụng **Artifact** nếu nội dung dài.
