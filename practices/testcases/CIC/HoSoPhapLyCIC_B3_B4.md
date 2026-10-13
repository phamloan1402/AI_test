# [FUNC-XLDL-009] XLDL hồ sơ pháp lý — B3 Phân rã & B4 Truy vết

> Pipeline: `HoSoPhapLyCIC` · Mã TC: `HSPL_###` · Q&A: `practices/Q&A/HoSoPhapLyCIC_QA.md` (user chọn "Dùng assumptions, tiếp tục B3" — 2026-10-12)
> Ký hiệu nguồn giữ nguyên như file Q&A: [P0] 1212957 · [P1] 1213026 · [P2] 6029984 · [P3] 6030523 · [P4] 6030601 · [P5] 6031014 · [P6] 6031340 · [P7] 43521153 · [P8] 43521156 · [QT] `Template/Quy+tắc+component.md`
> **Ký hiệu:**
> - `[A-Qxx]` = dùng phương án `>> Chọn` của Q-ID (WARNING/SUGGESTION, không ⚠️) làm assumption — user đã chấp thuận.
> - `[BA-Qxx]` = theo câu trả lời BA/PO trong `practices/Q&A/HoSoPhapLyCIC_QA.md` (cập nhật 2026-10-12): Q01, Q02, Q03, Q04, Q05, Q06, Q07 (user chốt Option B), Q21, Q38, Q40.
> - Không còn kịch bản `PENDING-Q&A`.
> - `[U-Q32]` = user chốt tại B5b (GAP-01) thay assumption Q32 — REOPEN `HoSoPhapLyCIC-20261012-03`.

---

## B3a — Phân rã module & dependency

| Module | Màn hình / phạm vi | Sub-module | Risk | Phụ thuộc |
|---|---|---|---|---|
| **M1 — Danh sách hồ sơ pháp lý** | MH-001 (FEAT-01) | M1a Header (Cấu hình hiển thị, Xuất Excel) · M1b Khu vực tìm kiếm (13 điều kiện + Thêm bộ lọc / Làm mới / Tìm kiếm) · M1c Chọn bản ghi + dải thao tác hàng loạt + banner INF_009 · M1d Lưới 16 cột + menu Thao tác · M1e Phân trang | **High** (điểm vào mọi thao tác; phạm vi dữ liệu) | M8 (dữ liệu hồ sơ ở 4 trạng thái), RBAC |
| **M2 — Xem chi tiết D10/D11** | MH-002 (FEAT-02) | M2a Thẻ thông tin + Lý do · M2b Tab Thông tin hồ sơ — KH Tổ chức (TTC, TC001–TC023, TC024/025/026 khối lặp) · M2c Tab Thông tin hồ sơ — KH Cá nhân (TTC, CN001–CN022) · M2d Tab Lịch sử cập nhật | Medium | M1 (menu Xem), M8 (lịch sử) |
| **M3 — Xem chi tiết Q11** | MH-003 (FEAT-03) | như M2 với tập chỉ tiêu Q11 (KB001; Tổ chức TC004–007, TC011–013, TC015, TC017–022; Cá nhân CN001–012, CN014, CN016, CN017, CN022) | Medium | M1, M8 |
| **M4 — Xử lý hồ sơ D10/D11** | MH-004 (FEAT-04) + MH-006/MH-007 | M4a Thẻ Hồ sơ xem xét · M4b Thẻ Hồ sơ tại CIC · M4c Tóm tắt + công tắc (mặc định tắt) · M4d Bảng so sánh 3 cột (★, tooltip, dropdown Ngày báo cáo, nhãn C06, tô nền, BR-048/049, sticky header) · M4e Nút Hủy/Từ chối/Cập nhật · M4f Popup MH-006 · M4g Popup MH-007 | **High** (ghi dữ liệu pháp lý) | M1, M8; sau xác nhận → M8 (C06, nghi trùng, INF_011) |
| **M5 — Xử lý hồ sơ Q11** | MH-005 (FEAT-05) + MH-006/MH-007 | như M4, tập chỉ tiêu Q11, không có chỉ tiêu dạng bảng | **High** | M1, M8 |
| **M6 — Popup xác nhận Cập nhật / Từ chối** | MH-006, MH-007 | Không lập sheet riêng — theo `[CHECK 10]` được sinh **đầy đủ trong từng sheet M4, M5, M7** nơi popup được mở | **High** | M4, M5, M7 |
| **M7 — Xử lý đồng thời** | MH-008 (FEAT-06 D10/D11, FEAT-07 Q11) + MH-006/MH-007 | M7a Danh sách hồ sơ đã chọn (checkbox, chip khác biệt, mờ khi bỏ chọn) · M7b Vùng so sánh (công tắc mặc định bật) · M7c Footer Hủy / Từ chối (n) / Cập nhật (n) · M7d Popup MH-006/007 (một lý do chung) · M7e Biến thể Q11 | **High** (ghi hàng loạt) | M1 (≥2 hồ sơ), M4/M5 (dùng chung quy tắc so sánh) |
| **M8 — Nghiệp vụ tự động, trạng thái & tích hợp** | FEAT-08 + BR liên chức năng | M8a Phân loại khi tiếp nhận (3 nhánh) · M8b Chờ cấp mã → Đã xử lý · M8c Cờ QHTD · M8d Sau xác nhận: C06, nghi trùng · M8e INF_010 / INF_011 · M8f Lịch sử theo KH · M8g State machine · M8h RBAC & phạm vi dữ liệu | **High** | FUNC-XLDL-002 (đầu vào), FUNC-XLDL-013/035 (đầu ra) |

**Chuỗi phụ thuộc:** FUNC-XLDL-002 tiếp nhận tệp → **M8a** phân loại (+ INF_010) → **M1** tra cứu → **M2/M3** xem · **M4/M5** xử lý một hồ sơ · **M7** xử lý đồng thời → **M6** popup xác nhận → **M8d/M8e** C06, nghi trùng, INF_011 → **M1** danh sách cập nhật trạng thái; **M8b** do FUNC-XLDL-013 kích hoạt.

**Tổ chức sheet Excel (COMPACT):** `M1_DanhSach` · `M2_ChiTiet_D10D11` · `M3_ChiTiet_Q11` · `M4_XuLy_D10D11` · `M5_XuLy_Q11` · `M7_XuLyDongThoi` (gồm biến thể Q11 ở section riêng) · `M8_NghiepVu_TichHop`. Mỗi sheet có đủ Nhóm A + button + popup của chính nó (`[CHECK 10]`).

---

## B3b — Field Inventory & Common TC mapping

> Nguyên tắc kết hợp: **SRS > [QT] > checklist**. Chỉ liệt kê control có trong bảng "Mô tả các thành phần" của SRS hoặc được assumption đã chấp thuận bổ sung (ghi rõ `[A-Qxx]`).

### 3b.1 Field Inventory

#### M1 — MH-001 Danh sách hồ sơ pháp lý

