from flask import Flask, render_template, send_from_directory
import os
import time
import threading
from tts import tts_bp  # Import the Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register the TTS Blueprint
app.register_blueprint(tts_bp)

# Cấu hình thư mục lưu trữ media
MEDIA_FOLDER = 'media'
SHORT_MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, 'short')
LONG_MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, 'long')

# Thời gian xoá tệp (N phút)
DELETE_TIME = 1 * 60  # N phút

# Tạo thư mục nếu chưa tồn tại
os.makedirs(SHORT_MEDIA_FOLDER, exist_ok=True)
os.makedirs(LONG_MEDIA_FOLDER, exist_ok=True)

# Hàm dọn dẹp tệp cũ
def cleanup_old_files():
    while True:
        time.sleep(DELETE_TIME)
        now = time.time()
        for filename in os.listdir(SHORT_MEDIA_FOLDER):
            file_path = os.path.join(SHORT_MEDIA_FOLDER, filename)
            if os.path.isfile(file_path):
                file_age = now - os.path.getmtime(file_path)
                if file_age > DELETE_TIME:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")

# Khởi chạy tiến trình dọn dẹp
cleanup_thread = threading.Thread(target=cleanup_old_files)
cleanup_thread.daemon = True
cleanup_thread.start()

# API để phục vụ tệp tĩnh
@app.route('/media/<storage_type>/<filename>')
def media(storage_type, filename):
    if storage_type == 'short':
        directory = SHORT_MEDIA_FOLDER
    elif storage_type == 'long':
        directory = LONG_MEDIA_FOLDER
    else:
        return jsonify({"error": "Invalid storage type"}), 400
    return send_from_directory(directory, filename)

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)