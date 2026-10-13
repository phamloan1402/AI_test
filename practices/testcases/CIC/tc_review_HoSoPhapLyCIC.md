# TC Lead Review Report — [FUNC-XLDL-009] XLDL hồ sơ pháp lý

> Pipeline: `HoSoPhapLyCIC` · Bước 5b (TC Lead Review Gate) · Ngày review: 2026-10-12
> Bộ TC: `scripts/gen_tc_hosophaplycic.py` → `practices/testcases/CIC/HoSoPhapLyCIC_TestCases.xlsx` (bản chạy thử, chưa phải bản final)
> Căn cứ: SRS Confluence 1212957 + 8 trang con · Q&A `practices/Q&A/HoSoPhapLyCIC_QA.md` · Truy vết `practices/testcases/CIC/HoSoPhapLyCIC_B3_B4.md` (B4 đã duyệt)

## Số liệu bộ TC

| Sheet | Tổng | Giao diện | Chức năng | Cao | Trung bình | Thấp |
|---|---:|---:|---:|---:|---:|---:|
| M1_DanhSach | 448 | 409 | 39 | 125 | 237 | 86 |
| M2_ChiTiet_D10D11 | 103 | 85 | 18 | 43 | 39 | 21 |
| M3_ChiTiet_Q11 | 93 | 75 | 18 | 36 | 36 | 21 |
| M4_XuLy_D10D11 | 241 | 183 | 58 | 98 | 120 | 23 |
| M5_XuLy_Q11 | 229 | 183 | 46 | 89 | 117 | 23 |
| M7_XuLyDongThoi | 270 | 195 | 75 | 116 | 130 | 24 |
| M8_NghiepVu_TichHop | 21 | 0 | 21 | 16 | 5 | 0 |
| **Tổng** | **1.405** | **1.130** | **275** | **523** | **684** | **198** |

**Kiểm tra tự động đã chạy (Verification Checklist):**
- Nhóm A: đủ A01–A06 (+A08) cho MH-001, MH-002, MH-003, MH-004, MH-005, MH-008 và từng popup MH-006/MH-007 trong mỗi sheet sử dụng.
- Nhóm G (Lý do): 6 ô Lý do (MH-006, MH-007 × sheet M4, M5, M7), mỗi ô đủ 4 TC tĩnh + 17 item nhập + 17 item copy/paste + G07, G11, G12 = 41 TC.
- Nhóm H/J: mọi dropdown/combobox có đủ hiển thị, mặc định, placeholder, bắt buộc, options, bàn phím, chọn giá trị, API states; 6 control có ô tìm kiếm có thêm nhóm tìm kiếm (D22–D28).
- Nhóm C: C01, C02, C03, C05, C07, C11–C16 + 3 tc_group phân trang; Nhóm U: 15 cột + 2 thao tác (MH-001), 8 cột lịch sử (MH-002/003), 4 cột so sánh (MH-004/005/008).
- CONF: mỗi popup MH-006/MH-007 có nút xác nhận (3), Hủy (3), icon X (2).
- Truy vết: đủ 48/48 BR (BR-039 không tồn tại); đủ 11/11 mã thông báo (ERR_001, ERR_003, ERR_011, ERR_023, WAR_009, INF_003, INF_009, INF_010, INF_011, SUC_001, CONF_001).
- Cột B không có "Kiểm tra kiểm tra"; cột C không chứa mã nhóm/STT; 100% nội dung tiếng Việt có dấu.

## Tóm tắt đánh giá

| Tiêu chí | Trạng thái | Số lượng vấn đề |
|----------|-----------|----------------|
| Coverage | ⚠️ Cần bổ sung | 5 (GAP-01, 02, 03, 04, 05) |
| Clarity | ⚠️ Cần xác nhận | 2 (GAP-06, 07) |
| Accuracy | ⚠️ Cần xác nhận | 2 (GAP-08, 09) |
| Feasibility | ⚠️ Cần chuẩn bị môi trường | 1 (GAP-10) |
| Organization | ✅ Đạt (1 ghi nhận) | 1 (GAP-11) |
| Traceability & RBT | ⚠️ Cần bổ sung | 1 (GAP-12) |

## Danh sách vấn đề phát hiện

