from flask import Flask, render_template, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# -------------------
# Route /admin94 không cần mật khẩu
# -------------------
@app.route('/admin94')
def admin94():
    return render_template('generate_key.html')

# -------------------
# API trả thời gian server (múi giờ Việt Nam)
# -------------------
@app.route('/time')
def get_time():
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(tz)
    return jsonify({"datetime": now.isoformat()})

if __name__ == '__main__':
    app.run(debug=True)
