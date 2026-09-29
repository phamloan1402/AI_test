---
description: Tập hợp Common TC dùng chung cho mọi màn hình GUI, được tổ chức theo 23 nhóm (A–W) tương ứng với field type và chức năng. BẮT BUỘC áp dụng cho mọi workflow sinh test case (QUICK, FULL RBT, Review TC). Nguồn gốc: Checklist_commons_GUI.xlsx + Quy tắc component CUCI.
---

# Common TC Checklist — GUI

> **Phạm vi áp dụng:** Checklist này **BẮT BUỘC** cho mọi workflow sinh test case (QUICK, FULL RBT, Review TC).
> - **Nhóm D:** Bắt buộc đủ **38 cases** cho mỗi control Textbox (4 tĩnh D01–D04 + 17 Nhập D05–D21 + 17 Copy-paste D05cp–D21cp). **QUY TẮC CỐT LÕI: Textbox KHÔNG CÓ case "Kiểm tra nhập tìm kiếm"** (nghiệp vụ tìm kiếm thuộc về Section Chức năng hoặc Button Tìm kiếm, không đưa vào control Textbox). D22–D28 chỉ áp dụng khi có ô tìm kiếm option bên trong popup của Searchable Dropdown / Combobox.
>
> **Cách dùng hiệu quả:** KHÔNG đọc toàn bộ file mỗi lần. Sau khi lập Field Inventory, dùng **Bảng điều phối** để xác định nhóm áp dụng, rồi chỉ đọc các nhóm đó.
>
> **Tham chiếu bổ sung:** `Template/Quy+tắc+component.md` — Quy tắc FE chung cho CUCI. Khi sinh TC, **kết hợp** checklist này + Quy tắc component + SRS để xác định expected result chính xác. Nếu Quy tắc component mô tả hành vi cụ thể hơn checklist → ưu tiên Quy tắc component.

---

## Bảng điều phối — Field Type → Nhóm Common TC

| Field Type / Chức năng màn hình | Nhóm áp dụng | Prefix ID |
|---|---|---|
| **Mọi màn hình** | **A** (Giao diện chung) | `CMN_A` |
| Panel có collapse/expand | B | `CMN_B` |
| Danh sách dạng bảng (grid + paging) | C | `CMN_C` |
| TEXT (input single line) | D | `CMN_D` |
| NUMBER | E | `CMN_E` |
| EMAIL — TEXT có validate email | F | `CMN_F` |
| TEXTAREA | G | `CMN_G` |
| CBB (combobox searchable), DROPDOWN | H | `CMN_H` |
| CHECKBOX, CHECKBOX_GROUP | I | `CMN_I` |
| MULTI (multi-selectbox, không có ô tìm kiếm) | J | `CMN_J` |
| MULTISELECT+SEARCH (multi-select **có ô tìm kiếm**) | J + D *(ô search)* | `CMN_J`, `CMN_D` |
| DATE, DATETIME | K | `CMN_K` |
| PASSWORD | L | `CMN_L` |
| **Mọi màn hình có button action** | **M** (Button) | `CMN_M` |
| RADIO | N | `CMN_N` |
| IP Address (TEXT đặc biệt) | O | `CMN_O` |
| Chức năng Xóa bản ghi | P | `CMN_P` |
| FILE UPLOAD | Q | `CMN_Q` |
| Chức năng Import | R | `CMN_R` |
| Chức năng có phân quyền truy cập | S | `CMN_S` |
| Màn hình tra cứu có khu vực tìm kiếm nhiều trường | T | `CMN_T` |
| Grid kết quả có trường dữ liệu chỉnh sửa và cột thao tác | U | `CMN_U` |
| Màn hình Chỉnh sửa (Edit Form) | V *(+ nhóm theo field type cho trường được phép sửa)* | `CMN_V` |
| Component phức tạp: Checkbox Matrix (W1), Tag Input Email (W2), Status Badge (W3), Dynamic Form Visibility (W4) | W *(chỉ sub-group tương ứng)* | `CMN_W` |

### Quy ước định dạng trường & Tên Session / Subsection chuẩn (BẮT BUỘC)
Khi phân rã màn hình, lập Field Inventory và đặt tên tiêu đề phân nhóm (Subsection) cho từng trường:
- **Ô nhập chữ** (TEXT single line) => **Textbox** → Tiêu đề: `Kiểm tra Textbox <Tên trường>`
- **Danh sách chọn một** (Dropdown single select, CBB chọn 1) => **Dropdown** → Tiêu đề: `Kiểm tra Dropdown <Tên trường>`
- **Ô nhập nhiều dòng** (TEXTAREA) => **Area box** → Tiêu đề: `Kiểm tra Area box <Tên trường>`
- **Danh sách chọn nhiều / Ô chọn nhiều** (MULTISELECT, Multi-selectbox, Checkbox chọn dòng) => **Combobox** → Tiêu đề: `Kiểm tra Combobox <Tên trường>`
- **Ô nhập số** (NUMBER, integer, decimal) => **Number** → Tiêu đề: `Kiểm tra Number <Tên trường>`

**Format ID:** `[FEATURE]_[SỐ]`
> Ví dụ: `M1_001`, `M1_002`, `M2_001` — không phân biệt Common/Business trong ID; phân biệt bằng phân loại nội bộ (UI / CMN / BIZ) khi tổ chức TC

### 📌 QUY ƯỚC CỘT C (TRƯỜNG HỢP KIỂM THỬ) — BỎ HẾT MÃ NHÓM & STT (BẮT BUỘC)
- **Cột C (Trường hợp kiểm thử):** Tuyệt đối **KHÔNG** chứa bất kỳ mã nhóm hay tiền tố STT nào (CẤM ghi `K01 — `, `K02 — `, `A01 — `, `D01 — `, `E01 — `, `H06 — `, `C01 — `, `M01 — `, `CONF_001 — `, `V01 — `, `E_SP_01 — `, `1. `...).
- **Nội dung Cột C:** Chỉ ghi trực tiếp hành vi / trường hợp cần kiểm thử, viết hoa chữ cái đầu tiên (Ví dụ: *"Focus Calendar khi ô Thời gian gửi yêu cầu từ ngày đến ngày trống"*, *"Chọn khoảng ngày từ Calendar popup"*, *"Bấm icon (X) xóa ngày"*, *"Kiểm tra hiển thị nút Gửi yêu cầu"*, *"Nút Đồng ý trên popup xác nhận"*).
- **Mã nhóm (K01, D01, H06, M01...):** Chỉ dùng làm mã tham chiếu nội bộ trong tài liệu checklist này, **TUYỆT ĐỐI KHÔNG ĐƯA VÀO CỘT C TRONG FILE EXCEL**.

---

## Hướng dẫn áp dụng (3 bước)

**3b.1 — Xác định nhóm:** Dùng bảng điều phối trên, tick nhóm theo Field Inventory.

**3b.2 — Điều chỉnh theo spec:**
- TC có chú thích `(tùy spec)` → xác định expected result từ tài liệu trước khi sinh.
- TC có chú thích `(nếu có)` → xác định có áp dụng hay không trong tài liệu SRS.
- **Nhiều field cùng loại → mỗi field PHẢI có đủ toàn bộ checklist riêng.** NGHIÊM CẤM cắt bớt case cho field thứ 2 trở đi. VD: Nếu màn hình có 4 dropdown thì cả 4 đều phải có đủ H01-H12 (+ scroll + chọn giá trị + search nếu có).
- TC không áp dụng → đánh `N/A` + ghi lý do vào cột `Ghi chú`.

**3b.3 — Gán ID:** Dùng format `[FEATURE]_[SỐ]` (VD: `M1_001`).

---

## Chi tiết các nhóm TC

### Nhóm A — Giao diện chung *(Luôn áp dụng)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| A01 | Kiểm tra hiển thị | Hiển thị giao diện như trong SRS bao gồm:<br>- Title màn hình<br>- Đường dẫn chức năng<br>- Các Button tác vụ (Xuất excel, Thêm mới...)<br>- Các block bộ lọc (Textbox, Dropdown list...)<br>- Danh sách dưới grid view bao gồm (liệt kê đủ các cột):<br>  + STT: Grid column<br>  + [Tên cột]: Grid column<br>- Phân trang |
| A02 | Kiểm tra tổng thể giao diện màn hình | 1. Các label, textbox, combo có độ dài, rộng và khoảng cách bằng nhau, không xô lệch<br>2. Các label sử dụng cùng 1 loại font, cỡ chữ, căn lề trái<br>3. Các trường bắt buộc nhập phải có dấu (*)<br>4. Kiểm tra tất cả lỗi về chính tả, cấu trúc câu, ngữ pháp trên màn hình<br>5. Form được bố trí hợp lý và dễ sử dụng |
| A03 | Thứ tự di chuyển trỏ trên màn hình khi nhấn phím Tab | Con trỏ di chuyển lần lượt trên các trường input, button, hyperlink theo thứ tự trái sang phải, trên xuống dưới |
| A04 | Thứ tự di chuyển trỏ trên màn hình khi nhấn phím Shift+Tab | Con trỏ di chuyển theo thứ tự ngược lại trên các trường input, các button, hyperlink: từ dưới lên trên, từ phải sang trái |
| A05 | Phím Enter | Focus button chính → kích hoạt thao tác mặc định; tại trường input → kích hoạt tìm kiếm hoặc form submit mặc định |
| A06 | Tính năng responsive màn hình (Ctrl+−, Ctrl+=) | Layout hiển thị hài hòa, không tràn khung, không vỡ giao diện ở các mức zoom 75%, 100%, 125%, 150% |
| A07 | Phím tắt CRUD *(QT component)* | F3/Ctrl+N → Tạo mới; F5 → Refresh; Ctrl+Shift+E → Xuất Excel; Ctrl+P → In *(tùy spec)* |
| A08 | Ngôn ngữ tiếng Việt chuẩn hành chính *(QT component)* | Không viết tắt không định nghĩa; từ viết tắt phải có tooltip |

---

### Nhóm B — Collapse / Expand *(Nếu có panel thu gọn)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| B01 | Click nút Collapse (−) | Panel ẩn, hiển thị `[+] <title>` |
| B02 | Click nút Expand (+) | Panel hiện, hiển thị `[−] <title>` |

---

### Nhóm C — Grid + Paging *(Nếu có danh sách dạng bảng)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| C01 | Format Grid | Header căn giữa; giá trị: text trái, số phải, date/STT/Thao tác căn giữa. Cột STT và Thao tác cố định |
| C02 | Số thứ tự bản ghi | STT tăng dần liên tục qua các trang |
| C03 | Không hiển thị paging khi ≤ 10 bản ghi | Control phân trang ẩn |
| C04 | Số bản ghi/trang đúng cấu hình *(dùng tc_group — xem bên dưới)* | Mặc định 20; tùy chọn 10/20/50/100 |
| C05 | Style paging | Format: `Hiển thị 1–20 trong N kết quả` + Trang X/Y + Bản ghi/trang |
| C06 | Mở trang bất kỳ (đầu/cuối/giữa) *(dùng tc_group — xem bên dưới)* | Load đúng trang, STT đầu tiên tiếp nối trang trước |
| C07 | Header/footer không đổi khi chuyển trang | Layout ổn định |
| C08 | Thay đổi số bản ghi/trang *(dùng tc_group — xem bên dưới)* | Back về trang 1, số trang tính lại đúng |
| C09 | Thêm/Sửa/Xóa từ trang N | Quay về trang 1 sau action |
| C10 | Xóa bản ghi cuối trang cuối | Không còn trang rỗng, quay về trang N−1 |
| C11 | Skeleton loading khi đang tải dữ liệu *(QT component)* | Hiển thị skeleton loading thay vì bảng trống |
| C12 | Grid trống — không có dữ liệu *(QT component)* | Hiển thị "Không có dữ liệu" + icon |
| C13 | Icon mở rộng full screen *(QT component)* | Nhấn icon → grid mở full screen; nhấn lại → thu nhỏ |
| C14 | Filter trên từng cột (trừ STT, Thao tác) *(QT component)* | Nhập giá trị → lọc trên trang hiện tại; icon "x" xóa filter |
| C15 | Cột Ngày — hover hiển thị đầy đủ *(QT component)* | Hiển thị dd/mm/yyyy; hover → dd/mm/yyyy HH:MM:SS |
| C16 | Cột Người — hover hiển thị họ tên *(QT component)* | Hiển thị username; hover → Họ và tên đầy đủ |

