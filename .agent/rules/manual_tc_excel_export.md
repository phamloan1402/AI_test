---
trigger: always_on
description: Quy chuẩn xuất file Excel test case theo template CIC. Giới hạn < 12.000 ký tự.
---

# Rule: Manual TC Excel Export (Quy Chuẩn Xuất Excel Test Case)

> 📖 **Tài liệu tham chiếu chi tiết:**
> - Chi tiết kịch bản & quy tắc mở rộng: [manual_tc_excel_export_details.md](references/manual_tc_excel_export_details.md)
> - Ví dụ code mẫu & template Python: [tc_excel_export_examples.md](references/tc_excel_export_examples.md)
> - Checklist kiểm thử chuẩn (Nhóm A–W): [common_tc_checklist.md](../skills/rbt_manual_testing/references/common_tc_checklist.md)

---

## 1. Nguyên Tắc Cốt Lõi

- **Engine:** Bắt buộc dùng `scripts/tc_excel_writer.py`. CẤM tự code openpyxl.
- **Import:** `from tc_excel_writer import section, subsection, tc, tc_group, tc_sub, tc_item, FeatureSpec, generate_excel`
- **Output:** `practices/testcases/<DU_AN>/<TenChucNang>_TestCases.xlsx`
- **Sheet độc lập:** Mỗi `FeatureSpec` là 1 sheet hoàn chỉnh. CẤM tách thành phần chung ra sheet M0.
- **Ngôn ngữ:** 100% tiếng Việt có dấu Unicode chuẩn cho mọi cột nội dung.

---

## 2. Quy Chuẩn tc_group() Bắt Buộc (Mặc Định)

AI PHẢI TỰ ĐỘNG group các hành vi, KHÔNG viết thành các `tc()` riêng lẻ:

| Nhóm Control | Tĩnh (`tc()` riêng) | Hành vi (BẮT BUỘC `tc_group()`) |
|---|---|---|
| **D — TEXT** | D01–D04 (Hiển thị, Default, Placeholder, Required) | Nhập keyboard (**17 items**) + Copy-paste (**17 items**) = 34 items |
| **G — TEXTAREA** | D01–D04 + G07 (Enter/Shift+Enter), G11 (Đếm ký tự), G12 (Resize) | Kế thừa đủ Nhóm D: 17 keyboard + 17 paste = Đủ **41 TCs** |
| **E — NUMBER** | E01–E04 (Hiển thị, Default, Placeholder, Required) | Nhập keyboard (**19 items**) + Copy-paste (**19 items**) = 38 items |
| **H — Dropdown** | H01–H06 (gồm H06 bàn phím 5 bước), D22–D23 | Scroll (3 sub), Chọn giá trị (3 sub), **H13–H16 API states (3 sub)**, Search (4 sub) |
| **J — Multiselect** | J01–J06, J14, J10b (bỏ chọn bằng icon ×) | Chọn giá trị (4 sub), Scroll (3 sub), **H13–H16 API states (3 sub)**, Search (4 sub) |
| **C — Grid+Paging** | C01–C03, C05, C07, C09, C10 (Bỏ C04, C06, C08) | Phân trang (5 sub), Combobox số dòng (6 sub), Nhập số trang (4 sub) |

- **BVA đối xứng:** 3 case BVA (`max-1`, `max`, `max+1`) PHẢI group thành `tc_sub("Kiểm tra nhập maxlength")` trong group nhập, đối xứng hoàn toàn với `tc_sub("Kiểm tra copy/paste maxlength")` trong group paste.
- **Coverage Symmetry:** MỌI field cùng loại đều phải có đủ checklist riêng (4 dropdown thì cả 4 đều phải đủ H01–H16). CẤM cắt bớt field sau!

---

## 3. Quy Ước Naming & Auto-Transform (Cột B & Cột C)

