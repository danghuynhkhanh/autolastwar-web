import sqlite3
from flask import Flask, render_template, jsonify, redirect
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
DB_FILE = "stats.db"

# ---- Tạo database nếu chưa có ----
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY,
                    views INTEGER DEFAULT 0,
                    downloads INTEGER DEFAULT 0
                )''')
    # Nếu chưa có dòng dữ liệu thì thêm vào
    c.execute("SELECT COUNT(*) FROM stats")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO stats (views, downloads) VALUES (0, 0)")
    conn.commit()
    conn.close()

# ---- Hàm load và lưu thống kê ----
def load_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT views, downloads FROM stats WHERE id=1")
    row = c.fetchone()
    if row is None:
        # Nếu chưa có dữ liệu thì thêm mới
        c.execute("INSERT INTO stats (views, downloads) VALUES (0, 0)")
        conn.commit()
        row = (0, 0)
    conn.close()
    return {"views": row[0], "downloads": row[1]}

def save_stats(stats):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE stats SET views=?, downloads=? WHERE id=1",
              (stats["views"], stats["downloads"]))
    conn.commit()
    conn.close()

# ---- Trang chủ ----
@app.route('/')
def home():
    stats = load_stats()
    stats["views"] += 1
    save_stats(stats)
    return render_template('index.html')

# ---- Tải phần mềm (đếm + chuyển hướng Dropbox) ----
@app.route('/download')
def download():
    stats = load_stats()
    stats["downloads"] += 1
    save_stats(stats)
    return redirect("https://www.dropbox.com/scl/fi/i8nfouze066brzdex4kcd/autolastwar.exe?rlkey=uf2ozr4jshbijflzcpwb83crz&st=qqo9j9fk&dl=1")

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
    init_db()
    app.run(debug=True)
