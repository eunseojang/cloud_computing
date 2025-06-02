
# 🗳 클라우드 기반 투표 시스템 (Docker + AWS)
간단한 투표 애플리케이션을 Docker + AWS(Amazon S3, CloudWatch Logs, SNS) 기반으로 만든 프로젝트입니다.


## ✅ 주요 기능

- Flask 기반 투표 웹 애플리케이션
- SQLite에 실시간 투표 결과 저장
- 주기적 백업: 투표 결과를 JSON으로 변환 후 S3에 업로드
- CloudWatch 로그 연동 (서버 로그 기록)
- SNS 연동 (특정 이벤트 시 알림 전송)


## ⚙️ 실행 전 준비사항

1. **`.env` 파일 생성 (루트 디렉토리에):**
```
AWS_ACCESS_KEY_ID=당신의_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=당신의_AWS_SECRET
AWS_REGION=ap-northeast-2
S3_BUCKET_NAME=vote-backup-eunseo
SNS_TOPIC_ARN=arn:aws:sns:ap-northeast-2:계정ID:vote-app-topic
```


2. **AWS 리소스 준비:**
   - S3 버킷 생성: `vote-backup-eunseo`
   - CloudWatch Log Group: `vote-app-logs`
   - SNS Topic 생성: `vote-app-topic` (이메일 구독 필수)
   - IAM 권한: 해당 키가 S3, CloudWatch Logs, SNS를 사용할 수 있도록 설정


## 🚀 실행 방법

### 1. 전체 컨테이너 빌드 및 실행

```bash
docker compose up --build
```

### 2. 웹 접속
http://localhost:5000

- 투표 후 결과가 바로 반영됨
- 로그는 CloudWatch에 기록됨
- SNS 알림은 투표 시 자동 발송됨

### 3. 수동 백업 실행
```bash
docker compose run vote_backup
```

## 🧪 확인 방법
- CloudWatch Logs: AWS Console → CloudWatch → 로그 그룹 vote-app-logs
- S3 Backup: AWS Console → S3 → vote-backup-eunseo 버킷 → backup/ 폴더 확인
- SNS 알림: 이메일 구독을 완료했다면, 투표 시 메일 도착 확인

## 🧹 정리 명령어
```bash
docker compose down
```

