import sqlite3
import json
import boto3
import os
from datetime import datetime

DB_PATH = "vote_results.db"
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")

def export_votes_to_json():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT option, COUNT(*) FROM votes GROUP BY option")
    results = dict(cursor.fetchall())
    conn.close()

    filename = "votes.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return filename

def upload_to_s3(filename):
    s3 = boto3.client("s3")
    key = f"backup/{datetime.utcnow().isoformat()}_{filename}"
    s3.upload_file(filename, S3_BUCKET, key)
    print(f"✅ Uploaded to S3: s3://{S3_BUCKET}/{key}")

if __name__ == "__main__":
    file = export_votes_to_json()
    upload_to_s3(file)
