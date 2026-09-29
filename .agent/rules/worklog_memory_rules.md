# Work Log & Memory Rules — Quy tắc ghi Approval/Change Audit Log và cập nhật trạng thái

> **Phạm vi:** Áp dụng cho mọi agent làm việc trong repo này (Claude Code, Gemini/Antigravity, Codex CLI).
> **Nguồn chuẩn duy nhất.** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` chỉ chứa một **quick reference không mang tính chuẩn**.
> Khi quick reference lệch với file này → **file này luôn thắng**.
> ⚠️ **BẮT BUỘC đọc file này tại thời điểm trigger**, trước khi ghi Work Log hoặc Memory. Không được ghi chỉ dựa vào quick reference.

---

## 0. Nguyên tắc cốt lõi

| | Work Log | Memory |
|---|---|---|
| **Bản chất** | **Approval & Change Audit Log** — nhật ký các mốc được duyệt và các thay đổi tác động tới nội dung đã duyệt | Tri thức nền & trạng thái hiện tại — cần nhớ gì để làm tiếp |
| **Cách ghi** | Append-only tuyệt đối: chỉ thêm bản ghi mới, không sửa/xóa bản ghi cũ | Có thể cập nhật, gộp, thay thế |
| **Trục thời gian** | Theo sự kiện, có timestamp | Luôn phản ánh trạng thái **mới nhất** |

> **Đây KHÔNG phải session log đầy đủ.** Các lần chạy FAIL, thử nghiệm, sửa lặt vặt **không** được ghi vào đây —
> chúng thuộc về Tier 2 (log của test runner) theo Logging Strategy. Work Log chỉ ghi 4 loại sự kiện ở §2.1.

**Chiều dữ liệu (chống trùng lặp):**

- KHÔNG sao chép **nguyên văn** giữa hai file.
- Rule / Business rule / Quyết định của user: ghi **bản chuẩn hóa** vào Memory. Work Log **chỉ trỏ tới**, không chép lại.
  - ✅ `- Rule/Decision đã xác nhận: → memory/<slug>_MEMORY.md §2 "Cột STT bảng Grid"`
  - ❌ Chép lại toàn văn nội dung rule vào Work Log.
- Ngược lại, Memory được phép tham chiếu ngược tới bản ghi Work Log bằng **Event ID** (§3.3).

---

## 1. Vị trí file (BẮT BUỘC — không được tự đoán)

```
practices/worklog/PROJECT_MEMORY.md                           # Index + trạng thái scope + preference (cross-feature)
practices/worklog/memory/<slug>_MEMORY.md                     # Memory chi tiết theo feature (mục 1-5)
practices/worklog/<slug>_WORKLOG.md                           # Work Log active, mỗi feature một file
practices/worklog/archive/<slug>_WORKLOG-<YYYYMMDD-HHmmss>.md # Work Log đã rotate (§8.1)
```

### 1.1 Chuẩn hóa `<slug>`

Tên feature do user đặt có thể chứa khoảng trắng, dấu tiếng Việt, `/`, `:` — không dùng trực tiếp làm tên file.

- `<slug>` chỉ được chứa `[A-Za-z0-9_-]`, tối đa 60 ký tự.
- Quy tắc chuyển: bỏ dấu tiếng Việt → thay mọi ký tự ngoài tập hợp trên bằng `_` → gộp `_` liên tiếp → cắt `_` ở hai đầu.
  - `Đề nghị điều chỉnh TCTD` → `De_nghi_dieu_chinh_TCTD`
  - `S70 / Báo cáo DNNN` → `S70_Bao_cao_DNNN`
- **Tên hiển thị gốc** lưu ở dòng đầu trong file: `> Feature: <tên gốc do user đặt>`.
- Slug đã tạo thì **giữ nguyên**, không đổi khi user gọi feature bằng tên khác.

### 1.2 Phân chia nội dung Memory

| Nội dung | Nơi lưu |
|---|---|
| Mục 6 (Trạng thái scope mọi feature), Mục 7 (Preference của user) | `PROJECT_MEMORY.md` |
| Mục 1–5 của một feature cụ thể | `memory/<slug>_MEMORY.md` |
| Mục 1–5 áp dụng cho **mọi** feature | `PROJECT_MEMORY.md`, dưới heading `## Cross-feature` |

