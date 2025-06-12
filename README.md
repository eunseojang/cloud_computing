## Github Link
https://github.com/eunseojang/cloud_computing


# 🗳 클라우드 기반 투표 시스템 (Docker + AWS)
간단한 투표 애플리케이션을 Docker + AWS(Amazon S3, CloudWatch Logs, SNS) 기반으로 만든 프로젝트입니다.


## ✅ 주요 기능

- Flask 기반 투표 웹 애플리케이션
- SQLite에 실시간 투표 결과 저장
- 주기적 백업: 투표 결과를 JSON으로 변환 후 S3에 업로드
- CloudWatch 로그 연동 (서버 로그 기록)
- SNS 연동 (특정 이벤트 시 알림 전송)

## 🧑‍💻 구현 방법


📦 도커 환경 구성

- Dockerfile로 웹앱(vote_web)과 백업 컨테이너(vote_backup) 각각 빌드

- docker-compose.yml로 두 컨테이너를 함께 실행, 동일 네트워크에서 통신
  

📝 .env 환경 변수 설정

- AWS 접근 키, S3 버킷, SNS 토픽 정보 등 외부 노출 없이 안전하게 관리


🗳 Flask 웹앱 구현 (app.py)

- 투표 항목 선택 후 SQLite에 저장

- CloudWatch Logs로 로그 출력

- SNS로 알림 전송 (boto3 사용)


🧾 주기적 백업 (backup.py)

- DB → JSON 변환 후 S3 업로드

- 웹앱 컨테이너 내부에서 threading.Timer()로 1시간마다 실행되도록 구성



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

docker desktop 실행


```bash
git clone https://github.com/eunseojang/cloud_computing
cd vote_app
```

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
- **CloudWatch Logs**

    AWS Console → CloudWatch → 로그 그룹 vote-app-logs
  
- **S3 Backup**

  WS Console → S3 → vote-backup-eunseo 버킷 → backup/ 폴더 확인

- **SNS 알림**

   이메일 구독을 완료했다면, 투표 시 메일 도착 확인

## 🧹 정리 명령어
```bash
docker compose down
```

