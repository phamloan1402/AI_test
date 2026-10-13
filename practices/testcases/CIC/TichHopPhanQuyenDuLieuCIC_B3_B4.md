# Tích hợp Phân quyền dữ liệu tài khoản (16911348) — B3 Phân rã & B4 Truy vết

> Pipeline: `TichHopPhanQuyenDuLieuCIC` · Mã TC: `PQDLTH_###` · Q&A: `practices/Q&A/PhanQuyenDuLieuCIC_QA.md` (assumptions đã chấp thuận 2026-09-30)
> Ký hiệu nguồn giữ nguyên như file Q&A: [P0] 16911267 · [P1] 16911348 · [P2] 34800037 · [P3] 34799907 · [P4] 34799997 · [P5] 16911306 · [P6] 16911309 · [P7] 16911299 · [P8] 16911312 · [P9] 16911337 · [P10] 16911185 · [P11] 16911420 · [P12] 34815209 · [P13] 16909447 · [P14] 26968323 · [P15] 26968066 · [P16] 16911912
> `PENDING-Q&A` = kịch bản giữ chỗ, chưa có expected result cho tới khi BA/PO trả lời Q-ID có ⚠️.

---

## B3a — Phân rã module & dependency

| Module | Mô tả | Risk | Phụ thuộc |
|---|---|---|---|
| **M1 — Luồng vào: điều kiện mở & dữ liệu nguồn** | Chức năng khác quyết định 16911348 được mở cho tài khoản nào, bởi ai, và nạp dữ liệu gì (thông tin người dùng, cây chức năng, danh sách TCTD, danh sách tài khoản nhận) | **High** (kiểm soát truy cập) | [P7] Tra cứu, [P0] Activity, [P5]/[P6] tài khoản, [P9]/[P10] trạng thái, [P11]/[P12] điều chuyển, NV16 |
| **M2 — Luồng ra: phiên & hiển thị ở quản lý người dùng** | Sau khi Lưu/Chuyển ở 16911348: đăng xuất tài khoản bị ảnh hưởng; dữ liệu phản ánh ở Tra cứu (chip, bộ lọc), Xem chi tiết (TCTD đã chọn, Lịch sử), Phê duyệt | **High** (đăng xuất) / Medium (hiển thị) | M1 (mở được màn), [P7], [P8], [P9] |
| **M3 — Luồng ra: hiệu lực trên màn áp dụng** | Mỗi thao tác ở 16911348 (thêm/sửa/xóa/chuyển) thay đổi đúng bộ lọc Mã đầu mối, kết quả và nút hành động trên 4 màn Tệp | **High** (lộ/chặn nhầm dữ liệu) | M2 (đăng xuất → đăng nhập lại), [P2], [P13]–[P16] |
| **M4 — Vòng đời liên chức năng** | Điều chuyển, Hết hiệu lực/Hiệu lực, thu hồi quyền chức năng, TCTD đổi trạng thái, thao tác đồng thời tác động lên quyền dữ liệu đã lưu | **High** | M1–M3, [P10], [P11], [P12], [P6] |

**Chuỗi phụ thuộc:** tạo tài khoản ([P5]) → phê duyệt Hoạt động ([P9]) → **M1** mở Phân quyền → Lưu → **M2** đăng xuất / hiển thị → **M3** hiệu lực trên màn Tệp → **M4** sự kiện vòng đời làm thay đổi kết quả của M2/M3.

---

## B3b — Field Inventory (điểm tích hợp) & Common TC mapping

> Chỉ liệt kê control tham gia tích hợp. Validate UI đầy đủ của từng control thuộc bộ TC chức năng của trang sở hữu (đã loại khỏi scope ở B1).

### 3b.1 Field Inventory