Writer tự động xử lý `muc_dich` đầu tiên của `tc()`: Strip prefix ID `WORD_WORD_... - ` -> Strip mã nhóm `H01 `, `D01 ` -> Lowercase chữ đầu -> Thêm `"Kiểm tra "`.
- **Viết `muc_dich` (Cột B):** Viết mô tả thuần túy, chữ thường (VD: `"căn lề, chính tả label button"` -> Cột B: *"Kiểm tra căn lề, chính tả label button"*).
- ❌ **CẤM:** Gõ lặp `"Kiểm tra ..."`, viết hoa chữ đầu, dùng ký tự `→`, gắn đuôi tên trường/màn hình sau mỗi case (vì đã có Section/Subsection phân cấp).
- **Quy ước Cột C (Trường hợp kiểm thử):** Tuyệt đối **KHÔNG** chứa bất kỳ mã nhóm hay tiền tố STT nào (CẤM ghi `K01 — `, `K02 — `, `A01 — `, `D01 — `, `E01 — `, `H06 — `, `C01 — `, `M01 — `, `CONF_001 — `, `V01 — `, `1. `...). Cột C chỉ ghi nội dung hành vi / trường hợp cần kiểm thử (VD: *"Focus Calendar khi ô Thời gian gửi yêu cầu từ ngày đến ngày trống"*). Engine `tc_excel_writer.py` cũng tự động strip các mã này nếu vô tình truyền vào.

**Chuẩn hóa tên `subsection()`:**
- Textbox: `subsection("Kiểm tra Textbox <Tên trường>")`
- Textarea: `subsection("Kiểm tra Area box <Tên trường>")`
- Dropdown (1 chọn): `subsection("Kiểm tra Dropdown <Tên trường>")`
- Combobox (nhiều chọn): `subsection("Kiểm tra Combobox <Tên trường>")`
- Number: `subsection("Kiểm tra Number <Tên trường>")`

---

## 4. Cấu Trúc Section & Kịch Bản Đặc Thù

Mỗi Feature Sheet gồm 2 Section chính:
1. **Section "Giao diện":** Mở đầu bằng `subsection("Nhóm A — Giao diện chung")` với **đủ 6 TC chuẩn A01–A06** (Hiển thị, Mặc định, Bố cục/Dấu *, Tab thuận, Shift+Tab nghịch, Zoom responsive). Tiếp theo là các control nhập liệu.
2. **Section "Chức năng":** Tên chuẩn:
   ```python
   section("Chức năng (Phần này viết các trường hợp kiểm thử kiểm tra các ràng buộc trong cơ sở dữ liệu và cho các luồng nghiệp vụ trong tài liệu giải pháp, tích hợp với các chức năng khác)")
   ```
   Gồm 3 subsection: `"Kiểm tra <hành động> thành công"`, `"Kiểm tra <hành động> không thành công"`, `"Kiểm tra phân quyền"`.

