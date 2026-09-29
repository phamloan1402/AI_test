# Checklist review SRS — 96 tiêu chí / 19 nhóm (A–S)

Danh sách chi tiết dùng khi cần review toàn diện một tài liệu SRS. Mỗi tiêu chí có mã, mức độ ưu tiên gợi ý (Cao/Trung bình/Thấp), và ví dụ cụ thể minh họa.

Lưu ý: các nhóm J (State/Transition), N (Đa ngôn ngữ), O (Audit log), P (Tương thích thiết bị), Q (Bảo mật & pháp lý), R (Migration dữ liệu) chỉ áp dụng khi nghiệp vụ đang review có liên quan — nếu không áp dụng, đánh dấu N/A, không tính là điểm trừ. Nhóm S (luồng liên chức năng) áp dụng khi SRS mô tả từ 2 chức năng/module trở lên có tương tác với nhau; nếu SRS chỉ mô tả 1 chức năng độc lập, đánh N/A cho nhóm S.


## Nhóm A — THÔNG TIN CHUNG & PHẠM VI TÀI LIỆU

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| A1 | Tài liệu có tiêu đề, mã tài liệu (Doc ID) và số phiên bản (version) rõ ràng | Thấp | VD: "SRS-ORDER-v2.3", cập nhật 15/03/2026, phê duyệt bởi Nguyễn Văn A (PM) |
| A2 | Có ngày cập nhật gần nhất và người phê duyệt (approver) được ghi rõ | Thấp | VD: Cập nhật lần cuối 20/03/2026 bởi BA Trần Thị B; đã duyệt bởi PM ngày 21/03/2026 |
| A3 | Có bảng lịch sử thay đổi (change log) ghi rõ nội dung thay đổi theo từng version | Thấp | VD: v1.0 (khởi tạo) → v1.1 (bổ sung rule chiết khấu) → v2.0 (thêm tích hợp thanh toán) |
| A4 | Mục tiêu nghiệp vụ (business objective) của chức năng được nêu rõ, không chung chung | Trung bình | VD: "Cho phép khách đặt hàng online và nhận thông báo trạng thái qua email" (không chỉ ghi "cải thiện trải nghiệm") |
| A5 | Phạm vi trong (in-scope) của release/sprint hiện tại được liệt kê cụ thể | Cao | VD in-scope: đặt hàng, thanh toán online, hủy đơn trong 24h |
| A6 | Phạm vi ngoài (out-of-scope) được liệt kê rõ, tránh hiểu nhầm là thiếu sót khi test | Cao | VD out-of-scope: chưa hỗ trợ đặt hàng qua app di động, chưa tích hợp ví điện tử X |
| A7 | Có liên kết đầy đủ tới tài liệu liên quan (BRD, wireframe, API spec) và link còn truy cập được | Trung bình | VD: link Figma, link Swagger API spec, link BRD gốc — kiểm tra từng link có mở được không |

## Nhóm B — ACTOR / ROLE & PHÂN QUYỀN

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| B1 | Liệt kê đầy đủ toàn bộ actor/role tham gia hệ thống (Admin, Sales, Customer, Guest, System/Batch job...) | Cao | VD: Admin, Sales Staff, Customer (đã đăng nhập), Guest (chưa đăng nhập), Batch job đối soát cuối ngày |
| B2 | Có ma trận phân quyền (permission matrix) chi tiết cho từng chức năng: ai được xem/thêm/sửa/xóa/duyệt | Cao | VD bảng: chức năng "Duyệt đơn hàng" — Admin: Có, Sales: Không, Customer: Không |
| B3 | Có mô tả rõ hành vi khi actor không đủ quyền truy cập (message lỗi, redirect trang nào) | Trung bình | VD: Sales cố truy cập trang Duyệt đơn hàng → redirect về Dashboard, hiển thị "Bạn không có quyền truy cập chức năng này" |
| B4 | Có mô tả rõ trường hợp 1 tài khoản có nhiều role cùng lúc (nếu có) thì áp dụng quyền theo rule nào | Trung bình | VD: tài khoản vừa Sales vừa Admin tạm quyền — áp dụng quyền cao nhất (Admin) hay theo role đang active? |

