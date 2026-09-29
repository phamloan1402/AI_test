# Phân tích sâu Q&A — Senior Test Architect / QA Lead

Kết hợp cách phân tích SRS của analyzer với trọng tâm thiết kế test của FULL RBT. Mục tiêu là tìm điểm mờ, logic chưa hợp lý và mâu thuẫn có tác động thực tế đến Pass/Fail. Không đặt chỉ tiêu số câu hỏi; không sinh testcase chi tiết ở bước này.

## 1. Rà từng requirement và lập bản đồ nghiệp vụ

Đọc toàn bộ nguồn trong scope, kể cả bảng, ghi chú, thông báo và ngoại lệ. Tách câu ghép thành các rule nguyên tử, giữ ID/vị trí nguồn; không tự đặt ID rồi trình bày như ID gốc.

Với mỗi rule, xác định: actor và phạm vi dữ liệu, điều kiện trước, trigger, input/constraint, xử lý, trạng thái/dữ liệu sau, kết quả quan sát được, nhánh lỗi. Đối chiếu Given/When/Then và checklist A–S cùng `Ambiguity.md`. Ghi điểm chưa rõ sau khi tìm câu trả lời ở các phần khác và phản hồi BA đã có.

Dựng Happy/Alternate/Exception Paths đến kết quả cuối cùng. Theo dấu dữ liệu từ tạo → sửa → gửi/duyệt → sử dụng → hủy/xóa khi có các bước đó. Với rule tính toán, xác định đơn vị, nguồn dữ liệu, thời điểm chốt, rounding và giá trị null/0/âm nếu liên quan.

## 2. Dựng mô hình để phát hiện khoảng trống logic

Chọn mô hình theo nghiệp vụ, không ép mọi feature có đủ mọi loại bảng:

| Mô hình | Nội dung cần đối chiếu | Dấu hiệu cần điều tra |
|---|---|---|
| Decision table | Điều kiện, tổ hợp hợp lệ, thứ tự ưu tiên, output | Hai rule cùng đúng nhưng trả kết quả khác; không rule nào xử lý; điều kiện không thể đạt |
| State transition | Trạng thái đầu, action, actor, guard, trạng thái cuối, side effect | Không có đường tới/thoát trạng thái; được sửa sau khi khóa; hủy nhưng dữ liệu vẫn được dùng |
| Role × action × state | Quyền thao tác, phạm vi bản ghi, trạng thái, UI và xử lý phía hệ thống | Flow cho phép nhưng RBAC cấm; nút ẩn nhưng quyền thực thi chưa rõ; vượt phạm vi dữ liệu |
| Field/data dependency | Required, editable, default, nguồn option, field cha/con, uniqueness | Field bắt buộc nhưng bị khóa rỗng; đổi cha vẫn giữ con không hợp lệ; create/edit/import có rule khác nhau chưa giải thích |

Lưu bảng gọn có nguồn và liên kết Q-ID trong artifact. Phân biệt điều kiện không thể đạt do thiết kế có chủ đích với điều kiện khiến luồng nghiệp vụ bắt buộc không thể hoàn tất.

## 3. Đối chiếu giữa các phần và module

Đối chiếu các cặp có liên quan: mô tả flow ↔ business rule; rule ↔ validation/message; permission matrix ↔ action; state ↔ button; field definition ↔ wireframe; UI ↔ API contract nếu có; tìm kiếm ↔ export; thao tác đơn ↔ hàng loạt; dữ liệu nguồn ↔ báo cáo; module tạo dữ liệu ↔ module tiêu thụ dữ liệu.

- Mâu thuẫn: dẫn **cả hai vị trí**, xác nhận cùng actor, trạng thái, phạm vi và phiên bản trước khi kết luận. Nếu khác phiên bản chưa xác định bản hiệu lực, hỏi bản nào áp dụng.
- Thiếu rule: ghi nơi phát sinh hành vi và phạm vi đã kiểm tra mà chưa có xử lý. Nguồn chưa đủ thì ghi `Cần kiểm tra thêm`.
- Logic chưa hợp lý: chỉ ra hệ quả trái mục tiêu hoặc invariant nghiệp vụ được nguồn xác lập; nếu invariant do QA đề xuất thì ghi rõ cần BA xác nhận.

## 4. Phản biện bằng tình huống cụ thể

Thử tình huống đủ nhỏ để chứng minh vấn đề, dựa trên capability thực tế:

