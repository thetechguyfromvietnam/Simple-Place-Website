# 🌐 Web Control Interface cho Auto Upload

Web interface để điều khiển `auto_upload_simple.py` từ trình duyệt của bạn.

## 🚀 Cách sử dụng

### Bước 1: Cài đặt dependencies

```bash
pip install -r requirements_auto.txt
```

### Bước 2: Khởi động web server

```bash
python3 auto_upload_web.py
```

Bạn sẽ thấy:
```
======================================================================
🌐 AUTO UPLOAD WEB CONTROL
======================================================================
🚀 Server starting at: http://localhost:5001
📁 Mở trình duyệt và truy cập: http://localhost:5001
======================================================================
```

### Bước 3: Mở trình duyệt

Mở trình duyệt và truy cập: **http://localhost:5001**

## 🎮 Chức năng

### Buttons trên giao diện:

1. **▶️ Bắt đầu** - Khởi động script auto upload
2. **⏹️ Dừng** - Dừng script đang chạy
3. **🗑️ Xóa logs** - Xóa tất cả logs

### Features:

- ✅ Real-time status (Đang chạy / Đang dừng)
- ✅ Real-time logs hiển thị output của script
- ✅ Auto-scroll logs
- ✅ Beautiful modern UI

## 📋 API Endpoints

### `GET /api/status`
Lấy trạng thái script

**Response:**
```json
{
  "running": true,
  "pid": 12345,
  "start_time": "2024-01-01T10:00:00",
  "logs": ["log1", "log2", ...]
}
```

### `POST /api/start`
Khởi động script

**Response:**
```json
{
  "success": true,
  "pid": 12345
}
```

### `POST /api/stop`
Dừng script

**Response:**
```json
{
  "success": true
}
```

### `GET /api/logs`
Lấy tất cả logs

**Response:**
```json
{
  "logs": ["log1", "log2", ...],
  "count": 100
}
```

### `POST /api/clear-logs`
Xóa logs

**Response:**
```json
{
  "success": true
}
```

## 🔧 Configuration

File `auto_upload_web.py` chạy trên port **5001** (mặc định).

Nếu port bị chiếm, sửa dòng cuối trong file:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📝 Lưu ý

- Script sẽ chạy trong background, bạn có thể xem logs real-time
- Để dừng script, click nút "Dừng"
- Logs được giới hạn 1000 entries để tránh quá tải bộ nhớ
- Web interface tự động cập nhật status và logs mỗi giây

## 🌐 Truy cập từ thiết bị khác

Nếu muốn truy cập từ máy khác trong cùng mạng:

1. Tìm IP của máy bạn: `ifconfig` (Mac/Linux) hoặc `ipconfig` (Windows)
2. Truy cập: `http://YOUR_IP:5001`

Ví dụ: `http://192.168.1.100:5001`
