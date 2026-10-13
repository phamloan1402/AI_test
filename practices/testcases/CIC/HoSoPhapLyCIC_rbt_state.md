---
feature: "[FUNC-XLDL-009] XLDL hồ sơ pháp lý"
project: CIC
started: 2026-10-12
last_updated: 2026-10-12
current_step: B7 (chờ user duyệt B5b / bộ TC final)
mode: COMPACT (>2 modules & >80 TC)
output_script: scripts/gen_tc_hosophaplycic.py
output_xlsx: practices/testcases/CIC/HoSoPhapLyCIC_TestCases.xlsx
qa_file: practices/Q&A/HoSoPhapLyCIC_QA.md
tc_prefix: HSPL
tc_count: 1721
working_file: practices/testcases/CIC/HoSoPhapLyCIC_B3_B4.md
---

## ✅ Bước 1 — Context (CONFIRMED 2026-10-12)

**User xác nhận:** "ok B1, sang B2" (2026-10-12).

**Tài liệu gốc (Confluence space CIC — đã đọc toàn bộ text, 9 trang):**

| Tag | Page ID | Tài liệu |
|---|---|---|
| P0 | 1212957 | IV.3.2.5. [FUNC-XLDL-009] XLDL hồ sơ pháp lý (v1.8 approved) — BR-001…049, RBAC, Sơ đồ trạng thái, Luồng XL13 |
| P1 | 1213026 | FEAT-XLDL-009-01 Tra cứu danh sách hồ sơ pháp lý |
| P2 | 6029984 | FEAT-XLDL-009-02 Xem chi tiết hồ sơ pháp lý tệp D10/D11 |
| P3 | 6030523 | FEAT-XLDL-009-03 Xem chi tiết hồ sơ pháp lý tệp Q11 |
| P4 | 6030601 | FEAT-XLDL-009-04 Xử lý hồ sơ pháp lý tệp D10/D11 |
| P5 | 6031014 | FEAT-XLDL-009-05 Xử lý hồ sơ pháp lý tệp Q11 |
| P6 | 6031340 | FEAT-XLDL-009-06 Xử lý đồng thời hồ sơ pháp lý tệp D10/D11 |
| P7 | 43521153 | FEAT-XLDL-009-07 Xử lý đồng thời hồ sơ pháp lý tệp Q11 |
| P8 | 43521156 | FEAT-XLDL-009-08 Xử lý tự động hồ sơ pháp lý khi tiếp nhận (chạy nền) |

**Ảnh mockup đã xem:** P1 (MH-001 trống / Tổ chức / Cá nhân + các bản cũ), P6 (MH-008, popup MH-006/MH-007 + các bản cũ). **Không tải được** (MCP "Connection closed"): P2, P4 (thử 2 lần); chưa tải: P0, P3, P5, P7.

**Scope đã xác nhận:**
- **M1 MH-001 Danh sách hồ sơ pháp lý (P1)** — Cấu hình hiển thị, Xuất Excel (3 lựa chọn), 3 bộ lọc bắt buộc + bộ lọc bổ sung (Mã CIC, Mã KH, Người cập nhật, Nhóm KH, Trạng thái, 2 khoảng ngày; Tên tệp, CCCD/CMND mặc định tắt), Thêm bộ lọc / Làm mới / Tìm kiếm, dải thao tác hàng loạt + banner INF_009, lưới (checkbox, 16 cột, badge, menu Thao tác, empty state), phân trang 20/5000.
- **M2 MH-002 Xem chi tiết D10/D11 (P2)** — tab Thông tin hồ sơ (thẻ KH, Lý do, KB001–004, Tổ chức TTC/TC001–023 + TC024/025/026 dạng khối lặp, Cá nhân TTC/CN001–022, tooltip) + tab Lịch sử cập nhật (8 cột) + Đóng.
- **M3 MH-003 Xem chi tiết Q11 (P3)** — như M2 với tập chỉ tiêu Q11.
- **M4 MH-004 Xử lý D10/D11 (P4)** — 2 thẻ, tóm tắt khác biệt, công tắc (mặc định tắt), bảng so sánh 3 cột (★, tooltip, dropdown Ngày báo cáo TCTD ≤3, nhãn C06, tô nền ô, BR-048/049, sticky header), Hủy/Từ chối/Cập nhật.
- **M5 MH-005 Xử lý Q11 (P5)** — như M4 với tập chỉ tiêu Q11, không có chỉ tiêu dạng bảng.
- **M6 MH-006/MH-007 popup xác nhận Cập nhật/Từ chối** — CONF_001, Lý do textarea bắt buộc ≤1000 + bộ đếm, Hủy/xác nhận, ERR_001/ERR_023, SUC_001.
- **M7 MH-008 Xử lý đồng thời (P6, P7)** — danh sách hồ sơ đã chọn (checkbox, chip chỉ tiêu khác biệt, mờ khi bỏ chọn), vùng so sánh (công tắc mặc định bật), Hủy / Từ chối (n) / Cập nhật (n), một lý do chung.
- **M8 BIZ tự động & tích hợp (P8, P0)** — phân loại 3 nhánh theo TTC00+TTC03, Chờ cấp mã → Đã xử lý khi cấp mã, cờ QHTD, C06 (BR-010), nghi trùng (BR-011), INF_010/INF_011, lịch sử theo KH, state machine.
- **RBAC** — ROLE-CBTTXLDL (FEAT-01…07), user không quyền (ERR_011), phạm vi dữ liệu theo TCTD được phân quyền.

