# Manual TC Excel Export — Đặc Tả Chi Tiết & Kịch Bản Chuẩn

> **Tài liệu tham chiếu chuyên sâu cho rule:** `.agent/rules/manual_tc_excel_export.md`  
> **Ví dụ mã nguồn Python:** `.agent/rules/references/tc_excel_export_examples.md`  
> **Engine chính:** `scripts/tc_excel_writer.py`

---

## 1. Đặc Tả Chi Tiết Các Nhóm tc_group() Bắt Buộc

### 1.1. Nhóm D — TEXT Field (Chuẩn 38 TCs)
- **Tĩnh (dùng `tc()` riêng):** D01 (Hiển thị), D02 (Mặc định), D03 (Placeholder), D04 (Bỏ trống required).
- **Hành vi nhập keyboard (`tc_group("Kiểm tra khi nhập giá trị")` — 17 tc_item):**
  - BẮT BUỘC mở đầu bằng: `tc_sub("Kiểm tra nhập maxlength")` gồm 3 items BVA: `max-1`, `max`, `max+1`.
  - Các sub tiếp theo: Khoảng trắng (toàn space, đầu cuối, giữa), Ký tự số, Ký tự đặc biệt (hợp lệ / không hợp lệ theo spec), Chữ hoa, Chữ thường, Ký tự tiếng Việt có dấu, Ký tự Unicode/emoji, Security (SQLi `' OR '1'='1'`, XSS `<script>`).
- **Hành vi copy/paste (`tc_group("Kiểm tra khi copy/paste giá trị")` — 17 tc_item):**
  - BẮT BUỘC mở đầu bằng: `tc_sub("Kiểm tra copy/paste maxlength")` gồm 3 items BVA: `max-1`, `max`, `max+1` (dùng thuật ngữ *"bị cắt còn <max>"* / truncate, không dùng *"bị chặn"*).
  - Đối xứng hoàn toàn 1-1 với 17 items của nhóm nhập keyboard (ký tự không hợp lệ khi paste thì *"bị lọc"*).

### 1.2. Nhóm G — Textarea / Area Box (Chuẩn 41 TCs)
Bao gồm đủ **38 TCs của Nhóm D** (4 tĩnh + 17 nhập keyboard + 17 copy-paste) cộng thêm **3 TCs đặc thù Textarea**:
- `G07`: Kiểm tra ngắt dòng bằng phím Enter và Shift+Enter (con trỏ xuống dòng mới mượt mà, lưu trữ chuỗi newline `\n` chính xác).
- `G11`: Kiểm tra bộ đếm số ký tự (nếu UI có hiển thị dạng `x/max`, số đếm tăng/giảm realtime khi nhập hoặc xóa ký tự).
- `G12`: Kiểm tra kéo giãn kích thước (Resize handle: thử kéo góc dưới bên phải để mở rộng vùng nhập liệu, layout không bị vỡ).
> ⚠️ **Lưu ý:** Không tách Textarea lý do/ghi chú ra sheet riêng; mỗi sheet FeatureSpec phải chứa đầy đủ Nhóm G độc lập.

### 1.3. Nhóm E — NUMBER Field (Chuẩn 42 TCs)
- **Tĩnh:** E01-E04 (Hiển thị, Mặc định, Placeholder, Bỏ trống required).
- **Hành vi keyboard & paste:** Mỗi nhóm gồm **19 items** (BVA min-1, min, min+1, max-1, max, max+1, số âm, số thập phân dấu chấm/phẩy, ký tự chữ, ký tự đặc biệt, leading zeros, định dạng phân cách hàng nghìn).

