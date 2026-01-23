# Hướng dẫn thiết lập Email Notification

Hệ thống sẽ tự động gửi email thông báo lên điện thoại của bạn khi có booking mới.

## Bước 1: Tạo App Password cho Gmail (Nếu dùng Gmail)

Nếu bạn dùng Gmail, cần tạo App Password để gửi email:

1. Vào [Google Account](https://myaccount.google.com/)
2. Click **Security** (Bảo mật)
3. Bật **2-Step Verification** (Xác minh 2 bước) nếu chưa bật
4. Sau khi bật, tìm **App passwords** (Mật khẩu ứng dụng)
5. Chọn **Mail** và **Other (Custom name)**
6. Đặt tên: "Simple Place Booking"
7. Click **Generate**
8. **Copy mật khẩu 16 ký tự** (dạng: `abcd efgh ijkl mnop`) - đây là App Password

**Lưu ý:** Không dùng mật khẩu Gmail thông thường, phải dùng App Password!

## Bước 2: Cấu hình Environment Variables

Tạo hoặc cập nhật file `.env.local` trong thư mục gốc của project:

```env
# Email để nhận notification (bắt buộc)
NOTIFICATION_EMAIL=simpleplace199f@gmail.com

# SMTP Configuration
# Nếu dùng Gmail:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=simpleplace199f@gmail.com
SMTP_PASSWORD=your-app-password-16-chars

# Nếu dùng Outlook:
# SMTP_HOST=smtp-mail.outlook.com
# SMTP_PORT=587
# SMTP_USER=your-email@outlook.com
# SMTP_PASSWORD=your-password

# Nếu dùng email khác, tìm SMTP settings của provider đó
```

### Ví dụ với Gmail:

```env
NOTIFICATION_EMAIL=simpleplace199f@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=simpleplace199f@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
```

**Lưu ý:** Thay `abcd efgh ijkl mnop` bằng App Password thực tế của bạn (16 ký tự).

**Lưu ý:** 
- `SMTP_USER` là email dùng để gửi (có thể khác `NOTIFICATION_EMAIL`)
- `SMTP_PASSWORD` là App Password (Gmail) hoặc mật khẩu thường (Outlook/khác)
- Không có khoảng trắng trong App Password khi paste vào `.env.local`

## Bước 3: Bật Push Notification trên điện thoại

### Android:
1. Cài app **Gmail** hoặc **Email**
2. Vào **Settings** > **Notifications**
3. Bật **"All emails"** hoặc tạo filter cho email từ booking system
4. Đảm bảo app có quyền notification

### iPhone:
1. Cài app **Gmail** hoặc **Mail**
2. Vào **Settings** > **Notifications** > **Gmail/Mail**
3. Bật notifications
4. Chọn **Alert** style để hiện notification

## Bước 4: Test

1. Restart development server:
   ```bash
   # Dừng server (Ctrl+C) và chạy lại
   npm run dev
   ```

2. Thử đặt bàn trên website

3. Kiểm tra email - bạn sẽ nhận được email thông báo trong vài giây!

## Format Email

Email sẽ có:
- **Subject**: "🔔 Đặt bàn mới - [Tên khách hàng]"
- **Nội dung**: 
  - 👤 Tên khách hàng
  - 📧 Email
  - 📱 Số điện thoại
  - 🕐 Ngày giờ đặt bàn
  - 👥 Số khách
  - 💬 Ghi chú
  - ⏰ Thời gian đặt

Email có format HTML đẹp và dễ đọc.

## SMTP Settings cho các Provider phổ biến

### Gmail
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=app-password (16 chars)
```

### Outlook/Hotmail
```
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Yahoo Mail
```
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=app-password
```

### Custom SMTP (SendGrid, Mailgun, etc.)
```
SMTP_HOST=smtp.sendgrid.net (hoặc host của bạn)
SMTP_PORT=587
SMTP_USER=apikey (hoặc username của bạn)
SMTP_PASSWORD=your-api-key
```

## Troubleshooting

### Lỗi: "Invalid login" hoặc "Authentication failed"

**Gmail:**
- Đảm bảo đã bật 2-Step Verification
- Đảm bảo dùng App Password, không phải mật khẩu Gmail thường
- Kiểm tra App Password có đúng không (16 ký tự, không có khoảng trắng)

**Outlook/khác:**
- Kiểm tra mật khẩu có đúng không
- Đảm bảo SMTP settings đúng

### Lỗi: "Connection timeout"

- Kiểm tra `SMTP_HOST` và `SMTP_PORT` có đúng không
- Kiểm tra firewall/network có block port 587 không
- Thử đổi port sang 465 và set `secure: true` trong code (nếu cần)

### Email không nhận được

1. Kiểm tra spam folder
2. Kiểm tra console log trên server để xem có lỗi không
3. Kiểm tra lại các biến môi trường trong `.env.local`
4. Đảm bảo đã restart server sau khi thay đổi `.env.local`

### Email gửi được nhưng không có notification trên điện thoại

- Kiểm tra app email có bật notification không
- Kiểm tra phone settings có cho phép notification từ app email không
- Thử tạo filter/rule trong email để highlight email booking

## Gửi đến nhiều email

Nếu muốn gửi đến nhiều email, có thể:
1. Tạo email group trong Gmail/Outlook
2. Hoặc sửa code để gửi đến nhiều địa chỉ (dùng dấu phẩy)

## Bảo mật

- **Không commit** file `.env.local` lên Git
- **Không share** App Password
- Đảm bảo `.env.local` đã có trong `.gitignore`

## Production (Vercel)

Khi deploy lên Vercel:
1. Vào **Settings** > **Environment Variables**
2. Thêm tất cả các biến từ `.env.local`
3. Deploy lại

**Lưu ý:** App Password của Gmail vẫn hoạt động trên production.