- Biên min/max, đúng bằng ngưỡng, khoảng giao nhau hoặc khoảng hở, null/0, ngày hiệu lực và thời điểm chuyển ngày.
- Hai role/hai người cùng thao tác; quyền, trạng thái hoặc dữ liệu đổi sau khi mở màn hình nhưng trước khi lưu/duyệt.
- Bấm lặp, retry sau timeout, phản hồi đến trễ; không xác định đã lưu hay chưa; tác động trùng lặp khi chạy lại.
- Lỗi giữa nhiều bước, thành công một phần, hủy hoặc khôi phục; trạng thái, dữ liệu và thông báo có nhất quán không?
- Dữ liệu tham chiếu bị khóa/xóa/đổi hiệu lực; nguồn dữ liệu thay đổi nhưng báo cáo hoặc module sau vẫn dùng bản cũ.

Mẫu chứng minh: `Nguồn → điều kiện/dữ liệu → thao tác → rule cùng áp dụng → hai kết quả hoặc kết quả không thể đạt → tác động kiểm thử → quyết định cần BA chốt`.
Ví dụ giả lập: quyền cho phép người lập sửa bản nháp; flow lại chỉ cho lưu khi đã gửi duyệt và cấm sửa sau khi gửi. Cần làm rõ thời điểm được lưu; không tự đề xuất bỏ kiểm soát duyệt.

## 5. Rà trọng tâm FULL RBT theo capability

Đánh dấu từng chủ đề là đã rõ, có Q-ID, N/A hoặc cần nguồn bổ sung. Không hỏi lại nội dung đã có đáp án.

| Capability | Trọng tâm câu hỏi |
|---|---|
| Search nhiều trường | Liệt kê từng field; AND/OR, ưu tiên điều kiện, normalization, tìm một trường và tổ hợp nhiều trường; khi reset/rỗng; trường hợp điều kiện xung đột |
| Filter, kể cả trang read-only/chi tiết | Dropdown/multiselect/searchable, nguồn option, phụ thuộc field, giá trị hết hiệu lực, giữ/reset filter |
| Form và button | Create/edit: field được sửa/bị khóa, required/maxlength/format, validation onBlur/onSubmit, giữ dữ liệu khi lỗi, Lưu/Hủy/Trình duyệt |
| State và permission | Button hiển thị/ẩn/disabled theo từng role và state; quyền xử lý và phạm vi dữ liệu; mâu thuẫn permission ↔ flow |
| Nhiều danh sách/tab | Pagination, page size, sorting, filter độc lập hay dùng chung; dữ liệu/thao tác trên trang hiện tại hay toàn bộ tập kết quả |
| Export/import, batch | Tên/format file, phạm vi và giới hạn; N=1/N>1; tập hỗn hợp hợp lệ/không hợp lệ; thành công một phần, thông báo và retry |
| Concurrency và dependency | Ghi đè/xung đột, timeout, mất kết nối, phản hồi muộn, dữ liệu thay đổi; outcome cần bảo đảm, không ép chọn kỹ thuật locking |
| NFR, audit, security | Chỉ áp dụng khi liên quan: tiêu chí đo, điều kiện tải, truy vết thay đổi, bảo vệ dữ liệu và trách nhiệm chốt yêu cầu |

## 6. Chốt finding và tự rà độ bao phủ

- Một finding tương ứng một quyết định nghiệp vụ có thể chốt riêng; gộp biểu hiện cùng nguyên nhân, giữ liên kết mọi nguồn bị ảnh hưởng.
- Câu hỏi nêu tình huống và yêu cầu chọn kết quả mong đợi; assumption chỉ khi ít rủi ro, nếu không dùng Options hoặc để BA quyết định.
- Sắp ưu tiên theo ảnh hưởng: rule cốt lõi, quyền, state và tính toàn vẹn dữ liệu trước chi tiết trình bày; severity theo tác động, không theo chủ đề cố định.
- Mỗi flow/rule áp dụng đã được rà cả nhánh thành công và nhánh lỗi liên quan; mỗi điểm chưa rõ có Q-ID hoặc lý do cần nguồn. Không chỉ rà field đầu tiên hay Happy Path.
- Kiểm tra lại finding với toàn bộ nguồn và câu trả lời đã chốt; loại câu hỏi đã có đáp án, trùng lặp hoặc nằm ngoài scope.
- Sau phản hồi BA, rà tác động quyết định lên rule/flow liên quan, đóng/mở lại finding khi có căn cứ và tính lại verdict. Không coi im lặng là đồng ý assumption.
