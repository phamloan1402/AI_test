# Dấu hiệu nhận biết SRS mơ hồ, chưa rõ ràng

SRS mơ hồ là khi một yêu cầu có thể được hiểu theo nhiều cách khác nhau bởi các đối tượng khác nhau (BA, Dev, Tester, User) mà không ai sai — dẫn đến không thể viết test case có tiêu chí Pass/Fail rõ ràng. Dùng 5 nhóm dấu hiệu dưới đây để soi bất kỳ đoạn SRS/user story nào.

## 1. Dùng từ định tính, không định lượng

| ❌ Mơ hồ | Vì sao mơ hồ | ✅ Nên viết |
|---|---|---|
| Hệ thống phải phản hồi nhanh | "Nhanh" là bao nhiêu giây? | Phản hồi ≤ 2 giây với 95% request |
| Cho phép nhập một số lượng lớn sản phẩm | "Lớn" là bao nhiêu? | Cho phép nhập tối đa 500 sản phẩm/lần |
| Mật khẩu phải đủ mạnh | "Mạnh" theo tiêu chí nào? | ≥ 8 ký tự, có hoa/thường/số/ký tự đặc biệt |
| Giao diện thân thiện, dễ sử dụng | Không đo lường được | Cần Acceptance Criteria cụ thể, hoặc loại khỏi SRS nếu chỉ là mô tả cảm tính |

Danh sách đầy đủ bên dưới chia theo 6 nhóm từ khóa cờ đỏ (bản dịch tiếng Việt kèm từ gốc tiếng Anh, vì nhiều SRS/tài liệu tham khảo quốc tế dùng thuật ngữ tiếng Anh) — dùng Ctrl+F rà từng nhóm khi review một tài liệu SRS.

### 1.1 Từ định tính/chủ quan không đo lường được

| Từ/cụm từ tiếng Việt | Từ gốc tiếng Anh | Gợi ý viết lại |
|---|---|---|
| nhanh, nhanh chóng | fast, quick | Nêu số giây/mili-giây cụ thể (VD: ≤2 giây) |
| chậm | slow | Nêu ngưỡng thời gian tối đa chấp nhận được |
| thân thiện với người dùng | user-friendly | Thay bằng Acceptance Criteria đo lường được (VD: hoàn thành thao tác trong ≤3 bước) hoặc bỏ khỏi SRS |
| dễ dàng, đơn giản | easy, simple | Mô tả cụ thể số bước/thao tác thay vì cảm tính |
| trực quan | intuitive | Không đo lường được — thay bằng kịch bản UAT cụ thể |
| phù hợp, hợp lý, thích hợp | appropriate, reasonable, suitable | Liệt kê rõ điều kiện/tiêu chí để được coi là phù hợp (bảng rule) |
| đầy đủ, đủ, thỏa đáng | adequate, sufficient, enough | Liệt kê danh sách cụ thể các thành phần/số lượng bắt buộc |
| đúng đắn, chính xác | proper, correct, accurate | Nêu rõ tiêu chí đúng/sai cụ thể, hoặc sai số cho phép (VD: ±0.01) |
| hiệu quả, có tác dụng | efficient, effective | Nêu chỉ số đo lường hiệu quả cụ thể (VD: giảm 20% thời gian xử lý) |
| tối ưu, tốt nhất, tốt hơn, được cải thiện | optimal, best, better, improved | Nêu số liệu so sánh cụ thể trước/sau |
| liền mạch, mượt mà, trơn tru | seamless, smooth | Mô tả cụ thể hành vi kỹ thuật (VD: không có màn hình loading giữa 2 bước) |
| mạnh mẽ, ổn định, đáng tin cậy | robust, reliable, stable | Nêu chỉ số cụ thể (VD: uptime 99.9%, MTBF ≥ 720 giờ) |
| bảo mật, an toàn | secure | Xem mục 1.6 — luôn cần tiêu chí bảo mật cụ thể, không dùng chung chung |
| linh hoạt | flexible | Liệt kê rõ phạm vi/giá trị được phép thay đổi |
| có khả năng mở rộng | scalable | Nêu con số cụ thể (VD: mở rộng lên 10.000 user mà không đổi kiến trúc) |
| khi cần thiết, khi phù hợp, khi được yêu cầu, nếu cần, khi áp dụng được | as needed, as appropriate, as required, if necessary, when applicable | Liệt kê rõ điều kiện kích hoạt cụ thể — nếu không liệt kê được, đây là dấu hiệu rule chưa được nghĩ đến đầy đủ |
| v.v., và tương tự, và những thứ tương tự | etc., and so on, and the like | Liệt kê đầy đủ danh sách — "v.v." trong SRS luôn là dấu hiệu thiếu sót |