## Nhóm C — BUSINESS RULE / CÔNG THỨC TÍNH TOÁN

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| C1 | Business rule/công thức được trình bày bằng bảng hoặc công thức tường minh, không phải văn xuôi dài dòng | Cao | VD bảng chiết khấu: Đơn <500k: 0%, 500k–1tr: 5%, >1tr: 10% (thay vì viết "chiết khấu theo giá trị đơn") |
| C2 | Không còn mục nào ghi "TBD/TBC/sẽ update sau" trong bản SRS final | Cao | VD: rà lại toàn bộ SRS, không còn dòng nào ghi "(sẽ cập nhật sau khi họp Kế toán)" |
| C3 | Có nêu rõ thứ tự ưu tiên áp dụng khi nhiều rule/điều kiện cùng thỏa mãn (rule conflict priority) | Cao | VD: đơn vừa đủ điều kiện mã giảm giá vừa đủ điều kiện free ship → áp mã giảm giá trước, tính ship sau khi đã giảm |
| C4 | Có ít nhất 1 ví dụ số liệu cụ thể minh họa cho mỗi công thức tính toán phức tạp | Trung bình | VD: đơn 1.200.000đ → chiết khấu 10% = 120.000đ → thành tiền 1.080.000đ |

## Nhóm D — ACCEPTANCE CRITERIA

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| D1 | Mỗi user story/use case đều có Acceptance Criteria riêng, không dùng chung chung cho nhiều case | Cao | VD: US-045 "Áp mã giảm giá" có AC riêng, không dùng chung AC của US-044 "Đặt hàng" |
| D2 | Acceptance Criteria được viết theo cấu trúc Given-When-Then hoặc cấu trúc tương đương rõ ràng | Cao | VD: Given giỏ hàng 300.000đ, When nhập mã "SALE10", Then báo lỗi "Đơn hàng chưa đạt giá trị tối thiểu 200.000đ" |
| D3 | Mỗi Acceptance Criteria cho ra kết quả Pass/Fail đo lường được, không mập mờ | Cao | VD: sửa AC "hệ thống xử lý nhanh" thành "hệ thống trả kết quả trong ≤2 giây" để đo được Pass/Fail |
| D4 | Không còn Acceptance Criteria dùng từ định tính (nhanh, phù hợp, thân thiện, hợp lý...) | Cao | VD cần loại bỏ: "giao diện thân thiện" → thay bằng tiêu chí đo lường cụ thể hoặc bỏ khỏi AC |

## Nhóm E — DATA DICTIONARY / ĐẶC TẢ FIELD

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| E1 | Mỗi field có định nghĩa kiểu dữ liệu rõ ràng (String/Number/Date/Boolean...) | Cao | VD: MaKH – String, NgaySinh – Date, SoLuong – Number, DaXacNhan – Boolean |
| E2 | Mỗi field có độ dài tối thiểu/tối đa cụ thể (nếu áp dụng) | Cao | VD: Họ tên tối đa 100 ký tự, Số điện thoại đúng 10 chữ số |
| E3 | Mỗi field xác định rõ Mandatory hay Optional | Cao | VD: Email – Mandatory, Số fax – Optional |
| E4 | Mỗi field có định dạng cụ thể (VD: dd/mm/yyyy, email regex, số điện thoại 10 số) | Cao | VD: Ngày sinh dd/mm/yyyy; Email theo regex RFC 5322; SĐT 10 số bắt đầu bằng 0 |
| E5 | Mỗi field có giá trị mặc định (default value) nếu có, nêu rõ giá trị | Trung bình | VD: Trạng thái đơn hàng mặc định = "Draft" khi mới tạo |
| E6 | Mỗi field có validation rule cụ thể: unique, range, dependency với field khác | Cao | VD: MaKH unique toàn hệ thống; Tuổi phải ≥18 nếu đăng ký tài khoản Premium |
| E7 | Với field dùng để check trùng lặp: có quy định rõ phân biệt hoa/thường không? có trim khoảng trắng trước khi so sánh không? | Cao | VD: so sánh MaKHLQ không phân biệt hoa/thường, có trim khoảng trắng đầu-cuối trước khi check trùng |
| E8 | Có quy định rõ phạm vi kiểm tra trùng lặp: trong 1 dòng/file, trong tab, hay toàn hệ thống | Cao | VD: check trùng MaKHLQ trên toàn hệ thống, không chỉ trong file đang import |