| # | Field / Control | Type | Required | Default / Placeholder | Constraint / Nguồn | Nhóm |
|---|---|---|---|---|---|---|
| 1 | Loại khách hàng | DROPDOWN (single) | Yes | Cá nhân | Cá nhân, Tổ chức (BR-013); không xóa được `[A-Q20]` | H (+H17) |
| 2 | Mã đầu mối | CBB autocomplete (single) | Yes | Trống / "Mã đầu mối" | Gõ mã/tên, đầu mối gửi báo cáo NV-16 (BR-014); chỉ gợi ý đầu mối thuộc TCTD được phân quyền `[BA-Q21]` | H + D22–D28 |
| 3 | Mã tệp | DROPDOWN (single) | Yes | D10 `[A-Q20]` | D10, D11, Q11 | H (+H17) |
| 4 | Mã CIC | MULTISELECT+SEARCH | No | Trống / "Mã CIC" | Theo Loại KH + Mã đầu mối (BR-015); reset khi đổi cha `[A-Q22]` | J + D22–D28 |
| 5 | Tên tệp | MULTISELECT+SEARCH | No (bộ lọc mặc định tắt) | "Tên tệp" | Theo Mã tệp + Mã đầu mối `[A-Q22]` | J + D22–D28 |
| 6 | Mã khách hàng | MULTISELECT+SEARCH | No | "Mã khách hàng" | Khớp chính xác TTC03 (BR-015) `[A-Q22]` | J + D22–D28 |
| 7 | Nhóm khách hàng | MULTISELECT | No | "Nhóm khách hàng" | 4 giá trị (BR-016) | J |
| 8 | Trạng thái | MULTISELECT | No | "Trạng thái" | Chờ cấp mã, Chờ xem xét, Đã xử lý, Từ chối | J |
| 9 | Người cập nhật | MULTISELECT+SEARCH | No | "Người cập nhật" | Cán bộ CIC + "Sys" `[A-Q22]` | J + D22–D28 |
| 10 | CCCD/CMND | MULTISELECT+SEARCH | No (bộ lọc mặc định tắt) | "CCCD/CMND" | CN008 / TC011 theo Loại KH `[A-Q25]` | J + D22–D28 |
| 11 | Từ ngày cập nhật – Đến ngày cập nhật | DATE range | No | Trống / dd/mm/yyyy | Đến ≥ Từ (BR-018, ERR_003); 1 vế, cận bao gồm `[A-Q24]` | K (K01–K08, K12–K16) |
| 12 | Từ ngày báo cáo – Đến ngày báo cáo | DATE range | No | Trống / dd/mm/yyyy | như #11 | K |
| 13 | Cấu hình hiển thị | BUTTON + popup CMP-025 | — | — | Ẩn/hiện, kéo thả, Áp dụng; 4 cột bắt buộc (BR-021) `[A-Q29]` | M |
| 14 | Xuất Excel | BUTTON (3 lựa chọn) | — | — | HoSoPhapLy_ddmmyyyy (BR-022) `[A-Q28]` | M (Xuất Excel 7 TC) |
| 15 | Thêm bộ lọc | BUTTON + popup | — | — | Bật/tắt bộ lọc, 3 bắt buộc luôn hiện (BR-019) `[A-Q29]` | M |
| 16 | Làm mới | BUTTON | — | — | Trả điều kiện mặc định, lưới về trạng thái rỗng `[A-Q20]` | M |
| 17 | Tìm kiếm | BUTTON | — | — | WAR_009, ERR_003, INF_003 | M + T |
| 18 | Dải thao tác hàng loạt + "Đã chọn n hồ sơ" | LABEL | — | Ẩn | BR-026 | BIZ |
| 19 | Xử lý hồ sơ (dải) | BUTTON | — | — | 1 hồ sơ → MH-004/005; ≥2 → MH-008 | M |
| 20 | Bỏ chọn | BUTTON | — | — | BR-026 | M |
| 21 | Chọn tất cả | CHECKBOX (3 trạng thái) | — | Unchecked | Chỉ dòng bật `[A-Q19]` | I |
| 22 | Chọn bản ghi | CHECKBOX | — | Unchecked; chỉ bật khi Chờ xem xét | BR-024 | I |
| 23 | Banner INF_009 | Notification | — | Ẩn | Chỉ phần hiển thị/tắt `[A-Q18]` | BIZ |
| 24 | Lưới: STT, Ngày báo cáo, Mã tệp*, Tên tệp*, Mã đầu mối, Mã KH, Tên KH, CCCD/MSDN, Địa chỉ, Loại KH*, Mã CIC, Nhóm KH, Trạng thái (badge), Ngày cập nhật*, Người cập nhật*, Thao tác (* = ẩn mặc định) | GRID (16 cột) | — | Sắp Ngày cập nhật giảm dần | BR-020, BR-021; lọc theo cột = [QT] C14 (giải thích icon phễu trên mockup — Q26); không có sắp xếp theo cột `[A-Q26]` | C + U (U01–U04 × 15 cột dữ liệu) + W3 |
| 25 | Menu Thao tác: Xem, Xử lý hồ sơ | ACTION | — | — | BR-023 | U (U05–U07 × 2) |
| 26 | Số bản ghi/trang, Số trang, ô Đến trang | PAGINATION | — | 20 / trang 1 | Max 5000; vượt → trang cuối (BR-027) `[A-Q27]` | C (3 tc_group) |

#### M2 / M3 — MH-002 / MH-003 Xem chi tiết

| # | Field / Control | Type | Constraint / Nguồn | Nhóm |
|---|---|---|---|---|
| 1 | Tab Thông tin hồ sơ / Lịch sử cập nhật | TABS | Mặc định tab Thông tin (BR-028) | A + BIZ |
| 2 | Thẻ: Tên KH, Đầu mối báo cáo, Mã KH, Loại KH, Nhóm KH, Mã CIC, Trạng thái (badge), Lý do, Tên tệp | LABEL | Lý do chỉ khi Đã xử lý/Từ chối (BR-029); Đầu mối "mã - tên", rỗng → trống `[A-Q37]` | BIZ + W3 |
| 3 | Chỉ tiêu KB/TTC/TC/CN (M2: 56 chỉ tiêu; M3: 35 chỉ tiêu) | LABEL + tooltip | Giá trị đang lưu (BR-028); tooltip tên chỉ tiêu (BR-030); nhóm theo Loại KH | BIZ (đại diện từng nhóm chỉ tiêu) |
| 4 | Khối lặp TC024 / TC025 / TC026 (chỉ M2, Tổ chức) | LABEL repeat | 0 bản ghi → chỉ tiêu đề nhóm `[A-Q37]` | BIZ |
| 5 | Bảng Lịch sử: STT, Thời gian, Người cập nhật (tooltip), Hành động, Giá trị cũ, Giá trị mới, Địa chỉ IP, Mô tả | GRID (8 cột, scroll, mới nhất trên cùng — [QT]) | BR-031; nội dung theo Hành động `[A-Q36]` | U (U01–U04 × 8; U03 N/A — SRS không có lọc cột trong tab lịch sử) + C12 |
| 6 | Đóng | BUTTON | Về MH-001 | M |

#### M4 / M5 — MH-004 / MH-005 Xử lý một hồ sơ (+ MH-006/007)

| # | Field / Control | Type | Required | Default | Constraint / Nguồn | Nhóm |
|---|---|---|---|---|---|---|
| 1 | Thẻ Hồ sơ xem xét: Tên KH, Mã KH, Loại KH, Đầu mối báo cáo, Ngày báo cáo, Trạng thái | LABEL + badge | — | Trạng thái Chờ xem xét | BR-047 thứ tự dòng | BIZ + W3 |
| 2 | Thẻ Hồ sơ tại CIC: Mã CIC, Loại KH tại CIC, TCTD có liên quan (tooltip NV-16) | LABEL + tooltip | — | — | Tô nền khi lệch Loại KH; "còn hiệu lực" `[A-Q15]` | BIZ |
| 3 | Tóm tắt khác biệt + chú thích | LABEL | — | — | Cách đếm `[A-Q10]`; nhãn `[A-Q42]` | BIZ |
| 4 | Chỉ hiện chỉ tiêu khác biệt | TOGGLE | — | Tắt (M4/M5) | BR-045 | I (I01–I05 áp dụng cho switch) + BIZ |
| 5 | Bảng so sánh: Chỉ tiêu (★, tooltip), Hồ sơ đang xem xét, Hồ sơ tại TCTD, Hồ sơ tại CIC (nhãn C06) | GRID so sánh | — | — | BR-030, 032–037, 046, 048, 049 (M4); cột TCTD: cùng Mã CIC + cùng TTC00, không gồm chính hồ sơ `[BA-Q03]`; cột CIC (CICinfo) không đổi sau cập nhật `[BA-Q02]` | U (U01–U04 × 4 cột; U03 N/A — không có lọc cột) + BIZ |
| 6 | Ngày báo cáo (cột TCTD) | DROPDOWN (single) | — | Phiên bản mới nhất | ≤3 option; trùng/trống `[A-Q35]` | H |
| 7 | Hủy · Từ chối · Cập nhật | BUTTON | — | — | — | M |
| 8 | MH-006: câu CONF_001, Lý do, Hủy, Cập nhật, icon X `[A-Q31]` | POPUP | — | — | CONF_001 action "cập nhật" | M (CONF: nút xác nhận 3, Hủy 3, X 2) |
| 9 | MH-006 — Lý do | TEXTAREA | Yes | Trống / "Nhập lý do" | Max 1000; trim, chặn ở 1000, paste cắt + inline, validate khi bấm xác nhận `[A-Q32]`; ERR_001/ERR_023 | **G (41 TC)** |
| 10 | MH-007: câu CONF_001, Lý do, Hủy, Từ chối, icon X `[A-Q31]` | POPUP | — | — | CONF_001 action "từ chối cập nhật" | M (CONF 8 TC) |
| 11 | MH-007 — Lý do | TEXTAREA | Yes | Trống / "Nhập lý do" | như #9 | **G (41 TC)** |

