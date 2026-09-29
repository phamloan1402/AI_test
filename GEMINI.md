# GEMINI.md

> **Scope:** Applies to every manual test-case generation task run by Gemini (Antigravity) in this project. It mirrors `CLAUDE.md` and `AGENTS.md` — keep all three in sync when updating rules.

## Project Overview

**AI_test** is a lean AI-driven kit for **manual test case generation using the AI-RBT (Risk-Based Testing) process**. It contains only the rules, skills, workflows and scripts needed to go from an SRS/spec (Confluence or user-provided) to a reviewed Q&A, a traceable test-case set, and a formatted Excel deliverable. Targets Vietnamese QA teams.

## Language Convention

- **Communication & explanations:** Vietnamese
- **Test case content (Excel / Markdown):** Tiếng Việt có dấu đầy đủ (Unicode)
- **Code (variables, functions, classes, comments):** English

---

## Security & Credentials (HIGHEST PRIORITY — READ FIRST)

> This rule takes effect at the start of every task. Follow before any auth-related action.

**NEVER read `.env` files directly** — do not use any tool (`view_file`, `read_url_content`, `run_command`, `grep`, etc.) to extract credentials (username, password, token, API key) from `.env` files.

> Reason: `.env` files contain sensitive credentials. Direct reads risk leaking secrets into logs, chat history, or AI artifacts.

---

## 📌 SRS Fidelity & Non-Inference Rule (BÁM SÁT SRS — CẤM TỰ SUY DIỄN)

> ⚠️ **MANDATORY RULE FOR REQUIREMENTS ANALYSIS & TEST CASE GENERATION**

* **Bám sát 100% tài liệu SRS/Specs trên Confluence:** AI chỉ được phép sinh test case, xác định danh sách trường (Field Inventory), control UI, quy tắc nghiệp vụ (BR), mã thông báo và luồng xử lý dựa trên ĐÚNG những gì được mô tả trong tài liệu Confluence (hoặc spec do user cung cấp).
* **CẤM TỰ Ý SUY DIỄN (ZERO INVENTED FIELDS / NO OVER-ASSUMPTION):**
  - Tuyệt đối **KHÔNG** tự ý thêm các trường nhập liệu, control UI, nút bấm, upload file hay checkbox nếu SRS không mô tả (ví dụ: tự thêm Upload file tài liệu, tự thêm Checkbox cam kết điều khoản khi spec không có).
  - Tuyệt đối **KHÔNG** mang thói quen/logic từ các sản phẩm khác áp đặt vào sản phẩm đang phân tích.
* **Quy trình khi phát hiện điểm mơ hồ hoặc nghi ngờ thiếu sót:**
  - Nếu phát hiện spec thiếu thông tin hoặc nghi ngờ thiếu trường: **BẮT BUỘC** đưa vào danh sách Q&A tại Bước 2 để hỏi BA/PO/User.
  - **TUYỆT ĐỐI KHÔNG** tự đưa các trường suy diễn vào Field Inventory hay bộ Test Cases khi chưa có câu trả lời xác nhận từ User/BA.
* **Đọc tài liệu:** BẮT BUỘC đọc **toàn bộ** nội dung mỗi tài liệu (Confluence page, PDF, spec) trước khi định nghĩa scope — KHÔNG kết luận dựa trên tiêu đề, TOC hoặc đọc không đầy đủ.

---

## Architecture

```
AI_test/
├── .agent/
│   ├── rules/                 # Mandatory behavior rules
│   ├── skills/                # 2 core skills + 4 workflow skills (wf_*)
│   └── workflows/             # Slash-command wrappers (wf_* skills + /pass)
├── Template/                  # FE component rules + Excel column-layout template
├── scripts/                   # Excel generation tooling (Python)
└── practices/                 # Deliverables (Q&A, test cases, work log & memory)
```

### `.agent/rules/`

| File | Purpose |
|------|---------|
| `manual_tc_excel_export.md` | Rules for exporting manual TCs to Excel (column layout, grouping, format) |
| `references/manual_tc_excel_export_details.md` | Detailed export rules |
| `references/tc_excel_export_examples.md` | Export examples |
| `worklog_memory_rules.md` | **Single source of truth** for Work Log & Memory: triggers, file paths, REOPEN handling, redaction, size limits |