## Nhóm F — LUỒNG XỬ LÝ (HAPPY / ALTERNATIVE / EXCEPTION)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| F1 | Có mô tả đầy đủ Happy path (luồng chính) theo từng bước, kèm kết quả mong đợi | Cao | VD: B1 Chọn sản phẩm → B2 Thêm giỏ hàng → B3 Thanh toán → B4 Nhận email xác nhận |
| F2 | Có mô tả Alternative flow (luồng phụ vẫn hợp lệ) nếu nghiệp vụ có nhiều kịch bản hợp lệ | Trung bình | VD: khách vãng lai đặt hàng không cần đăng nhập vs khách đã đăng nhập dùng địa chỉ đã lưu |
| F3 | Có mô tả Exception flow: lỗi hệ thống (timeout, mất kết nối), lỗi dữ liệu (duplicate, conflict) | Cao | VD: cổng thanh toán timeout 30s → hệ thống rollback đơn về "Chờ thanh toán", cho phép thử lại |
| F4 | Có danh sách đầy đủ error message/mã lỗi tương ứng cho từng trường hợp lỗi | Cao | VD bảng: Hết hàng → "Sản phẩm X đã hết hàng"; Timeout → "Giao dịch quá thời gian chờ, vui lòng thử lại" |
| F5 | Có nêu rõ hành vi xử lý khi lỗi xảy ra: reject toàn bộ hay chỉ phần dữ liệu bị lỗi (VD: file nhiều dòng) | Cao | VD: file Excel 100 dòng, 3 dòng lỗi định dạng → chỉ reject 3 dòng đó, 97 dòng còn lại vẫn import |
| F6 | Có sơ đồ luồng (flowchart) hoặc mô tả tuần tự đủ chi tiết cho luồng nghiệp vụ phức tạp | Trung bình | VD: đính kèm flowchart luồng thanh toán có nhánh rẽ khi thẻ bị từ chối |

## Nhóm G — WIREFRAME / MOCKUP / API SPEC

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| G1 | Có đính kèm wireframe/mockup cho mỗi màn hình liên quan đến yêu cầu | Trung bình | VD: đính kèm link Figma cho màn hình Giỏ hàng, Checkout, Xác nhận đơn hàng |
| G2 | Có API spec đầy đủ: request/response mẫu, status code, header, error schema | Trung bình | VD: POST /api/orders → Request {productId, quantity}, Response 200 {orderId,status}, 400 {errorCode,message} |
| G3 | Nội dung SRS và wireframe không mâu thuẫn nhau (tên field, label khớp nhau) | Cao | VD: SRS ghi field "SoDienThoai" nhưng wireframe hiển thị label "Phone Number" — cần thống nhất |
| G4 | Có mô tả rõ trạng thái loading/empty/error trên giao diện (nếu áp dụng) | Trung bình | VD: giỏ hàng rỗng hiển thị "Giỏ hàng của bạn đang trống" kèm nút "Tiếp tục mua sắm" |

## Nhóm H — NON-FUNCTIONAL REQUIREMENT (NFR)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| H1 | Có yêu cầu performance cụ thể, đo lường được (VD: response time ≤ 2s với 95% request) | Trung bình | VD: API tra cứu đơn hàng phản hồi ≤2 giây với 95% request trong điều kiện tải bình thường |
| H2 | Có yêu cầu security cụ thể (mã hóa dữ liệu, phân quyền truy cập, session timeout) | Trung bình | VD: mật khẩu mã hóa bcrypt, session hết hạn sau 30 phút không hoạt động |
| H3 | Có yêu cầu khả năng chịu tải / số lượng concurrent user tối đa | Thấp | VD: hệ thống chịu tải 1.000 người dùng đồng thời trong giờ cao điểm 9h–11h, 20h–22h |
| H4 | Có yêu cầu tính khả dụng hệ thống (uptime SLA) nếu áp dụng | Thấp | VD: cam kết uptime 99.5%/tháng, bảo trì định kỳ thông báo trước 24h |