**Out of scope:** logic cấp mã CIC & bộ quy tắc nghi trùng (FUNC-XLDL-013), xác thực C06 (FUNC-XLDL-035), danh mục chỉ tiêu quan trọng (FUNC-XLDL-027), mẫu thông báo (FUNC-HTVH-013), gộp mã (FUNC-XLDL-052), màn FUNC-WEB-002 (chỉ kiểm liên kết), hồ sơ lỗi (FUNC-XLDL-010), đầu vào khác D10/D11/Q11.

**Mã TC:** `HSPL_###` (đề xuất ở B1, user duyệt cùng scope).

## ✅ Bước 2 — Q&A Resolved (BA trả lời + assumptions — 2026-10-12)

- **BA/PO trả lời (2026-10-12, nhập qua `practices/Q&A/HoSoPhapLyCIC_QA.xlsx`, đã đồng bộ vào `.md` §3 và §5):** Q01, Q02, Q03, Q04, Q05, Q06, Q21, Q38, Q40 — đều theo Option A / phương án `>> Chọn` (Q40: ngoài phạm vi).
- **Q07:** ô trả lời chứa cả hai option → user chốt **Option B — all-or-nothing** (2026-10-12).
- **Verdict tính lại:** CONDITIONAL (0 BLOCKING, 0 Q-ID mở; WARNING còn lại dùng assumption user đã chấp thuận).

- **User phản hồi:** "Dùng assumptions, tiếp tục B3" (2026-10-12).
- **Assumption áp dụng:** dòng `>> Chọn` của các Q-ID WARNING/SUGGESTION không ⚠️: Q04, Q08–Q20, Q22–Q37, Q39, Q41, Q42.
- **(Trước khi BA trả lời) không dùng làm assumption:** Q01, Q02, Q03, Q05, Q06, Q07, Q21, Q38, Q40 — nay đã có câu trả lời, trừ Q07.
- **Bổ sung từ [QT] (B3):** icon lọc cột trên mockup MH-001 = quy tắc QT C14 (lọc theo cột trên trang hiện tại) → áp dụng; icon sắp xếp cột vẫn ngoài phạm vi `[A-Q26]`.

### Lịch sử B2

- **File:** `practices/Q&A/HoSoPhapLyCIC_QA.md` (Full Review, 19 nhóm CR-A…CR-S, self-check (a)–(f) PASS 2026-10-12)
- **Verdict:** BLOCKED — 42 Q-ID: 3 BLOCKING, 37 WARNING, 2 SUGGESTION
- **BLOCKING:** Q01 (baseline so sánh khi tiếp nhận), Q02 (kho đích & điểm kiểm chứng sau cập nhật), Q03 (phạm vi cột Hồ sơ tại TCTD)
- **⚠️ Cần BA/PO (không dùng làm assumption):** Q01, Q02, Q03, Q05, Q06, Q07, Q21, Q38, Q40
- **Phát hiện từ mockup/đối chiếu:** BR-025 không thể kích hoạt do BR-013 (Q18); icon lọc/sắp xếp cột trên lưới (Q26); thiếu ô Đến trang (Q27); popup xác nhận có icon X + nút "Xác nhận" (Q31); tên cột CCCD/MSDN không thống nhất (Q25); BR-039 không tồn tại (Q41)
- **Handoff:** chờ "Dùng assumptions, tiếp tục B3" hoặc "Đã trả lời Q&A, tiếp tục B3"
## ✅ Bước 3 — Modules & Field Inventory (DONE 2026-10-12)

- **File:** `practices/testcases/CIC/HoSoPhapLyCIC_B3_B4.md` §B3a–B3b
- **Modules:** M1 Danh sách · M2 Xem D10/D11 · M3 Xem Q11 · M4 Xử lý D10/D11 · M5 Xử lý Q11 · M6 Popup MH-006/007 (sinh trong M4, M5, M7) · M7 Xử lý đồng thời (+Q11) · M8 Nghiệp vụ tự động/tích hợp/RBAC
- **Sheet:** M1_DanhSach, M2_ChiTiet_D10D11, M3_ChiTiet_Q11, M4_XuLy_D10D11, M5_XuLy_Q11, M7_XuLyDongThoi, M8_NghiepVu_TichHop
- **Nhóm Common TC:** A, C, D22–D28 (ô search), G (Lý do ×2 mỗi sheet M4/M5/M7), H, I, J, K, M (Xuất Excel 7, CONF 8/popup), S, T, U, W3
- **Ước lượng:** ~1.300 TC
## ✅ Bước 4 — Traceability [APPROVED 2026-10-12]

- **User xác nhận:** "ok duyệt B4" (2026-10-12) — Work Log `HoSoPhapLyCIC-20261012-02`; giữ đủ popup/Lý do ở M4/M5/M7 theo [CHECK 10].