### 1.3 Quy tắc khởi tạo

- File **chỉ được tạo ở lần ghi hợp lệ đầu tiên**. Không tạo file rỗng.
- Khi tạo mới, ghi heading chuẩn:
  - Work Log: `# Work Log — <tên gốc>` + `> Feature: <tên gốc>` + `> Append-only. Quy tắc: .agent/rules/worklog_memory_rules.md`
  - Memory feature: `# Memory — <tên gốc>` + `> Feature: <tên gốc>` + 5 heading `## 1. …` đến `## 5. …` theo §4.1.
  - `PROJECT_MEMORY.md`: `# Project Memory` + `## Index` + `## 6. Trạng thái scope` + `## 7. Preference` + `## Cross-feature`.

> ⛔ **CẤM** ghi theo template này vào **kho auto-memory riêng của agent host**. Mỗi host có kho riêng với schema khác:
> Claude Code dùng `~/.claude/projects/<project>/memory/MEMORY.md` (index 1 dòng/memory trỏ tới file con);
> Gemini/Antigravity và Codex CLI có cơ chế tương đương riêng.
> Có thể trùng tên file nhưng **không phải** cùng một thứ — ghi nhầm sẽ phá kho đó.

---

## 2. Điều kiện kích hoạt

### 2.1 Bảng trigger theo trạng thái

| Trạng thái | Kích hoạt khi | Cần user xác nhận? | Blocking issue có chặn không? |
|---|---|---|---|
| **PASS** | User xác nhận PASS **tường minh có nêu scope**, hoặc lệnh `/pass <scope>`; toàn bộ scope đạt | ✅ Có | ⛔ Có — không ghi |
| **PARTIAL** | User xác nhận PASS cho **một phần** scope, phần còn lại chưa kết luận | ✅ Có (cho phần được nêu) | ⛔ Có — không ghi |
| **REOPEN** | Requirement/spec mới làm thay đổi nội dung đã PASS (§5) | ❌ Không | ✅ Không chặn — **vẫn phải ghi** |
| **CORRECTION** | Đính chính một bản ghi cũ **cụ thể** đã ghi sai/thiếu | ❌ Không | ✅ Không chặn — **vẫn phải ghi** |

Ví dụ xác nhận hợp lệ: *"pass phần Field Inventory"*, *"chốt bộ TC S70"*, *"duyệt B3 rồi nhé"*.

> **Quan trọng:** blocking issue và kết quả FAIL chỉ ngăn ghi **PASS/PARTIAL**. Sự kiện REOPEN và CORRECTION
> **luôn phải được ghi** để bảo toàn audit trail — kể cả khi đang còn câu hỏi mở với BA.

### 2.2 KHÔNG ghi PASS/PARTIAL khi

- Kết quả FAIL, hoặc scope chưa được user xác nhận.
- Còn **blocking** open issue (§2.4).
- Các bước thử nghiệm / sửa lặt vặt trong quá trình làm việc → thuộc Tier 2, không thuộc Work Log.

### 2.3 Từ khóa không phải trigger

`ok`, `done`, `xong`, `được rồi`, `ghi lại` **đứng một mình** không phải trigger.

> Lý do: đây là từ đệm phổ biến trong hội thoại tiếng Việt (*"ok em làm tiếp đi"*, *"ghi lại giúp anh cái link"*).
> Bắt trigger theo từ khóa trần sẽ ghi log sai trạng thái.
> Gặp các từ này mà không rõ scope → **hỏi lại**: *"Bạn xác nhận PASS cho phạm vi nào?"* rồi mới ghi.