**Kịch bản kiểm thử đặc thù:**
- **Button Action:** Mỗi nút -> `subsection("Kiểm tra button <Tên>")` với **ít nhất 3 TC chuẩn** (Hiển thị / Trạng thái / Onclick). Cột C BẮT BUỘC bắt đầu bằng `"Kiểm tra "`, KHÔNG chứa tiền tố mã `M01 — `, `M02 — `.
- **Button Xuất Excel:** Có nút Xuất Excel -> PHẢI có `subsection("Kiểm tra button Xuất Excel")` với **đủ 7 TC chuẩn** (Trang hiện tại, Bộ lọc, Tên file chuẩn kèm timestamp, Chia zip > 1 triệu dòng, Dữ liệu rỗng có header, Lỗi API, Token timeout).
- **Hộp thoại xác nhận (CONF_*):** Có popup xác nhận (`ALT-01`, Xóa, Duyệt...) -> BẮT BUỘC tạo đủ 3 subsections cho **3 control con**: Nút Đồng ý (3 TCs), Nút Huỷ bỏ (3 TCs), Icon đóng X (2 TCs).
- **Màn hình Chỉnh sửa (Edit):** Trường sửa được phải đủ TC như tạo mới. BẮT BUỘC có **5 case đặc thù Edit (thuộc Nhóm V)**: `V01` (Nạp dữ liệu cũ), `V02` (Khóa trường ID/mã), `V03` (Sửa và Lưu), `V04` (Giữ nguyên và Lưu), `V05` (Hủy bỏ khôi phục giá trị cũ). Mã test case chuẩn tuân thủ định dạng: `[tên_chức_năng]_[SỐ]` (ví dụ: `[tên_chức_năng]_001`, `[tên_chức_năng]_V01`).
- **Xem chi tiết (Detail View):** Thẻ trạng thái (Status Tag màu/nhãn, readonly), 100% trường dữ liệu readonly, nút thao tác (Đóng, Sửa).
- **Batch Action:** Phân tách rõ 3 trạng thái: $N = 0$ (Chặn/cảnh báo), $N = 1$ (Xác nhận đơn lẻ kèm mã/tên), $N > 1$ (Xác nhận tổng thể N bản ghi).
- **SQL Tra cứu BIZ:** Mọi ca tra cứu trong Section Chức năng BẮT BUỘC đính kèm câu lệnh SQL mẫu đối soát CSDL (`SELECT ... WHERE ...`), bao gồm cả ca Empty state.
- **Quy tắc dải ID & Mã testcase:** Mã test case chuẩn luôn có format `[tên_chức_năng]_[SỐ]` (ví dụ: `Login_001`, `M1_001`). Nhập keyboard liền mạch (`M1_001..`), Copy-paste dải **500+** (`M1_500..`), Search option popup dải **600+** (`M1_600..`).

---

## 5. Bảng Anti-Patterns Cốt Lõi (NGHIÊM CẤM)

| Nhóm | ❌ Hành vi SAI (Bị từ chối) | ✅ Hành vi ĐÚNG (Chuẩn hóa) |
|---|---|---|
| **Module** | Tự code openpyxl; Tách thành phần chung ra sheet M0 riêng | Dùng `tc_excel_writer.py`; Mỗi FeatureSpec là 1 sheet độc lập tự hoàn chỉnh |
| **Ngôn ngữ** | Viết không dấu, tiếng Anh trong nội dung TC | 100% tiếng Việt có dấu đầy đủ Unicode chuẩn |
| **Cấu trúc** | Thiếu Nhóm A 6 TCs; BIZ đặt tên sai chuẩn | Đủ Nhóm A01–A06; Section BIZ chuẩn: `"Chức năng (Phần này viết...)"` |
| **tc_group** | Dùng `tc()` riêng lẻ cho BVA D05–D07 / copy-paste / H07-H16 | BẮT BUỘC dùng `tc_group()` cho toàn bộ hành vi nhập, paste, scroll, API states |
| **Button** | Cột C chứa tiền tố mã `M01 — `; Thiếu 3 TC popup `CONF_*` | Cột C bắt đầu bằng `"Kiểm tra "`; Đủ 8 TCs cho 3 control popup CONF_* |
| **Coverage** | Cắt bớt checklist của field 2+ khi có nhiều field cùng loại | **Coverage Symmetry**: MỌI field cùng loại đều phải có đủ 100% checklist riêng |
| **Textarea** | Chỉ sinh vài case ngắn gọn cho Textarea lý do/ghi chú | Đủ **41 TCs Nhóm G** (4 tĩnh + 17 keyboard + 17 paste + G07 + G11 + G12) |
| **Cột C** | Chứa mã nhóm/STT: `K01 — `, `D01 — `, `M01 — `, `C01 — `, `CONF_001 — `, `1. ` | Tuyệt đối KHÔNG chứa mã nhóm hay STT, chỉ ghi trực tiếp hành vi kiểm thử |