> **Quy tắc tc_group cho Phân trang (BẮT BUỘC):** C04, C06, C08 được mở rộng thành 3 `tc_group()`:
> - `tc_group("Kiểm tra phân trang", [...])` — 5 sub: mặc định (20/trang), trang cuối (last-page disabled), trang đầu (first-page disabled), next trang, previous trang
> - `tc_group("Kiểm tra combobox phân trang", [...])` — 6 sub: giá trị mặc định, giá trị trong combobox (10/20/30/40/50/80/100), chọn 1, chọn nhiều (không cho phép), không chọn, phím tắt lên/xuống+Enter
> - `tc_group("Kiểm tra nhập tìm kiếm số trang", [...])` — 4 sub: ký tự chữ (chặn), ký tự đặc biệt (chặn), ký tự số (cho phép + di chuyển), vượt max (hiển thị trang cuối)
>
> Khi đã dùng 3 tc_group trên: **bỏ** các `tc()` riêng lẻ C04, C06, C08 để tránh trùng lặp. Giữ lại C05 (Style paging — kiểm tra format chuỗi hiển thị).

---

### Nhóm D — Textbox / TEXT field *(Bắt buộc đầy đủ cho mọi trường text)*

> Nhiều trường cùng loại → tạo nhiều section, mỗi section tương ứng cho 1 trường (`Kiểm tra Textbox <Tên trường>`).
> - **TEXT (Textbox):** Chuẩn **38 cases** = 4 cases tĩnh (D01–D04) + 17 cases Nhập keyboard (D05–D21, trong đó D05–D07 được gom vào `tc_sub("Kiểm tra nhập maxlength")`) trong `tc_group("Kiểm tra khi nhập giá trị")` + 17 cases Copy-paste (D05cp–D21cp, trong đó D05cp–D07cp được gom vào `tc_sub("Kiểm tra copy/paste maxlength")`) trong `tc_group("Kiểm tra khi copy/paste giá trị")`.
> - ⚠️ **QUY TẮC CỐT LÕI (BẮT BUỘC): Textbox TUYỆT ĐỐI KHÔNG CÓ case "Kiểm tra nhập tìm kiếm".** Kể cả khi ô text nằm trong thanh bộ lọc tra cứu, nó vẫn chỉ là control Textbox và chỉ kiểm tra hành vi nhập/paste của control (38 cases). Hành vi tìm kiếm (lọc tương đối, tuyệt đối, không có dữ liệu, phân biệt hoa/thường/dấu...) thuộc về **Section Chức năng (BIZ)** khi nhấn Button Tìm kiếm hoặc Enter, KHÔNG đưa vào subsection Textbox.
> - **Quy tắc lặp Copy-paste:** Các case D05–D21 (Nhập keyboard) được lặp lại đối xứng với prefix "Copy-paste" thành D05cp–D21cp trong `tc_group("Kiểm tra khi copy/paste giá trị")` (bắt đầu bằng `tc_sub("Kiểm tra copy/paste maxlength")`). Hành vi Ctrl+V có thể khác bàn phím: D07cp — QT component **luôn truncate** khi paste vượt maxlength (không block); các ký tự bị chặn theo charset vẫn bị lọc khi paste.
> - **ID range trong script:** Nhập keyboard = ID thường (VD: M2_007–M2_027); Copy-paste = ID cao hơn 500 (VD: M2_500–M2_516) để tránh đụng.

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| D01 | Giá trị mặc định | Trống |
| D02 | Kiểm tra hiển thị UI (kích thước, căn lề, viền) | Hiển thị đúng theo design / Figma |
| D03 | Kiểm tra placeholder | Hiển thị đúng text placeholder theo spec |
| D04 | Kiểm tra trường bắt buộc | Thông báo lỗi + focus vào trường hoặc *(tùy spec)* |
| D05 | Nhập (Max − 1) ký tự | Thành công |
| D06 | Nhập đúng Max ký tự | Thành công |
| D07 | Nhập (Max + 1) ký tự / copy-paste vượt giới hạn | HT tự động chặn khi nhập quá maxlength; paste vượt → cắt bớt *(QT component)* |
| D08 | Nhập toàn khoảng trắng (vd: `"   "`) | Thông báo lỗi hoặc coi như rỗng theo spec |
| D09 | Nhập khoảng trắng đầu và cuối (vd: `" ABC "`) | HT tự động trim khi blur + trim khi submit *(QT component)* |
| D10 | Nhập khoảng trắng giữa ký tự (vd: `"A B"`) | Cho phép, lưu đúng |
| D11 | Nhập nhiều khoảng trắng giữa ký tự (vd: `"A   B"`) | Theo spec: trim hoặc giữ nguyên |
| D12 | Nhập ký tự in hoa (vd: `"NGUYEN VAN A"`) | Thành công, không lỗi font |
| D13 | Nhập ký tự in thường (vd: `"nguyen van a"`) | Thành công, không lỗi font |
| D14 | Nhập ký tự số (vd: `"1234567890"`) | Thành công |
| D15 | Nhập ký tự đặc biệt (vd: `"!@#$%^&*()_+"`) | Theo spec: chặn tại input kèm thông báo inline hướng dẫn nhập đúng *(QT component)* HOẶC cho phép |
| D16 | Nhập ký tự hỗn hợp (vd: `"abc123!@#"`) | Theo spec |
| D17 | Nhập tiếng Việt có dấu (vd: `"Nguyễn Văn A"`) | Thành công, không lỗi font |
| D18 | Nhập HTML / XSS (vd: `<script>alert('xss')</script>`) | Không execute; lưu/hiển thị đúng ký tự thô |
| D19 | Nhập SQL injection (vd: `' OR '1'='1`) | Không inject; xử lý an toàn |
| D20 | Nhập URL (vd: `https://www.google.com`) | Theo spec: lưu dạng text thuần |
| D21 | Nhập CSRF payload (vd: `<img src=x onerror=alert(1)>`) | Không execute; xử lý an toàn |

**Đặc thù ô tìm kiếm option trong Dropdown/Combobox (D22–D28)** *(CHỈ áp dụng cho popup Dropdown/Combobox có ô search option, TUYỆT ĐỐI KHÔNG áp dụng cho Textbox)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| D22 | Tìm kiếm không phân biệt hoa/thường  | Kết quả đúng bất kể case |
| D23 | Tìm kiếm không phân biệt có dấu/không dấu  | Nhập "nguyen" tìm được "Nguyễn"; nhập "Nguyễn" tìm được "nguyen" |
| D24 | Tìm kiếm giá trị tương đối có trong danh sách  | Hệ thống hiển thị danh sách giá trị tương ứng theo kết quả nhập vào.|
| D25 | Tìm kiếm giá trị tuyệt đối có trong danh sách  | Hệ thống hiển thị danh sách giá trị tương ứng theo kết quả nhập vào.|
| D26 | Tìm kiếm giá trị không có trong danh sách | Hệ thống hiển thị thông báo “Không có dữ liệu” hoặc danh sách trống.|
| D27 | Kiểm tra nhập tìm kiếm <= <max_length_number> | Hệ thống cho phép nhập.|
| D28 | Kiểm tra nhập tìm kiếm > <max_length_number> | Hệ thống chặn không cho nhập quá <max_length_number> ký tự.|

---

### Nhóm E — Number field
> - **NUMBER:** **42 cases** = 4 cases tĩnh (E01–E04) + 19 cases Nhập keyboard (E05–E23) + 19 cases Copy-paste (E05cp–E23cp).
> - **Quy tắc BVA:** E05–E07 **BẮT BUỘC** nằm trong `tc_group("Kiểm tra khi nhập giá trị")` dưới dạng `tc_sub("Kiểm tra nhập maxlength")` (giống D05–D07). tc_group chứa E05–E23 = **19 tc_item**.
> - **Quy tắc lặp Copy-paste:** Các case E05–E23 (bao gồm BVA) được lặp lại với prefix "Copy-paste" thành E05cp–E23cp = **19 tc_item** trong tc_group "Kiểm tra khi copy/paste giá trị". Hành vi Ctrl+V có thể khác bàn phím: E07cp — QT component luôn truncate khi paste vượt maxlength (không block), tương tự nhóm D.

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| E01 | Giá trị mặc định | Trống |
| E02 | Kiểm tra hiển thị UI (kích thước, căn lề, viền) | Hiển thị đúng theo design / Figma |
| E03 | Kiểm tra placeholder | Hiển thị đúng text placeholder theo spec |
| E04 | Kiểm tra trường bắt buộc | Thông báo lỗi + focus vào trường hoặc *(tùy spec)* |
| E05 | Nhập (Max − 1) ký tự | Thành công |
| E06 | Nhập đúng Max ký tự | Thành công |
| E07 | Nhập (Max + 1) ký tự / copy-paste vượt giới hạn | HT tự động chặn khi nhập quá maxlength; paste vượt → cắt bớt *(QT component)* |
| E08 | Nhập toàn khoảng trắng (vd: `"   "`) | Thông báo lỗi hoặc coi như rỗng theo spec |
| E09 | Nhập khoảng trắng đầu và cuối (vd: `" 12 "`) | HT tự động trim khi blur + trim khi submit *(QT component)* |
| E10 | Nhập khoảng trắng giữa ký tự (vd: `"1 2"`) | Cho phép, lưu đúng |
| E11 | Nhập nhiều khoảng trắng giữa ký tự (vd: `"1   2"`) | Theo spec: trim hoặc giữ nguyên |
| E12 | Nhập ký tự chữ/ký tự không phải số (vd: `"ABc123"`) | Theo spec: chặn tại input kèm thông báo inline hướng dẫn nhập đúng *(QT component)* HOẶC cho phép |
| E13 | Nhập ký tự số (vd: `"1234567890"`) | Thành công |
| E14 | Nhập ký tự đặc biệt (vd: `"!@#$%^&*()_+"`) | Theo spec: chặn tại input kèm thông báo inline hướng dẫn nhập đúng *(QT component)* HOẶC cho phép |
| E15 | Nhập ký tự hỗn hợp (vd: `"abc123!@#"`) | Theo spec |
| E16 | Nhập HTML / XSS (vd: `<script>alert('xss')</script>`) | Hệ thống chặn không cho phép nhập |
| E17 | Nhập SQL injection (vd: `' OR '1'='1`) | Hệ thống chặn không cho phép nhập |
| E18 | Nhập URL (vd: `https://www.google.com`) | Hệ thống chặn không cho phép nhập |
| E19 | Nhập CSRF payload (vd: `<img src=x onerror=alert(1)>`) | Hệ thống chặn không cho phép nhập |
| E20 | Nhập số thập phân *(tùy spec)* | Theo spec: cho phép hoặc thông báo lỗi |
| E21 | Nhập số âm *(tùy spec)* | Theo spec: cho phép hoặc thông báo lỗi |
| E22 | Nhập số chữ số thập phân vượt quy định | Thông báo lỗi hoặc tự làm tròn theo spec |
| E23 | Nhập số có chữ số 0 đầu *(tùy spec)* | Theo spec |