## Nhóm I — TÍCH HỢP HỆ THỐNG THỨ 3

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| I1 | Mô tả rõ hệ thống thứ 3 liên quan: tên hệ thống, mục đích tích hợp | Trung bình | VD: tích hợp cổng thanh toán VNPay để xử lý thanh toán online |
| I2 | Có contract dữ liệu trao đổi (field mapping) đầy đủ giữa 2 hệ thống | Cao | VD mapping: field "orderId" hệ thống A = field "ref_code" hệ thống B |
| I3 | Có quy định timeout/retry policy khi hệ thống thứ 3 lỗi hoặc không phản hồi | Cao | VD: timeout 15s, retry tối đa 3 lần, cách nhau 5s giữa các lần |
| I4 | Có mô tả rollback/compensation khi tích hợp thất bại giữa chừng | Cao | VD: trừ tiền thành công nhưng cập nhật đơn thất bại → tự động hoàn tiền và ghi log đối soát thủ công |

## Nhóm J — STATE / TRANSITION (NẾU CÓ VÒNG ĐỜI TRẠNG THÁI)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| J1 | Có sơ đồ trạng thái (state diagram) đầy đủ toàn bộ trạng thái của đối tượng | Cao | VD: Draft → Pending → Approved → Shipped → Completed; hoặc → Cancelled |
| J2 | Liệt kê rõ các transition hợp lệ giữa các trạng thái | Cao | VD: Pending → Approved (hợp lệ), Approved → Shipped (hợp lệ) |
| J3 | Liệt kê rõ các transition KHÔNG hợp lệ và behavior tương ứng (block, message lỗi) | Cao | VD: Completed → Pending là KHÔNG hợp lệ, hệ thống chặn và báo "Đơn hàng đã hoàn tất, không thể quay lại" |
| J4 | Nêu rõ actor/điều kiện nào được phép thực hiện transition nào | Trung bình | VD: chỉ Admin được chuyển Approved → Cancelled sau khi đã Shipped |

## Nhóm K — CHẤT LƯỢNG VIẾT (IEEE 830 / ISO-IEC-IEEE 29148)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| K1 | Correct: yêu cầu đã được stakeholder xác nhận, không phải giả định riêng của BA | Cao | VD: rule chiết khấu đã được Kế toán trưởng ký xác nhận qua email, đính kèm làm phụ lục |
| K2 | Unambiguous: không dùng từ định tính không định lượng (nhanh, lớn, phù hợp, linh hoạt...) | Cao | VD: thay "phản hồi nhanh" bằng "phản hồi ≤2 giây" |
| K3 | Complete: không thiếu case, không còn "TBD/TBC" | Cao | VD: rà soát không còn ô nào ghi TBD trong bảng Data Dictionary |
| K4 | Consistent: không mâu thuẫn giữa các phần trong SRS và với wireframe/API spec | Cao | VD: field "TrangThai" trong SRS và wireframe phải cùng danh sách giá trị (Draft/Pending/Approved...) |
| K5 | Verifiable/Testable: mỗi yêu cầu viết được test case cho kết quả Pass/Fail rõ ràng | Cao | VD: "Hệ thống khóa tài khoản sau 5 lần sai" viết được test case Pass/Fail rõ ràng |
| K6 | Traceable: có mã REQ-ID để trace sang test case/traceability matrix | Trung bình | VD: REQ-045 "Áp dụng mã giảm giá" trace sang TC-102, TC-103, TC-104 |
| K7 | Prioritized: có mức ưu tiên Must/Should/Could cho từng yêu cầu | Trung bình | VD: REQ-045 mức Must (bắt buộc release này), REQ-050 mức Could (có thể làm sau) |

