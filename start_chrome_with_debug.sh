#!/bin/bash
# Script để khởi động Chrome với remote debugging port
# Sử dụng script này để mở Chrome, sau đó script Python có thể kết nối

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT=9222

# Kiểm tra Chrome có đang chạy với remote debugging không
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ Chrome đã chạy với remote debugging port $PORT"
    echo "   Bạn có thể chạy auto_upload_web.py ngay bây giờ"
else
    echo "🚀 Đang khởi động Chrome với remote debugging port $PORT..."
    "$CHROME_PATH" --remote-debugging-port=$PORT --user-data-dir="$HOME/Library/Application Support/Google/Chrome" &
    echo "✅ Chrome đã khởi động với remote debugging"
    echo "   Bây giờ bạn có thể chạy auto_upload_web.py"
fi