---

### Nhóm F — Email field *(Nếu có trường email)*

> Nhiều trường cùng loại → tạo nhiều section, mỗi section bao gồm đầy đủ **38 cases** của **Nhóm D** (Các case cơ bản về bỏ trống, độ dài, khoảng trắng, v.v. đã được bao phủ bởi Nhóm D) và bổ sung thêm các **cases nhóm F** (đặc thù cho email) tương ứng cho 1 trường. Kết quả mong muốn theo mô tả *(tùy spec)*
| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| F02 | Nhập email đã tồn tại *(nếu unique)* | Thông báo email đã tồn tại |
| F03 | Email thiếu `@` hoặc `.` | Thông báo định dạng không hợp lệ |
| F06 | Định dạng email không hợp lệ (nhiều `@`, thiếu domain...) | Thông báo lỗi |
| F07 | Định dạng email hợp lệ (`abc@gmail.com`, `abc-cd@yahoo.com`) | Thành công |

---

### Nhóm G — Textarea

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| G01 | Giá trị mặc định | Trống |
| G02 | Kiểm tra trường bắt buộc | Bắt buộc phải chọn hoặc *(tùy spec)*|
| G03 | Nhập quá maxlength (thường 300+ ký tự) | Thông báo vượt maxlength |
| G04 | Nhập ký tự đặc biệt / HTML | Không execute; lưu/hiển thị đúng |
| G05 | Trim space đầu/cuối | Data lưu đã trim |
| G06 | Nhập tiếng Việt có dấu | Thành công |
| G07 | Nhập nhiều dòng (Enter xuống dòng) | Hiển thị đúng nhiều dòng như khi nhập |
| G08 | Nhập (Max − 1) ký tự | Thành công |
| G09 | Nhập đúng Max ký tự | Thành công |
| G10 | Nhập (Max + 1) ký tự / copy-paste vượt giới hạn | Paste vượt → cắt bớt phần dư + thông báo inline *(QT component)* |
| G11 | Bộ đếm ký tự realtime *(QT component)* | Hiển thị "đã dùng/tối đa" (VD: 150/500) cập nhật theo thời gian thực |
| G12 | Auto resize chiều cao theo nội dung *(QT component)* | TextArea tự động mở rộng; giới hạn maxRows không vỡ layout |

---

### Nhóm H — Combobox / Dropdown

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| H01 | Kiểm tra hiển thị | Hiển thị dropdown list theo design căn chỉnh figma |
| H02 | Kiểm tra giá trị mặc định | Rỗng *(tùy spec)* |
| H03 | Kiểm tra placeholder | Hiển thị placeholder theo *(tùy spec)* |
| H04 | Kiểm tra trường bắt buộc | Bắt buộc phải chọn hoặc *(tùy spec)*|
| H05 | Options hiển thị đúng | Số lượng, thứ tự, nội dung option đúng spec/DB |
| H06 | Sử dụng bàn phím | Nhấn Tab/Shift+Tab focus → Enter mở list → Up/Down duyệt option → Enter chọn giá trị → Tab/Shift+Tab chuyển field tiếp theo |
| H07 | Kiểm tra hiển thị scroll khi số bản ghi < 5 | Không hiển thị thanh scroll |
| H08 | Kiểm tra hiển thị scroll khi số bản ghi > 5 | Hiển thị thanh scroll |
| H09 | Kiểm tra hiển thị scroll khi số bản ghi = 5 | Không hiển thị thanh scroll |
| H10 | Kiểm tra chọn 1 giá trị | Hệ thống cho phép chọn 1 giá trị và hiển thị giá trị được chọn lên, đồng thời đóng dropdown list. Giá trị đã chọn được focus |
| H11 | Kiểm tra chọn nhiều giá trị | Không cho phép chọn nhiều giá trị. Hiển thị giá trị gần nhất được chọn lên dropdown list hoặc *(tùy spec)* |
| H12 | Kiểm tra bỏ chọn giá trị đã chọn | Bỏ chọn giá trị đã chọn |
| H13 | Kiểm tra options — API thành công, có dữ liệu | Dropdown hiển thị đầy đủ danh sách options đúng theo dữ liệu API trả về |
| H14 | Kiểm tra options — API thành công, không có dữ liệu | Dropdown hiển thị trạng thái rỗng: "Không có dữ liệu" + icon *(QT component)* |
| H15 | Kiểm tra options — API thất bại (lỗi server/mạng) | Hiển thị thông báo lỗi hoặc trạng thái rỗng theo spec; không crash UI |
| H16 | Kiểm tra options — API timeout | Loading state trong thời gian chờ; sau timeout hiển thị thông báo lỗi hoặc trạng thái rỗng; UI không bị treo |
| H17 | Kiểm tra dropdown bắt buộc / chỉ đọc không cho bỏ chọn *(nếu có)* | Dropdown hiển thị trạng thái disabled hoặc readonly; người dùng không thể xóa/thay đổi giá trị đã chọn; giá trị vẫn được submit trong form |



> ⚠️ **QUY TẮC QUAN TRỌNG — NHIỀU DROPDOWN:**
> Khi màn hình có **nhiều trường Dropdown / Combobox**, **MỌI trường đều PHẢI có đủ H01–H16** (bao gồm scroll group 3 TH, chọn giá trị group 3 sub, search group nếu có, và API states H13-H16). **NGHIÊM CẤM** chỉ sinh đầy đủ cho dropdown đầu tiên rồi cắt bớt cho các dropdown còn lại. Lý do: mỗi dropdown có data source khác nhau, hành vi scroll/search/options đều cần kiểm tra riêng.

> **Cấu trúc tc_group cho H13-H16 (BẮT BUỘC):** Gộp 4 cases vào 1 `tc_group("Kiểm tra options hiển thị đúng", [...])` với:
> - `tc_sub("TH call API thành công")` → `tc_item("TH dữ liệu trả về khác rỗng")` + `tc_item("TH dữ liệu trả về là rỗng")`
> - `tc_sub("TH Call API bị thất bại")` → 1 tc_item
> - `tc_sub("TH Call API bị time out")` → 1 tc_item

**Lưu ý:**
- Nếu dropdown có **nhiều hơn 5 options**, không sinh TC duyệt hết từng option → chỉ sinh TC chọn option đầu, giữa, cuối và option bất kỳ.
- Nếu dropdown có **search**, sinh thêm TC nhập ký tự để test search. Dùng quy tắc tìm kiếm trong nhóm D
- *(QT component)* Khi danh sách ≥ 10 items → bắt buộc có search + virtual scroll.
- *(QT component)* Debounce 300ms khi search (gõ xong 300ms mới gọi API).
- *(QT component)* Đang tải → hiển thị loading spinner trong dropdown.
- *(QT component)* Không có kết quả → hiển thị "Không tìm thấy dữ liệu".
- *(QT component)* Click vào toàn bộ vùng control đều mở dropdown (không chỉ icon arrow).
- *(QT component)* Validate khi blur + submit.

---

### Nhóm I — Checkbox

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| I01 | Kiểm tra hiển thị | Hiển thị checkbox theo design căn chỉnh figma |
| I02 | Kiểm tra giá trị mặc định | Checked hoặc Unchecked *(tùy spec)* |
| I03 | Kiểm tra check | Trạng thái: Enable |
| I04 | Kiểm tra trạng thái | Hiển thị trạng thái check |
| I05 | Kiểm tra uncheck | Hiển thị trạng thái uncheck |
| I06 | Check All → tick tất cả *(nếu có)* | Mọi checkbox con được tick |
| I07 | Bỏ 1 checkbox khi đang Check All *(nếu có)* | Checkbox Check All cũng bỏ tick |
| I08 | Checkbox bật/tắt đối tượng khác *(nếu có)* | Tick → hiện element; bỏ tick → ẩn element |
| I09 | Ràng buộc chọn trước Sửa/Xóa *(nếu có)* | Chưa chọn → thông báo; chọn >1 khi Sửa → thông báo |
| I10 | Kiểm tra checkbox bắt buộc luôn được chọn (mandatory/disabled) *(nếu có)* | Checkbox hiển thị ở trạng thái checked và disabled; người dùng không thể bỏ tick; checkbox vẫn được gửi lên server trong form submit |

---

### Nhóm J — Multi-selectbox

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| J01 | Kiểm tra hiển thị | Hiển thị dropdown list theo design căn chỉnh figma |
| J02 | Giá trị mặc định | Không có giá trị nào được chọn |
| J03 | Kiểm tra placeholder | Hiển thị placeholder theo *(tùy spec)* |
| J04 | Bỏ trống trường Required | Thông báo bắt buộc phải chọn hoặc theo SRS |
| J05 | Thứ tự sắp xếp giá trị | Sắp xếp đúng điều kiện quy định (A-Z hoặc theo DB) |
| J06 | Căn lề các giá trị trong list | Căn trái |
| J07 | Kiểm tra chọn 1 giá trị | Hệ thống cho phép chọn 1 giá trị và hiển thị giá trị được chọn lên. Giá trị đã chọn được focus |
| J08 | Chọn nhiều giá trị cùng lúc | Cho phép chọn đồng thời nhiều item và hiển thị giá trị được chọn lên. Giá trị đã chọn được focus |
| J09 | Kiểm tra bỏ chọn 1 giá trị đã chọn | Bỏ chọn 1 giá trị đã chọn |
| J10 | Kiểm tra bỏ chọn nhiều giá trị đã chọn | Bỏ chọn nhiều giá trị đã chọn (click bỏ check từng item) |
| J10b | Kiểm tra bỏ chọn bằng dấu x (icon ×) trên tag đã chọn *(QT component)* | Click icon × trên từng tag giá trị đã chọn → giá trị bị xóa khỏi danh sách đã chọn; danh sách dropdown vẫn mở *(tùy spec)* |
| J11 | Kiểm tra hiển thị scroll khi số bản ghi < 5 | Không hiển thị thanh scroll |
| J12 | Kiểm tra hiển thị scroll khi số bản ghi > 5 | Hiển thị thanh scroll |
| J13 | Kiểm tra hiển thị scroll khi số bản ghi = 5 | Không hiển thị thanh scroll |
| J14 | Kiểm tra focus vào option có ký tự đầu tiên map với ký tự đánh từ bàn phím | Focus item đầu tiên bắt đầu bằng ký tự vừa nhập |

**Lưu ý:**
- Nếu multi-select có **ô search** (MULTISELECT+SEARCH), sinh thêm TC nhập ký tự để test search. Dùng quy tắc tìm kiếm trong nhóm D (D22 case-insensitive bắt buộc; D18–D21 security tùy spec).
- Ô search trong multi-select là TEXT field → áp dụng Group D độc lập cho từng ô search.
- *(QT component)* Khi chọn nhiều giá trị: hiển thị **"item1 + N items"** và có icon "x" để bỏ chọn từng giá trị.
- *(QT component)* Mặc định hiển thị 10 items → phần còn lại load khi scroll hoặc search.
- *(QT component)* Khi số lượng option ≥ 10 → bắt buộc có search trong dropdown.

---