### 1.2 Định lượng mơ hồ (số lượng không rõ ràng)

| Từ/cụm từ tiếng Việt | Từ gốc tiếng Anh | Gợi ý viết lại |
|---|---|---|
| một vài, một số ít | several, a few | Nêu con số hoặc khoảng cụ thể (VD: 2–3) |
| nhiều, rất nhiều | many, multiple, a lot | Nêu ngưỡng cụ thể (VD: > 10) |
| một số, một số lượng | some, a number of | Nêu con số hoặc điều kiện lọc cụ thể |
| nhiều loại, đa dạng | various | Liệt kê danh sách cụ thể |
| hầu hết, gần như | most, almost, nearly | Nêu tỷ lệ % cụ thể (VD: ≥95%) |
| xấp xỉ, khoảng | approximately, around, about | Nêu giá trị chính xác hoặc khoảng sai số cho phép (VD: 100 ±5) |

### 1.3 So sánh/tương đối chưa có mốc so sánh

| Từ/cụm từ tiếng Việt | Từ gốc tiếng Anh | Gợi ý viết lại |
|---|---|---|
| tốt hơn, tệ hơn | better, worse | So với cái gì? Nêu rõ baseline và mức chênh lệch cụ thể |
| cao hơn, thấp hơn, lớn hơn, nhỏ hơn, nhiều hơn, ít hơn | higher, lower, larger, smaller, more, less | Nêu giá trị baseline và giá trị đích cụ thể |
| tăng lên, giảm xuống | increased, decreased | Nêu % hoặc số liệu tăng/giảm cụ thể so với mốc nào |
| được nâng cao, được tối ưu hóa | enhanced, optimized | Nêu chỉ số đo lường trước/sau cụ thể |

### 1.4 Mơ hồ về thời gian (không có tiêu chí đo lường)

| Từ/cụm từ tiếng Việt | Từ gốc tiếng Anh | Gợi ý viết lại |
|---|---|---|
| kịp thời, đúng lúc | promptly, timely | Nêu khung thời gian cụ thể (VD: trong vòng 5 phút) |
| ngay lập tức | immediately | Nêu độ trễ tối đa cho phép (VD: ≤1 giây) |
| sớm, càng sớm càng tốt | soon, as soon as possible | Nêu deadline/SLA cụ thể |
| thời gian thực, gần thời gian thực | real-time, near real-time | Nêu độ trễ cụ thể (VD: cập nhật trong ≤500ms) |

### 1.5 Mơ hồ về hiệu năng (không có tiêu chí đo lường)

| Từ/cụm từ tiếng Việt | Từ gốc tiếng Anh | Gợi ý viết lại |
|---|---|---|
| hiệu năng cao | high performance | Nêu chỉ số cụ thể (throughput, response time) |
| phản hồi nhanh | fast response | Response time ≤ X giây với Y% request |
| độ trễ thấp | low latency | Nêu ngưỡng độ trễ cụ thể (VD: ≤100ms) |
| thông lượng cao | high throughput | Nêu số request/giây cụ thể (VD: ≥1000 TPS) |
| xử lý được tải cao | handles high load | Nêu số lượng concurrent user/request cụ thể |
| hiệu quả, được tối ưu hóa | efficient, optimized | Nêu chỉ số benchmark cụ thể |
| chi phí phát sinh tối thiểu | minimal overhead | Nêu % hoặc con số overhead tối đa chấp nhận được |
| hiệu năng chấp nhận được, hiệu năng tốt | acceptable performance, good performance | Nêu ngưỡng SLA cụ thể — "chấp nhận được" theo ai? |
| không bị chậm đi | does not slow down | Nêu ngưỡng suy giảm hiệu năng tối đa cho phép (VD: không quá 10%) |
| hoạt động tốt khi chịu tải | performs well under load | Nêu kịch bản tải cụ thể (số user, thời gian) và ngưỡng response time tương ứng |

### 1.6 Mơ hồ về bảo mật (không có tiêu chí đo lường)