| Module | Điểm/Control | Màn sở hữu | Loại | Vai trò trong tích hợp | Nguồn |
|---|---|---|---|---|---|
| M1 | Nút **Phân quyền** (menu Thao tác) | Tra cứu người dùng | BUTTON | Cổng vào 16911348; hiện theo trạng thái tài khoản | [P7] |
| M1 | Danh sách người dùng | Tra cứu người dùng | GRID | Tập tài khoản người thao tác nhìn thấy (theo vai trò) | [P7] |
| M1 | 15 trường Thông tin người dùng (Họ tên … Nhóm người dùng) | MH-1 | LABEL | Phải khớp dữ liệu tài khoản ở [P5]/[P6] | [P1], [P5], [P6] |
| M1 | Phân hệ | MH-2 | DROPDOWN | Nguồn = Quản lý chức năng (4 phân hệ, không Web Portal) | [P1] |
| M1 | Chức năng / Cây chức năng | MH-2 | DROPDOWN+SEARCH / TREE | Nguồn = Nhóm quyền của tài khoản được phân quyền | [P1], [P5] |
| M1 | Tổ chức tín dụng + danh sách trái | MH-2 | MULTISELECT+SEARCH / GRID | Nguồn = NV16 theo chế độ Phân quyền theo | [P1] |
| M1 | Chọn tài khoản nhận | MH-3 | DROPDOWN+SEARCH | Nguồn = người dùng Đang hoạt động, cùng Phòng ban hiện hành, trừ tài khoản nguồn | [P1], [P6], [P11] |
| M2 | Thông báo đăng xuất | Toàn hệ thống | MESSAGE | "Đã có thông tin quyền dữ liệu được cập nhật. Vui lòng đăng nhập lại" | [P1] |
| M2 | Cột **Phân quyền dữ liệu** (chip) | Tra cứu người dùng | CHIP | Hiển thị bản ghi đã lưu | [P7] |
| M2 | Bộ lọc Phân quyền dữ liệu – Loại quản lý / Tổ chức | Tra cứu người dùng | MULTISELECT+SEARCH | Lọc theo Phân loại đã lưu | [P7] |
| M2 | Danh sách TCTD đã chọn | Xem chi tiết người dùng | GRID | Hiển thị bản ghi đã lưu | [P8] |
| M2 | Lịch sử cập nhật | Xem chi tiết người dùng | GRID | Ghi nhận thay đổi quyền (Q17 assumption) | [P8] |
| M2 | Mục Phân quyền dữ liệu | Phê duyệt người dùng | LABEL/GRID | Hiển thị theo mô hình 16911348 | [P9] |
| M3 | Bộ lọc Mã đầu mối | 4 màn Tệp | MULTISELECT+SEARCH | Chỉ TCTD trong phạm vi | [P13]–[P16] |
| M3 | Grid kết quả (cột Mã đầu mối) | 4 màn Tệp | GRID | Không trả tệp ngoài phạm vi | [P13]–[P16] |
| M3 | Nút Tiếp nhận / Từ chối | M1, M3 màn Tệp | BUTTON | Ẩn khi không có hành động | [P13], [P15] |
| M3 | Nút Di chuyển tệp / Gán nhãn tệp | Tiếp nhận tệp phi cấu trúc | BUTTON | Disabled + tooltip khi không có hành động | [P15] |
| M3 | Nút Chấp nhận / Từ chối cả file | Kiểm tra nội dung tệp | BUTTON | Theo hành động (Q05 ⚠️) | [P16] |
| M4 | (không có control mới — dùng lại control của M1–M3) | — | — | — | — |

### 3b.2 Nhóm Common TC

| Nhóm | Áp dụng? | Field / Lý do |
|---|---|---|
| A — Giao diện chung | **N/A** | Bộ TC tích hợp không có màn hình riêng; A01–A06 của MH-1…MH-4, Tra cứu, Xem chi tiết, 4 màn Tệp thuộc bộ TC chức năng của từng màn (đã loại ở B1) |
| C — Grid + Paging | **N/A** | Chỉ kiểm tra **nội dung** grid sau tích hợp (BIZ), không kiểm tra hành vi grid |
| H / J — Dropdown / Multi-select | **N/A (UI)** | Chỉ kiểm tra **tập option** do chức năng khác cung cấp (BIZ): Chọn tài khoản nhận, Chức năng, TCTD, bộ lọc Mã đầu mối, bộ lọc Loại quản lý/Tổ chức |
| M — Button | ✅ | Nút **Phân quyền** ở Tra cứu (3 TC: hiển thị theo trạng thái / trạng thái / onclick mở MH-1). Các nút khác chỉ kiểm tra ẩn/hiện theo quyền (thuộc S) |
| S — Phân quyền chức năng | ✅ | S01/S02 cho: mở Phân quyền (M1); nút hành động trên màn Tệp (M3) |
| W3 — Status Badge | **N/A** | Không kiểm tra badge; trạng thái TCTD chỉ kiểm tra giá trị (BIZ) |
| D, E, F, G, I, K, L, N, O, P, Q, R, T, U, V | **N/A** | Không có trường nhập/ xóa / upload / import / tra cứu đa trường thuộc scope tích hợp |

### 3b.3 Kỹ thuật thiết kế sẽ dùng ở B5
- **State Transition:** trạng thái tài khoản × nút Phân quyền; vòng đời nhóm quyền (chưa có → đã lưu → sửa → xóa / chuyển); điều chuyển (Chờ duyệt → Chờ hiệu lực → Đã duyệt / Từ chối).
- **Decision Table:** chế độ Phân quyền theo × loại mã (3 số / 8 số tự báo cáo / 8 số báo cáo qua đầu mối) → Phân loại lưu → phạm vi tệp hiển thị.
- **EP:** danh sách tài khoản nhận (Đang hoạt động/không; cùng/khác phòng; nguồn; đang chờ điều chuyển).
- **BVA:** số chip 3 / 4 (+N); điều chuyển tự từ chối đúng 03 ngày / hơn 03 ngày.

---

## B4 — Ma trận truy vết 4 tầng

### Tầng 1 — Functional / Use case ↔ Module ↔ Tiêu chí nghiệm thu

