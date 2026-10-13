---
feature: Tích hợp Phân quyền dữ liệu tài khoản (16911348) với các chức năng IV.2.3.7 và màn áp dụng
project: CIC
started: 2026-09-30
last_updated: 2026-09-30
current_step: B4
mode: COMPACT
output_script: scripts/gen_tc_tichhopphanquyendulieucic.py
output_xlsx: practices/testcases/CIC/TichHopPhanQuyenDuLieuCIC_TestCases.xlsx
qa_file: practices/Q&A/PhanQuyenDuLieuCIC_QA.md
working_file: practices/testcases/CIC/TichHopPhanQuyenDuLieuCIC_B3_B4.md
tc_prefix: PQDLTH
tc_count: 0
---

## ✅ Bước 1 — Context (CONFIRMED 2026-09-30)

- Trọng tâm: TC tích hợp 2 chiều quanh 16911348 — luồng vào (Tra cứu/nút Phân quyền, vòng đời tài khoản, dữ liệu nguồn tài khoản/NV16/Nhóm quyền, điều chuyển chờ) và luồng ra (đăng xuất, Tra cứu chip/bộ lọc, Xem chi tiết, Phê duyệt, hiệu lực trên 4 màn Tệp, vòng đời điều chuyển/hết hiệu lực/thu hồi quyền chức năng).
- Modules: M1 Luồng vào · M2 Luồng ra — phiên & hiển thị · M3 Luồng ra — hiệu lực trên màn áp dụng · M4 Vòng đời liên chức năng.
- Ngoài phạm vi: validate UI MH-1…MH-4 (bộ TC chức năng 16911348); ma trận 3 bước × 3 vai trò của 34800037 (pipeline KTPQDL); màn Tệp số 5 + 5 màn Kho (Q02).
- Tài liệu: [P0]–[P16] như file Q&A (đã đọc toàn bộ trong session 2026-09-30).

## ✅ Bước 2 — Q&A Resolved (assumptions chấp thuận 2026-09-30)

- File: `practices/Q&A/PhanQuyenDuLieuCIC_QA.md` (self-check PASS).
- Dùng assumption (dòng `>> Chọn Option X`): Q06 (A), Q11 (A), Q12 (A), Q13 (A), Q14 (A), Q16 (A), Q17 (A), Q20 (A), Q22 (A), Q24 (A).
- **Hoãn — PENDING-Q&A (⚠️ cần BA/PO):** Q01 → SC-M3-10; Q05 → SC-M3-09; Q07 → SC-M2-06; Q15 → SC-M1-05 + RBAC ô PENDING; Q23 → SC-M3-11.
- Không ảnh hưởng scope: Q02 (phần còn mở), Q03 (thuộc KTPQDL), Q04, Q08, Q09, Q10, Q18, Q19, Q21.

## ✅ Bước 3 — Modules & Field Inventory

- Chi tiết: `TichHopPhanQuyenDuLieuCIC_B3_B4.md` §B3a, §B3b.
- Common TC: A N/A (không có màn riêng — lý do ghi trong file), M ✅ (nút Phân quyền ở Tra cứu), S ✅ (M1, M3); C/H/J chỉ kiểm tra nội dung option/grid dưới dạng BIZ; các nhóm còn lại N/A.
- Kỹ thuật: State Transition, Decision Table, EP, BVA.

## ✅ Bước 4 — Traceability [APPROVED 2026-09-30 — trừ 5 kịch bản PENDING-Q&A]

- Chi tiết: `TichHopPhanQuyenDuLieuCIC_B3_B4.md` §B4 (4 tầng + 48 kịch bản, 5 PENDING-Q&A).
- BR: 14 BR-IN + 23 BR-OUT + 10 BR-LC = 47 dòng; 7 mã/nội dung thông báo được map.
- Work Log: Event `Tich_hop_Phan_quyen_du_lieu_tai_khoan_16911348-20260930-01` (PARTIAL/APPROVED).

## ✅ Bước 5 — TC Summary (COMPACT, draft trong script — chưa xuất xlsx)

- Script: `scripts/gen_tc_tichhopphanquyendulieucic.py`
- M1-LuongVao 36 · M2-PhienHienThi 31 · M3-HieuLucManTep 26 · M4-VongDoi 20 → **113 TC** (9 PENDING-Q&A: 015, 016, 017, 047, 089–093)

## ⏳ Bước 5b — TC Lead Review Gate [PENDING]

- Báo cáo: `practices/testcases/CIC/tc_review_TichHopPhanQuyenDuLieuCIC.md` — 12 GAP (Coverage 2, Clarity 1, Accuracy 4, Feasibility 2, Organization 1, Traceability 2)
- Chờ user đánh dấu hành động từng GAP.
## ⏳ Bước 6 — Template Mapping [SKIP-COMPACT]
## ⏳ Bước 7 — Output