### Nhóm K — Date / DateTime field

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| K01 | Focus Calendar khi textbox trống | Highlight ngày hiện tại hệ thống |
| K02 | Focus Calendar khi textbox có giá trị | Highlight ngày đang có trong textbox |
| K03 | Chọn ngày từ Calendar | Calendar đóng, textbox hiển thị ngày đã chọn |
| K04 | Nút Bỏ chọn *(nếu có)* | Textbox reset về rỗng |
| K05 | Bỏ trống trường Required | Thông báo bắt buộc + focus |
| K06 | Sai định dạng (không phải dd/MM/yyyy) *(nếu cho phép nhập)* | Thông báo sai định dạng + focus |
| K07 | Đúng định dạng nhưng ngày không tồn tại (VD: 31/02/2024) *(nếu cho phép nhập)* | Thông báo ngày không tồn tại |
| K08 | Ngày hợp lệ: cuối tháng, 29/02 năm nhuận *(nếu cho phép nhập)* | Thành công |
| K09 | Ngày > hôm nay *(nếu cấm tương lai)* | Thông báo không được lớn hơn ngày hiện tại |
| K10 | Ngày = hôm nay *(nếu cấm ngày hiện tại)* | Thông báo không được là ngày hiện tại |
| K11 | Ngày < hôm nay *(nếu cấm quá khứ)* | Thông báo không được nhỏ hơn ngày hiện tại |
| K12 | Từ ngày > Đến ngày | Thông báo Từ ngày phải ≤ Đến ngày. Tự động cảnh báo *(QT component)* |
| K13 | Từ ngày = Đến ngày | Thành công |
| K14 | Từ ngày < Đến ngày | Thành công |
| K15 | Nhập tay ngày hợp lệ vào ô DatePicker *(QT component)* | Cho phép nhập tay; validate khi blur |
| K16 | Nhập tay ký tự không hợp lệ (chữ, ký tự đặc biệt khác "/") *(QT component)* | Hiển thị lỗi ngay khi blur |
| K17 | Nhập ngày < 01/01/1900 (khi nhập liệu, không áp dụng tìm kiếm) *(QT component)* | Không cho nhập; hiển thị lỗi |

---

### Nhóm L — Password field *(Nếu có)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| L01 | Nhập ký tự hợp lệ | Mã hóa thành `***`, lưu thành công |
| L02 | Nhập quá maxlength (thường 30 ký tự) | Không cho nhập / thông báo lỗi |
| L03 | Nhập số | Cho phép |
| L04 | Nhập ký tự đặc biệt | Cho phép |
| L05 | Kiểm tra ràng buộc pattern *(tùy spec)* | Đúng pattern quy định |

---

### Nhóm M — Button *(Luôn áp dụng nếu có button action)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| M01 | Căn lề, chính tả label button | Text căn giữa, chữ thường + chữ cái đầu in hoa *(QT component)*, không lỗi chính tả |
| M02 | Trạng thái enabled/disabled theo điều kiện | Hiển thị đúng trạng thái; chỉ 1 Primary Button trong 1 khu vực *(QT component)* |
| M03 | Click button → thực hiện đúng chức năng | Action đúng theo spec |
| M04 | Loading + disable khi đang xử lý *(QT component)* | Hiển thị loading spinner + disable button → tránh submit nhiều lần |
| M05 | Button Tìm kiếm → F5/chuyển trang → quay lại *(QT component)* | Giữ được bộ lọc + cấu hình hiển thị đã chọn trước đó |

> ⚠️ **QUY TẮC BẮT BUỘC — Button Xuất Excel:**
> Nếu màn hình Tra cứu / Danh sách có nút **Xuất Excel**, PHẢI sinh `subsection("Kiểm tra button Xuất Excel")` với ít nhất 3 TC chuẩn: (1) Hiển thị button, (2) Trạng thái button, (3) Onclick button (tải file, tên file, nội dung file theo bộ lọc). **KHÔNG** được bỏ qua chỉ vì button Xuất Excel không thuộc phần Nghiệp vụ — button này thuộc phần Giao diện.

---

### Nhóm N — Radio button

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| N01 | Kiểm tra giá trị mặc định | Không chọn hoặc chọn mặc định theo spec |
| N02 | Kiểm tra bắt buộc | Không chọn hoặc chọn mặc định theo spec |
| N03 | Kiểm tra chọn 1 option | Cho phép, chỉ 1 option được chọn tại 1 thời điểm |
| N04 | Kiểm tra bỏ chọn 1 option | Cho phép bỏ chọn option đã chọn |

---

### Nhóm O — IP Address field *(Nếu có)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| O01 | Giá trị mặc định | Trống |
| O02 | Nhập IP hợp lệ (`192.168.168.179`) | Thành công |
| O03 | Nhập ký tự chữ / đặc biệt / tiếng Việt / space | Thông báo lỗi |
| O04 | Nhập quá maxlength (15 ký tự) | Không cho nhập |
| O05 | IP có cổng (`192.168.168.179:8001`) *(nếu cho phép)* | Thành công |

---

### Nhóm P — Xóa bản ghi

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| P01 | Xóa khi đã chọn bản ghi | Hiển thị confirm dialog trước khi xóa |
| P02 | Click Xóa khi chưa chọn bản ghi | Thông báo chưa chọn bản ghi |
| P03 | Popup Lý do xóa *(QT component)* | Label: "Lý do", TextArea max 1000. Mặc định **không bắt buộc** (trừ khi SRS quy định bắt buộc) |

---

### Nhóm Q — File Upload

> **Quy tắc phân nhóm (BẮT BUỘC):** Kiểm thử chức năng Upload file được chia thành 3 phân nhóm chính theo thao tác người dùng và hiển thị:
> 1. **Kéo thả file vào vùng dropzone (Drag & Drop)**
> 2. **Click button 'Chọn file' (File Picker Dialog)**
> 3. **Hiển thị file sau khi tải lên & Thao tác file**
> 4. **Kiểm tra nội dung & bảo mật chuyên sâu (khi hệ thống đọc/parse nội dung file)**

#### 1. Kéo thả file vào vùng dropzone (Drag & Drop)

| # | Mục đích kiểm thử | Trường hợp kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|---|
| Q01 | Kiểm tra giá trị mặc định | Trạng thái ban đầu của vùng dropzone | Mặc định: Trống, hiển thị icon và text hướng dẫn kéo thả hoặc click chọn file |
| Q02 | Kiểm tra trường bắt buộc | Để trống tệp khi là trường bắt buộc | Hệ thống hiển thị thông báo lỗi bắt buộc nhập/tải tệp |
| Q03 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp đúng định dạng | Hệ thống cho phép và tải file lên thành công |
| Q04 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp sai định dạng | Hệ thống hiển thị thông báo: "File tải lên không đúng định dạng hoặc không đúng mẫu quy định. Vui lòng kiểm tra lại" |
| Q05 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả 1 tệp | Hệ thống cho phép và tải 1 file lên thành công |
| Q06 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả nhiều tệp *(nếu hỗ trợ multi-file)* | Hệ thống cho phép và tải nhiều file lên thành công |
| Q07 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên là tiếng Việt có dấu | Hệ thống cho phép và tải file lên thành công, hiển thị đúng font tiếng Việt |
| Q08 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên là ký tự số | Hệ thống cho phép và tải file lên thành công |
| Q09 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên là ký tự đặc biệt | Hệ thống cho phép và tải file lên thành công |
| Q10 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên < 255 ký tự | Hệ thống cho phép và tải file lên thành công |
| Q11 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên = 255 ký tự | Tải thành công và tên file được hiển thị dạng 'Tên file...' (cắt bớt / ellipsis) |
| Q12 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên > 255 ký tự | Tải thành công và tên file được hiển thị dạng 'Tên file...' (cắt bớt / ellipsis) |
| Q13 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có tên là thẻ html | Tải thành công và tên file được hiển thị dạng '<html>/...' (mã hóa an toàn HTML entities, không thực thi script) |
| Q14 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có dung lượng = 0 (file rỗng) | Hệ thống hiển thị thông báo: 'Không được tải file rỗng!' |
| Q15 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có dung lượng < dung lượng giới hạn | Hệ thống cho phép và tải file lên thành công |
| Q16 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả tệp có dung lượng > dung lượng giới hạn | Hệ thống hiển thị thông báo: "File tải lên vượt quá [dung lượng file tối đa]" |
| Q17 | Thực hiện kéo thả file vào vùng dropzone | Kéo thả file trùng tên cùng 1 phiên tải | Hệ thống không cho phép tải lên 2 file trùng tên (hoặc cảnh báo ghi đè/tự động đổi tên theo spec) |
| Q18 | Kéo thả file ngoài vùng dropzone | Thả file vào khu vực ngoài dropzone | Không thực hiện tải file lên, con trỏ chuột hiển thị biểu tượng không được phép thả |

#### 2. Click button 'Chọn file' (File Picker Dialog)

| # | Mục đích kiểm thử | Trường hợp kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|---|
| Q19 | Kiểm tra hiển thị button Chọn file | Hiển thị button trên giao diện | Button hiển thị đúng theo design/SRS (nhãn 'Chọn file', icon tải lên, vị trí, kích thước) |
| Q20 | Kiểm tra trạng thái button Chọn file | Trạng thái Enable / Disable | Trạng thái: Enable (chuyển Disable nếu đã đạt số lượng file tối đa cho phép tải lên) |
| Q21 | Kiểm tra khi onclick button Chọn file | Click chuột vào button Chọn file | Onclick hệ thống hiển thị hộp thoại/màn hình chức năng chọn file upload của hệ điều hành (File Dialog) |
| Q22 | Thực hiện tải file qua button | Upload tệp đúng định dạng | Hệ thống cho phép và tải file lên thành công |
| Q23 | Thực hiện tải file qua button | Upload tệp sai định dạng | Hệ thống hiển thị thông báo: "File tải lên không đúng định dạng hoặc không đúng mẫu quy định. Vui lòng kiểm tra lại" |
| Q24 | Thực hiện tải file qua button | Upload 1 tệp | Hệ thống cho phép và tải file lên thành công |
| Q25 | Thực hiện tải file qua button | Upload nhiều tệp *(nếu hỗ trợ multi-file)* | Hệ thống cho phép và tải nhiều file lên thành công |
| Q26 | Thực hiện tải file qua button | Upload tệp có tên là tiếng Việt có dấu | Hệ thống cho phép và tải file lên thành công, hiển thị chuẩn Unicode |
| Q27 | Thực hiện tải file qua button | Upload tệp có tên là ký tự số | Hệ thống cho phép và tải file lên thành công |
| Q28 | Thực hiện tải file qua button | Upload tệp có tên là ký tự đặc biệt | Hệ thống cho phép và tải file lên thành công |
| Q29 | Thực hiện tải file qua button | Upload tệp có tên < 255 ký tự | Hệ thống cho phép và tải file lên thành công |
| Q30 | Thực hiện tải file qua button | Upload tệp có tên = 255 ký tự | Tải thành công và tên file được hiển thị dạng 'Tên file...' (cắt bớt / ellipsis) |
| Q31 | Thực hiện tải file qua button | Upload tệp có tên > 255 ký tự | Tải thành công và tên file được hiển thị dạng 'Tên file...' (cắt bớt / ellipsis) |
| Q32 | Thực hiện tải file qua button | Upload tệp có tên là thẻ html | Tải thành công và tên file được hiển thị an toàn dạng '<html>/...' (mã hóa an toàn) |
| Q33 | Thực hiện tải file qua button | Upload tệp có dung lượng = 0 (file rỗng) | Hệ thống hiển thị thông báo: 'Không được tải file rỗng!' |
| Q34 | Thực hiện tải file qua button | Upload tệp có dung lượng < dung lượng giới hạn | Hệ thống cho phép và tải file lên thành công |
| Q35 | Thực hiện tải file qua button | Upload tệp có dung lượng > dung lượng giới hạn | Hệ thống hiển thị thông báo: "File tải lên vượt quá [dung lượng file tối đa]" |
| Q36 | Thực hiện tải file qua button | Upload file trùng tên cùng 1 phiên tải | Hệ thống không cho phép tải lên 2 file trùng tên |
| Q37 | Hủy chọn file trên File Dialog | Bấm nút Cancel hoặc đóng hộp thoại chọn file | Đóng File Dialog, giữ nguyên trạng thái cũ, không làm mất các file đã tải lên trước đó |