### `.agent/skills/`

| Skill | Role |
|-------|------|
| `rbt_manual_testing` | **Master skill** — manual TC generation, modes QUICK (single pass) and FULL RBT (7 steps). FULL RBT B2 delegates to `srs_qa_architect` |
| `srs_qa_architect` | SRS review through BA, UX/UI, state-flow and QA-testability lenses; **single source of truth** for the Test Readiness Quality Gate and B2 Q&A |
| `rbt_manual_testing/references/common_tc_checklist.md` | **Mandatory** checklist groups (A–W) used when building the Field Inventory (B3b) and generating TCs; includes the per-case-ID **Verification Checklist** |
| `rbt_manual_testing/references/test_design_techniques.md` | EP, BVA, decision table, state transition, … |
| `srs_qa_architect/references/` | `checklist-review.md` (CR-A…CR-S), `Ambiguity.md`, `deep-logic-review.md` |
| `wf_generate_manual_testcases_rbt` | Workflow: full 7-step AI-RBT pipeline |
| `wf_generate_testcases_from_requirements` | Workflow: QUICK mode (draft → TC Lead Review Gate → final) for small, clear requirements |
| `wf_analyze_srs_qa` | Workflow: SRS analysis + Q&A only (B2 standalone) |
| `wf_review_testcases_with_srs` | Workflow: review an existing TC set against the SRS → gap report |

### `Template/`

- `Quy+tắc+component.md` — Common FE rules per component (**"QT component"**) of the **CUCI/CIC** project; **combine** with `common_tc_checklist.md` when generating TCs. Priority on conflict: **SRS > component rules > checklist**. For a different project, replace this file with that project's FE rules (or drop the QT-only cases).
- `CIC_Chức_năng_A.xlsx` — Reference Excel column layout that `scripts/tc_excel_writer.py` reproduces.

---

## Slash Commands (Workflows)

| Command | Skill | Purpose |
|---------|-------|---------|
| `/generate_manual_testcases_rbt` | `wf_generate_manual_testcases_rbt` | Full 7-step AI-RBT manual TC generation |
| `/generate_testcases_from_requirements` | `wf_generate_testcases_from_requirements` | QUICK mode — fast TC generation from clear requirements (auto-switches to FULL RBT if too complex/ambiguous) |
| `/analyze_srs_qa` | `wf_analyze_srs_qa` | Analyse an SRS and produce the Quality Gate + Q&A for BA/PO review |
| `/review_testcases_with_srs` | `wf_review_testcases_with_srs` | Review a manual TC set against the SRS for coverage gaps |
| `/pass <scope>` | `worklog_memory_rules.md` | Record user approval (PASS/PARTIAL) of a named scope into Work Log & Memory |

On agents without native slash commands: open `.agent/workflows/<command>.md`, then the `SKILL.md` it points to, then every *Dependent skill* it declares.

### FULL RBT — 7 steps & checkpoints

| Step | Output | Stop for user confirmation |
|------|--------|:---:|
| B1 Context & Role-play (read ALL documents first) | `practices/testcases/<PROJECT>/<Feature>_rbt_state.md` | ✅ |
| B2 Analysis & Q&A (via `srs_qa_architect`) | `practices/Q&A/<Feature>_QA.md` | ✅ |
| B3 Decomposition + Field Inventory (B3b, via `common_tc_checklist.md`) | inventory in state/working files | |
| B4 4-Layer Traceability & High-Level Scenarios | traceability matrix | ✅ |
| B5 RBT & TC Generation (FULL: ≤2 modules & ≤80 TC → Markdown; else COMPACT → script directly) | TCs | |
| B5b TC Lead Review Gate (6 criteria) | `practices/testcases/<PROJECT>/tc_review_<module>.md` | ✅ |
| B6 Template Mapping (skipped in COMPACT) | Markdown table (UI → CMN → BIZ) | |
| B7 Excel Export — **MUST use `scripts/tc_excel_writer.py`** | `scripts/gen_tc_<name>.py` → `.xlsx` | |

- Steps are **sequential** — never merge steps, never advance past a checkpoint without an explicit user reply.
- Always update the state file after each step so the pipeline can resume.

---

