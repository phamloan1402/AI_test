# TC Lead Review Report — Tích hợp Phân quyền dữ liệu tài khoản (16911348)

> Bộ TC: `scripts/gen_tc_tichhopphanquyendulieucic.py` (COMPACT — chưa xuất .xlsx)
> Tổng: **113 TC** — M1 Luồng vào 36 · M2 Phiên & hiển thị 31 · M3 Hiệu lực trên màn Tệp 26 · M4 Vòng đời 20
> Trong đó **9 TC PENDING-Q&A** (chưa có expected result): PQDLTH_015, 016, 017 (Q15) · 047 (Q07) · 089, 090 (Q05) · 091 (Q01) · 092, 093 (Q23)
> Nguồn truy vết: `TichHopPhanQuyenDuLieuCIC_B3_B4.md` (B4 đã duyệt, Event `Tich_hop_Phan_quyen_du_lieu_tai_khoan_16911348-20260930-01`)

## Tóm tắt đánh giá

| Tiêu chí | Trạng thái | Số lượng vấn đề |
|----------|-----------|----------------|
| Coverage | ⚠️ Cần xác nhận | 2 |
| Clarity | ⚠️ Cần sửa | 1 |
| Accuracy | ⚠️ Cần sửa | 4 |
| Feasibility | ⚠️ Cần bổ sung | 2 |
| Organization | ⚠️ Cần sửa | 1 |
| Traceability & RBT | ⚠️ Cần quyết định | 2 |

**Điểm đạt:** 48/48 kịch bản B4 đều có ít nhất 1 TC (bảng phụ lục); mọi TC có test data cụ thể (tài khoản, mã TCTD, ngày N); 100% tiếng Việt có dấu; mọi expected result dựa trên assumption đều gắn nhãn `[Assumption Qxx-A]`; không thêm field/control ngoài SRS; mức ưu tiên Cao dồn vào M1/M3 (kiểm soát truy cập, lộ dữ liệu) và đăng xuất ở M2 đúng đánh giá rủi ro B3.

## Danh sách vấn đề phát hiện

### [GAP-01] — Tham chiếu chéo dùng mã nội bộ không hiển thị trong Excel
- **Tiêu chí:** Organization
- **TC liên quan:** PQDLTH_001–005, 040, 046, 051, 066, 082–084, 095–101, 103–105, 107, 108 (các bước/data ghi "PQDLTH_xxx" hoặc "Sau PQDLTH_xxx")
- **Vấn đề:** Writer đánh số cột ID tự động **lại từ 1 cho mỗi sheet**, mã `PQDLTH_xxx` trong `muc_dich` bị strip. Trong Excel, "Sau PQDLTH_045" không trỏ được tới dòng nào (PQDLTH_045 hiển thị là ID 9 của sheet M2).
- **Đề xuất:** Thay mọi tham chiếu bằng dạng `sheet + ID hiển thị` (VD "Sau TC M2-PhienHienThi #9"). Mình sẽ tự tính lại ID theo thứ tự dòng.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-02] — Không có Nhóm A (6 TC) và section Giao diện ở M2–M4
- **Tiêu chí:** Coverage
- **TC liên quan:** sheet M1 (chỉ có button Phân quyền), M2, M3, M4
- **Vấn đề:** Rule export yêu cầu mỗi sheet mở đầu bằng Nhóm A01–A06. B3 (đã duyệt ở B4) ghi Nhóm A = N/A vì bộ TC tích hợp không có màn hình riêng. Reviewer đọc Excel có thể đánh giá là thiếu.
- **Đề xuất:** Giữ N/A. Thêm 1 dòng ghi chú trong precondition mỗi sheet: "Nhóm A — N/A: giao diện thuộc bộ TC chức năng của từng màn".
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-03] — Expected result có hai khả năng ("hoặc")
- **Tiêu chí:** Accuracy
- **TC liên quan:** PQDLTH_095 (bước 3), PQDLTH_113
- **Vấn đề:** 095 ghi "Không có dữ liệu cũ (hoặc 403 nếu mất quyền chức năng…)"; 113 ghi "ERR-005 … hoặc thông báo dữ liệu đã thay đổi". TC không xác định được Pass/Fail duy nhất.
- **Đề xuất:**
  - 095: cố định dữ liệu. NND_TiepNhan gắn với phòng TT XLDL, nên điều chuyển sẽ thu hồi nhóm này. Expected = trang 403 "Bạn không có quyền truy cập chức năng này." (theo [P11] "thu hồi Nhóm quyền/Nhóm người dùng gắn với Phòng ban cũ").
  - 113: theo Q14-A, kiểm tra "dữ liệu đã thay đổi" trước. Expected = chặn với thông báo dữ liệu đã được cập nhật, yêu cầu tải lại; CSDL có đúng 1 bản ghi 201 - Theo đầu mối.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-04] — Danh sách đầu mối trong bộ lọc ghi chung chung