#### 3. Hiển thị file sau khi tải lên & Thao tác file

| # | Mục đích kiểm thử | Trường hợp kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|---|
| Q38 | Kiểm tra hiển thị file khi tải lên thành công | Hiển thị thông tin file sau khi upload | Hệ thống hiển thị file tải lên bao gồm icon loại file (excel, pdf, docx, zip...), tên file, kích thước dung lượng file (KB/MB) |
| Q39 | Kiểm tra button icon Xóa file | Trạng thái hiển thị icon Xóa | Trạng thái: Active (hiển thị nút/icon xóa dạng thùng rác hoặc dấu X cạnh tên file) |
| Q40 | Kiểm tra thao tác xóa file vừa tải lên | Click button icon Xóa | Xóa file tương ứng khỏi danh sách tải lên; cập nhật lại trạng thái vùng upload cho phép tải file mới |
| Q41 | Kiểm tra tải xuống / xem trước file *(nếu có)* | Click vào tên file hoặc icon xem trước | Hệ thống cho phép tải về đúng file vừa tải lên hoặc mở popup xem trước nội dung file |

#### 4. Kiểm tra nội dung & bảo mật chuyên sâu *(khi hệ thống đọc/parse nội dung file)*

| # | Mục đích kiểm thử | Trường hợp kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|---|
| Q42 | Upload file có mật khẩu bảo vệ | File ZIP/XLSX/PDF có password bảo vệ | Thông báo không thể đọc file có mật khẩu; từ chối xử lý an toàn |
| Q43 | Upload file sai cú pháp dữ liệu (malformed) | File XML/JSON/Excel hỏng cấu trúc | Thông báo cú pháp file không hợp lệ; không gây crash hoặc treo hệ thống |
| Q44 | Upload file có encoding không phải UTF-8 | File text/CSV có encoding lạ | Thông báo lỗi encoding hoặc tự động chuyển đổi; không hiển thị ký tự rác/vỡ font |
| Q45 | Upload file có MIME type giả mạo | Đổi extension file (vd: đổi .exe thành .xlsx hoặc ngược lại) | Hệ thống kiểm tra magic bytes / MIME type thực tế và từ chối tải lên; không chỉ dựa vào extension |
| Q46 | Upload file thiếu sheet/cột bắt buộc | File không khớp cấu trúc schema theo spec | Thông báo cụ thể tên sheet/cột nào bị thiếu; liệt kê yêu cầu cấu trúc file chuẩn |

> **Lưu ý áp dụng Q42–Q46:** Chỉ áp dụng khi hệ thống đọc/xử lý nội dung file (không chỉ lưu trữ). Q42–Q46 là các case **nghiệp vụ chuyên sâu** — xác định với BA/PO xem hệ thống có parse nội dung không trước khi sinh TC.

---

### Nhóm R — Import *(Nếu màn hình có chức năng Import)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| R01 | Import file hợp lệ, ≤ max bản ghi | Import thành công, lưu đúng vào DB |
| R02 | Có ít nhất 1 bản ghi lỗi | Không import; hiển thị thông báo lỗi từng dòng |
| R03 | Có 2 bản ghi trùng nhau trong file | Không import; thông báo lỗi trùng |
| R04 | File có nhiều dòng trống | Import thành công, bỏ qua dòng trống |
| R05 | File sai định dạng | Thông báo sai định dạng |
| R06 | Chưa chọn file → click Import | Thông báo chưa chọn file |
| R07 | Số bản ghi > max cho phép | Thông báo vượt quá số lượng |
| R08 | Cấu trúc cột file không khớp màn hình | Thông báo cấu trúc file không đúng |
| R09 | File Import rỗng | Thông báo file rỗng |
| R10 | Trim space dữ liệu cột trước khi insert | Data lưu đã được trim |

---

### Nhóm S — Phân quyền chức năng *(Nếu chức năng có kiểm soát quyền truy cập)*

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| S01 | Kiểm tra người dùng **được** phân quyền chức năng | NSD được phép truy cập chức năng `<tên chức năng>` và thực hiện được thao tác `<tên chức năng>` |
| S02 | Kiểm tra người dùng **không được** phân quyền chức năng | NSD không được phép truy cập chức năng `<tên chức năng>` và không hiển thị button `<tên chức năng>` |

---

### Nhóm T — Tra cứu / Tìm kiếm kết hợp *(Áp dụng khi màn hình có khu vực tìm kiếm từ 2 trường trở lên)*

> Mục đích: đảm bảo bộ lọc hoạt động đúng khi tìm theo **từng trường riêng lẻ** và **kết hợp nhiều trường** (AND logic leo thang). Mỗi trường tìm kiếm phải được kiểm tra độc lập trước khi kiểm tra tổ hợp.

**Quy tắc sinh TC (bắt buộc):**

1. **Riêng lẻ (T02–T0N):** Mỗi trường tìm kiếm → **1 TC độc lập** (nhập đúng 1 trường, bỏ trống các trường còn lại).
2. **Kết hợp leo thang (TK01–TKN):** Tổ hợp 2 trường → 3 trường → ... → tất cả trường.
   - Với **N trường** → sinh tối thiểu: **N cases riêng lẻ + (N−1) cases tổ hợp leo thang + 1 case tổ hợp đủ tất cả trường**.
   - Chọn tổ hợp đại diện, không cần sinh đủ mọi hoán vị khi số trường lớn (≥ 5).
3. **Không có kết quả (TX01):** 1 TC tìm kiếm với điều kiện không khớp bản ghi nào.
4. **Reset điều kiện (TX02):** 1 TC xóa/reset toàn bộ điều kiện → kết quả về mặc định.

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| T01 | Tìm kiếm khi không nhập điều kiện nào (bỏ trống toàn bộ) | Hiển thị toàn bộ bản ghi theo phân trang mặc định |
| T02 | Tìm kiếm theo `<trường 1>` riêng lẻ — có kết quả | Danh sách chỉ chứa bản ghi khớp `<trường 1>` |
| T03 | Tìm kiếm theo `<trường 2>` riêng lẻ — có kết quả | Danh sách chỉ chứa bản ghi khớp `<trường 2>` |
| T0N | *(Lặp lại cho mỗi trường tìm kiếm)* Tìm kiếm theo `<trường N>` riêng lẻ | Danh sách chỉ chứa bản ghi khớp `<trường N>` |
| TK01 | Kết hợp 2 trường: `<trường 1>` + `<trường 2>` | Bản ghi thỏa đồng thời cả 2 điều kiện (AND) |
| TK02 | Kết hợp 3 trường: `<trường 1>` + `<trường 2>` + `<trường 3>` | Bản ghi thỏa đồng thời cả 3 điều kiện (AND) |
| TK0N | *(Leo thang đến N−1 trường)* Kết hợp N−1 trường | Bản ghi thỏa đồng thời N−1 điều kiện |
| TKN | Kết hợp **tất cả** trường tìm kiếm | Bản ghi thỏa đồng thời toàn bộ điều kiện |
| TX01 | Tìm kiếm với điều kiện không khớp bản ghi nào | Hiển thị "Không có dữ liệu" hoặc danh sách rỗng |
| TX02 | Xóa / Reset toàn bộ điều kiện tìm kiếm | Quay về kết quả mặc định (toàn bộ bản ghi) |

**Ví dụ minh họa — màn hình tra cứu có 4 trường: Mã, Tên, Trạng thái, Ngày tạo:**

| TC | Mã | Tên | Trạng thái | Ngày tạo | Kỳ vọng |
|---|---|---|---|---|---|
| T01 | *(trống)* | *(trống)* | *(trống)* | *(trống)* | Toàn bộ bản ghi |
| T02 | `"KH-001"` | *(trống)* | *(trống)* | *(trống)* | Lọc đúng theo Mã |
| T03 | *(trống)* | `"Nguyễn"` | *(trống)* | *(trống)* | Lọc đúng theo Tên |
| T04 | *(trống)* | *(trống)* | `"Hoạt động"` | *(trống)* | Lọc đúng theo Trạng thái |
| T05 | *(trống)* | *(trống)* | *(trống)* | `01/01–31/01/2025` | Lọc đúng theo Ngày tạo |
| TK01 | `"KH"` | `"Nguyễn"` | *(trống)* | *(trống)* | AND: Mã + Tên |
| TK02 | `"KH"` | `"Nguyễn"` | `"Hoạt động"` | *(trống)* | AND: Mã + Tên + Trạng thái |
| TKN | `"KH"` | `"Nguyễn"` | `"Hoạt động"` | `01/01–31/01/2025` | AND: cả 4 trường (TKN = case tất cả trường) |
| TX01 | `"KHONG_TON_TAI"` | *(trống)* | *(trống)* | *(trống)* | "Không có dữ liệu" |
| TX02 | *(nhấn Reset)* | | | | Toàn bộ bản ghi hiển thị lại |

**Lưu ý:**
- TC riêng lẻ phải dùng **test data có kết quả thực tế** trong DB — không dùng placeholder.
- Khi trường tìm kiếm là partial match (LIKE) → dùng chuỗi con, kiểm tra kết quả chứa chuỗi con đó.
- Khi trường là exact match → dùng giá trị chính xác.
- Tổ hợp nên chọn dữ liệu sao cho **kết quả hẹp dần** qua từng tổ hợp để dễ phân biệt đúng/sai.
- **Khoảng ngày tối đa (Date Range Constraint) *(nếu có)*:** Khi bộ lọc có cặp Từ ngày – Đến ngày và SRS giới hạn khoảng ngày tối đa (VD: ≤31 ngày, ≤3 tháng), phải sinh thêm 3 TC riêng:
  - TK_DATERANGE_01: Chọn khoảng ngày = giới hạn tối đa → tìm kiếm thành công
  - TK_DATERANGE_02: Chọn khoảng ngày = giới hạn tối đa − 1 ngày → thành công
  - TK_DATERANGE_03: Chọn khoảng ngày > giới hạn tối đa → thông báo lỗi khoảng ngày vượt quá giới hạn

---

### Nhóm U — Grid kết quả chức năng tách *(Nếu có grid kết quả với trường chỉnh sửa và cột thao tác)*

> Áp dụng cho màn hình có grid kết quả bao gồm: trường dữ liệu (hiển thị, chỉnh sửa, tìm kiếm theo cột, căn lề) và cột thao tác (action button/icon).
> **Quy tắc tổ chức:** Mỗi trường dữ liệu là 1 subsection con riêng (U01–U04). Mỗi thao tác là 1 subsection con riêng (U05–U07). **NGHIÊM CẤM** gộp chung nhiều trường hoặc nhiều thao tác vào 1 subsection.