- **File:** `practices/testcases/CIC/HoSoPhapLyCIC_B3_B4.md` §B4 — 4 tầng (BR-001…049 từng dòng, 12 mã thông báo, RBAC, state T1–T9, NFR, CMP) + 94 scenario (0 PENDING-Q&A — cập nhật theo câu trả lời BA/user 2026-10-12)
## ✅ Bước 5 — TC Summary (COMPACT, chạy thử 2026-10-12)

- **Script:** `scripts/gen_tc_hosophaplycic.py` → `practices/testcases/CIC/HoSoPhapLyCIC_TestCases.xlsx` (bản chạy thử)
- **Số TC:** M1 448 · M2 103 · M3 93 · M4 241 · M5 229 · M7 270 · M8 21 = **1.405** (Giao diện 1.130, Chức năng 275; Cao 523, Trung bình 684, Thấp 198)
- **Verification:** đủ Nhóm A mọi màn/popup; G 41×6; 48/48 BR; 11/11 mã thông báo
## ⏳ Bước 5b — TC Lead Review Gate [GAP đã xử lý 2026-10-12 — chờ user duyệt bộ final]

- **Report:** `practices/testcases/CIC/tc_review_HoSoPhapLyCIC.md` (đã ghi quyết định user) — 12 GAP (đề xuất bổ sung: GAP-01 ERR_023, GAP-05 loading công tắc, GAP-12 M8 phân loại theo tệp/loại KH; còn lại N/A / xác nhận)
## ✅ Bước 6 — Template Mapping [SKIP-COMPACT]
## ✅ Bước 7 — Output (2026-10-12)

- **Script:** `scripts/gen_tc_hosophaplycic.py`
- **Excel:** `practices/testcases/CIC/HoSoPhapLyCIC_TestCases.xlsx` — 7 sheet + Tổng hợp
- **Số TC final:** M1 594 · M2 174 · M3 138 · M4 255 · M5 243 · M7 284 · M8 33 = **1.721**
- **M2/M3 bổ sung (user 2026-10-12):** "Kiểm tra xem chi tiết không thành công" (API lỗi, API timeout, hết phiên, thu hồi quyền giữa chừng) và "Kiểm tra xem lịch sử thay đổi không thành công" (4 ca tương tự) — 8 TC/sheet
- **Đối chiếu toàn bộ `common1.xlsx` (2026-10-12):** +65 TC — title mọi màn (12), DatePicker định dạng/bắt buộc/icon calendar/copy-paste/xóa (10), cột Thao tác (3), chọn/bỏ nhiều bản ghi (2), leo thang tìm kiếm 3/5/6 có dữ liệu + 3/4/5/6 không dữ liệu (7), xuất Excel thành công kèm danh sách trường (3), xóa Mã đầu mối (1), M4/M5/M7 mỗi sheet: 2 tab cùng tài khoản (2), 2 cán bộ cùng từ chối (1), Cập nhật/Từ chối khi API lỗi/timeout/hết phiên (6). Không lấy: ngày > hiện tại (user bỏ K09–K11), Textbox Tên tệp và link Tên tệp (SRS là combobox), phân quyền theo từng thao tác (SRS chỉ có 1 vai trò đủ quyền)
- **Bổ sung theo mẫu `practices/testcases/common1.xlsx` (user yêu cầu 2026-10-12):** button + popup Cấu hình hiển thị (80 TC: title, ô tìm kiếm trường, checkbox 16 cột, kéo thả 16 cột, Bỏ chọn, Chọn tất cả, Áp dụng, icon X), button + popup Thêm bộ lọc (16 TC: 12 bộ lọc), tìm kiếm không thành công thêm API lỗi / API timeout / hết token (thông báo "Đã có lỗi xảy ra. Vui lòng thử lại." theo mẫu)
- **Cấu trúc tìm kiếm M1 (user yêu cầu 2026-10-12):** "Kiểm tra tìm kiếm thành công có dữ liệu" (19) / "... không có dữ liệu" (16: 13 điều kiện + tổ hợp + xuất Excel rỗng + tìm lại) / "Kiểm tra thao tác trên danh sách thành công" (9) / "Kiểm tra tìm kiếm không thành công" (4 — WAR_009, ERR_003)
- **Thay đổi sau B5b:** +127 TC (GAP-02 +14, GAP-03 +2, GAP-04 +96, GAP-05 +3, GAP-12 +12); sửa 12 TC ERR_023 (GAP-01) và 8 TC thông báo Q06 (GAP-06) — REOPEN `HoSoPhapLyCIC-20261012-03`
- **Điều kiện môi trường test:** `tc_review_HoSoPhapLyCIC.md` §Điều kiện môi trường test
- **Hiển thị tên màn hình (user yêu cầu 2026-10-12):** nội dung Excel không dùng mã MH-00x; script tự đổi sang `màn hình/popup "<tên màn hình>"` (hàm `expand_screen_codes`). Tài liệu nội bộ (Q&A, B3/B4) vẫn giữ mã MH để truy vết với SRS.