### [GAP-01] — Thiếu coverage: ERR_023 không có TC kiểm tra hiển thị thực tế
- **Tiêu chí:** Coverage
- **TC liên quan:** M4/M5/M7 → "Kiểm tra Area box Lý do (MH-006/MH-007)" → nhóm "Kiểm tra nhập maxlength" (item 1001 ký tự)
- **Vấn đề:** Theo assumption Q32, ô Lý do chặn nhập ở 1000 ký tự và cắt khi paste, nên ERR_023 ("Lý do không được vượt quá 1000 ký tự.") không bao giờ hiện qua UI. Nhưng SRS EXC-01 vẫn liệt kê ERR_023. Hiện chưa có TC nào kiểm tra ERR_023 thực sự xuất hiện.
- **Đề xuất:** Bổ sung 1 TC cho mỗi popup ở mỗi sheet (6 TC): bỏ maxlength bằng DevTools (hoặc gửi trực tiếp API) với Lý do 1001 ký tự → hệ thống trả ERR_023, không ghi dữ liệu.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-02] — Coverage rút gọn: nhóm scroll của dropdown có danh sách cố định chỉ có trường hợp "< 5"
- **Tiêu chí:** Coverage (`[CHECK 1]` yêu cầu đủ 3 trường hợp scroll)
- **TC liên quan:** Loại khách hàng (2 option), Mã tệp (3), Nhóm khách hàng (4), Trạng thái (4), Ngày báo cáo cột TCTD (tối đa 3 — BR-032)
- **Vấn đề:** Các danh sách này cố định theo SRS nên không thể tạo dữ liệu có 5 hoặc trên 5 option. Tôi chỉ sinh trường hợp "< 5".
- **Đề xuất:** Bỏ qua, ghi N/A với lý do: danh sách cố định theo SRS.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-03] — Coverage N/A: C09/C10 (thêm/sửa/xóa từ trang N) và K04, K09–K11, K17
- **Tiêu chí:** Coverage
- **TC liên quan:** M1 → "Kiểm tra lưới dữ liệu và phân trang"; 2 DatePicker khoảng ngày
- **Vấn đề:**
  - C09/C10 không áp dụng: lưới không có thêm/sửa/xóa. Thay vào đó có TC Chức năng "trạng thái danh sách sau khi xử lý và quay về" (assumption Q33).
  - K04 (nút bỏ chọn ngày): mockup hiện hành của MH-001 không có icon x; mockup cũ thì có.
  - K09–K11: SRS không cấm ngày quá khứ/tương lai.
  - K17: Quy tắc component cho phép chọn ngày tự do khi tìm kiếm.