| Từ/cụm từ tiếng Việt | Từ gốc tiếng Anh | Gợi ý viết lại |
|---|---|---|
| bảo mật, an toàn, được bảo vệ | secure, safe, protected | Nêu rõ cơ chế cụ thể (mã hóa gì, chuẩn nào) — xem nhóm Q trong checklist 96 tiêu chí |
| được mã hóa | encrypted | Nêu thuật toán/độ dài khóa cụ thể (VD: AES-256) |
| được xác thực, được phân quyền/ủy quyền | authenticated, authorized | Nêu cơ chế cụ thể (VD: OAuth2, MFA, RBAC theo role nào) |
| chống giả mạo | tamper-proof | Nêu cơ chế kiểm tra toàn vẹn cụ thể (checksum, chữ ký số...) |
| chống chịu được tấn công | resistant to attacks | Nêu loại tấn công cụ thể được phòng chống (VD: chống SQL injection, rate limit chống brute-force) |
| tuân theo thông lệ tốt nhất, bảo mật theo tiêu chuẩn ngành | follows best practices, industry standard security | Nêu rõ tiêu chuẩn cụ thể (VD: OWASP Top 10, PCI-DSS, ISO 27001) |
| bảo mật đầy đủ, bảo mật mạnh | adequate security, strong security | Không có nghĩa nếu thiếu tiêu chí đo — nêu rõ yêu cầu cụ thể |
| ngăn chặn truy cập trái phép | prevents unauthorized access | Nêu cơ chế cụ thể (RBAC, IP whitelist, rate limit...) |
| dữ liệu được bảo vệ | data is protected | Nêu rõ dữ liệu nào, bảo vệ bằng cơ chế gì (mã hóa at-rest/in-transit) |

**Mẹo dùng nhanh:** khi rà một SRS, mở file này và Ctrl+F từng cụm tiếng Việt lẫn tiếng Anh gốc (nhiều SRS Việt Nam chèn xen từ tiếng Anh) trong tài liệu — mỗi lần bắt được 1 từ trong 6 bảng trên là 1 điểm cần hỏi lại BA.

## 2. Thiếu điều kiện biên (boundary chưa định nghĩa)

- "Số lượng đặt hàng không được vượt quá giới hạn cho phép" — giới hạn là bao nhiêu? >= hay >?
- "Tuổi khách hàng phải hợp lệ" — hợp lệ là 0–150? 18–99? Có cho phép 0 không?
- "File upload không được quá lớn" — dung lượng cụ thể (MB)? định dạng nào?

→ Tester không biết test giá trị biên ở đâu, dễ bỏ sót boundary case.

## 3. Đại từ / liên từ mơ hồ, câu ghép nhiều nghĩa

- "Nếu đơn hàng bị hủy hoặc hết hạn, hệ thống sẽ gửi email và cập nhật trạng thái" — gửi email cho ai? Cập nhật trạng thái thành gì? Cả 2 trường hợp xử lý giống nhau hay khác nhau?
- "Người dùng có thể chỉnh sửa hoặc xóa đơn hàng nếu chưa được duyệt" — "chưa được duyệt" là trạng thái nào?

→ Câu có "và/hoặc", "nếu...thì" lồng nhau mà không tách rõ từng nhánh là dấu hiệu mơ hồ điển hình.

## 4. Thiếu rule xử lý ngoại lệ / lỗi

- "Hệ thống xử lý thanh toán qua cổng thanh toán bên thứ 3" — nếu timeout thì sao? Rollback hay giữ trạng thái pending?
- "Import file Excel danh sách nhân viên" — nếu sai định dạng, trùng mã, thiếu cột bắt buộc thì xử lý ra sao?

Đây là kiểu mơ hồ nguy hiểm nhất vì tester không phát hiện được thiếu sót cho đến khi test thực tế hoặc production gặp lỗi thật.

## 5. Nhiều actor/role nhưng mô tả chung chung

- "Người dùng có thể xem báo cáo doanh thu" — "người dùng" là Admin, Sales, hay Customer? Phạm vi dữ liệu xem được là gì?

## Các dấu hiệu khác cần cảnh giác

- Còn từ "TBD" (To Be Determined), "sẽ update sau" sót lại trong bản final.
- Mâu thuẫn giữa 2 phần trong cùng SRS, hoặc giữa SRS và wireframe/API spec.
- Không có Acceptance Criteria cụ thể (chỉ mô tả chung, không có Given-When-Then).
- Requirement không có REQ-ID để trace, không rõ version nào là bản mới nhất.
- Business rule diễn đạt bằng văn xuôi dài dòng thay vì bảng/công thức.
- Điều kiện kiểm tra trùng lặp (duplicate check) không nêu rõ: phạm vi (file/tab/toàn hệ thống), có phân biệt hoa/thường không, có trim khoảng trắng không, có xét composite key (nhiều field cùng lúc) hay chỉ 1 field.

