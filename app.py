from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    return sqlite3.connect("life_os.db")

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        mood TEXT,
        study INTEGER,
        sleep INTEGER,
        water INTEGER
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC")
    data = c.fetchall()

    score = 0
    streak = len(data)
    trend = "No data"

    if data:
        last = data[0]
        score = last[3]*10 + last[4]*5 + last[5]*2

    if len(data) >= 3:
        if data[0][3] > data[1][3] > data[2][3]:
            trend = "📈 Improving"
        else:
            trend = "⚖️ Stable"

    return render_template("index.html", data=data, score=score, streak=streak, trend=trend)

@app.route("/add", methods=["POST"])
def add():
    mood = request.form["mood"]
    study = int(request.form["study"])
    sleep = int(request.form["sleep"])
    water = int(request.form["water"])

    date = datetime.now().strftime("%Y-%m-%d")

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO logs (date, mood, study, sleep, water) VALUES (?, ?, ?, ?, ?)",
              (date, mood, study, sleep, water))
    conn.commit()

    return home()

# 🔥 API ENDPOINT
@app.route("/api/data")
def api_data():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    data = c.fetchall()

    result = []
    for row in data:
        result.append({
            "date": row[1],
            "mood": row[2],
            "study": row[3],
            "sleep": row[4],
            "water": row[5]
        })

    return jsonify(result)

# 🤖 AI (FREE LOGIC)
@app.route("/ai")
def ai():
    return "🤖 Stay consistent. Small improvements daily = big success 🚀"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)