**Trả lời cho câu hỏi làm rõ đó LÀ trigger hợp lệ** — không hỏi vòng lặp:
- User nêu một phạm vi cụ thể (module / artifact / bước) → ghi ngay, không hỏi lại lần nữa.
- User vẫn trả lời mơ hồ (*"tất cả"*, *"như cũ"*) → yêu cầu nêu tên cụ thể, **tối đa 1 lần hỏi lại nữa**.
- Sau đó vẫn không rõ → **không ghi**, báo user lý do và dừng.

### 2.4 Open issue — blocking vs non-blocking

| Loại | Định nghĩa | Ảnh hưởng |
|---|---|---|
| **Blocking** | Câu hỏi chưa có đáp án làm scope không thể kết luận đúng/sai (BA chưa trả lời Q&A ảnh hưởng trực tiếp scope đó) | ⛔ Không ghi PASS/PARTIAL. REOPEN/CORRECTION vẫn ghi. |
| **Non-blocking / out-of-scope** | Vấn đề đã ghi nhận nhưng không ảnh hưởng kết luận của scope (thuộc module khác, cải tiến sau) | ✅ Được ghi PASS, liệt kê ở trường `Open issue còn lại`. |

---

## 3. Work Log

### 3.1 Append-only tuyệt đối

- **CHỈ THÊM bản ghi mới.** Không sửa, không xóa, không chèn dòng vào bản ghi đã tồn tại — kể cả để bổ sung.
- Cần đính chính/bổ sung một bản ghi cũ → tạo **bản ghi mới** `Trạng thái: CORRECTION`, Event ID mới, kèm trường `Đính chính cho: <Event ID gốc>`.
- Ngoại lệ được phép ghi đè: **không có**.

### 3.2 Chống ghi trùng & tranh chấp

**Trước khi ghi, BẮT BUỘC:**

1. **Re-read** file Work Log ngay trước khi append (không dùng nội dung đã đọc từ đầu session) — hạn chế hai agent/phiên ghi đè nhau.
2. Kiểm tra Event ID trên **cả file active và toàn bộ file trong `archive/`**, không chỉ bản ghi cuối.

| Tình huống | Hành động |
|---|---|
| **Trùng chính xác Event ID** (active hoặc archive) | ⛔ Không ghi, dừng. Đảm bảo idempotent khi agent retry. |
| Cần đính chính một event cũ **cụ thể** (ghi sai, ghi thiếu) | ✅ Bản ghi `CORRECTION` + `Đính chính cho: <Event ID gốc>`. |
| **Công việc mới** trên cùng scope (lần thực thi hợp lệ mới, có artifact mới) | ✅ Bản ghi `PASS` / `PARTIAL` **mới**, Event ID mới. **KHÔNG** dùng CORRECTION. |

> CORRECTION chỉ dùng để **sửa bản ghi**, không dùng để ghi **công việc mới**.

### 3.3 Timestamp — phải đúng `+07:00`

`Get-Date` và `date` mặc định lấy timezone của **máy đang chạy**. Agent chạy trên máy UTC sẽ sinh timestamp sai quy định.
BẮT BUỘC convert timezone tường minh:

- PowerShell:
  ```powershell
  $tz = [TimeZoneInfo]::FindSystemTimeZoneById('SE Asia Standard Time')
  [TimeZoneInfo]::ConvertTime([DateTimeOffset]::UtcNow, $tz).ToString('yyyy-MM-ddTHH:mmzzz')
  ```
- Bash: `TZ=Asia/Ho_Chi_Minh date +"%Y-%m-%dT%H:%M%z"`

**Kiểm tra bắt buộc:** offset đầu ra phải là `+07:00` (hoặc `+0700`). Nếu khác → **dừng, không ghi**, báo user.
⛔ TUYỆT ĐỐI không tự suy đoán / bịa ngày giờ.

