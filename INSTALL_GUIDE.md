# 🔧 설치 가이드 (완전 초보자용)

## ⚠️ 현재 상태
Python이 설치되어 있지 않거나 PATH에 등록되지 않은 상태입니다.

---

## 📥 1단계: Python 설치

### Python 다운로드 및 설치

1. **Python 공식 사이트 접속**
   - https://www.python.org/downloads/

2. **Python 3.11 또는 3.12 다운로드**
   - "Download Python 3.x.x" 버튼 클릭

3. **설치 시 중요!**
   - ✅ **"Add Python to PATH" 체크박스를 반드시 체크!**
   - "Install Now" 클릭

4. **설치 확인**
   - 새로운 PowerShell 또는 CMD 창을 열고:
   ```powershell
   python --version
   ```
   - 또는:
   ```powershell
   py --version
   ```

---

## 📥 2단계: FFMPEG 설치

### 방법 1: Chocolatey 사용 (권장)

1. **PowerShell을 관리자 권한으로 실행**
   - Windows 검색 → "PowerShell" → 우클릭 → "관리자 권한으로 실행"

2. **Chocolatey 설치** (아직 없다면)
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

3. **FFMPEG 설치**
   ```powershell
   choco install ffmpeg
   ```

4. **설치 확인**
   ```powershell
   ffmpeg -version
   ```

### 방법 2: 수동 설치

1. **FFMPEG 다운로드**
   - https://github.com/BtbN/FFmpeg-Builds/releases
   - `ffmpeg-master-latest-win64-gpl.zip` 다운로드

2. **압축 해제**
   - 예: `C:\ffmpeg\` 폴더에 압축 해제

3. **환경 변수 PATH에 추가**
   - Windows 검색 → "환경 변수" → "시스템 환경 변수 편집"
   - "환경 변수" 버튼 클릭
   - "시스템 변수"에서 "Path" 선택 → "편집"
   - "새로 만들기" → `C:\ffmpeg\bin` 입력
   - 모든 창에서 "확인" 클릭

4. **새로운 PowerShell 창에서 확인**
   ```powershell
   ffmpeg -version
   ```

---

## 📥 3단계: Python 패키지 설치

### VS Code 터미널에서 실행

1. **VS Code에서 터미널 열기**
   - `Ctrl + ` ` (백틱)
   - 또는 상단 메뉴 → Terminal → New Terminal

2. **프로젝트 폴더로 이동**
   ```powershell
   cd c:\image_transfer
   ```

3. **패키지 설치 (방법 1: 한 번에)**
   ```powershell
   python -m pip install -r requirements.txt
   ```
   
   또는 (py 명령어 사용):
   ```powershell
   py -m pip install -r requirements.txt
   ```

4. **패키지 설치 (방법 2: 하나씩)**
   
   각 패키지를 개별적으로 설치:
   ```powershell
   python -m pip install Flask==3.0.0
   python -m pip install moviepy==1.0.3
   python -m pip install discord-webhook==1.3.0
   python -m pip install Werkzeug==3.0.1
   ```

### 설치 실패 시 해결 방법

#### 오류 1: "pip is not recognized"
```powershell
# pip 업그레이드
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### 오류 2: "Microsoft Visual C++ 14.0 is required"
- Visual Studio Build Tools 설치 필요
- https://visualstudio.microsoft.com/downloads/
- "Build Tools for Visual Studio" 다운로드 및 설치

#### 오류 3: 특정 패키지 설치 실패
```powershell
# 캐시 없이 재설치
python -m pip install --no-cache-dir 패키지명

# 또는 최신 버전으로 설치
python -m pip install 패키지명 --upgrade
```

#### 오류 4: 권한 오류
```powershell
# 사용자 폴더에 설치
python -m pip install --user -r requirements.txt
```

---

## 📥 4단계: 설치 확인

### 모든 패키지가 설치되었는지 확인

```powershell
python -m pip list
```

다음 패키지들이 보여야 합니다:
- Flask (3.0.0)
- moviepy (1.0.3)
- discord-webhook (1.3.0)
- Werkzeug (3.0.1)

---

## 🚀 5단계: 서버 실행

### 서버 시작

```powershell
cd c:\image_transfer
python app.py
```

또는:
```powershell
py app.py
```

### 성공 메시지

다음과 같은 메시지가 나타나면 성공:
```
============================================================
🎬 영상 자동 캡처 & 디스코드 업로드 서버 시작
============================================================
📌 서버 주소: http://127.0.0.1:5000
📌 FFMPEG가 설치되어 있는지 확인하세요!
============================================================
```

### 브라우저 접속

- http://127.0.0.1:5000
- 또는 http://localhost:5000

---

## 🎯 6단계: 디스코드 웹훅 사용

### 웹 페이지에서 입력할 정보

1. **영상 파일**: 로컬 영상 파일 선택
2. **디스코드 웹훅 URL**: 
   ```
   https://discordapp.com/api/webhooks/1437610959303606343/fRXM_sVUEZUP9GgZSH5qOxBMeA2PdCBzUFsjIB4Wap3ow7rylZ5kS6GkINuyK9Wfiyyb
   ```
3. **캡처 주기**: 원하는 분 단위 (예: 10분)

---

## 🐛 문제 해결

### Python이 설치되었는데도 인식 안 됨
1. PowerShell/CMD를 완전히 종료하고 다시 열기
2. 컴퓨터 재시작
3. Python 재설치 (PATH 체크 확인)

### FFMPEG이 설치되었는데도 인식 안 됨
1. PowerShell/CMD를 완전히 종료하고 다시 열기
2. 컴퓨터 재시작
3. 환경 변수 PATH 재확인

### 포트 5000 사용 중 오류
```powershell
# app.py의 마지막 줄을 다음과 같이 수정:
app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
# 그리고 http://127.0.0.1:8080 으로 접속
```

---

## 📞 추가 도움

설치 중 문제가 발생하면:
1. 오류 메시지 전체를 복사
2. 어떤 단계에서 문제가 발생했는지 확인
3. 해당 정보를 제공하면 더 정확한 도움을 드릴 수 있습니다

---

**설치 성공을 기원합니다! 🎉**