#### M7 — MH-008 Xử lý đồng thời (+ MH-006/007)

| # | Field / Control | Type | Default | Constraint / Nguồn | Nhóm |
|---|---|---|---|---|---|
| 1 | Tiêu đề "Hồ sơ đã chọn (n)" + dòng phụ "Tệp <mã> · Khách hàng <loại>" | LABEL | — | `[A-Q34]` | BIZ |
| 2 | Danh sách hồ sơ đã chọn (cuộn dọc) | SCROLLABLE LIST | Hồ sơ đầu tiên đang xem | Thứ tự theo MH-001 `[A-Q34]` | BIZ |
| 3 | Chọn hồ sơ | CHECKBOX (mỗi hồ sơ) | Checked | Bỏ chọn → mờ, vẫn xem được (BR-042) | I |
| 4 | Tên KH, Mã KH + mã đầu mối, Mã CIC, chip chỉ tiêu khác biệt (★) | LABEL | — | BR-042, BR-043 `[A-Q14]` | BIZ |
| 5 | Vùng so sánh (thẻ, tóm tắt, bảng, dropdown Ngày báo cáo, nhãn C06) | như M4 #1–#6 | Công tắc **bật** | BR-045; công tắc/phiên bản đặt lại khi chuyển hồ sơ `[A-Q34]` | I, H, U, BIZ |
| 6 | Hủy · Từ chối (n) · Cập nhật (n) | BUTTON | — | Khóa khi n = 0 (BR-042) | M |
| 7 | MH-006 / MH-007 (Lý do chung) | POPUP + TEXTAREA | — | BR-044; giữ lý do khi Hủy `[A-Q32]` | M (CONF 8 TC × 2) + **G (41 TC × 2)** |

#### M8 — Không có UI riêng (kiểm chứng qua M1/M2/M3 và dữ liệu)

| # | Đối tượng | Kiểm chứng tại | Nguồn |
|---|---|---|---|
| 1 | Nhóm KH, Trạng thái, Mã CIC, cờ chỉ tiêu quan trọng thay đổi | Cột lưới MH-001, thẻ MH-002/003 | [P8] bảng thành phần |
| 2 | Lịch sử Tiếp nhận / Cập nhật tự động / Cấp mã CIC / Cập nhật / Từ chối | Tab Lịch sử MH-002/003 | BR-031 `[A-Q36]` |
| 3 | INF_010 (trong hệ thống), INF_011 (Push + Email) | Chuông thông báo cán bộ; hộp thư/push đơn vị báo cáo | BR-008, BR-012 `[A-Q08]`, `[A-Q09]` |
| 4 | Chuyển C06 / nghi trùng | Danh sách FUNC-XLDL-035 / FUNC-XLDL-013 | BR-010/011 `[A-Q16]` |

### 3b.2 Nhóm Common TC áp dụng

| Nhóm | Áp dụng | Field / màn áp dụng |
|---|---|---|
| A — Giao diện chung (A01–A06; A07–A08 QT) | ✅ | M1, M2, M3, M4, M5, M7 + mỗi popup MH-006/007 (trong sheet sử dụng) |
| B — Collapse/Expand | ❌ | SRS dùng Tabs (CMP-030), không có panel thu gọn |
| C — Grid + Paging | ✅ | M1 lưới (đủ C01–C16 + 3 tc_group); M2/M3 bảng lịch sử (C01, C02, C12 — không phân trang theo [QT]); C09/C10 N/A (không có Thêm/Sửa/Xóa trên lưới — thay bằng BIZ "sau xử lý quay về MH-001" `[A-Q33]`) |
| D — TEXT | ❌ (D22–D28 ✅) | Không có Textbox; D22–D28 cho ô tìm kiếm của 6 control searchable ở M1 |
| E, F, L, O — Number/Email/Password/IP | ❌ | Không có |
| G — Textarea (41 TC/field) | ✅ | Lý do MH-006, Lý do MH-007 — trong mỗi sheet M4, M5, M7 |
| H — Dropdown | ✅ | Loại KH, Mã đầu mối, Mã tệp (M1); Ngày báo cáo cột TCTD (M4, M5, M7) |
| I — Checkbox | ✅ | Chọn tất cả, Chọn bản ghi (M1); Chọn hồ sơ (M7); công tắc Chỉ hiện chỉ tiêu khác biệt (M4, M5, M7 — áp I01–I05) |
| J — Multi-select | ✅ | Mã CIC, Tên tệp, Mã KH, Nhóm KH, Trạng thái, Người cập nhật, CCCD/CMND (M1) |
| K — Date | ✅ | 2 RangePicker M1 (K01–K08 gồm K04 icon x — B5b GAP-03, K12–K16; K09–K11 N/A — không cấm ngày; K17 N/A — tìm kiếm cho chọn ngày tự do theo [QT]) |
| M — Button | ✅ | Mọi màn; Xuất Excel đủ 7 TC; CONF MH-006/007 đủ 8 TC/popup |
| N, P, Q, R — Radio/Xóa/Upload/Import | ❌ | Không có trong SRS |
| S — Phân quyền | ✅ | M1 (menu, dữ liệu theo TCTD), M8h |
| T — Tra cứu kết hợp | ✅ | M1: 12 điều kiện → riêng lẻ + leo thang + tất cả + TX01/TX02; AND giữa / OR trong `[A-Q23]` |
| U — Grid cột & thao tác | ✅ | M1 (15 cột dữ liệu + 2 thao tác), M2/M3 bảng lịch sử (8 cột), M4/M5/M7 bảng so sánh (4 cột) |
| V — Edit form | ❌ | Không có chỉnh sửa trường; Cập nhật/Từ chối là xác nhận nghiệp vụ |
| W — Component phức tạp | ✅ W3 | Badge Trạng thái (M1, M2, M3, M4, M5, M7) |

### 3b.3 Kỹ thuật thiết kế dùng ở B5

| Kỹ thuật | Áp dụng cho |
|---|---|
| Decision table | Phân loại khi tiếp nhận (R1–R4 trong Q&A §2.3); BR-023/024 (trạng thái × thao tác); BR-026 (số hồ sơ chọn × loại tệp) |
| State transition | ST-HOSOPL-01…04: 6 transition hợp lệ + chặn thao tác ở trạng thái cuối/Chờ cấp mã |
| EP + BVA | Lý do 0/1/999/1000/1001 ký tự; số phiên bản TCTD 1/2/3/4; số hồ sơ chọn 0/1/2; số bản ghi/trang 20/5000; số trang vượt max; khoảng ngày Từ = Đến, Từ > Đến 1 ngày |
| Pairwise / leo thang | Tra cứu kết hợp 12 điều kiện (Nhóm T) |
| Error guessing | BR-048 (trim, NULL vs rỗng, hoa/thường `[A-Q11]`), BR-049 (khóa trùng/rỗng `[A-Q12]`) |

### 3b.4 Ước lượng số TC (COMPACT)