### 3.4 Template bản ghi

```markdown
---
### [<ISO-8601 +07:00>] <Session/Task>
- **Event ID:** <slug>-<YYYYMMDD>-<NN>
- **Trạng thái:** PASS | PARTIAL | REOPEN | CORRECTION
- **Approval:** N/A | PENDING | APPROVED
- **Đính chính cho:** <Event ID gốc>   <!-- chỉ với CORRECTION, bỏ trường này ở trạng thái khác -->
- **Phạm vi/sự kiện:** <PASS/PARTIAL: scope được duyệt — PARTIAL phải nêu rõ phần CHƯA duyệt.
                        REOPEN: nội dung nào bị tác động. CORRECTION: sửa cái gì.>
- **Mục tiêu:** <1-2 câu>
- **Công việc đã hoàn thành:** <danh sách ngắn | N/A>
- **Rule/Decision đã xác nhận:** <trỏ tới mục Memory, KHÔNG chép nguyên văn | "Không">
- **Bằng chứng:** <test/điều kiện đã pass, ID testcase, số liệu — đã redact theo §7 | N/A>
- **File/Artifact đã tạo hoặc chỉnh sửa:** <đường dẫn | N/A>
- **Giả định (nếu có):** <ghi kèm nhãn "[GIẢ ĐỊNH - chưa xác nhận]">
- **Vấn đề gặp phải & cách xử lý:** <... | "Không">
- **Open issue còn lại:** <phân loại blocking / non-blocking theo §2.4 | "Không">
- **Việc tiếp theo:** <nếu có>
---
```

**Giá trị `Approval` theo trạng thái:**

| Trạng thái | Approval |
|---|---|
| PASS / PARTIAL | `APPROVED` |
| REOPEN khi requirement **chưa** được BA/user duyệt | `PENDING` |
| REOPEN khi requirement **đã** được duyệt | `APPROVED` |
| CORRECTION | `N/A` |

### 3.5 Fact vs Giả định

Work Log được ghi **cả hai**, nhưng phải phân biệt rõ:
- **Fact** đã xác minh trong session → ghi bình thường.
- **Giả định** chưa được user/BA xác nhận → BẮT BUỘC gắn nhãn `[GIẢ ĐỊNH - chưa xác nhận]`, đặt ở trường `Giả định`.
- **Memory chỉ chứa nội dung đã được xác nhận** — giả định không bao giờ được đưa sang Memory (§4.3).

---

## 4. Memory

### 4.1 Cấu trúc cố định (7 mục)

Các mục **nội dung chuẩn hóa** nằm ở `memory/<slug>_MEMORY.md`; **Trạng thái scope** và **Preference** nằm ở `PROJECT_MEMORY.md` (§1.2).

1. **Project/Module context** — bối cảnh dự án, module, luồng nghiệp vụ, giới hạn hệ thống.
2. **Business rule đã xác nhận.**
3. **Quyết định của user** và lý do.
4. **Mapping/Terminology** — thuật ngữ, ánh xạ tên/mã.
5. **Quy ước kỹ thuật & bẫy đã gặp** — chuẩn đặt tên, cấu trúc, môi trường; root cause lỗi khó và cách phòng tránh.
6. **Trạng thái scope** — hai trục độc lập, xem §4.4.
7. **Preference & quy tắc làm việc của user.**

> **Tên gọi ổn định** — luôn tham chiếu bằng tên này, không phụ thuộc số thứ tự (số chỉ là gợi ý vị trí):
> mục 1–5 = **nội dung chuẩn hóa** · mục 6 = **Trạng thái scope** · mục 7 = **Preference**.

Template mỗi mục (1–5, 7):
```
- [YYYY-MM-DD] **<Chủ đề>**: <1-3 dòng> (Nguồn: <Event ID>)
```

### 4.2 Quy tắc cập nhật

