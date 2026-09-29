# AI_test — AI-RBT Manual Test Case Kit

Bộ kit tối giản để AI agent (Claude Code, Codex, Gemini/Antigravity) sinh **manual test case** theo quy trình **AI-RBT 7 bước** (Risk-Based Testing): từ SRS/Confluence → Q&A → Field Inventory → Traceability → Test Cases → Excel.

## Cài đặt

```bash
pip install openpyxl        # bắt buộc — sinh Excel (B7)
```

## Sử dụng

| Lệnh | Mục đích |
|------|---------|
| `/generate_manual_testcases_rbt` | Chạy đủ 7 bước AI-RBT (dừng xác nhận tại B1, B2, B4, B5b) |
| `/generate_testcases_from_requirements` | Mode QUICK — sinh TC nhanh cho module nhỏ, requirement rõ (tự chuyển FULL RBT nếu phức tạp) |
| `/analyze_srs_qa` | Chỉ phân tích SRS → Quality Gate + Q&A cho BA/PO |
| `/review_testcases_with_srs` | Review bộ TC có sẵn so với SRS → báo cáo GAP |
| `/pass <scope>` | Ghi nhận duyệt một scope vào Work Log & Memory (VD: `/pass B2 Q&A`) |

Agent không hỗ trợ slash command: mở `.agent/workflows/<lệnh>.md` và làm theo.

## Cấu trúc

```
.agent/rules/        Rule xuất Excel, Work Log & Memory
.agent/skills/       rbt_manual_testing, srs_qa_architect + 4 workflow skill (wf_*)
.agent/workflows/    Slash command wrappers
Template/            Quy tắc component FE + mẫu layout Excel
scripts/             tc_excel_writer.py, ví dụ gen_tc_quanlychucnang.py
practices/           Output: Q&A/, testcases/<PROJECT>/, worklog/
```

## Output

| Deliverable | Đường dẫn |
|---|---|
| Q&A (Review Gate B2) | `practices/Q&A/<Feature>_QA.md` |
| State file, báo cáo review (`tc_review_*`), Excel | `practices/testcases/<PROJECT>/` |
| Script sinh Excel | `scripts/gen_tc_<feature>.py` |
| Work Log & Memory | `practices/worklog/` (không commit — xem `.agent/rules/worklog_memory_rules.md`) |

Quy tắc chi tiết cho agent: xem `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`.
