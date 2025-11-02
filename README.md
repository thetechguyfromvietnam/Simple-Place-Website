# 🧾 RESTAURANT TAX INVOICE PROCESSOR

Phần mềm xử lý hóa đơn thuế cho nhà hàng - Tự động tạo và upload hóa đơn lên website thuế

## ✨ Tính năng

### 📊 Xử lý hóa đơn

- ✅ Kết hợp và tách file `sale_by_payment_method` thành nhiều file Excel riêng lẻ
- ✅ Xử lý theo payment method (ATM, Transfer)
- ✅ Tự động match tên món với menu (tiếng Việt/Anh)
- ✅ Xử lý giảm giá và chiết khấu thanh toán
- ✅ Thay thế rượu/bia → đồ ăn (điều chỉnh thuế)
- ✅ Tạo hóa đơn Grab với menu random

### 🤖 Tự động hóa upload (MỚI!)

- ✅ Tự động đăng nhập vào website thuế
- ✅ Tự động tạo hóa đơn mới
- ✅ Tự động upload file Excel lên website
- ✅ Tự động lưu và lặp lại cho tất cả files
- ✅ Không cần thao tác thủ công nữa!

## 📁 Cấu trúc thư mục

```
restaurant-tax/
├── process_invoices.py         # Script chính - Xử lý hóa đơn
├── auto_upload_simple.py       # Script upload tự động
├── requirements_auto.txt       # Dependencies cho auto upload
├── HUONG_DAN_TU_DONG_HOA.md   # Hướng dẫn tiếng Việt
├── Menu/
│   ├── parse_menu.py           # Parse menu từ Excel
│   ├── simple-place-menu.xlsx  # Menu Simple Place
│   └── taco-place-menu.xlsx    # Menu Taco Place
├── tax_files/                  # Output folder cho files Excel
└── web_app/                    # Web app version (optional)
```

## 🚀 Quick Start

### 1. Cài đặt

```bash
# Cài dependencies cho xử lý hóa đơn
pip3 install openpyxl xlsxwriter

# Cài dependencies cho auto upload (OPTIONAL)
pip3 install selenium webdriver-manager
```

### 2. Tạo files Excel

```bash
python3 process_invoices.py
```

Menu sẽ hiển thị:

```
============================================================
🧾 PHẦN MỀM XỬ LÝ HÓA ĐƠN
============================================================

Chọn chức năng:
   1. 🔄 Xử lý Sale by Payment Method (kết hợp và tách)
   2. 📄 Xử lý file đơn
   3. 🏪 Tạo hóa đơn Grab
   0. ❌ Thoát
```

### 3. Upload tự động (OPTIONAL)

Sau khi có files Excel, chạy:

```bash
python3 auto_upload_simple.py
```

Script sẽ:
1. Mở website (bạn đăng nhập thủ công trong 10 giây)
2. Tự động click "Quản lý hóa đơn" → "Tạo hóa đơn"
3. Điền thông tin khách hàng và upload file Excel
4. Lưu và lặp lại cho tất cả files

## 📖 Hướng dẫn chi tiết

### Option 1: Xử lý Sale by Payment Method

Kết hợp 2 files `sale_by_payment_method.xls` và `sale_by_payment_method (1).xls`:

1. Đặt 2 files này trong thư mục gốc
2. Chạy `python3 process_invoices.py` → chọn `1`
3. Files được tạo trong `tax_files/`

### Option 2: Xử lý file đơn

Xử lý một file bất kỳ:

1. Chạy `python3 process_invoices.py` → chọn `2`
2. Nhập tên file
3. Files được tạo trong `tax_files/`

### Option 3: Tạo hóa đơn Grab

Tạo hóa đơn Grab với menu random:

1. Chạy `python3 process_invoices.py` → chọn `3`
2. Chọn menu (Simple Place hoặc Taco Place)
3. Nhập tổng doanh thu (đã có thuế 8%)
4. File được tạo trong `tax_files/`

## 🤖 Tự động hóa upload

### Cài đặt

```bash
pip3 install selenium webdriver-manager
```

### Cấu hình

Mở `auto_upload_simple.py` và sửa (nếu cần):

```python
# Thông tin khách hàng (3 trường bắt buộc)
CUSTOMER_FULLNAME = "Khách Hàng Không Cung Cấp Thông Tin"
CUSTOMER_COMPANY = "Khách Hàng Không Cung Cấp Thông Tin"
CUSTOMER_ADDRESS = "Khách Hàng Không Cung Cấp Thông Tin"
```