| UC | Mô tả | Module | Tiêu chí nghiệm thu | Nguồn |
|---|---|---|---|---|
| UC-01 | Mở màn Phân quyền dữ liệu từ Tra cứu người dùng | M1 | Chỉ tài khoản Hoạt động có nút Phân quyền; mở đúng MH-1 của tài khoản chọn | [P7], [P1] |
| UC-02 | Nạp dữ liệu nguồn vào MH-1/MH-2/MH-3 | M1 | Thông tin, cây chức năng, danh sách TCTD, danh sách tài khoản nhận lấy đúng nguồn | [P1], [P5], [P6] |
| UC-03 | Lưu thay đổi quyền → đăng xuất tài khoản bị ảnh hưởng | M2 | Mọi phiên bị đăng xuất kèm thông báo; không đổi thì không đăng xuất | [P1] |
| UC-04 | Hiển thị quyền đã lưu ở Tra cứu / Xem chi tiết / Phê duyệt | M2 | Chip, bộ lọc, danh sách TCTD, lịch sử khớp CSDL | [P7], [P8], [P9] |
| UC-05 | Chuyển nhóm quyền sang tài khoản khác | M2, M3 | Nguồn mất nhóm, nhận có nhóm; trùng → ERR-005 chặn toàn bộ | [P1] |
| UC-06 | Quyền đã lưu có hiệu lực trên màn Tệp | M3 | Bộ lọc, kết quả, nút hành động đúng phạm vi mới | [P2], [P13]–[P16] |
| UC-07 | Sự kiện vòng đời tác động quyền dữ liệu | M4 | Điều chuyển xóa quyền; Không hoạt động/Hiệu lực lại; thu hồi quyền chức năng | [P10], [P11], [P12] |

### Tầng 2 — Business Rule & mã thông báo (1 dòng / BR)