### 1.4. Nhóm H — Dropdown (Single Select)
- **Tĩnh:** H01-H06 (Hiển thị, Mặc định, Mở popup, Đóng khi click ngoài, Icon mũi tên, Điều hướng bàn phím 5 bước H06).
- **Hành vi (Bắt buộc dùng `tc_group`):**
  - Scroll options: `tc_group("Kiểm tra hiển thị scroll")` (3 sub: danh sách <5, =5, >5 items).
  - Chọn giá trị: `tc_group("Kiểm tra chọn giá trị")` (3 sub: chọn 1 giá trị, không cho chọn nhiều, bỏ chọn/chọn lại).
  - Tìm kiếm option popup (nếu Searchable): `tc_group("Kiểm tra nhập tìm kiếm")` (4 sub: tìm kiếm tương đối/tuyệt đối, tìm không ra kết quả, chuỗi ≤N ký tự, chuỗi >N ký tự).
  - **API States (H13-H16 BẮT BUỘC):** `tc_group("Kiểm tra options hiển thị đúng")` gồm 3 `tc_sub`:
    + *"Trường hợp call API thành công"*: 2 items (Dữ liệu trả về khác rỗng / Dữ liệu trả về rỗng).
    + *"Trường hợp Call API bị thất bại"*: 1 item (Lỗi server 500 / Network down).
    + *"Trường hợp Call API bị time out"*: 1 item (Quá thời gian phản hồi > 30s).

### 1.5. Nhóm J — Multiselect (Combobox Chọn Nhiều)
- Kế thừa toàn bộ H01-H06, H13-H16 API states, scroll và search popup.
- Chọn giá trị: `tc_group("Kiểm tra chọn giá trị")` gồm 4 sub: (1) Chọn 1 giá trị, (2) Chọn nhiều giá trị, (3) Bỏ chọn 1 giá trị bằng click lại list item, (4) Bỏ chọn nhiều giá trị.
- **TC riêng J10b (Bỏ chọn bằng icon ×):** Khi tag hiển thị có icon ×, bắt buộc có `tc()` kiểm tra click icon × để gỡ bỏ lựa chọn.

### 1.6. Nhóm C — Grid / Table & Phân Trang
- **TC riêng lẻ:** C01 (Hiển thị grid), C02 (Cột STT tự tăng liên tục qua các trang), C03 (Ẩn phân trang khi tổng bản ghi ≤ 10), C05 (Empty state "Không có dữ liệu"), C07 (Loading spinner khi tải API), C09 (Hover highlight dòng), C10 (Cuộn ngang fixed header/columns).
- **3 nhóm `tc_group` phân trang (BẮT BUỘC):**
  - `tc_group("Kiểm tra phân trang")`: 5 sub (Trang mặc định 1, Chuyển đến trang cuối, Về trang đầu, Nút Next, Nút Previous).
  - `tc_group("Kiểm tra combobox phân trang")`: 6 sub (Giá trị mặc định 10/20 dòng, Danh sách options 10/20/50/100, Chọn 1 option, Chọn nhiều bị chặn, Không chọn giá trị, Thao tác phím mũi tên).
  - `tc_group("Kiểm tra nhập tìm kiếm số trang")`: 4 sub (Nhập ký tự chữ, Nhập ký tự đặc biệt, Nhập số trang hợp lệ nhảy đúng trang, Nhập số trang vượt quá trang tối đa).
  - ⚠️ Khi đã dùng 3 nhóm trên, **BỎ** các `tc()` riêng lẻ C04, C06, C08 để tránh trùng lặp.

---

## 2. Kịch Bản Chuẩn Cho Các Màn Hình & Control Đặc Thù

### 2.1. Button Xuất Excel (Đủ 7 Test Cases Chuẩn)
Khi màn hình có chức năng xuất file Excel, bắt buộc tạo `subsection("Kiểm tra button Xuất Excel")` với 7 cases:
1. `Xuất trang hiện tại`: Chỉ xuất đúng số lượng bản ghi đang hiển thị trên trang hiện tại của bảng.
2. `Xuất theo bộ lọc`: Xuất toàn bộ dữ liệu thỏa mãn bộ lọc tìm kiếm (không giới hạn phân trang).
3. `Tên file chuẩn`: Tên tệp không dấu kèm timestamp: `<ten_danh_sach_khong_dau>_ddmmyyyyhhmmss.xlsx`.
4. `Chia tệp zip khi dữ liệu lớn`: Dữ liệu > 1.000.000 dòng -> hệ thống tự đóng gói thành tệp `.zip` chứa nhiều file `.xlsx`.
5. `Dữ liệu rỗng`: Khi bộ lọc không có bản ghi nào -> file Excel xuất ra vẫn có hàng tiêu đề (Header).
6. `Lỗi ngoại lệ API`: Xử lý khi API lỗi 500 hoặc timeout -> thông báo "Yêu cầu mất quá nhiều thời gian để phản hồi".
7. `Hết phiên đăng nhập / Token timeout`: Token hết hạn trong khi click xuất file -> điều hướng về trang Login.
> ⚠️ **Nếu Xuất Excel mở popup chứa nhiều lựa chọn con:** Tạo riêng subsection cho từng nút con ("Xuất trang hiện tại", "Xuất theo bộ lọc", "In ấn"), mỗi subsection đủ 3 TC chuẩn.