## Scripts

### Python Excel writer (mandatory for B7)

```bash
# Requires: pip install openpyxl
python scripts/gen_tc_<feature>.py
```

- `scripts/tc_excel_writer.py` — core writer (`section`, `subsection`, `tc`, `tc_group`, `tc_sub`, `tc_item`).
- `scripts/gen_tc_quanlychucnang.py` — **reference example** (COMPACT style) for new `gen_tc_<feature>.py` scripts. Compute output paths from the repo root (see its `OUT_PATH`) — never hardcode an absolute drive path.

---

## Key Standards

### Test Case IDs

Tiền tố và định dạng mã Test Case BẮT BUỘC tuân thủ: `[tên_chức_năng]_[SỐ]` (ví dụ: `[tên_chức_năng]_001`, `Login_001`, `M1_001`, `QLCN_001`).

### Q&A Deliverable

When analysing requirements in FULL RBT step 2, the agent **MUST reuse `srs_qa_architect`** and its `checklist-review.md` + `Ambiguity.md` references. Save the combined Quality Gate and Q&A to `practices/Q&A/<FeatureName>_QA.md`, preserving the standard evidence, issue, question, assumption/options, and BA answer columns. This file is the official review gate before the pipeline may proceed. QUICK mode has **no** Q&A step: if requirements turn out ambiguous or incomplete, it must switch to FULL RBT (B2 produces the Q&A file).

- **One schema for every Q&A file** — defined only in `srs_qa_architect/SKILL.md` (§4–§5), used by both `/analyze_srs_qa` and FULL RBT B2, so a file from `/analyze_srs_qa` is reusable at B2. Full Review: Coverage lists all 19 groups `CR-A`…`CR-S` → Q-ID or N/A reason, every Q-ID has a `Mã checklist` column (e.g. `CR-B2`), and Self-check (a)–(d) runs before stopping. Inline mode: `Mã checklist` only, no 19-group coverage.
- Review codes use the `CR-` prefix from `checklist-review.md` — **never** the Common TC groups of `common_tc_checklist.md` (those start at B3b).
- Column `Vấn đề & Rủi ro`: problem type, problem (object + what SRS says / does not say), concrete scenario, test risk.
- Column `Assumption / Options`: list Option A/B/(C), then always pick one as **>> Chọn Option X vì: <lý do>**; security / compliance / finance / core-business conflicts additionally carry `⚠️ Cần BA/PO quyết định` and must not be used as an assumption until BA/PO answers. Column `Câu trả lời` stays empty for BA/PO.
- These column rules and the Self-check (a)–(f) live in `srs_qa_architect/SKILL.md` — workflows only point to them.

### Output Paths

| Deliverable | Path |
|---|---|
| Q&A | `practices/Q&A/<Feature>_QA.md` |
| State file, working files, Excel | `practices/testcases/<PROJECT>/` |
| TC Lead Review report (B5b / QUICK) | `practices/testcases/<PROJECT>/tc_review_<module>.md` |
| SRS gap review (`/review_testcases_with_srs`) | `practices/testcases/<PROJECT>/tc_review_<Feature>_srs_gap.md` |
| Generator script | `scripts/gen_tc_<feature>.py` |
| Work Log & Memory | `practices/worklog/` (git-ignored — internal log) |

### 📝 Logging Strategy — 3 Tiers

`worklog_memory_rules.md` refers to these tier names — keep them.

1. **Tier 1 — Temporary files (MUST CLEANUP):** debug dumps, scratch scripts. Store only in `.agent/tmp/` (git-ignored) or the agent's scratchpad — never a hardcoded `/tmp` path (Windows). Delete before task completion.
2. **Tier 2 — Working artifacts & trial runs:** state file, intermediate outputs, trial runs of `gen_tc_*.py`. Written only to the output paths above — never to the project root. Trial/fix iterations are **not** Work Log events.
3. **Tier 3 — Execution & Audit Summary** (end of each task): TC counts per group/module, artifacts created/updated, open Q&A items, cleanup report, **Work Log & Memory report (§10 of the rules)**, and token efficiency (`rtk gain`).

---

## Definition of Done (Manual TC)

