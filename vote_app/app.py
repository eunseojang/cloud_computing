from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os
import logging
import boto3
import watchtower
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
DB_PATH = 'vote_results.db'

sns = boto3.client("sns", region_name=os.environ.get("AWS_REGION"))
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

# CloudWatch 로그 설정
logger = logging.getLogger("vote-app")
logger.setLevel(logging.INFO)
logger.addHandler(watchtower.CloudWatchLogHandler(
    log_group='vote-app-log-group',
    stream_name='vote-stream',
    boto3_client=boto3.client('logs', region_name=os.environ.get("AWS_REGION"))
))

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
    logger.info("✅ DB 초기화 완료")

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
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"🗳️ 새로운 투표: {selected}",
                Subject="Vote Notification"
            )
            logger.info(f"🗳️ 투표 완료: {selected}")
        return redirect("/")
    
    vote_counts = get_vote_counts()
    logger.info(f"📊 현재 집계: {vote_counts}")
    return render_template("index.html", vote_counts=vote_counts)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