---

# Ví dụ minh họa chi tiết (mô hình chuẩn để theo khi review)

Mỗi ví dụ dưới đây trình bày đúng 4 phần: **SRS gốc** → **Vấn đề** → **Câu hỏi cần hỏi lại BA** → **Viết lại rõ ràng** → **Test case rút ra được**. Dùng làm mẫu khi review một đoạn SRS thực tế.

## Ví dụ 1: Chức năng đăng nhập — khóa tài khoản

**SRS gốc:** "Hệ thống sẽ khóa tài khoản nếu người dùng đăng nhập sai nhiều lần."

**Vấn đề:**
- "Nhiều lần" là bao nhiêu? Không có con số cụ thể.
- Không rõ khóa tạm thời hay vĩnh viễn, khóa trong bao lâu.
- Không rõ đếm theo tài khoản, theo IP, hay cả hai.

**Câu hỏi cần hỏi BA:**
- Ngưỡng chính xác là bao nhiêu lần (3, 5, hay 10)?
- Khóa trong bao lâu (15 phút, 1 giờ, hay khóa vĩnh viễn cần admin mở)?
- Đếm theo IP, theo tài khoản, hay cả hai?
- Sau khi hết thời gian khóa, bộ đếm có reset về 0 không?

**Viết lại rõ ràng:** Nếu người dùng nhập sai mật khẩu 5 lần liên tiếp trong vòng 15 phút (tính theo tài khoản), hệ thống khóa tài khoản trong 30 phút. Sau 30 phút, bộ đếm reset về 0. Hiển thị message: "Tài khoản đã bị khóa, vui lòng thử lại sau 30 phút."

**Test case rút ra được:**
- Boundary: lần sai thứ 4 (chưa khóa) vs lần thứ 5 (khóa) vs lần thứ 6 (đã khóa, không cho nhập dù đúng password).
- Negative: nhập sai password nhiều lần với các tài khoản không tồn tại.
- Exception: hết 30 phút khóa, đăng nhập lại đúng — có cho vào không, bộ đếm có reset đúng không.

## Ví dụ 2: Đặt hàng — số lượng sản phẩm

**SRS gốc:** "Khách hàng có thể đặt một số lượng lớn sản phẩm trong một đơn hàng."

**Vấn đề:**
- "Lớn" không định lượng, không rõ số tối đa.
- Không rõ giới hạn dưới (có cho đặt số lượng 0 hoặc số âm không).
- Không rõ xử lý khi vượt tồn kho.

**Câu hỏi cần hỏi BA:**
- Số lượng tối thiểu/tối đa mỗi sản phẩm trong 1 đơn là bao nhiêu?
- Có giới hạn tổng số dòng sản phẩm/đơn không?
- Nếu vượt tồn kho thì chặn hoàn toàn hay cho đặt trước (backorder)?

**Viết lại rõ ràng:** Số lượng mỗi sản phẩm trong đơn hàng: tối thiểu 1, tối đa 99. Nếu nhập 0 hoặc số âm, hiển thị lỗi "Số lượng không hợp lệ". Nếu số lượng đặt lớn hơn tồn kho hiện có, hệ thống chặn submit và hiển thị "Chỉ còn {n} sản phẩm trong kho".

**Test case rút ra được:**
- Happy path: đặt số lượng = 1, = 99.
- Boundary: 0, 1, 99, 100.
- Negative: số âm, ký tự chữ, số thập phân.
- Exception: số lượng đặt vượt tồn kho tại thời điểm submit (race condition khi 2 người đặt cùng lúc).

## Ví dụ 3: Áp dụng mã giảm giá

**SRS gốc:** "Hệ thống áp dụng mã giảm giá phù hợp cho đơn hàng và thông báo cho khách hàng."

**Vấn đề:**
- "Phù hợp" là điều kiện gì, không định nghĩa rõ.
- Không rõ 1 đơn có được áp nhiều mã cùng lúc không.
- "Thông báo" là UI, email, hay cả hai — không rõ.

**Câu hỏi cần hỏi BA:**
- Điều kiện áp mã: theo giá trị đơn tối thiểu? theo danh mục sản phẩm? theo hạng thành viên?
- Có giới hạn 1 mã/đơn hay được combine nhiều mã?
- Mã hết hạn/hết lượt sử dụng xử lý message gì? Có case tài khoản đã dùng mã rồi không?