- **Tiêu chí:** Accuracy
- **TC liên quan:** tc_group "bộ lọc Mã đầu mối chỉ gồm tổ chức trong phạm vi quyền" (PQDLTH_071–074)
- **Vấn đề:** Expected ghi "201, 303 (và đơn vị gửi báo cáo thuộc 201)", không liệt kê cụ thể nên không đo được.
- **Đề xuất:** Liệt kê theo Q22-A: bộ lọc = {201, 79201019, 79201012, 79201017, 303}; không có 310, 01201500, 01203500.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-05] — TC đồng thời dùng tài khoản có quyền đang PENDING
- **Tiêu chí:** Accuracy
- **TC liên quan:** PQDLTH_112
- **Vấn đề:** Phiên B dùng vh.qt, trong khi quyền phân quyền của VHAN đang PENDING Q15. Kết quả có thể là "không mở được màn", thay vì kịch bản đồng thời cần kiểm tra.
- **Đề xuất:** Thêm tài khoản test `pp.ttxldl` (Phó phòng TT XLDL, Vai trò Lãnh đạo phòng — [P0] Luồng 2 "Trưởng phòng/Phó phòng") vào precondition, dùng làm phiên B.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-06] — SQL đối soát dùng tên bảng giữ chỗ / thiếu SQL
- **Tiêu chí:** Accuracy / Coverage (CHECK 14)
- **TC liên quan:** tc_group "bộ lọc phân quyền dữ liệu khớp phân loại quản lý đã lưu" (PQDLTH_057–060)
- **Vấn đề:** CHECK 14 yêu cầu SQL mẫu cho ca tra cứu BIZ. SRS không có tên bảng quyền dữ liệu/người dùng, nên 057 dùng `<bảng … theo thiết kế DB>` (placeholder), còn 058–060 chưa có SQL.
- **Đề xuất:** (a) DEV cung cấp tên bảng/cột thì mình điền SQL cho cả 4 item; hoặc (b) bỏ SQL, ghi "Đối soát CSDL theo thiết kế DB — SRS chưa công bố schema".
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-07] — Precondition M4 thiếu điều kiện môi trường cho kịch bản theo ngày
- **Tiêu chí:** Feasibility
- **TC liên quan:** PQDLTH_094–099, 102–105
- **Vấn đề:** Các TC cần chờ tới ngày N+1, hoặc cần yêu cầu có Ngày hiệu lực quá khứ (N−3, N−4) và job tự động chạy. Precondition chưa nêu cách thực hiện trên môi trường test.
- **Đề xuất:** Thêm vào PRECOND_M4: "Môi trường test cho phép chạy thủ công job cập nhật điều chuyển / tự động từ chối và tạo dữ liệu yêu cầu có Ngày hiệu lực quá khứ (qua DB seed)". Nếu môi trường không hỗ trợ thì cần DEV hỗ trợ.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-08] — Dữ liệu test "NND_TiepNhan", "NND_KiemTraNoiDung" là tên giả định
- **Tiêu chí:** Feasibility
- **TC liên quan:** PQDLTH_018, 020, 021, 083, 084, 106–108, 110
- **Vấn đề:** SRS không đặt tên Nhóm người dùng. Mình đặt tên để test data cụ thể, và tester cần tạo các nhóm này trước.
- **Đề xuất:** Thêm vào PRECOND_BASE: "Tạo Nhóm người dùng NND_TiepNhan (chức năng 4 màn Tệp) và NND_KiemTraNoiDung (Kiểm tra nội dung tệp báo cáo), loại Trong CIC, trạng thái Hoạt động".
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-09] — Data test tham chiếu mơ hồ
- **Tiêu chí:** Clarity
- **TC liên quan:** PQDLTH_056
- **Vấn đề:** Data ghi "Tài khoản có 5 bản ghi (PQDLTH item 5 bản ghi)", không rõ trỏ tới đâu.
- **Đề xuất:** Ghi rõ: "cb.a có 5 bản ghi: 201, 303, 310 - Theo đầu mối; 01201500, 01203500 - Theo chi nhánh".
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-10] — Xử lý 9 TC PENDING-Q&A khi xuất Excel
- **Tiêu chí:** Traceability & RBT
- **TC liên quan:** PQDLTH_015, 016, 017, 047, 089, 090, 091, 092, 093
- **Vấn đề:** Các TC này có bước và data nhưng expected result là "PENDING-Q&A …". Nếu xuất vào Excel, tester có thể chạy nhầm; nếu bỏ đi, sẽ mất dấu vết kịch bản rủi ro cao.
- **Đề xuất:** (a) Giữ trong Excel và đặt Mức độ = Cao, tester bỏ qua đến khi BA trả lời (khuyến nghị); hoặc (b) tách khỏi Excel, chỉ giữ trong báo cáo này.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-11] — Không có mã SC/BR trong Excel
- **Tiêu chí:** Traceability & RBT
- **TC liên quan:** toàn bộ
- **Vấn đề:** Writer không có cột Ghi chú/Requirement ID. Truy vết TC → SC/BR chỉ nằm trong phụ lục dưới đây.
- **Đề xuất:** (a) Giữ truy vết ở phụ lục báo cáo này (không đổi template); hoặc (b) thêm hậu tố `[SC-Mx-yy]` vào cột Trường hợp kiểm thử.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