| Sheet | Ước lượng | Ghi chú |
|---|---:|---|
| M1_DanhSach | ~470 | 3 H + 7 J (×~17) + 6 ô search D22–D28 + 2 K + C + U (17×) + T + M (Xuất Excel 7) + BIZ |
| M2_ChiTiet_D10D11 | ~80 | A + tab + nhóm chỉ tiêu Tổ chức/Cá nhân + khối lặp + lịch sử U×8 |
| M3_ChiTiet_Q11 | ~65 | như M2, tập Q11 |
| M4_XuLy_D10D11 | ~200 | 2 Lý do × G 41 + 2 CONF × 8 + H + U×4 + BIZ so sánh + BR-049 |
| M5_XuLy_Q11 | ~185 | như M4, không có BR-049 |
| M7_XuLyDongThoi | ~240 | như M4 + danh sách hồ sơ + biến thể Q11 |
| M8_NghiepVu_TichHop | ~45 | phân loại, trạng thái, thông báo, tích hợp, RBAC |
| **Tổng** | **~1.300** | +~15 TC BIZ cho 10 kịch bản trước đây PENDING (nay đã có expected theo câu trả lời BA/user) |

---

## B4 — Ma trận truy vết 4 tầng

### Tầng 1 — Use case / Feature ↔ Module ↔ Tiêu chí nghiệm thu

| UC / FEAT | Nội dung | Module | Tiêu chí chấp nhận (nguồn) | Scenario |
|---|---|---|---|---|
| UC-0539 | Kiểm tra thông tin pháp lý khi tiếp nhận (BR-003) | M8a | [P8] AC#1–#3 | SC-M8-01…04 |
| UC-0540 | Phân nhóm KH mới, đánh dấu QHTD (BR-004, 006) | M8a, M8c | [P8] AC#1 | SC-M8-01, 02, 07 |
| UC-0541 | Tra cứu Nhóm "Mới - Không QHTD" | M1 | [P1] AC#1, #7 | SC-M1-20 |
| UC-0542 | Cập nhật tự động thông tin không quan trọng (BR-007) | M8a | [P8] AC#2 | SC-M8-03 |
| UC-0543, UC-0544 | Đánh dấu chỉ tiêu quan trọng (FUNC-XLDL-027 — dùng chung) | M4d, M8a | — (đọc cờ BR-009) | SC-M4-07 |
| UC-0545 | Đánh dấu hồ sơ thay đổi thông tin quan trọng (BR-008) | M8a | [P8] AC#3 | SC-M8-04 |
| UC-0546 | Gửi INF_010 (BR-008) | M8e | [P8] AC#4 | SC-M8-09 |
| UC-0547 | Tra cứu Nhóm "Thay đổi TTQT" | M1 | [P1] AC#3 | SC-M1-20 |
| UC-0548 | Từ chối tiếp nhận hồ sơ | M4, M5, M7, M6 | [P4] AC#5, [P5] AC#6, [P6] — | SC-M4-14, SC-M5-03, SC-M7-08 |
| UC-0549 | Xác nhận hồ sơ hợp lệ | M4, M5, M7, M6 | [P4] AC#3–#4, [P5] AC#4–#5, [P6] AC#3 | SC-M4-12, SC-M5-03, SC-M7-07 |
| UC-0550 | Cập nhật thông tin pháp lý sau xác nhận (BR-040) | M4, M5, M7 | [P4] AC#4 | SC-M4-12, 13 |
| UC-0551 | Gửi KH vừa cập nhật sang kiểm tra nghi trùng (BR-011) | M8d | — | SC-M8-11 |
| UC-0552 | Danh sách cảnh báo nghi trùng (FUNC-XLDL-013 — dùng chung) | M8d | — | SC-M8-11 (chỉ kiểm việc chuyển) |
| Không thuộc UC — FEAT-02 | Xem chi tiết D10/D11 | M2 | [P2] AC#1–#4 | SC-M2-01…08 |
| Không thuộc UC — FEAT-03 | Xem chi tiết Q11 | M3 | [P3] AC#1–#4 | SC-M3-01…04 |
| FEAT-01 (8 AC) | Tra cứu | M1 | [P1] AC#1–#8 | SC-M1-01…24 |
| FEAT-06 / FEAT-07 (4 AC mỗi FEAT) | Xử lý đồng thời | M7 | [P6] AC#1–#4, [P7] AC#1–#4 | SC-M7-01…14 |

### Tầng 2 — Business Rule & mã thông báo (1 dòng / BR)

