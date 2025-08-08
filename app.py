from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)