- **Đề xuất:** Bỏ qua C09, C10, K09–K11, K17 (N/A). Riêng K04: nếu môi trường thật có icon x thì bổ sung 1 TC cho mỗi DatePicker (2 TC).
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-04] — Coverage rút gọn theo RBT: hiển thị chỉ tiêu ở màn xem chi tiết kiểm theo nhóm
- **Tiêu chí:** Coverage
- **TC liên quan:** M2/M3 → "Kiểm tra nhóm chỉ tiêu khách hàng tổ chức/cá nhân" (1 TC/nhóm, liệt kê đủ mã chỉ tiêu trong kết quả mong muốn)
- **Vấn đề:** MH-002 có 56 chỉ tiêu, MH-003 có 35 chỉ tiêu, đều là label chỉ đọc với cùng một quy tắc (BR-028, BR-030). Tôi gộp mỗi nhóm thành 1 TC thay vì 1 TC cho từng chỉ tiêu.
- **Đề xuất:** Giữ nguyên vì đây là nhãn chỉ đọc, rủi ro thấp. Nếu muốn truy vết tới từng chỉ tiêu, có thể tách 1 TC/chỉ tiêu (thêm khoảng 90 TC).
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-05] — Coverage: công tắc "Chỉ hiện chỉ tiêu khác biệt" chưa kiểm trạng thái loading
- **Tiêu chí:** Coverage
- **TC liên quan:** M4/M5/M7 → "Kiểm tra Checkbox Chỉ hiện chỉ tiêu khác biệt (công tắc)"
- **Vấn đề:** Công tắc đang được kiểm bằng nhóm I (bật/tắt). Quy tắc component về Switch còn yêu cầu nhãn Bật/Tắt và trạng thái loading. Mockup P6 không có nhãn Bật/Tắt (SRS ưu tiên hơn), nhưng phần loading không mâu thuẫn với SRS.
- **Đề xuất:** Bổ sung 1 TC loading cho mỗi sheet (3 TC); không thêm TC nhãn Bật/Tắt.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-06] — Clarity: thông báo khi hồ sơ đã được xử lý (Q06) chưa có nội dung chính xác
- **Tiêu chí:** Clarity
- **TC liên quan:** M4/M5/M7 → "hồ sơ đã được cán bộ khác xử lý", "mở xử lý từ danh sách cũ"
- **Vấn đề:** BA chốt "chặn + thông báo hồ sơ đã được xử lý" nhưng chưa có mã hoặc nội dung thông báo. Vì vậy kết quả mong muốn chỉ kiểm được ý nghĩa, không đối chiếu được câu chữ.
- **Đề xuất:** Xin BA mã/nội dung thông báo rồi sửa kết quả mong muốn. Trong lúc chờ, giữ nguyên.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-07] — Clarity: câu lệnh SQL đối soát dùng tên bảng/cột giả định
- **Tiêu chí:** Clarity / Feasibility
- **TC liên quan:** Mọi TC tra cứu ở M1, M2, M3, M4, M5, M7, M8 có "SQL đối soát (mẫu)"
- **Vấn đề:** SRS ghi "Tên bảng xác định tại thiết kế cơ sở dữ liệu", nên SQL đang dùng tên giả: `<HO_SO_PHAP_LY>`, `<KHO_TCTD>`, `<KHO_CHUAN_CICINFO>`, cột `MA_DAU_MOI`, `NHOM_KH`…
- **Đề xuất:** Nếu bạn có tài liệu thiết kế CSDL, cung cấp để tôi thay tên thật; nếu chưa có, giữ dạng mẫu.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-08] — Accuracy: thứ tự Tab ở MH-004/MH-005/MH-008 suy từ text, chưa đối chiếu mockup
- **Tiêu chí:** Accuracy
- **TC liên quan:** M4/M5/M7 → Nhóm A "thứ tự di chuyển con trỏ khi nhấn phím Tab"
- **Vấn đề:** Ảnh mockup của P4 (6030601) không tải được; thứ tự Tab dựa trên mô tả bố cục trong text và mockup P6.
- **Đề xuất:** Giữ nguyên và xác nhận khi chạy thực tế; nếu lệch thì ghi nhận lỗi giao diện.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-09] — Accuracy: một số kết quả mong muốn dựa trên assumption chưa được BA xác nhận riêng
- **Tiêu chí:** Accuracy
- **TC liên quan:** Các TC có ghi "assumption Qxx": Q08–Q20, Q22–Q37, Q39, Q41, Q42 (ví dụ Làm mới → lưới rỗng; chặn nhập 1000 ký tự; công tắc đặt lại khi chuyển hồ sơ)
- **Vấn đề:** Bạn đã chấp thuận dùng các assumption này ở B2, nhưng BA chưa xác nhận từng câu.
- **Đề xuất:** Giữ nguyên. Khi BA phản hồi khác thì ghi REOPEN và sửa các TC có cùng mã Qxx (dễ tìm theo chuỗi "assumption Qxx").
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-10] — Feasibility: nhiều TC cần môi trường/công cụ ngoài chức năng
- **Tiêu chí:** Feasibility
- **TC liên quan:**
  - M8: nạp tệp D10/D11/Q11, cấp mã ở FUNC-XLDL-013, chuông thông báo.
  - M4/M5/M7: kiểm chứng C06 (FUNC-XLDL-035), nghi trùng (FUNC-XLDL-013), INF_011 (Push/Email), liên kết FUNC-WEB-002.
  - M7: giả lập lỗi bước sau để kiểm tra rollback all-or-nothing (Q07).
  - Mọi sheet: giả lập API lỗi/time out.