| BR | Nội dung rút gọn | Module | Scenario | Trạng thái |
|---|---|---|---|---|
| BR-001 | Đăng nhập + phân quyền; không quyền không thấy menu; ERR_011 | M1, M8h | SC-M8-15, 16 | ✅ menu ẩn; URL trực tiếp → ERR_011; ROLE + 0 TCTD → danh sách rỗng; thu hồi giữa chừng → chặn ERR_011 `[BA-Q38]` |
| BR-002 | Danh sách = kho tiền dữ liệu, loại "Pháp lý", Hợp lệ, D10/D11/Q11 | M1, M8a | SC-M1-21, SC-M8-14 | ✅ |
| BR-003 | KH mới = khóa TTC00+TTC03 chưa có trong CICinfo; KH cũ đối chiếu thông tin quan trọng | M8a | SC-M8-01…04 | ✅ đối chiếu với phiên bản mới nhất tại kho TCTD cùng TTC00+TTC03 `[BA-Q01]` |
| BR-004 | KH mới: Mới-Có/Không QHTD; Chờ cấp mã; chuyển cấp mã | M8a | SC-M8-01, 02, 05 | ✅ (nhận lặp KH mới `[A-Q04]`) |
| BR-005 | Chờ cấp mã được cấp mã → Đã xử lý + Mã CIC | M8b | SC-M8-06 | ✅ |
| BR-006 | Nhận hồ sơ QHTD của KH không QHTD → đã có QHTD | M8c | SC-M8-07 | ✅ kiểm chứng ở CSDL `[A-Q17]` |
| BR-007 | KH cũ không đổi TTQT → cập nhật tự động, "Không thay đổi TTQT", Đã xử lý | M8a | SC-M8-03 | ✅ ghi kho TCTD, CICinfo không đổi `[BA-Q02]` |
| BR-008 | KH cũ có đổi TTQT → đánh dấu, "Thay đổi TTQT", Chờ xem xét, INF_010 | M8a, M8e | SC-M8-04, 09 | ✅ `[BA-Q01]`, `[A-Q09]` |
| BR-009 | Chỉ tiêu quan trọng theo danh mục FUNC-XLDL-027 | M4d, M8a | SC-M4-07, SC-M8-04 | ✅ (TTC03 là một phần khóa → không phát sinh khác biệt `[BA-Q01]`) |
| BR-010 | Đổi trường định danh → chuyển C06 | M8d | SC-M8-10 | ✅ KH cá nhân `[A-Q16]` |
| BR-011 | Sau cập nhật → gửi FUNC-XLDL-013 kiểm tra nghi trùng | M8d | SC-M8-11 | ✅ `[A-Q16]` |
| BR-012 | Tệp hết Chờ xem xét → INF_011 danh sách từ chối (Push + Email) | M8e | SC-M8-12, 13 | ✅ `[A-Q08]` |
| BR-013 | 3 điều kiện bắt buộc; mặc định Cá nhân + tệp đầu tiên; empty state; WAR_009 | M1 | SC-M1-01, 02, 03 | ✅ `[A-Q20]` |
| BR-014 | Mã đầu mối gần đúng mã/tên, NV-16 đầu mối gửi báo cáo | M1 | SC-M1-05 | ✅ chỉ gợi ý đầu mối thuộc TCTD được phân quyền `[BA-Q21]` |
| BR-015 | Mã CIC/Mã KH theo Loại KH + Mã đầu mối; Mã KH khớp chính xác, chọn nhiều | M1 | SC-M1-06, 07 | ✅ `[A-Q22]` |
| BR-016 | 4 Nhóm KH; ánh xạ Trạng thái ↔ Nhóm | M1, M2, M3, M8a | SC-M1-08, SC-M8-08 | ✅ |
| BR-017 | Cột CCCD/MSDN theo Loại KH; bộ lọc CCCD/CMND | M1 | SC-M1-09 | ✅ `[A-Q25]`, `[A-Q23]` |
| BR-018 | Đến ngày ≥ Từ ngày (ERR_003) | M1 | SC-M1-10 | ✅ `[A-Q24]` |
| BR-019 | Thêm bộ lọc: 3 bắt buộc luôn hiện; Tên tệp, CCCD/CMND mặc định tắt | M1 | SC-M1-11 | ✅ `[A-Q29]` |
| BR-020 | Sắp Ngày cập nhật giảm dần | M1 | SC-M1-12 | ✅ |
| BR-021 | Cấu hình hiển thị: cột mặc định/ẩn/bắt buộc, lưu trên máy | M1 | SC-M1-13 | ✅ `[A-Q29]` |
| BR-022 | Xuất trang hiện tại / theo bộ lọc / In; tên tệp HoSoPhapLy_ddmmyyyy | M1 | SC-M1-14 | ✅ `[A-Q28]`; dữ liệu xuất chỉ trong TCTD được phân quyền `[BA-Q21]` |
| BR-023 | Menu Thao tác: Xem luôn có; Xử lý chỉ Chờ xem xét | M1 | SC-M1-15 | ✅ |
| BR-024 | Ô chọn chỉ bật khi Chờ xem xét; chọn tất cả 3 trạng thái | M1 | SC-M1-16 | ✅ `[A-Q19]` |
| BR-025 | Khóa ô chọn khác loại KH + banner INF_009 | M1 | SC-M1-17 | ✅ phần banner · phần khóa N/A `[A-Q18]` |
| BR-026 | Dải thao tác hàng loạt; 1 hồ sơ → MH-004/005; ≥2 → MH-008; Bỏ chọn | M1 | SC-M1-18, 19 | ✅ |
| BR-027 | Phân trang 20/5000, trang 1, vượt → trang cuối | M1 | SC-M1-22 | ✅ `[A-Q27]` |
| BR-028 | Xem chi tiết: tab Thông tin mặc định; giá trị đang lưu | M2, M3 | SC-M2-01, SC-M3-01 | ✅ `[A-Q37]` |
| BR-029 | Lý do chỉ khi Đã xử lý / Từ chối | M2, M3 | SC-M2-03, SC-M3-03 | ✅ |
| BR-030 | Mọi chỉ tiêu hiện mã; hover tooltip tên | M2, M3, M4, M5, M7 | SC-M2-06, SC-M4-06 | ✅ |
| BR-031 | Lịch sử theo KH (TTC00+TTC03); 5 Hành động; chỉ trường thay đổi; tooltip Người cập nhật | M2, M3, M8f | SC-M2-07, 08, SC-M8-14 | ✅ `[A-Q36]` |
| BR-032 | Cột TCTD: phiên bản theo Mã CIC, ≤3 mới nhất, mặc định mới nhất, trống → Ngày tạo | M4, M5, M7 | SC-M4-04, 05 | ✅ chỉ cùng Mã CIC + cùng TTC00, không gồm chính hồ sơ `[BA-Q03]`, `[A-Q35]` |
| BR-033 | Cột CIC: phiên bản duy nhất kho chuẩn theo Mã CIC | M4, M5, M7 | SC-M4-03 | ✅ |
| BR-034 | Nhãn C06 khi hồ sơ tại CIC đã xác thực | M4, M5, M7 | SC-M4-08 | ✅ `[A-Q42]` |
| BR-035 | Biểu tượng ★ trước mã chỉ tiêu quan trọng | M4, M5, M7 | SC-M4-07 | ✅ |
| BR-036 | So độc lập 2 cặp; hồ sơ đang xem xét là gốc | M4, M5, M7 | SC-M4-09 | ✅ |
| BR-037 | Tô nền ô khác, không tô dòng, không đổi màu chữ | M4, M5, M7 | SC-M4-09 | ✅ |
| BR-038 | Lý do bắt buộc, ≤1000 (ERR_001, ERR_023) | M6 (trong M4, M5, M7) | SC-M6-01…04 | ✅ `[A-Q32]` |
| BR-039 | — (không tồn tại trong SRS) | — | — | N/A `[A-Q41]` |
| BR-040 | Xác nhận → ghi kho TCTD theo Mã CIC, lưu lý do, Đã xử lý, SUC_001 | M4, M5, M7 | SC-M4-12, 13 | ✅ ghi kho TCTD; CICinfo không đổi; hồ sơ vừa ghi là phiên bản mới nhất ở cột TCTD `[BA-Q02]` |
| BR-041 | Từ chối → Từ chối, lưu lý do, không cập nhật | M4, M5, M7 | SC-M4-14 | ✅ |
| BR-042 | MH-008: danh sách, hồ sơ đầu tiên, bỏ chọn mờ, nút (n), khóa khi 0 | M7 | SC-M7-01…05 | ✅ `[A-Q34]` |
| BR-043 | MH-008: Mã CIC duy nhất khớp kết quả tìm kiếm | M7 | SC-M7-06 | ✅ `[A-Q14]` |
| BR-044 | MH-008: một lần xác nhận/từ chối, cùng lý do, cho mọi hồ sơ còn chọn | M7 | SC-M7-07, 08 | ✅ all-or-nothing: một hồ sơ lỗi → cả lô không cập nhật `[BA-Q07]` |
| BR-045 | Tóm tắt khác biệt + công tắc (tắt M4/M5, bật M7) | M4, M5, M7 | SC-M4-10, SC-M7-09 | ✅ `[A-Q10]` |
| BR-046 | Tiêu đề cột cố định khi cuộn | M4, M5, M7 | SC-M4-11 | ✅ |
| BR-047 | Thẻ CIC: Mã CIC, Loại KH, TCTD có liên quan + tooltip; tô nền lệch Loại KH | M4, M5, M7 | SC-M4-02, 03 | ✅ `[A-Q15]` |
| BR-048 | So sánh 1 giá trị: trim, từng ký tự, NULL = rỗng | M4, M5, M7 | SC-M4-15 | ✅ `[A-Q11]` |
| BR-049 | So sánh dạng bảng TC024/025/026 theo trường khóa | M4, M7 (D10/D11 Tổ chức) | SC-M4-16 | ✅ `[A-Q12]` |

**Mã thông báo:**

| Mã | Loại | Điều kiện | Module | Scenario |
|---|---|---|---|---|
| ERR_001 | Inline | Lý do trống (cả MH-006 và MH-007) | M6 | SC-M6-01 |
| ERR_003 | Inline | Từ ngày > Đến ngày (2 cặp ngày) | M1 | SC-M1-10 |
| ERR_011 | Toast | Không có quyền | M1, M8h | SC-M8-15, SC-M8-16 `[BA-Q38]` |
| ERR_023 | Inline | Lý do > 1000: chặn nhập + hiển thị ERR_023; paste cắt + ERR_023 | M6 | SC-M6-02 `[U-Q32]` |
| WAR_009 | Toast | Tìm kiếm khi thiếu điều kiện bắt buộc | M1 | SC-M1-03 |
| INF_003 | Toast | Không có kết quả | M1 | SC-M1-04 `[A-Q30]` |
| INF_009 (cá nhân / tổ chức) | Banner | Chọn hồ sơ đầu tiên | M1 | SC-M1-17 |
| INF_010 | Thông báo trong hệ thống | Tệp có hồ sơ Chờ xem xét | M8e | SC-M8-09 |
| INF_011 | Push + Email | Tệp hết Chờ xem xét và có hồ sơ Từ chối | M8e | SC-M8-12, 13 |
| SUC_001 | Toast | Cập nhật thành công (đơn & đồng thời) | M4, M5, M7 | SC-M4-12, SC-M7-07 |
| CONF_001 (cập nhật) | Popup | Mở MH-006 | M6 | SC-M6-05 |
| CONF_001 (từ chối cập nhật) | Popup | Mở MH-007 | M6 | SC-M6-06 |

### Tầng 3 — Ma trận phân quyền (RBAC)