#### Template — Subsection cho mỗi trường dữ liệu

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| U01 | Kiểm tra hiển thị | Trường hiển thị đúng: header, dữ liệu, format, vị trí cột theo design |
| U02 | Kiểm tra chỉnh sửa | Cho phép / không cho phép chỉnh sửa trực tiếp trên grid theo spec; lưu đúng sau khi chỉnh sửa |
| U03 | Kiểm tra thao tác search trên column | Nhập từ khóa vào ô filter column → lọc đúng kết quả; icon "x" xóa filter → hiển thị lại toàn bộ |
| U04 | Kiểm tra căn lề | Cột text căn trái, số căn phải, date/STT/trạng thái căn giữa theo tiêu chuẩn *(QT component)* |

#### Template — Subsection cho mỗi thao tác (action button/icon)

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| U05 | Kiểm tra hiển thị | Button/icon hiển thị đúng: icon, label, tooltip, màu sắc theo design |
| U06 | Kiểm tra trạng thái | Enabled/disabled đúng điều kiện (trạng thái bản ghi, quyền hạn người dùng) |
| U07 | Kiểm tra khi onclick | Click → thực hiện đúng action theo spec; có loading/spinner nếu gọi API; button bị disable khi đang xử lý |

**Ví dụ cấu trúc — màn hình có cột "Tên đơn vị", "Mã số thuế" và thao tác "Xem chi tiết", "Xóa":**

```
subsection("Cột Tên đơn vị")        → U01, U02, U03, U04
subsection("Cột Mã số thuế")        → U01, U02, U03, U04
subsection("Thao tác Xem chi tiết") → U05, U06, U07
subsection("Thao tác Xóa")          → U05, U06, U07
```

**Lưu ý:**
- U02 **BẮT BUỘC** cho mọi cột, kể cả cột readonly — không được bỏ qua. Cột readonly: U02 expected result = "không mở edit mode, không có input field, dữ liệu readonly"; không ghi `N/A` mà viết TC thực.
- Cột không có filter search → U03 là `N/A` + ghi lý do.
- Mỗi thao tác phải có đủ cả 3 cases U05–U07, kể cả thao tác đơn giản (VD: nút "Xem").

---

### Nhóm V — Màn hình Chỉnh sửa (Edit Form) *(Luôn áp dụng khi có chức năng Chỉnh sửa)*

> ⚠️ **Quy tắc phân loại trường và kế thừa kịch bản:**
> 1. **Bắt buộc đọc spec/SRS:** Tùy từng màn hình sẽ có nghiệp vụ quy định cụ thể trường nào cho phép sửa hoặc không cho phép sửa (khóa/readonly) => AI PHẢI đọc spec để phân loại chính xác danh mục trường được sửa và trường bị khóa.
> 2. **Số lượng test case cho các trường cho phép sửa:** Đối với các trường cho phép sửa, nhiều nhất PHẢI có số lượng test case tương đương màn hình Tạo mới (đủ D, E, H, J, K...). Không được cắt xén.
> 3. **5 case đặc thù của Edit (BẮT BUỘC):**

| # | Mục đích kiểm thử | Kết quả mong muốn tóm tắt |
|---|---|---|
| V01 | Nạp dữ liệu cũ chính xác | Mở form chỉnh sửa, kiểm tra toàn bộ trường hiển thị đúng 100% dữ liệu đã lưu của bản ghi |
| V02 | Khóa trường ID/Mã không cho sửa | Các trường mã/khóa/hệ thống sinh ở trạng thái `disabled` hoặc `readonly`, con trỏ không thể focus nhập hay paste |
| V03 | Chỉnh sửa 1 hoặc nhiều trường | Sửa đổi dữ liệu hợp lệ và nhấn Lưu → Lưu thành công, dữ liệu mới được cập nhật trên database và danh sách |
| V04 | Giữ nguyên không đổi và Lưu | Mở form, không thay đổi bất kỳ trường nào rồi nhấn Lưu → Lưu thành công, không báo lỗi trùng lặp hay validation error, dữ liệu giữ nguyên |
| V05 | Hủy bỏ khôi phục giá trị ban đầu | Mở form, sửa một số trường nhưng nhấn [Hủy] hoặc nút đóng popup → Form đóng lại, không lưu các thay đổi dở dang, dữ liệu bản ghi giữ nguyên giá trị ban đầu |

---

### Nhóm W — Các Component Giao diện Phức tạp *(Nếu có trên màn hình)*

#### W1 — Checkbox Matrix Pattern (Ma trận ô đánh dấu Sự kiện × Kênh)
- **W1_01 — Trạng thái tương tác:** Toàn bộ ô đánh dấu ở trạng thái enable, cho phép tương tác độc lập giữa các dòng và cột.
- **W1_02 — Bật/tắt bằng phím Space:** Khi ô có focus, nhấn phím Space đảo trạng thái tích/bỏ tích, có viền focus rõ ràng.
- **W1_03 — Phím Tab qua ma trận:** Focus di chuyển lần lượt theo từng hàng, từ trái sang phải rồi xuống hàng dưới.
- **W1_04 — Tính bền vững sau lưu:** Sau khi Lưu và mở lại, ma trận nạp lại đúng trạng thái đã lưu, không bị reset về mặc định.

#### W2 — Multi-select Tag Input Email (Ô chọn nhiều kèm gõ tự do)
- **W2_01 — Hiển thị & Placeholder:** Hiển thị ô chọn nhiều, placeholder rõ ràng (VD: *"Chọn user hoặc gõ email riêng..."*).
- **W2_02 — Chọn từ danh mục:** Chọn người dùng từ dropdown tạo thẻ tag hiển thị kèm icon 'x' để xóa.
- **W2_03 — Nhập tự do hợp lệ:** Cho phép gõ địa chỉ email tự do hợp lệ và nhấn Enter để tạo thẻ tag.
- **W2_04 — Validate định dạng:** Gõ chuỗi sai định dạng email → Hệ thống từ chối và cảnh báo lỗi.
- **W2_05 — Chống trùng lặp:** Gõ email trùng thẻ tag đã có → Không tạo thẻ trùng lặp hoặc cảnh báo đã tồn tại.
- **W2_06 — Bảo mật XSS/SQL Injection:** Gõ mã XSS (`<script>`) hoặc SQLi (`' OR '1'='1`) → Bị từ chối vì không phải email hợp lệ.
- **W2_07 — Copy/paste nhiều email:** Paste chuỗi chứa nhiều email phân tách bởi dấu phẩy/chấm phẩy → Tự động tách thành các thẻ tag riêng biệt.

#### W3 — Status Badge / Tag (Thẻ trạng thái bản ghi)
- **W3_01 — Vị trí & Màu sắc:** Hiển thị đúng vị trí (góc trên popup hoặc cột bảng), màu sắc và nhãn tương ứng từng trạng thái (Xanh lá: Hoạt động, Đỏ/Xám: Ngừng hoạt động, Vàng: Chờ duyệt/Đang chạy).
- **W3_02 — Tính chất chỉ đọc:** Thẻ trạng thái chỉ mang tính chất hiển thị (display-only), không cho phép click trực tiếp để đổi trạng thái.

#### W4 — Dynamic Form Visibility (Ẩn/Hiện trường theo điều kiện chọn)
- **W4_01 — Chuyển đổi Trigger:** Khi đổi giá trị trường điều khiển (VD: Trigger EVENT vs SCHEDULER), các trường phụ thuộc tương ứng tự động ẩn/hiện và cập nhật tính bắt buộc (`*`) tại đúng vị trí form.
- **W4_02 — Chuyển đổi ngược:** Khi đổi ngược lại giá trị ban đầu, các trường phụ thuộc cũ được phục hồi trạng thái và giá trị mặc định.

---

### Quy tắc bổ sung từ QT Component *(Tham chiếu)*

#### Xuất Excel *(QT component — 7 test case bắt buộc)*
1. **Xuất trang hiện tại:** Chỉ xuất các dòng dữ liệu hiển thị trên trang hiện tại.
2. **Xuất theo bộ lọc:** Xuất toàn bộ dữ liệu khớp với bộ lọc tìm kiếm (không giới hạn trang).
3. **Format tên file:** `<tên danh sách không dấu>_ddmmyyyyhhmmss.xlsx` (VD: `Danh_sach_Job_25102026170930.xlsx`).
4. **Chia file zip khi dữ liệu > 1.000.000 bản ghi:** Hệ thống xuất file `.zip` chứa nhiều file `.xlsx`, mỗi file tối đa 1.000.000 dòng.
5. **Dữ liệu rỗng:** Khi bộ lọc không có bản ghi nào, xuất file Excel chỉ có hàng tiêu đề (Header).
6. **Lỗi ngoại lệ API:** Hiển thị thông báo "Lỗi hệ thống" hoặc "Yêu cầu này mất quá nhiều thời gian để phản hồi" (timeout).
7. **Hết token phiên làm việc:** Điều hướng người dùng về trang đăng nhập Login.

#### Màn hình Xem chi tiết *(QT component)*
- Hiển thị dạng **popup** (trừ khi SRS quy định dạng Page)
- **Toàn bộ trường dữ liệu ở chế độ chỉ đọc (Readonly)**, hiển thị đúng 100% dữ liệu bản ghi gốc
- **Status Badge:** Hiển thị đúng màu sắc và nhãn trạng thái của bản ghi
- **Bắt buộc có Bảng Lịch sử thay đổi** (8 cột: STT, Thời gian, Người CN, Hành động, GT cũ, GT mới, IP, Mô tả)
- Bảng lịch sử mặc định **collapse** (thu gọn), click mới expand
- Bảng lịch sử: **scroll** (không phân trang), chiều cao tối đa 250px, sắp xếp mới nhất trên cùng
- Cột Mô tả > 2 dòng → hiển thị "..." + nút "Xem tiếp"; file đính kèm hiển thị dạng link tải về

#### Popup Lý do (Chỉnh sửa / Xóa / Vô hiệu hóa / Phê duyệt...) *(QT component)*
- Label: "Lý do"
- Component: TextArea, max 1000 ký tự
- Mặc định **không bắt buộc** (trừ khi SRS quy định khác)

#### Khu vực tìm kiếm & Câu lệnh SQL *(QT component)*
- Droplist trên khu vực tìm kiếm: **tùy SRS** có thể là single-select hoặc multi-select
- **BẮT BUỘC câu lệnh SQL đối soát Database:** Mọi trường hợp tìm kiếm (1 điều kiện, nhiều điều kiện, không có dữ liệu) phải đính kèm câu lệnh SQL tương ứng (`SELECT ... FROM ... WHERE ...`) để đối chiếu tầng DB.

---

## Verification Checklist — Danh sách đếm TC bắt buộc sau khi sinh

> **Mục đích:** Agent PHẢI dùng danh sách này để **đếm từng case** sau khi sinh TC xong mỗi module. Nếu thiếu case nào → bổ sung ngay trước khi chuyển sang Review Gate.
>
> **Cách dùng:** Với mỗi field type trong Field Inventory, tick từng case trong danh sách bên dưới. Case nào không áp dụng → đánh `N/A + lý do`.

### Nhóm D — TEXT: 38 cases bắt buộc (mỗi field)

**4 TC tĩnh (dùng `tc()` riêng):**
- [ ] D01 — Giá trị mặc định
- [ ] D02 — Hiển thị UI (kích thước, căn lề, viền)
- [ ] D03 — Placeholder
- [ ] D04 — Trường bắt buộc

