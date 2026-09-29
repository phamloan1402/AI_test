# TC Excel Export — Ví dụ chi tiết & API Reference

> File này chứa ví dụ code chi tiết cho rule `manual_tc_excel_export.md`.
> Đọc rule trước, tham chiếu file này khi cần xem ví dụ cụ thể.

---

## 1. Import & API cơ bản

```python
from tc_excel_writer import section, subsection, tc, tc_group, tc_sub, tc_item, FeatureSpec, generate_excel
```

### Khai báo data cơ bản

```python
ROWS = [
    section("Giao diện (Phần này viết các trường hợp kiểm thử cho giao diên chung và các giao diện cho các control)"),
    subsection("Nhóm A — Giao diện chung"),   # Excel hiển thị: "Kiểm tra giao diện chung"
    tc(
        muc_dich   = "M1_001 - màn hình hiển thị mặc định",   # Excel: "Kiểm tra màn hình hiển thị mặc định"
        truong_hop = "Kiểm tra trạng thái mặc định khi vào màn hình",
        data       = "",
        buoc       = "1. Mở màn hình\n2. Quan sát giao diện",
        ket_qua    = "Giao diện hiển thị đúng thiết kế",
        priority   = "Cao",
    ),
]
```

---

## 2. Tạo FeatureSpec và generate

```python
feature = FeatureSpec(
    sheet_title  = "Tên chức năng",         # tab name trong Excel
    feature_name = "Tên chức năng",         # hiển thị trong cell C3
    feature_code = "MA_TC",                 # mã ngắn trong cell C4
    precondition = "Pre-condition:\n- ...", # dòng vàng row 18
    rows         = ROWS,
    kbnv_url     = "",                      # optional: link tài liệu
)

generate_excel([feature], "output/file.xlsx")
```

### Nhiều chức năng trong 1 file

```python
generate_excel([feature_A, feature_B, feature_C], "output/module.xlsx")
# → mỗi FeatureSpec thành 1 sheet riêng
# → sheet "Tổng hợp" tự động tạo ở đầu
```

---

## 3. Ví dụ 6 TC chuẩn Nhóm A — Giao diện chung (BẮT BUỘC)

```python
ROWS = [
    section("Giao diện (Phần này viết các trường hợp kiểm thử cho giao diên chung và các giao diện cho các control)"),
    subsection("Nhóm A — Giao diện chung"),
    tc(
        muc_dich   = "Xx_001 - màn hình ở trạng thái mặc định",
        truong_hop = "Màn hình hiển thị đúng theo SRS khi vào lần đầu",
        data       = "",
        buoc       = "1. Đăng nhập hệ thống\n2. Điều hướng đến màn hình cần kiểm thử\n3. Quan sát giao diện",
        ket_qua    = "- Title đúng theo SRS\n- Các field, button hiển thị đúng\n- Giá trị mặc định đúng thiết kế\n- Phân trang mặc định đúng",
        priority   = "Cao",
    ),
    tc(
        muc_dich   = "Xx_002 - dữ liệu các control ở trạng thái mặc định",
        truong_hop = "Tất cả control hiển thị đúng giá trị mặc định",
        data       = "",
        buoc       = "1. Mở màn hình\n2. Kiểm tra từng control",
        ket_qua    = "Trường đầu tiên được focus, giá trị mặc định đúng thiết kế, header/footer hiển thị",
        priority   = "Cao",
    ),
    tc(
        muc_dich   = "Xx_003 - tổng thể giao diện (bố cục, font, chính tả)",
        truong_hop = "Bố cục, font, chính tả, dấu * trường bắt buộc đúng",
        data       = "",
        buoc       = "1. Kiểm tra bố cục, font chữ, chính tả, màu chữ\n2. Kiểm tra trường bắt buộc có dấu *",
        ket_qua    = "1. Label/control không xô lệch, căn lề đồng nhất\n2. Font đồng nhất\n3. Trường required có dấu (*)\n4. Không lỗi chính tả",
        priority   = "Trung bình",
    ),
    tc(
        muc_dich   = "Xx_004 - tab order tiến khi nhấn phím Tab",
        truong_hop = "Con trỏ di chuyển đúng thứ tự trái→phải, trên→dưới",
        data       = "",
        buoc       = "1. Mở màn hình\n2. Nhấn Tab từ trường đầu tiên liên tục",
        ket_qua    = "Con trỏ di chuyển lần lượt trên các trường input, button, hyperlink theo thứ tự trái→phải, trên→dưới",
        priority   = "Thấp",
    ),
    tc(
        muc_dich   = "Xx_005 - tab order lùi khi nhấn Shift+Tab",
        truong_hop = "Con trỏ di chuyển ngược chiều",
        data       = "",
        buoc       = "1. Mở màn hình\n2. Nhấn Shift+Tab từ trường cuối",
        ket_qua    = "Con trỏ di chuyển ngược: dưới→trên, phải→trái",
        priority   = "Thấp",
    ),
    tc(
        muc_dich   = "Xx_006 - responsive khi thu nhỏ/phóng to màn hình",
        truong_hop = "Layout không vỡ ở các mức zoom",
        data       = "",
        buoc       = "1. Nhấn Ctrl+− để thu nhỏ\n2. Nhấn Ctrl+= để phóng to\n3. Quan sát layout",
        ket_qua    = "Màn hình thu nhỏ/phóng to không bị vỡ giao diện",
        priority   = "Trung bình",
    ),
    # Sau Nhóm A: subsection cho từng control (Textbox, Dropdown, v.v.)
]
```