| BR | Nội dung | Nguồn | Q-ID | Kịch bản |
|---|---|---|---|---|
| BR-IN-01 | Nút Phân quyền chỉ có ở trạng thái **Hoạt động** | [P7] ma trận Thao tác | — | SC-M1-01 |
| BR-IN-02 | Không có nút Phân quyền ở Tạo mới, Chờ lãnh đạo duyệt, Chờ lãnh đạo duyệt hết hiệu lực, Chờ lãnh đạo duyệt hiệu lực, Không hoạt động | [P7] | — | SC-M1-02 |
| BR-IN-03 | Tập tài khoản người thao tác nhìn thấy ở Tra cứu: LĐ phòng — tài khoản trong phòng; Cán bộ — chính mình; phòng VHAN, LĐ đơn vị (BLĐ) — toàn bộ | [P7] | — | SC-M1-03 |
| BR-IN-04 | Người phân quyền dữ liệu là Trưởng/Phó phòng của phòng tài khoản | [P0] Luồng 2 | Q15 ⚠️ | SC-M1-04, SC-M1-05 (PENDING) |
| BR-IN-05 | Tài khoản chỉ được phân quyền dữ liệu sau khi được phê duyệt thành Hoạt động | [P0] Activity 4–6, [P9] | — | SC-M1-06 |
| BR-IN-06 | 15 trường Thông tin người dùng ở MH-1 khớp dữ liệu tài khoản (kể cả sau khi Cập nhật người dùng) | [P1] MH-1, [P5], [P6] | — | SC-M1-07 |
| BR-IN-07 | Cây chức năng MH-2 = chức năng tài khoản **được phân quyền** truy cập theo Nhóm quyền – Nhóm người dùng, không phải của người thao tác | [P1] MH-2, [P5] | — | SC-M1-08 |
| BR-IN-08 | Đổi Nhóm người dùng của tài khoản → cây chức năng MH-2 đổi theo | [P1], [P6] | Q12 | SC-M1-09 |
| BR-IN-09 | Phân hệ = 4 phân hệ level 1 khai báo ở Quản lý chức năng, không có Web Portal | [P1] | — | SC-M1-10 |
| BR-IN-10 | Danh sách TCTD: Theo đầu mối = mã 3 số; Theo chi nhánh = ORG_REPORTING_CODE 8 số; Theo tất cả = toàn bộ NV16 | [P1] | Q20 (A) | SC-M1-11 |
| BR-IN-11 | Lưu phân quyền kiểm tra Trạng thái TCTD; không hợp lệ → thông báo lỗi | [P0] bước 8, 10 | Q11 (A), Q13 (A) | SC-M1-12 |
| BR-IN-12 | Tài khoản nhận: Đang hoạt động, cùng Phòng ban hiện hành, loại trừ tài khoản nguồn, hiển thị "Tài khoản - Họ & tên" | [P1] MH-3 | — | SC-M1-13 |
| BR-IN-13 | Tài khoản nhận xét theo Phòng ban hiện hành — không tính yêu cầu điều chuyển chưa tới Ngày hiệu lực | [P1] MH-3, [P11] | — | SC-M1-14 |
| BR-IN-14 | Đổi Phòng ban tài khoản qua Cập nhật người dùng → danh sách tài khoản nhận theo phòng mới | [P1], [P6] | — | SC-M1-15 |
| BR-OUT-01 | Lưu MH-1 có thay đổi (thêm/sửa/xóa nhóm) → tài khoản bị ảnh hưởng bị đăng xuất **toàn bộ** phiên | [P1] MH-2, MH-4 | — | SC-M2-01 |
| BR-OUT-02 | Lưu MH-1 **không** có thay đổi → không đăng xuất | [P1] MH-2 | — | SC-M2-02 |
| BR-OUT-03 | Cập nhật/Xóa chỉ ghi CSDL khi Lưu MH-1; Hủy MH-1 → không ghi, không đăng xuất | [P1] | Q06 (A) | SC-M2-03 |
| BR-OUT-04 | Sao chép ghi CSDL ngay khi Lưu MH-3; tài khoản nhận nhận nhóm và bị đăng xuất | [P1] MH-3 | Q06 (A) | SC-M2-04 |
| BR-OUT-05 | Sao chép: nhóm bị xóa khỏi tài khoản nguồn | [P1] MH-3 | — | SC-M2-05 |
| BR-OUT-06 | Sao chép: tài khoản nguồn có bị đăng xuất | [P1] | Q07 ⚠️ | SC-M2-06 (PENDING) |
| BR-OUT-07 | Sao chép trùng (toàn bộ hoặc một phần) với tài khoản nhận → ERR-005, không ghi phần nào, nguồn giữ nguyên | [P1] MH-3 | — | SC-M2-07 |
| BR-OUT-08 | Tài khoản nhận thiếu quyền chức năng → bản ghi quyền dữ liệu vẫn lưu đủ nhưng chưa xem được; được cấp quyền chức năng sau → tự có hiệu lực | [P1] MH-3 | — | SC-M3-07 |
| BR-OUT-09 | Tra cứu: chip "<Mã TCTD> - <Phân loại quản lý>", Theo đầu mối trước rồi Mã tăng dần; tối đa 3 chip + "+N"; hover/click "+N" → popover đầy đủ | [P7] | — | SC-M2-08 |
| BR-OUT-10 | Tra cứu: bộ lọc Loại quản lý/Tổ chức khớp Phân loại đã lưu (kể cả mã 3 số gán qua Theo tất cả = Theo chi nhánh); không chọn → gồm cả tài khoản không có phân quyền dữ liệu | [P7] | — | SC-M2-09 |
| BR-OUT-11 | Xem chi tiết: Danh sách TCTD đã chọn (Mã, Tên, Phân loại, Trạng thái) khớp CSDL | [P8] | — | SC-M2-10 |
| BR-OUT-12 | Xem chi tiết: Lịch sử cập nhật ghi 1 dòng mỗi lần Lưu thay đổi quyền (Hành động = Chỉnh sửa) | [P8] | Q17 (A) | SC-M2-11 |
| BR-OUT-13 | Phê duyệt: mục Phân quyền dữ liệu hiển thị chức năng theo TCTD và Phân loại theo mô hình 16911348 | [P9] | Q16 (A) | SC-M2-12 |
| BR-OUT-14 | Màn Tệp — "X – Theo đầu mối": tệp có Mã đầu mối = X hoặc đơn vị có ORG_REPORTING_CODE = X | [P2] ví dụ | Q22 (A) | SC-M3-01 |
| BR-OUT-15 | Màn Tệp — "Y – Theo chi nhánh": chỉ tệp có Mã đầu mối = Y | [P2] | — | SC-M3-02 |
| BR-OUT-16 | Màn Tệp — "Z – Theo chi nhánh" gán qua Theo tất cả (Z mã 3 số): chỉ đúng Z, không phủ chi nhánh con | [P1] | Q22 (A) | SC-M3-03 |
| BR-OUT-17 | Bộ lọc Mã đầu mối chỉ gồm TCTD trong phạm vi; kết quả không trả tệp ngoài phạm vi kể cả nhập thẳng tên tệp | [P13]–[P16] | — | SC-M3-04 |
| BR-OUT-18 | Xóa nhóm quyền → sau đăng nhập lại không còn thấy tệp của các TCTD trong nhóm | [P1] MH-4 (popup "không được truy cập quyền dữ liệu đã thiết lập") | — | SC-M3-05 |
| BR-OUT-19 | Sửa nhóm (thêm/bớt TCTD hoặc hành động) → sau đăng nhập lại phạm vi đổi đúng | [P1] MH-2 | — | SC-M3-06 |
| BR-OUT-20 | Không có hành động ở cấp chức năng: Tiếp nhận/Từ chối ẩn; Di chuyển tệp/Gán nhãn disabled + tooltip | [P13], [P15] | — | SC-M3-08 |
| BR-OUT-21 | Có hành động ở TCTD A nhưng không ở TCTD B | [P1] | Q05 ⚠️ | SC-M3-09 (PENDING) |
| BR-OUT-22 | Một TCTD thuộc 2 nhóm (Theo đầu mối + Theo chi nhánh qua Theo tất cả) | [P1], [P7] | Q01 ⚠️ | SC-M3-10 (PENDING) |
| BR-OUT-23 | Xuất Excel/In, truy cập trực tiếp tệp ngoài phạm vi | [P13] | Q23 ⚠️ | SC-M3-11 (PENDING) |
| BR-LC-01 | Điều chuyển đến Ngày hiệu lực → cập nhật Phòng ban, thu hồi Nhóm quyền/Nhóm người dùng cũ, **xóa toàn bộ** quyền dữ liệu | [P11], [P12] | — | SC-M4-01 |
| BR-LC-02 | Xóa quyền do điều chuyển → đăng xuất toàn bộ phiên | [P1] MH-4 | Q16 (A) | SC-M4-02 |
| BR-LC-03 | Điều chuyển bị Từ chối thủ công hoặc tự động sau 03 ngày → quyền dữ liệu giữ nguyên | [P11] | — | SC-M4-03 |
| BR-LC-04 | Sau điều chuyển, LĐ phòng mới phân quyền lại; nhóm cũ không còn | [P11], [P12] | — | SC-M4-04 |
| BR-LC-05 | Hết hiệu lực → Không hoạt động → đăng xuất mọi thiết bị; nút Phân quyền biến mất; quyền dữ liệu giữ nguyên | [P10], [P7] | Q16 (A) | SC-M4-05 |
| BR-LC-06 | Hiệu lực lại → Hoạt động → quyền dữ liệu cũ có hiệu lực lại; nút Phân quyền xuất hiện | [P10], [P7] | Q16 (A) | SC-M4-06 |
| BR-LC-07 | Thu hồi quyền chức năng → hành động đã phân quyền dữ liệu vẫn lưu/hiển thị ở MH-1 nhưng không có tác dụng trên màn Tệp; cấp lại → tự có hiệu lực | [P1] MH-3, [P6] | Q12 (A) | SC-M4-07 |
| BR-LC-08 | TCTD bị hủy kích hoạt sau khi phân quyền → vẫn giữ trong nhóm, hiển thị trạng thái thực tế | NV16 | Q11 (A) | SC-M4-08 |
| BR-LC-09 | Hai người cùng sửa quyền một tài khoản → người Lưu sau bị chặn, phải tải lại | — | Q14 (A) | SC-M4-09 |
| BR-LC-10 | Thay đổi Nhóm người dùng/Phòng ban/Vai trò có hiệu lực ở lần truy vấn kế tiếp | [P6] | Q24 (A) | SC-M4-10 |

