# Hướng dẫn Deploy lên Vercel và cấu hình Environment Variables

## Bước 1: Push code lên GitHub

1. Tạo repository trên GitHub (nếu chưa có)
2. Push code lên GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```

## Bước 2: Import project vào Vercel

1. Truy cập [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** > **Project**
3. Import repository từ GitHub
4. Chọn project và click **Import**

## Bước 3: Thêm Environment Variables

Trong Vercel project settings, vào **Settings** > **Environment Variables** và thêm các biến sau:

### Các biến môi trường cần thêm:

1. **NOTIFICATION_EMAIL**
   - **Key**: `NOTIFICATION_EMAIL`
   - **Value**: `simpleplace199f@gmail.com`
   - **Environment**: Chọn tất cả (Production, Preview, Development)

2. **SMTP_HOST**
   - **Key**: `SMTP_HOST`
   - **Value**: `smtp.gmail.com`
   - **Environment**: Chọn tất cả (Production, Preview, Development)

3. **SMTP_PORT**
   - **Key**: `SMTP_PORT`
   - **Value**: `587`
   - **Environment**: Chọn tất cả (Production, Preview, Development)

4. **SMTP_USER**
   - **Key**: `SMTP_USER`
   - **Value**: `simpleplace199f@gmail.com`
   - **Environment**: Chọn tất cả (Production, Preview, Development)

5. **SMTP_PASSWORD**
   - **Key**: `SMTP_PASSWORD`
   - **Value**: `bkmh yygs tdvd fahv` (App Password của bạn)
   - **Environment**: Chọn tất cả (Production, Preview, Development)

### Cách thêm từng biến:

1. Click **Add New** trong Environment Variables
2. Điền **Key** (tên biến)
3. Điền **Value** (giá trị)
4. Chọn **Environment** (Production, Preview, Development - chọn tất cả)
5. Click **Save**
6. Lặp lại cho tất cả 5 biến

### Sau khi thêm xong:

1. Click **Redeploy** để deploy lại với environment variables mới
2. Hoặc đợi lần deploy tiếp theo, Vercel sẽ tự động sử dụng các biến mới

## Bước 4: Kiểm tra

1. Sau khi deploy xong, thử đặt bàn trên website production
2. Kiểm tra email `simpleplace199f@gmail.com` - bạn sẽ nhận được email thông báo

## Lưu ý quan trọng:

✅ **App Password vẫn hoạt động trên production** - không cần tạo mới  
✅ **Environment Variables được mã hóa** trong Vercel - an toàn  
✅ **Có thể cập nhật** bất cứ lúc nào trong Settings  
✅ **Không commit** `.env.local` lên Git - đã có trong `.gitignore`

## Troubleshooting

### Email không gửi được trên production:

1. Kiểm tra lại tất cả Environment Variables đã được thêm đúng chưa
2. Kiểm tra **SMTP_PASSWORD** có đúng không (không có khoảng trắng thừa)
3. Xem **Deployment Logs** trong Vercel để tìm lỗi
4. Đảm bảo đã **Redeploy** sau khi thêm environment variables

### Cách xem logs:

1. Vào Vercel Dashboard
2. Chọn project
3. Click vào deployment
4. Xem **Logs** tab để debug

## Tóm tắt các biến cần thêm:

| Key | Value | Mô tả |
|-----|-------|-------|
| `NOTIFICATION_EMAIL` | `simpleplace199f@gmail.com` | Email nhận notification |
| `SMTP_HOST` | `smtp.gmail.com` | SMTP server |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USER` | `simpleplace199f@gmail.com` | Email để gửi |
| `SMTP_PASSWORD` | `bkmh yygs tdvd fahv` | App Password |

---

**Lưu ý:** Sau khi thêm xong, nhớ click **Redeploy** để áp dụng thay đổi!
