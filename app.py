from flask import Flask, request, redirect, render_template
import sqlite3, string, random, os

app = Flask(__name__)
DB = 'shortener.db'

# Create DB if it doesn't exist
def init_db():
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, long TEXT, short TEXT)")

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        code = generate_code()
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO urls (long, short) VALUES (?, ?)", (long_url, code))
        short_url = request.host_url + code
    return render_template('index.html', short_url=short_url)

@app.route('/<code>')
def redirect_url(code):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT long FROM urls WHERE short=?", (code,))
        row = cur.fetchone()
        if row:
            return redirect(row[0])
    return "❌ URL not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