### Chạy

```bash
python3 auto_upload_simple.py
```

Script sẽ:
1. Mở website (bạn đăng nhập thủ công, có 10 giây)
2. Tự động click "Quản lý hóa đơn" → "Tạo hóa đơn"
3. Điền thông tin khách hàng và upload file
4. Lưu và lặp lại cho tất cả files

**Xem chi tiết**: `HUONG_DAN_TU_DONG_HOA.md`

## 🌐 Web App (Optional)

Nếu muốn dùng web app thay vì command line:

```bash
cd web_app
pip install -r requirements.txt
python app.py
```

Mở browser: http://localhost:5000

## 📚 Tài liệu

| File | Mô tả |
|------|-------|
| `process_invoices.py` | Script chính - Xử lý hóa đơn |
| `auto_upload_simple.py` | Script upload tự động |
| `HUONG_DAN_TU_DONG_HOA.md` | Hướng dẫn tự động hóa (tiếng Việt) |

## 🔧 Configuration

### Menu files

Sửa trong `process_invoices.py`:

```python
MENU_FILES = [
    'Menu/simple-place-menu.xlsx',
    'Menu/taco-place-menu.xlsx'
]
```

### Output directory

```python
OUTPUT_DIR = 'tax_files'
```

### Default files

```python
DEFAULT_FILE1 = 'sale_by_payment_method.xls'
DEFAULT_FILE2 = 'sale_by_payment_method (1).xls'
```

## 📋 Workflow hoàn chỉnh

```bash
# Bước 1: Xử lý dữ liệu gốc
python3 process_invoices.py
# Chọn: 1 = Sale by Payment Method
#       2 = Single file
#       3 = Create Grab invoice

# Files được tạo trong: tax_files/

# Bước 2: Upload tự động lên website (OPTIONAL)
python3 auto_upload_simple.py
```

## 🎯 Output Format

Mỗi file Excel có format:

| Tinh_chat | Ma_so | Ten_san_pham | Don_vi_tinh | So_luong | Don_gia |
|-----------|-------|--------------|-------------|----------|---------|
| 1 | (empty) | Tên món tiếng Việt / Tiếng Anh | Phần/Lon | Số lượng | Đơn giá |

## ⚠️ Lưu ý

1. **Thuế**: Files đã được tính thuế 8%
2. **Giảm giá**: Đã tự động áp dụng vào giá món
3. **Rượu/Bia**: Đã thay thế bằng đồ ăn (tăng giá 10%)
4. **Payment method**: ATM hoặc Transfer
5. **Validation**: Kiểm tra chênh lệch giữa data và tính toán

## 🐛 Troubleshooting

### "No module named 'openpyxl'"

```bash
pip3 install openpyxl xlsxwriter
```

### "File không tồn tại"

Đảm bảo files `.xls` nằm trong thư mục gốc

### "Không tìm thấy món"

Check file menu có đúng format không

### Auto upload lỗi

Xem `HUONG_DAN_TU_DONG_HOA.md` section Troubleshooting

## 📊 Examples

### Ví dụ input

File `sale_by_payment_method.xls` từ hệ thống POS

### Ví dụ output

```
tax_files/
├── 123456 - transfer - 108.000đ.xlsx
├── 123457 - atm - 216.000đ.xlsx
└── 123458 - transfer - 324.000đ.xlsx
```

## 🎓 Advanced Usage

### Custom menu

Thêm menu mới vào `Menu/` và update `MENU_FILES`

### Batch processing

Script tự động xử lý tất cả invoices trong file

### Validation

Script kiểm tra và báo cáo chênh lệch giữa data và tính toán

## 📞 Support

1. Đọc README files
2. Check console logs
3. Test với data sample
4. Xem examples trong code

## ✅ Features

- ✅ Kết hợp files
- ✅ Tách thành files riêng
- ✅ Match menu tự động
- ✅ Xử lý discount
- ✅ Thay rượu/bia
- ✅ Tạo Grab invoice
- ✅ Validation
- ✅ Export Excel
- ✅ Auto upload (NEW!)

## 🚧 Future Plans

- [ ] Web UI cải tiến
- [ ] API integration
- [ ] Batch validation
- [ ] Email reports
- [ ] Dashboard

## 📄 License

MIT License

## 🙏 Credits

- Selenium team
- OpenPyXL team
- XlsxWriter team

---

**Made with ❤️ for restaurant owners**