1. Đọc Memory hiện có **trước khi** ghi.
2. Không tạo mục trùng. Đã có → cập nhật mục cũ, ghi `(cập nhật YYYY-MM-DD)`.
3. Thông tin cũ đã bị thay thế bởi thay đổi **user xác nhận rõ ràng** → ghi đè bằng bản mới nhất, không giữ bản cũ.
4. **Xung đột chưa được user phân xử:** KHÔNG tự ghi đè, và **KHÔNG đưa nội dung đề xuất mới vào Memory**
   (Memory chỉ chứa nội dung đã xác nhận — §4.3).
   - Vẫn ghi bình thường các mục **không** xung đột trong cùng lượt.
   - Mục xung đột: giữ nguyên bản cũ, chèn **con trỏ**, không chèn nội dung:
     `⚠️ CONFLICT [YYYY-MM-DD]: xem Q&A <Q-xxx> / Work Log <Event ID> — chờ user quyết định`
   - Nội dung đề xuất thực tế nằm ở `practices/Q&A/<slug>_QA.md` hoặc bản ghi Work Log tương ứng.
   - §10 phải báo cáo số mục `CONFLICT`.
5. Gộp các mục cùng chủ đề. Chỉ xóa mục lỗi thời khi chắc chắn đã bị thay thế hoặc user đồng ý.

### 4.3 KHÔNG lưu vào Memory

- Giả định chưa được xác nhận → thuộc về Work Log (§3.5).
- Requirement mới **chưa được user/BA duyệt** → nội dung nằm ở `practices/Q&A/<slug>_QA.md`; dấu vết audit là bản ghi Work Log `REOPEN` / `Approval: PENDING` (§5). Memory chỉ đặt **change state** `PENDING_REVIEW`, KHÔNG đưa nội dung requirement vào các mục nội dung chuẩn hóa.
- Nội dung đề xuất đang CONFLICT → chỉ lưu con trỏ (§4.2.4).
- Dữ liệu tạm, nội dung brainstorm, lịch sử chat, thông tin đã bị thay thế.
- Bất kỳ dữ liệu nhạy cảm nào theo §7.

### 4.4 Trạng thái scope — HAI TRỤC ĐỘC LẬP

Trạng thái pipeline và trạng thái thay đổi là hai thứ khác nhau, **không được ghi đè lẫn nhau**.

| Trục | Nguồn chuẩn | Giá trị |
|---|---|---|
| **Pipeline state** — pipeline RBT đang ở đâu | `practices/testcases/**/<Feature>_rbt_state.md` | `PASSED` / `REMAINING` / bước hiện tại (vd `B3/B7`) |
| **Change state** — có thay đổi nào tác động nội dung đã duyệt không | **Memory — mục *Trạng thái scope*** (Memory sở hữu trục này) | `NONE` / `PENDING_REVIEW` / `REOPEN_REQUIRED` |

Dòng ghi ở mục *Trạng thái scope*:
```
- **<tên gốc>** (`<slug>`): pipeline=<...> · change=<...> · state file: <đường dẫn | N/A> · memory: memory/<slug>_MEMORY.md
```

**Quy tắc đối soát (§6.3, trước khi ghi):**
- Chỉ đối soát **pipeline state** với `<Feature>_rbt_state.md`. Lệch → lấy state file làm chuẩn, sửa Memory theo, báo user.
- ⛔ **Việc đối soát TUYỆT ĐỐI KHÔNG được chạm vào change state.** Cờ `PENDING_REVIEW` / `REOPEN_REQUIRED` chỉ
  đổi theo §5, bởi sự kiện REOPEN hoặc bởi quyết định duyệt của user — không bao giờ bị xóa do đồng bộ pipeline.
- Feature không có file state → ghi `state file: N/A`, pipeline state tự quản trong Memory, không bịa ra file.

**Ý nghĩa change state:**

