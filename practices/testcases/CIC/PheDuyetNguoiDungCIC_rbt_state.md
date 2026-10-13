---
feature: Phê duyệt dữ liệu Người dùng trong CIC
project: CIC
started: 2026-09-29
last_updated: 2026-09-29
current_step: B2
mode: TBD
output_script: scripts/gen_tc_pheduyetnguoidungcic.py
output_xlsx: practices/testcases/CIC/PheDuyetNguoiDungCIC_TestCases.xlsx
qa_file: practices/Q&A/PheDuyetNguoiDungCIC_QA.md
tc_prefix: PDND
tc_count: 0
---

## ✅ Bước 1 — Context (CONFIRMED 2026-09-29)

**Spec chính:** Confluence page 16911337 — IV.2.3.7.5. Phê duyệt dữ liệu Người dùng trong CIC (v8, cập nhật 23/09/2026).

**Tài liệu liên quan (đã đọc toàn bộ):**
| Page ID | Tài liệu | Vai trò |
|---|---|---|
| 34800037 | IV.2.3.7.12. Cấu trúc kiểm tra phân quyền dữ liệu (v9) | Check quyền 3 bước Phòng ban → TCTD → Vai trò |
| 16911348 | Phân quyền người dùng (phân quyền dữ liệu) | Nguồn dữ liệu TCTD / Phân loại quản lý / chức năng; ERR-005 |
| 16911185 | Hiệu lực / Hết hiệu lực người dùng | Luồng Yêu cầu phê duyệt; dùng chung mockup + popup Phê duyệt/Từ chối |
| 16911420 | Điều chuyển phòng ban của tài khoản | Đổi phòng ban → thu hồi nhóm quyền |
| 34799907 | Phân quyền dữ liệu theo phòng ban | Mapping Tệp ↔ Phòng phụ trách |

**Ảnh đã xem:** mockup 2026-9-15 (bản mới nhất), mockup 2026-8-24, 2026-4-7 (2 bản), 2026-1-27, 2025-11-12; popup "Xác nhận phê duyệt", "Từ chối phê duyệt"; flowchart check quyền 3 bước.

**Scope đã xác nhận:**
- MH-1 Màn hình Phê duyệt dữ liệu người dùng: Khu vực Thông tin người dùng (readonly + link Xem chi tiết quyền theo chức năng); Khu vực Phân quyền dữ liệu (label readonly, grid Danh sách TCTD phụ trách có phân trang, cây Danh sách chức năng phân quyền); nút Hủy / Từ chối / Phê duyệt.
- MH-2 Popup Xác nhận phê duyệt: Lý do (Textarea, không bắt buộc, 1000), Xác nhận (BUS-78, → Hoạt động, gửi email), Hủy, icon X.
- MH-3 Popup Từ chối phê duyệt: Lý do (Textarea, bắt buộc, 1000), Xác nhận (BUS-78, → Tạo mới), Hủy, icon X.
- BIZ: chuyển trạng thái, concurrency BUS-78, email, phân quyền chức năng + dữ liệu, nhất quán dữ liệu với 16911348/34799907, ảnh hưởng chéo 16911420/16911185.
- Out of scope: nội dung các chức năng Tra cứu người dùng, Tra cứu nhóm quyền, Phân quyền, Hiệu lực/Hết hiệu lực, Điều chuyển, Phân quyền theo phòng ban (chỉ kiểm tra điều hướng/tích hợp).

**Mã TC:** `PDND_###`.

## ⏳ Bước 2 — Q&A [PENDING]

- File: `practices/Q&A/PheDuyetNguoiDungCIC_QA.md`
- Verdict: **BLOCKED**
- BLOCKING chưa giải quyết: Q01, Q02, Q03, Q04, Q09
- WARNING: Q05, Q06, Q07, Q08, Q10, Q11, Q12, Q13, Q14, Q15, Q16
- SUGGESTION: Q17, Q18
- Assumptions: chưa được chấp thuận.

## ⏳ Bước 3 — Modules & Field Inventory
## ⏳ Bước 4 — Traceability [PENDING]
## ⏳ Bước 5 — TC Summary
## ⏳ Bước 5b — TC Lead Review Gate [PENDING]
## ⏳ Bước 6 — Template Mapping
## ⏳ Bước 7 — Output