## Nhóm L — DẤU HIỆU MƠ HỒ CẦN SOI KỸ (AMBIGUITY DETECTION)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| L1 | Không còn từ cờ đỏ định tính (nhanh, chậm, lớn, nhỏ, phù hợp, linh hoạt, thân thiện, hợp lý, đầy đủ, tối ưu, kịp thời, thường xuyên, một số, nhiều, ít...) | Cao | VD: rà từ khóa "nhanh, lớn, phù hợp" bằng Ctrl+F trong toàn bộ SRS |
| L2 | Mọi field/thông số có ngưỡng biên (min/max) được định nghĩa bằng con số cụ thể | Cao | VD: Tuổi khách hàng min=0, max=150; Số lượng SP/đơn min=1, max=99 |
| L3 | Không có câu ghép "và/hoặc", "nếu...thì" lồng nhau mà không tách rõ từng nhánh xử lý | Cao | VD: tách câu "nếu đơn hàng bị hủy hoặc hết hạn" thành 2 rule riêng: rule khi hủy, rule khi hết hạn |
| L4 | Mọi rule xử lý ngoại lệ/lỗi được mô tả tường minh, không bỏ ngỏ | Cao | VD: nêu rõ hành vi khi cổng thanh toán bên thứ 3 trả về lỗi không xác định (unknown error code) |
| L5 | Actor "người dùng" chung chung đã được cụ thể hóa thành role rõ ràng | Trung bình | VD: thay "người dùng có thể xem báo cáo" bằng "Admin và Sales Manager có thể xem báo cáo" |
| L6 | Không còn business rule phức tạp diễn đạt bằng văn xuôi dài dòng thay vì bảng/công thức | Trung bình | VD: chuyển đoạn văn mô tả cách tính thuế thành bảng công thức theo từng bậc thuế |

## Nhóm M — MÔI TRƯỜNG & DỮ LIỆU TEST

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| M1 | Đã xác định môi trường test cần thiết (config, tài khoản test theo từng role) | Trung bình | VD: cần 1 tài khoản Admin, 1 tài khoản Customer đã xác thực email, môi trường Staging kết nối sandbox cổng thanh toán |
| M2 | Đã xác định dữ liệu mẫu/dữ liệu giả lập cần chuẩn bị để test | Trung bình | VD: chuẩn bị 50 bản ghi khách hàng mẫu, trong đó 5 bản ghi trùng MaKHLQ để test duplicate case |
| M3 | Dependency giữa các field/màn hình khác nhau đã được mô tả rõ ràng | Cao | VD: field "Tỉnh/Thành" thay đổi thì field "Quận/Huyện" phải load lại theo danh sách tương ứng |

## Nhóm N — ĐA NGÔN NGỮ / LOCALIZATION (NẾU ÁP DỤNG)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| N1 | Đã liệt kê đầy đủ danh sách ngôn ngữ/vùng miền (locale) cần hỗ trợ | Trung bình | VD: hỗ trợ Tiếng Việt, English, 中文 (giản thể) cho phiên bản 2.0 |
| N2 | Có quy định rõ nguồn dịch thuật (translation key) và fallback ngôn ngữ khi thiếu bản dịch | Trung bình | VD: nếu thiếu bản dịch tiếng Trung, fallback hiển thị tiếng Anh thay vì để trống |
| N3 | Có quy định định dạng ngày giờ, số, tiền tệ theo từng locale (VD: dd/mm/yyyy vs mm/dd/yyyy) | Cao | VD: VN hiển thị 31/12/2026, US hiển thị 12/31/2026; VND hiển thị 1.000.000₫, USD hiển thị $1,000.00 |
| N4 | Có mô tả rõ xử lý văn bản dài do dịch thuật (truncate, wrap, overflow trên UI) | Thấp | VD: label nút "Đặt hàng ngay" dịch sang tiếng Đức dài hơn 40% — kiểm tra không vỡ giao diện nút |
| N5 | Có quy định rõ chuyển đổi múi giờ (timezone) khi hiển thị/lưu trữ dữ liệu ngày giờ | Cao | VD: đơn đặt lúc 23h59 giờ VN hiển thị đúng ngày giờ local khi khách ở múi giờ khác xem lại |

## Nhóm O — AUDIT LOG / LỊCH SỬ THAY ĐỔI DỮ LIỆU

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| O1 | Có quy định rõ những hành động nào cần ghi audit log (create/update/delete/login...) | Cao | VD: ghi log khi Admin sửa giá sản phẩm, khi user đổi mật khẩu, khi đơn hàng bị hủy |
| O2 | Có quy định rõ thông tin cần lưu trong audit log (ai, khi nào, giá trị cũ, giá trị mới) | Cao | VD: {user:"admin01", action:"update_price", old_value:100000, new_value:120000, timestamp:...} |
| O3 | Có quy định thời gian lưu trữ (retention) và quyền truy cập xem audit log | Trung bình | VD: lưu trữ audit log tối thiểu 2 năm, chỉ Admin cấp cao mới xem được log |
| O4 | Có mô tả rõ audit log có immutable (không sửa/xóa được) hay không | Cao | VD: audit log không cho phép sửa/xóa kể cả bởi Admin, chỉ có thể xem và export |