### 2.2. Hộp Thoại Xác Nhận (Dialog CONF_*)
Khi kích hoạt popup xác nhận (Huỷ form có dữ liệu `ALT-01`, Xoá bản ghi, Từ chối, Phê duyệt...), bắt buộc tạo đủ 3 subsections cho 3 control UI độc lập:
1. `subsection("Kiểm tra button Đồng ý trên Hộp thoại xác nhận <Mã popup>")`:
   - Hiển thị: Căn lề, màu sắc, nhãn chữ chuẩn thiết kế Ant Design.
   - Trạng thái: Nút ở trạng thái enable.
   - Onclick: Thực thi hành động xác nhận (đóng popup, hủy dữ liệu/cập nhật CSDL, điều hướng).
2. `subsection("Kiểm tra button Huỷ bỏ trên Hộp thoại xác nhận <Mã popup>")`:
   - Hiển thị, Trạng thái, Onclick (đóng popup, giữ nguyên màn hình và bảo toàn 100% dữ liệu đang nhập dở).
3. `subsection("Kiểm tra icon đóng (X) trên Hộp thoại xác nhận <Mã popup>")`:
   - Hiển thị (góc trên bên phải modal dialog), Onclick (đóng popup và bảo toàn dữ liệu tương tự nút Huỷ bỏ).

### 2.3. Màn Hình Chỉnh Sửa (Edit Form — 5 Cases Đặc Thù Bắt Buộc)
- **Quy tắc phân loại:** Đọc kỹ SRS để phân loại trường cho phép sửa vs trường khóa/readonly. Các trường cho phép sửa phải có số test case tương đương màn hình tạo mới (đủ D, H, J, K...).
- **5 cases đặc thù của Edit:**
  - `E_SP_01` (Nạp dữ liệu cũ chính xác): Mở form, kiểm tra 100% trường hiển thị đúng dữ liệu đã lưu trong DB.
  - `E_SP_02` (Khóa trường ID/Mã không cho sửa): Các trường mã/khóa/hệ thống sinh ở trạng thái `disabled` hoặc `readonly`.
  - `E_SP_03` (Chỉnh sửa 1 hoặc nhiều trường): Thay đổi dữ liệu hợp lệ và bấm Lưu -> Lưu thành công, cập nhật CSDL.
  - `E_SP_04` (Giữ nguyên không đổi và Lưu): Mở form, không thay đổi bất kỳ trường nào rồi bấm Lưu -> Lưu thành công, không báo lỗi trùng lặp.
  - `E_SP_05` (Hủy bỏ khôi phục giá trị ban đầu): Sửa một số trường rồi bấm Hủy -> Đóng form, giữ nguyên dữ liệu gốc ban đầu.

### 2.4. Màn Hình / Popup Xem Chi Tiết (Detail View)
1. **Kiểm tra Thẻ trạng thái (Status Badge/Tag):** Vị trí hiển thị, màu sắc/nhãn tương ứng từng trạng thái (Active, Inactive, Running, Failed, Đang xử lý...), tính chất chỉ đọc (không click chuyển trạng thái trực tiếp).
2. **Kiểm tra dữ liệu chi tiết:** Hiển thị đúng 100% dữ liệu của bản ghi được chọn, toàn bộ trường ở trạng thái chỉ đọc (`readonly` / `disabled`).
3. **Nút thao tác trên popup:** Kiểm tra nút Đóng, Chỉnh sửa, Tải tệp (nếu có).

