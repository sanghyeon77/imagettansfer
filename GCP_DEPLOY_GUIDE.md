# Google Cloud Platform 무료 배포 가이드

## 1단계: GCP 계정 생성 및 VM 인스턴스 만들기

### 1.1 GCP 가입
1. https://cloud.google.com/ 접속
2. "무료로 시작하기" 클릭
3. Google 계정으로 로그인
4. 신용카드 정보 입력 (자동 청구 안됨, 확인용)
5. $300 크레딧 받기 (90일간 유효)

### 1.2 VM 인스턴스 생성
1. GCP 콘솔 접속: https://console.cloud.google.com/
2. 좌측 메뉴 → "Compute Engine" → "VM 인스턴스"
3. "인스턴스 만들기" 클릭

**설정:**
- **이름**: video-discord-bot (원하는 이름)
- **리전**: us-central1, us-west1, us-east1 중 하나 (무료 티어)
- **영역**: 아무거나
- **머신 유형**: e2-micro (무료 티어)
  - vCPU: 0.25-2개
  - 메모리: 1GB
- **부팅 디스크**: 
  - OS: Ubuntu 22.04 LTS
  - 크기: 30GB (무료 티어)
- **방화벽**: HTTP, HTTPS 트래픽 허용 (선택사항)

4. "만들기" 클릭

---

## 2단계: SSH 접속

### 방법 1: 브라우저에서 SSH (간편)
1. VM 인스턴스 목록에서 "SSH" 버튼 클릭
2. 브라우저에서 터미널 열림

### 방법 2: 로컬에서 SSH
```bash
gcloud compute ssh video-discord-bot --zone=us-central1-a
```

---

## 3단계: 서버 설정

### 3.1 자동 설정 (권장)
```bash
# setup_gcp.sh 파일을 서버에 업로드 후
chmod +x setup_gcp.sh
./setup_gcp.sh
```

### 3.2 수동 설정
```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# FFmpeg 설치
sudo apt install ffmpeg -y

# Python 및 pip 설치
sudo apt install python3 python3-pip -y

# 필요한 패키지 설치
pip3 install requests

# 프로젝트 디렉토리 생성
mkdir -p ~/video_discord
cd ~/video_discord
```

---

## 4단계: 프로젝트 파일 업로드

### 방법 1: GitHub 사용 (권장)
```bash
cd ~/video_discord
git clone https://github.com/사용자명/저장소명.git .
```

### 방법 2: SCP로 직접 업로드
로컬 컴퓨터에서:
```bash
gcloud compute scp dual_video_to_discord.py video-discord-bot:~/video_discord/
gcloud compute scp config.json video-discord-bot:~/video_discord/
gcloud compute scp --recurse video1/ video-discord-bot:~/video_discord/
gcloud compute scp --recurse video2/ video-discord-bot:~/video_discord/
```

### 방법 3: 브라우저 SSH에서 파일 업로드
1. SSH 창 우측 상단 톱니바퀴 아이콘
2. "파일 업로드" 선택
3. 파일 선택하여 업로드

---

## 5단계: config.json 설정

```bash
cd ~/video_discord
nano config.json
```

다음 내용 입력:
```json
{
  "videos": [
    {
      "name": "video1",
      "input": "video1/영상파일명.mp4",
      "output": "video1/영상파일명_compressed.mp4",
      "webhook": "디스코드_웹훅_URL_1"
    },
    {
      "name": "video2",
      "input": "video2/영상파일명.mp4",
      "output": "video2/영상파일명_compressed.mp4",
      "webhook": "디스코드_웹훅_URL_2"
    }
  ],
  "interval_seconds": 60
}
```

저장: `Ctrl + X` → `Y` → `Enter`

---

## 6단계: 프로그램 실행

### 테스트 실행
```bash
python3 dual_video_to_discord.py
```

### 백그라운드 실행 (24시간)
```bash
nohup python3 dual_video_to_discord.py > output.log 2>&1 &
```

### 실행 확인
```bash
# 프로세스 확인
ps aux | grep python

# 로그 확인
tail -f output.log
```

### 프로세스 중지
```bash
pkill -f dual_video_to_discord.py
```

---

## 7단계: 자동 재시작 설정 (선택사항)

서버 재부팅 시 자동으로 프로그램 실행:

```bash
# crontab 편집
crontab -e

# 다음 줄 추가 (1번 선택 - nano)
@reboot cd /home/사용자명/video_discord && nohup python3 dual_video_to_discord.py > output.log 2>&1 &
```

저장: `Ctrl + X` → `Y` → `Enter`

---

## 8단계: 비용 관리

### 무료 티어 확인
1. GCP 콘솔 → "결제"
2. "무료 등급 사용량" 확인
3. e2-micro 인스턴스는 **월 730시간 무료** (24시간 가동 가능)

### 주의사항
- **e2-micro만 무료** (다른 머신 타입은 유료)
- **특정 리전만 무료** (us-central1, us-west1, us-east1)
- **30GB 디스크까지 무료**
- **월 1GB 네트워크 송신 무료** (초과 시 과금)

### 비용 알림 설정
1. GCP 콘솔 → "결제" → "예산 및 알림"
2. "예산 만들기" 클릭
3. 금액: $1 (알림용)
4. 이메일 알림 설정

---

## 9단계: 문제 해결

### FFmpeg 오류
```bash
sudo apt install ffmpeg -y
ffmpeg -version
```

### Python 패키지 오류
```bash
pip3 install --upgrade requests
```

### 디스크 공간 부족
```bash
# 사용량 확인
df -h

# 임시 파일 삭제
rm -rf ~/video_discord/temp_images/*
```

### 로그 확인
```bash
# 실시간 로그
tail -f output.log

# 전체 로그
cat output.log
```

---

## 10단계: 서버 중지/삭제

### VM 중지 (비용 절감)
1. GCP 콘솔 → "VM 인스턴스"
2. 인스턴스 선택 → "중지"
3. 디스크 비용만 발생 (무료 티어 내)

### VM 삭제
1. GCP 콘솔 → "VM 인스턴스"
2. 인스턴스 선택 → "삭제"
3. 모든 비용 중지

---

## 요약

1. ✅ GCP 가입 및 VM 생성 (e2-micro, 무료 리전)
2. ✅ SSH 접속
3. ✅ 서버 설정 (FFmpeg, Python)
4. ✅ 파일 업로드 (GitHub 또는 SCP)
5. ✅ config.json 설정
6. ✅ 백그라운드 실행
7. ✅ 자동 재시작 설정
8. ✅ 비용 모니터링

**무료로 24시간 실행 가능!** 🎉
