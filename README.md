
# 🗳 클라우드 기반 투표 시스템 (Docker + AWS)

## ✅ 개요
- 간단한 웹 투표 애플리케이션을 Docker로 배포
- 투표 결과를 AWS S3에 자동 백업하는 백업 컨테이너 포함

---

## 🔧 실행 방법 (로컬 기준)

1. AWS 자격증명 설정
   - `~/.aws/credentials` 또는 `.env` 파일 생성
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` 포함

2. 실행
```bash
docker-compose up --build
```

3. 브라우저 접속
http://localhost:5000

4. 투표 후, votes.json이 생성됨 → S3로 자동 업로드됨