| FEAT / Thao tác | CBTTXLDL – TCTD được phân quyền | CBTTXLDL – TCTD khác | Không có quyền chức năng | Hành vi UI khi bị chặn | Scenario |
|---|---|---|---|---|---|
| FEAT-01 Tra cứu, thêm bộ lọc, cấu hình, Xuất Excel, In | ✅ | Không thấy dữ liệu | ❌ | Menu "Hồ sơ pháp lý" ẩn (BR-001) | SC-M8-15, 17 |
| FEAT-02/03 Xem chi tiết | ✅ | ❌ | ❌ | Không có dòng để mở | SC-M8-17 |
| FEAT-04/05 Xử lý một hồ sơ | ✅ (Chờ xem xét) | ❌ | ❌ | Mục "Xử lý hồ sơ" ẩn khi không Chờ xem xét (BR-023) | SC-M1-15 |
| FEAT-06/07 Xử lý đồng thời | ✅ (≥2, Chờ xem xét) | ❌ | ❌ | Ô chọn khóa khi không Chờ xem xét (BR-024) | SC-M1-16 |
| FEAT-08 Xử lý tự động | Hệ thống | — | — | — | SC-M8-01…08 |
| Nhận INF_010 | ✅ cán bộ được phân quyền TCTD gửi tệp | ❌ | ❌ | — | SC-M8-09 |
| Lựa chọn Mã đầu mối ngoài quyền | — | Không có trong gợi ý `[BA-Q21]` | — | Đầu mối không hiển thị trong danh sách gợi ý | SC-M1-25 |
| URL trực tiếp / ROLE nhưng 0 TCTD / thu hồi giữa chừng | ROLE + 0 TCTD → menu hiện, danh sách rỗng | — | URL trực tiếp → ERR_011, không dữ liệu | Thu hồi giữa chừng → chặn thao tác, ERR_011 `[BA-Q38]` | SC-M8-16 |

### Tầng 4 — State machine, NFR & thành phần dùng chung

**State machine (ST-HOSOPL):**

| # | Transition | Loại | Scenario |
|---|---|---|---|
| T1 | (tiếp nhận) → ST-04 Chờ cấp mã | Hợp lệ | SC-M8-01, 02 |
| T2 | (tiếp nhận) → ST-01 Đã xử lý | Hợp lệ | SC-M8-03 |
| T3 | (tiếp nhận) → ST-03 Chờ xem xét | Hợp lệ | SC-M8-04 |
| T4 | ST-04 → ST-01 (cấp mã) | Hợp lệ | SC-M8-06 |
| T5 | ST-03 → ST-01 (Cập nhật) | Hợp lệ | SC-M4-12, SC-M7-07 |
| T6 | ST-03 → ST-02 (Từ chối) | Hợp lệ | SC-M4-14, SC-M7-08 |
| T7 | ST-01 / ST-02 / ST-04 → Cập nhật/Từ chối qua UI | Không hợp lệ — UI chặn (menu ẩn, ô chọn khóa) | SC-M1-15, 16 |
| T8 | Hồ sơ đã đổi trạng thái khi đang mở màn xử lý (stale / đồng thời) | Không hợp lệ — chặn, toast "Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.", tự thoát và reload sau khi toast tắt `[BA-Q06]` | SC-M8-18 |
| T9 | Hai hồ sơ Chờ xem xét cùng KH, xử lý không theo thứ tự | Hợp lệ — xử lý tự do, kho TCTD lưu theo lần xác nhận sau cùng `[BA-Q05]` | SC-M8-19 |

**NFR:**

| Hạng mục | Nội dung kiểm thử | Scenario |
|---|---|---|
| Hiệu năng | Không kiểm định lượng (SRS không có SLA) — chỉ kiểm hiển thị 5000 bản ghi/trang và có loading `[A-Q39]` | SC-M1-22 |
| Bất đồng bộ / chống bấm lặp | Nút xác nhận bị khóa + loading khi đang xử lý; không ghi 2 lần `[A-Q39]` | SC-M6-07 |
| Responsive | Nhóm A06 cho mọi màn | A06 mỗi sheet |
| Lưu trữ | Hồ sơ & lịch sử lưu vĩnh viễn — không kiểm trong phạm vi chức năng | N/A |
| Nhật ký truy cập PII | Ngoài phạm vi (audit chung hệ thống) `[BA-Q40]`; chỉ kiểm dữ liệu hiển thị/xuất không che | SC-M8-20 |

**Thành phần dùng chung:**

| Component | Vị trí | Scenario |
|---|---|---|
| CMP-025 Cấu hình hiển thị | M1 | SC-M1-13 |
| CMP-016 Xuất Excel & In | M1 | SC-M1-14 |
| CMP-018 Lịch sử cập nhật (biến thể theo KH) | M2, M3 | SC-M2-07, 08 |
| CMP-014 Bộ lọc / Thêm bộ lọc | M1 | SC-M1-11 |
| CMP-015 Phân trang | M1 | SC-M1-22 |
| CMP-021 Confirm dialog (MH-006/007) | M4, M5, M7 | SC-M6-05, 06 |
| CMP-028 Badge trạng thái | M1, M2, M3, M4, M5, M7 | SC-M1-23 |
| CMP-033 Empty state | M1, M2, M3 | SC-M1-01, 04 |
| CMP-042 Scrollable list | M7 | SC-M7-01 |

---

## B4 — High-Level Scenarios

> Loại: **H** = Happy · **A** = Alternate · **E** = Exception · **C** = Concurrency · **S** = Security/RBAC.

### M1 — Danh sách hồ sơ pháp lý

| ID | Loại | Kịch bản | Nguồn |
|---|---|---|---|
| SC-M1-01 | H | Mở màn: Loại KH = Cá nhân, Mã tệp = D10, Mã đầu mối trống, bộ lọc mặc định, lưới rỗng "Chưa có dữ liệu. Vui lòng chọn tiêu chí tìm kiếm.", cột ẩn/hiện mặc định | BR-013, 019, 021, [P1] AC#7–#8 |
| SC-M1-02 | H | Chọn đủ 3 điều kiện → Tìm kiếm → hiển thị hồ sơ đúng điều kiện, 20 dòng/trang | BR-013, 002 |
| SC-M1-03 | E | Tìm kiếm khi thiếu Mã đầu mối → WAR_009, lưới giữ trạng thái rỗng | BR-013 `[A-Q20]` |
| SC-M1-04 | E | Điều kiện không khớp → INF_003 + empty state | [P1] EXC-03 `[A-Q30]` |
| SC-M1-05 | H | Mã đầu mối: gõ mã / tên (gần đúng), chỉ đầu mối gửi báo cáo | BR-014 |
| SC-M1-06 | A | Đổi Loại KH / Mã đầu mối → option Mã CIC, Mã KH, Tên tệp, CCCD/CMND lọc lại; giá trị cũ bị xóa | BR-015 `[A-Q22]` |
| SC-M1-07 | H | Mã KH khớp chính xác TTC03, chọn nhiều | BR-015 |
| SC-M1-08 | H | Lọc Nhóm KH / Trạng thái (chọn nhiều, OR trong bộ lọc) | BR-016 `[A-Q23]` |
| SC-M1-09 | A | Cột CCCD (Cá nhân) / MSDN (Tổ chức) đổi sau Tìm kiếm; bộ lọc CCCD/CMND lấy CN008/TC011 | BR-017 `[A-Q25]`, `[A-Q23]` |
| SC-M1-10 | E | Từ ngày > Đến ngày (mỗi cặp) → ERR_003, không tìm; Từ = Đến; nhập 1 vế | BR-018 `[A-Q24]` |
| SC-M1-11 | A | Thêm bộ lọc: bật/tắt; 3 bộ lọc bắt buộc không tắt được; tắt bộ lọc xóa giá trị | BR-019 `[A-Q29]` |
| SC-M1-12 | H | Sắp xếp Ngày cập nhật mới nhất trên cùng | BR-020 |
| SC-M1-13 | A | Cấu hình hiển thị: ẩn/hiện, kéo thả, Áp dụng; 4 cột bắt buộc không ẩn; lưu sau tải lại | BR-021 `[A-Q29]` |
| SC-M1-14 | A | Xuất trang hiện tại / theo bộ lọc / In; tên HoSoPhapLy_ddmmyyyy; mọi trường cấu hình; không có dữ liệu → chỉ tiêu đề | BR-022 `[A-Q28]` |
| SC-M1-15 | H/S | Menu Thao tác theo 4 trạng thái: Xem luôn có; Xử lý hồ sơ chỉ Chờ xem xét | BR-023 |
| SC-M1-16 | A | Ô chọn: chỉ Chờ xem xét bật; chọn tất cả chỉ chọn dòng bật; trạng thái chọn một phần; đổi trang/tìm lại xóa lựa chọn | BR-024 `[A-Q19]` |
| SC-M1-17 | A | Chọn hồ sơ đầu tiên → banner INF_009 đúng loại KH; bỏ hết → tắt banner | BR-025 `[A-Q18]` |
| SC-M1-18 | H | Dải thao tác: ẩn khi 0, hiện "Đã chọn n hồ sơ"; Bỏ chọn bỏ hết | BR-026 |
| SC-M1-19 | H | Xử lý hồ sơ trên dải: 1 hồ sơ D10/D11 → MH-004; 1 hồ sơ Q11 → MH-005; ≥2 → MH-008 | BR-026 |
| SC-M1-20 | H | Tra cứu theo Nhóm "Mới - Không QHTD" (UC-0541) và "Thay đổi TTQT" (UC-0547) | UC-0541, 0547 |
| SC-M1-21 | H | Danh sách chỉ gồm hồ sơ loại Pháp lý, Hợp lệ, D10/D11/Q11 | BR-002 |
| SC-M1-22 | A | Phân trang: 20 mặc định, đổi số bản ghi/trang tới 5000, nhập số trang vượt → trang cuối | BR-027 `[A-Q27]` |
| SC-M1-23 | H | Badge Trạng thái 4 màu (xám/cam/xanh lá/đỏ) | [P1] #37 |
| SC-M1-24 | H | Tra cứu kết hợp leo thang (Nhóm T) | [P1] Luồng chính |
| SC-M1-25 | S | Gợi ý Mã đầu mối chỉ gồm đầu mối thuộc TCTD được phân quyền; gõ mã/tên đầu mối ngoài quyền → không có gợi ý | BR-014 `[BA-Q21]` |