**Mã thông báo ↔ kịch bản:**

| Mã / nội dung | Nguồn | Kịch bản |
|---|---|---|
| ERR-005 "Mã <X> - <Phân loại> đã tồn tại. Vui lòng kiểm tra lại." (khi Sao chép trùng với tài khoản nhận) | [P1] MH-3 | SC-M2-07 |
| "Đã có thông tin quyền dữ liệu được cập nhật. Vui lòng đăng nhập lại" | [P1] MH-4 | SC-M2-01, SC-M2-04, SC-M4-02 |
| "Không tìm thấy bản ghi phù hợp" (Tra cứu, màn Tệp) | [P7], [P13] | SC-M2-09, SC-M3-04 |
| Trang 403 "Bạn không có quyền truy cập chức năng này." | [P13]–[P15] | SC-M1-05 (PENDING), SC-M4-07 |
| Tooltip "Bạn không có quyền thực hiện thao tác này." | [P15] | SC-M3-08 |
| Thông báo lỗi kiểm tra thông tin phân quyền (chưa có mã) | [P0] bước 10 | SC-M1-12 (expected theo Q13 assumption: BUS-70 inline — ghi rõ "chưa có mã trong SRS") |
| BUS-238 (chọn nhiều tệp khác trạng thái) | [P13] | Ngoài scope tích hợp (thuộc bộ TC màn Tiếp nhận) |

### Tầng 3 — Ma trận phân quyền (RBAC)

| Thao tác | LĐ phòng — tài khoản cùng phòng | LĐ phòng — tài khoản phòng khác | Phòng VHAN | LĐ đơn vị (BLĐ) | Cán bộ | Không có quyền chức năng Phân quyền |
|---|---|---|---|---|---|---|
| Thấy tài khoản ở Tra cứu | ✅ | ❌ (không hiển thị) | ✅ | ✅ | Chỉ chính mình | — |
| Nút Phân quyền (tài khoản Hoạt động) | ✅ | ❌ (không thấy dòng) | PENDING Q15 | PENDING Q15 | PENDING Q15 (tự phân quyền) | ❌ ẩn; URL trực tiếp → PENDING Q15 |
| Lưu thay đổi ở MH-1 | ✅ | ❌ | PENDING Q15 | PENDING Q15 | PENDING Q15 | ❌ |
| Sao chép sang tài khoản cùng phòng | ✅ | ❌ | PENDING Q15 | PENDING Q15 | PENDING Q15 | ❌ |
| Xem dữ liệu Tệp sau khi được phân quyền (tài khoản bị tác động) | Theo Q03 ⚠️ (ngoài scope — pipeline KTPQDL) | — | — | Toàn bộ (không phụ thuộc 16911348) | Theo nhóm quyền đã lưu | — |