- **Vấn đề:** Không thực thi được nếu thiếu mock API, quyền truy cập các chức năng liên quan, hộp thư test.
- **Đề xuất:** Giữ TC và bổ sung vào kế hoạch test danh sách điều kiện môi trường (mock API, tài khoản cbxl01/cbxl02/cbxl03/nsd01, hộp thư nhận INF_011).
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-11] — Organization (ghi nhận): mã TC trong file
- **Tiêu chí:** Organization
- **TC liên quan:** Toàn bộ
- **Vấn đề:** `tc_excel_writer.py` tự đánh số cột ID (1..n) theo từng sheet; tiền tố `HSPL` chỉ nằm ở ô "Mã trường hợp kiểm thử" (C4). Cách này giống các bộ TC khác của dự án (CXĐ, Phân quyền dữ liệu).
- **Đề xuất:** Bỏ qua (theo chuẩn writer). Nếu cần ID dạng `HSPL_001` ở từng dòng thì phải sửa writer dùng chung, ảnh hưởng các dự án khác.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-12] — RBT: sheet M8 (rủi ro High) mỏng so với các sheet UI
- **Tiêu chí:** Traceability & RBT
- **TC liên quan:** M8_NghiepVu_TichHop (21 TC)
- **Vấn đề:** Phân loại khi tiếp nhận (BR-003/004/007/008) là logic lõi quyết định toàn bộ luồng sau, nhưng mới chỉ kiểm với tệp D11 và KH cá nhân. Chưa có kết hợp theo loại tệp (D10, Q11) × Loại KH Tổ chức (MSDN, TC004–TC006 quan trọng). Ngoài ra 80% bộ TC là Giao diện do checklist bắt buộc, trong khi phần Chức năng chỉ có 275 TC.
- **Đề xuất:** Bổ sung khoảng 12 TC cho M8:
  - Phân loại R1–R4 cho D10 và Q11 (8 TC).
  - KH tổ chức đổi MSDN / TC004 (2 TC).
  - Hồ sơ Q11 thay đổi chỉ tiêu không thuộc tập Q11 (1 TC).
  - INF_010 đếm đúng khi tệp có cả Chờ cấp mã và Chờ xem xét (1 TC).
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

## Hướng dẫn xác nhận
1. Đọc từng GAP trong danh sách trên.
2. Tích vào checkbox [x] cho hành động bạn muốn thực hiện (hoặc trả lời ngắn trong chat, ví dụ: "GAP-01, 05, 12 bổ sung; còn lại bỏ qua").
3. Với hành động "Bỏ qua": điền lý do vào dòng đó (hoặc đồng ý lý do N/A đã đề xuất).
4. Với hành động "Bổ sung TC mới": có thể ghi thêm gợi ý nội dung TC cần sinh.
5. Khi đã xử lý xong toàn bộ GAP, reply: **"Đã review xong, tiến hành sinh bộ TC final"**.

---

## Quyết định của user (2026-10-12) và kết quả xử lý

| GAP | Quyết định | Xử lý trong bộ TC final | Δ TC |
|---|---|---|---:|
| GAP-01 | Vừa chặn nhập vừa thông báo ERR_023 | Item "1001 ký tự" (nhập và copy/paste) ở 6 ô Lý do: chặn tại 1000 / cắt còn 1000 **và** hiển thị ERR_023 dưới ô. Q&A Q32 ghi "user chốt"; REOPEN `HoSoPhapLyCIC-20261012-03` | 0 (sửa 12 TC) |
| GAP-02 | Bổ sung đủ trường hợp = 5 và > 5 | Nhóm scroll của Loại khách hàng, Mã tệp, Nhóm khách hàng, Trạng thái, Ngày báo cáo (M4, M5, M7) có đủ 3 trường hợp; = 5 / > 5 dùng dữ liệu danh mục giả lập | +14 |
| GAP-03 | Bỏ qua C09, C10, K09–K11, K17; bổ sung K04 (có icon x) | Thêm TC "icon x xóa ngày" cho 2 DatePicker khoảng ngày | +2 |
| GAP-04 | Bổ sung TC truy vết tới từng chỉ tiêu | Mỗi chỉ tiêu ở MH-002 (61) và MH-003 (35) có 1 TC: mã, giá trị đang lưu, tooltip, chỉ đọc | +96 |
| GAP-05 | Không thêm TC nhãn Bật/Tắt; bổ sung loading | Thêm TC loading công tắc ở M4, M5, M7 | +3 |
| GAP-06 | Thông báo: Toast "Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang." — tự thoát popup và reload trang sau khi tắt | Sửa TC hai cán bộ cùng xử lý / mở từ danh sách cũ (M4, M5, M7) và TC all-or-nothing hồ sơ đã đổi trạng thái (M7 D10/D11, Q11). Q&A Q06 bổ sung; REOPEN `HoSoPhapLyCIC-20261012-03` | 0 (sửa 8 TC) |
| GAP-07 | Bỏ qua — bổ sung tên bảng thật sau khi thực hiện test | Giữ SQL mẫu | 0 |
| GAP-08 | Giữ nguyên, xác nhận khi chạy thực tế; lệch thì ghi lỗi giao diện | — | 0 |
| GAP-09 | Giữ nguyên; BA phản hồi khác → REOPEN và sửa TC cùng mã Qxx | — | 0 |
| GAP-10 | Giữ TC, bổ sung danh sách điều kiện môi trường vào kế hoạch test | Xem mục "Điều kiện môi trường test" bên dưới | 0 |
| GAP-11 | Bỏ qua | — | 0 |
| GAP-12 | Bổ sung TC mới | M8: phân loại R1–R4 cho tệp D10 và Q11 (8), KH tổ chức mới / đổi MSDN TC011 / chỉ đổi TC007 (3), INF_010 chỉ đếm hồ sơ Chờ xem xét (1); thêm TC011 vào danh mục chỉ tiêu quan trọng của dữ liệu test | +12 |
| **Tổng** | | 1.405 → **1.532** | **+127** |

