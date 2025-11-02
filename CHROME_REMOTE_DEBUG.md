# 🔌 Sử dụng Chrome với Remote Debugging

Script auto upload sử dụng remote debugging để kết nối với Chrome đang chạy.

## ✅ Cách hoạt động tự động

Khi bạn click "Bắt đầu" trong web interface:

1. **Script tự động kiểm tra** Chrome có đang chạy với remote debugging không
2. **Nếu có** → Kết nối trực tiếp với Chrome đang chạy ✅
3. **Nếu không** → Tự động đóng Chrome và mở lại với remote debugging + cùng profile

## 🚀 Sử dụng lần đầu

1. Chạy web interface:
   ```bash
   python3 auto_upload_web.py
   ```

2. Mở trình duyệt: http://localhost:5001

3. Click "Bắt đầu" → Script sẽ tự động setup Chrome với remote debugging

**Lưu ý:** Lần đầu có thể Chrome sẽ bị đóng và mở lại, nhưng đăng nhập Gmail sẽ được giữ lại.

## 🔧 Khởi động Chrome thủ công (tùy chọn)

Nếu muốn khởi động Chrome với remote debugging từ đầu:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Hoặc sử dụng script helper:
./start_chrome_with_debug.sh
```

Sau đó khi chạy script, nó sẽ kết nối với Chrome đang chạy này.

## 💡 Tips

- Chrome với remote debugging vẫn hoạt động bình thường
- Bạn có thể duyệt web, đăng nhập Gmail như bình thường
- Script sẽ tự động tạo tab mới khi cần
- Không cần lo về bảo mật vì chỉ chạy local (localhost:9222)