Kịch bản RBAC: SC-M1-03 (tập tài khoản nhìn thấy), SC-M1-04 (LĐ phòng cùng phòng — được), SC-M1-05 (vai trò khác / không quyền — PENDING Q15).

### Tầng 4 — State machine, NFR & thành phần dùng chung

**Trạng thái tài khoản × nút Phân quyền** ([P0] State Machine, [P7]):

| Trạng thái | Nút Phân quyền | Chuyển tiếp liên quan | Kịch bản |
|---|---|---|---|
| Tạo mới | ❌ | → Chờ lãnh đạo duyệt (gửi duyệt) | SC-M1-02 |
| Chờ lãnh đạo duyệt | ❌ | → Hoạt động (phê duyệt) → nút xuất hiện; → Tạo mới (từ chối) | SC-M1-02, SC-M1-06 |
| Hoạt động | ✅ | → Không hoạt động (hết hiệu lực không duyệt) / → Chờ duyệt hết hiệu lực | SC-M1-01, SC-M4-05 |
| Chờ lãnh đạo duyệt hết hiệu lực | ❌ | → Không hoạt động / → Hoạt động (từ chối) | SC-M1-02 |
| Chờ lãnh đạo duyệt hiệu lực | ❌ | → Hoạt động / → Không hoạt động (từ chối) | SC-M1-02 |
| Không hoạt động | ❌ | → Hoạt động (hiệu lực không duyệt) | SC-M1-02, SC-M4-06 |

**Vòng đời nhóm quyền dữ liệu:** Chưa có → (Lưu MH-1) Đã lưu → (Sửa + Lưu MH-1) Đã lưu v2 → (Xóa + Lưu MH-1) Không còn · Đã lưu → (Sao chép) Thuộc tài khoản nhận · Đã lưu → (Điều chuyển tới Ngày hiệu lực) Không còn · Chuyển tiếp **không hợp lệ**: Sao chép nhóm chưa lưu (nút disabled — thuộc bộ TC chức năng 16911348), Sao chép trùng → giữ nguyên (SC-M2-07).

**Điều chuyển** ([P12]): Chờ duyệt → Đã duyệt / Chờ hiệu lực → (Ngày hiệu lực) xóa quyền · Chờ duyệt → Từ chối (thủ công / tự động sau 03 ngày) → giữ quyền. Kịch bản SC-M4-01…04.

**NFR:** đăng xuất đa thiết bị (≥ 2 trình duyệt) — SC-M2-01; không có SLA/hiệu năng trong nguồn → N/A; Responsive → N/A (thuộc bộ TC từng màn).
**Thành phần dùng chung:** chip + popover "+N" ([P7]) — SC-M2-08; Lịch sử cập nhật ([P8]) — SC-M2-11; Xuất Excel của Tra cứu người dùng — N/A (danh sách cột xuất theo Cài đặt hiển thị, [P7] không nêu cột Phân quyền dữ liệu có trong Cài đặt hiển thị → không test nội dung chip trong file xuất).

---

## B4 — High-Level Scenarios