---

## 4. Ví dụ tc_group() cho Nhóm D TEXT field

Cấu trúc phân cấp 3 cấp tạo merge cells trong Excel:
- **Cấp 1 (cột B):** Nhóm lớn — merge dọc. VD: "Kiểm tra khi nhập giá trị"
- **Cấp 2 (cột C):** Nhóm con — merge dọc. VD: "Kiểm tra khi nhập khoảng trắng"
- **Cấp 3 (cột D):** Chi tiết — mỗi variation 1 hàng

```python
subsection("Nhóm D — Textbox Mã (max 100, A-Z 0-9 _ .)"),

# === Nhập keyboard ===
tc_group("Kiểm tra khi nhập giá trị", [
    tc_sub("Kiểm tra khi nhập khoảng trắng", [
        tc_item("nhập toàn khoảng trắng",
                "1. Nhập '     ' (5 spaces) vào Mã\n2. Click Lưu",
                "Hệ thống báo lỗi: coi như rỗng → BUS-70",
                "Cao"),
        tc_item("nhập khoảng trắng ở đầu cuối ký tự",
                "1. Nhập ' QUAN_LY ' vào Mã\n2. Click ra ngoài (blur)",
                "Hệ thống chặn ký tự space hoặc tự xóa space",
                "Cao"),
        tc_item("nhập khoảng trắng ở giữa ký tự",
                "1. Nhập 'QUAN LY' vào Mã",
                "Hệ thống chặn tại input, không cho nhập space",
                "Cao"),
        tc_item("nhập nhiều khoảng trắng ở giữa các ký tự",
                "1. Nhập 'QUAN   LY' vào Mã",
                "Hệ thống chặn tại input",
                "Trung bình"),
    ]),
    tc_sub("Kiểm tra nhập maxlength", [
        tc_item("Nhập <= 100 ký tự",
                "1. Nhập 99 ký tự 'A' vào Mã",
                "Hệ thống chấp nhận",
                "Cao"),
        tc_item("Nhập > 100 ký tự",
                "1. Nhập 101 ký tự 'A' vào Mã",
                "Hệ thống tự động chặn khi nhập quá maxlength",
                "Cao"),
    ]),
    tc_sub("Kiểm tra nhập ký tự số", [
        tc_item("", "1. Nhập '12345' vào Mã", "Hệ thống chấp nhận", "Cao"),
    ]),
    tc_sub("Kiểm tra nhập ký tự đặc biệt", [
        tc_item('Là dấu gạch ngang "-" và dấu dạch dưới "_"',
                "1. Nhập 'ABC_DEF-123' vào Mã",
                "Hệ thống chấp nhận", "Cao"),
        tc_item('khác dấu gạch ngang "-" và dấu dạch dưới "_"',
                "1. Nhập '!@#$%' vào Mã",
                "Hệ thống chặn tại input", "Cao"),
    ]),
    tc_sub("Kiểm tra khi nhập kí tự chữ in hoa", [
        tc_item("", "1. Nhập 'QUANLY'", "Thành công", "Cao"),
    ]),
    tc_sub("Kiểm tra khi nhập kí tự chữ in thường", [
        tc_item("", "1. Nhập 'quanly'", "Chặn hoặc tự convert hoa", "Cao"),
    ]),
    tc_sub("Kiểm tra nhập ký tự chữ có dấu, tiếng Việt", [
        tc_item("", "1. Nhập 'Quản Lý'", "Chặn ký tự tiếng Việt", "Cao"),
    ]),
]),

# === Copy-paste (cấu trúc tương tự) ===
tc_group("Kiểm tra khi copy/paste giá trị", [
    tc_sub("Kiểm tra khi copy/paste khoảng trắng", [
        tc_item("Copy/paste toàn khoảng trắng", "1. Copy spaces\n2. Ctrl+V", "Chặn", "Cao"),
        # ... tương tự ...
    ]),
    tc_sub("Kiểm tra copy/paste maxlength", [
        tc_item("Copy/paste <= 100 ký tự", "1. Copy 99 chars\n2. Ctrl+V", "OK", "Cao"),
        tc_item("Copy/paste > 100 ký tự", "1. Copy 101 chars\n2. Ctrl+V", "Truncate còn 100", "Cao"),
    ]),
    # ... tương tự nhập keyboard ...
]),
```

