---
feature: Tệp có cấu trúc chưa xác định (CXĐ) — Gửi / Tiếp nhận / Xử lý
project: CIC
started: 2026-10-09
last_updated: 2026-10-09
current_step: B2
mode: COMPACT (dự kiến — >2 modules & >80 TC)
output_script: scripts/gen_tc_tepcxdcic.py
output_xlsx: practices/testcases/CIC/TepCXD_CIC_TestCases.xlsx
qa_file: practices/Q&A/TepCXD_CIC_QA.md
tc_prefix: CXD
tc_count: 0
---

## ✅ Bước 1 — Context (CONFIRMED 2026-10-09)

**User xác nhận:** "xác nhận sang B2" (2026-10-09).

**Tài liệu gốc (Confluence space CIC — đã đọc toàn bộ text, 18 trang):**

| Tag | Page ID | Tài liệu |
|---|---|---|
| P1 | 26979982 | IV.6.5.4. TCTD gửi báo cáo có cấu trúc chưa xác định (v5) |
| P1a | 26979985 | IV.6.5.4.1. Gửi báo cáo |
| P1b | 26979987 | IV.6.5.4.2. Tra cứu báo cáo đã gửi |
| P2 | 26968271 | IV.3.1.3. Tiếp nhận dữ liệu có cấu trúc chưa xác định (v10) |
| P2a | 26968323 | Danh sách tệp có cấu trúc chưa xác định |
| P3 | 26017971 | IV.3.2.2. Xử lý dữ liệu có cấu trúc chưa xác định (v5) |
| P3a | 26981869 | IV.3.2.2.1. Danh sách kiểm tra nội dung tệp CXĐ |
| — | 26981871 / 26981873 / 34242682 | Trang chứa (rỗng) |
| P3b | 34242667 | Thêm mới quy tắc chuyển đổi |
| P3c | 34242669 | Sửa quy tắc chuyển đổi |
| P3d | 34242671 | Xóa quy tắc chuyển đổi |
| P3e | 34242673 | Phê duyệt/Từ chối/Ngưng sử dụng/Kích hoạt |
| P3f | 34242676 | Danh sách quy tắc chuyển đổi |
| P3g | 34242678 | Xem chi tiết quy tắc chuyển đổi |
| P3h | 34242685 | Chuyển đổi thủ công |
| P3i | 34242687 | Xem trước (Preview) kết quả chuyển đổi |
| BUS | 1212453 | III.2. Bảng mã lỗi (đọc các dòng mã được dẫn chiếu) |

**Ảnh mockup đã xem:** P1b, P3a, P3b, P3e, P3f, P3h, P3i. **Chưa xem được** (lỗi kết nối MCP khi tải ảnh): P1a, P2a; chưa tải: P1, P2, P3, P3c, P3d, P3g.

**Scope đã xác nhận:**
- **M1 Gửi báo cáo (P1a)** — chỉ nhánh "Tệp có cấu trúc khác" (CXĐ): MH 3.1 chọn tệp (radio Phân loại, Dropzone, Thêm tệp, bảng 16 cột, Mô tả tệp, Ghi chú, Hủy, Lưu & Gửi) + MH 3.2 quá trình tải (4 trạng thái tải lên).
- **M2 Tra cứu báo cáo đã gửi (P1b)** — Cài đặt hiển thị, Kết xuất Excel, 11 bộ lọc, lưới 3 nhóm badge trạng thái, phân trang, popup Xem chi tiết (Vùng 1/Vùng 2).
- **M3 Luồng tiếp nhận tự động (P2)** — BIZ: rule tên tệp → Đã tiếp nhận / CIC từ chối, thông báo TCTD.
- **M4 Danh sách tệp CXĐ (P2a)** — bộ lọc, lưới, Xem chi tiết, Xử lý dữ liệu, 403/phạm vi dữ liệu.
- **M5 Danh sách kiểm tra nội dung tệp CXĐ (P3a)** — MH1 danh sách + Chạy lại kiểm tra + popup Chuyển đổi; MH2 kiểm tra hệ thống chỉ tiêu; MH3 xem dữ liệu bảng raw.
- **M6 Danh sách / Xem chi tiết quy tắc chuyển đổi (P3f, P3g).**
- **M7 Thêm mới / Sửa quy tắc chuyển đổi (P3b, P3c).**
- **M8 Xóa / Phê duyệt / Từ chối / Ngưng sử dụng / Kích hoạt (P3d, P3e).**
- **M9 Chuyển đổi thủ công + Preview kết quả (P3h, P3i)** + popup Xác nhận lưu / Trùng tên tệp / Xác nhận hủy bỏ.
- **BIZ E2E:** gửi → tiếp nhận → kiểm tra cấu trúc → kiểm tra chỉ tiêu → lưu raw → chuyển đổi (không cần/tự động/thủ công) → preview → lưu → kích hoạt XL07; vòng đời quy tắc chuyển đổi.

**Out of scope:** nhánh Tệp theo Thông tư & Tệp phi cấu trúc; nội dung luồng XL07 (chỉ kiểm tra việc kích hoạt); kênh H2H/API (chỉ hiển thị giá trị Kênh gửi); màn cấu hình mẫu tệp/ngưỡng/quy tắc kiểm tra chỉ tiêu.

**Mã TC:** `CXD_###` (đề xuất mặc định ở B1, user không phản đối).

## ⏳ Bước 2 — Q&A [PENDING — chờ BA/PO trả lời]

- **File:** `practices/Q&A/TepCXD_CIC_QA.md` (Full Review, 19 nhóm CR-A…CR-S, self-check (a)–(f) PASS 2026-10-09)
- **Verdict:** BLOCKED — 66 Q-ID: 15 BLOCKING, 47 WARNING, 4 SUGGESTION
- **BLOCKING:** Q02, Q04, Q06, Q07, Q13, Q22, Q32, Q34, Q37, Q38, Q39, Q41, Q43, Q47, Q50
- **⚠️ Cần BA/PO (không dùng làm assumption):** Q02, Q04, Q07, Q13, Q22, Q32, Q37, Q38, Q39, Q41, Q43, Q44, Q50, Q52, Q59, Q62
- **Phát hiện từ mockup (không có trong text):** popup Xác nhận chuyển đổi có Lý do bắt buộc (Q64); MH2 có nút Chấp nhận/Từ chối vượt ngưỡng (Q40); trạng thái ánh xạ "Bỏ qua" (Q58); Preview nhiều tab (Q62); BUS-265/266 bị gán ngược ở P3h (Q46)
- **Handoff:** chờ "Dùng assumptions, tiếp tục B3" hoặc "Đã trả lời Q&A, tiếp tục B3"
## ⏳ Bước 3 — Modules & Field Inventory
## ⏳ Bước 4 — Traceability [PENDING]
## ⏳ Bước 5 — TC Summary
## ⏳ Bước 5b — TC Lead Review Gate [PENDING]
## ⏳ Bước 6 — Template Mapping [SKIP-COMPACT dự kiến]
## ⏳ Bước 7 — Output