### M2 / M3 — Xem chi tiết

| ID | Loại | Kịch bản | Nguồn |
|---|---|---|---|
| SC-M2-01 / SC-M3-01 | H | Xem → popup mở tab Thông tin hồ sơ, giá trị đang lưu | BR-028 |
| SC-M2-02 / SC-M3-02 | H | KH Tổ chức hiển thị TTC + TC (M2 gồm TC024/025/026); KH Cá nhân hiển thị TTC + CN; M3 đúng tập Q11 | [P2] AC#3, [P3] AC#2–#3 |
| SC-M2-03 / SC-M3-03 | A | Lý do hiện khi Đã xử lý / Từ chối; ẩn khi Chờ cấp mã / Chờ xem xét | BR-029 |
| SC-M2-04 | A | Khối lặp TC024/025/026 có 0, 1, nhiều bản ghi | [P2] #40–#42 `[A-Q37]` |
| SC-M2-05 / SC-M3-04 | H | Mã CIC hiển thị khi có; Chờ cấp mã → trống | [P2] #7 |
| SC-M2-06 | H | Hover mã chỉ tiêu → tooltip tên | BR-030 |
| SC-M2-07 | H | Tab Lịch sử: dòng theo KH (TTC00+TTC03) qua các kỳ, mới nhất trên cùng, đủ 8 cột, chỉ trường thay đổi | BR-031 `[A-Q36]` |
| SC-M2-08 | A | Nội dung dòng theo Hành động (Tiếp nhận, Cập nhật tự động, Cấp mã CIC, Cập nhật, Từ chối); tooltip Người cập nhật | BR-031 `[A-Q36]` |
| SC-M2-09 | A | Chuyển tab qua lại; Đóng → về MH-001 | [P2] ALT-01 |

### M4 / M5 — Xử lý một hồ sơ (M5 lặp lại các kịch bản tương ứng với tập Q11, bỏ SC-M4-16)

| ID | Loại | Kịch bản | Nguồn |
|---|---|---|---|
| SC-M4-01 | H | Mở MH-004 từ menu Thao tác / từ dải (1 hồ sơ): đủ 2 thẻ, tóm tắt, công tắc tắt, bảng 3 cột | [P4] Luồng chính bước 1 |
| SC-M4-02 | H | Thẻ CIC: Mã CIC, Loại KH tại CIC, TCTD có liên quan (;) + tooltip tên NV-16 | BR-047 `[A-Q15]` |
| SC-M4-03 | A | Loại KH lệch → tô nền cả hai ô, vẫn cho Cập nhật/Từ chối; cột CIC lấy kho chuẩn theo Mã CIC | BR-047, 033 `[A-Q15]` |
| SC-M4-04 | H | Dropdown Ngày báo cáo TCTD: 1/2/3/4 phiên bản → tối đa 3, mặc định mới nhất; trùng/trống ngày | BR-032 `[BA-Q03]`, `[A-Q35]` |
| SC-M4-05 | A | Đổi phiên bản → nạp lại cột TCTD, tô lại, tính lại tóm tắt | BR-032, 037 `[A-Q10]` |
| SC-M4-06 | H | Hover mã chỉ tiêu → tooltip | BR-030 |
| SC-M4-07 | H | ★ trước chỉ tiêu quan trọng | BR-035, 009 |
| SC-M4-08 | A | Nhãn C06 hiện / ẩn theo cờ xác thực | BR-034 `[A-Q42]` |
| SC-M4-09 | H | Tô nền đúng ô khác (cột TCTD, cột CIC riêng biệt), không tô dòng, không đổi màu chữ | BR-036, 037 |
| SC-M4-10 | A | Tóm tắt số khác biệt / số quan trọng; bật công tắc → chỉ dòng khác + tiêu đề nhóm; 0 khác biệt | BR-045 `[A-Q10]` |
| SC-M4-11 | H | Cuộn bảng: hàng tiêu đề + ô chọn Ngày báo cáo cố định | BR-046 |
| SC-M4-12 | H | Cập nhật → MH-006 → lý do hợp lệ → SUC_001, Đã xử lý, lý do lưu, ghi kho TCTD theo Mã CIC, về MH-001 | BR-040 `[BA-Q02]`, `[A-Q33]` |
| SC-M4-13 | A | Sau Cập nhật, mở hồ sơ khác cùng KH: cột CIC giữ giá trị CICinfo cũ; hồ sơ vừa xác nhận là phiên bản mới nhất (mặc định) ở dropdown cột TCTD | BR-040, 032 `[BA-Q02]` |
| SC-M4-14 | H | Từ chối → MH-007 → lý do hợp lệ → Từ chối, lý do lưu, kho giữ nguyên, về MH-001 | BR-041 |
| SC-M4-15 | A | So sánh: khoảng trắng đầu/cuối, NULL vs rỗng, hoa/thường | BR-048 `[A-Q11]` |
| SC-M4-16 | A | Bảng TC024/025/026: khớp khóa, thiếu ở TCTD/CIC, chỉ có ở TCTD/CIC, khóa trùng/rỗng (chỉ M4, Tổ chức) | BR-049 `[A-Q12]` |
| SC-M4-17 | A | Hủy trên MH-004 → về MH-001, hồ sơ vẫn Chờ xem xét, giữ bộ lọc/trang | [P4] ALT-03 `[A-Q33]` |
| SC-M4-18 | A | KH có hồ sơ của nhiều TCTD cùng Mã CIC → dropdown/cột TCTD chỉ gồm hồ sơ cùng đầu mối, không gồm chính hồ sơ đang xem xét | BR-032 `[BA-Q03]` |

### M6 — Popup MH-006 / MH-007 (sinh trong từng sheet M4, M5, M7)

| ID | Loại | Kịch bản | Nguồn |
|---|---|---|---|
| SC-M6-01 | E | Lý do trống / toàn khoảng trắng → ERR_001 dưới ô, viền đỏ, popup giữ, không ghi | BR-038 `[A-Q32]` |
| SC-M6-02 | E | Lý do 999/1000/1001 ký tự: nhập vượt → chặn tại 1000 + ERR_023; paste vượt → cắt còn 1000 + ERR_023 | BR-038 `[U-Q32]` (user chốt B5b GAP-01) |
| SC-M6-03 | A | Hủy popup → ở lại màn xử lý, mở lại giữ lý do | [P4] ALT-02 `[A-Q32]` |
| SC-M6-04 | A | Icon X đóng popup như Hủy | `[A-Q31]` |
| SC-M6-05 | H | MH-006 hiển thị CONF_001 "cập nhật … thông tin pháp lý quan trọng của khách hàng" | CONF_001 `[A-Q31]` |
| SC-M6-06 | H | MH-007 hiển thị CONF_001 "từ chối cập nhật …" | CONF_001 |
| SC-M6-07 | E | Bấm xác nhận nhiều lần liên tiếp → chỉ một lần ghi, nút loading/khóa | [QT] Button `[A-Q39]` |