---

## 5. Ví dụ Section "Chức năng" (BIZ)

```python
ROWS = [
    section("Chức năng (Phần này viết các trường hợp kiểm thử kiểm tra các ràng buộc trong cơ sở dữ liệu và cho các luồng nghiệp vụ trong tài liệu giải pháp, tích hợp với các chức năng khác)"),
    subsection("Kiểm tra thêm mới thành công"),
    tc(
        muc_dich   = "M2_001 - thêm bản ghi hợp lệ với đủ trường bắt buộc",
        truong_hop = "Điền đầy đủ dữ liệu hợp lệ → lưu thành công",
        data       = "Mã: 'NEW_001'; Tên: 'TEST'",
        buoc       = "1. Nhập dữ liệu\n2. Click Thêm mới",
        ket_qua    = "BUS-42: Thêm mới thành công. Bản ghi xuất hiện trong danh sách",
        priority   = "Cao",
    ),
    subsection("Kiểm tra thêm mới không thành công"),
    tc(
        muc_dich   = "M2_010 - bỏ trống trường bắt buộc → BUS-70",
        truong_hop = "Submit thiếu trường Mã → lỗi validation",
        data       = "Mã: (rỗng)",
        buoc       = "1. Bỏ trống Mã\n2. Click Thêm mới",
        ket_qua    = "BUS-70 hiển thị tại trường Mã. Không lưu",
        priority   = "Cao",
    ),
    subsection("Kiểm tra phân quyền"),
    tc(
        muc_dich   = "M2_020 - không có quyền thêm mới → nút ẩn",
        truong_hop = "User không có quyền Thêm mới → không thấy nút",
        data       = "User chỉ có quyền Xem chi tiết",
        buoc       = "1. Đăng nhập tài khoản không có quyền\n2. Quan sát màn hình",
        ket_qua    = "Nút Thêm mới ẩn hoàn toàn",
        priority   = "Cao",
    ),
]
```

---

## 6. Ví dụ Subsection "Kiểm tra button"

Mỗi button action **phải có đúng 3 TC**, theo thứ tự:
> ⚠️ **LƯU Ý CỘT TRƯỜNG HỢP KIỂM THỬ:** BẮT BUỘC bắt đầu bằng `"Kiểm tra "`, không để tiền tố mã `M01 — `, `M02 — `, `M03 — ` (VD: `"Kiểm tra hiển thị nút Gửi yêu cầu"`).

```python
subsection("Kiểm tra button <Tên Button>"),
tc(
    muc_dich   = "hiển thị button trên giao diện",
    truong_hop = "Kiểm tra hiển thị nút <tên button>",
    data       = "",
    buoc       = "1. Mở màn hình\n2. Quan sát nút <tên button>",
    ket_qua    = "Nút hiển thị giống như trong SRS, icon và nhãn chữ đúng chính tả.",
    priority   = "Cao",
),
tc(
    muc_dich   = "trạng thái kích hoạt của button",
    truong_hop = "Kiểm tra trạng thái enable/disable của nút <tên button>",
    data       = "",
    buoc       = "1. Mở màn hình\n2. Quan sát trạng thái nút <tên button>",
    ket_qua    = "Trạng thái: Enable (hoặc Disable theo điều kiện form)",
    priority   = "Cao",
),
tc(
    muc_dich   = "thao tác click button",
    truong_hop = "Kiểm tra click nút <tên button>",
    data       = "<điền dữ liệu hợp lệ đầy đủ theo SRS>",
    buoc       = "1. Điền dữ liệu hợp lệ\n2. Click nút <tên button>",
    ket_qua    = 'Onclick hệ thống thực hiện validate dữ liệu. Hệ thống lưu thông tin với trạng thái "<theo SRS>", chuyển về màn hình Danh sách.',
    priority   = "Cao",
),
```