### [GAP-12] — BR-OUT-17 chưa phủ màn (4) cho ca "nhập thẳng tên tệp"
- **Tiêu chí:** Coverage
- **TC liên quan:** tc_group "không trả tệp ngoài phạm vi khi nhập thẳng tên tệp" (075–077)
- **Vấn đề:** Chỉ có 3 màn (1)–(3). Trang [P16] không có câu "kể cả khi nhập thẳng tên tệp", chỉ nói bộ lọc Mã đầu mối bị giới hạn.
- **Đề xuất:** Bỏ qua cho màn (4), vì SRS không quy định và Q23 ⚠️ đang chờ BA. Ghi lý do tại đây.
- **Hành động:** [ ] Bổ sung TC mới  [ ] Sửa TC hiện có  [ ] Bỏ qua (ghi lý do)

## Phụ lục — Truy vết TC ↔ Kịch bản B4

| Kịch bản | TC | Kịch bản | TC |
|---|---|---|---|
| SC-M1-01 | 001, 002, 003 | SC-M2-07 | 048–050, 051 |
| SC-M1-02 | 006–010 | SC-M2-08 | 052–054, 055, 056 |
| SC-M1-03 | 011–014 | SC-M2-09 | 057–060 |
| SC-M1-04 | 005 | SC-M2-10 | 061–064 |
| SC-M1-05 (PENDING) | 015, 016, 017 | SC-M2-11 | 065, 066 |
| SC-M1-06 | 004 | SC-M2-12 | 067 |
| SC-M1-07 | 018, 019 | SC-M3-01/02/03 | 068, 069, 070 |
| SC-M1-08 | 020 | SC-M3-04 | 071–074, 075–077 |
| SC-M1-09 | 021 | SC-M3-05 | 078 |
| SC-M1-10 | 022 | SC-M3-06 | 079, 080 |
| SC-M1-11 | 023–025 | SC-M3-07 | 083, 084 |
| SC-M1-12 | 026, 027 | UC-05 (chuyển quyền trên màn Tệp) | 081, 082 |
| SC-M1-13 | 028–032, 033 | SC-M3-08 | 085–088 |
| SC-M1-14 | 034, 035 | SC-M3-09 (PENDING) | 089, 090 |
| SC-M1-15 | 036 | SC-M3-10 (PENDING) | 091 |
| SC-M2-01 | 037, 038, 039, 040 | SC-M3-11 (PENDING) | 092, 093 |
| SC-M2-02 | 041, 044 | SC-M4-01 | 094, 095 |
| SC-M2-03 | 042, 043 | SC-M4-02 | 096 |
| SC-M2-04 | 045 | SC-M4-03 | 097–099 |
| SC-M2-05 | 046 | SC-M4-04 | 100, 101 |
| SC-M2-06 (PENDING) | 047 | SC-M4-05 | 102, 103 |
|  |  | SC-M4-06 | 104, 105 |
|  |  | SC-M4-07 | 106, 107, 108 |
|  |  | SC-M4-08 | 109 |
|  |  | SC-M4-09 | 112, 113 |
|  |  | SC-M4-10 | 110, 111 |

## Hướng dẫn xác nhận
1. Đọc từng GAP trong danh sách trên.
2. Tích vào checkbox [x] cho hành động bạn muốn thực hiện.
3. Với hành động "Bỏ qua": điền lý do vào dòng đó.
4. Với hành động "Bổ sung TC mới": có thể ghi thêm gợi ý nội dung TC cần sinh.
5. Khi đã xử lý xong toàn bộ GAP, reply: **"Đã review xong, tiến hành sinh bộ TC final"**