**Viết lại rõ ràng:** Mỗi đơn hàng chỉ áp dụng được 1 mã giảm giá. Điều kiện: giá trị đơn từ 200.000đ trở lên, mã còn hạn sử dụng, mã chưa vượt quá số lượt dùng tối đa/tài khoản (1 lượt/tài khoản). Nếu không đủ điều kiện, hiển thị message tương ứng: "Đơn hàng chưa đạt giá trị tối thiểu", "Mã đã hết hạn", "Bạn đã sử dụng mã này".

**Test case rút ra được:**
- Happy path: áp mã hợp lệ, đơn đủ điều kiện.
- Boundary: giá trị đơn đúng bằng 200.000đ, thấp hơn 1 đồng.
- Negative: nhập mã sai định dạng, mã không tồn tại.
- Exception: mã hợp lệ nhưng sản phẩm trong giỏ bị đổi giá sau khi áp mã, trước khi thanh toán.

## Ví dụ 4: Upload file danh sách nhân viên

**SRS gốc:** "Người dùng upload file không được quá lớn và đúng định dạng."

**Vấn đề:**
- Không nêu dung lượng cụ thể (MB).
- Không nêu định dạng file cụ thể được chấp nhận.
- Không mô tả behavior khi nội dung file sai cấu trúc.

**Câu hỏi cần hỏi BA:**
- Dung lượng tối đa là bao nhiêu MB?
- Định dạng cho phép: .xlsx, .csv, .pdf...?
- Nếu file đúng định dạng nhưng sai cấu trúc (thiếu cột, sai header) thì sao?
- Có validate tên file (ký tự đặc biệt, độ dài tên) không?

**Viết lại rõ ràng:** Cho phép upload file định dạng .xlsx, dung lượng tối đa 5MB. Nếu vượt 5MB: hiển thị "File vượt quá dung lượng cho phép (5MB)". Nếu sai định dạng: "Vui lòng upload file .xlsx". Nếu đúng định dạng nhưng thiếu cột bắt buộc (Mã NV, Họ tên, Email): hiển thị danh sách cột thiếu và không cho import.

**Test case rút ra được:**
- Boundary: file đúng 5MB, file 5MB + 1 byte.
- Negative: sai định dạng (.doc, .csv thay vì .xlsx), file rỗng.
- Exception: mất kết nối giữa lúc upload, file bị corrupt, trùng dữ liệu với bản ghi đã tồn tại.

## Ví dụ 5: Kiểm tra trùng dữ liệu (composite key dễ bị hiểu sai)

**SRS gốc:** "Trùng MAKHLQ thì hệ thống báo lỗi."

**Vấn đề — đây là dạng mơ hồ dễ bị bỏ sót nhất vì trông có vẻ đơn giản:**
- Trùng trong cùng file hay toàn hệ thống? Trùng trong cùng tab hay khác tab cũng tính?
- MAKHLQ giống nhưng field khác (VD TDNONGLQ) khác nhau có tính là trùng không — đây là điểm rủi ro cao nhất, quyết định đây là single-key check hay composite-key check.
- So sánh có phân biệt hoa/thường không? Có trim khoảng trắng trước khi check không?
- Nếu trùng thì reject cả file hay chỉ dòng lỗi? Message lỗi cụ thể là gì?

**Viết lại rõ ràng (kèm giả định cần xác nhận):** Hệ thống kiểm tra trùng MAKHLQ trên toàn hệ thống (không giới hạn trong file/tab đang thao tác), so sánh không phân biệt hoa/thường và đã trim khoảng trắng đầu-cuối. Chỉ cần MAKHLQ trùng là đủ điều kiện báo lỗi, không xét giá trị các field khác. Khi phát hiện trùng, hệ thống chỉ reject dòng dữ liệu bị lỗi, các dòng hợp lệ khác vẫn được import. Message: "MAKHLQ {giá trị} đã tồn tại trong hệ thống (dòng {n})".

**Bài học chung:** với bất kỳ yêu cầu "check trùng X" nào, luôn hỏi đủ 6 điểm: (1) phạm vi kiểm tra, (2) có phải composite key không, (3) phân biệt hoa/thường, (4) trim khoảng trắng, (5) reject toàn bộ hay reject từng dòng, (6) message lỗi cụ thể — thiếu 1 trong 6 điểm này là chưa đủ để viết test case duplicate-check.