| ID | Module | Loại | Kịch bản | BR |
|---|---|---|---|---|
| SC-M1-01 | M1 | Happy | Tài khoản Hoạt động có nút Phân quyền; click mở MH-1 đúng tài khoản | BR-IN-01 |
| SC-M1-02 | M1 | Exception | 5 trạng thái còn lại không có nút Phân quyền (1 TC/trạng thái) | BR-IN-02 |
| SC-M1-03 | M1 | RBAC | LĐ phòng chỉ thấy tài khoản phòng mình; Cán bộ chỉ thấy mình; VHAN/BLĐ thấy toàn bộ | BR-IN-03 |
| SC-M1-04 | M1 | RBAC-Happy | LĐ phòng phân quyền dữ liệu cho cán bộ cùng phòng thành công | BR-IN-04 |
| SC-M1-05 | M1 | RBAC | VHAN/BLĐ/Cán bộ tự phân quyền/không có quyền chức năng (PENDING Q15) | BR-IN-04 |
| SC-M1-06 | M1 | State | Tài khoản vừa được phê duyệt (Chờ lãnh đạo duyệt → Hoạt động) xuất hiện nút Phân quyền | BR-IN-05 |
| SC-M1-07 | M1 | Data | MH-1 hiển thị đúng 15 trường; sau khi Cập nhật người dùng (đổi Email, Chức vụ) MH-1 hiển thị giá trị mới | BR-IN-06 |
| SC-M1-08 | M1 | Data | Cây chức năng theo Nhóm quyền của tài khoản được phân quyền (người thao tác có nhiều chức năng hơn — không hiện chức năng thừa) | BR-IN-07 |
| SC-M1-09 | M1 | Data | Đổi Nhóm người dùng của tài khoản → cây chức năng MH-2 đổi theo | BR-IN-08 |
| SC-M1-10 | M1 | Data | Dropdown Phân hệ = 4 phân hệ, không có Web Portal | BR-IN-09 |
| SC-M1-11 | M1 | Decision table | 3 chế độ trả đúng tập TCTD (201 / 01201500 / mọi mã) | BR-IN-10 |
| SC-M1-12 | M1 | Exception | Lưu với TCTD không còn Kích hoạt → chặn, thông báo lỗi | BR-IN-11 |
| SC-M1-13 | M1 | EP | Danh sách tài khoản nhận: chỉ Đang hoạt động, cùng phòng, không có tài khoản nguồn, định dạng "Tài khoản - Họ & tên" (5 lớp: hợp lệ, khác phòng, không hoạt động, nguồn, trạng thái chờ) | BR-IN-12 |
| SC-M1-14 | M1 | Alternate | Tài khoản cùng phòng có yêu cầu điều chuyển Chờ hiệu lực vẫn nằm trong danh sách nhận; tài khoản sắp chuyển đến chưa nằm | BR-IN-13 |
| SC-M1-15 | M1 | Alternate | Đổi Phòng ban tài khoản nhận qua Cập nhật người dùng → danh sách nhận đổi theo | BR-IN-14 |
| SC-M2-01 | M2 | Happy / NFR | Thêm nhóm → Lưu MH-1 → tài khoản đích đang đăng nhập trên 2 trình duyệt bị đăng xuất cả 2, có thông báo | BR-OUT-01 |
| SC-M2-02 | M2 | Alternate | Mở MH-1 → Lưu không đổi gì → tài khoản đích không bị đăng xuất | BR-OUT-02 |
| SC-M2-03 | M2 | Alternate | Sửa/Xóa nhóm → Hủy MH-1 → CSDL không đổi, không đăng xuất, chip Tra cứu không đổi | BR-OUT-03 |
| SC-M2-04 | M2 | Happy | Sao chép nhóm sang tài khoản nhận → nhận có nhóm ngay, bị đăng xuất | BR-OUT-04 |
| SC-M2-05 | M2 | Happy | Sau Sao chép, nhóm biến mất ở tài khoản nguồn (MH-1, chip Tra cứu) | BR-OUT-05 |
| SC-M2-06 | M2 | PENDING | Tài khoản nguồn có bị đăng xuất sau Sao chép (Q07) | BR-OUT-06 |
| SC-M2-07 | M2 | Exception | Sao chép trùng toàn bộ / trùng 1 trong 3 TCTD → ERR-005 liệt kê cặp trùng; nguồn & nhận không đổi; không ai bị đăng xuất | BR-OUT-07 |
| SC-M2-08 | M2 | BVA | Chip ở Tra cứu: 3 nhóm/TCTD → 3 chip; 5 TCTD → 3 chip + "+2", thứ tự đúng; popover đầy đủ | BR-OUT-09 |
| SC-M2-09 | M2 | Data | Bộ lọc Loại quản lý/Tổ chức: tìm được tài khoản có "201 - Theo chi nhánh" gán qua Theo tất cả; không chọn → gồm tài khoản chưa có phân quyền | BR-OUT-10 |
| SC-M2-10 | M2 | Data | Xem chi tiết: Danh sách TCTD đã chọn khớp sau Thêm/Sửa/Xóa/Chuyển | BR-OUT-11 |
| SC-M2-11 | M2 | Audit | Lịch sử cập nhật có 1 dòng/lần Lưu với Giá trị cũ/mới | BR-OUT-12 |
| SC-M2-12 | M2 | Data | Màn Phê duyệt (duyệt Hiệu lực lại) hiển thị Phân quyền dữ liệu khớp 16911348 | BR-OUT-13 |
| SC-M3-01 | M3 | Decision table | Quyền "201 – Theo đầu mối" → thấy tệp 201 và 79201019/79201012/79201017; không thấy 303 | BR-OUT-14 |
| SC-M3-02 | M3 | Decision table | Quyền "01201500 – Theo chi nhánh" → chỉ thấy tệp 01201500 | BR-OUT-15 |
| SC-M3-03 | M3 | Decision table | Quyền "201 – Theo chi nhánh" (Theo tất cả) → chỉ tệp 201, không thấy 79201019 | BR-OUT-16 |
| SC-M3-04 | M3 | Security | Bộ lọc Mã đầu mối chỉ có TCTD được cấp; nhập thẳng tên tệp của 303 → "Không tìm thấy bản ghi phù hợp" (4 màn Tệp) | BR-OUT-17 |
| SC-M3-05 | M3 | Happy | Xóa nhóm 303 → đăng nhập lại → không còn 303 ở bộ lọc/kết quả | BR-OUT-18 |
| SC-M3-06 | M3 | Happy | Thêm TCTD 310 vào nhóm → đăng nhập lại → 310 xuất hiện; bỏ hành động Tiếp nhận → nút Tiếp nhận ẩn | BR-OUT-19 |
| SC-M3-07 | M3 | Alternate | Tài khoản nhận thiếu quyền chức năng Tiếp nhận dữ liệu → không vào được màn (403); được cấp Nhóm người dùng có chức năng → thấy dữ liệu theo nhóm đã chuyển | BR-OUT-08 |
| SC-M3-08 | M3 | RBAC | Không có hành động: Tiếp nhận/Từ chối ẩn; Di chuyển/Gán nhãn disabled + tooltip | BR-OUT-20 |
| SC-M3-09 | M3 | PENDING | Hành động có ở TCTD A không có ở TCTD B (Q05) | BR-OUT-21 |
| SC-M3-10 | M3 | PENDING | TCTD thuộc 2 nhóm (Q01) | BR-OUT-22 |
| SC-M3-11 | M3 | PENDING | Xuất Excel/In, URL trực tiếp tệp ngoài phạm vi (Q23) | BR-OUT-23 |
| SC-M4-01 | M4 | State | Điều chuyển (Lưu và điều chuyển) → đến Ngày hiệu lực: Phòng ban mới, MH-1 không còn nhóm quyền, chip Tra cứu trống, màn Tệp không còn dữ liệu cũ | BR-LC-01 |
| SC-M4-02 | M4 | State | Tài khoản đang đăng nhập bị đăng xuất khi điều chuyển có hiệu lực | BR-LC-02 |
| SC-M4-03 | M4 | Alternate | Điều chuyển bị Từ chối thủ công / tự động (đúng 03 ngày chưa từ chối, quá 03 ngày tự từ chối) → quyền giữ nguyên | BR-LC-03 |
| SC-M4-04 | M4 | Happy | LĐ phòng mới phân quyền lại cho tài khoản sau điều chuyển; LĐ phòng cũ không còn thấy tài khoản | BR-LC-04 |
| SC-M4-05 | M4 | State | Hết hiệu lực (không duyệt) → đăng xuất; nút Phân quyền biến mất; quyền dữ liệu còn trong CSDL | BR-LC-05 |
| SC-M4-06 | M4 | State | Hiệu lực lại → nút Phân quyền xuất hiện; đăng nhập thấy dữ liệu theo nhóm cũ | BR-LC-06 |
| SC-M4-07 | M4 | Alternate | Bỏ Nhóm người dùng chứa chức năng Tiếp nhận dữ liệu → 403 ở màn Tiếp nhận; MH-1 vẫn hiển thị hành động; cấp lại → dữ liệu hiển thị lại | BR-LC-07 |
| SC-M4-08 | M4 | Data | TCTD bị hủy kích hoạt sau khi phân quyền → MH-1/Xem chi tiết hiển thị trạng thái mới, bản ghi vẫn còn | BR-LC-08 |
| SC-M4-09 | M4 | Concurrency | 2 LĐ phòng cùng mở MH-1 một tài khoản, A Lưu trước, B Lưu sau → B bị chặn | BR-LC-09 |
| SC-M4-10 | M4 | Alternate | Đổi Phòng ban/Nhóm người dùng khi tài khoản đang đăng nhập → lần Tìm kiếm kế tiếp phản ánh thay đổi | BR-LC-10 |