**17 tc_item trong tc_group("Kiểm tra khi nhập giá trị"):**
*tc_sub("Kiểm tra nhập maxlength") (3 items BVA — BẮT BUỘC group, không để tc() riêng lẻ):*
- [ ] D05 — Nhập (Max−1) ký tự
- [ ] D06 — Nhập đúng Max ký tự
- [ ] D07 — Nhập (Max+1) ký tự

*tc_sub("Kiểm tra khi nhập khoảng trắng") (4 items):*
- [ ] D08 — Nhập toàn khoảng trắng `"   "`
- [ ] D09 — Nhập khoảng trắng đầu cuối `" ABC "`
- [ ] D10 — Nhập khoảng trắng giữa `"A B"`
- [ ] D11 — Nhập NHIỀU khoảng trắng giữa `"A   B"` ⚠️ *thường bị thiếu*

*Các tc_sub ký tự và security (10 items):*
- [ ] D12 — Nhập ký tự IN HOA `"NGUYEN VAN A"` ⚠️ *thường bị thiếu*
- [ ] D13 — Nhập ký tự in thường `"nguyen van a"` ⚠️ *thường bị thiếu*
- [ ] D14 — Nhập ký tự số `"1234567890"` ⚠️ *thường bị thiếu*
- [ ] D15 — Nhập ký tự đặc biệt `"!@#$%^&*()_+"`
- [ ] D16 — Nhập ký tự hỗn hợp `"abc123!@#"` ⚠️ *thường bị thiếu*
- [ ] D17 — Nhập tiếng Việt có dấu `"Nguyễn Văn A"`
- [ ] D18 — Nhập XSS/HTML `<script>alert('xss')</script>`
- [ ] D19 — Nhập SQL injection `' OR '1'='1`
- [ ] D20 — Nhập URL `https://www.google.com` ⚠️ *thường bị thiếu*
- [ ] D21 — Nhập CSRF payload `<img src=x onerror=alert(1)>` ⚠️ *thường bị thiếu*

**17 tc_item trong tc_group("Kiểm tra khi copy/paste giá trị"):**
*tc_sub("Kiểm tra copy/paste maxlength") (3 items BVA):*
- [ ] D05cp — Paste (Max−1) ký tự
- [ ] D06cp — Paste đúng Max ký tự
- [ ] D07cp — Paste (Max+1) → cắt bớt (truncate)

*tc_sub("Kiểm tra copy/paste khoảng trắng") (4 items):*
- [ ] D08cp — Paste toàn khoảng trắng
- [ ] D09cp — Paste khoảng trắng đầu cuối
- [ ] D10cp — Paste khoảng trắng giữa
- [ ] D11cp — Paste nhiều khoảng trắng giữa

*Các tc_sub copy/paste ký tự và security (10 items):*
- [ ] D12cp — Paste ký tự IN HOA
- [ ] D13cp — Paste ký tự in thường
- [ ] D14cp — Paste ký tự số
- [ ] D15cp — Paste ký tự đặc biệt
- [ ] D16cp — Paste ký tự hỗn hợp
- [ ] D17cp — Paste tiếng Việt có dấu
- [ ] D18cp — Paste XSS/HTML
- [ ] D19cp — Paste SQL injection
- [ ] D20cp — Paste URL
- [ ] D21cp — Paste CSRF payload

> ⚠️ **LƯU Ý QUAN TRỌNG: Textbox KHÔNG CÓ case "Kiểm tra nhập tìm kiếm".** (Chỉ kiểm tra đủ 38 cases D01–D21 + D05cp–D21cp).
> D22–D28 dưới đây CHỈ áp dụng khi Dropdown/Combobox có tích hợp ô tìm kiếm option bên trong popup:
- [ ] D22 — Tìm kiếm không phân biệt hoa/thường *(Searchable Dropdown/Combobox popup)*
- [ ] D23 — Tìm kiếm không phân biệt dấu/không dấu *(Searchable Dropdown/Combobox popup)*
- [ ] D24 — Tìm kiếm tương đối (contains) — tc_group sub *(Searchable Dropdown/Combobox popup)*
- [ ] D25 — Tìm kiếm tuyệt đối (exact) — tc_group sub *(Searchable Dropdown/Combobox popup)*
- [ ] D26 — Tìm kiếm không có kết quả — tc_group sub *(Searchable Dropdown/Combobox popup)*
- [ ] D27 — Nhập ≤ max ký tự — tc_group sub *(Searchable Dropdown/Combobox popup)*
- [ ] D28 — Nhập > max ký tự — tc_group sub *(Searchable Dropdown/Combobox popup)*

### Nhóm A — 6 TC bắt buộc (mỗi module)

- [ ] A01 — Màn hình mặc định
- [ ] A02 — Tổng thể giao diện (bố cục, font, dấu *, chính tả)
- [ ] A03 — Tab order tiến ⚠️ *M2/M3 thường bị thiếu*
- [ ] A04 — Tab order lùi (Shift+Tab) ⚠️ *M2/M3 thường bị thiếu*
- [ ] A05 — Phím Enter ⚠️ *thường bị thiếu*
- [ ] A06 — Responsive (Ctrl+−, Ctrl+=)

### Nhóm C — Grid: 7+ TC bắt buộc

- [ ] C01 — Format Grid (header/value alignment)
- [ ] C02 — STT tăng dần liên tục qua trang ⚠️ *thường bị thiếu*
- [ ] C03 — Ẩn paging khi ≤10 bản ghi ⚠️ *thường bị thiếu*
- [ ] C05 — Style paging: format chuỗi "Hiển thị 1–20 trong N kết quả" ⚠️ *thường bị thiếu*
- [ ] C07 — Header/footer không đổi khi chuyển trang ⚠️ *thường bị thiếu*
- [ ] C09 — Thêm/Sửa/Xóa từ trang N → quay trang 1 ⚠️ *thường bị thiếu*
- [ ] C10 — Xóa bản ghi cuối trang cuối → quay trang N−1 ⚠️ *thường bị thiếu*
- [ ] tc_group phân trang (5 sub)
- [ ] tc_group combobox phân trang (6 sub)
- [ ] tc_group nhập tìm kiếm số trang (4 sub)
- [ ] C11 — Skeleton loading (QT)
- [ ] C12 — Grid trống "Không có dữ liệu" (QT)
- [ ] C13 — Icon mở rộng full screen (QT)
- [ ] C14 — Filter từng cột (QT)
- [ ] C15 — Cột Ngày hover hiển thị đầy đủ (QT)
- [ ] C16 — Cột Người hover hiển thị họ tên (QT)

### Nhóm H — Dropdown: 15+ TC bắt buộc (mỗi field)

- [ ] H01 — Hiển thị
- [ ] H02 — Giá trị mặc định ⚠️ *thường bị thiếu cho field 2+*
- [ ] H03 — Placeholder ⚠️ *thường bị thiếu cho field 2+*
- [ ] H04 — Trường bắt buộc (hoặc N/A nếu filter)
- [ ] H05 — Options đúng đủ
- [ ] H06 — Sử dụng bàn phím ⚠️ *thường bị thiếu* 
- [ ] tc_group scroll 3 sub (H07–H09)
- [ ] tc_group chọn giá trị 3 sub (H10–H12)
- [ ] tc_group API states 3 sub (H13–H16)

⚠️ **LƯU Ý H06**
  > **H06: Sử dụng bàn phím**: 
  Các bước thực hiện như sau: 
  1. Tại màn hình *theo thông tin trong SRS*, thực hiện nhấn phím tab/ shift tab vào dropdown list
  2. Thực hiện nhấn phím Enter
  3. Thực hiện di chuyển các phím up/ down
  4. Thực hiện nhấn phím enter khi đang focus vào 1 giá trị trong dropdown list
  5. Thực hiện nhấn tab/ shift tab

  Kết quả mong muốn:
  1. Thực hiện nhấn phím tab/ shift tab vào dropdown list
  2. Thực hiện nhấn phím Enter → danh sách lựa chọn hiển thị 
  3. Thực hiện di chuyển các phím up/ down → con trỏ di chuyển theo danh sách lựa chọn
  4. Thực hiện nhấn phím enter khi đang focus vào 1 giá trị trong dropdown list → giá trị được chọn và hiển thị 
  5. Thực hiện nhấn tab/ shift tab → con trỏ di chuyển đến field tiếp theo


### Nhóm J — Multi-select: 17+ TC bắt buộc (mỗi field)

- [ ] J01 — Hiển thị
- [ ] J02 — Giá trị mặc định ⚠️ *thường bị thiếu*
- [ ] J03 — Placeholder ⚠️ *thường bị thiếu*
- [ ] J04 — Required (hoặc N/A nếu filter)
- [ ] J05 — Thứ tự sắp xếp ⚠️ *thường bị thiếu*
- [ ] J06 — Căn lề ⚠️ *thường bị thiếu*
- [ ] tc_group chọn giá trị 4 sub (J07–J10)
- [ ] tc_group scroll 3 sub (J11–J13)
- [ ] J14 — Focus bàn phím ⚠️ *thường bị thiếu*
- [ ] tc_group API states 3 sub (H13–H16 pattern) ⚠️ *thường bị thiếu cho field 2+*

### Nhóm K — Date: 8+ TC bắt buộc (mỗi field)

- [ ] K01 — Focus Calendar trống ⚠️ *thường bị thiếu*
- [ ] K02 — Focus Calendar có giá trị ⚠️ *thường bị thiếu*
- [ ] K03 — Chọn ngày
- [ ] K05 — Required
- [ ] K06 — Sai định dạng
- [ ] K07 — Ngày không tồn tại (31/02)
- [ ] K08 — Ngày biên (29/02 năm nhuận, cuối tháng) ⚠️ *thường bị thiếu*
- [ ] K09–K11 — Ngày tương lai / hôm nay / quá khứ (tùy spec)
- [ ] K12–K14 — Từ ngày > Đến ngày / = / < (RangePicker)
- [ ] K15 — Nhập tay hợp lệ (QT)
- [ ] K16 — Nhập ký tự không hợp lệ (QT)
- [ ] K17 — Ngày < 01/01/1900 (QT) ⚠️ *thường bị thiếu*

### Nhóm E — NUMBER: 42 cases bắt buộc (mỗi field)

**4 TC tĩnh (dùng `tc()` riêng):**
- [ ] E01 — Giá trị mặc định
- [ ] E02 — Hiển thị UI (kích thước, căn lề, viền)
- [ ] E03 — Placeholder
- [ ] E04 — Trường bắt buộc

**19 tc_item trong tc_group("Kiểm tra khi nhập giá trị"):**
*tc_sub("Kiểm tra nhập maxlength") (3 items BVA — BẮT BUỘC group, không để tc() riêng lẻ):*
- [ ] E05 — Nhập (Max−1) ký tự
- [ ] E06 — Nhập đúng Max ký tự
- [ ] E07 — Nhập (Max+1) ký tự

*Các tc_sub khoảng trắng, ký tự, security và số đặc thù (16 items):*
- [ ] E08 — Nhập toàn khoảng trắng `"   "` ⚠️ *thường bị thiếu*
- [ ] E09 — Nhập khoảng trắng đầu cuối `" 12 "`
- [ ] E10 — Nhập khoảng trắng giữa `"1 2"`
- [ ] E11 — Nhập nhiều khoảng trắng giữa `"1   2"` ⚠️ *thường bị thiếu*
- [ ] E12 — Nhập ký tự chữ/không phải số `"ABc123"` ⚠️ *thường bị thiếu*
- [ ] E13 — Nhập ký tự số `"1234567890"`
- [ ] E14 — Nhập ký tự đặc biệt `"!@#$%^&*()_+"`
- [ ] E15 — Nhập ký tự hỗn hợp `"abc123!@#"` ⚠️ *thường bị thiếu*
- [ ] E16 — Nhập HTML/XSS `<script>alert('xss')</script>`
- [ ] E17 — Nhập SQL injection `' OR '1'='1`
- [ ] E18 — Nhập URL `https://www.google.com` ⚠️ *thường bị thiếu*
- [ ] E19 — Nhập CSRF payload `<img src=x onerror=alert(1)>`
- [ ] E20 — Nhập số thập phân *(tùy spec)*
- [ ] E21 — Nhập số âm *(tùy spec)*
- [ ] E22 — Nhập số thập phân vượt quy định
- [ ] E23 — Nhập số có chữ số 0 đầu *(tùy spec)*