- [ ] Every field/control/BR/message in the TC set is traceable to the SRS or to an **answered** Q&A item — zero invented fields
- [ ] Field Inventory checked against `common_tc_checklist.md` (all applicable groups A–W, selected via the dispatch table)
- [ ] **Verification Checklist** in `common_tc_checklist.md` ticked per case-ID after generation
- [ ] Coverage Symmetry respected (see below)
- [ ] B5b TC Lead Review done — `tc_review_<module>.md` produced and user confirmed
- [ ] Excel exported per `manual_tc_excel_export.md`; content in Vietnamese with full diacritics
- [ ] State file updated; temp files removed
- [ ] Summary reported: TC counts, skipped items (with reason), open questions / known limitations

---

## Anti-Patterns (FORBIDDEN)

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| Invent / assume fields not in the SRS (e.g. adding file upload, terms checkbox) | **100% SRS Fidelity**: only include fields explicitly defined in the SRS component table; ask via Q&A if in doubt |
| Advance past B1/B2/B4/B5b without explicit user confirmation | Stop at every checkpoint and wait |
| Use `common_tc_checklist.md` for B2 Q&A | B2 uses `srs_qa_architect/references/checklist-review.md` |
| Forget buttons on Confirmation Dialog (CONF_*) when action opens popup | Every confirmation popup (CONF_*) MUST have independent subsections for each button: Confirm/OK (3 TCs), Cancel (3 TCs), and close icon X (2 TCs) |
| Keep code prefix M01 —, M02 — in Test Case column (Col C) for Button | MUST start with "Kiểm tra ", NEVER leave prefix code M01 — (e.g. "Kiểm tra hiển thị nút Gửi yêu cầu") |
| Dropdown H06 written poorly without keyboard steps | MUST have all 5 keyboard steps: Tab/Shift-Tab focus → Enter open dropdown → Up/Down select → Enter choose option → Tab/Shift-Tab next field |
| File upload not categorized or missing cases | MUST divide into 3 groups: Drag & drop zone, Click 'Choose file' button, File list display and actions after upload |
| Skip QA Lead Review Testcase (Step 5b) | MUST evaluate 6 quality criteria, generate `tc_review_<module>.md` report, and halt at checkpoint before handover |
| Write TC content in English or Vietnamese without diacritics | Vietnamese with full diacritics |

---

## Coverage Symmetry Rule

**Every field of the same type MUST have complete test cases.** Never write full tests only for the first field and skip remaining fields of the same type.

**Checklist per TEXT field (38 cases mandatory):**

| Group | Keyboard (D) | Copy/Paste (Dcp) | Description |
|-------|-------------|-----------------|-------------|
| **Default & UI** | D01-D04 (4) | — | Default value, UI display, placeholder, required |
| **BVA** | D05-D07 (3) | D05cp-D07cp (3) | Max−1, Max, Max+1 → truncate on paste |
| **Whitespace** | D08-D11 (4) | D08cp-D11cp (4) | All spaces, leading/trailing, middle, multiple middle |
| **Characters** | D12-D17 (6) | D12cp-D17cp (6) | UPPER, lower, digits, special, mixed, Vietnamese |
| **Security** | D18-D21 (4) | D18cp-D21cp (4) | XSS/HTML, SQL injection, URL, CSRF |
| **Total** | **21 cases** | **17 cases** | **= 38 cases per field** (Textbox has NO search cases) |
| **Dropdown Search** | D22-D28 (+7) | — | Search box inside a Dropdown/Combobox/Multi-select popup only — **never** for a Textbox (search business logic belongs to the BIZ section) |
| **NUMBER (Group E)** | E01-E04 (4) + E05-E23 (19) | E05cp-E23cp (19) | **= 42 cases per field**; E20 decimal, E21 negative, E22 decimal places, E23 leading zeros are *per spec* |

