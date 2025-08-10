from flask import Flask, render_template, jsonify, send_file
from datetime import datetime, timezone, timedelta
import json, os

app = Flask(__name__)
DATA_FILE = "stats.json"

# ---- Hàm load và lưu thống kê ----
def load_stats():
    if not os.path.exists(DATA_FILE):
        return {"views": 0, "downloads": 0}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_stats(stats):
    with open(DATA_FILE, "w") as f:
        json.dump(stats, f)

# ---- Trang chủ ----
@app.route('/')
def home():
    stats = load_stats()
    stats["views"] += 1
    save_stats(stats)
    return render_template('index.html')

# ---- Nút tải ----
@app.route('/download')
def download():
    stats = load_stats()
    stats["downloads"] += 1
    save_stats(stats)
    return send_file("autolastwar.exe", as_attachment=True)

# ---- Trang xem thống kê ----
@app.route('/view')
def view_stats():
    stats = load_stats()
    return render_template('view.html', stats=stats)

# ---- Trang tạo key ----
@app.route('/admin94')
def admin94():
    return render_template('generate_key.html')

# ---- API trả thời gian server (múi giờ Việt Nam) ----
@app.route('/time')
def get_time():
    vn_time = datetime.now(timezone(timedelta(hours=7)))
    return jsonify({"datetime": vn_time.isoformat()})

if __name__ == '__main__':
    app.run(debug=True)
