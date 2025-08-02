from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# Dữ liệu mặc định nếu chưa có file data.json
DEFAULT_DATA = {
    "title": "AUTO LASTWAR",
    "download_link": "https://www.dropbox.com/s/abcxyz123/autolastwar.exe?dl=1",
    "video_link": "https://www.youtube.com/embed/VIDEO_ID",
    "usage": "Đây là đoạn văn hướng dẫn sử dụng phần mềm. Bạn có thể cập nhật nội dung này từ trang /admin để phù hợp với phần mềm của bạn.",
    "contact": "Zalo: 0366905470<br>Email: danghuynhkhanh@gmail.com"
}

# Tải dữ liệu từ file
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=2)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Lưu dữ liệu
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', **data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    data = load_data()
    if request.method == 'POST':
        data['title'] = request.form['title']
        data['download_link'] = request.form['download_link']
        data['video_link'] = request.form['video_link']
        data['usage'] = request.form['usage']
        data['contact'] = request.form['contact']
        save_data(data)
        return redirect(url_for('home'))
    return render_template('admin.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