**19 tc_item trong tc_group("Kiểm tra khi copy/paste giá trị"):**
- [ ] E05cp — Paste (Max−1) ký tự
- [ ] E06cp — Paste đúng Max ký tự
- [ ] E07cp — Paste (Max+1) → cắt bớt (truncate)
- [ ] E08cp — Paste toàn khoảng trắng
- [ ] E09cp — Paste khoảng trắng đầu cuối
- [ ] E10cp — Paste khoảng trắng giữa
- [ ] E11cp — Paste nhiều khoảng trắng giữa
- [ ] E12cp — Paste ký tự chữ/không phải số
- [ ] E13cp — Paste ký tự số
- [ ] E14cp — Paste ký tự đặc biệt
- [ ] E15cp — Paste ký tự hỗn hợp
- [ ] E16cp — Paste HTML/XSS
- [ ] E17cp — Paste SQL injection
- [ ] E18cp — Paste URL
- [ ] E19cp — Paste CSRF payload
- [ ] E20cp — Paste số thập phân *(tùy spec)*
- [ ] E21cp — Paste số âm *(tùy spec)*
- [ ] E22cp — Paste số thập phân vượt quy định
- [ ] E23cp — Paste số có chữ số 0 đầu *(tùy spec)*

### Nhóm G — TEXTAREA: 41 cases bắt buộc (mỗi field)

> TEXTAREA áp dụng đầy đủ **Nhóm D (38 cases)** + thêm **3 cases đặc thù G**. Tổng = 41.

**Nhóm D đủ 38 cases (tham chiếu Verification Checklist Nhóm D ở trên):**
- [ ] D01–D04 — 4 TC tĩnh
- [ ] D05–D21 — 17 tc_item trong tc_group nhập keyboard (bắt đầu bằng `tc_sub("Kiểm tra nhập maxlength")` 3 items)
- [ ] D05cp–D21cp — 17 tc_item trong tc_group copy-paste (bắt đầu bằng `tc_sub("Kiểm tra copy/paste maxlength")` 3 items)

**3 TC đặc thù TEXTAREA (dùng `tc()` riêng, thêm ngoài Nhóm D):**
- [ ] G07 — Nhập nhiều dòng (Enter xuống dòng) ⚠️ *thường bị thiếu*
- [ ] G11 — Bộ đếm ký tự realtime "đã dùng/tối đa" *(QT component)* ⚠️ *thường bị thiếu*
- [ ] G12 — Auto resize chiều cao theo nội dung *(QT component)* ⚠️ *thường bị thiếu*

> Nếu field không dùng QT component → G11, G12 = N/A + ghi lý do. **KHÔNG** được bỏ trống.

### Nhóm M — Button: 5 TC cấp màn hình + 3 TC mỗi button action

**5 TC cấp màn hình (dùng `tc()` riêng):**
- [ ] M01 — Căn lề, chính tả label button
- [ ] M02 — Trạng thái enabled/disabled theo điều kiện
- [ ] M03 — Click button → thực hiện đúng chức năng
- [ ] M04 — Loading + disable khi đang xử lý *(QT component)*
- [ ] M05 — Button Tìm kiếm giữ bộ lọc sau F5/chuyển trang *(QT component)*

**3 TC chuẩn cho MỖI `subsection("Kiểm tra button <Tên>")`:**
- [ ] hiển thị — Cột C: `"Kiểm tra hiển thị nút <Tên>"` (kết quả: hiển thị đúng theo SRS, icon và nhãn chữ đúng chính tả)
- [ ] trạng thái — Cột C: `"Kiểm tra trạng thái enable/disable của nút <Tên>"` (kết quả: trạng thái enable/disable theo điều kiện form)
- [ ] onclick — Cột C: `"Kiểm tra click nút <Tên>"` (kết quả: Onclick hệ thống validate và thực hiện đúng nghiệp vụ theo SRS)

> ⚠️ **LƯU Ý CỘT TRƯỜNG HỢP KIỂM THỬ:** Tuyệt đối KHÔNG ghi tiền tố mã `M01 — `, `M02 — `, `M03 — ` tại cột C (Trường hợp kiểm thử). BẮT BUỘC bắt đầu bằng `"Kiểm tra "` (VD: `M01 — Hiển thị nút Gửi yêu cầu` => `Kiểm tra hiển thị nút Gửi yêu cầu`).

> ⚠️ **Button Xuất Excel:** Nếu màn hình Tra cứu/Danh sách có nút Xuất Excel → BẮT BUỘC có `subsection("Kiểm tra button Xuất Excel")` với **đủ 7 TC chuẩn** (xuất trang hiện tại, xuất theo bộ lọc, tên file `<tên>-ddmmyyyyhhmmss.xlsx`, chia zip >1M dòng, file rỗng chỉ có header, lỗi API hệ thống/timeout, hết token login).

> ⚠️ **Button trên Hộp thoại xác nhận (CONF_*):** Khi một thao tác (Huỷ form khi đã có dữ liệu `ALT-01`, Xoá bản ghi, Phê duyệt, Từ chối, Tiếp nhận...) kích hoạt mở popup xác nhận `CONF_*` → **BẮT BUỘC** tạo riêng subsection cho từng nút trên popup:
> - `subsection("Kiểm tra button Đồng ý trên Hộp thoại xác nhận <Mã popup>")` — Đủ 3 TC (hiển thị / trạng thái / click xác nhận hành động).
> - `subsection("Kiểm tra button Huỷ bỏ trên Hộp thoại xác nhận <Mã popup>")` — Đủ 3 TC (hiển thị / trạng thái / click hủy bỏ đóng popup bảo toàn dữ liệu dở dang).
> - `subsection("Kiểm tra icon đóng (X) trên Hộp thoại xác nhận <Mã popup>")` — Đủ 2 TC (hiển thị / click đóng popup).

### Nhóm V — Chỉnh sửa (Edit Form): Đủ field inventory cho trường được sửa + 5 case đặc thù

- [ ] V_SPEC — Đọc spec phân loại chính xác: trường cho phép sửa vs trường không cho phép sửa (khóa)
- [ ] V_FIELDS — Các trường cho phép sửa: có số lượng test case đầy đủ tương đương Tạo mới (D, E, H, J, K...)
- [ ] V01 — Nạp dữ liệu cũ chính xác 100%
- [ ] V02 — Khóa trường ID/Mã không cho sửa (readonly/disabled)
- [ ] V03 — Sửa 1 hoặc nhiều trường hợp lệ và Lưu thành công
- [ ] V04 — Giữ nguyên không đổi và Lưu (không phát sinh lỗi)
- [ ] V05 — Hủy bỏ (Cancel) khôi phục giá trị ban đầu, không lưu dở dang

### Nhóm Q — FILE UPLOAD (Đủ 3 phân nhóm chính + chuyên sâu)

**1. Kéo thả file vào vùng dropzone (Drag & Drop):**
- [ ] Q01 — Giá trị mặc định (trống, hiển thị hướng dẫn)
- [ ] Q02 — Kiểm tra trường bắt buộc (bỏ trống tệp báo lỗi)
- [ ] Q03 — Kéo thả tệp đúng định dạng
- [ ] Q04 — Kéo thả tệp sai định dạng
- [ ] Q05 — Kéo thả 1 tệp
- [ ] Q06 — Kéo thả nhiều tệp (nếu hỗ trợ)
- [ ] Q07 — Kéo thả tệp có tên tiếng Việt có dấu
- [ ] Q08 — Kéo thả tệp có tên ký tự số
- [ ] Q09 — Kéo thả tệp có tên ký tự đặc biệt
- [ ] Q10 — Kéo thả tệp có tên < 255 ký tự
- [ ] Q11 — Kéo thả tệp có tên = 255 ký tự (hiển thị cắt bớt 'Tên file...')
- [ ] Q12 — Kéo thả tệp có tên > 255 ký tự (hiển thị cắt bớt 'Tên file...')
- [ ] Q13 — Kéo thả tệp có tên thẻ HTML (mã hóa an toàn '<html>/...')
- [ ] Q14 — Kéo thả tệp dung lượng = 0 (file rỗng báo lỗi)
- [ ] Q15 — Kéo thả tệp dung lượng < giới hạn
- [ ] Q16 — Kéo thả tệp dung lượng > giới hạn (báo lỗi vượt dung lượng)
- [ ] Q17 — Kéo thả file trùng tên trong cùng phiên tải
- [ ] Q18 — Kéo thả file ngoài vùng dropzone (không tải lên)

**2. Click button 'Chọn file' (File Picker Dialog):**
- [ ] Q19 — Hiển thị button Chọn file
- [ ] Q20 — Trạng thái button Chọn file (Enable/Disable)
- [ ] Q21 — Click button Chọn file mở File Dialog
- [ ] Q22 — Upload tệp đúng định dạng
- [ ] Q23 — Upload tệp sai định dạng
- [ ] Q24 — Upload 1 tệp
- [ ] Q25 — Upload nhiều tệp (nếu hỗ trợ)
- [ ] Q26 — Upload tệp có tên tiếng Việt có dấu
- [ ] Q27 — Upload tệp có tên ký tự số
- [ ] Q28 — Upload tệp có tên ký tự đặc biệt
- [ ] Q29 — Upload tệp có tên < 255 ký tự
- [ ] Q30 — Upload tệp có tên = 255 ký tự (hiển thị 'Tên file...')
- [ ] Q31 — Upload tệp có tên > 255 ký tự (hiển thị 'Tên file...')
- [ ] Q32 — Upload tệp có tên thẻ HTML (mã hóa an toàn)
- [ ] Q33 — Upload tệp dung lượng = 0 (file rỗng báo lỗi)
- [ ] Q34 — Upload tệp dung lượng < giới hạn
- [ ] Q35 — Upload tệp dung lượng > giới hạn (báo lỗi vượt dung lượng)
- [ ] Q36 — Upload file trùng tên trong cùng phiên tải
- [ ] Q37 — Hủy chọn file (Cancel File Dialog giữ nguyên trạng thái)

**3. Hiển thị file sau khi tải lên & Thao tác file:**
- [ ] Q38 — Hiển thị thông tin file (icon loại file, tên file, dung lượng KB/MB)
- [ ] Q39 — Trạng thái button icon Xóa (Active)
- [ ] Q40 — Click button icon Xóa file thành công
- [ ] Q41 — Tải xuống / xem trước file vừa tải lên (nếu có)

**4. Kiểm tra nội dung & bảo mật chuyên sâu (khi parse file):**
- [ ] Q42 — File có mật khẩu bảo vệ
- [ ] Q43 — File sai cú pháp dữ liệu (malformed)
- [ ] Q44 — File encoding không phải UTF-8
- [ ] Q45 — File có MIME type giả mạo (magic bytes)
- [ ] Q46 — File thiếu sheet/cột bắt buộc


