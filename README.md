# 🎬 영상 자동 캡처 & 디스코드 업로드 시스템

FFmpeg 기반의 영상 자동 압축 및 디스코드 웹훅 업로드 애플리케이션입니다.

## 🌟 새로운 기능

- ✅ **듀얼 영상 동시 처리**: 두 개의 영상을 동시에 압축하고 전송
- ✅ **자동 압축**: FFmpeg를 이용한 고품질 영상 압축 (720p, H.264)
- ✅ **무한 반복**: 모든 이미지 전송 완료 후 자동으로 처음부터 재시작
- ✅ **클라우드 배포 지원**: Google Cloud Platform 무료 티어로 24시간 실행 가능
- ✅ **보안 강화**: 웹훅 URL을 config.json으로 분리

## 📋 주요 기능

- ✅ 영상 파일 업로드 (MP4, AVI, MOV, MKV, WEBM, FLV)
- ✅ 디스코드 웹훅 URL 설정
- ✅ 자동 캡처 주기 설정 (분 단위, 기본값: 10분)
- ✅ 백그라운드 스레드를 통한 자동 스케줄링
- ✅ 실시간 상태 모니터링 (실행 중 / 중지됨)
- ✅ 시작/중지 버튼을 통한 프로세스 제어
- ✅ 현대적이고 직관적인 웹 UI

## 📁 프로젝트 구조

```
image_transfer/
├── app.py                  # Flask 메인 애플리케이션
├── requirements.txt        # Python 패키지 의존성
├── README.md              # 프로젝트 문서
├── templates/
│   └── index.html         # 웹 인터페이스
└── temp_uploads/          # 임시 파일 저장 폴더
    └── .gitkeep
```

## 🛠️ 설치 방법

### 1. FFMPEG 설치 (필수!)

moviepy는 FFMPEG를 사용하므로 반드시 설치해야 합니다.

**Windows:**
1. https://ffmpeg.org/download.html 에서 다운로드
2. 압축 해제 후 `bin` 폴더를 시스템 PATH에 추가
3. 또는 Chocolatey 사용: `choco install ffmpeg`

**확인 방법:**
```powershell
ffmpeg -version
```

### 2. Python 패키지 설치

프로젝트 폴더에서 다음 명령어를 실행하세요:

```powershell
pip install -r requirements.txt
```

**설치되는 패키지:**
- Flask==3.0.0 (웹 프레임워크)
- moviepy==1.0.3 (영상 처리)
- discord-webhook==1.3.0 (디스코드 업로드)
- Werkzeug==3.0.1 (파일 업로드 보안)

## 🚀 실행 방법

### VS Code에서 실행

1. **터미널 열기**: `Ctrl + ` ` (백틱) 또는 상단 메뉴 → Terminal → New Terminal

2. **프로젝트 폴더로 이동**:
   ```powershell
   cd c:\image_transfer
   ```

3. **Flask 서버 시작**:
   ```powershell
   python app.py
   ```

4. **브라우저에서 접속**:
   - 주소: http://127.0.0.1:5000
   - 또는: http://localhost:5000

### 명령 프롬프트에서 실행

```powershell
cd c:\image_transfer
python app.py
```

## 📖 사용 방법

### 1. 디스코드 웹훅 URL 생성

1. 디스코드 서버 → 채널 설정 → 연동 → 웹훅
2. "새 웹훅" 클릭
3. 웹훅 URL 복사 (예: `https://discord.com/api/webhooks/123456789/abcdefg...`)

### 2. 애플리케이션 사용

1. **영상 파일 선택**: 로컬 영상 파일 업로드 (최대 500MB)
2. **웹훅 URL 입력**: 복사한 디스코드 웹훅 URL 붙여넣기
3. **캡처 주기 설정**: 원하는 주기(분) 입력 (기본값: 10분)
4. **시작 버튼 클릭**: 자동 캡처 시작
5. **중지 버튼 클릭**: 언제든지 중지 가능

### 3. 동작 방식

- 영상의 0분, 10분, 20분, 30분... 시점을 자동으로 캡처
- 설정한 주기마다 디스코드로 스크린샷 전송
- 영상 끝에 도달하면 자동 종료
- 백그라운드에서 실행되므로 웹 페이지는 정상 작동

## 🔧 기술 스택

### Backend
- **Flask**: 웹 서버 프레임워크
- **moviepy**: 영상 처리 및 프레임 추출
- **discord-webhook**: 디스코드 메시지 전송
- **threading**: 백그라운드 스케줄링

### Frontend
- **HTML5**: 구조
- **CSS3**: 스타일링 (그라데이션, 애니메이션)
- **JavaScript (Vanilla)**: 동적 기능 및 API 통신

## 📝 API 엔드포인트

### `POST /upload`
영상 파일 업로드 및 스케줄러 시작

**요청:**
- `video`: 영상 파일 (multipart/form-data)
- `webhook_url`: 디스코드 웹훅 URL
- `interval_minutes`: 캡처 주기 (분)

**응답:**
```json
{
  "success": true,
  "message": "스케줄러가 시작되었습니다. 10분마다 캡처합니다."
}
```

### `POST /stop`
스케줄러 중지

**응답:**
```json
{
  "success": true,
  "message": "스케줄러가 중지되었습니다."
}
```

### `GET /status`
현재 상태 조회

**응답:**
```json
{
  "running": true,
  "interval_minutes": 10,
  "current_position": 600,
  "video_duration": 3600
}
```

## ⚠️ 주의사항

1. **FFMPEG 필수**: moviepy 사용을 위해 반드시 FFMPEG를 설치해야 합니다.
2. **파일 크기 제한**: 최대 500MB까지 업로드 가능 (app.py에서 수정 가능)
3. **동시 실행 제한**: 한 번에 하나의 스케줄러만 실행 가능
4. **웹훅 URL 보안**: 웹훅 URL은 외부에 노출되지 않도록 주의
5. **서버 종료**: 서버를 종료하면 실행 중인 스케줄러도 중지됩니다.

## 🐛 문제 해결

### FFMPEG 오류
```
ImageMagick is not installed or not found
```
→ FFMPEG를 설치하고 PATH에 추가했는지 확인

### 포트 충돌
```
Address already in use
```
→ 5000번 포트를 사용 중인 다른 프로그램 종료 또는 app.py의 포트 번호 변경

### 디스코드 업로드 실패
- 웹훅 URL이 올바른지 확인
- 디스코드 서버에서 웹훅이 삭제되지 않았는지 확인
- 파일 크기가 디스코드 제한(8MB)을 초과하지 않는지 확인

## 📄 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 자유롭게 사용 가능합니다.

## 👨‍💻 개발자

AI Assistant (Cascade)

---

**즐거운 개발 되세요! 🚀**