**Tổng:** 48 kịch bản (M1: 15 · M2: 12 · M3: 11 · M4: 10) — trong đó **5 PENDING-Q&A** (SC-M1-05, SC-M2-06, SC-M3-09, SC-M3-10, SC-M3-11).
**Ước lượng B5:** ~95–110 TC (4 module) → **COMPACT mode** (summary trong chat, chi tiết ghi thẳng vào `scripts/gen_tc_tichhopphanquyendulieucic.py`).

**Dữ liệu test chuẩn bị (dùng chung B5):**
- Phòng TT XLDL: LĐ phòng `lp.ttxldl`, cán bộ `cb.a` (Hoạt động), `cb.b` (Hoạt động), `cb.c` (Không hoạt động), `cb.d` (Chờ lãnh đạo duyệt); phòng XHTD: cán bộ `cb.x`; phòng VHAN: `vh.qt`; BLĐ: `ld.dv`.
- TCTD (NV16): 201 (đầu mối), 79201019/79201012/79201017 (ORG_REPORTING_CODE = 201), 01201500, 01203500 (tự báo cáo), 303, 310.
- Tệp mẫu ở 4 màn Tệp: mỗi Mã đầu mối trên ít nhất 1 tệp trạng thái Chờ tiếp nhận + 1 tệp Đã tiếp nhận; tệp tên `D32201…`, `D32303…`.