## Nhóm P — TƯƠNG THÍCH TRÌNH DUYỆT / THIẾT BỊ (COMPATIBILITY)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| P1 | Đã liệt kê danh sách trình duyệt và phiên bản tối thiểu cần hỗ trợ (Chrome, Safari, Edge...) | Trung bình | VD: hỗ trợ Chrome ≥100, Safari ≥15, Edge ≥100; không hỗ trợ Internet Explorer |
| P2 | Đã liệt kê danh sách thiết bị/độ phân giải màn hình cần hỗ trợ (desktop, tablet, mobile) | Trung bình | VD: hỗ trợ desktop ≥1280px, tablet 768–1024px, mobile 320–767px |
| P3 | Có mô tả rõ hành vi responsive/breakpoint khi thay đổi kích thước màn hình | Trung bình | VD: ở màn hình <768px, menu chuyển từ thanh ngang sang hamburger menu |
| P4 | Có mô tả rõ mức độ hỗ trợ khi dùng trình duyệt/thiết bị không nằm trong danh sách hỗ trợ | Thấp | VD: nếu trình duyệt không hỗ trợ, hiển thị "Vui lòng nâng cấp trình duyệt" thay vì để trắng trang |

## Nhóm Q — BẢO MẬT & PHÁP LÝ (SECURITY & COMPLIANCE)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| Q1 | Có yêu cầu tuân thủ quy định pháp lý liên quan (GDPR, Nghị định 13/2023/NĐ-CP, PCI-DSS...) nếu áp dụng | Cao | VD: tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân nếu lưu trữ dữ liệu người dùng Việt Nam |
| Q2 | Có quy định rõ dữ liệu nhạy cảm (PII) nào cần mã hóa khi lưu trữ và truyền tải | Cao | VD: mã hóa số CCCD, số thẻ ngân hàng bằng AES-256 khi lưu trong database |
| Q3 | Có quy định rõ chính sách xác thực (authentication) và phân quyền — MFA, SSO nếu áp dụng | Cao | VD: bắt buộc xác thực 2 lớp (OTP) khi Admin đăng nhập từ thiết bị lạ |
| Q4 | Có quy định rõ chính sách xử lý khi phát hiện truy cập trái phép/tấn công (rate limit, block IP, alert) | Trung bình | VD: khóa IP tạm thời 15 phút nếu phát hiện >20 request/giây từ cùng 1 IP |
| Q5 | Có quy định rõ quyền của người dùng đối với dữ liệu cá nhân (xem, sửa, xóa, xuất dữ liệu) nếu áp dụng | Trung bình | VD: khách hàng có thể yêu cầu xuất toàn bộ dữ liệu cá nhân hoặc xóa tài khoản qua mục Cài đặt |

## Nhóm R — MIGRATION DỮ LIỆU (NẾU CÓ CHUYỂN ĐỔI/NÂNG CẤP HỆ THỐNG)

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| R1 | Có mô tả rõ nguồn dữ liệu cần migrate và khối lượng dữ liệu ước tính | Trung bình | VD: migrate 500.000 bản ghi khách hàng từ hệ thống CRM cũ (SQL Server) sang PostgreSQL |
| R2 | Có quy định rõ mapping trường dữ liệu giữa hệ thống cũ và hệ thống mới | Cao | VD mapping: "cust_name" (cũ) → "full_name" (mới), "cust_dob" → "date_of_birth" |
| R3 | Có kế hoạch xử lý dữ liệu lỗi/không hợp lệ phát hiện trong quá trình migrate | Cao | VD: bản ghi thiếu email hợp lệ → đưa vào "migration_errors.csv" để xử lý thủ công, không migrate |
| R4 | Có kế hoạch rollback nếu migration thất bại giữa chừng | Cao | VD: nếu migration lỗi >5% số bản ghi, tự động rollback về trạng thái trước khi migrate |
| R5 | Có quy định rõ thời gian downtime cho phép (nếu có) khi thực hiện migration | Trung bình | VD: downtime tối đa cho phép 2 giờ, thực hiện 2h–4h sáng Chủ nhật |