### M7 — Xử lý đồng thời (FEAT-06 + biến thể Q11 FEAT-07)

| ID | Loại | Kịch bản | Nguồn |
|---|---|---|---|
| SC-M7-01 | H | Mở MH-008 với n hồ sơ: tiêu đề (n), dòng phụ, mọi hồ sơ được chọn, hồ sơ đầu tiên đang xem | BR-042 `[A-Q34]` |
| SC-M7-02 | H | Mỗi hồ sơ hiển thị Tên KH, Mã KH, đầu mối, Mã CIC, chip khác biệt (★) | BR-042 |
| SC-M7-03 | A | Chọn hồ sơ khác → vùng so sánh chuyển; công tắc/phiên bản đặt lại mặc định | BR-042 `[A-Q34]` |
| SC-M7-04 | A | Bỏ chọn / chọn lại → mờ / bình thường, vẫn xem được; số trên nút thay đổi | BR-042 |
| SC-M7-05 | E | Bỏ chọn hết (n = 0) → Từ chối (0), Cập nhật (0) bị khóa | BR-042 |
| SC-M7-06 | H | Mã CIC mỗi hồ sơ và cột CIC theo Mã CIC của hồ sơ | BR-043 `[A-Q14]` |
| SC-M7-07 | H | Cập nhật (n) → MH-006 → một lý do → mọi hồ sơ còn chọn Đã xử lý, cùng lý do, SUC_001; hồ sơ bỏ chọn giữ Chờ xem xét | BR-044 |
| SC-M7-08 | H | Từ chối (n) → MH-007 → mọi hồ sơ còn chọn Từ chối, cùng lý do | BR-044 |
| SC-M7-09 | A | Công tắc mặc định bật; tắt → hiện đủ chỉ tiêu | BR-045 |
| SC-M7-10 | A | Hủy MH-008 → về MH-001, mọi hồ sơ Chờ xem xét | [P6] ALT-03 |
| SC-M7-11 | A | Biến thể Q11 (FEAT-07): tập chỉ tiêu Q11 trong vùng so sánh và chip | [P7] AC#1–#4 `[A-Q13]` |
| SC-M7-12 | A | Lô 2 hồ sơ (biên dưới) và lô nhiều hồ sơ (cuộn danh sách) | BR-026, 042 |
| SC-M7-13 | E | Một hồ sơ trong lô thất bại / đã đổi trạng thái → cả lô không được cập nhật/từ chối, mọi hồ sơ giữ Chờ xem xét, không có SUC_001 | BR-044 `[BA-Q07]` |
| SC-M7-14 | E | Lỗi ở bước C06/nghi trùng/INF_011 sau khi cập nhật lô → rollback toàn bộ lô (kho TCTD, trạng thái, lý do về như trước) | BR-010, 011, 012 `[BA-Q07]` |

### M8 — Nghiệp vụ tự động, trạng thái & tích hợp

| ID | Loại | Kịch bản | Nguồn |
|---|---|---|---|
| SC-M8-01 | H | Tiếp nhận KH mới, khóa có ở tệp khác → "Mới - Có QHTD", Chờ cấp mã, chuyển cấp mã | BR-004 |
| SC-M8-02 | H | Tiếp nhận KH mới, khóa không có ở tệp khác → "Mới - Không QHTD", Chờ cấp mã | BR-004 |
| SC-M8-03 | H | KH cũ, không đổi chỉ tiêu quan trọng → "Không thay đổi TTQT", Đã xử lý, lịch sử "Cập nhật tự động" | BR-007 `[BA-Q01]` |
| SC-M8-04 | H | KH cũ, đổi chỉ tiêu quan trọng → "Thay đổi TTQT", Chờ xem xét, đánh dấu chỉ tiêu đổi | BR-008 `[BA-Q01]` |
| SC-M8-05 | A | Hồ sơ KH mới thứ hai khi hồ sơ trước còn Chờ cấp mã → cũng Chờ cấp mã; cấp mã cập nhật cả hai | `[A-Q04]` |
| SC-M8-06 | H | FUNC-XLDL-013 cấp mã → Đã xử lý, Mã CIC hiển thị, lịch sử "Cấp mã CIC" | BR-005 |
| SC-M8-07 | A | Nhận hồ sơ QHTD cho KH không QHTD → cờ đổi; Nhóm KH giữ nguyên | BR-006 `[A-Q17]` |
| SC-M8-08 | H | Ánh xạ Trạng thái ↔ Nhóm KH hợp lệ (Chờ cấp mã ↔ Mới; Chờ xem xét/Từ chối ↔ Thay đổi TTQT) | BR-016 |
| SC-M8-09 | H | INF_010: mỗi tệp một thông báo, đúng tên tệp + số hồ sơ, gửi cán bộ được phân quyền TCTD | BR-008 `[A-Q09]` |
| SC-M8-10 | H | Cập nhật KH cá nhân đổi CCCD/CMND/họ tên/ngày sinh/giới tính → chuyển C06; không đổi → không chuyển | BR-010 `[A-Q16]` |
| SC-M8-11 | H | Sau cập nhật → KH xuất hiện ở luồng kiểm tra nghi trùng FUNC-XLDL-013 | BR-011 `[A-Q16]` |
| SC-M8-12 | H | Tệp hết Chờ xem xét, có ≥1 Từ chối → INF_011 (Push + Email) với danh sách + lý do, liên kết FUNC-WEB-002 | BR-012 `[A-Q08]` |
| SC-M8-13 | A | Tệp hết Chờ xem xét, 0 Từ chối → không gửi; tệp còn Chờ xem xét → không gửi | BR-012 `[A-Q08]` |
| SC-M8-14 | H | Tiếp nhận ghi dòng "Tiếp nhận"; hồ sơ không hợp lệ không vào danh sách | BR-031, 002, [P8] EXC-01 |
| SC-M8-15 | S | User không có quyền: menu ẩn | BR-001 |
| SC-M8-16 | S | URL trực tiếp → ERR_011, không dữ liệu, ở lại trang; ROLE + 0 TCTD → menu hiện, danh sách rỗng; thu hồi quyền giữa chừng → thao tác bị chặn, ERR_011 | BR-001 `[BA-Q38]` |
| SC-M8-17 | S | Cán bộ chỉ thấy hồ sơ của TCTD được phân quyền (tra cứu, xem, xử lý, xuất) | Ma trận phân quyền |
| SC-M8-18 | C | Hai cán bộ cùng xử lý một hồ sơ / mở từ danh sách cũ → người sau bị chặn, toast "Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.", tự thoát popup/màn và reload sau khi toast tắt | `[BA-Q06]` (nội dung chốt B5b GAP-06) |
| SC-M8-19 | C | Hai hồ sơ Chờ xem xét cùng KH, xử lý ngược thứ tự → đều cho phép; kho TCTD lưu theo lần xác nhận sau cùng | `[BA-Q05]` |
| SC-M8-20 | S | Dữ liệu cá nhân hiển thị/xuất không che đúng SRS (nhật ký truy cập ngoài phạm vi) | Phân loại dữ liệu `[BA-Q40]` |
| SC-M8-21 | A | Kho TCTD và CICinfo lệch nhau: hồ sơ trùng giá trị kho TCTD → Không thay đổi TTQT / Đã xử lý; khác kho TCTD → Thay đổi TTQT / Chờ xem xét | BR-003, 008 `[BA-Q01]` |

**Tổng scenario:** 94 mã (M1 25 · M2/M3 9 · M4/M5 18 · M6 7 · M7 14 · M8 21; M3 và M5 dùng lại mã của M2/M4 với tập chỉ tiêu Q11) — **0 `PENDING-Q&A`**; 10 kịch bản trước đây PENDING đã có expected theo câu trả lời BA/user (2026-10-12).
