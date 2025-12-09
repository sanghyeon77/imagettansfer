# 📦 배포 가이드

이 가이드는 프로그램을 다른 컴퓨터에 배포하고 실행하는 방법을 설명합니다.

## 📋 목차
1. [배포 패키지 생성](#배포-패키지-생성)
2. [새 컴퓨터에 설치](#새-컴퓨터에-설치)
3. [설정 방법](#설정-방법)
4. [실행 방법](#실행-방법)
5. [문제 해결](#문제-해결)

---

## 🎁 배포 패키지 생성

### 자동 생성 (권장)

1. **`create_release.bat`** 파일 실행
2. 자동으로 ZIP 파일이 생성됩니다
3. 파일명 예시: `video_auto_capture_20251119_001234.zip`

### 수동 생성

다음 파일들을 ZIP으로 압축:

**필수 파일:**
```
✅ dual_video_to_discord.py
✅ config.example.json
✅ requirements.txt
✅ install.bat
✅ stop.bat
✅ README.md
```

**선택 파일:**
```
📄 start_auto.bat
📄 register_autostart.bat
📄 unregister_autostart.bat
📄 INSTALL_GUIDE.md
📄 QUICK_START.md
📄 AUTOSTART_GUIDE.md
```

**폴더 구조:**
```
📁 temp_images/
📁 video1/
📁 video2/
```

---

## 💻 새 컴퓨터에 설치

### 1단계: 압축 해제

ZIP 파일을 원하는 위치에 압축 해제
- 예: `C:\video_capture\`
- 예: `D:\Programs\video_auto_capture\`

### 2단계: Python 설치 확인

```cmd
python --version
```

**Python이 없다면:**
1. https://www.python.org/downloads/ 에서 다운로드
2. 설치 시 **"Add Python to PATH"** 체크 필수!

### 3단계: FFmpeg 설치

**방법 1: Chocolatey (권장)**
```powershell
# PowerShell 관리자 권한으로 실행
choco install ffmpeg
```

**방법 2: 수동 설치**
1. https://github.com/BtbN/FFmpeg-Builds/releases 에서 다운로드
2. 압축 해제 (예: `C:\ffmpeg\`)
3. 시스템 환경 변수 PATH에 `C:\ffmpeg\bin` 추가

**설치 확인:**
```cmd
ffmpeg -version
```

### 4단계: Python 패키지 설치

압축 해제한 폴더에서:

```cmd
install.bat
```

또는 수동으로:

```cmd
python -m pip install -r requirements.txt
```

---

## ⚙️ 설정 방법

### 1. 설정 파일 생성

`config.example.json`을 복사하여 `config.json` 생성:

```cmd
copy config.example.json config.json
```

### 2. 디스코드 웹훅 URL 설정

`config.json` 파일을 텍스트 에디터로 열기:

```json
{
  "videos": [
    {
      "name": "video1",
      "input": "video1/my_video.mp4",
      "output": "video1/my_video_compressed.mp4",
      "webhook": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_1"
    },
    {
      "name": "video2",
      "input": "video2/another_video.mp4",
      "output": "video2/another_video_compressed.mp4",
      "webhook": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_2"
    }
  ],
  "interval_seconds": 60
}
```

**변경할 항목:**
- `input`: 원본 영상 파일 경로
- `output`: 압축된 영상 저장 경로
- `webhook`: 디스코드 웹훅 URL
- `interval_seconds`: 캡처 간격 (초 단위)

### 3. 영상 파일 배치

영상 파일을 해당 폴더에 복사:
- `video1/` 폴더에 첫 번째 영상
- `video2/` 폴더에 두 번째 영상

---

## 🚀 실행 방법

### 방법 1: 직접 실행

```cmd
python dual_video_to_discord.py
```

### 방법 2: 배치 파일 사용

`start_auto.bat` 더블클릭

### 방법 3: 자동 시작 설정

컴퓨터 재시작 시 자동 실행:

1. `register_autostart.bat` 우클릭
2. "관리자 권한으로 실행" 선택

자세한 내용은 `AUTOSTART_GUIDE.md` 참고

---

## 🛑 프로그램 중지

### 방법 1: stop.bat 실행

`stop.bat` 더블클릭

### 방법 2: 키보드 단축키

실행 중인 콘솔 창에서 `Ctrl + C`

### 방법 3: 작업 관리자

1. `Ctrl + Shift + Esc`
2. `python.exe` 프로세스 찾기
3. "작업 끝내기"

---

## 🔧 문제 해결

### 문제 1: "Python을 찾을 수 없습니다"

**해결책:**
1. Python 설치 확인
2. 환경 변수 PATH에 Python 추가
3. 명령 프롬프트 재시작

### 문제 2: "FFmpeg를 찾을 수 없습니다"

**해결책:**
1. FFmpeg 설치 확인: `ffmpeg -version`
2. PATH에 FFmpeg 추가
3. 컴퓨터 재시작

### 문제 3: "ModuleNotFoundError"

**해결책:**
```cmd
python -m pip install -r requirements.txt
```

### 문제 4: "영상 파일을 찾을 수 없습니다"

**해결책:**
1. `config.json`의 경로 확인
2. 영상 파일이 올바른 폴더에 있는지 확인
3. 파일명이 정확한지 확인 (대소문자, 공백 포함)

### 문제 5: "디스코드 전송 실패"

**해결책:**
1. 웹훅 URL이 올바른지 확인
2. 인터넷 연결 확인
3. 디스코드 서버에서 웹훅이 삭제되지 않았는지 확인

### 문제 6: "압축 실패"

**해결책:**
1. 디스크 공간 확인
2. 영상 파일이 손상되지 않았는지 확인
3. FFmpeg 설치 확인

---

## 📊 시스템 요구사항

### 최소 사양
- **OS**: Windows 10 이상
- **CPU**: 듀얼 코어 이상
- **RAM**: 4GB 이상
- **저장공간**: 영상 크기의 2배 이상
- **인터넷**: 안정적인 연결

### 권장 사양
- **OS**: Windows 10/11
- **CPU**: 쿼드 코어 이상
- **RAM**: 8GB 이상
- **저장공간**: 여유 공간 충분히
- **인터넷**: 고속 연결

---

## 📝 배포 체크리스트

배포 전 확인사항:

- [ ] Python 설치됨
- [ ] FFmpeg 설치됨
- [ ] requirements.txt의 모든 패키지 설치됨
- [ ] config.json 파일 생성 및 설정 완료
- [ ] 영상 파일 배치 완료
- [ ] 디스코드 웹훅 URL 설정 완료
- [ ] 테스트 실행 성공

---

## 🌐 클라우드 배포

24시간 실행을 원한다면:

1. **Google Cloud Platform**: `GCP_DEPLOY_GUIDE.md` 참고
2. **Oracle Cloud**: 무료 VM 제공
3. **AWS EC2**: 1년 무료 티어

자세한 내용은 별도 가이드 참고

---

## 📞 지원

문제가 계속되면:
1. README.md 확인
2. 오류 메시지 전체 복사
3. Python 버전 확인: `python --version`
4. FFmpeg 버전 확인: `ffmpeg -version`

---

**배포 성공을 기원합니다! 🚀**
