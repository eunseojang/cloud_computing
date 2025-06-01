from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = 'vote_results.db'

# DB 초기화
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            option TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 결과 집계
def get_vote_counts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT option, COUNT(*) FROM votes GROUP BY option")
    results = dict(c.fetchall())
    conn.close()
    return results

@app.route("/", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        selected = request.form.get("vote")
        if selected:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO votes (option) VALUES (?)", (selected,))
            conn.commit()
            conn.close()
        return redirect("/")
    
    vote_counts = get_vote_counts()
    return render_template("index.html", vote_counts=vote_counts)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
