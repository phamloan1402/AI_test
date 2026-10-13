# -*- coding: utf-8 -*-
"""
gen_tc_hosophaplycic.py
=======================
Generate Excel test cases — [FUNC-XLDL-009] XLDL hồ sơ pháp lý (CIC project), FULL RBT / COMPACT mode.

Sheets: M1 Danh sách | M2 Xem chi tiết D10/D11 | M3 Xem chi tiết Q11 | M4 Xử lý D10/D11 |
        M5 Xử lý Q11 | M7 Xử lý đồng thời (D10/D11 + Q11) | M8 Nghiệp vụ tự động & tích hợp
Popups MH-006 / MH-007 are generated inside every sheet that opens them ([CHECK 10]).

Sources: Confluence 1212957 and child pages; Q&A practices/Q&A/HoSoPhapLyCIC_QA.md;
traceability practices/testcases/CIC/HoSoPhapLyCIC_B3_B4.md.

Run:
    cd <repo root>
    python scripts/gen_tc_hosophaplycic.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tc_excel_writer import section, subsection, tc, tc_group, tc_sub, tc_item, FeatureSpec, generate_excel

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "practices", "testcases", "CIC", "HoSoPhapLyCIC_TestCases.xlsx")

UI_SECTION = ("Giao diện (Phần này viết các trường hợp kiểm thử cho giao diện chung "
              "và các giao diện cho các control)")
BIZ_SECTION = ("Chức năng (Phần này viết các trường hợp kiểm thử kiểm tra các ràng buộc trong cơ sở dữ liệu "
               "và cho các luồng nghiệp vụ trong tài liệu giải pháp, tích hợp với các chức năng khác)")

CAO, TB, THAP = "Cao", "Trung bình", "Thấp"

MENU_PATH = "Thu thập và xử lý dữ liệu > Xử lý dữ liệu > Hồ sơ pháp lý"

# Test accounts (no credentials stored here — taken from the test environment).
ACC_MAIN = "cbxl01 (ROLE-CBTTXLDL, phân quyền TCTD 31358001 và 79202501)"
ACC_PEER = "cbxl02 (ROLE-CBTTXLDL, phân quyền TCTD 31358001)"
ACC_NO_TCTD = "cbxl03 (ROLE-CBTTXLDL, chưa được phân quyền TCTD nào)"
ACC_NO_ROLE = "nsd01 (không có quyền chức năng Hồ sơ pháp lý)"
DM_IN = "31358001"        # đầu mối được phân quyền
DM_IN2 = "79202501"       # đầu mối được phân quyền thứ hai
DM_OUT = "01201001"       # đầu mối gửi báo cáo, KHÔNG được phân quyền cho cbxl01

PRECOND_BASE = (
    "Pre-condition:\n"
    f"- Đăng nhập tài khoản {ACC_MAIN}\n"
    f"- Menu: {MENU_PATH}\n"
    "- Kho tiền dữ liệu có hồ sơ pháp lý hợp lệ tệp D10, D11, Q11 của cả KH Cá nhân và Tổ chức, "
    "ở đủ 4 trạng thái Chờ cấp mã / Chờ xem xét / Đã xử lý / Từ chối\n"
)


def steps(*lines):
    """Join step lines into a numbered block."""
    return "\n".join(f"{i}. {line}" for i, line in enumerate(lines, 1))


def sql(where, order="NGAY_CAP_NHAT DESC"):
    """Sample reconciliation SQL; table/column names are placeholders (fixed at DB design)."""
    return (f"\nSQL đối soát (mẫu):\nSELECT * FROM <HO_SO_PHAP_LY> WHERE LOAI_DU_LIEU = 'Pháp lý' "
            f"AND TRANG_THAI_DU_LIEU = 'Hợp lệ' AND MA_TEP IN ('D10','D11','Q11') AND {where} ORDER BY {order};")


# ══════════════════════════════════════════════════════════════════════════════
# Common-group builders
# ══════════════════════════════════════════════════════════════════════════════

def group_a(screen, open_steps, display, tab_order, enter_result, qt_extra=True):
    """Nhóm A — A01–A06 (+ A07/A08 QT component)."""
    rows = [
        subsection("Nhóm A — Giao diện chung"),
        tc("hiển thị màn hình mặc định", f"Hiển thị {screen} khi mở", "",
           steps(*open_steps, f"Quan sát {screen}"), display, CAO),
        tc("tổng thể giao diện màn hình", "Bố cục, font chữ, căn lề, dấu (*), chính tả", "",
           steps(*open_steps, "Quan sát toàn bộ label, control, button"),
           "1. Label, control có kích thước, khoảng cách đồng đều, không xô lệch\n"
           "2. Cùng một font, cỡ chữ; label căn trái\n3. Trường bắt buộc có dấu (*)\n"
           "4. Không có lỗi chính tả, ngữ pháp", TB),
        tc("thứ tự di chuyển con trỏ khi nhấn phím Tab", "Nhấn Tab liên tục từ control đầu tiên", "",
           steps(*open_steps, "Nhấn phím Tab liên tục"), f"Con trỏ di chuyển lần lượt: {tab_order}", TB),
        tc("thứ tự di chuyển con trỏ khi nhấn phím Shift+Tab", "Nhấn Shift+Tab liên tục từ control cuối cùng", "",
           steps(*open_steps, "Focus control cuối cùng", "Nhấn Shift+Tab liên tục"),
           "Con trỏ di chuyển theo thứ tự ngược lại với phím Tab (từ dưới lên trên, từ phải sang trái)", TB),
        tc("phím Enter", "Nhấn Enter khi đang focus control", "",
           steps(*open_steps, "Focus control", "Nhấn phím Enter"), enter_result, TB),
        tc("tính năng responsive màn hình", "Thay đổi mức zoom bằng Ctrl+− / Ctrl+=", "Zoom 75%, 100%, 125%, 150%",
           steps(*open_steps, "Nhấn Ctrl+− / Ctrl+= để đổi mức zoom"),
           "Layout hiển thị hài hòa, không tràn khung, không vỡ giao diện ở mọi mức zoom", THAP),
    ]
    if qt_extra:
        rows += [
            tc("ngôn ngữ tiếng Việt chuẩn hành chính", "Rà toàn bộ nhãn, từ viết tắt trên màn hình",
               "Từ viết tắt: KH, TCTD, TTQT, QHTD, CIC, C06", steps(*open_steps, "Rà các nhãn, giá trị có từ viết tắt"),
               "Không có từ viết tắt không được định nghĩa; từ viết tắt có tooltip giải thích (Quy tắc component)", THAP),
        ]
    return rows


def button(name, ctx, show, state, click, prio=CAO):
    """3 standard TCs for one action button."""
    return [
        subsection(f"Kiểm tra button {name}"),
        tc("hiển thị button", f"Kiểm tra hiển thị nút {name}", "", steps(ctx, f"Quan sát nút {name}"), show, TB),
        tc("trạng thái button", f"Kiểm tra trạng thái enable/disable của nút {name}", "",
           steps(ctx, f"Quan sát trạng thái nút {name} theo từng điều kiện"), state, TB),
        tc("thao tác click button", f"Kiểm tra click nút {name}", "", steps(ctx, f"Click nút {name}"), click, prio),
    ]


def screen_buttons(ctx, buttons_text, primary):
    """M01–M05 screen-level button checks."""
    return [
        subsection("Kiểm tra button chung trên màn hình"),
        tc("căn lề, chính tả label button", "Kiểm tra căn lề, chính tả label các button", "",
           steps(ctx, f"Quan sát các button: {buttons_text}"),
           "Text căn giữa, chữ thường và chữ cái đầu in hoa, không lỗi chính tả", THAP),
        tc("trạng thái enabled/disabled của các button theo điều kiện", "Kiểm tra trạng thái các button", "",
           steps(ctx, "Quan sát trạng thái các button"),
           f"Hiển thị đúng trạng thái theo điều kiện SRS; chỉ có duy nhất 1 Primary button ({primary}) trong một khu vực", TB),
        tc("click button thực hiện đúng chức năng", "Kiểm tra click các button", "",
           steps(ctx, "Click lần lượt từng button"), "Mỗi button thực hiện đúng chức năng mô tả trong SRS", CAO),
        tc("loading và disable button khi đang xử lý", "Kiểm tra button khi hệ thống đang xử lý",
           "Giả lập mạng chậm (DevTools: Slow 3G)", steps(ctx, "Click button gọi API", "Click tiếp nhiều lần khi đang xử lý"),
           "Button hiển thị loading spinner và bị disable; thao tác chỉ được thực hiện 1 lần", CAO),
        tc("giữ bộ lọc sau khi F5 hoặc chuyển trang", "Kiểm tra giữ tùy chọn bộ lọc và cấu hình hiển thị", "",
           steps(ctx, "Chọn điều kiện, Tìm kiếm", "Nhấn F5 hoặc chuyển sang chức năng khác rồi quay lại"),
           "Hệ thống giữ tùy chọn bộ lọc và cấu hình hiển thị đã chọn trước đó (không lưu giá trị) — Quy tắc component", TB),
    ]


def api_group():
    """H13–H16 API states."""
    return tc_group("Kiểm tra options hiển thị đúng", [
        tc_sub("Trường hợp call API thành công", [
            tc_item("Dữ liệu trả về khác rỗng", steps("Click mở danh sách"),
                    "Danh sách hiển thị đầy đủ options đúng theo dữ liệu API trả về", TB),
            tc_item("Dữ liệu trả về là rỗng", steps("Giả lập API trả về danh sách rỗng", "Click mở danh sách"),
                    "Danh sách hiển thị trạng thái rỗng \"Không có dữ liệu\" kèm icon", TB),
        ]),
        tc_sub("Trường hợp call API bị thất bại", [
            tc_item("API trả lỗi 500 / mất kết nối", steps("Giả lập API lỗi", "Click mở danh sách"),
                    "Hiển thị thông báo lỗi hoặc trạng thái rỗng; giao diện không bị treo/crash", TB),
        ]),
        tc_sub("Trường hợp call API bị time out", [
            tc_item("API phản hồi quá thời gian chờ", steps("Giả lập API time out", "Click mở danh sách"),
                    "Hiển thị loading trong thời gian chờ; sau time out hiển thị thông báo lỗi hoặc trạng thái rỗng; UI không treo", TB),
        ]),
    ])


def search_group(name, ctx, hit_partial, hit_exact, exact_only=False):
    """D22–D28 — search box inside a dropdown / combobox popup."""
    partial_res = ("Chỉ hiển thị option khớp chính xác toàn bộ giá trị đã gõ (BR-015); gõ một phần không hiển thị option"
                   if exact_only else f"Hiển thị các option chứa chuỗi '{hit_partial}' (tìm gần đúng)")
    return tc_group("Kiểm tra nhập tìm kiếm", [
        tc_sub("Tìm kiếm gần đúng / chính xác", [
            tc_item(f"Gõ một phần: '{hit_partial}'", steps(ctx, f"Click {name}", f"Gõ '{hit_partial}'", "Dừng gõ 300ms"),
                    partial_res, CAO),
            tc_item(f"Gõ đầy đủ: '{hit_exact}'", steps(ctx, f"Click {name}", f"Gõ '{hit_exact}'"),
                    f"Hiển thị đúng option '{hit_exact}'", CAO),
        ]),
        tc_sub("Không phân biệt hoa thường, có dấu / không dấu", [
            tc_item("Gõ chữ hoa / chữ thường, có dấu / không dấu", steps(ctx, f"Click {name}", "Gõ chuỗi đổi hoa thường, bỏ dấu"),
                    "Kết quả tìm kiếm giống khi gõ đúng hoa thường, có dấu (Quy tắc component — tìm like, không phân biệt hoa thường, có dấu/không dấu)", TB),
        ]),
        tc_sub("Không có kết quả", [
            tc_item("Gõ 'KHONG_TON_TAI_999'", steps(ctx, f"Click {name}", "Gõ 'KHONG_TON_TAI_999'"),
                    "Hiển thị \"Không tìm thấy dữ liệu\" thay vì danh sách trống", TB),
        ]),
        tc_sub("Khoảng trắng và ký tự đặc biệt", [
            tc_item(f"Gõ '  {hit_exact}  ' (khoảng trắng đầu cuối)", steps(ctx, f"Click {name}", "Gõ chuỗi có khoảng trắng đầu cuối"),
                    "Hệ thống trim khoảng trắng đầu cuối, kết quả như khi gõ không có khoảng trắng", TB),
            tc_item("Gõ '<script>alert(1)</script>'", steps(ctx, f"Click {name}", "Gõ chuỗi script"),
                    "Không thực thi script; hiển thị \"Không tìm thấy dữ liệu\"", CAO),
            tc_item("Gõ \"' OR '1'='1\"", steps(ctx, f"Click {name}", "Gõ chuỗi SQL injection"),
                    "Không lỗi hệ thống, không trả về toàn bộ dữ liệu; hiển thị \"Không tìm thấy dữ liệu\"", CAO),
        ]),
    ])


def scroll_group(control, ctx, n_opts=None):
    """H07–H09 / J11–J13 — always 3 cases (GAP-02); fixed lists need simulated catalogue data."""
    if n_opts is None:
        lt, eq, gt = "Dữ liệu nguồn có 3 option", "Dữ liệu nguồn có 5 option", "Dữ liệu nguồn có > 10 option"
    else:
        sim = f"Danh sách theo SRS cố định {n_opts} giá trị — giả lập danh mục trên môi trường test"
        lt, eq, gt = f"Danh sách thực tế {n_opts} option", f"{sim} có 5 option", f"{sim} có > 10 option"
    return tc_group("Kiểm tra hiển thị scroll", [
        tc_sub("Số option < 5", [tc_item(lt, steps(ctx, f"Mở {control}"), "Không hiển thị thanh scroll", THAP)]),
        tc_sub("Số option = 5", [tc_item(eq, steps(ctx, f"Mở {control}"), "Không hiển thị thanh scroll", THAP)]),
        tc_sub("Số option > 5", [tc_item(gt, steps(ctx, f"Mở {control}", "Cuộn danh sách"),
                                         "Hiển thị thanh scroll; mặc định hiển thị 10 item, phần còn lại tải khi cuộn hoặc tìm kiếm (virtual scroll — Quy tắc component)", THAP)]),
    ])


def dropdown(name, ctx, default, placeholder, required, options, n_opts=None, searchable=False,
             locked_required=False, search_hits=("", "")):
    """Nhóm H — single-select dropdown / combobox."""
    rows = [
        subsection(f"Kiểm tra Dropdown {name}"),
        tc("hiển thị", f"Hiển thị Dropdown {name}", "", steps(ctx, f"Quan sát Dropdown {name}"),
           "Dropdown hiển thị đúng vị trí, kích thước theo thiết kế, có icon mũi tên; click toàn bộ vùng control đều mở danh sách", TB),
        tc("giá trị mặc định", "Giá trị mặc định khi mở màn hình", "", steps(ctx, f"Quan sát giá trị Dropdown {name}"), default, CAO),
        tc("placeholder", "Placeholder khi chưa có giá trị", "", steps(ctx, f"Quan sát placeholder Dropdown {name}"), placeholder, THAP),
        tc("trường bắt buộc", "Tính bắt buộc của trường", "", steps(ctx, f"Quan sát nhãn / dấu (*) của {name}"), required, CAO),
        tc("options hiển thị đúng", "Danh sách option", "", steps(ctx, f"Click mở Dropdown {name}"), options, CAO),
        tc("sử dụng bàn phím", "Thao tác hoàn toàn bằng bàn phím", "",
           steps(f"{ctx}, nhấn Tab/Shift+Tab focus vào Dropdown {name}", "Nhấn phím Enter",
                 "Nhấn phím Up/Down", "Nhấn phím Enter khi đang focus một giá trị", "Nhấn Tab/Shift+Tab"),
           "1. Dropdown được focus\n2. Danh sách lựa chọn hiển thị\n3. Con trỏ di chuyển theo danh sách lựa chọn\n"
           "4. Giá trị được chọn và hiển thị lên dropdown\n5. Con trỏ di chuyển đến control tiếp theo / trước đó", TB),
    ]
    rows.append(scroll_group(f"Dropdown {name}", ctx, n_opts))
    unselect = ("Không cho bỏ chọn về rỗng: dropdown luôn giữ một giá trị (trường bắt buộc chọn đúng một giá trị — BR-013)"
                if locked_required else "Bỏ chọn được giá trị đã chọn; dropdown trở về placeholder")
    rows.append(tc_group("Kiểm tra chọn giá trị", [
        tc_sub("Chọn 1 giá trị", [tc_item("Chọn một option bất kỳ", steps(ctx, f"Mở Dropdown {name}", "Click một option"),
                                          "Giá trị được chọn hiển thị lên dropdown, danh sách đóng lại, giá trị được focus", CAO)]),
        tc_sub("Chọn nhiều giá trị", [tc_item("Chọn lần lượt 2 option", steps(ctx, "Chọn option thứ nhất", "Mở lại và chọn option thứ hai"),
                                              "Không cho phép chọn nhiều; dropdown hiển thị giá trị chọn gần nhất", TB)]),
        tc_sub("Bỏ chọn giá trị đã chọn", [tc_item("Xóa giá trị đã chọn", steps(ctx, "Chọn một option", "Thực hiện bỏ chọn (icon x / phím Delete)"),
                                                   unselect, TB)]),
    ]))
    rows.append(api_group())
    if locked_required:
        rows.append(tc("dropdown bắt buộc không cho bỏ chọn", "Dropdown bắt buộc luôn có giá trị", "",
                       steps(ctx, f"Thử xóa giá trị của Dropdown {name}"),
                       "Không thể xóa về rỗng; giá trị vẫn được gửi khi Tìm kiếm", TB))
    if searchable:
        rows.append(search_group(name, ctx, *search_hits))
    return rows


def multiselect(name, ctx, placeholder, options, order, n_opts=None, searchable=False, search_hits=("", ""), exact_only=False):
    """Nhóm J — multi-select combobox (+ D22–D28 when searchable)."""
    rows = [
        subsection(f"Kiểm tra Combobox {name}"),
        tc("hiển thị", f"Hiển thị Combobox {name}", "", steps(ctx, f"Quan sát Combobox {name}"),
           "Combobox hiển thị đúng vị trí, kích thước theo thiết kế; click toàn bộ vùng control đều mở danh sách", TB),
        tc("giá trị mặc định", "Giá trị mặc định khi mở màn hình", "", steps(ctx, f"Quan sát Combobox {name}"),
           "Không có giá trị nào được chọn", TB),
        tc("placeholder", "Placeholder khi chưa chọn", "", steps(ctx, f"Quan sát placeholder Combobox {name}"), placeholder, THAP),
        tc("trường không bắt buộc", "Tìm kiếm khi bỏ trống", "",
           steps(ctx, "Chọn đủ 3 điều kiện bắt buộc", f"Bỏ trống {name}", "Click Tìm kiếm"),
           f"Tìm kiếm thành công, không lọc theo {name}; không có dấu (*)", TB),
        tc("thứ tự sắp xếp giá trị", "Thứ tự option trong danh sách", "", steps(ctx, f"Mở Combobox {name}"), order, THAP),
        tc("căn lề các giá trị trong danh sách", "Căn lề option", "", steps(ctx, f"Mở Combobox {name}"),
           "Các giá trị căn trái; option dài hiển thị tooltip", THAP),
        tc("focus option theo ký tự gõ từ bàn phím", "Gõ ký tự đầu khi danh sách đang mở", "",
           steps(ctx, f"Mở Combobox {name}", "Gõ ký tự đầu của một option"),
           "Focus vào item đầu tiên bắt đầu bằng ký tự vừa gõ", THAP),
        tc("bỏ chọn bằng icon x trên tag", "Click icon × trên giá trị đã chọn", "",
           steps(ctx, "Chọn 2 giá trị", "Click icon × trên một tag"),
           "Giá trị bị xóa khỏi danh sách đã chọn; khi chọn nhiều hiển thị dạng \"item 1 + N items\" (Quy tắc component)", TB),
        tc_group("Kiểm tra chọn giá trị", [
            tc_sub("Chọn 1 giá trị", [tc_item("Chọn một option", steps(ctx, f"Mở {name}", "Tick một option"),
                                              "Giá trị được chọn hiển thị lên combobox", CAO)]),
            tc_sub("Chọn nhiều giá trị", [tc_item("Chọn 3 option", steps(ctx, f"Mở {name}", "Tick 3 option"),
                                                  "Cho phép chọn đồng thời; hiển thị \"item 1 + 2 items\"", CAO)]),
            tc_sub("Bỏ chọn 1 giá trị", [tc_item("Bỏ tick một option đã chọn", steps(ctx, "Chọn 2 option", "Bỏ tick một option"),
                                                 "Option bị bỏ chọn, option còn lại giữ nguyên", TB)]),
            tc_sub("Bỏ chọn nhiều giá trị", [tc_item("Bỏ tick lần lượt mọi option đã chọn", steps(ctx, "Chọn 3 option", "Bỏ tick cả 3"),
                                                     "Combobox trở về placeholder", TB)]),
        ]),
    ]
    rows.append(scroll_group(f"Combobox {name}", ctx, n_opts))
    rows.append(tc("options hiển thị đúng", "Nội dung danh sách option", "", steps(ctx, f"Mở {name}"), options, CAO))
    rows.append(api_group())
    if searchable:
        rows.append(search_group(name, ctx, *search_hits, exact_only=exact_only))
    return rows


def date_range(name, ctx, err_pair):
    """Nhóm K — RangePicker used as a search filter (K09–K11, K17 N/A: tìm kiếm cho chọn ngày tự do)."""
    return [
        subsection(f"Kiểm tra DatePicker {name}"),
        tc("hiển thị", f"Hiển thị RangePicker {name}", "", steps(ctx, f"Quan sát {name}"),
           "Hiển thị 2 ô Từ ngày → Đến ngày, icon lịch; mặc định để trống, placeholder dd/mm/yyyy", TB),
        tc("focus calendar khi ô trống", "Mở calendar khi chưa có giá trị", "", steps(ctx, f"Click ô Từ ngày của {name}"),
           "Calendar mở, highlight ngày hiện tại hệ thống", TB),
        tc("focus calendar khi ô có giá trị", "Mở calendar khi đã có giá trị", "Từ ngày = 15/08/2025",
           steps(ctx, "Chọn Từ ngày 15/08/2025", "Click lại ô Từ ngày"), "Calendar highlight ngày 15/08/2025", TB),
        tc("chọn ngày từ calendar", "Chọn khoảng ngày từ calendar", "01/08/2025 → 31/08/2025",
           steps(ctx, "Chọn Từ ngày 01/08/2025", "Chọn Đến ngày 31/08/2025"),
           "Calendar đóng; hiển thị 01/08/2025 → 31/08/2025 đúng định dạng DD/MM/YYYY", CAO),
        tc("icon x xóa ngày", "Click icon x trên ô ngày", "01/08/2025 → 31/08/2025",
           steps(ctx, "Chọn khoảng ngày", "Hover vào ô, click icon x"),
           "Xóa giá trị cả Từ ngày và Đến ngày, ô trở về placeholder dd/mm/yyyy; icon x chỉ hiển thị khi có giá trị (quyết định user GAP-03)", TB),
        tc("định dạng của datepicker", "Định dạng hiển thị", "", steps(ctx, f"Chọn ngày ở {name}", "Kiểm tra định dạng"),
           "Định dạng của datepicker: dd/mm/yyyy (theo mẫu common1)", TB),
        tc("tính bắt buộc", "Bỏ trống khoảng ngày", "", steps(ctx, f"Bỏ trống {name}", "Click Tìm kiếm"),
           "Cho phép bỏ trống; tìm kiếm không lọc theo khoảng ngày này", TB),
        tc("click vào icon calendar", "Mở calendar bằng icon", "", steps(ctx, f"Click icon Calendar bên cạnh {name}"),
           "Hiển thị hộp Calendar, focus ngày đang được chọn (ngày hiện tại nếu chưa chọn)", TB),
        tc("copy/paste dữ liệu vào datepicker", "Dán ngày hợp lệ", "Copy '15/08/2025'", steps(ctx, "Copy '15/08/2025'", "Ctrl+V vào ô Từ ngày", "Blur khỏi ô"),
           "Hệ thống cho phép copy/paste, nhận giá trị 15/08/2025", TB),
        tc("xóa dữ liệu bằng bàn phím", "Xóa giá trị đã chọn", "", steps(ctx, "Chọn ngày", "Đặt con trỏ vào ô, nhấn Backspace/Delete xóa hết", "Blur khỏi ô"),
           "Hệ thống cho phép xóa; ô trở về trống", TB),
        tc("nhập tay ngày hợp lệ", "Nhập tay ngày đúng định dạng", "05/09/2025",
           steps(ctx, "Nhập '05/09/2025' vào ô Từ ngày", "Blur khỏi ô"), "Hệ thống nhận giá trị 05/09/2025", TB),
        tc("nhập tay sai định dạng", "Nhập tay ngày sai định dạng", "2025-09-05; abc; 05/09/25",
           steps(ctx, "Nhập lần lượt từng giá trị", "Blur khỏi ô"), "Hiển thị lỗi ngay khi blur; không nhận giá trị (Quy tắc component)", TB),
        tc("nhập tay ngày không tồn tại", "Nhập ngày đúng định dạng nhưng không tồn tại", "31/02/2025; 32/01/2025",
           steps(ctx, "Nhập giá trị", "Blur khỏi ô"), "Hiển thị lỗi ngày không hợp lệ ngay khi blur", TB),
        tc("ngày 29/02 năm nhuận và cuối tháng", "Nhập ngày đặc biệt hợp lệ", "29/02/2024; 30/04/2025; 31/12/2025",
           steps(ctx, "Nhập giá trị", "Blur khỏi ô"), "Hệ thống nhận giá trị hợp lệ", TB),
        tc("nhập ký tự không hợp lệ", "Nhập chữ, ký tự đặc biệt khác '/'", "ab/cd/efgh; 05-09-2025; @#$",
           steps(ctx, "Nhập giá trị", "Blur khỏi ô"), "Hiển thị lỗi ngay khi blur", TB),
        tc("từ ngày lớn hơn đến ngày", "Từ ngày > Đến ngày", "Từ 10/09/2025, Đến 09/09/2025",
           steps(ctx, "Chọn khoảng ngày", "Click Tìm kiếm"),
           f"Hiển thị lỗi inline ERR_003 \"Từ ngày phải nhỏ hơn hoặc bằng Đến ngày.\" tại {err_pair}; không tìm kiếm (BR-018)", CAO),
        tc("từ ngày bằng đến ngày", "Từ ngày = Đến ngày", "Từ 30/08/2025, Đến 30/08/2025",
           steps(ctx, "Chọn khoảng ngày", "Click Tìm kiếm"), "Tìm kiếm thành công, lấy bản ghi trong ngày 30/08/2025 (cận bao gồm)", CAO),
        tc("từ ngày nhỏ hơn đến ngày", "Từ ngày < Đến ngày", "Từ 01/08/2025, Đến 31/08/2025",
           steps(ctx, "Chọn khoảng ngày", "Click Tìm kiếm"), "Tìm kiếm thành công", TB),
        tc("chỉ nhập một vế", "Chỉ nhập Từ ngày hoặc chỉ nhập Đến ngày", "Chỉ Từ 01/08/2025; chỉ Đến 31/08/2025",
           steps(ctx, "Nhập một vế, bỏ trống vế còn lại", "Click Tìm kiếm"),
           "Tìm kiếm thành công: chỉ Từ → từ ngày đó trở về sau; chỉ Đến → đến hết ngày đó (assumption Q24)", TB),
    ]


def textarea(name, ctx_open, popup, confirm_btn):
    """Nhóm G — Area box (41 TCs): D01–D04 + 17 keyboard + 17 paste + G07, G11, G12."""
    open_ = steps(*ctx_open)
    click = f"Click nút {confirm_btn} trên {popup}"
    kb = lambda data, res, prio=TB: tc_item(data, open_ + f"\n{len(ctx_open) + 1}. Nhập: {data}\n{len(ctx_open) + 2}. {click}", res, prio)
    cp = lambda data, res, prio=TB: tc_item(data, open_ + f"\n{len(ctx_open) + 1}. Copy chuỗi: {data}\n{len(ctx_open) + 2}. Ctrl+V vào ô Lý do\n{len(ctx_open) + 3}. {click}", res, prio)
    ok = "Chấp nhận; thao tác thành công, Lý do được lưu đúng giá trị đã nhập"
    return [
        subsection(f"Kiểm tra Area box {name}"),
        tc("hiển thị", "Hiển thị ô Lý do", "", steps(*ctx_open, "Quan sát ô Lý do"),
           "Hiển thị nhãn \"Lý do\" kèm dấu (*), textarea, bộ đếm \"0/1000 ký tự\"", TB),
        tc("giá trị mặc định", "Giá trị mặc định khi mở popup", "", steps(*ctx_open, "Quan sát ô Lý do"), "Ô Lý do trống", TB),
        tc("placeholder", "Placeholder khi chưa nhập", "", steps(*ctx_open, "Quan sát ô Lý do"), "Hiển thị placeholder \"Nhập lý do\"", THAP),
        tc("trường bắt buộc", "Bỏ trống Lý do rồi xác nhận", "Lý do: (rỗng)", steps(*ctx_open, click),
           "Popup giữ nguyên; ô Lý do viền đỏ, hiển thị ERR_001 \"Lý do không được để trống.\" ngay dưới ô; không ghi dữ liệu (BR-038)", CAO),
        tc_group("Kiểm tra khi nhập giá trị", [
            tc_sub("Kiểm tra nhập maxlength", [
                kb("999 ký tự", ok, CAO),
                kb("1000 ký tự", ok + "; bộ đếm hiển thị 1000/1000", CAO),
                kb("1001 ký tự", "Không nhập được ký tự thứ 1001 (chặn tại 1000) đồng thời hiển thị ERR_023 \"Lý do không được vượt quá 1000 ký tự.\" ngay dưới ô Lý do (BR-038, quyết định user GAP-01)", CAO),
            ]),
            tc_sub("Kiểm tra khi nhập khoảng trắng", [
                kb("Toàn khoảng trắng '     '", "Trim → rỗng; hiển thị ERR_001 \"Lý do không được để trống.\"; không ghi dữ liệu", CAO),
                kb("'   Hồ sơ hợp lệ   ' (khoảng trắng đầu cuối)", "Trim khoảng trắng đầu cuối khi blur/submit; lưu \"Hồ sơ hợp lệ\""),
                kb("'Hồ sơ hợp lệ' (khoảng trắng giữa)", "Giữ nguyên khoảng trắng ở giữa; lưu thành công"),
                kb("'Hồ  sơ    hợp lệ' (nhiều khoảng trắng giữa)", "Giữ nguyên chuỗi; lưu thành công"),
            ]),
            tc_sub("Kiểm tra nhập ký tự", [
                kb("Chữ in hoa 'HO SO HOP LE'", ok),
                kb("Chữ in thường 'ho so hop le'", ok),
                kb("Ký tự số '1234567890'", ok),
                kb("Ký tự đặc biệt '!@#$%^&*()_+-=[]{};:,./?'", ok),
                kb("Hỗn hợp 'Hồ sơ HSPL-01 đã đối chiếu 100%'", ok),
                kb("Tiếng Việt có dấu 'Thông tin pháp lý đã được xác minh với đơn vị'", ok),
            ]),
            tc_sub("Kiểm tra bảo mật", [
                kb("'<script>alert(1)</script>'", "Lưu dạng text; không thực thi script khi hiển thị lại ở tab Lịch sử / INF_011", CAO),
                kb("\"' OR '1'='1'; DROP TABLE X;--\"", "Lưu dạng text; không lỗi hệ thống, không ảnh hưởng CSDL", CAO),
                kb("'https://example.com/a?b=1'", "Lưu dạng text, không tự sinh liên kết thực thi", TB),
                kb("'<img src=x onerror=alert(1)>' (CSRF/HTML)", "Lưu dạng text đã escape; không gửi request ngoài ý muốn", CAO),
            ]),
        ]),
        tc_group("Kiểm tra khi copy/paste giá trị", [
            tc_sub("Kiểm tra copy/paste maxlength", [
                cp("999 ký tự", ok, CAO),
                cp("1000 ký tự", ok + "; bộ đếm 1000/1000", CAO),
                cp("1001 ký tự", "Bị cắt còn 1000 ký tự đồng thời hiển thị ERR_023 \"Lý do không được vượt quá 1000 ký tự.\" ngay dưới ô Lý do (BR-038, quyết định user GAP-01)", CAO),
            ]),
            tc_sub("Kiểm tra khi copy/paste khoảng trắng", [
                cp("Toàn khoảng trắng", "Trim → rỗng; ERR_001 khi xác nhận", CAO),
                cp("Khoảng trắng đầu cuối", "Trim khi blur/submit; lưu chuỗi đã trim"),
                cp("Khoảng trắng giữa", "Giữ nguyên; lưu thành công"),
                cp("Nhiều khoảng trắng giữa", "Giữ nguyên; lưu thành công"),
            ]),
            tc_sub("Kiểm tra copy/paste ký tự", [
                cp("Chữ in hoa", ok), cp("Chữ in thường", ok), cp("Ký tự số", ok),
                cp("Ký tự đặc biệt", ok), cp("Hỗn hợp chữ, số, ký tự đặc biệt", ok), cp("Tiếng Việt có dấu", ok),
            ]),
            tc_sub("Kiểm tra copy/paste bảo mật", [
                cp("'<script>alert(1)</script>'", "Lưu dạng text; không thực thi script", CAO),
                cp("Chuỗi SQL injection", "Không lỗi hệ thống, không ảnh hưởng CSDL", CAO),
                cp("URL", "Lưu dạng text", TB),
                cp("Thẻ HTML có sự kiện (CSRF)", "Lưu dạng text đã escape", CAO),
            ]),
        ]),
        tc("nhập nhiều dòng bằng phím Enter", "Xuống dòng trong ô Lý do", "Dòng 1 + Enter + Dòng 2 (Shift+Enter)",
           steps(*ctx_open, "Nhập 'Dòng 1', nhấn Enter, nhập 'Dòng 2'", click),
           "Con trỏ xuống dòng; lý do lưu và hiển thị lại đúng nhiều dòng (cột Mô tả tab Lịch sử)", TB),
        tc("bộ đếm ký tự realtime", "Bộ đếm \"đã dùng/tối đa\"", "Nhập 15 ký tự, xóa 5 ký tự",
           steps(*ctx_open, "Nhập 15 ký tự", "Xóa 5 ký tự"), "Bộ đếm cập nhật tức thời 15/1000 → 10/1000", TB),
        tc("tự động thay đổi chiều cao", "Auto resize theo nội dung", "Nhập 20 dòng",
           steps(*ctx_open, "Nhập lần lượt 20 dòng"), "Textarea tự mở rộng chiều cao tới giới hạn maxRows rồi hiển thị scroll; popup không vỡ layout", THAP),
    ]


def confirm_popup_controls(code, ctx, confirm_label, confirm_effect, keep_reason=True):
    """CONF_* popup controls: confirm (3), cancel (3), close icon X (2)."""
    keep = "ô Lý do giữ nguyên nội dung đã nhập khi mở lại popup (assumption Q32)" if keep_reason else ""
    return [
        subsection(f"Kiểm tra button {confirm_label} trên Hộp thoại xác nhận {code}"),
        tc("hiển thị button xác nhận", f"Kiểm tra hiển thị nút {confirm_label}", "", steps(ctx, f"Quan sát nút {confirm_label}"),
           f"Nút \"{confirm_label}\" là Primary button, căn giữa cùng nút Hủy, nhãn đúng chính tả", TB),
        tc("trạng thái button xác nhận", f"Kiểm tra trạng thái enable/disable của nút {confirm_label}", "",
           steps(ctx, f"Quan sát nút {confirm_label} khi Lý do trống và khi đã nhập"),
           "Nút luôn enable; validate Lý do khi click (BR-038)", TB),
        tc("click button xác nhận", f"Kiểm tra click nút {confirm_label}", "Lý do: 'Đã đối chiếu với đơn vị'",
           steps(ctx, "Nhập Lý do hợp lệ", f"Click nút {confirm_label}"), confirm_effect, CAO),
        subsection(f"Kiểm tra button Hủy trên Hộp thoại xác nhận {code}"),
        tc("hiển thị button hủy", "Kiểm tra hiển thị nút Hủy", "", steps(ctx, "Quan sát nút Hủy"),
           "Nút \"Hủy\" là Secondary button, đặt trước nút xác nhận", TB),
        tc("trạng thái button hủy", "Kiểm tra trạng thái enable/disable của nút Hủy", "", steps(ctx, "Quan sát nút Hủy"), "Nút luôn enable", TB),
        tc("click button hủy", "Kiểm tra click nút Hủy", "Lý do đã nhập: 'Test hủy'",
           steps(ctx, "Nhập Lý do", "Click Hủy", "Mở lại popup"),
           "Popup đóng, ở lại màn xử lý, không ghi dữ liệu, hồ sơ vẫn Chờ xem xét; " + keep, CAO),
        subsection(f"Kiểm tra icon đóng (X) trên Hộp thoại xác nhận {code}"),
        tc("hiển thị icon đóng", "Kiểm tra hiển thị icon X", "", steps(ctx, "Quan sát góc trên bên phải popup"),
           "Icon X hiển thị góc trên bên phải, cạnh tiêu đề \"Xác nhận thông tin hồ sơ\" (assumption Q31)", THAP),
        tc("click icon đóng", "Kiểm tra click icon X", "Lý do đã nhập: 'Test đóng'", steps(ctx, "Nhập Lý do", "Click icon X"),
           "Popup đóng như nút Hủy: ở lại màn xử lý, không ghi dữ liệu, hồ sơ vẫn Chờ xem xét", TB),
    ]


def grid_column(name, ctx, display, align, filterable=True):
    """Nhóm U — one data column (U01–U04)."""
    filt = (tc("thao tác lọc trên cột", f"Lọc theo cột {name}", "Nhập giá trị có trên trang hiện tại",
               steps(ctx, f"Nhập giá trị vào ô lọc cột {name}", "Click icon x để xóa giá trị lọc"),
               "Chỉ lọc các dòng trên trang đang hiển thị; click x hiển thị lại toàn bộ dòng của trang (Quy tắc component C14)", TB)
            if filterable else
            tc("thao tác lọc trên cột", f"Cột {name} không có ô lọc", "", steps(ctx, f"Quan sát header cột {name}"),
               f"Cột {name} không có icon/ô lọc (Quy tắc component: STT, Thao tác không lọc; SRS không mô tả lọc cho bảng này)", THAP))
    return [
        subsection(f"Kiểm tra cột {name}"),
        tc("hiển thị", f"Hiển thị cột {name}", "", steps(ctx, f"Quan sát cột {name}"), display, TB),
        tc("chỉnh sửa", f"Cột {name} chỉ đọc", "", steps(ctx, f"Double-click / nhấn F2 vào ô của cột {name}"),
           "Không mở edit mode, không có ô nhập; dữ liệu chỉ đọc", TB),
        filt,
        tc("căn lề", f"Căn lề cột {name}", "", steps(ctx, f"Quan sát cột {name}"), align, THAP),
    ]


def grid_action(name, ctx, show, state, click):
    """Nhóm U — one row action (U05–U07)."""
    return [
        subsection(f"Kiểm tra thao tác {name}"),
        tc("hiển thị thao tác", f"Hiển thị mục {name} trong menu Thao tác", "", steps(ctx, "Click icon ... tại cột Thao tác"), show, TB),
        tc("trạng thái thao tác", f"Mục {name} theo trạng thái hồ sơ", "Hồ sơ ở 4 trạng thái", steps(ctx, "Mở menu Thao tác lần lượt từng dòng"), state, CAO),
        tc("click thao tác", f"Click mục {name}", "", steps(ctx, f"Click {name}"), click, CAO),
    ]


def paging(ctx, screen):
    """Nhóm C — grid + paging with the 3 mandatory tc_groups."""
    return [
        subsection("Kiểm tra lưới dữ liệu và phân trang"),
        tc("format lưới", "Format header và giá trị", "", steps(ctx, "Quan sát lưới"),
           "Header căn giữa; text căn trái, số căn phải, ngày/STT/Thao tác căn giữa; cột STT và Thao tác cố định khi cuộn ngang; chỉ có đường kẻ ngang", TB),
        tc("số thứ tự bản ghi", "STT tăng liên tục qua các trang", "> 20 bản ghi", steps(ctx, "Quan sát STT trang 1", "Sang trang 2"),
           "STT tăng dần 1..20 ở trang 1, 21..40 ở trang 2", TB),
        tc("ẩn phân trang khi ít bản ghi", "Không hiển thị phân trang khi ≤ 10 bản ghi", "Điều kiện cho 8 kết quả",
           steps(ctx, "Tìm kiếm cho ra 8 kết quả"), "Control phân trang ẩn", THAP),
        tc("style phân trang", "Chuỗi thông tin phân trang", "987 kết quả",
           steps(ctx, "Quan sát vùng phân trang"), "Hiển thị \"Hiển thị 1 - 20 trên tổng số 987 bản ghi\", số bản ghi/trang, các nút trang", THAP),
        tc("header và footer ổn định khi chuyển trang", "Layout khi chuyển trang", "", steps(ctx, "Chuyển qua lại các trang"),
           "Header, footer, vùng điều kiện không thay đổi vị trí", THAP),
        tc("skeleton loading", "Trạng thái đang tải dữ liệu", "Giả lập mạng chậm", steps(ctx, "Click Tìm kiếm"),
           "Hiển thị skeleton loading thay vì bảng trống trong lúc tải (Quy tắc component)", THAP),
        tc("lưới trống", "Không có dữ liệu", "Điều kiện không khớp", steps(ctx, "Tìm kiếm điều kiện không khớp"),
           "Hiển thị empty state CMP-033 kèm icon (assumption Q30)", TB),
        tc("icon mở rộng full screen", "Mở rộng lưới toàn màn hình", "", steps(ctx, "Click icon mở rộng", "Click lại"),
           "Lưới mở full screen; click lại thu về kích thước ban đầu (Quy tắc component)", THAP),
        tc("cột ngày hiển thị đầy đủ khi hover", "Hover cột Ngày cập nhật", "", steps(ctx, "Bật cột Ngày cập nhật", "Hover vào giá trị"),
           "Hiển thị dd/mm/yyyy; hover hiển thị dd/mm/yyyy HH:MM:SS", THAP),
        tc("cột người hiển thị họ tên khi hover", "Hover cột Người cập nhật", "", steps(ctx, "Bật cột Người cập nhật", "Hover vào username"),
           "Hiển thị username; hover hiển thị Họ và tên đầy đủ", THAP),
        tc_group("Kiểm tra phân trang", [
            tc_sub("Mặc định phân trang", [tc_item("987 bản ghi", steps(ctx, "Quan sát phân trang"), "Mặc định trang 1, 20 bản ghi/trang (BR-027)", TB)]),
            tc_sub("Chuyển đến trang cuối", [tc_item("", steps(ctx, "Click trang cuối"), "Hiển thị trang cuối; nút Next bị disable", TB)]),
            tc_sub("Về trang đầu", [tc_item("", steps(ctx, "Đang ở trang 3, click trang 1"), "Hiển thị trang 1; nút Previous bị disable", TB)]),
            tc_sub("Nút Next", [tc_item("", steps(ctx, "Click nút >"), "Chuyển sang trang kế tiếp", TB)]),
            tc_sub("Nút Previous", [tc_item("", steps(ctx, "Đang ở trang 2, click nút <"), "Quay về trang trước", TB)]),
        ]),
        tc_group("Kiểm tra combobox phân trang", [
            tc_sub("Giá trị mặc định", [tc_item("", steps(ctx, "Quan sát combobox số bản ghi/trang"), "Mặc định 20 / trang", TB)]),
            tc_sub("Giá trị trong combobox", [tc_item("", steps(ctx, "Mở combobox"), "Các lựa chọn theo CMP-015, giá trị lớn nhất 5000 (BR-027, assumption Q27)", TB)]),
            tc_sub("Chọn 1 giá trị", [tc_item("Chọn 5000", steps(ctx, "Chọn 5000 / trang"), "Hiển thị tối đa 5000 bản ghi/trang, quay về trang 1, số trang tính lại đúng", CAO)]),
            tc_sub("Chọn nhiều giá trị", [tc_item("", steps(ctx, "Chọn 2 giá trị liên tiếp"), "Không cho chọn nhiều; giữ giá trị chọn sau cùng", THAP)]),
            tc_sub("Không chọn giá trị", [tc_item("", steps(ctx, "Mở combobox rồi đóng"), "Giữ giá trị hiện tại", THAP)]),
            tc_sub("Phím tắt lên xuống", [tc_item("", steps(ctx, "Focus combobox, dùng phím lên/xuống", "Nhấn Enter"), "Chọn được giá trị bằng bàn phím", THAP)]),
        ]),
        tc_group("Kiểm tra nhập tìm kiếm số trang", [
            tc_sub("Nhập ký tự chữ", [tc_item("'abc'", steps(ctx, "Nhập 'abc' vào ô Đến trang", "Click icon di chuyển"), "Chặn ký tự chữ", TB)]),
            tc_sub("Nhập ký tự đặc biệt", [tc_item("'@#'", steps(ctx, "Nhập '@#' vào ô Đến trang"), "Chặn ký tự đặc biệt", TB)]),
            tc_sub("Nhập ký tự số hợp lệ", [tc_item("'3'", steps(ctx, "Nhập '3'", "Click icon di chuyển"), "Chuyển đến trang 3", TB)]),
            tc_sub("Nhập số trang vượt số trang hiện có", [tc_item("Có 50 trang, nhập '60'", steps(ctx, "Nhập '60'", "Click icon di chuyển"),
                                                                    "Hiển thị trang cuối (trang 50) — BR-027", CAO)]),
        ]),
    ]


def checkbox(name, ctx, rows_extra):
    """Nhóm I — checkbox basics + extra cases."""
    return [
        subsection(f"Kiểm tra Checkbox {name}"),
        tc("hiển thị", f"Hiển thị checkbox {name}", "", steps(ctx, f"Quan sát checkbox {name}"), "Checkbox hiển thị đúng vị trí theo thiết kế", TB),
        tc("giá trị mặc định", "Trạng thái mặc định", "", steps(ctx, f"Quan sát checkbox {name}"), rows_extra["default"], TB),
        tc("check", "Tick checkbox", "", steps(ctx, f"Tick checkbox {name}"), rows_extra["check"], CAO),
        tc("uncheck", "Bỏ tick checkbox", "", steps(ctx, f"Tick rồi bỏ tick checkbox {name}"), rows_extra["uncheck"], CAO),
        tc("thao tác bằng bàn phím", "Space để tick / bỏ tick", "", steps(ctx, f"Focus checkbox {name} bằng Tab", "Nhấn Space"),
           "Trạng thái checkbox đảo ngược, có viền focus rõ ràng (Quy tắc component)", THAP),
    ] + [tc(*r) for r in rows_extra.get("more", [])]


# ══════════════════════════════════════════════════════════════════════════════
# M1 — MH-XLDL-009-001 Danh sách hồ sơ pháp lý (FEAT-XLDL-009-01)
# ══════════════════════════════════════════════════════════════════════════════
PRECOND_M1 = PRECOND_BASE + (
    f"- Đầu mối {DM_IN} có > 1.000 hồ sơ tệp D11 (đủ để phân trang tới trang 50)\n"
    f"- Đầu mối {DM_OUT} là đầu mối gửi báo cáo nhưng KHÔNG thuộc TCTD được phân quyền của cbxl01\n"
)
C1 = "Mở MH-001 Danh sách hồ sơ pháp lý"
C1S = f"Mở MH-001, chọn Loại KH = Cá nhân, Mã đầu mối = {DM_IN}, Mã tệp = D11, click Tìm kiếm"

M1_DISPLAY = (
    "Hiển thị đúng như SRS:\n- Tiêu đề \"Danh sách hồ sơ pháp lý\", breadcrumb Trang chủ / Xử lý dữ liệu\n"
    "- Nút Cấu hình hiển thị, Xuất Excel\n"
    "- Điều kiện: Loại khách hàng (*) = Cá nhân, Mã đầu mối (*) trống, Mã tệp (*) = tệp đầu tiên được phân quyền (D10), "
    "Mã CIC, Mã khách hàng, Nhóm khách hàng, Trạng thái, Người cập nhật, Từ ngày cập nhật → Đến ngày cập nhật, "
    "Từ ngày báo cáo → Đến ngày báo cáo; Tên tệp và CCCD/CMND KHÔNG hiển thị (mặc định tắt)\n"
    "- Nút Thêm bộ lọc, Làm mới, Tìm kiếm\n"
    "- Lưới: checkbox, STT, Ngày báo cáo, Mã đầu mối, Mã khách hàng, Tên khách hàng, CCCD, Địa chỉ, Mã CIC, Nhóm khách hàng, "
    "Trạng thái, Thao tác (Mã tệp, Tên tệp, Loại khách hàng, Ngày cập nhật, Người cập nhật ẩn)\n"
    "- Vùng lưới hiển thị \"Chưa có dữ liệu. Vui lòng chọn tiêu chí tìm kiếm.\"; phân trang 20 / trang\n"
    "- Không hiển thị dải thao tác hàng loạt và banner INF_009 (BR-013, BR-019, BR-021)"
)
M1_TAB = ("Cấu hình hiển thị → Xuất Excel → Loại khách hàng → Mã đầu mối → Mã tệp → Mã CIC → Mã khách hàng → Nhóm khách hàng → "
          "Trạng thái → Người cập nhật → Từ ngày cập nhật → Đến ngày cập nhật → Từ ngày báo cáo → Đến ngày báo cáo → "
          "Thêm bộ lọc → Làm mới → Tìm kiếm → lưới → phân trang")

COLS_M1 = [
    ("STT", "Số thứ tự bản ghi trong danh sách", "Căn giữa", False),
    ("Ngày báo cáo", "Ngày kỳ báo cáo định dạng DD/MM/YYYY; cột bắt buộc, không ẩn được (BR-021)", "Căn giữa", True),
    ("Mã tệp", "Mã tệp D10/D11/Q11 của hồ sơ; ẩn mặc định, hiện khi bật trong Cấu hình hiển thị", "Căn trái", True),
    ("Tên tệp", "Tên tệp báo cáo chứa hồ sơ; ẩn mặc định", "Căn trái", True),
    ("Mã đầu mối", "Mã đầu mối TCTD/CNTCTD gửi báo cáo; cột bắt buộc", "Căn trái", True),
    ("Mã khách hàng", "TTC03; cột bắt buộc", "Căn trái", True),
    ("Tên khách hàng", "TTC04; tên dài xuống dòng, không tràn ô", "Căn trái", True),
    ("CCCD/MSDN", "Tiêu đề \"CCCD\" (CN008) khi Loại KH = Cá nhân, \"MSDN\" (TC011) khi Tổ chức (BR-017, assumption Q25)", "Căn trái", True),
    ("Địa chỉ", "Địa chỉ của khách hàng; dài thì rút gọn \"...\" kèm tooltip", "Căn trái", True),
    ("Loại khách hàng", "Cá nhân / Tổ chức; ẩn mặc định", "Căn trái", True),
    ("Mã CIC", "Mã CIC của KH; trống với hồ sơ Chờ cấp mã", "Căn trái", True),
    ("Nhóm khách hàng", "Một trong 4 nhóm: Mới - Có QHTD, Mới - Không QHTD, Thay đổi TTQT, Không thay đổi TTQT (BR-016)", "Căn trái", True),
    ("Trạng thái", "Badge chấm màu + chữ: Chờ cấp mã xám, Chờ xem xét cam, Đã xử lý xanh lá, Từ chối đỏ (chữ đỏ)", "Căn giữa", True),
    ("Ngày cập nhật", "Thời điểm cập nhật hồ sơ (dd/mm/yyyy, hover đầy đủ giờ); ẩn mặc định", "Căn giữa", True),
    ("Người cập nhật", "Username tài khoản cập nhật hoặc \"Sys\"; hover hiển thị họ tên; ẩn mặc định", "Căn trái", True),
]


# Display-config columns (BR-021): (name, checked by default, locked = mandatory column)
CONFIG_COLS = [
    ("STT", True, False), ("Ngày báo cáo", True, True), ("Mã tệp", False, False), ("Tên tệp", False, False),
    ("Mã đầu mối", True, True), ("Mã khách hàng", True, True), ("Tên khách hàng", True, False),
    ("CCCD/MSDN", True, False), ("Địa chỉ", True, False), ("Loại khách hàng", False, False), ("Mã CIC", True, False),
    ("Nhóm khách hàng", True, False), ("Trạng thái", True, False), ("Ngày cập nhật", False, False),
    ("Người cập nhật", False, False), ("Thao tác", True, True),
]
# Add-filter options (BR-019): (name, checked by default, locked = mandatory filter)
FILTERS = [
    ("Loại khách hàng", True, True), ("Mã đầu mối", True, True), ("Mã tệp", True, True), ("Mã CIC", True, False),
    ("Tên tệp", False, False), ("Mã khách hàng", True, False), ("Nhóm khách hàng", True, False), ("Trạng thái", True, False),
    ("Người cập nhật", True, False), ("CCCD/CMND", False, False),
    ("Từ ngày cập nhật → Đến ngày cập nhật", True, False), ("Từ ngày báo cáo → Đến ngày báo cáo", True, False),
]


EXPORT_FIELDS = "\n".join(f"- {n}" for n, _c, _l in CONFIG_COLS if n != "Thao tác")


def _state(checked, locked):
    if locked:
        return "Checkbox ở trạng thái check và disable, không cho phép thao tác (cột/bộ lọc bắt buộc)"
    return f"Checkbox mặc định {'check' if checked else 'uncheck'} và enable, cho phép check/uncheck"


def title_rows(title, ctx):
    """Screen / popup title — fixed text, not editable (per practices/testcases/common1.xlsx)."""
    return [
        subsection(f"Kiểm tra title {title}"),
        tc("hiển thị title", "Kiểm tra hiển thị title", "", steps(ctx, "Kiểm tra hiển thị title"), f"Title cố định mặc định: \"{title}\"", THAP),
        tc("chỉnh sửa title", "Kiểm tra chỉnh sửa title", "", steps(ctx, "Click / thử nhập vào title"), "Không cho phép chỉnh sửa", THAP),
    ]


def api_fail_rows(ctx, action_label, confirm_steps, who):
    """API lỗi / API timeout / hết phiên for a confirm action (per common1.xlsx)."""
    msg = "Hệ thống hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; " + who + " giữ trạng thái Chờ xem xét, không ghi lý do (theo mẫu common1)"
    return [
        tc(f"{action_label.lower()} khi API lỗi", f"{action_label} thất bại — API lỗi", "Giả lập API trả lỗi 500 / mất kết nối",
           steps(ctx, *confirm_steps), msg, CAO),
        tc(f"{action_label.lower()} khi API timeout", f"{action_label} thất bại — API timeout", "Giả lập API phản hồi quá thời gian chờ",
           steps(ctx, *confirm_steps), "Hiển thị loading trong thời gian chờ; sau đó " + msg[0].lower() + msg[1:], CAO),
        tc(f"{action_label.lower()} khi hết phiên đăng nhập", f"{action_label} khi hết token", "Token phiên đăng nhập hết hạn trước khi xác nhận",
           steps(ctx, *confirm_steps[:-1], "Chờ token hết hạn", confirm_steps[-1]),
           f"Hết token đăng nhập, điều hướng về màn hình đăng nhập; đăng nhập lại, {who} không bị chuyển trạng thái (theo mẫu common1)", CAO),
    ]


def display_config_rows():
    """Button Cấu hình hiển thị + popup (structure per practices/testcases/common1.xlsx; columns per BR-021)."""
    P = f"{C1S}, click button Cấu hình hiển thị"
    default_list = "\n".join(f"- {n}: mặc định {'check' if c else 'uncheck'}{' (disable)' if l else ''}" for n, c, l in CONFIG_COLS)
    rows = button("Cấu hình hiển thị", C1, "Button hiển thị giống như trong SRS: góc phải tiêu đề trang, có icon, nhãn \"Cấu hình hiển thị\"",
                  "Trạng thái: Enable",
                  "Hiển thị popup Cấu hình hiển thị gồm: tiêu đề \"Cấu hình hiển thị\", icon X, ô tìm kiếm trường thông tin, "
                  "danh sách cột kèm checkbox theo đúng thứ tự trên lưới:\n" + default_list +
                  "\n- Button Bỏ chọn, Chọn tất cả, Áp dụng (BR-021, CMP-025)", TB)
    rows += [
        subsection("Kiểm tra title popup Cấu hình hiển thị"),
        tc("hiển thị title", "Kiểm tra hiển thị title", "", steps(P, "Kiểm tra hiển thị title"), "Title cố định: \"Cấu hình hiển thị\"", THAP),
        tc("chỉnh sửa title", "Kiểm tra chỉnh sửa title", "", steps(P, "Click vào title"), "Không được chỉnh sửa", THAP),
        subsection("Kiểm tra ô tìm kiếm trường thông tin trên popup Cấu hình hiển thị"),
        tc("giá trị mặc định", "Kiểm tra giá trị mặc định", "", steps(P, "Kiểm tra giá trị mặc định ô tìm kiếm"), "Mặc định bỏ trống", TB),
        tc("bỏ trống", "Kiểm tra bỏ trống", "", steps(P, "Bỏ trống ô tìm kiếm", "Focus out"), "Hệ thống cho phép bỏ trống; hiển thị đủ danh sách cột", TB),
        tc_group("Kiểm tra nhập tìm kiếm", [
            tc_sub("Nhập tìm kiếm giá trị có trong danh sách", [
                tc_item("Tìm kiếm tương đối: 'Mã'", steps(P, "Click vào ô tìm kiếm", "Nhập 'Mã'"),
                        "Hiển thị các cột chứa 'Mã': Mã tệp, Mã đầu mối, Mã khách hàng, Mã CIC", TB),
                tc_item("Tìm kiếm tuyệt đối: 'Nhóm khách hàng'", steps(P, "Click vào ô tìm kiếm", "Nhập 'Nhóm khách hàng'"),
                        "Hiển thị đúng cột Nhóm khách hàng", TB),
            ]),
            tc_sub("Nhập tìm kiếm giá trị không có trong danh sách", [
                tc_item("'Dung lượng'", steps(P, "Click vào ô tìm kiếm", "Nhập 'Dung lượng'"), "Không hiển thị cột nào trong danh sách", TB),
            ]),
        ]),
        tc_group("Kiểm tra khi nhập giá trị", [
            tc_sub("Kiểm tra khi nhập khoảng trắng", [
                tc_item("Nhập toàn khoảng trắng", steps(P, "Tại ô tìm kiếm, nhập toàn khoảng trắng", "Focus out"), "Hệ thống tự động trim khoảng trắng khi focus out", TB),
                tc_item("Nhập khoảng trắng ở đầu cuối ký tự", steps(P, "Nhập '  Mã CIC  '", "Focus out"), "Hệ thống tự động trim khoảng trắng khi focus out", TB),
                tc_item("Nhập khoảng trắng ở giữa ký tự", steps(P, "Nhập 'Mã CIC'", "Focus out"), "Hệ thống cho phép nhập", TB),
                tc_item("Nhập nhiều khoảng trắng ở giữa các ký tự", steps(P, "Nhập 'Mã    CIC'", "Focus out"), "Hệ thống cho phép nhập", TB),
            ]),
            tc_sub("Kiểm tra nhập maxlength", [
                tc_item("Nhập < 100 ký tự", steps(P, "Nhập 99 ký tự", "Focus out"), "Hệ thống cho phép nhập", TB),
                tc_item("Nhập = 100 ký tự", steps(P, "Nhập 100 ký tự", "Focus out"), "Hệ thống cho phép nhập", TB),
                tc_item("Nhập > 100 ký tự", steps(P, "Nhập 101 ký tự", "Focus out"), "Hệ thống chặn không cho nhập quá maxlength", TB),
            ]),
            tc_sub("Kiểm tra khi nhập ký tự số", [tc_item("'123'", steps(P, "Nhập ký tự số"), "Hệ thống cho phép nhập", THAP)]),
            tc_sub("Kiểm tra khi nhập ký tự đặc biệt", [tc_item("'/@#'", steps(P, "Nhập ký tự đặc biệt"), "Hệ thống cho phép nhập", THAP)]),
            tc_sub("Kiểm tra khi nhập ký tự chữ in hoa", [tc_item("'MÃ CIC'", steps(P, "Nhập chữ in hoa"), "Hệ thống cho phép nhập; kết quả tìm không phân biệt hoa thường", THAP)]),
            tc_sub("Kiểm tra khi nhập ký tự chữ in thường", [tc_item("'mã cic'", steps(P, "Nhập chữ in thường"), "Hệ thống cho phép nhập; kết quả tìm không phân biệt hoa thường", THAP)]),
            tc_sub("Kiểm tra nhập ký tự chữ có dấu, tiếng Việt", [tc_item("'Người cập nhật'", steps(P, "Nhập chữ có dấu"), "Hệ thống cho phép nhập", THAP)]),
        ]),
        tc_group("Kiểm tra khi copy/paste giá trị", [
            tc_sub("Kiểm tra khi copy/paste khoảng trắng", [
                tc_item("Copy/paste toàn khoảng trắng", steps(P, "Copy/paste toàn khoảng trắng", "Focus out"), "Hệ thống cho phép copy/paste; trim khi focus out", TB),
                tc_item("Copy/paste khoảng trắng ở đầu cuối ký tự", steps(P, "Copy/paste '  Mã CIC  '", "Focus out"), "Hệ thống cho phép copy/paste; trim khi focus out", TB),
                tc_item("Copy/paste khoảng trắng ở giữa ký tự", steps(P, "Copy/paste 'Mã CIC'", "Focus out"), "Hệ thống cho phép copy/paste", TB),
                tc_item("Copy/paste nhiều khoảng trắng ở giữa các ký tự", steps(P, "Copy/paste 'Mã    CIC'", "Focus out"), "Hệ thống cho phép copy/paste", TB),
            ]),
            tc_sub("Kiểm tra copy/paste maxlength", [
                tc_item("Copy/paste = 100 ký tự", steps(P, "Copy/paste 100 ký tự", "Focus out"), "Hệ thống cho phép copy/paste", TB),
                tc_item("Copy/paste > 100 ký tự", steps(P, "Copy/paste 101 ký tự", "Focus out"), "Hệ thống chặn không cho nhập quá maxlength (cắt còn 100 ký tự)", TB),
            ]),
            tc_sub("Kiểm tra khi copy/paste ký tự số", [tc_item("'123'", steps(P, "Copy/paste ký tự số"), "Hệ thống cho phép copy/paste", THAP)]),
            tc_sub("Kiểm tra khi copy/paste ký tự đặc biệt", [tc_item("'/@#'", steps(P, "Copy/paste ký tự đặc biệt"), "Hệ thống cho phép copy/paste", THAP)]),
            tc_sub("Kiểm tra khi copy/paste ký tự chữ in hoa", [tc_item("'MÃ CIC'", steps(P, "Copy/paste chữ in hoa"), "Hệ thống cho phép copy/paste", THAP)]),
            tc_sub("Kiểm tra khi copy/paste ký tự chữ in thường", [tc_item("'mã cic'", steps(P, "Copy/paste chữ in thường"), "Hệ thống cho phép copy/paste", THAP)]),
            tc_sub("Kiểm tra copy/paste ký tự chữ có dấu, tiếng Việt", [tc_item("'Người cập nhật'", steps(P, "Copy/paste chữ có dấu"), "Hệ thống cho phép copy/paste", THAP)]),
        ]),
        subsection("Kiểm tra checkbox trên popup Cấu hình hiển thị"),
        tc("hiển thị checkbox", "Kiểm tra hiển thị", "", steps(P, "Kiểm tra hiển thị checkbox"), "Hiển thị căn chỉnh hợp lý như trong SRS; mỗi cột một checkbox", TB),
        tc("giá trị mặc định checkbox", "Kiểm tra giá trị mặc định", "", steps(P, "Kiểm tra giá trị mặc định"), "Trạng thái mặc định các checkbox:\n" + default_list + " (BR-021)", CAO),
        tc_group("Kiểm tra onclick checkbox", [
            tc_sub(name, [tc_item("", steps(P, f"Click vào checkbox {name}"), _state(c, l) + (" — sau Áp dụng, cột hiển thị/ẩn trên lưới tương ứng" if not l else ""),
                                  CAO if l else TB)])
            for name, c, l in CONFIG_COLS
        ]),
        tc_group("Kiểm tra kéo thả các trường", [
            tc_sub(name, [tc_item("", steps(P, f"Giữ và kéo trường {name} sang vị trí khác", "Click Áp dụng"),
                                  "Được phép kéo thả trường; sau Áp dụng, thứ tự cột trên lưới thay đổi tương ứng (BR-021)", TB)])
            for name, _c, _l in CONFIG_COLS
        ]),
    ]
    rows += button("Bỏ chọn (popup Cấu hình hiển thị)", P, "Button hiển thị, căn chỉnh như trong SRS", "Trạng thái: Enable",
                   "Bỏ chọn mọi trường không bị disable; các cột bắt buộc (Ngày báo cáo, Mã đầu mối, Mã khách hàng, Thao tác) vẫn được chọn", TB)
    rows += [
        subsection("Kiểm tra button Chọn tất cả (popup Cấu hình hiển thị)"),
        tc("hiển thị button", "Kiểm tra hiển thị nút Chọn tất cả", "", steps(P, "Kiểm tra hiển thị button"), "Button hiển thị \"Chọn tất cả\", căn chỉnh như trong SRS", TB),
        tc("trạng thái button", "Kiểm tra trạng thái enable/disable của nút Chọn tất cả", "", steps(P, "Kiểm tra trạng thái button"), "Trạng thái: Enable", TB),
        tc_group("Kiểm tra click nút Chọn tất cả", [
            tc_sub("Trường hợp các trường option chưa được tích chọn", [tc_item("", steps(P, "Click Bỏ chọn", "Click Chọn tất cả"),
                                                                       "Tích chọn tất cả các trường option", TB)]),
            tc_sub("Trường hợp đã có trường option được tích chọn", [tc_item("", steps(P, "Giữ trạng thái mặc định", "Click Chọn tất cả"),
                                                                     "Tích chọn tất cả các trường option, trường đã chọn giữ nguyên", TB)]),
        ]),
        tc("căn lề button", "Kiểm tra căn lề nút Chọn tất cả", "", steps(P, "Kiểm tra căn lề"), "Căn lề phải", THAP),
    ]
    rows += button("Áp dụng (popup Cấu hình hiển thị)", P, "Button \"Áp dụng\" là Primary button của popup", "Trạng thái: Enable",
                   "Đóng popup; lưới hiển thị đúng các cột đã chọn và thứ tự đã kéo thả; cấu hình được lưu trên máy người dùng, giữ sau F5 (BR-021)", CAO)
    rows += [
        subsection("Kiểm tra icon đóng (X) trên popup Cấu hình hiển thị"),
        tc("hiển thị icon đóng", "Kiểm tra hiển thị icon X", "", steps(P, "Quan sát góc trên bên phải popup"), "Icon X hiển thị góc trên bên phải popup", THAP),
        tc("click icon đóng", "Kiểm tra click icon X", "Đã bỏ chọn cột Địa chỉ nhưng chưa Áp dụng", steps(P, "Bỏ chọn Địa chỉ", "Click icon X"),
           "Đóng popup, không áp dụng thay đổi; lưới vẫn hiển thị cột Địa chỉ", TB),
    ]
    return rows


def add_filter_rows():
    """Button Thêm bộ lọc + popup (structure per practices/testcases/common1.xlsx; filters per BR-019)."""
    P = f"{C1}, click button Thêm bộ lọc"
    flist = "\n".join(f"- {n}{' (disabled, luôn check)' if l else (' (mặc định check)' if c else ' (mặc định uncheck)')}" for n, c, l in FILTERS)
    rows = button("Thêm bộ lọc", C1, "Button hiển thị giống như trong SRS: góc phải vùng điều kiện, cạnh Làm mới, Tìm kiếm", "Trạng thái: Enable",
                  "Hiển thị popup Thêm bộ lọc gồm danh sách bộ lọc kèm checkbox:\n" + flist + " (BR-019)", TB)
    rows += [
        subsection("Kiểm tra popup Thêm bộ lọc"),
        tc("mặc định popup", "Kiểm tra mặc định tích chọn", "", steps(P, "Kiểm tra mặc định tích chọn"),
           "Các checkbox mặc định:\n" + flist + "\nKhớp với các bộ lọc đang hiển thị trên vùng điều kiện (BR-019)", CAO),
        tc_group("Kiểm tra thao tác check/uncheck", [
            tc_sub(name, [tc_item("", steps(P, f"Check/uncheck bộ lọc {name}"),
                                  _state(c, l) + ("" if l else f" — check: bộ lọc {name} hiển thị trên vùng điều kiện; uncheck: bộ lọc ẩn và giá trị bị loại khỏi điều kiện tìm kiếm (assumption Q29)"),
                                  CAO if l else TB)])
            for name, c, l in FILTERS
        ]),
    ]
    return rows


def m1_rows():
    rows = [section(UI_SECTION)]
    rows += group_a("MH-001 Danh sách hồ sơ pháp lý", [C1], M1_DISPLAY, M1_TAB,
                    "Focus ô điều kiện và nhấn Enter → kích hoạt Tìm kiếm; focus nút → thực hiện chức năng của nút")
    rows += [tc("phím tắt thao tác", "Phím tắt theo Quy tắc component", "F5; Ctrl+Shift+E; Ctrl+P",
                steps(C1S, "Nhấn lần lượt F5, Ctrl+Shift+E, Ctrl+P"),
                "F5 làm mới trang; Ctrl+Shift+E mở lựa chọn Xuất Excel; Ctrl+P mở In trang hiện tại", THAP)]
    rows += title_rows("Danh sách hồ sơ pháp lý", C1)
    rows += screen_buttons(C1, "Cấu hình hiển thị, Xuất Excel, Thêm bộ lọc, Làm mới, Tìm kiếm, Xử lý hồ sơ, Bỏ chọn", "Tìm kiếm")
    rows += display_config_rows()
    rows += [
        subsection("Kiểm tra button Xuất Excel"),
        tc("xuất trang hiện tại", "Kiểm tra xuất trang hiện tại", "Trang 2, 20 bản ghi/trang",
           steps(C1S, "Sang trang 2", "Click Xuất Excel → Xuất trang hiện tại"), "Tệp chỉ chứa đúng 20 bản ghi của trang 2 (BR-022)", CAO),
        tc("xuất theo bộ lọc", "Kiểm tra xuất theo bộ lọc", "987 bản ghi thỏa bộ lọc",
           steps(C1S, "Click Xuất Excel → Xuất theo bộ lọc"),
           "Tệp chứa đủ 987 bản ghi của mọi trang; gồm mọi trường có thể chọn trong Cấu hình hiển thị (kể cả cột đang ẩn), không gồm cột Thao tác (BR-022, assumption Q28)", CAO),
        tc("tên file xuất", "Kiểm tra tên tệp", "Thực hiện ngày 12/10/2026", steps(C1S, "Xuất Excel"),
           "Tên tệp HoSoPhapLy_12102026.xlsx theo ngày thực hiện (BR-022 — SRS ưu tiên hơn quy tắc tên tệp chung)", CAO),
        tc("xuất khi dữ liệu rất lớn", "Kiểm tra xuất > 1.000.000 dòng", "Bộ lọc trả > 1.000.000 bản ghi",
           steps(C1S, "Xuất theo bộ lọc"), "Hệ thống xuất tệp .zip gồm nhiều tệp .xlsx, mỗi tệp tối đa 1.000.000 dòng (Quy tắc component)", TB),
        tc("xuất khi không có dữ liệu", "Kiểm tra xuất khi bộ lọc rỗng", "Điều kiện không khớp bản ghi",
           steps("Tìm kiếm điều kiện không khớp", "Xuất theo bộ lọc"), "Tệp chỉ có hàng tiêu đề (assumption Q28)", TB),
        tc("xuất khi API lỗi", "Kiểm tra lỗi API khi xuất", "Giả lập API lỗi / time out",
           steps(C1S, "Xuất theo bộ lọc"), "Hiển thị \"Lỗi hệ thống\" hoặc \"Yêu cầu này mất quá nhiều thời gian để phản hồi\"; không tải tệp lỗi", TB),
        tc("xuất khi hết phiên đăng nhập", "Kiểm tra token hết hạn", "Token hết hạn", steps(C1S, "Chờ token hết hạn", "Xuất Excel"),
           "Điều hướng về trang đăng nhập", TB),
    ]
    rows += button("Xuất trang hiện tại", f"{C1S}, click Xuất Excel", "Lựa chọn \"Xuất trang hiện tại\" hiển thị trong menu Xuất Excel",
                   "Luôn enable", "Tải tệp chứa bản ghi của trang hiện tại", TB)
    rows += button("Xuất theo bộ lọc", f"{C1S}, click Xuất Excel", "Lựa chọn \"Xuất theo bộ lọc\" hiển thị trong menu Xuất Excel",
                   "Luôn enable", "Tải tệp chứa mọi bản ghi thỏa bộ lọc đang áp dụng", TB)
    rows += button("In trang hiện tại", f"{C1S}, click Xuất Excel", "Lựa chọn \"In trang hiện tại\" hiển thị trong menu Xuất Excel",
                   "Luôn enable", "Hiển thị màn xem trước bản in của trang hiện tại theo cột đang hiển thị, in ra máy in mặc định (BR-022, assumption Q28)", TB)
    rows += add_filter_rows()
    rows += button("Làm mới", C1, "Nút/icon \"Làm mới\" cạnh nút Tìm kiếm", "Luôn enable",
                   "Xóa mọi điều kiện, trả về điều kiện như khi mở màn lần đầu (Cá nhân, D10, Mã đầu mối trống); lưới về trạng thái \"Chưa có dữ liệu. Vui lòng chọn tiêu chí tìm kiếm.\" (assumption Q20)", CAO)
    rows += button("Tìm kiếm", C1, "Nút \"Tìm kiếm\" là Primary button của vùng điều kiện", "Luôn enable",
                   "Kiểm tra 3 điều kiện bắt buộc và khoảng ngày, hiển thị kết quả sắp theo Ngày cập nhật giảm dần, 20 bản ghi/trang (BR-013, BR-018, BR-020)", CAO)
    rows += button("Xử lý hồ sơ (dải thao tác hàng loạt)", f"{C1S}, tick 1 hồ sơ Chờ xem xét",
                   "Nút \"Xử lý hồ sơ\" trên dải thao tác hàng loạt, bên phải \"Đã chọn n hồ sơ\"",
                   "Chỉ hiển thị khi có ≥ 1 hồ sơ được chọn (BR-026)",
                   "1 hồ sơ D10/D11 → MH-004; 1 hồ sơ Q11 → MH-005; ≥ 2 hồ sơ → MH-008 (BR-026)")
    rows += button("Bỏ chọn", f"{C1S}, tick 2 hồ sơ Chờ xem xét", "Nút \"Bỏ chọn\" trên dải thao tác hàng loạt",
                   "Chỉ hiển thị khi có ≥ 1 hồ sơ được chọn", "Bỏ chọn mọi hồ sơ, dải thao tác và banner INF_009 ẩn (BR-025, BR-026)", TB)
    # Filters
    rows += dropdown("Loại khách hàng", C1, "Mặc định \"Cá nhân\" (BR-013)", "Không áp dụng — luôn có giá trị mặc định",
                     "Có dấu (*); bắt buộc chọn đúng một giá trị (BR-013)", "Đúng 2 option: Cá nhân, Tổ chức", n_opts=2, locked_required=True)
    rows += dropdown("Mã đầu mối", C1, "Trống", "Hiển thị placeholder \"Mã đầu mối\"",
                     "Có dấu (*); thiếu thì Tìm kiếm báo WAR_009 (BR-013)",
                     "Chỉ gồm đầu mối được đánh dấu gửi báo cáo trong NV-16 VÀ thuộc TCTD được phân quyền (BR-014, Q21); hiển thị mã - tên",
                     searchable=True, search_hits=("3135", DM_IN))
    rows += dropdown("Mã tệp", C1, "Mặc định tệp đầu tiên trong danh sách được phân quyền = D10 (BR-013, assumption Q20)",
                     "Không áp dụng — luôn có giá trị mặc định", "Có dấu (*); bắt buộc chọn đúng một giá trị",
                     "Đúng 3 option: D10, D11, Q11", n_opts=3, locked_required=True)
    rows += multiselect("Mã CIC", f"{C1}, chọn Mã đầu mối = {DM_IN}", "Hiển thị placeholder \"Mã CIC\"",
                        "Chỉ gồm Mã CIC thuộc Loại khách hàng và Mã đầu mối đã chọn (BR-015)", "Sắp xếp theo giá trị (A-Z)",
                        searchable=True, search_hits=("2312", "CIC#231289"))
    rows += multiselect("Tên tệp", f"{C1}, bật bộ lọc Tên tệp trong Thêm bộ lọc, chọn Mã đầu mối = {DM_IN}", "Hiển thị placeholder \"Tên tệp\"",
                        "Chỉ gồm tên tệp tương ứng Mã tệp và Mã đầu mối đã chọn (assumption Q22)", "Sắp xếp theo tên tệp (A-Z)",
                        searchable=True, search_hits=("D11_", "D11_TPBANK_15092025.001.JSON"))
    rows += multiselect("Mã khách hàng", f"{C1}, chọn Mã đầu mối = {DM_IN}", "Hiển thị placeholder \"Mã khách hàng\"",
                        "Chỉ gồm TTC03 thuộc Loại khách hàng và Mã đầu mối đã chọn (BR-015)", "Sắp xếp theo mã (A-Z)",
                        searchable=True, search_hits=("CIF00001234", "CIF0000123456"), exact_only=True)
    rows += multiselect("Nhóm khách hàng", C1, "Hiển thị placeholder \"Nhóm khách hàng\"",
                        "Đúng 4 option: Mới - Có QHTD, Mới - Không QHTD, Thay đổi TTQT, Không thay đổi TTQT (BR-016)",
                        "Đúng thứ tự như SRS", n_opts=4)
    rows += multiselect("Trạng thái", C1, "Hiển thị placeholder \"Trạng thái\"",
                        "Đúng 4 option: Chờ cấp mã, Chờ xem xét, Đã xử lý, Từ chối", "Đúng thứ tự như SRS", n_opts=4)
    rows += multiselect("Người cập nhật", C1, "Hiển thị placeholder \"Người cập nhật\"",
                        "Gồm cán bộ CIC có trong hệ thống và \"Hệ thống (Sys)\" (assumption Q22)", "Sắp xếp theo username (A-Z)",
                        searchable=True, search_hits=("cbxl", "cbxl01"))
    rows += multiselect("CCCD/CMND", f"{C1}, bật bộ lọc CCCD/CMND, chọn Mã đầu mối = {DM_IN}", "Hiển thị placeholder \"CCCD/CMND\"",
                        "Loại KH = Cá nhân → giá trị CN008; Tổ chức → giá trị TC011 (BR-017, assumption Q25)", "Sắp xếp theo giá trị (A-Z)",
                        searchable=True, search_hits=("0603000", "060300012345"))
    rows += date_range("Từ ngày cập nhật - Đến ngày cập nhật", C1S, "cặp ngày cập nhật")
    rows += date_range("Từ ngày báo cáo - Đến ngày báo cáo", C1S, "cặp ngày báo cáo")
    # Selection
    rows += checkbox("Chọn tất cả", C1S, {
        "default": "Chưa chọn",
        "check": "Chọn mọi dòng Chờ xem xét đang hiển thị (bỏ qua dòng bị khóa); dải thao tác hiển thị \"Đã chọn n hồ sơ\" (BR-024, assumption Q19)",
        "uncheck": "Bỏ chọn mọi dòng; dải thao tác và banner ẩn",
        "more": [
            ("trạng thái chọn một phần", "Bỏ chọn 1 dòng khi đang chọn tất cả", "", steps(C1S, "Tick Chọn tất cả", "Bỏ tick 1 dòng"),
             "Ô Chọn tất cả chuyển trạng thái chọn một phần (indeterminate) — BR-024", CAO),
            ("chọn tất cả khi trang không có hồ sơ chờ xem xét", "Trang chỉ có hồ sơ Đã xử lý/Từ chối/Chờ cấp mã", "Lọc Trạng thái = Đã xử lý",
             steps(C1S, "Lọc Trạng thái = Đã xử lý", "Quan sát ô Chọn tất cả"), "Ô Chọn tất cả bị khóa (assumption Q19)", TB),
        ]})
    rows += checkbox("Chọn bản ghi", C1S, {
        "default": "Chưa chọn; chỉ bật với hồ sơ Chờ xem xét, khóa với Chờ cấp mã / Đã xử lý / Từ chối (BR-024)",
        "check": "Dòng được đánh dấu; dải thao tác hiển thị \"Đã chọn 1 hồ sơ\"; banner INF_009 hiển thị (BR-025, BR-026)",
        "uncheck": "Bỏ chọn; khi không còn hồ sơ nào được chọn, dải thao tác và banner ẩn",
        "more": [
            ("ô chọn của hồ sơ không ở trạng thái chờ xem xét", "Tick hồ sơ Chờ cấp mã / Đã xử lý / Từ chối", "3 hồ sơ ở 3 trạng thái",
             steps(C1S, "Click ô chọn của từng hồ sơ"), "Ô chọn bị khóa, không tick được (BR-024)", CAO),
            ("giữ lựa chọn khi đổi trang hoặc tìm kiếm lại", "Lựa chọn sau khi đổi trang / Tìm kiếm", "", steps(C1S, "Tick 2 hồ sơ", "Sang trang 2 hoặc click Tìm kiếm"),
             "Lựa chọn bị xóa; dải thao tác ẩn (assumption Q19)", TB),
            ("tích chọn nhiều bản ghi", "Tích chọn > 1 bản ghi", "3 hồ sơ Chờ xem xét", steps(C1S, "Tick lần lượt 3 hồ sơ Chờ xem xét"),
             "Các hồ sơ Chờ xem xét ở trang hiện tại được tích chọn; dải hiển thị \"Đã chọn 3 hồ sơ\"", CAO),
            ("bỏ tích chọn nhiều bản ghi", "Bỏ tích > 1 bản ghi", "Đang chọn 3 hồ sơ", steps(C1S, "Tick 3 hồ sơ", "Bỏ tick 2 hồ sơ"),
             "2 hồ sơ được bỏ chọn; dải hiển thị \"Đã chọn 1 hồ sơ\"", TB),
        ]})
    rows += [
        subsection("Kiểm tra banner chọn cùng loại khách hàng"),
        tc("hiển thị banner khi chọn hồ sơ cá nhân", "Chọn hồ sơ KH cá nhân đầu tiên", "Loại KH = Cá nhân", steps(C1S, "Tick 1 hồ sơ Chờ xem xét"),
           "Banner INF_009 \"Bạn đang chọn hồ sơ khách hàng cá nhân, chỉ có thể chọn hồ sơ cùng loại cá nhân để xử lý.\" (BR-025)", CAO),
        tc("hiển thị banner khi chọn hồ sơ tổ chức", "Chọn hồ sơ KH tổ chức đầu tiên", "Loại KH = Tổ chức",
           steps("Tìm kiếm Loại KH = Tổ chức", "Tick 1 hồ sơ Chờ xem xét"),
           "Banner INF_009 \"Bạn đang chọn hồ sơ khách hàng tổ chức, chỉ có thể chọn hồ sơ cùng loại tổ chức để xử lý.\"", CAO),
        tc("tắt banner khi bỏ chọn hết", "Bỏ chọn mọi hồ sơ", "", steps(C1S, "Tick 2 hồ sơ", "Bỏ tick cả 2 (hoặc click Bỏ chọn)"),
           "Banner INF_009 tắt (BR-025)", TB),
    ]
    rows += [
        subsection("Kiểm tra dải thao tác hàng loạt"),
        tc("ẩn dải khi chưa chọn hồ sơ", "Trạng thái mặc định của dải", "", steps(C1S, "Quan sát phía trên lưới"),
           "Không hiển thị dải thao tác hàng loạt (BR-026, AC#5)", CAO),
        tc("số hồ sơ đã chọn", "Nhãn \"Đã chọn n hồ sơ\"", "Chọn 1, 2, 5 hồ sơ", steps(C1S, "Tick lần lượt 1, 2, 5 hồ sơ"),
           "Nhãn cập nhật đúng \"Đã chọn 1 hồ sơ\", \"Đã chọn 2 hồ sơ\", \"Đã chọn 5 hồ sơ\"", TB),
    ]
    rows += paging(C1S, "MH-001")
    for name, disp, align, filt in COLS_M1:
        rows += grid_column(name, C1S, disp, align, filterable=filt)
    rows += [
        subsection("Kiểm tra cột Thao tác"),
        tc("hiển thị", "Kiểm tra hiển thị nút ... tại cột Thao tác", "", steps(C1S, "Kiểm tra hiển thị cột Thao tác"),
           "Mỗi dòng hiển thị nút \"...\" mở menu thao tác gồm: Xem, Xử lý hồ sơ (chỉ hồ sơ Chờ xem xét); cột cố định khi cuộn ngang (BR-023)", TB),
        tc("trạng thái", "Kiểm tra trạng thái nút ...", "", steps(C1S, "Kiểm tra trạng thái nút ... ở các dòng"), "Trạng thái: Enable ở mọi dòng", TB),
        tc("khi onclick", "Kiểm tra click nút ...", "", steps(C1S, "Click nút ... của một dòng"),
           "Mở menu thao tác của dòng đó: Xem; Xử lý hồ sơ (nếu Chờ xem xét); click ra ngoài thì menu đóng", CAO),
    ]
    rows += grid_action("Xem", C1S, "Mục \"Xem\" hiển thị trong menu Thao tác của mọi dòng",
                        "Hiển thị ở cả 4 trạng thái Chờ cấp mã, Chờ xem xét, Đã xử lý, Từ chối (BR-023)",
                        "Hồ sơ D10/D11 → mở MH-002; hồ sơ Q11 → mở MH-003")
    rows += grid_action("Xử lý hồ sơ", C1S, "Mục \"Xử lý hồ sơ\" hiển thị trong menu Thao tác của hồ sơ Chờ xem xét",
                        "Chỉ hiển thị khi hồ sơ Chờ xem xét; ẩn với Chờ cấp mã, Đã xử lý, Từ chối (BR-023, AC#3)",
                        "Hồ sơ D10/D11 → mở MH-004; hồ sơ Q11 → mở MH-005")
    rows += [
        subsection("Kiểm tra badge trạng thái"),
        tc("vị trí và màu sắc badge", "Màu và nhãn theo trạng thái", "4 hồ sơ ở 4 trạng thái", steps(C1S, "Quan sát cột Trạng thái"),
           "Chờ cấp mã: chấm xám; Chờ xem xét: chấm cam; Đã xử lý: chấm xanh lá; Từ chối: chấm đỏ, chữ đỏ", TB),
        tc("tính chỉ đọc của badge", "Click vào badge", "", steps(C1S, "Click badge trạng thái"),
           "Không đổi trạng thái, không mở thao tác nào", THAP),
    ]

    # ─── CHỨC NĂNG ───
    base = f"LOAI_KH = 'Cá nhân' AND MA_DAU_MOI = '{DM_IN}' AND MA_TEP = 'D11'"
    rows += [section(BIZ_SECTION), subsection("Kiểm tra tìm kiếm thành công có dữ liệu")]
    # (label, data có dữ liệu, where có dữ liệu, data không có dữ liệu, where không có dữ liệu)
    single = [
        ("chỉ ba điều kiện bắt buộc", f"Loại KH = Cá nhân, Mã đầu mối = {DM_IN}, Mã tệp = D11", base,
         f"Loại KH = Cá nhân, Mã đầu mối = {DM_IN2}, Mã tệp = Q11 (đầu mối chưa có hồ sơ Q11 cá nhân)",
         f"LOAI_KH = 'Cá nhân' AND MA_DAU_MOI = '{DM_IN2}' AND MA_TEP = 'Q11'"),
        ("loại khách hàng tổ chức", f"Loại KH = Tổ chức, {DM_IN}, D11", f"LOAI_KH = 'Tổ chức' AND MA_DAU_MOI = '{DM_IN}' AND MA_TEP = 'D11'",
         f"Loại KH = Tổ chức, {DM_IN2}, D10 (chưa có hồ sơ tổ chức D10)", f"LOAI_KH = 'Tổ chức' AND MA_DAU_MOI = '{DM_IN2}' AND MA_TEP = 'D10'"),
        ("mã tệp Q11", f"Cá nhân, {DM_IN}, Q11", f"LOAI_KH = 'Cá nhân' AND MA_DAU_MOI = '{DM_IN}' AND MA_TEP = 'Q11'",
         f"Cá nhân, {DM_IN2}, Q11 (chưa có hồ sơ Q11)", f"LOAI_KH = 'Cá nhân' AND MA_DAU_MOI = '{DM_IN2}' AND MA_TEP = 'Q11'"),
        ("mã CIC", "+ Mã CIC = CIC#231289", base + " AND MA_CIC IN ('CIC#231289')",
         "+ Mã CIC = CIC#564456 (chỉ có hồ sơ tệp D10, không có hồ sơ D11)", base + " AND MA_CIC IN ('CIC#564456')"),
        ("mã khách hàng khớp chính xác", "+ Mã KH = CIF0000123456, CIF0000123457", base + " AND MA_KH IN ('CIF0000123456','CIF0000123457')",
         "+ Mã KH = CIF0000123460 (chỉ có hồ sơ tệp D10)", base + " AND MA_KH IN ('CIF0000123460')"),
        ("nhóm khách hàng thay đổi thông tin quan trọng", "+ Nhóm KH = Thay đổi TTQT (UC-0547)", base + " AND NHOM_KH IN ('Thay đổi TTQT')",
         "+ Nhóm KH = Thay đổi TTQT trên tệp chưa có hồ sơ thay đổi TTQT", base + " AND NHOM_KH IN ('Thay đổi TTQT')"),
        ("nhóm khách hàng mới không quan hệ tín dụng", "+ Nhóm KH = Mới - Không QHTD (UC-0541)", base + " AND NHOM_KH IN ('Mới - Không QHTD')",
         "+ Nhóm KH = Mới - Không QHTD trên tệp chỉ có khách hàng cũ", base + " AND NHOM_KH IN ('Mới - Không QHTD')"),
        ("trạng thái", "+ Trạng thái = Chờ xem xét, Từ chối", base + " AND TRANG_THAI IN ('Chờ xem xét','Từ chối')",
         "+ Trạng thái = Từ chối trên tệp chưa có hồ sơ bị từ chối", base + " AND TRANG_THAI IN ('Từ chối')"),
        ("người cập nhật", "+ Người cập nhật = Sys", base + " AND NGUOI_CAP_NHAT IN ('Sys')",
         "+ Người cập nhật = cbxl03 (chưa cập nhật hồ sơ nào)", base + " AND NGUOI_CAP_NHAT IN ('cbxl03')"),
        ("tên tệp", "+ Tên tệp = D11_TPBANK_15092025.001.JSON", base + " AND TEN_TEP IN ('D11_TPBANK_15092025.001.JSON')",
         "+ Tên tệp chỉ chứa hồ sơ tổ chức (khi Loại KH = Cá nhân)", base + " AND TEN_TEP IN ('<tệp chỉ có hồ sơ tổ chức>')"),
        ("CCCD/CMND", "+ CCCD/CMND = 060300012345", base + " AND CN008 IN ('060300012345')",
         "+ CCCD/CMND = 060300099999 (khách hàng thuộc tệp D10)", base + " AND CN008 IN ('060300099999')"),
        ("khoảng ngày cập nhật", "+ Ngày cập nhật 01/09/2025 → 30/09/2025", base + " AND TRUNC(NGAY_CAP_NHAT) BETWEEN '01/09/2025' AND '30/09/2025'",
         "+ Ngày cập nhật 01/01/2020 → 31/01/2020 (chưa có hồ sơ)", base + " AND TRUNC(NGAY_CAP_NHAT) BETWEEN '01/01/2020' AND '31/01/2020'"),
        ("khoảng ngày báo cáo", "+ Ngày báo cáo 30/08/2025 → 30/08/2025", base + " AND NGAY_BAO_CAO BETWEEN '30/08/2025' AND '30/08/2025'",
         "+ Ngày báo cáo 01/01/2020 → 31/01/2020 (chưa có kỳ báo cáo)", base + " AND NGAY_BAO_CAO BETWEEN '01/01/2020' AND '31/01/2020'"),
    ]
    for label, data, where, _nd, _nw in single:
        rows.append(tc(f"tìm kiếm theo {label}", f"Tìm kiếm theo {label} — có dữ liệu", data,
                       steps(C1, f"Chọn điều kiện: {data}", "Click Tìm kiếm"),
                       "Danh sách chỉ gồm hồ sơ thỏa điều kiện, sắp theo Ngày cập nhật mới nhất trên cùng, 20 bản ghi/trang; "
                       "phân trang hiển thị đúng tổng số bản ghi (BR-002, BR-020, BR-027)" + sql(where), CAO))
    rows += [
        tc("tìm kiếm kết hợp hai điều kiện bổ sung", "AND giữa các bộ lọc — có dữ liệu", "+ Nhóm KH = Thay đổi TTQT + Trạng thái = Chờ xem xét",
           steps(C1, "Chọn 3 điều kiện bắt buộc", "Chọn Nhóm KH và Trạng thái", "Click Tìm kiếm"),
           "Kết quả thỏa đồng thời cả hai điều kiện (AND); trong một bộ lọc chọn nhiều là OR (assumption Q23)"
           + sql(base + " AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Chờ xem xét')"), CAO),
        tc("tìm kiếm kết hợp ba điều kiện bổ sung", "Leo thang điều kiện — có dữ liệu", "+ Nhóm KH + Trạng thái + Mã CIC",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 3 điều kiện bổ sung", "Click Tìm kiếm"), "Kết quả thỏa đồng thời mọi điều kiện"
           + sql(base + " AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Chờ xem xét') AND MA_CIC IN ('CIC#231345')"), CAO),
        tc("tìm kiếm kết hợp năm điều kiện bổ sung", "Leo thang điều kiện — có dữ liệu", "+ Mã CIC + Mã KH + Nhóm KH + Trạng thái + Ngày báo cáo",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 5 điều kiện bổ sung", "Click Tìm kiếm"), "Kết quả thỏa đồng thời mọi điều kiện"
           + sql(base + " AND MA_CIC IN ('CIC#231345') AND MA_KH IN ('CIF0000123462') AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Chờ xem xét') AND NGAY_BAO_CAO = '30/08/2025'"), CAO),
        tc("tìm kiếm kết hợp sáu điều kiện bổ sung", "Leo thang điều kiện — có dữ liệu", "+ Mã CIC + Mã KH + Nhóm KH + Trạng thái + Người cập nhật + Ngày báo cáo",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 6 điều kiện bổ sung", "Click Tìm kiếm"), "Kết quả thỏa đồng thời mọi điều kiện"
           + sql(base + " AND MA_CIC IN ('CIC#231345') AND MA_KH IN ('CIF0000123462') AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Chờ xem xét') AND NGUOI_CAP_NHAT IN ('Sys') AND NGAY_BAO_CAO = '30/08/2025'"), CAO),
        tc("tìm kiếm kết hợp bốn điều kiện bổ sung", "Leo thang điều kiện", "+ Mã CIC + Nhóm KH + Trạng thái + Ngày báo cáo",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 4 điều kiện bổ sung", "Click Tìm kiếm"), "Kết quả thu hẹp, thỏa đồng thời mọi điều kiện"
           + sql(base + " AND MA_CIC IN ('CIC#231345') AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Chờ xem xét') AND NGAY_BAO_CAO = '30/08/2025'"), CAO),
        tc("tìm kiếm kết hợp tất cả điều kiện", "Mọi điều kiện (bật cả Tên tệp, CCCD/CMND)", "Mọi bộ lọc có giá trị khớp 1 hồ sơ",
           steps(C1, "Bật mọi bộ lọc trong Thêm bộ lọc", "Chọn giá trị cho mọi điều kiện", "Click Tìm kiếm"),
           "Chỉ trả về hồ sơ thỏa đồng thời toàn bộ điều kiện" + sql(base + " AND <mọi điều kiện bổ sung>"), CAO),
        tc("sắp xếp mặc định", "Thứ tự kết quả", "Hồ sơ có Ngày cập nhật khác nhau", steps(C1S, "Bật cột Ngày cập nhật"),
           "Ngày cập nhật mới nhất nằm trên cùng (BR-020)", CAO),
        tc("phạm vi dữ liệu danh sách", "Chỉ hồ sơ pháp lý hợp lệ", "Kho có hồ sơ loại khác Pháp lý, hồ sơ không Hợp lệ, tệp D01",
           steps(C1S), "Không hiển thị hồ sơ khác loại Pháp lý, không Hợp lệ, hoặc không thuộc D10/D11/Q11 (BR-002)" + sql(base), CAO),
        tc("đổi tiêu đề cột CCCD/MSDN theo loại khách hàng", "Tiêu đề cột sau Tìm kiếm", "Cá nhân rồi Tổ chức",
           steps(C1S, "Đổi Loại KH = Tổ chức, chưa Tìm kiếm", "Click Tìm kiếm"),
           "Trước Tìm kiếm tiêu đề vẫn \"CCCD\"; sau Tìm kiếm tiêu đề \"MSDN\", dữ liệu TC011 (BR-017, assumption Q23)", CAO),
        subsection("Kiểm tra tìm kiếm thành công không có dữ liệu"),
    ]
    nodata = ("Tìm kiếm thực hiện thành công (không có lỗi validate); toast INF_003 \"Không tìm thấy bản ghi phù hợp.\"; "
              "lưới hiển thị empty state \"Không tìm thấy bản ghi phù hợp.\" kèm icon; phân trang \"0 - 0 trên tổng số 0 bản ghi\"; "
              "không hiển thị dải thao tác hàng loạt và banner (EXC-03, assumption Q30)")
    for label, _d, _w, data, where in single:
        rows.append(tc(f"tìm kiếm theo {label} không có dữ liệu", f"Tìm kiếm theo {label} — không có dữ liệu", data,
                       steps(C1, f"Chọn điều kiện: {data}", "Click Tìm kiếm"), nodata + sql(where + " -- 0 bản ghi"), CAO))
    rows += [
        tc("tìm kiếm kết hợp nhiều điều kiện không có dữ liệu", "Mỗi điều kiện riêng có dữ liệu nhưng tổ hợp không có",
           "+ Mã CIC = CIC#231289 + Trạng thái = Từ chối (KH này không có hồ sơ bị từ chối)",
           steps(C1, "Chọn 3 điều kiện bắt buộc, Mã CIC và Trạng thái", "Click Tìm kiếm"),
           nodata + sql(base + " AND MA_CIC IN ('CIC#231289') AND TRANG_THAI IN ('Từ chối') -- 0 bản ghi"), CAO),
        tc("tìm kiếm kết hợp ba điều kiện không có dữ liệu", "Leo thang 3 điều kiện bổ sung — không có dữ liệu", "+ Mã CIC + Nhóm KH = Mới - Có QHTD + Trạng thái = Từ chối",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 3 điều kiện bổ sung", "Click Tìm kiếm"),
           nodata + sql(base + " AND MA_CIC IN ('CIC#231289') AND NHOM_KH IN ('Mới - Có QHTD') AND TRANG_THAI IN ('Từ chối') -- 0 bản ghi"), CAO),
        tc("tìm kiếm kết hợp bốn điều kiện không có dữ liệu", "Leo thang 4 điều kiện bổ sung — không có dữ liệu", "+ Mã CIC + Mã KH + Nhóm KH + Trạng thái (tổ hợp không tồn tại)",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 4 điều kiện bổ sung", "Click Tìm kiếm"),
           nodata + sql(base + " AND MA_CIC IN ('CIC#231289') AND MA_KH IN ('CIF0000123462') AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Từ chối') -- 0 bản ghi"), CAO),
        tc("tìm kiếm kết hợp năm điều kiện không có dữ liệu", "Leo thang 5 điều kiện bổ sung — không có dữ liệu", "+ 4 điều kiện trên + Ngày báo cáo 01/01/2020 → 31/01/2020",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 5 điều kiện bổ sung", "Click Tìm kiếm"),
           nodata + sql(base + " AND MA_CIC IN ('CIC#231289') AND MA_KH IN ('CIF0000123462') AND NHOM_KH IN ('Thay đổi TTQT') AND TRANG_THAI IN ('Từ chối') AND NGAY_BAO_CAO BETWEEN '01/01/2020' AND '31/01/2020' -- 0 bản ghi"), CAO),
        tc("tìm kiếm kết hợp sáu điều kiện không có dữ liệu", "Leo thang 6 điều kiện bổ sung — không có dữ liệu", "+ 5 điều kiện trên + Người cập nhật = cbxl03",
           steps(C1, "Chọn 3 điều kiện bắt buộc và 6 điều kiện bổ sung", "Click Tìm kiếm"),
           nodata + sql(base + " AND <5 điều kiện trên> AND NGUOI_CAP_NHAT IN ('cbxl03') -- 0 bản ghi"), CAO),
        tc("xuất Excel khi tìm kiếm không có dữ liệu", "Xuất theo bộ lọc khi kết quả rỗng", "Kết quả tìm kiếm 0 bản ghi",
           steps(C1, "Tìm kiếm điều kiện không có dữ liệu", "Click Xuất Excel → Xuất theo bộ lọc"),
           "Tệp HoSoPhapLy_ddmmyyyy chỉ có hàng tiêu đề (assumption Q28)", TB),
        tc("tìm kiếm lại sau khi không có dữ liệu", "Chuyển từ kết quả rỗng sang có dữ liệu", "",
           steps(C1, "Tìm kiếm điều kiện không có dữ liệu", f"Đổi Mã đầu mối = {DM_IN}, Mã tệp = D11", "Click Tìm kiếm"),
           "Empty state biến mất; lưới hiển thị dữ liệu trang 1, phân trang hiển thị lại", TB),
        subsection("Kiểm tra xuất file Excel thành công"),
        tc("xuất trang hiện tại thành công", "Xuất trang hiện tại", "Trang 1, 20 bản ghi", steps(C1S, "Click Xuất Excel", "Chọn Xuất trang hiện tại"),
           "Xuất các bản ghi của trang hiện tại ra tệp HoSoPhapLy_ddmmyyyy.xlsx; các trường là mọi trường có thể chọn trong Cấu hình hiển thị:\n"
           + EXPORT_FIELDS + "\nDữ liệu từng dòng khớp lưới (BR-022, assumption Q28)", CAO),
        tc("xuất theo bộ lọc thành công", "Xuất theo bộ lọc", "987 bản ghi thỏa bộ lọc", steps(C1S, "Click Xuất Excel", "Chọn Xuất theo bộ lọc"),
           "Xuất mọi bản ghi của mọi trang theo bộ lọc đang áp dụng; các trường:\n" + EXPORT_FIELDS + "\nSố dòng = tổng số bản ghi tìm được (BR-022)"
           + sql(base), CAO),
        tc("in trang hiện tại thành công", "In trang hiện tại", "", steps(C1S, "Click Xuất Excel", "Chọn In trang hiện tại"),
           "Hiển thị màn hình xem trước bản in các bản ghi của trang hiện tại; cho phép chọn in từ giao diện xem trước ra máy in mặc định của thiết bị (BR-022)", CAO),
        subsection("Kiểm tra thao tác trên danh sách thành công"),
        tc("xóa mã đầu mối đã chọn", "Phụ thuộc khi xóa Mã đầu mối", f"Đã chọn Mã đầu mối {DM_IN}, Mã CIC, Mã KH",
           steps(C1, f"Chọn Mã đầu mối {DM_IN}, chọn Mã CIC và Mã KH", "Xóa Mã đầu mối", "Mở Mã CIC, Mã KH"),
           "Giá trị Mã CIC, Mã KH, Tên tệp, CCCD/CMND đã chọn bị xóa; danh sách option của các bộ lọc này rỗng cho tới khi chọn lại Mã đầu mối (BR-015, assumption Q22)", CAO),
        tc("làm mới sau khi tìm kiếm", "Click Làm mới khi đang có kết quả", "", steps(C1S, "Click Làm mới"),
           "Điều kiện trở về mặc định; lưới hiển thị \"Chưa có dữ liệu. Vui lòng chọn tiêu chí tìm kiếm.\" (assumption Q20)", TB),
        tc("lọc lại danh sách mã CIC, mã khách hàng khi đổi điều kiện cha", "Phụ thuộc bộ lọc", f"Đổi Mã đầu mối {DM_IN} → {DM_IN2}",
           steps(C1, f"Chọn Mã đầu mối {DM_IN}, chọn 2 Mã KH", f"Đổi Mã đầu mối = {DM_IN2}", "Mở Mã KH, Mã CIC"),
           f"Giá trị Mã KH đã chọn bị xóa; option Mã CIC, Mã KH chỉ còn của {DM_IN2} (BR-015, assumption Q22)", CAO),
        tc("thêm bộ lọc", "Bật / tắt bộ lọc bổ sung", "Bật Tên tệp, CCCD/CMND; tắt Người cập nhật",
           steps(C1, "Click Thêm bộ lọc", "Bật Tên tệp, CCCD/CMND; tắt Người cập nhật đang có giá trị", "Click Tìm kiếm"),
           "Tên tệp, CCCD/CMND hiển thị; Người cập nhật ẩn và giá trị bị loại khỏi điều kiện; 3 bộ lọc bắt buộc không tắt được (BR-019, assumption Q29)", CAO),
        tc("cấu hình hiển thị", "Ẩn/hiện, kéo thả, áp dụng, lưu", "Bật Mã tệp, Loại KH; ẩn Địa chỉ; kéo Mã CIC lên đầu",
           steps(C1S, "Mở Cấu hình hiển thị", "Thực hiện thay đổi", "Click Áp dụng", "Nhấn F5"),
           "Lưới hiển thị đúng cấu hình; 4 cột bắt buộc (Ngày báo cáo, Mã đầu mối, Mã KH, Thao tác) không bỏ chọn được; cấu hình giữ sau F5 trên cùng máy (BR-021, assumption Q29)", CAO),
        tc("menu thao tác theo trạng thái", "Bảng quyết định trạng thái × mục menu", "4 hồ sơ: Chờ cấp mã, Chờ xem xét, Đã xử lý, Từ chối",
           steps(C1S, "Mở menu Thao tác từng dòng"), "Chỉ hồ sơ Chờ xem xét có \"Xử lý hồ sơ\"; mọi hồ sơ có \"Xem\" (BR-023)", CAO),
        tc("xử lý một hồ sơ từ dải thao tác", "N = 1", "1 hồ sơ D11 Chờ xem xét", steps(C1S, "Tick 1 hồ sơ", "Click Xử lý hồ sơ trên dải"),
           "Mở MH-004 của hồ sơ đó (BR-026)", CAO),
        tc("xử lý một hồ sơ tệp Q11 từ dải thao tác", "N = 1, tệp Q11", "1 hồ sơ Q11 Chờ xem xét",
           steps("Tìm kiếm Mã tệp = Q11", "Tick 1 hồ sơ", "Click Xử lý hồ sơ"), "Mở MH-005 (BR-026)", CAO),
        tc("xử lý đồng thời từ dải thao tác", "N ≥ 2", "2 hồ sơ D11 Chờ xem xét", steps(C1S, "Tick 2 hồ sơ", "Click Xử lý hồ sơ"),
           "Mở MH-008 với 2 hồ sơ đã chọn (BR-026)", CAO),
        tc("trạng thái danh sách sau khi xử lý và quay về", "Quay về MH-001 sau Cập nhật thành công", "Đang ở trang 3",
           steps(C1S, "Sang trang 3", "Xử lý 1 hồ sơ, Cập nhật thành công"),
           "Quay về MH-001 giữ bộ lọc và trang 3; danh sách tải lại, hồ sơ hiển thị Đã xử lý; lựa chọn bị xóa (assumption Q33)", CAO),
        subsection("Kiểm tra tìm kiếm không thành công"),
        tc("tìm kiếm khi thiếu mã đầu mối", "Thiếu điều kiện bắt buộc", "Mã đầu mối trống", steps(C1, "Click Tìm kiếm"),
           "Toast WAR_009 \"Vui lòng chọn Loại khách hàng, Mã đầu mối, Mã tệp để tìm kiếm.\"; lưới giữ trạng thái chưa có dữ liệu (BR-013, AC#1)", CAO),
        tc("mở màn hình chưa truy vấn dữ liệu", "Trạng thái khi chưa đủ điều kiện", "", steps(C1),
           "Không truy vấn dữ liệu; lưới hiển thị \"Chưa có dữ liệu. Vui lòng chọn tiêu chí tìm kiếm.\" (BR-013)", CAO),
        tc("từ ngày cập nhật lớn hơn đến ngày cập nhật", "Khoảng ngày sai", "Từ 10/09/2025, Đến 09/09/2025", steps(C1S, "Chọn khoảng ngày", "Click Tìm kiếm"),
           "ERR_003 \"Từ ngày phải nhỏ hơn hoặc bằng Đến ngày.\"; giữ nguyên điều kiện, không tìm kiếm (BR-018, AC#2)", CAO),
        tc("từ ngày báo cáo lớn hơn đến ngày báo cáo", "Khoảng ngày sai", "Từ 31/08/2025, Đến 30/08/2025", steps(C1S, "Chọn khoảng ngày", "Click Tìm kiếm"),
           "ERR_003 tại cặp ngày báo cáo; không tìm kiếm", CAO),
        tc("tìm kiếm khi API lỗi", "Tra cứu thất bại — API lỗi", "Giả lập API tìm kiếm trả lỗi 500 / mất kết nối",
           steps(C1, "Chọn điều kiện tìm kiếm", "Click Tìm kiếm"),
           "Hệ thống hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; lưới không hiển thị dữ liệu sai, giữ nguyên điều kiện tìm kiếm (theo mẫu common1)", CAO),
        tc("tìm kiếm khi API timeout", "Tra cứu thất bại — API timeout", "Giả lập API tìm kiếm phản hồi quá thời gian chờ",
           steps(C1, "Chọn điều kiện tìm kiếm", "Click Tìm kiếm"),
           "Hiển thị loading trong thời gian chờ; hết thời gian hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; UI không bị treo (theo mẫu common1)", CAO),
        tc("tìm kiếm khi hết phiên đăng nhập", "Hết token đăng nhập", "Token phiên đăng nhập hết hạn",
           steps(C1, "Chọn điều kiện tìm kiếm", "Chờ token hết hạn", "Click Tìm kiếm"),
           "Hết token đăng nhập, hệ thống điều hướng về màn hình đăng nhập (Login)", CAO),
        subsection("Kiểm tra phân quyền"),
        tc("người dùng được phân quyền chức năng", "NSD có ROLE-CBTTXLDL", ACC_MAIN, steps("Đăng nhập", "Mở menu Xử lý dữ liệu"),
           "Thấy menu Hồ sơ pháp lý; truy cập và thao tác được MH-001", CAO),
        tc("người dùng không được phân quyền chức năng", "NSD không có quyền", ACC_NO_ROLE, steps("Đăng nhập", "Mở menu Xử lý dữ liệu"),
           "Không hiển thị menu Hồ sơ pháp lý (BR-001)", CAO),
        tc("truy cập trực tiếp bằng đường dẫn khi không có quyền", "URL trực tiếp", ACC_NO_ROLE, steps("Đăng nhập", "Dán URL của MH-001 vào trình duyệt"),
           "Toast ERR_011 \"Người dùng không được phân quyền.\"; không hiển thị dữ liệu, ở lại trang (Q38)", CAO),
        tc("người dùng có vai trò nhưng chưa được phân quyền TCTD", "ROLE + 0 TCTD", ACC_NO_TCTD, steps("Đăng nhập", "Mở MH-001", "Mở Mã đầu mối"),
           "Menu hiển thị; danh sách Mã đầu mối rỗng, không tra cứu được dữ liệu (Q38)", CAO),
        tc("gợi ý mã đầu mối chỉ thuộc TCTD được phân quyền", "Phạm vi dữ liệu Mã đầu mối", f"Gõ '{DM_OUT}'", steps(C1, f"Gõ '{DM_OUT}' vào Mã đầu mối"),
           f"Không có gợi ý {DM_OUT}; chỉ gợi ý {DM_IN}, {DM_IN2} (BR-014, Q21)", CAO),
        tc("chỉ thấy hồ sơ của TCTD được phân quyền", "Phạm vi dữ liệu tra cứu và xuất", f"cbxl02 chỉ có {DM_IN}",
           steps("Đăng nhập cbxl02", "Tìm kiếm", "Xuất theo bộ lọc"),
           f"Danh sách và tệp xuất chỉ chứa hồ sơ của {DM_IN} (Ma trận phân quyền, Q21)", CAO),
    ]
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# Indicator sets (from P2/P3 component tables; processing screens exclude KB)
# ══════════════════════════════════════════════════════════════════════════════
def _codes(prefix, start, end, skip=()):
    return [f"{prefix}{i:03d}" for i in range(start, end + 1) if i not in skip]


IND_D10 = {
    "kb": ["KB001", "KB002", "KB003", "KB004"],
    "Tổ chức": [
        ("Thông tin định danh", ["TTC03", "TTC04"]),
        ("Thông tin chung", _codes("TC", 1, 10)),
        ("Thông tin pháp lý", _codes("TC", 11, 16)),
        ("Loại hình & ngành nghề", ["TC017", "TC018"]),
        ("Tổng giám đốc/Giám đốc", ["TC019", "TC020", "TC021"]),
        ("Thông tin thành viên", ["TC022", "TC023"]),
    ],
    "Cá nhân": [
        ("Thông tin định danh", ["TTC03", "TTC04"]),
        ("Thông tin chung", _codes("CN", 1, 7)),
        ("Thông tin pháp lý", _codes("CN", 8, 15)),
        ("Thông tin vợ/chồng", ["CN016", "CN017"]),
        ("Thông tin nghề nghiệp và thu nhập", _codes("CN", 18, 21)),
        ("Thông tin thành viên", ["CN022"]),
    ],
    "tables": [
        ("TC024 Vốn điều lệ", "Vốn điều lệ", "TC0241, TC0242", "TC0241"),
        ("TC025 Thông tin người đại diện", "Người đại diện", "TC0251, TC0252, TC0253", "TC0252"),
        ("TC026 Thành viên HĐQT/HĐTV", "Thành viên", "TC0261, TC0262, TC0263", "TC0262"),
    ],
}
IND_Q11 = {
    "kb": ["KB001"],
    "Tổ chức": [
        ("Thông tin định danh", ["TTC03", "TTC04"]),
        ("Thông tin chung", ["TC004", "TC005", "TC006", "TC007"]),
        ("Thông tin pháp lý", ["TC011", "TC012", "TC013", "TC015"]),
        ("Loại hình & ngành nghề", ["TC017", "TC018"]),
        ("Tổng giám đốc/Giám đốc", ["TC019", "TC020", "TC021"]),
        ("Thông tin thành viên", ["TC022"]),
    ],
    "Cá nhân": [
        ("Thông tin định danh", ["TTC03", "TTC04"]),
        ("Thông tin chung", _codes("CN", 1, 7)),
        ("Thông tin pháp lý", ["CN008", "CN009", "CN010", "CN011", "CN012", "CN014"]),
        ("Thông tin vợ/chồng", ["CN016", "CN017"]),
        ("Thông tin thành viên", ["CN022"]),
    ],
    "tables": [],
}


# ══════════════════════════════════════════════════════════════════════════════
# M2 / M3 — Xem chi tiết hồ sơ pháp lý (MH-002 D10/D11, MH-003 Q11)
# ══════════════════════════════════════════════════════════════════════════════
def per_indicator_group(group, codes, ctx):
    """GAP-04 — one TC per indicator for traceability (code, stored value, tooltip, read-only)."""
    return tc_group(f"Kiểm tra hiển thị từng chỉ tiêu nhóm {group}", [
        tc_sub(f"Chỉ tiêu {code}", [tc_item(code, steps(ctx, f"Quan sát dòng {code}", f"Hover vào mã {code}"),
                                            f"Hiển thị mã {code} và giá trị đang lưu tại CSDL; tooltip đúng tên chỉ tiêu {code} theo danh mục chỉ tiêu; "
                                            "chỉ đọc (BR-028, BR-030)", TB)])
        for code in codes
    ])


def detail_rows(v):
    """v: dict(code, tep, ind, ctx, ctx_org) — builds a whole detail sheet."""
    ind, code, ctx, ctx_org = v["ind"], v["code"], v["ctx"], v["ctx_org"]
    hist_ctx = f"{ctx}, chọn tab Lịch sử cập nhật"
    display = (f"Popup {code} hiển thị:\n- 2 tab: Thông tin hồ sơ (đang chọn), Lịch sử cập nhật\n"
               "- Thẻ: Tên khách hàng, Đầu mối báo cáo, Mã khách hàng, Loại khách hàng, Nhóm khách hàng, Mã CIC, Trạng thái (badge), "
               "Lý do (khi Đã xử lý/Từ chối), Tên tệp\n"
               f"- Nhóm Thông tin khai báo chung: {', '.join(ind['kb'])}\n- Các nhóm chỉ tiêu theo Loại khách hàng\n- Nút Đóng")
    rows = [section(UI_SECTION)]
    rows += group_a(f"popup {code}", [ctx], display, "Tab Thông tin hồ sơ → Tab Lịch sử cập nhật → vùng nội dung → nút Đóng",
                    "Focus nút Đóng và nhấn Enter → đóng popup; focus tab và nhấn Enter → chuyển tab")
    rows += title_rows("Xem chi tiết hồ sơ pháp lý", ctx)
    rows += [
        subsection("Kiểm tra Tabs"),
        tc("tab mặc định", "Tab mở sẵn khi vào màn", "", steps(ctx), "Tab Thông tin hồ sơ được chọn mặc định (BR-028, AC#1)", CAO),
        tc("chuyển sang tab lịch sử cập nhật", "Click tab Lịch sử cập nhật", "", steps(ctx, "Click tab Lịch sử cập nhật"),
           "Hiển thị bảng lịch sử của khách hàng; tab được highlight", CAO),
        tc("quay lại tab thông tin hồ sơ", "Click lại tab Thông tin hồ sơ", "", steps(hist_ctx, "Click tab Thông tin hồ sơ"),
           "Hiển thị lại thông tin hồ sơ, không tải lại popup (ALT-01)", TB),
        tc("chuyển tab bằng bàn phím", "Ctrl+Tab / Ctrl+Shift+Tab", "", steps(ctx, "Nhấn Ctrl+Tab", "Nhấn Ctrl+Shift+Tab"),
           "Chuyển qua lại giữa 2 tab (Quy tắc component)", THAP),
    ]
    card = [("Tên khách hàng", "TTC04"), ("Đầu mối báo cáo", "TTC00, hiển thị mã - tên (assumption Q37)"),
            ("Mã khách hàng", "TTC03"), ("Loại khách hàng", "Cá nhân hoặc Tổ chức"),
            ("Nhóm khách hàng", "Một trong 4 nhóm (BR-016)"), ("Mã CIC", "Mã CIC nếu có; trống khi Chờ cấp mã"),
            ("Tên tệp", "Giá trị đang lưu tại CSDL")]
    rows.append(subsection("Kiểm tra thẻ thông tin hồ sơ"))
    for name, desc in card:
        rows.append(tc(f"hiển thị trường {name.lower()}", f"Hiển thị {name}", "", steps(ctx, f"Quan sát {name}"),
                       f"Hiển thị nhãn \"{name}\" và giá trị: {desc}; chỉ đọc", TB))
    rows.append(tc_group("Kiểm tra hiển thị Lý do theo trạng thái", [
        tc_sub("Hồ sơ Đã xử lý do cán bộ cập nhật", [tc_item("Lý do 'Đã đối chiếu với đơn vị'", steps(ctx), "Hiển thị Lý do đang lưu (BR-029)", CAO)]),
        tc_sub("Hồ sơ Từ chối", [tc_item("Lý do 'Sai số CCCD'", steps(ctx), "Hiển thị Lý do từ chối đang lưu (BR-029)", CAO)]),
        tc_sub("Hồ sơ Chờ xem xét", [tc_item("", steps(ctx), "Không hiển thị trường Lý do (BR-029, AC#2)", CAO)]),
        tc_sub("Hồ sơ Chờ cấp mã", [tc_item("", steps(ctx), "Không hiển thị trường Lý do (BR-029)", CAO)]),
    ]))
    rows += [
        subsection("Kiểm tra badge trạng thái"),
        tc("vị trí và màu sắc badge", "Badge trạng thái trên thẻ", "4 hồ sơ ở 4 trạng thái", steps(ctx),
           "Màu nhãn cùng tông với cột Trạng thái ở MH-001 (xám/cam/xanh lá/đỏ)", TB),
        tc("tính chỉ đọc của badge", "Click vào badge", "", steps(ctx, "Click badge"), "Không đổi trạng thái", THAP),
    ]
    rows.append(subsection("Kiểm tra nhóm Thông tin khai báo chung"))
    rows.append(tc("hiển thị chỉ tiêu khai báo chung", "Mã và giá trị các chỉ tiêu KB", ", ".join(ind["kb"]), steps(ctx, "Quan sát nhóm Thông tin khai báo chung"),
                   f"Hiển thị đủ {', '.join(ind['kb'])} với giá trị đang lưu tại CSDL (BR-028)", CAO))
    rows.append(per_indicator_group("Thông tin khai báo chung", ind["kb"], ctx))
    for kh, cctx in (("Tổ chức", ctx_org), ("Cá nhân", ctx)):
        rows.append(subsection(f"Kiểm tra nhóm chỉ tiêu khách hàng {kh.lower()}"))
        for grp, codes in ind[kh]:
            rows.append(tc(f"hiển thị nhóm {grp.lower()}", f"Nhóm \"{grp}\"", ", ".join(codes), steps(cctx, f"Quan sát nhóm {grp}"),
                           f"Hiển thị tiêu đề nhóm \"{grp}\" và đủ {len(codes)} chỉ tiêu {', '.join(codes)}: mã chỉ tiêu + giá trị đang lưu; chỉ đọc (BR-028, BR-030)", CAO))
            rows.append(per_indicator_group(f"{grp} ({kh.lower()})", codes, cctx))
        rows.append(tc("tooltip tên chỉ tiêu", "Di chuột vào mã chỉ tiêu", ind[kh][1][1][0], steps(cctx, f"Hover vào mã {ind[kh][1][1][0]}"),
                       "Hiển thị tooltip tên chỉ tiêu lấy từ danh mục chỉ tiêu (BR-030)", TB))
    if ind["tables"]:
        rows.append(subsection("Kiểm tra khối lặp vốn điều lệ, người đại diện, HĐQT/HĐTV"))
        for name, block, subs, _key in ind["tables"]:
            rows.append(tc_group(f"Kiểm tra hiển thị {name}", [
                tc_sub("Không có bản ghi", [tc_item("0 bản ghi", steps(ctx_org, f"Quan sát {name}"),
                                                    "Chỉ hiển thị tiêu đề nhóm, không có dòng dữ liệu (assumption Q37)", TB)]),
                tc_sub("Có 1 bản ghi", [tc_item("1 bản ghi", steps(ctx_org, f"Quan sát {name}"),
                                                f"Hiển thị khối \"{block} 1\" gồm {subs} với giá trị đang lưu", CAO)]),
                tc_sub("Có nhiều bản ghi", [tc_item("3 bản ghi", steps(ctx_org, f"Quan sát {name}"),
                                                    f"Hiển thị \"{block} 1\", \"{block} 2\", \"{block} 3\" trải xuống dưới, mỗi khối đủ {subs}", CAO)]),
            ]))
            rows.append(per_indicator_group(name, subs.split(", "), ctx_org))
    rows.append(subsection("Kiểm tra bảng Lịch sử cập nhật"))
    hist_cols = [
        ("STT", "Số thứ tự dòng lịch sử", "Căn giữa"),
        ("Thời gian", "Định dạng DD/MM/YYYY HH:MM:SS", "Căn giữa"),
        ("Người cập nhật", "Tên tài khoản hoặc \"Sys\"; hover hiển thị tên đầy đủ và tên viết tắt phòng ban (BR-031)", "Căn trái"),
        ("Hành động", "Một trong: Tiếp nhận, Cập nhật tự động, Cấp mã CIC, Cập nhật, Từ chối (BR-031)", "Căn trái"),
        ("Giá trị cũ", "Chỉ các trường có thay đổi, mỗi trường một dòng (BR-031)", "Căn trái"),
        ("Giá trị mới", "Giá trị sau thay đổi, chỉ các trường có thay đổi, mỗi trường một dòng", "Căn trái"),
        ("Địa chỉ IP", "IP thiết bị của tài khoản tại thời điểm thao tác; trống với hành động Hệ thống (assumption Q36)", "Căn trái"),
        ("Mô tả", "Mô tả / lý do của hành động; > 2 dòng hiển thị \"...\" kèm nút \"Xem tiếp\" (Quy tắc component)", "Căn trái"),
    ]
    for name, disp, align in hist_cols:
        rows += grid_column(name, hist_ctx, disp, align, filterable=False)
    rows += [
        tc("sắp xếp và cuộn bảng lịch sử", "Thứ tự và cuộn", "KH có 12 dòng lịch sử", steps(hist_ctx),
           "Mới nhất trên cùng; bảng cuộn dọc, không phân trang (Quy tắc component, assumption Q36)", TB),
        tc("bảng lịch sử rỗng", "Không có dòng lịch sử", "Xóa dữ liệu lịch sử trên môi trường test", steps(hist_ctx),
           "Hiển thị empty state CMP-033 (EXC-01)", THAP),
    ]
    rows += button("Đóng", ctx, f"Nút \"Đóng\" ở cuối popup {code}", "Luôn enable", "Đóng popup, trở về MH-001 giữ nguyên bộ lọc và trang", TB)

    # ─── CHỨC NĂNG ───
    rows += [section(BIZ_SECTION), subsection("Kiểm tra xem chi tiết thành công")]
    for st in ("Chờ cấp mã", "Chờ xem xét", "Đã xử lý", "Từ chối"):
        rows.append(tc(f"mở xem chi tiết hồ sơ {st.lower()}", f"Xem hồ sơ {v['tep']} trạng thái {st}", f"Hồ sơ {v['tep']} – {st}",
                       steps(f"Tìm kiếm hồ sơ tệp {v['tep']} trạng thái {st}", "Menu Thao tác → Xem"),
                       f"Mở {code} ở tab Thông tin hồ sơ; mọi giá trị đúng giá trị đang lưu tại CSDL (BR-028)"
                       + sql(f"MA_KH = '<mã KH>' AND MA_DAU_MOI = '{DM_IN}' AND TRANG_THAI = '{st}'"), CAO))
    rows += [
        tc("mở đúng màn hình theo loại tệp", "Phân luồng màn xem theo tệp", "Hồ sơ D10, D11, Q11",
           steps("Xem lần lượt hồ sơ D10, D11, Q11"), "D10 và D11 mở MH-002; Q11 mở MH-003 (Luồng màn hình)", CAO),
        tc("khách hàng tổ chức chỉ hiển thị nhóm chỉ tiêu tổ chức", "Tập chỉ tiêu theo Loại KH = Tổ chức", "Hồ sơ Tổ chức", steps(ctx_org),
           v["org_ac"], CAO),
        tc("khách hàng cá nhân chỉ hiển thị nhóm chỉ tiêu cá nhân", "Tập chỉ tiêu theo Loại KH = Cá nhân", "Hồ sơ Cá nhân", steps(ctx),
           v["ind_ac"], CAO),
        tc("giá trị hiển thị là giá trị đang lưu", "Đối chiếu với CSDL", "Hồ sơ đã được cán bộ Cập nhật",
           steps(ctx, "Đối chiếu từng chỉ tiêu với CSDL"), "Mọi giá trị khớp giá trị đang lưu của hồ sơ tại CSDL (BR-028)"
           + sql("MA_KH = '<mã KH>' AND MA_DAU_MOI = '31358001' AND NGAY_BAO_CAO = '<ngày>'", "MA_TEP"), CAO),
        subsection("Kiểm tra lịch sử cập nhật"),
        tc("lịch sử theo khách hàng qua nhiều kỳ báo cáo", "Phạm vi lịch sử TTC00 + TTC03", f"KH CIF0000123462 có hồ sơ kỳ 30/06 và 30/08 của {DM_IN}; KH cùng TTC03 nhưng đầu mối {DM_IN2}",
           steps(hist_ctx), f"Hiển thị dòng lịch sử của cả 2 kỳ của cặp {DM_IN} + CIF0000123462; không hiển thị lịch sử của {DM_IN2} (BR-031)", CAO),
        tc_group("Kiểm tra nội dung dòng lịch sử theo hành động", [
            tc_sub("Tiếp nhận", [tc_item("Hồ sơ mới tiếp nhận", steps(hist_ctx),
                                         "Dòng \"Tiếp nhận\", Người cập nhật Sys; mọi hồ sơ có ít nhất dòng này (BR-031, assumption Q36)", CAO)]),
            tc_sub("Cập nhật tự động", [tc_item("Hồ sơ Không thay đổi TTQT", steps(hist_ctx),
                                                "Dòng \"Cập nhật tự động\", Sys; Giá trị cũ/mới chỉ gồm trường không quan trọng có thay đổi", CAO)]),
            tc_sub("Cấp mã CIC", [tc_item("Hồ sơ đã được cấp mã", steps(hist_ctx), "Dòng \"Cấp mã CIC\", Sys; Giá trị mới là Mã CIC được cấp", CAO)]),
            tc_sub("Cập nhật", [tc_item("Hồ sơ cán bộ cbxl01 Cập nhật", steps(hist_ctx),
                                        "Dòng \"Cập nhật\", cbxl01, IP thiết bị; Giá trị cũ/mới các trường thay đổi; Mô tả = lý do", CAO)]),
            tc_sub("Từ chối", [tc_item("Hồ sơ cbxl01 Từ chối", steps(hist_ctx),
                                       "Dòng \"Từ chối\", cbxl01; Giá trị cũ/mới trống; Mô tả = lý do từ chối (assumption Q36)", CAO)]),
        ]),
        tc("chỉ hiển thị trường có thay đổi", "Giá trị cũ / Giá trị mới", "Cập nhật đổi CN003 và CN009", steps(hist_ctx),
           "Giá trị cũ / mới chỉ có 2 dòng CN003, CN009, mỗi trường một dòng (BR-031, AC#4)", CAO),
        tc("tooltip người cập nhật", "Hover Người cập nhật", "cbxl01", steps(hist_ctx, "Hover vào cbxl01"),
           "Tooltip gồm tên đầy đủ và tên viết tắt phòng ban của tài khoản (BR-031)", TB),
        subsection("Kiểm tra xem chi tiết không thành công"),
        tc("xem chi tiết khi API lỗi", "Xem chi tiết thất bại — API lỗi", "Giả lập API lấy chi tiết hồ sơ trả lỗi 500 / mất kết nối",
           steps(v["open"], "Click Xem"),
           "Hệ thống hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; popup không hiển thị dữ liệu sai/trống lẫn dữ liệu cũ; "
           "ở lại danh sách, giữ bộ lọc (theo mẫu common1)", CAO),
        tc("xem chi tiết khi API timeout", "Xem chi tiết thất bại — API timeout", "Giả lập API lấy chi tiết phản hồi quá thời gian chờ",
           steps(v["open"], "Click Xem"),
           "Hiển thị loading trong thời gian chờ; hết thời gian hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; giao diện không bị treo (theo mẫu common1)", CAO),
        tc("xem chi tiết khi hết phiên đăng nhập", "Hết token đăng nhập", "Token hết hạn trước khi click Xem",
           steps(v["open"], "Chờ token hết hạn", "Click Xem"),
           "Hết token đăng nhập, hệ thống điều hướng về màn hình đăng nhập (Login)", CAO),
        tc("xem chi tiết khi bị thu hồi quyền giữa chừng", "Quyền bị thu hồi khi đang ở danh sách", "Quản trị thu hồi quyền chức năng của cbxl01",
           steps(v["open"], "Thu hồi quyền của cbxl01", "Click Xem"),
           "Thao tác bị chặn, toast ERR_011 \"Người dùng không được phân quyền.\"; không hiển thị dữ liệu hồ sơ (Q38)", CAO),
        subsection("Kiểm tra xem lịch sử thay đổi không thành công"),
        tc("xem lịch sử khi API lỗi", "Xem lịch sử thất bại — API lỗi", "Giả lập API lấy lịch sử trả lỗi 500 / mất kết nối",
           steps(ctx, "Click tab Lịch sử cập nhật"),
           "Hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; bảng lịch sử không hiển thị dữ liệu sai; vẫn quay lại được tab Thông tin hồ sơ (theo mẫu common1)", CAO),
        tc("xem lịch sử khi API timeout", "Xem lịch sử thất bại — API timeout", "Giả lập API lấy lịch sử phản hồi quá thời gian chờ",
           steps(ctx, "Click tab Lịch sử cập nhật"),
           "Hiển thị loading trong bảng lịch sử; hết thời gian hiển thị thông báo \"Đã có lỗi xảy ra. Vui lòng thử lại.\"; popup không bị treo, nút Đóng vẫn dùng được", CAO),
        tc("xem lịch sử khi hết phiên đăng nhập", "Hết token khi chuyển tab", "Token hết hạn trong lúc đang mở popup",
           steps(ctx, "Chờ token hết hạn", "Click tab Lịch sử cập nhật"),
           "Hết token đăng nhập, hệ thống điều hướng về màn hình đăng nhập (Login)", CAO),
        tc("xem lịch sử khi bị thu hồi quyền giữa chừng", "Quyền bị thu hồi khi đang mở popup", "Quản trị thu hồi quyền chức năng của cbxl01",
           steps(ctx, "Thu hồi quyền của cbxl01", "Click tab Lịch sử cập nhật"),
           "Thao tác bị chặn, toast ERR_011; không hiển thị dữ liệu lịch sử (Q38)", CAO),
        subsection("Kiểm tra phân quyền"),
        tc("xem hồ sơ thuộc TCTD được phân quyền", "NSD được phân quyền", ACC_MAIN, steps(ctx), f"Mở được {code} (Ma trận phân quyền)", CAO),
        tc("xem hồ sơ ngoài TCTD được phân quyền qua đường dẫn", "Truy cập trực tiếp", f"cbxl02 mở URL xem hồ sơ của {DM_IN2}",
           steps("Đăng nhập cbxl02", f"Dán URL xem chi tiết hồ sơ của {DM_IN2}"),
           "Toast ERR_011, không hiển thị dữ liệu (Q38)", CAO),
    ]
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# M4 / M5 / M7 — Xử lý hồ sơ (MH-004, MH-005, MH-008) + popups MH-006 / MH-007
# ══════════════════════════════════════════════════════════════════════════════
def popup_rows(code, kind, open_ctx, bulk):
    """MH-006 (kind='update') or MH-007 (kind='reject') — group A, CONF text, Lý do (G), controls."""
    upd = kind == "update"
    label = "Cập nhật" if upd else "Từ chối"
    action = "cập nhật" if upd else "từ chối cập nhật"
    ctx = f"{open_ctx}, click nút {label}{' (n)' if bulk else ''} để mở {code}"
    who = "mọi hồ sơ còn được chọn" if bulk else "hồ sơ"
    effect = (f"Popup và màn xử lý đóng; {who} chuyển Đã xử lý, lưu lý do, ghi thông tin pháp lý vào kho TCTD theo Mã CIC; "
              "toast SUC_001 \"Cập nhật thông tin thành công.\"; quay về MH-001 (BR-040" + (", BR-044)" if bulk else ")")
              if upd else
              f"Popup và màn xử lý đóng; {who} chuyển Từ chối, lưu lý do, kho TCTD giữ nguyên; quay về MH-001 (BR-041" + (", BR-044)" if bulk else ")"))
    rows = [subsection(f"Kiểm tra popup {code}")]
    rows += group_a(f"popup {code}", [ctx],
                    f"Popup tiêu đề \"Xác nhận thông tin hồ sơ\", icon X, câu xác nhận CONF_001, nhãn \"Lý do\" (*), ô Lý do, bộ đếm \"0/1000 ký tự\", nút Hủy và {label}",
                    f"Ô Lý do → nút Hủy → nút {label} → icon X", f"Focus nút {label} và nhấn Enter → thực hiện xác nhận; trong ô Lý do Enter xuống dòng",
                    qt_extra=False)[1:]
    rows.append(tc("câu xác nhận", f"Nội dung CONF_001 trên {code}", "", steps(ctx),
                   f"Hiển thị \"Bạn có chắc chắn muốn {action} thông tin pháp lý quan trọng của khách hàng không?\" (CONF_001, assumption Q31)", CAO))
    rows += textarea(f"Lý do ({code})", [ctx], code, label)
    rows += confirm_popup_controls(code, ctx, label, effect)
    return rows


def process_rows(v):
    """v keys: code, tep, ind, ctx, ctx_org, bulk, tables, toggle_on, sheet_tag."""
    code, ctx, ctx_org, bulk, ind = v["code"], v["ctx"], v["ctx_org"], v["bulk"], v["ind"]
    n_lbl = " (n)" if bulk else ""
    rows = [section(UI_SECTION)]
    display = (f"{'Màn hình' if bulk else 'Popup'} {code} hiển thị:\n"
               + ("- Vùng trái \"Hồ sơ đã chọn (n)\", dòng phụ \"Tệp <mã> · Khách hàng <loại>\", danh sách hồ sơ có ô chọn\n" if bulk else "")
               + "- Thẻ hồ sơ đang xem xét: Tên KH, Mã khách hàng, Loại khách hàng, Đầu mối báo cáo, Ngày báo cáo, Trạng thái\n"
               "- Thẻ Hồ sơ tại CIC: Mã CIC, Loại khách hàng, TCTD có liên quan\n"
               "- Dòng \"So sánh thông tin chỉ tiêu\": tóm tắt số khác biệt, chú thích ★ / ô tô nền, công tắc \"Chỉ hiện chỉ tiêu khác biệt\" "
               f"({'bật' if v['toggle_on'] else 'tắt'})\n"
               "- Bảng 3 cột giá trị: Hồ sơ đang xem xét / Hồ sơ khách hàng tại TCTD (ô chọn Ngày báo cáo) / Hồ sơ khách hàng tại CIC (nhãn C06)\n"
               f"- Nút Hủy, Từ chối{n_lbl}, Cập nhật{n_lbl}")
    rows += group_a(code, [ctx], display,
                    ("Danh sách hồ sơ đã chọn → " if bulk else "") + "công tắc → ô chọn Ngày báo cáo → bảng → Hủy → Từ chối → Cập nhật",
                    "Focus nút và nhấn Enter → thực hiện chức năng của nút")
    rows += screen_buttons(ctx, f"Hủy, Từ chối{n_lbl}, Cập nhật{n_lbl}", f"Cập nhật{n_lbl}")
    rows += title_rows("Xử lý đồng thời hồ sơ pháp lý" if bulk else "Xử lý hồ sơ pháp lý", ctx)
    if bulk:
        rows += [
            subsection("Kiểm tra danh sách hồ sơ đã chọn"),
            tc("tiêu đề và dòng phụ", "Tiêu đề vùng danh sách", "8 hồ sơ D11 cá nhân", steps(ctx),
               "Tiêu đề \"Hồ sơ đã chọn (8)\", dòng phụ \"Tệp D11 · Khách hàng cá nhân\" (assumption Q34)", TB),
            tc("nội dung mỗi hồ sơ", "Thông tin trên từng dòng", "", steps(ctx),
               "Mỗi hồ sơ: ô chọn, Tên khách hàng, \"Mã KH ... · Đầu mối ...\", \"Mã CIC ...\", chip mã chỉ tiêu khác biệt (★ trước chỉ tiêu quan trọng) — BR-042", CAO),
            tc("thứ tự hồ sơ", "Thứ tự trong danh sách", "Chọn dòng 7 rồi dòng 3 trên MH-001", steps(ctx),
               "Thứ tự theo thứ tự trên MH-001 (dòng 3 trước dòng 7) — assumption Q34", TB),
            tc("hồ sơ đang xem mặc định", "Hồ sơ được xem khi mở trang", "", steps(ctx), "Hồ sơ đầu tiên được highlight và hiển thị ở vùng so sánh (BR-042, AC#1)", CAO),
            tc("cuộn danh sách", "Danh sách nhiều hồ sơ", "20 hồ sơ", steps(ctx, "Cuộn vùng danh sách"),
               "Danh sách cuộn dọc độc lập với vùng so sánh, footer nút không bị che (CMP-042)", TB),
            tc("chuyển hồ sơ đang xem", "Click một hồ sơ khác", "", steps(ctx, "Click hồ sơ thứ 3"),
               "Hồ sơ 3 được highlight; vùng so sánh chuyển sang hồ sơ 3 (thẻ, tóm tắt, bảng) — BR-042", CAO),
        ]
        rows += checkbox("Chọn hồ sơ", ctx, {
            "default": "Mọi hồ sơ trong danh sách đều được chọn (BR-042)",
            "check": "Hồ sơ hiển thị bình thường; số trên nút Từ chối (n), Cập nhật (n) tăng 1",
            "uncheck": "Hồ sơ hiển thị mờ, vẫn click xem được; số trên nút giảm 1 (BR-042, ALT-04)",
            "more": [("bỏ chọn tất cả hồ sơ", "n = 0", "Bỏ chọn cả 8 hồ sơ", steps(ctx, "Bỏ tick lần lượt 8 hồ sơ"),
                      "Nút Từ chối (0), Cập nhật (0) bị khóa (BR-042)", CAO)]})
    rows += [subsection("Kiểm tra thẻ hồ sơ đang xem xét")]
    for name, desc in [("Tên khách hàng", "TTC04 của hồ sơ đang xem xét"), ("Mã khách hàng", "TTC03, cùng dòng với Mã CIC ở thẻ phải (BR-047)"),
                       ("Loại khách hàng", "TTC05"), ("Đầu mối báo cáo", "TTC00 dạng mã - tên"),
                       ("Ngày báo cáo", "KB001, DD/MM/YYYY"), ("Trạng thái", "Badge \"Chờ xem xét\" màu cam")]:
        rows.append(tc(f"hiển thị {name.lower()}", f"Hiển thị {name}", "", steps(ctx, f"Quan sát {name}"), f"Hiển thị {desc}; chỉ đọc", TB))
    rows += [subsection("Kiểm tra thẻ Hồ sơ tại CIC")]
    rows += [
        tc("hiển thị mã CIC", "Mã CIC chỉ xem", "", steps(ctx, "Quan sát Mã CIC", "Thử click / sửa Mã CIC"),
           "Hiển thị Mã CIC của KH, không chọn được mã khác (MH-004 #7" + (", BR-043, assumption Q14)" if bulk else ")"), CAO),
        tc("hiển thị loại khách hàng tại CIC", "TTC05 tại kho chuẩn", "", steps(ctx), "Hiển thị TTC05 của hồ sơ tại kho chuẩn CIC (BR-047)", TB),
        tc("hiển thị TCTD có liên quan", "Danh sách mã TCTD", "KH được 3 TCTD báo cáo", steps(ctx),
           "Hiển thị mã các TCTD/CNTCTD còn hiệu lực ngăn cách bằng \";\" (BR-047, assumption Q15)", TB),
        tc("tooltip TCTD có liên quan", "Hover một mã TCTD", "68202001", steps(ctx, "Hover mã 68202001"),
           "Tooltip tên đầy đủ TCTD/CNTCTD lấy từ NV-16", TB),
        tc("thứ tự dòng hai thẻ", "Căn hàng giữa 2 thẻ", "", steps(ctx), "Hai thẻ cùng thứ tự dòng: mã, Loại khách hàng, Đầu mối báo cáo / TCTD có liên quan (BR-047)", THAP),
    ]
    rows += [
        subsection("Kiểm tra tóm tắt khác biệt"),
        tc("hiển thị tóm tắt và chú thích", "Dòng So sánh thông tin chỉ tiêu", "5 chỉ tiêu khác, 1 quan trọng", steps(ctx),
           "Hiển thị \"5 chỉ tiêu khác biệt, 1 chỉ tiêu quan trọng\", chú thích \"★ Chỉ tiêu quan trọng\", \"Dữ liệu thay đổi\" (BR-045, assumption Q10, Q42)", CAO),
    ]
    rows += checkbox("Chỉ hiện chỉ tiêu khác biệt (công tắc)", ctx, {
        "default": ("Bật (mặc định ở màn xử lý đồng thời — BR-045)" if v["toggle_on"] else "Tắt (mặc định ở màn xử lý một hồ sơ — BR-045)"),
        "check": "Bảng chỉ hiển thị dòng chỉ tiêu khác biệt và tiêu đề nhóm chứa chúng (BR-045, AC#6)",
        "uncheck": "Bảng hiển thị đủ mọi chỉ tiêu",
        "more": [("trạng thái loading của công tắc", "Công tắc khi đang xử lý", "Giả lập mạng chậm, hồ sơ nhiều chỉ tiêu",
                  steps(ctx, "Bật / tắt công tắc", "Click tiếp công tắc nhiều lần khi đang xử lý"),
                  "Công tắc hiển thị trạng thái loading và không nhận thao tác lặp cho tới khi bảng lọc xong (Quy tắc component — Switch; GAP-05)", TB)],
    })
    rows += dropdown("Ngày báo cáo (cột Hồ sơ khách hàng tại TCTD)", ctx, "Mặc định phiên bản mới nhất theo Ngày báo cáo (BR-032)",
                     "Không áp dụng — luôn có giá trị", "Không đánh dấu (*); luôn có một phiên bản được chọn",
                     "Tối đa 3 phiên bản mới nhất theo Ngày báo cáo, cùng Mã CIC và cùng đầu mối, không gồm chính hồ sơ đang xem xét (BR-032, Q03); định dạng DD/MM/YYYY",
                     n_opts=3, locked_required=True)
    for name, disp in [
        ("Chỉ tiêu", "Mã chỉ tiêu; ★ trước mã chỉ tiêu quan trọng; hover hiển thị tên chỉ tiêu; nhóm theo tiêu đề nhóm (BR-030, BR-035)"),
        ("Hồ sơ đang xem xét", "Giá trị chỉ tiêu của hồ sơ đang xem xét — mốc so sánh (BR-036)"),
        ("Hồ sơ khách hàng tại TCTD", "Giá trị theo phiên bản Ngày báo cáo đang chọn; ô khác mốc được tô nền (BR-032, BR-037)"),
        ("Hồ sơ khách hàng tại CIC", "Giá trị phiên bản duy nhất tại kho chuẩn CIC theo Mã CIC; ô khác mốc được tô nền; nhãn C06 cạnh tiêu đề khi đã xác thực (BR-033, BR-034)"),
    ]:
        rows += grid_column(name, ctx, disp, "Căn trái", filterable=False)
    rows += [
        subsection("Kiểm tra bảng so sánh"),
        tc("cố định hàng tiêu đề khi cuộn", "Cuộn bảng so sánh", "Hồ sơ đủ chỉ tiêu, công tắc tắt", steps(ctx, "Cuộn bảng xuống cuối"),
           "Hai thẻ và dòng tóm tắt cuộn khuất; hàng tiêu đề cột cùng ô chọn Ngày báo cáo giữ ở đầu vùng cuộn (BR-046, AC#7)", CAO),
        tc("nhãn C06", "Nhãn đã xác thực C06", "Hồ sơ CIC có cờ C06 / không có cờ", steps(ctx),
           "Có cờ: hiển thị nhãn \"C06\" cạnh tiêu đề cột CIC; không có cờ: không hiển thị (BR-034, assumption Q42)", CAO),
    ]
    rows += button("Hủy", ctx, f"Nút \"Hủy\" ở chân {code}", "Luôn enable",
                   "Đóng màn xử lý, về MH-001 giữ bộ lọc/trang; " + ("mọi hồ sơ" if bulk else "hồ sơ") + " vẫn Chờ xem xét (ALT-03, assumption Q33)", TB)
    rows += button(f"Từ chối{n_lbl}", ctx, "Nút \"Từ chối" + (" (8)\" ghi kèm số hồ sơ còn được chọn" if bulk else "\""),
                   "Khóa khi không còn hồ sơ nào được chọn (BR-042)" if bulk else "Luôn enable", "Mở popup MH-007 xác nhận từ chối")
    rows += button(f"Cập nhật{n_lbl}", ctx, "Nút \"Cập nhật" + (" (8)\" ghi kèm số hồ sơ còn được chọn, Primary" if bulk else "\" là Primary button"),
                   "Khóa khi không còn hồ sơ nào được chọn (BR-042)" if bulk else "Luôn enable", "Mở popup MH-006 xác nhận cập nhật")
    rows += popup_rows("MH-006", "update", ctx, bulk)
    rows += popup_rows("MH-007", "reject", ctx, bulk)

    # ─── CHỨC NĂNG ───
    rows += [section(BIZ_SECTION), subsection("Kiểm tra mở màn xử lý và hiển thị so sánh")]
    if bulk:
        rows += [
            tc("mở màn xử lý đồng thời với hai hồ sơ", "Biên dưới N = 2", "2 hồ sơ D11 cá nhân Chờ xem xét",
               steps("Tại MH-001 tick 2 hồ sơ", "Click Xử lý hồ sơ trên dải"), "Mở MH-008 với 2 hồ sơ, cả 2 được chọn, hồ sơ đầu tiên đang xem (BR-026, BR-042)", CAO),
            tc("mở màn xử lý đồng thời với nhiều hồ sơ", "N = 8", "8 hồ sơ", steps(ctx), "Danh sách đủ 8 hồ sơ; nút Từ chối (8), Cập nhật (8)", CAO),
            tc("chip chỉ tiêu khác biệt của từng hồ sơ", "Chip trong danh sách", "Hồ sơ khác CN003, CN004, CN009, ★CN010, CN020",
               steps(ctx), "Chip đúng 5 mã khác biệt, ★ trước CN010; khớp các dòng tô nền khi xem hồ sơ đó với phiên bản TCTD mặc định (BR-042, assumption Q10)", CAO),
            tc("đặt lại công tắc và phiên bản khi chuyển hồ sơ", "Trạng thái vùng so sánh khi chuyển", "",
               steps(ctx, "Tắt công tắc, đổi Ngày báo cáo ở hồ sơ 1", "Chuyển sang hồ sơ 2", "Quay lại hồ sơ 1"),
               "Mỗi lần chuyển hồ sơ: công tắc bật lại, Ngày báo cáo về phiên bản mới nhất (assumption Q34)", TB),
            tc("mã CIC của từng hồ sơ", "Cột CIC theo Mã CIC của hồ sơ", "Hồ sơ 1 CIC#83753223433A, hồ sơ 2 CIC#83753224108B",
               steps(ctx, "Xem lần lượt hồ sơ 1 và 2"), "Thẻ và cột CIC hiển thị đúng Mã CIC riêng của từng hồ sơ (BR-042, BR-043, AC#1)", CAO),
        ]
    else:
        rows += [
            tc("mở từ menu thao tác", "Mở màn xử lý từ menu Thao tác", f"Hồ sơ {v['tep']} Chờ xem xét",
               steps("Tại MH-001 mở menu Thao tác của hồ sơ", "Click Xử lý hồ sơ"), f"Mở {code} của đúng hồ sơ (Luồng chính bước 1)", CAO),
            tc("mở từ dải thao tác hàng loạt", "Mở khi chỉ chọn 1 hồ sơ", "", steps("Tick 1 hồ sơ", "Click Xử lý hồ sơ trên dải"), f"Mở {code} (BR-026)", CAO),
        ]
    rows += [
        tc("tập chỉ tiêu khách hàng cá nhân", "Dòng chỉ tiêu theo Loại KH = Cá nhân", "", steps(ctx, "Tắt công tắc"), v["ind_ac"], CAO),
        tc("tập chỉ tiêu khách hàng tổ chức", "Dòng chỉ tiêu theo Loại KH = Tổ chức", "", steps(ctx_org, "Tắt công tắc"), v["org_ac"], CAO),
        tc_group("Kiểm tra danh sách phiên bản cột Hồ sơ khách hàng tại TCTD", [
            tc_sub("Có 1 phiên bản", [tc_item("1 hồ sơ khác cùng Mã CIC và đầu mối", steps(ctx, "Mở ô Ngày báo cáo"), "Dropdown có 1 option, đang chọn (assumption Q35)", CAO)]),
            tc_sub("Có 3 phiên bản", [tc_item("30/06, 31/07, 31/08/2025", steps(ctx, "Mở ô Ngày báo cáo"), "Có đủ 3 option, mặc định 31/08/2025 (BR-032)", CAO)]),
            tc_sub("Có 4 phiên bản", [tc_item("31/05, 30/06, 31/07, 31/08/2025", steps(ctx, "Mở ô Ngày báo cáo"),
                                              "Chỉ có 3 option mới nhất 31/08, 31/07, 30/06; không có 31/05 (BR-032, AC#2)", CAO)]),
            tc_sub("Trùng Ngày báo cáo", [tc_item("2 phiên bản cùng 31/08/2025", steps(ctx, "Mở ô Ngày báo cáo"),
                                                  "Phiên bản có Ngày tạo mới nhất xếp trước (assumption Q35)", TB)]),
            tc_sub("Mọi Ngày báo cáo đều trống", [tc_item("3 phiên bản không có Ngày báo cáo", steps(ctx),
                                                          "Mặc định lấy hồ sơ có Ngày tạo mới nhất (BR-032)", CAO)]),
            tc_sub("Có hồ sơ của TCTD khác cùng Mã CIC", [tc_item(f"KH có hồ sơ của {DM_IN} và {DM_IN2}", steps(ctx, "Mở ô Ngày báo cáo"),
                                                                  f"Chỉ gồm hồ sơ của đầu mối {DM_IN} (cùng đầu mối hồ sơ đang xem xét), không gồm chính hồ sơ đang xem xét (Q03)", CAO)]),
        ]),
        tc("đổi phiên bản tại TCTD", "Chọn Ngày báo cáo khác", "31/08 → 30/06/2025", steps(ctx, "Chọn 30/06/2025"),
           "Cột TCTD nạp lại theo phiên bản 30/06; tô lại ô khác biệt; tóm tắt và công tắc tính lại (BR-032, BR-037, assumption Q10)", CAO),
        tc("cột hồ sơ tại CIC", "Nguồn cột CIC", "Mã CIC CIC#231345", steps(ctx),
           "Hiển thị giá trị phiên bản duy nhất tại kho chuẩn CIC theo Mã CIC (BR-033)" + sql("MA_CIC = 'CIC#231345'", "MA_CIC").replace("<HO_SO_PHAP_LY>", "<KHO_CHUAN_CICINFO>"), CAO),
        tc("so sánh độc lập hai cột", "Khác chỉ ở cột TCTD", "CN020: xem xét 8 năm, TCTD 6 năm, CIC 8 năm", steps(ctx),
           "Chỉ ô CN020 cột TCTD tô nền; ô cột CIC không tô (BR-036, BR-037)", CAO),
        tc("chỉ tô ô có giá trị khác", "Phạm vi tô nền", "CN003 khác ở cả 2 cột", steps(ctx),
           "Tô nền 2 ô cột TCTD và CIC của CN003; không tô cả dòng, không đổi màu chữ (BR-037, AC#1)", CAO),
        tc("biểu tượng chỉ tiêu quan trọng", "★ trước mã chỉ tiêu quan trọng", "CN010 được đánh dấu quan trọng ở FUNC-XLDL-027", steps(ctx),
           "★ hiển thị trước CN010 trong ô Chỉ tiêu; chỉ tiêu không quan trọng không có ★ (BR-035, BR-009)", CAO),
        tc("tooltip tên chỉ tiêu", "Hover mã chỉ tiêu", "CN009", steps(ctx, "Hover CN009"), "Tooltip tên chỉ tiêu (BR-030)", TB),
        tc_group("Kiểm tra quy tắc so sánh một giá trị", [
            tc_sub("Khoảng trắng đầu cuối", [tc_item("Xem xét '  Hà Nội ', TCTD 'Hà Nội'", steps(ctx), "Coi là giống, không tô nền (BR-048)", CAO)]),
            tc_sub("Giá trị rỗng và NULL", [tc_item("Xem xét NULL, TCTD chuỗi rỗng ''", steps(ctx), "Coi là giống, không tô nền (BR-048)", CAO)]),
            tc_sub("Khác hoa thường", [tc_item("Xem xét 'NGUYỄN VĂN A', CIC 'Nguyễn Văn A'", steps(ctx), "Coi là khác, tô nền ô CIC (assumption Q11)", TB)]),
            tc_sub("Khác một ký tự", [tc_item("Xem xét '001085012345', TCTD '001085012346'", steps(ctx), "Coi là khác, tô nền ô TCTD", CAO)]),
        ]),
        tc_group("Kiểm tra tóm tắt và công tắc chỉ hiện khác biệt", [
            tc_sub("Có khác biệt", [tc_item("5 dòng khác, 1 quan trọng", steps(ctx, "Bật công tắc"),
                                            "Tóm tắt \"5 chỉ tiêu khác biệt, 1 chỉ tiêu quan trọng\"; bảng chỉ còn 5 dòng và tiêu đề nhóm chứa chúng (BR-045)", CAO)]),
            tc_sub("Một dòng khác ở cả hai cột", [tc_item("CN003 khác TCTD và CIC", steps(ctx), "Tính là 1 chỉ tiêu khác biệt (assumption Q10)", TB)]),
            tc_sub("Không có khác biệt", [tc_item("Hồ sơ trùng cả 2 cột", steps(ctx, "Bật công tắc"),
                                                  "Tóm tắt \"0 chỉ tiêu khác biệt\"; bảng chỉ còn tiêu đề cột, không có dòng chỉ tiêu", TB)]),
        ]),
        tc("loại khách hàng lệch giữa hai thẻ", "Lệch Loại KH", "Xem xét: Cá nhân; CIC: Tổ chức", steps(ctx),
           "Tô nền cả hai ô Loại khách hàng; vẫn cho Cập nhật / Từ chối (BR-047, AC#4, assumption Q15)", CAO),
    ]
    if v["tables"]:
        for name, _block, _subs, key in ind["tables"]:
            rows.append(tc_group(f"Kiểm tra so sánh dạng bảng {name}", [
                tc_sub("Khớp trường khóa ở cả hai cột", [tc_item(f"{key} giống nhau, chỉ tiêu con khác", steps(ctx_org),
                                                                 "Xếp cùng hàng; so từng chỉ tiêu con theo BR-048, tô ô khác (BR-049)", CAO)]),
                tc_sub("Không tìm thấy ở hồ sơ tại TCTD", [tc_item(f"{key} chỉ có ở hồ sơ đang xem xét và CIC", steps(ctx_org),
                                                                   "Ô cột TCTD để trống và coi là khác biệt (BR-049 bước 2)", CAO)]),
                tc_sub("Bản ghi chỉ có ở TCTD hoặc CIC", [tc_item(f"{key} chỉ có ở hồ sơ tại CIC", steps(ctx_org),
                                                                  "Thêm hàng mới, ô cột đang xem xét để trống, coi là khác biệt (BR-049 bước 3)", CAO)]),
                tc_sub("Trường khóa trùng hoặc rỗng", [tc_item(f"2 bản ghi cùng {key}; 1 bản ghi {key} rỗng", steps(ctx_org),
                                                               "Mỗi bản ghi một hàng, coi là khác biệt (assumption Q12)", TB)]),
            ]))
    rows.append(subsection("Kiểm tra " + ("cập nhật đồng thời" if bulk else "cập nhật") + " thành công"))
    who = "mọi hồ sơ còn được chọn" if bulk else "hồ sơ"
    rows += [
        tc("cập nhật với lý do hợp lệ", "Xác nhận cập nhật", "Lý do 'Đã xác minh với đơn vị'",
           steps(ctx, f"Click Cập nhật{n_lbl}", "Nhập Lý do", "Click Cập nhật trên MH-006"),
           f"Toast SUC_001; {who} chuyển Đã xử lý; lý do được lưu" + (" chung cho các hồ sơ" if bulk else "")
           + "; popup và màn xử lý đóng, về MH-001 đã tải lại (BR-040" + (", BR-044, AC#3)" if bulk else ", AC#4)")
           + sql("MA_KH = '<mã KH>' AND TRANG_THAI = 'Đã xử lý' AND LY_DO = 'Đã xác minh với đơn vị'"), CAO),
        tc("ghi thông tin pháp lý vào kho TCTD", "Dữ liệu sau cập nhật", "", steps(ctx, "Cập nhật thành công", "Truy vấn kho TCTD theo Mã CIC"),
           "Kho TCTD có bản ghi mang giá trị của hồ sơ vừa xác nhận theo Mã CIC (BR-040, Q02)"
           + sql("MA_CIC = '<Mã CIC>'", "NGAY_BAO_CAO DESC").replace("<HO_SO_PHAP_LY>", "<KHO_TCTD>"), CAO),
        tc("kho chuẩn CICinfo không đổi", "Dữ liệu CICinfo sau cập nhật", "", steps(ctx, "Ghi nhận giá trị cột CIC", "Cập nhật thành công", "Mở hồ sơ khác cùng KH"),
           "Cột Hồ sơ khách hàng tại CIC vẫn hiển thị giá trị cũ (CICinfo không bị cập nhật) — Q02, Dữ liệu và tích hợp #3", CAO),
        tc("hồ sơ vừa xác nhận là phiên bản mới nhất tại TCTD", "Phiên bản cột TCTD sau cập nhật", "",
           steps(ctx, "Cập nhật hồ sơ A thành công", "Mở hồ sơ Chờ xem xét khác cùng KH"),
           "Dropdown Ngày báo cáo có hồ sơ A là phiên bản mới nhất, được chọn mặc định (Q02)", CAO),
        tc("ghi lịch sử cập nhật", "Dòng lịch sử sau cập nhật", "", steps(ctx, "Cập nhật thành công", "Xem chi tiết hồ sơ → tab Lịch sử"),
           "Có dòng \"Cập nhật\", Người cập nhật cbxl01, Mô tả = lý do (BR-031)", CAO),
        tc("chuyển xác thực C06 khi đổi trường định danh", "Gửi C06", "KH cá nhân đổi CN008 (số CCCD)", steps(ctx, "Cập nhật thành công"),
           "Thông tin CN008 thay đổi được chuyển sang quy trình xác thực C06 — kiểm tra tại FUNC-XLDL-035 (BR-010, assumption Q16)", CAO),
        tc("không chuyển C06 khi không đổi trường định danh", "Không gửi C06", "KH cá nhân chỉ đổi CN003 (địa chỉ)", steps(ctx, "Cập nhật thành công"),
           "Không phát sinh yêu cầu xác thực C06 (BR-010)", TB),
        tc("gửi kiểm tra nghi trùng mã CIC", "Gửi FUNC-XLDL-013", "", steps(ctx, "Cập nhật thành công"),
           "KH vừa cập nhật được gửi sang kiểm tra nghi trùng — kiểm tra tại danh sách cảnh báo FUNC-XLDL-013 (BR-011)", CAO),
        tc("gửi INF_011 khi tệp hết hồ sơ chờ xem xét", "Thông báo đơn vị báo cáo", "Tệp còn 1 hồ sơ Chờ xem xét; trước đó đã có 2 hồ sơ Từ chối",
           steps(ctx, "Cập nhật hồ sơ chờ cuối cùng của tệp"),
           "Đơn vị cung cấp nhận Push + Email INF_011 \"Tệp <tên tệp> có 2 hồ sơ pháp lý bị từ chối...\" kèm danh sách, lý do, liên kết FUNC-WEB-002 (BR-012, assumption Q08)", CAO),
        tc("không gửi INF_011 khi tệp còn hồ sơ chờ xem xét", "Chưa đủ điều kiện gửi", "Tệp còn 3 hồ sơ Chờ xem xét", steps(ctx, "Cập nhật 1 hồ sơ"),
           "Không gửi INF_011 (BR-012)", TB),
        tc("không gửi INF_011 khi tệp không có hồ sơ từ chối", "0 hồ sơ Từ chối", "Mọi hồ sơ của tệp đều được Cập nhật", steps(ctx, "Cập nhật hồ sơ chờ cuối cùng"),
           "Không gửi INF_011 (assumption Q08)", TB),
    ]
    rows.append(subsection("Kiểm tra " + ("từ chối đồng thời" if bulk else "từ chối") + " thành công"))
    rows += [
        tc("từ chối với lý do hợp lệ", "Xác nhận từ chối", "Lý do 'Sai số CCCD, đề nghị gửi lại'",
           steps(ctx, f"Click Từ chối{n_lbl}", "Nhập Lý do", "Click Từ chối trên MH-007"),
           f"{who.capitalize()} chuyển Từ chối, lưu lý do; popup và màn đóng, về MH-001 (BR-041" + (", BR-044)" if bulk else ", AC#5)")
           + sql("MA_KH = '<mã KH>' AND TRANG_THAI = 'Từ chối'"), CAO),
        tc("kho TCTD giữ nguyên khi từ chối", "Dữ liệu sau từ chối", "", steps(ctx, "Từ chối thành công", "Truy vấn kho TCTD theo Mã CIC"),
           "Không phát sinh bản ghi mới; giá trị kho TCTD giữ nguyên (BR-041)", CAO),
        tc("ghi lịch sử từ chối", "Dòng lịch sử sau từ chối", "", steps(ctx, "Từ chối thành công", "Xem tab Lịch sử"),
           "Có dòng \"Từ chối\", Mô tả = lý do từ chối (BR-031)", CAO),
        tc("gửi INF_011 sau khi từ chối hồ sơ chờ cuối cùng", "Thông báo đơn vị", "Tệp còn đúng 1 hồ sơ chờ", steps(ctx, "Từ chối hồ sơ đó"),
           "Gửi INF_011 với so_luong = số hồ sơ Từ chối của tệp, kèm lý do từng hồ sơ (BR-012)", CAO),
    ]
    if bulk:
        rows += [
            subsection("Kiểm tra xử lý một phần danh sách"),
            tc("hồ sơ bỏ chọn không bị xử lý", "Loại hồ sơ khỏi lần xác nhận", "Bỏ chọn 2/8 hồ sơ",
               steps(ctx, "Bỏ tick 2 hồ sơ", "Click Cập nhật (6)", "Nhập Lý do, xác nhận"),
               "6 hồ sơ Đã xử lý cùng lý do; 2 hồ sơ bỏ chọn giữ Chờ xem xét (BR-042, ALT-04)", CAO),
            tc("chọn lại hồ sơ đã bỏ chọn", "Đưa lại vào lần xác nhận", "", steps(ctx, "Bỏ tick rồi tick lại 1 hồ sơ"),
               "Hồ sơ hiển thị bình thường; số trên nút tăng lại (BR-042)", TB),
            tc("INF_011 cho từng tệp khi lô gồm nhiều tệp", "Một thông báo mỗi tệp", "Lô gồm hồ sơ của 2 tên tệp D11, cả 2 tệp hết hồ sơ chờ sau lần từ chối",
               steps(ctx, "Từ chối (n)"), "Gửi 2 thông báo INF_011, mỗi tệp một thông báo (BR-012)", CAO),
        ]
    rows.append(subsection("Kiểm tra " + ("xử lý đồng thời" if bulk else "xử lý") + " không thành công"))
    rows += [
        tc("xác nhận khi chưa nhập lý do", "Lý do trống", "", steps(ctx, f"Click Cập nhật{n_lbl}", "Để trống Lý do", "Click Cập nhật trên popup"),
           "Popup giữ; ERR_001 dưới ô Lý do; không ghi gì vào kho (BR-038, AC#3)", CAO),
        tc("hủy trên popup xác nhận", "Hủy MH-006 / MH-007", "", steps(ctx, f"Click Từ chối{n_lbl}", "Nhập Lý do", "Click Hủy"),
           "Popup đóng, ở lại màn xử lý; hồ sơ vẫn Chờ xem xét (ALT-02)", TB),
        tc("hủy màn xử lý", "Hủy " + code, "", steps(ctx, "Click Hủy"),
           "Về MH-001; " + ("mọi hồ sơ" if bulk else "hồ sơ") + " vẫn Chờ xem xét, không ghi lịch sử (ALT-03)", CAO),
        tc("hồ sơ đã được cán bộ khác xử lý", "Hai cán bộ cùng xử lý", "cbxl01 và cbxl02 cùng mở hồ sơ X; cbxl02 Cập nhật trước",
           steps(f"cbxl01: {ctx}", "cbxl02 Cập nhật hồ sơ X thành công", "cbxl01 click Từ chối, nhập Lý do, xác nhận"),
           "cbxl01 bị chặn: toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\"; sau khi toast tắt, hệ thống tự thoát popup/màn hiện tại và reload MH-001; hồ sơ X giữ Đã xử lý, không ghi lý do của cbxl01 (Q06)", CAO),
        tc("mở xử lý từ danh sách cũ", "Danh sách chưa tải lại", "Hồ sơ X đã Đã xử lý nhưng MH-001 của cbxl01 chưa tải lại",
           steps("cbxl01 click Xử lý hồ sơ X từ danh sách cũ", "Xác nhận Cập nhật"),
           "Bị chặn: toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\"; sau khi toast tắt, tự thoát popup/màn hiện tại và reload MH-001 (Q06)", CAO),
        tc("hai hồ sơ chờ xem xét cùng khách hàng xử lý ngược thứ tự", "Lần xác nhận sau cùng thắng", "Kỳ 30/08 TTC04 = 'A1', kỳ 30/09 TTC04 = 'A2'",
           steps("Cập nhật hồ sơ kỳ 30/09", "Cập nhật hồ sơ kỳ 30/08"), "Cả 2 đều được phép; kho TCTD lưu 'A1' theo lần xác nhận sau cùng (Q05)", TB),
        tc("thu hồi quyền trong lúc đang xử lý", "Quyền bị thu hồi giữa chừng", "Quản trị thu hồi quyền chức năng của cbxl01 khi đang mở " + code,
           steps(ctx, "Thu hồi quyền", "Click Cập nhật, nhập Lý do, xác nhận"), "Thao tác bị chặn, toast ERR_011; dữ liệu không đổi (Q38)", CAO),
        tc("cập nhật đồng thời cùng hồ sơ tại 2 tab", "Cùng tài khoản, 2 tab trình duyệt", "cbxl01 mở cùng hồ sơ X ở Tab 1 và Tab 2",
           steps(f"Tab 1 và Tab 2: {ctx}, click Cập nhật{n_lbl}, nhập Lý do", "Tab 1: xác nhận Cập nhật → thành công", "Tab 2: xác nhận Cập nhật"),
           "Tab 2 bị chặn: toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\", tự thoát popup và reload sau khi toast tắt; hồ sơ chỉ được cập nhật 1 lần (Q06, theo mẫu common1)", CAO),
        tc("từ chối đồng thời cùng hồ sơ tại 2 tab", "Cùng tài khoản, 2 tab trình duyệt", "cbxl01 mở cùng hồ sơ X ở Tab 1 và Tab 2",
           steps(f"Tab 1 và Tab 2: {ctx}, click Từ chối{n_lbl}, nhập Lý do", "Tab 1: xác nhận Từ chối → thành công", "Tab 2: xác nhận Từ chối"),
           "Tab 2 bị chặn: toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\", tự thoát popup và reload; hồ sơ giữ lý do của Tab 1 (Q06)", CAO),
        tc("hai cán bộ cùng từ chối một hồ sơ", "Cùng thao tác, 2 người dùng", "cbxl01 và cbxl02 cùng từ chối hồ sơ X",
           steps(f"cbxl01 và cbxl02: {ctx}, click Từ chối{n_lbl}, nhập Lý do", "cbxl01 xác nhận → thành công", "cbxl02 xác nhận"),
           "cbxl02 hiển thị toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\", tự thoát popup và reload sau khi tắt; hồ sơ giữ lý do của cbxl01 (Q06)", CAO),
    ]
    who_fail = "mọi hồ sơ còn được chọn" if bulk else "hồ sơ"
    rows += api_fail_rows(ctx, "Cập nhật", [f"Click Cập nhật{n_lbl}", "Nhập Lý do hợp lệ", "Click Cập nhật trên popup xác nhận"], who_fail)
    rows += api_fail_rows(ctx, "Từ chối", [f"Click Từ chối{n_lbl}", "Nhập Lý do hợp lệ", "Click Từ chối trên popup xác nhận"], who_fail)
    if bulk:
        rows += [
            tc("một hồ sơ trong lô thất bại", "All-or-nothing", "Lô 8 hồ sơ; hồ sơ thứ 5 đã bị cbxl02 Từ chối trước khi xác nhận",
               steps(ctx, "Click Cập nhật (8)", "Nhập Lý do, xác nhận"),
               "Cả lô không được cập nhật: 7 hồ sơ còn lại giữ Chờ xem xét, không có SUC_001, không ghi lịch sử (Q07 — Option B); "
               "toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\", sau khi toast tắt tự thoát và reload MH-001 (Q06)", CAO),
            tc("lỗi ở bước sau khi cập nhật lô", "Rollback toàn bộ", "Giả lập lỗi gửi C06 / nghi trùng / INF_011",
               steps(ctx, "Click Cập nhật (8)", "Nhập Lý do, xác nhận"),
               "Rollback toàn bộ lô: kho TCTD, trạng thái, lý do, lịch sử trở về như trước; hiển thị thông báo lỗi (Q07 — Option B)", CAO),
        ]
    return rows


def m7_q11_rows():
    """FEAT-XLDL-009-07 — MH-008 with Q11 records (same page; differences only)."""
    ctx = "Tại MH-001 tìm Mã tệp = Q11, tick 3 hồ sơ cá nhân Chờ xem xét, click Xử lý hồ sơ"
    return [
        section(BIZ_SECTION + " — Biến thể tệp Q11 (FEAT-XLDL-009-07)"),
        subsection("Kiểm tra xử lý đồng thời hồ sơ tệp Q11"),
        tc("mở xử lý đồng thời hồ sơ Q11", "Mở MH-008 với hồ sơ Q11", "3 hồ sơ Q11 cá nhân", steps(ctx),
           "Mở MH-008; dòng phụ \"Tệp Q11 · Khách hàng cá nhân\"; hồ sơ đầu tiên đang xem; cột CIC theo Mã CIC của hồ sơ (FEAT-07 AC#1)", CAO),
        tc("tập chỉ tiêu Q11 khách hàng cá nhân", "Dòng chỉ tiêu Q11", "", steps(ctx, "Tắt công tắc"),
           "Chỉ hiển thị TTC03, TTC04, CN001–CN012, CN014, CN016, CN017, CN022; không có KB và chỉ tiêu ngoài tập Q11 (FEAT-07 AC#2, assumption Q13)", CAO),
        tc("tập chỉ tiêu Q11 khách hàng tổ chức", "Dòng chỉ tiêu Q11 tổ chức", "3 hồ sơ Q11 tổ chức", steps("Tìm Q11, Loại KH = Tổ chức, tick 3 hồ sơ", "Xử lý hồ sơ", "Tắt công tắc"),
           "Chỉ hiển thị TTC03, TTC04, TC004–TC007, TC011–TC013, TC015, TC017–TC022; không có TC024/TC025/TC026", CAO),
        tc("phiên bản TCTD gồm hồ sơ của mọi loại tệp", "Nguồn phiên bản cột TCTD", "KH có hồ sơ D10 kỳ 30/06 và Q11 đang xem xét",
           steps(ctx, "Mở ô Ngày báo cáo"), "Có phiên bản 30/06 (D10); bảng chỉ so các chỉ tiêu thuộc tập Q11 (assumption Q13)", TB),
        tc("chip khác biệt theo tập Q11", "Chip chỉ tiêu khác biệt", "", steps(ctx), "Chip chỉ chứa mã thuộc tập chỉ tiêu Q11", TB),
        tc("cập nhật đồng thời hồ sơ Q11", "Xác nhận cập nhật", "Lý do 'Đã xác minh'", steps(ctx, "Click Cập nhật (3)", "Nhập Lý do, xác nhận"),
           "3 hồ sơ Đã xử lý, cùng lý do, SUC_001 (FEAT-07 AC#3)", CAO),
        tc("từ chối đồng thời hồ sơ Q11", "Xác nhận từ chối", "Lý do 'Sai thông tin'", steps(ctx, "Click Từ chối (3)", "Nhập Lý do, xác nhận"),
           "3 hồ sơ Từ chối, cùng lý do, kho giữ nguyên", CAO),
        tc("loại khách hàng lệch trên hồ sơ Q11", "Tô nền Loại KH", "Xem xét Cá nhân, CIC Tổ chức", steps(ctx), "Tô nền cả hai ô Loại khách hàng (FEAT-07 AC#4)", TB),
        tc("all-or-nothing với hồ sơ Q11", "Một hồ sơ thất bại", "1/3 hồ sơ đã bị xử lý trước", steps(ctx, "Click Cập nhật (3)", "Xác nhận"),
           "Cả lô không được cập nhật (Q07 — Option B); toast \"Dữ liệu đã bị thay đổi bởi người khác. Vui lòng làm mới trang.\", sau khi toast tắt tự thoát và reload MH-001 (Q06)", CAO),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# M8 — Xử lý tự động khi tiếp nhận, trạng thái, tích hợp (FEAT-XLDL-009-08 + BR liên chức năng)
# ══════════════════════════════════════════════════════════════════════════════
PRECOND_M8 = (
    "Pre-condition:\n"
    "- Có quyền gửi tệp D10, D11, Q11 qua FUNC-XLDL-002 trên môi trường test (hoặc công cụ nạp tệp của nhóm test)\n"
    f"- Đăng nhập {ACC_MAIN} để kiểm chứng trên MH-001 / MH-002 / MH-003\n"
    "- Danh mục chỉ tiêu (FUNC-XLDL-027) đánh dấu quan trọng: TTC04, CN001, CN005, CN006, CN008, CN010, CN016, TC004–TC006, TC011\n"
    "- Truy cập được danh sách FUNC-XLDL-013 (cấp mã, nghi trùng) và FUNC-XLDL-035 (xác thực C06) để kiểm chứng\n"
)
C8 = f"Gửi tệp D11 của đầu mối {DM_IN} chứa hồ sơ cần kiểm tra, chờ hệ thống tiếp nhận"
C8V = f"Mở MH-001, tìm Loại KH, Mã đầu mối = {DM_IN}, Mã tệp = D11, bật cột Ngày cập nhật, Người cập nhật"


def m8_rows():
    rows = [section(BIZ_SECTION), subsection("Kiểm tra phân loại hồ sơ khi tiếp nhận")]
    rows += [
        tc("khách hàng mới có quan hệ tín dụng", "Khóa TTC00+TTC03 chưa có trong CICinfo, có ở tệp khác", f"{DM_IN} + CIF0009001 chưa có trong CICinfo; có trong tệp D01 ở kho xem xét",
           steps(C8, C8V), "Hồ sơ Nhóm \"Mới - Có QHTD\", Trạng thái Chờ cấp mã, Mã CIC trống; được chuyển sang FUNC-XLDL-013 cấp mã (BR-003, BR-004, AC#1)", CAO),
        tc("khách hàng mới không có quan hệ tín dụng", "Khóa chưa có ở bất kỳ tệp nào", f"{DM_IN} + CIF0009002 mới hoàn toàn",
           steps(C8, C8V), "Nhóm \"Mới - Không QHTD\", Trạng thái Chờ cấp mã (BR-004)", CAO),
        tc("khách hàng cũ không đổi thông tin quan trọng", "So với phiên bản mới nhất tại kho TCTD", "CIF0000123464: chỉ đổi CN003 (không quan trọng) so với kho TCTD",
           steps(C8, C8V), "Nhóm \"Không thay đổi TTQT\", Trạng thái Đã xử lý; CN003 được cập nhật tự động vào kho TCTD, CICinfo không đổi (BR-007, AC#2, Q01, Q02)", CAO),
        tc("khách hàng cũ có đổi thông tin quan trọng", "Đổi chỉ tiêu quan trọng", "CIF0000123462: đổi CN008 (quan trọng) so với kho TCTD",
           steps(C8, C8V), "Nhóm \"Thay đổi TTQT\", Trạng thái Chờ xem xét; CN008 được đánh dấu là chỉ tiêu quan trọng thay đổi (BR-008, AC#3, Q01)", CAO),
        tc("đối chiếu với kho TCTD khi kho TCTD và CICinfo lệch nhau", "Baseline so sánh", "Kho TCTD CN008 = 001085099999; CICinfo CN008 = 001085012345; hồ sơ mới CN008 = 001085099999",
           steps(C8, C8V), "Hồ sơ là \"Không thay đổi TTQT\" / Đã xử lý vì trùng giá trị kho TCTD mới nhất cùng TTC00+TTC03 (Q01)", CAO),
        tc("đổi nhiều chỉ tiêu quan trọng", "Đánh dấu nhiều chỉ tiêu", "Đổi CN001, CN008, CN016", steps(C8, "Mở Xử lý hồ sơ của hồ sơ đó"),
           "Hồ sơ Chờ xem xét; 3 chỉ tiêu được đánh dấu, có ★ và tô nền ở màn xử lý (BR-008, BR-035)", CAO),
        tc("chỉ tiêu mã khách hàng không phát sinh khác biệt", "TTC03 là một phần khóa", "Hồ sơ đổi TTC03 so với kỳ trước",
           steps(C8, C8V), "Được nhận diện là khách hàng mới (khóa mới), không phải \"Thay đổi TTQT\" (BR-003, Q01)", TB),
        tc("nhận lặp khách hàng mới khi hồ sơ trước còn chờ cấp mã", "Hai hồ sơ Chờ cấp mã cùng khóa", "CIF0009002 kỳ 30/08 đang Chờ cấp mã; gửi tiếp kỳ 30/09",
           steps(C8, C8V), "Hồ sơ kỳ 30/09 cũng Chờ cấp mã, Nhóm Mới (Q04)", TB),
        tc("hồ sơ không hợp lệ không vào danh sách", "Hồ sơ lỗi tại kho tiền dữ liệu", "Hồ sơ sai cấu trúc trong tệp D11",
           steps(C8, C8V), "Không hiển thị ở MH-001; được xử lý tại FUNC-XLDL-010 (BR-002, EXC-01)", CAO),
    ]
    # GAP-12 — classification R1–R4 for the other file codes
    for tep in ("D10", "Q11"):
        send = f"Gửi tệp {tep} của đầu mối {DM_IN}, chờ hệ thống tiếp nhận"
        view = f"Mở MH-001, tìm Loại KH = Cá nhân, Mã đầu mối = {DM_IN}, Mã tệp = {tep}"
        rows += [
            tc(f"phân loại khách hàng mới có quan hệ tín dụng tệp {tep}", f"R1 với tệp {tep}", f"Khóa {DM_IN} + CIF00{tep}01 chưa có trong CICinfo, có ở tệp tín dụng",
               steps(send, view), "Nhóm \"Mới - Có QHTD\", Chờ cấp mã, chuyển cấp mã CIC (BR-004)", CAO),
            tc(f"phân loại khách hàng mới không quan hệ tín dụng tệp {tep}", f"R2 với tệp {tep}", f"Khóa {DM_IN} + CIF00{tep}02 mới hoàn toàn",
               steps(send, view), "Nhóm \"Mới - Không QHTD\", Chờ cấp mã (BR-004)", CAO),
            tc(f"phân loại khách hàng cũ không đổi thông tin quan trọng tệp {tep}", f"R3 với tệp {tep}", "Chỉ đổi CN003 so với phiên bản mới nhất tại kho TCTD",
               steps(send, view), "Nhóm \"Không thay đổi TTQT\", Đã xử lý; cập nhật tự động vào kho TCTD (BR-007, Q01, Q02)", CAO),
            tc(f"phân loại khách hàng cũ có đổi thông tin quan trọng tệp {tep}", f"R4 với tệp {tep}", "Đổi CN008 so với phiên bản mới nhất tại kho TCTD",
               steps(send, view), "Nhóm \"Thay đổi TTQT\", Chờ xem xét; CN008 được đánh dấu thay đổi (BR-008, Q01)", CAO),
        ]
    org_view = f"Mở MH-001, tìm Loại KH = Tổ chức, Mã đầu mối = {DM_IN}, Mã tệp = D11"
    rows += [
        tc("phân loại khách hàng tổ chức mới", "R1/R2 với KH tổ chức", f"Khóa {DM_IN} + DN0009001 chưa có trong CICinfo",
           steps(C8, org_view), "Nhóm \"Mới - Có QHTD\" hoặc \"Mới - Không QHTD\" theo tệp tín dụng; Chờ cấp mã (BR-004)", CAO),
        tc("khách hàng tổ chức đổi mã số doanh nghiệp", "R4 với KH tổ chức", "Đổi TC011 (MSDN — chỉ tiêu quan trọng)",
           steps(C8, org_view), "Nhóm \"Thay đổi TTQT\", Chờ xem xét; TC011 được đánh dấu thay đổi (BR-008, BR-009)", CAO),
        tc("khách hàng tổ chức chỉ đổi chỉ tiêu không quan trọng", "R3 với KH tổ chức", "Chỉ đổi TC007 (Số điện thoại)",
           steps(C8, org_view), "Nhóm \"Không thay đổi TTQT\", Đã xử lý, cập nhật tự động vào kho TCTD (BR-007)", CAO),
        tc("INF_010 chỉ đếm hồ sơ chờ xem xét", "Tham số so_luong của INF_010", "Tệp D11 có 3 hồ sơ Chờ cấp mã, 4 hồ sơ Chờ xem xét, 2 hồ sơ Đã xử lý",
           steps(C8, "Mở chuông thông báo của cbxl01"), "INF_010 \"Tệp <tên tệp> có 4 hồ sơ pháp lý chờ xem xét.\" (so_luong = số hồ sơ Chờ xem xét — FEAT-08 Thông báo)", CAO),
        subsection("Kiểm tra chuyển trạng thái"),
        tc("chờ cấp mã chuyển đã xử lý khi được cấp mã", "ST-04 → ST-01", "Hồ sơ CIF0009001 Chờ cấp mã",
           steps("Tại FUNC-XLDL-013 cấp mã CIC cho KH", C8V), "Hồ sơ Đã xử lý, Mã CIC hiển thị; lịch sử \"Cấp mã CIC\" (BR-005, AC#5)", CAO),
        tc("cấp mã cập nhật mọi hồ sơ chờ cấp mã cùng khóa", "Nhiều hồ sơ Chờ cấp mã", "CIF0009002 có 2 hồ sơ Chờ cấp mã",
           steps("Cấp mã cho CIF0009002", C8V), "Cả 2 hồ sơ chuyển Đã xử lý và nhận cùng Mã CIC (Q04)", CAO),
        tc("trạng thái cuối không chuyển tiếp", "ST-01, ST-02 là trạng thái cuối", "Hồ sơ Đã xử lý và Từ chối",
           steps(C8V, "Mở menu Thao tác, thử tick ô chọn"), "Không có Xử lý hồ sơ, ô chọn bị khóa; không có đường chuyển sang trạng thái khác (Sơ đồ trạng thái, BR-023, BR-024)", CAO),
        tc("ánh xạ trạng thái và nhóm khách hàng", "Tổ hợp Trạng thái × Nhóm KH", "Dữ liệu sau các ca trên", steps(C8V),
           "Chờ cấp mã ↔ Mới - Có/Không QHTD; Chờ xem xét, Từ chối ↔ Thay đổi TTQT; Đã xử lý ↔ mọi nhóm (BR-016)"
           + sql(f"MA_DAU_MOI = '{DM_IN}' GROUP BY TRANG_THAI, NHOM_KH", "TRANG_THAI"), CAO),
        subsection("Kiểm tra cờ quan hệ tín dụng"),
        tc("cập nhật cờ đã có quan hệ tín dụng", "BR-006", "CIF0009002 đang đánh dấu không có QHTD; TCTD gửi hồ sơ quan hệ tín dụng (D01) của KH",
           steps("Gửi tệp tín dụng của CIF0009002", "Truy vấn thông tin khách hàng"),
           "Cờ quan hệ tín dụng của KH chuyển \"đã có\"; Nhóm KH trên MH-001 giữ nguyên (BR-006, assumption Q17)", TB),
        subsection("Kiểm tra lịch sử khi tiếp nhận"),
        tc("ghi dòng lịch sử tiếp nhận", "Lịch sử theo khách hàng", "", steps(C8, "Xem chi tiết hồ sơ → tab Lịch sử"),
           "Có dòng \"Tiếp nhận\" do Sys ghi theo cặp TTC00 + TTC03 (BR-031, AC#6)", CAO),
        tc("ghi dòng lịch sử cập nhật tự động", "Hồ sơ Không thay đổi TTQT", "", steps(C8, "Xem tab Lịch sử"),
           "Có dòng \"Cập nhật tự động\" do Sys, Giá trị cũ/mới các trường thay đổi (BR-031)", CAO),
        subsection("Kiểm tra thông báo INF_010"),
        tc("gửi INF_010 khi tệp có hồ sơ chờ xem xét", "Thông báo cho cán bộ", "Tệp D11 có 5 hồ sơ Chờ xem xét",
           steps(C8, "Đăng nhập cbxl01, mở chuông thông báo"),
           "Nhận 1 thông báo INF_010 \"Tệp <tên tệp> có 5 hồ sơ pháp lý chờ xem xét.\" cho tệp đó (BR-008, AC#4, assumption Q09)", CAO),
        tc("mỗi tệp một thông báo INF_010", "2 tệp cùng có hồ sơ chờ", "2 tệp D11 và Q11", steps("Gửi 2 tệp", "Mở chuông thông báo"),
           "Nhận 2 thông báo, mỗi tệp 1 thông báo với số lượng đúng", CAO),
        tc("chỉ cán bộ được phân quyền TCTD gửi tệp nhận INF_010", "Người nhận", f"Tệp của {DM_IN2}; cbxl02 chỉ được phân quyền {DM_IN}",
           steps(f"Gửi tệp của {DM_IN2}", "Kiểm tra thông báo của cbxl01 và cbxl02"), "cbxl01 nhận; cbxl02 không nhận (BR-008)", CAO),
        tc("không gửi INF_010 khi tệp không có hồ sơ chờ xem xét", "Không đủ điều kiện", "Tệp chỉ có KH mới và Không thay đổi TTQT", steps(C8),
           "Không phát sinh INF_010 (FEAT-08 Xử lý sự kiện #3)", TB),
        subsection("Kiểm tra phân quyền và dữ liệu cá nhân"),
        tc("dữ liệu cá nhân hiển thị và xuất không che", "Phân loại dữ liệu", "Hồ sơ cá nhân có CN008, CN021",
           steps(C8V, "Xem chi tiết", "Xuất theo bộ lọc"),
           "Giá trị hiển thị và trong tệp xuất không bị che (Phân loại dữ liệu: Không che). Nhật ký truy cập ngoài phạm vi kiểm thử (Q40)", TB),
    ]
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# Feature assembly
# ══════════════════════════════════════════════════════════════════════════════
def _ind_text(ind, kh):
    return ", ".join(f"{g}: {c[0]}–{c[-1]}" if len(c) > 2 else f"{g}: {', '.join(c)}" for g, c in ind[kh])


V_DETAIL_D10 = dict(
    code="MH-002", tep="D10/D11", ind=IND_D10,
    open=f"Tại MH-001 (Cá nhân, {DM_IN}, D11) mở menu Thao tác của hồ sơ cá nhân",
    ctx=f"Tại MH-001 (Cá nhân, {DM_IN}, D11) mở menu Thao tác → Xem của hồ sơ cá nhân",
    ctx_org=f"Tại MH-001 (Tổ chức, {DM_IN}, D11) mở menu Thao tác → Xem của hồ sơ tổ chức",
    org_ac="Hiển thị nhóm KB, TTC, TC (" + _ind_text(IND_D10, "Tổ chức") + ") và các khối TC024, TC025, TC026; không có nhóm CN (AC#3)",
    ind_ac="Hiển thị nhóm KB, TTC, CN (" + _ind_text(IND_D10, "Cá nhân") + "); không có nhóm TC (AC#3)",
)
V_DETAIL_Q11 = dict(
    code="MH-003", tep="Q11", ind=IND_Q11,
    open=f"Tại MH-001 (Cá nhân, {DM_IN}, Q11) mở menu Thao tác của hồ sơ cá nhân",
    ctx=f"Tại MH-001 (Cá nhân, {DM_IN}, Q11) mở menu Thao tác → Xem của hồ sơ cá nhân",
    ctx_org=f"Tại MH-001 (Tổ chức, {DM_IN}, Q11) mở menu Thao tác → Xem của hồ sơ tổ chức",
    org_ac="Chỉ hiển thị KB001, TTC03, TTC04, TC004–TC007, TC011–TC013, TC015, TC017–TC022 (FEAT-03 AC#2)",
    ind_ac="Chỉ hiển thị KB001, TTC03, TTC04, CN001–CN012, CN014, CN016, CN017, CN022 (FEAT-03 AC#3)",
)
V_PROC_D10 = dict(
    code="MH-004", tep="D10/D11", ind=IND_D10, bulk=False, tables=True, toggle_on=False,
    ctx=f"Tại MH-001 (Cá nhân, {DM_IN}, D11) mở menu Thao tác → Xử lý hồ sơ của hồ sơ Chờ xem xét",
    ctx_org=f"Tại MH-001 (Tổ chức, {DM_IN}, D11) mở Xử lý hồ sơ của hồ sơ tổ chức Chờ xem xét",
    ind_ac="Bảng gồm TTC và CN (" + _ind_text(IND_D10, "Cá nhân") + "); không có Thông tin khai báo chung (MH-004 #12)",
    org_ac="Bảng gồm TTC, TC (" + _ind_text(IND_D10, "Tổ chức") + ") và bảng TC024, TC025, TC026; không có KB",
)
V_PROC_Q11 = dict(
    code="MH-005", tep="Q11", ind=IND_Q11, bulk=False, tables=False, toggle_on=False,
    ctx=f"Tại MH-001 (Cá nhân, {DM_IN}, Q11) mở menu Thao tác → Xử lý hồ sơ của hồ sơ Chờ xem xét",
    ctx_org=f"Tại MH-001 (Tổ chức, {DM_IN}, Q11) mở Xử lý hồ sơ của hồ sơ tổ chức Chờ xem xét",
    ind_ac="Chỉ hiển thị TTC03, TTC04, CN001–CN012, CN014, CN016, CN017, CN022; không có KB (FEAT-05 AC#1)",
    org_ac="Chỉ hiển thị TTC03, TTC04, TC004–TC007, TC011–TC013, TC015, TC017–TC022; không có chỉ tiêu dạng bảng (FEAT-05 AC#1)",
)
V_PROC_BULK = dict(
    code="MH-008", tep="D10/D11", ind=IND_D10, bulk=True, tables=True, toggle_on=True,
    ctx=f"Tại MH-001 (Cá nhân, {DM_IN}, D11) tick 8 hồ sơ Chờ xem xét, click Xử lý hồ sơ trên dải thao tác",
    ctx_org=f"Tại MH-001 (Tổ chức, {DM_IN}, D11) tick 3 hồ sơ tổ chức Chờ xem xét, click Xử lý hồ sơ",
    ind_ac="Vùng so sánh dùng tập chỉ tiêu D10/D11 cá nhân như MH-004 (FEAT-06 AC#2)",
    org_ac="Vùng so sánh dùng tập chỉ tiêu D10/D11 tổ chức gồm bảng TC024, TC025, TC026 (FEAT-06 AC#2)",
)

PRECOND_PROC = PRECOND_BASE + (
    f"- Có hồ sơ Chờ xem xét của {DM_IN} có ≥ 3 phiên bản tại kho TCTD cùng Mã CIC và đầu mối; KH có hồ sơ tại CIC (có/không cờ C06)\n"
    "- Danh mục chỉ tiêu đánh dấu quan trọng: TTC04, CN001, CN005, CN006, CN008, CN010, CN016, TC004–TC006, TC011\n"
    f"- Tài khoản {ACC_PEER} để kiểm tra xử lý đồng thời giữa 2 cán bộ\n"
)


# Screen codes are expanded to full screen names in every output cell (user request — no "MH-00x" abbreviations).
SCREENS = {
    "1": ("màn hình", "Danh sách hồ sơ pháp lý"),
    "2": ("popup", "Xem chi tiết hồ sơ pháp lý tệp D10/D11"),
    "3": ("popup", "Xem chi tiết hồ sơ pháp lý tệp Q11"),
    "4": ("popup", "Xử lý hồ sơ pháp lý tệp D10/D11"),
    "5": ("popup", "Xử lý hồ sơ pháp lý tệp Q11"),
    "6": ("popup", "Xác nhận cập nhật thông tin hồ sơ"),
    "7": ("popup", "Xác nhận từ chối cập nhật thông tin hồ sơ"),
    "8": ("màn hình", "Xử lý đồng thời hồ sơ pháp lý"),
}


def expand_screen_codes(text):
    """Replace MH-XLDL-009-00x / MH-00x with '<loại> "<tên màn hình>"' without duplicating the name."""
    if not isinstance(text, str) or "MH-" not in text:
        return text
    starts_upper = text.startswith("MH-")
    text = re.sub(r"MH-XLDL-009-00(\d)", r"MH-00\1", text)
    for n, (kind, name) in SCREENS.items():
        text = text.replace(f"MH-00{n} {name}", f"{kind} \"{name}\"")
    text = re.sub(r"Hộp thoại xác nhận MH-00(\d)", lambda m: f"Hộp thoại \"{SCREENS[m.group(1)][1]}\"", text)
    text = re.sub(r"MH-00(\d) #(\d+)", lambda m: f"mục {m.group(2)} bảng thành phần của {SCREENS[m.group(1)][0]} \"{SCREENS[m.group(1)][1]}\"", text)
    text = re.sub(r"(?i)\b(popup|trang|màn hình)\s+MH-00(\d)", lambda m: f"{m.group(1)} \"{SCREENS[m.group(2)][1]}\"", text)
    text = re.sub(r"MH-00(\d)", lambda m: f"{SCREENS[m.group(1)][0]} \"{SCREENS[m.group(1)][1]}\"", text)
    return text[0].upper() + text[1:] if starts_upper and text else text


def _expand(obj):
    if isinstance(obj, str):
        return expand_screen_codes(obj)
    if isinstance(obj, (list, tuple)):
        return type(obj)(_expand(x) for x in obj)
    return obj


def build_features():
    return [_expand_spec(f) for f in _raw_features()]


def _expand_spec(spec):
    spec.feature_name = expand_screen_codes(spec.feature_name)
    spec.precondition = expand_screen_codes(spec.precondition)
    spec.rows = _expand(spec.rows)
    return spec


def _raw_features():
    return [
        FeatureSpec("M1_DanhSach", "MH-XLDL-009-001 Danh sách hồ sơ pháp lý (FEAT-XLDL-009-01)", "HSPL",
                    PRECOND_M1, m1_rows()),
        FeatureSpec("M2_ChiTiet_D10D11", "MH-XLDL-009-002 Xem chi tiết hồ sơ pháp lý tệp D10/D11 (FEAT-XLDL-009-02)", "HSPL",
                    PRECOND_BASE, detail_rows(V_DETAIL_D10)),
        FeatureSpec("M3_ChiTiet_Q11", "MH-XLDL-009-003 Xem chi tiết hồ sơ pháp lý tệp Q11 (FEAT-XLDL-009-03)", "HSPL",
                    PRECOND_BASE, detail_rows(V_DETAIL_Q11)),
        FeatureSpec("M4_XuLy_D10D11", "MH-XLDL-009-004 Xử lý hồ sơ pháp lý tệp D10/D11 + MH-006/MH-007 (FEAT-XLDL-009-04)", "HSPL",
                    PRECOND_PROC, process_rows(V_PROC_D10)),
        FeatureSpec("M5_XuLy_Q11", "MH-XLDL-009-005 Xử lý hồ sơ pháp lý tệp Q11 + MH-006/MH-007 (FEAT-XLDL-009-05)", "HSPL",
                    PRECOND_PROC, process_rows(V_PROC_Q11)),
        FeatureSpec("M7_XuLyDongThoi", "MH-XLDL-009-008 Xử lý đồng thời hồ sơ pháp lý D10/D11 và Q11 + MH-006/MH-007 (FEAT-XLDL-009-06, 07)", "HSPL",
                    PRECOND_PROC, process_rows(V_PROC_BULK) + m7_q11_rows()),
        FeatureSpec("M8_NghiepVu_TichHop", "Xử lý tự động khi tiếp nhận, trạng thái và tích hợp (FEAT-XLDL-009-08)", "HSPL",
                    PRECOND_M8, m8_rows()),
    ]


if __name__ == "__main__":
    features = build_features()
    generate_excel(features, OUT_PATH)
    for f in features:
        sys.stdout.buffer.write(f"  {f.sheet_title}: {f.tc_count} TC\n".encode("utf-8"))