> `<tên button>`, `<theo SRS>` là placeholder — thay bằng giá trị thực tế.

### Ví dụ Hộp thoại xác nhận (Confirmation Popup / Dialog CONF_*)

```python
# Button trên Hộp thoại xác nhận (Đồng ý + Huỷ bỏ + Icon X)
subsection("Kiểm tra button Đồng ý trên Hộp thoại xác nhận CONF_001"),
tc(
    muc_dich   = "căn lề, chính tả label button",
    truong_hop = "Kiểm tra hiển thị nút Đồng ý trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Quan sát nút Đồng ý",
    ket_qua    = "Nút Đồng ý hiển thị rõ ràng, màu sắc nổi bật, nhãn chữ đúng chính tả theo thiết kế Ant Design.",
    priority   = "Thấp",
),
tc(
    muc_dich   = "trạng thái mặc định button",
    truong_hop = "Kiểm tra trạng thái enable/disable của nút Đồng ý trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Quan sát trạng thái nút Đồng ý",
    ket_qua    = "Nút Đồng ý ở trạng thái enable, sẵn sàng nhận tương tác click.",
    priority   = "Trung bình",
),
tc(
    muc_dich   = "thao tác click button",
    truong_hop = "Kiểm tra click nút Đồng ý trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Click nút Đồng ý",
    ket_qua    = "Hệ thống xác nhận hành động: Đóng popup CONF_001, đóng form Tạo yêu cầu, hủy bỏ toàn bộ dữ liệu đang nhập dở và điều hướng về màn hình danh sách.",
    priority   = "Cao",
),
subsection("Kiểm tra button Huỷ bỏ trên Hộp thoại xác nhận CONF_001"),
tc(
    muc_dich   = "căn lề, chính tả label button",
    truong_hop = "Kiểm tra hiển thị nút Huỷ bỏ trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Quan sát nút Huỷ bỏ",
    ket_qua    = "Nút Huỷ bỏ hiển thị rõ ràng, nhãn chữ đúng chính tả theo thiết kế Ant Design.",
    priority   = "Thấp",
),
tc(
    muc_dich   = "trạng thái mặc định button",
    truong_hop = "Kiểm tra trạng thái enable/disable của nút Huỷ bỏ trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Quan sát trạng thái nút Huỷ bỏ",
    ket_qua    = "Nút Huỷ bỏ ở trạng thái enable, sẵn sàng nhận tương tác click.",
    priority   = "Trung bình",
),
tc(
    muc_dich   = "thao tác click button",
    truong_hop = "Kiểm tra click nút Huỷ bỏ trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Click nút Huỷ bỏ",
    ket_qua    = "Hệ thống hủy bỏ thao tác: Đóng popup CONF_001, giữ nguyên màn hình Tạo yêu cầu và bảo toàn 100% dữ liệu đang nhập dở.",
    priority   = "Cao",
),
subsection("Kiểm tra icon đóng (X) trên Hộp thoại xác nhận CONF_001"),
tc(
    muc_dich   = "căn lề, vị trí icon đóng popup",
    truong_hop = "Kiểm tra hiển thị icon đóng (X) trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Quan sát góc trên bên phải popup",
    ket_qua    = "Icon 'X' hiển thị rõ nét ở góc trên bên phải của modal dialog theo đúng chuẩn Ant Design Modal.",
    priority   = "Thấp",
),
tc(
    muc_dich   = "thao tác click icon đóng popup",
    truong_hop = "Kiểm tra click icon đóng (X) trên Hộp thoại xác nhận CONF_001",
    data       = "",
    buoc       = "1. Mở popup xác nhận CONF_001\n2. Click icon 'X' ở góc trên bên phải popup",
    ket_qua    = "Đóng popup xác nhận CONF_001, giữ nguyên màn hình Tạo yêu cầu và bảo toàn 100% dữ liệu đang nhập dở.",
    priority   = "Trung bình",
),
```