## Điều kiện môi trường test (GAP-10 — đưa vào kế hoạch test)

| # | Điều kiện | Dùng cho |
|---|---|---|
| 1 | Tài khoản: cbxl01 (ROLE-CBTTXLDL, TCTD 31358001 + 79202501), cbxl02 (ROLE-CBTTXLDL, TCTD 31358001), cbxl03 (ROLE-CBTTXLDL, 0 TCTD), nsd01 (không có quyền chức năng) | Phân quyền, xử lý đồng thời giữa 2 cán bộ |
| 2 | Công cụ/quyền gửi tệp D10, D11, Q11 qua FUNC-XLDL-002 cho đầu mối 31358001, 79202501 | M8 phân loại khi tiếp nhận, INF_010 |
| 3 | Dữ liệu kho TCTD: KH có ≥ 4 phiên bản cùng Mã CIC + đầu mối; phiên bản trùng / trống Ngày báo cáo; KH có hồ sơ của 2 TCTD cùng Mã CIC | BR-032, Q03 |
| 4 | Kho chuẩn CICinfo: hồ sơ có / không cờ C06; KH lệch Loại khách hàng; dữ liệu kho TCTD lệch CICinfo | BR-033, BR-034, BR-047, Q01 |
| 5 | Danh mục chỉ tiêu (FUNC-XLDL-027) đánh dấu quan trọng: TTC04, CN001, CN005, CN006, CN008, CN010, CN016, TC004–TC006, TC011 | ★, phân loại BR-008/009 |
| 6 | Truy cập FUNC-XLDL-013 (cấp mã CIC, danh sách cảnh báo nghi trùng), FUNC-XLDL-035 (xác thực C06), FUNC-WEB-002 (tra cứu báo cáo đã gửi) | BR-005, BR-010, BR-011, liên kết INF_011 |
| 7 | Hộp thư email + thiết bị nhận Push Notification của tài khoản đơn vị cung cấp báo cáo | INF_011 |
| 8 | Mock/proxy API (DevTools, mock server) giả lập lỗi 500, time out, mạng chậm; giả lập lỗi bước C06 / nghi trùng / INF_011 | API states H13–H16, loading, rollback all-or-nothing (Q07) |
| 9 | Danh mục giả lập có 5 và > 10 giá trị cho Loại khách hàng, Mã tệp, Nhóm khách hàng, Trạng thái, Ngày báo cáo | GAP-02 scroll |
| 10 | Dữ liệu > 1.000.000 bản ghi (hoặc giả lập) cho xuất Excel dạng .zip; ≥ 1.000 hồ sơ D11 của 31358001 cho phân trang tới trang 50 | Xuất Excel, phân trang |
| 11 | Tài liệu thiết kế CSDL (tên bảng/cột thật) — bổ sung sau khi test (GAP-07) | SQL đối soát |