## Nhóm S — LUỒNG NGHIỆP VỤ LIÊN CHỨC NĂNG & DEPENDENCY GIỮA CÁC CHỨC NĂNG

| Mã | Tiêu chí kiểm tra chi tiết | Ưu tiên | Ví dụ / Gợi ý cụ thể |
|---|---|---|---|
| S1 | Đã xác định rõ chức năng nào phụ thuộc vào chức năng nào khác, và thứ tự thực hiện bắt buộc giữa các chức năng | Cao | VD: phải tạo hồ sơ Khách hàng (chức năng Quản lý khách hàng) thành công trước khi cho phép tạo Đơn hàng (chức năng Đặt hàng) cho khách đó |
| S2 | Đã mô tả rõ tác động dây chuyền (side-effect) khi 1 chức năng thay đổi dữ liệu — các chức năng khác dùng chung dữ liệu đó có bị ảnh hưởng/cập nhật theo không | Cao | VD: Hủy đơn hàng (Quản lý đơn) có tự động hoàn tồn kho (Quản lý kho), hủy điểm tích lũy (Loyalty), hủy mã giảm giá đã áp (Khuyến mãi) hay không |
| S3 | Có sơ đồ luồng nghiệp vụ tổng thể (end-to-end/cross-functional flow) thể hiện chuỗi chức năng tham gia trong 1 quy trình lớn, không chỉ luồng nội bộ của riêng từng chức năng | Cao | VD: sơ đồ Đặt hàng → Duyệt đơn → Xuất kho → Giao hàng → Thanh toán → Đối soát, chỉ rõ chức năng nào bàn giao dữ liệu gì cho chức năng kế tiếp |
| S4 | Đã mô tả rõ dữ liệu đầu ra của chức năng này có phải là input bắt buộc của chức năng khác không, và 2 bên có thống nhất field/format/kiểu dữ liệu (data contract nội bộ) hay không | Cao | VD: chức năng Đặt hàng trả về orderId dạng String, chức năng Thanh toán nhận vào orderId — cần đối chiếu 2 bên có cùng định dạng/độ dài không |
| S5 | Đã mô tả rõ khi 1 chức năng xử lý lỗi/rollback giữa chừng, các chức năng liên quan đã chạy trước đó trong cùng quy trình có được rollback theo không (ranh giới transaction xuyên chức năng) | Cao | VD: chức năng Trừ kho chạy thành công nhưng chức năng Tạo đơn hàng thất bại ngay sau đó — kho có được hoàn lại tự động không hay phải xử lý thủ công |
| S6 | Đã xác định rõ những chức năng nào có thể xử lý song song (độc lập) và những chức năng nào bắt buộc tuần tự trong cùng một quy trình nghiệp vụ | Trung bình | VD: trong quy trình Duyệt đơn, chức năng Gửi email thông báo và chức năng Ghi audit log có thể chạy song song, nhưng chức năng Cập nhật trạng thái đơn phải hoàn tất trước cả hai |
| S7 | Đã mô tả rõ khả năng phụ thuộc vòng (circular dependency) giữa các chức năng nếu có, và cách hệ thống tránh vòng lặp vô hạn/deadlock | Trung bình | VD: chức năng A gọi chức năng B để validate, chức năng B lại cần dữ liệu do chức năng A tạo ra — cần làm rõ thứ tự khởi tạo dữ liệu ban đầu |
| S8 | Đã mô tả rõ khi một chức năng bị tắt/chưa được cấp phép (feature toggle, chưa mua gói) thì các chức năng phụ thuộc nó xử lý ra sao (ẩn đi, báo lỗi, hay fallback) | Trung bình | VD: nếu chức năng Khuyến mãi bị tắt ở gói Basic, chức năng Đặt hàng vẫn hoạt động bình thường nhưng ẩn hoàn toàn ô nhập mã giảm giá, không hiển thị lỗi |