| Giá trị | Nghĩa |
|---|---|
| `NONE` | Không có thay đổi nào đang chờ |
| `PENDING_REVIEW` | Có requirement/spec mới **chưa được duyệt** có khả năng tác động — nội dung đã PASS **vẫn còn hiệu lực** cho tới khi BA trả lời |
| `REOPEN_REQUIRED` | Thay đổi **đã được duyệt** → nội dung đã PASS mất hiệu lực, phải làm lại |

**Biểu diễn PARTIAL:** một event `PARTIAL` không tạo giá trị pipeline state riêng. Ghi tách phần:
```
pipeline=PASSED <phần đã duyệt> + REMAINING <phần chưa duyệt>
```
Ví dụ: `pipeline=PASSED B1-B4 + REMAINING B5-B7`.

---

## 5. Requirement mới làm thay đổi nội dung đã PASS (REOPEN)

1. Xác định phạm vi bị ảnh hưởng: artifact, testcase, module liên quan.
2. Thông báo cho user danh sách nội dung bị ảnh hưởng.
3. **Xử lý theo trạng thái duyệt của requirement mới:**

| Trạng thái requirement | Hành động |
|---|---|
| **Chưa được user/BA duyệt** | ⛔ KHÔNG cập nhật các mục nội dung chuẩn hóa trong Memory. Nội dung ghi vào `practices/Q&A/<slug>_QA.md`. Ghi bản ghi Work Log `Trạng thái: REOPEN`, `Approval: PENDING`. Đặt change state = `PENDING_REVIEW`. Pipeline state **giữ nguyên**. |
| **Đã được user/BA duyệt** | Đặt change state = `REOPEN_REQUIRED`. Cập nhật các mục nội dung chuẩn hóa theo §4.2. Ghi bản ghi Work Log `REOPEN` / `Approval: APPROVED`. Cập nhật `<Feature>_rbt_state.md` nếu pipeline phải quay lại bước trước. |

> **Lý do:** rule *SRS Fidelity & Non-Inference* cấm đưa nội dung chưa được BA xác nhận vào artifact, và
> `practices/Q&A/<slug>_QA.md` là review gate chính thức. Memory được nạp ở mọi session sau như sự thật đã chốt —
> nên không được phép đi vòng qua gate đó.
> Dấu vết audit (Work Log + change state) **vẫn phải ghi** kể cả khi requirement chưa duyệt và kể cả khi đang còn
> blocking issue — cái bị cấm là ghi **nội dung** requirement vào Memory, không phải cấm ghi log.

4. Luôn ghi **bản ghi Work Log mới**, không sửa bản ghi cũ.

---

## 6. Khi bắt đầu session mới

1. Chỉ đọc Memory khi task **tiếp nối một scope/dự án đã có**. Task độc lập (sửa script lẻ, hỏi đáp nhanh) → bỏ qua, tránh tốn context.
2. File chưa tồn tại → **bỏ qua bước này, không tạo file rỗng**.
3. Đọc theo thứ tự ưu tiên, dừng ngay khi đủ thông tin:
   1. `PROJECT_MEMORY.md` — mục *Trạng thái scope* + mục *Preference*
   2. `memory/<slug>_MEMORY.md` của **đúng feature** đang làm — không đọc memory của feature khác
   3. Tối đa **3 bản ghi Work Log gần nhất** của feature đó. Không đọc `archive/` trừ khi user hỏi lịch sử.
4. Tóm tắt ngắn: pipeline state, change state (`PENDING_REVIEW` / `REOPEN_REQUIRED`), mục `CONFLICT` nếu có.
5. Không phân tích lại nội dung đã PASS nếu không có thay đổi.

---

## 7. Bảo mật & Redaction — che/ẩn dữ liệu nhạy cảm (áp dụng cho CẢ HAI loại file)

Trường `Bằng chứng` của Work Log là nơi dễ dính dữ liệu thật nhất — redaction áp dụng cho Work Log **ngang bằng** Memory.

