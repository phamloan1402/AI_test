---
feature: Cấu trúc kiểm tra phân quyền dữ liệu (IV.2.3.7.12)
project: CIC
started: 2026-09-30
last_updated: 2026-09-30
current_step: B2
mode: TBD
output_script: scripts/gen_tc_kiemtraphanquyendulieucic.py
output_xlsx: practices/testcases/CIC/KiemTraPhanQuyenDuLieuCIC_TestCases.xlsx
qa_file: practices/Q&A/PhanQuyenDuLieuCIC_QA.md
tc_prefix: KTPQDL
tc_count: 0
---

## ✅ Bước 1 — Context (CONFIRMED 2026-09-30)

**Spec chính:** Confluence 34800037 — IV.2.3.7.12. Cấu trúc kiểm tra phân quyền dữ liệu (v13, 30/09/2026).

**Tài liệu liên quan (đã đọc toàn bộ):**
| Page ID | Tài liệu | Vai trò |
|---|---|---|
| 16911267 | IV.2.3.7 Người dùng trong CIC (cha) + Activity HT06 + State Machine | Vòng đời tài khoản, actor phân quyền |
| 34799907, 34799997 | IV.2.3.7.10 / .11 Phân quyền dữ liệu theo phòng ban | Cấu hình Bước 1 (Tệp ↔ Phòng phụ trách) |
| 16911348 | IV.2.3.7.6 Phân quyền dữ liệu tài khoản | Cấu hình Bước 2 (TCTD × Hành động), đăng xuất khi đổi quyền |
| 16911306, 16911309 | IV.2.3.7.2 / .3 Thêm mới / Cập nhật người dùng | Vai trò (HT-77) — Bước 3 |
| 16911299 | IV.2.3.7.1 Tra cứu người dùng | Quy tắc vai trò, nút Phân quyền chỉ ở Hoạt động |
| 16911312, 16911337, 16911185, 16911420, 34815209 | Xem chi tiết, Phê duyệt, Hiệu lực/Hết hiệu lực, Điều chuyển, DS điều chuyển | Lịch sử, vòng đời, xóa quyền khi điều chuyển |
| 16909447, 26968323, 26968066, 16911912 | 4 màn Tệp áp dụng | Nơi quan sát kết quả kiểm tra quyền |

**Scope đã xác nhận:**
- M1 Tiếp nhận dữ liệu có cấu trúc xác định; M2 Tiếp nhận dữ liệu có cấu trúc chưa xác định; M3 Tiếp nhận tệp phi cấu trúc; M4 Danh sách kiểm tra nội dung tệp báo cáo — chỉ các điểm áp dụng quyền (truy cập 403, bộ lọc Mã đầu mối, grid kết quả, nút thao tác theo quyền, xem chi tiết, xuất Excel).
- M5 Luồng liên chức năng: 3 bước × 3 vai trò, loại quyền Theo đầu mối/Theo chi nhánh/Theo tất cả, thay đổi cấu hình → hiệu lực/đăng xuất, điều chuyển, Không hoạt động.
- Out of scope: màn Tệp số 5 và 5 màn Kho (chưa có spec — hoãn theo Q02); validate UI của các màn cấu hình (feature riêng); trường không liên quan quyền trên M1–M4.
- Common TC chủ yếu N/A; trọng tâm Nhóm S + BIZ.

**Quyết định B1:** tái sử dụng `practices/Q&A/PhanQuyenDuLieuCIC_QA.md` cho B2; mã TC `KTPQDL_###`.

## ⏳ Bước 2 — Q&A [PENDING]

- File: `practices/Q&A/PhanQuyenDuLieuCIC_QA.md` (tái sử dụng, schema Full Review; mục 5 = phạm vi KTPQDL)
- Self-check (a)–(f): PASS (19 nhóm CR-A…CR-S; 24 Q-ID đủ 10 cột, có Mã checklist, có trong Coverage; cột Câu trả lời trống)
- Bổ sung ở B2: Q23 (lối vào khác: Xuất Excel/In, truy cập trực tiếp, bộ lọc trống — ⚠️), Q24 (thời điểm hiệu lực của thay đổi cấu hình)
- Verdict riêng KTPQDL: **BLOCKED** — chặn: Q01, Q03, Q05, Q07, Q23 (đều ⚠️ Cần BA/PO quyết định)
- WARNING dùng được assumption nếu user chấp thuận: Q04, Q11, Q14, Q16, Q20, Q21, Q22, Q24 (Q15 có ⚠️ nhưng TC 403 đã có nguồn [P13]–[P15])
- Ngoài scope KTPQDL: Q02 (phần còn mở), Q06, Q08, Q09, Q10, Q12, Q13, Q17, Q18, Q19
- Assumptions: **user chấp thuận "Dùng assumptions" (2026-09-30)** — WARNING không ⚠️ dùng dòng `>> Chọn Option X`; Q01, Q03, Q05, Q07, Q23 (⚠️) hoãn, TC liên quan đánh dấu PENDING-Q&A.
- Trạng thái pipeline: **TẠM DỪNG trước B3** — user ưu tiên pipeline riêng "Tích hợp Phân quyền dữ liệu (16911348)" (`TichHopPhanQuyenDuLieuCIC`).
## ⏳ Bước 3 — Modules & Field Inventory
## ⏳ Bước 4 — Traceability [PENDING]
## ⏳ Bước 5 — TC Summary
## ⏳ Bước 5b — TC Lead Review Gate [PENDING]
## ⏳ Bước 6 — Template Mapping
## ⏳ Bước 7 — Output