> **Verification Checklist:** See `common_tc_checklist.md` → **Verification Checklist** section for a per-case-ID enumeration to tick off after TC generation.

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| Input only has D01-D08 (basic+boundary) | Full 38 cases per TEXT field (D01–D21 + D05cp–D21cp) / 42 per NUMBER field (E01–E23 + E05cp–E23cp) including chars + security |
| TEXT tc_group input has only a few items (missing D05-D07 BVA or D11-D14, D16, D20-D21) | tc_group "Kiểm tra khi nhập giá trị" MUST have **17 tc_item** (D05–D21, starting with sub "Kiểm tra nhập maxlength" 3 items) |
| TEXT tc_group copy-paste has only a few items | tc_group "Kiểm tra khi copy/paste giá trị" MUST have **17 tc_item** (D05cp–D21cp, starting with sub "Kiểm tra copy/paste maxlength" 3 items) |
| Missing entire Copy/Paste group | Separate tc_group for copy/paste (D05cp–D21cp) per field |
| NUMBER tc_group has only a few items | tc_group "Kiểm tra khi nhập giá trị" MUST have **19 tc_item** (E05–E23) and copy/paste **19 tc_item** (E05cp–E23cp); E20–E23 expected results follow the spec |
| Nhóm A has only 3-5 TCs | MUST have **6 TCs** (A01–A06) for EVERY module/screen (A07–A08 are QT-component extras). A03/A04/A05 are most commonly missing |
| Grid (C) has only C01 + pagination | MUST also have C02 (STT), C03 (hide paging ≤10), C05, C07, C09, C10 + 3 tc_group pagination + QT C11–C16 |
| Multi-select (J) missing J02-J06, J14 | EVERY multi-select MUST have all 14 cases (J01–J14) + API states |
| DatePicker/RangePicker missing K01, K02, K08 | K01 (focus empty), K02 (focus with value), K08 (29/02 leap year) are mandatory; K15–K17 (incl. K17 <01/01/1900) are QT-component cases |
| Edit form has no Group V | Every edit screen MUST have V01–V05 + field-type cases for editable fields (dispatch table → V) |
| TEXTAREA uses Group D but missing Group G | If field is TextArea, must also have G07 (multiline Enter), G11 (counter QT), G12 (auto resize QT) |

---

## Work Log & Memory (on PASS / PARTIAL / REOPEN / CORRECTION)

> Full rules — **single source of truth**: [.agent/rules/worklog_memory_rules.md](.agent/rules/worklog_memory_rules.md)
> The summary below is a **non-normative quick reference**; if it disagrees with the rules file, the rules file wins.
> **On any trigger, MUST read `worklog_memory_rules.md` before writing Work Log or Memory** — never write from this summary alone.

- **Four event types:** `PASS`, `PARTIAL` (part of the scope approved), `REOPEN` (approved content is affected by a
  new requirement), `CORRECTION` (fixing one specific earlier entry).
- **Trigger for PASS/PARTIAL:** an explicit user confirmation **naming the scope**, or `/pass <scope>`.
  A bare `ok` / `done` / `xong` / `ghi lai` is **not** a trigger — ask which scope is being confirmed.
- **FAIL or a blocking open issue blocks PASS/PARTIAL only.** `REOPEN` and `CORRECTION` must still be written so the
  audit trail stays intact.
- **Work Log** (append-only, Event ID + `+07:00` timestamp converted explicitly to Asia/Ho_Chi_Minh)
  -> `practices/worklog/<slug>_WORKLOG.md`. Never edit an existing entry — add a `CORRECTION` entry instead.
- **Memory** -> `practices/worklog/PROJECT_MEMORY.md` (scope status + preferences)
  and `practices/worklog/memory/<slug>_MEMORY.md` (per-feature detail).
  Never write this template into the **host agent's own auto-memory store** (Claude Code:
  `~/.claude/projects/<project>/memory/MEMORY.md`; Gemini/Antigravity and Codex CLI have their own) — different schema.
- **Requirement not yet approved by BA/user:** do NOT put its content in Memory's *normalized-content* sections. Record the audit trail
  (`REOPEN` entry with `Approval: PENDING` + change state `PENDING_REVIEW`); the text belongs in
  `practices/Q&A/<slug>_QA.md`.
- **Two independent axes in Memory's *Scope Status* section:** *pipeline state* (source of truth `<Feature>_rbt_state.md`) and
  *change state* (`NONE` / `PENDING_REVIEW` / `REOPEN_REQUIRED`, owned by Memory). Reconciling the pipeline state must
  never clear the change state.
- **Redaction (masking sensitive data) applies to BOTH files.** Report inside the Tier 3 Execution & Audit Summary, not as a separate block.