**CẤM ghi vào cả Work Log lẫn Memory:**
- Mật khẩu, token, API key, session cookie → nếu cần nhắc tới, ghi `[ĐÃ ẨN]`.
- Dữ liệu cá nhân (CMND/CCCD, số tài khoản, số điện thoại, email thật của khách hàng).
- Dữ liệu production thật → thay bằng dữ liệu mô tả (`<mã DN hợp lệ>`, `<ngày trong quá khứ>`).
- Output log thô chưa lọc — chỉ trích phần cần thiết để truy vết.

> `practices/worklog/` đã được thêm vào `.gitignore` — đây là log nội bộ, không commit.
> Nếu team muốn chia sẻ, gỡ entry đó **và** rà lại toàn bộ nội dung theo mục này trước khi commit.

---

## 8. Lưu trữ & giới hạn kích thước

| File | Ngưỡng | Hành động khi vượt |
|---|---|---|
| `PROJECT_MEMORY.md` | **≤ 150 dòng** (index + *Trạng thái scope* + *Preference* + cross-feature) | Gộp/nén. Nội dung chi tiết của feature phải nằm ở file memory riêng, không dồn vào đây. |
| `memory/<slug>_MEMORY.md` | **≤ 200 dòng**, mỗi mục nội dung **≤ 40 dòng** | Gộp/nén các mục cùng chủ đề, xóa mục đã bị thay thế theo §4.2.5. |
| `<slug>_WORKLOG.md` | **> 300 dòng** | **Rotate nguyên file** (§8.1). |

### 8.1 Rotate Work Log — không được cắt lẻ bản ghi

Append-only nghĩa là **không bao giờ chỉnh sửa nội dung bản ghi**, kể cả khi lưu trữ. Vì vậy:

1. Sinh tên archive **duy nhất** theo timestamp đầy đủ (§3.3):
   `practices/worklog/archive/<slug>_WORKLOG-<YYYYMMDD-HHmmss>.md`
   > ⛔ Không dùng `<YYYY-MM>` — rotate hai lần trong cùng tháng sẽ đè mất archive trước.
2. **Kiểm tra file đích trước khi ghi.** Nếu đã tồn tại → **dừng, báo lỗi**, không ghi đè trong mọi trường hợp.
3. Di chuyển **toàn bộ** file active sang tên đó, giữ nguyên 100% nội dung.
4. Tạo file active mới chỉ gồm heading chuẩn (§1.3) + dòng:
   `> Archive trước đó: archive/<tên archive>`
5. ⛔ KHÔNG chép bản ghi nào sang file mới, KHÔNG cắt/ghép/sửa bản ghi.
6. Việc rotate phải được nêu trong báo cáo §10.

---

## 9. Fallback khi không ghi được file

Không có quyền ghi / sai đường dẫn / môi trường không hỗ trợ → xuất nội dung ra cuối response dưới hai tiêu đề:

```
### 📝 Work Log
### 🧠 Memory Update
```

Nêu rõ lý do không ghi được để user tự lưu. Không im lặng bỏ qua.

---

## 10. Báo cáo sau khi ghi

> Gộp chung vào block **Tier 3 — Execution & Audit Summary** của Logging Strategy. KHÔNG tạo báo cáo tách rời.

- Work Log: đã ghi `<đường dẫn>` — Event ID `<...>`, trạng thái `<PASS|PARTIAL|REOPEN|CORRECTION>`, approval `<...>`.
- Memory: thêm X mục, cập nhật Y mục, `⚠️ CONFLICT` Z mục cần user quyết định.
- Trạng thái scope: `pipeline=<...>` · `change=<NONE|PENDING_REVIEW|REOPEN_REQUIRED>`.
- Đối soát state file: khớp / lệch (nêu rõ) / N/A — và xác nhận change state **không** bị thay đổi bởi lần đối soát.
- Rotate (nếu có): đã chuyển `<file>` sang `<archive path>`.
