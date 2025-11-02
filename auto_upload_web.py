#!/usr/bin/env python3
"""
WEB INTERFACE FOR AUTO UPLOAD
==============================
Web interface để điều khiển auto_upload_simple.py từ trình duyệt
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import threading
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Global state
script_process = None
script_status = {
    "running": False,
    "pid": None,
    "start_time": None,
    "logs": []
}

SCRIPT_PATH = Path(__file__).parent / "auto_upload_simple.py"

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('auto_upload_control.html')

@app.route('/api/status')
def get_status():
    """Lấy trạng thái script"""
    return jsonify({
        "running": script_status["running"],
        "pid": script_status["pid"],
        "start_time": script_status["start_time"],
        "logs": script_status["logs"][-50:]  # Chỉ lấy 50 log cuối
    })

@app.route('/api/start', methods=['POST'])
def start_script():
    """Start script"""
    global script_process, script_status
    
    if script_status["running"]:
        return jsonify({"error": "Script đang chạy rồi"}), 400
    
    try:
        # Chạy script trong background
        script_process = subprocess.Popen(
            [sys.executable, str(SCRIPT_PATH)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        script_status["running"] = True
        script_status["pid"] = script_process.pid
        script_status["start_time"] = datetime.now().isoformat()
        script_status["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Script đã được khởi động")
        
        # Thread để đọc output
        def read_output():
            for line in iter(script_process.stdout.readline, ''):
                if line:
                    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {line.strip()}"
                    script_status["logs"].append(log_entry)
                    # Giới hạn log để tránh quá nhiều
                    if len(script_status["logs"]) > 1000:
                        script_status["logs"] = script_status["logs"][-500:]
            
            # Script đã kết thúc
            script_process.wait()
            script_status["running"] = False
            script_status["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Script đã kết thúc (exit code: {script_process.returncode})")
            script_process = None
        
        thread = threading.Thread(target=read_output, daemon=True)
        thread.start()
        
        return jsonify({"success": True, "pid": script_process.pid})
    
    except Exception as e:
        script_status["running"] = False
        return jsonify({"error": str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_script():
    """Stop script"""
    global script_process, script_status
    
    if not script_status["running"]:
        return jsonify({"error": "Script không đang chạy"}), 400
    
    try:
        if script_process:
            script_process.terminate()
            script_status["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Đang dừng script...")
            return jsonify({"success": True})
        else:
            script_status["running"] = False
            return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Lấy logs"""
    return jsonify({
        "logs": script_status["logs"],
        "count": len(script_status["logs"])
    })

@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Xóa logs"""
    script_status["logs"] = []
    return jsonify({"success": True})

if __name__ == '__main__':
    print("="*70)
    print("🌐 AUTO UPLOAD WEB CONTROL")
    print("="*70)
    
    url = "http://localhost:5001"
    
    print(f"🚀 Server starting at: {url}")
    print(f"📁 Mở trình duyệt và truy cập: {url}")
    print("="*70)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