### 2.5. Thao Tác Hàng Loạt (Batch Action)
Phân tách rõ 3 trạng thái số lượng bản ghi chọn:
- **$N = 0$ (Chưa chọn dòng nào):** Nút action bị disabled hoặc click vào hiển thị toast cảnh báo: *"Vui lòng chọn ít nhất một bản ghi để thực hiện!"*.
- **$N = 1$ (Chọn đúng 1 dòng):** Popup hiển thị câu hỏi xác nhận đơn lẻ kèm thông tin bản ghi (Mã, Tên bản ghi, `CONF_001`).
- **$N > 1$ (Chọn từ 2 dòng trở lên):** Popup hiển thị câu hỏi xác nhận tổng thể: *"Bạn có chắc chắn muốn thực hiện với N bản ghi đã chọn không?"* (`CONF_002`).

### 2.6. Kịch Bản Tra Cứu BIZ — Kèm SQL Database
- Mọi test case tra cứu trong Section Chức năng (BIZ) BẮT BUỘC đính kèm câu lệnh SQL mẫu tương ứng trong cột Kết quả mong muốn (`SELECT ... FROM ... WHERE ...`).
- Trường hợp tra cứu không có dữ liệu (Empty state) cũng phải có câu lệnh SQL chứng minh không có bản ghi trả về, kèm thông báo UI: *"Không tìm thấy bản ghi nào phù hợp"*.

---

## 3. Quy Tắc Auto-Transform Cho tc() (Cột B)

Hàm `tc()` trong `tc_excel_writer.py` tự động format tham số `muc_dich` đầu tiên theo các bước:
1. **Strip prefix ID:** Bỏ mọi tiền tố dạng `WORD_WORD_... - ` trước dấu ` - ` (VD: `M1_001 - `, `M1_CHAYLAI_M01 - `).
2. **Strip code nhóm:** Bỏ tiếp các mã nhóm `H01 `, `D01 ` nếu còn sót.
3. **Chuẩn hóa chữ đầu & Thêm "Kiểm tra ":** Lowercase chữ cái đầu và thêm tiền tố `"Kiểm tra "`.
> **Kết quả:** Cột B luôn hiển thị `"Kiểm tra [mô tả]"` — **Tuyệt đối KHÔNG có mã ID xuất hiện trong cột B của file Excel**.

**Quy tắc viết `muc_dich`:**
- Viết mô tả thuần túy, chữ thường (VD: `"căn lề, chính tả label button"` -> Cột B: *"Kiểm tra căn lề, chính tả label button"*).
- ❌ KHÔNG tự gõ `"Kiểm tra ..."` (gây lặp thành *"Kiểm tra kiểm tra..."*).
- ❌ KHÔNG đưa tên trường hoặc tên màn hình vào `muc_dich` vì đã có phân cấp Section và Subsection.

---

## 4. Quy Tắc Cột C (Trường Hợp Kiểm Thử) — Bỏ Hết Mã Nhóm & STT

- **Bỏ 100% mã nhóm & STT:** Cột C tuyệt đối **KHÔNG** chứa tiền tố mã nhóm hay số thứ tự (CẤM ghi `K01 — `, `K02 — `, `A01 — `, `D01 — `, `E01 — `, `H06 — `, `C01 — `, `M01 — `, `CONF_001 — `, `V01 — `, `1. `...).
- **Ghi trực tiếp hành vi:** Cột C chỉ ghi rõ ràng hành vi / ngữ cảnh kiểm thử, viết hoa chữ cái đầu tiên (VD: *"Focus Calendar khi ô Thời gian gửi yêu cầu từ ngày đến ngày trống"*, *"Chọn khoảng ngày từ Calendar popup"*, *"Nhập tay sai format ngày"*, *"Hiển thị cột STT tự động tăng"*).
- **Engine auto-strip:** Engine `scripts/tc_excel_writer.py` tích hợp sẵn bộ lọc regex `_strip_truong_hop()` tự động loại bỏ mọi mã nhóm hoặc STT nếu vô tình được truyền vào tham số `truong_hop`.
