# ⚡ 빠른 시작 가이드

## 🎯 당신의 디스코드 정보

### 디스코드 웹훅 URL
```
https://discordapp.com/api/webhooks/1437610959303606343/fRXM_sVUEZUP9GgZSH5qOxBMeA2PdCBzUFsjIB4Wap3ow7rylZ5kS6GkINuyK9Wfiyyb
```

### 디스코드 채널 ID
```
1435107412557430845
```

---

## 🚀 3단계로 시작하기

### 1️⃣ 자동 설치 (가장 쉬운 방법)

1. **`install.bat` 파일을 더블클릭**
   - 위치: `c:\image_transfer\install.bat`
   - 모든 필요한 패키지를 자동으로 설치합니다

2. **설치 완료 후 `start_server.bat` 더블클릭**
   - 위치: `c:\image_transfer\start_server.bat`
   - 서버가 자동으로 시작됩니다

3. **브라우저에서 접속**
   - http://127.0.0.1:5000

---

### 2️⃣ 수동 설치 (문제 발생 시)

#### Python 설치 확인
```powershell
python --version
```

Python이 없다면:
- https://www.python.org/downloads/
- **중요: "Add Python to PATH" 체크!**

#### 패키지 설치
```powershell
cd c:\image_transfer
python -m pip install -r requirements.txt
```

#### FFMPEG 설치
```powershell
# Chocolatey 사용 (PowerShell 관리자 권한)
choco install ffmpeg
```

#### 서버 시작
```powershell
python app.py
```

---

### 3️⃣ 웹 페이지 사용법

1. **브라우저에서 http://127.0.0.1:5000 접속**

2. **영상 파일 선택**
   - 로컬 영상 파일 업로드 (MP4, AVI, MOV 등)

3. **디스코드 웹훅 URL 입력**
   ```
   https://discordapp.com/api/webhooks/1437610959303606343/fRXM_sVUEZUP9GgZSH5qOxBMeA2PdCBzUFsjIB4Wap3ow7rylZ5kS6GkINuyK9Wfiyyb
   ```
   - 복사해서 붙여넣기만 하면 됩니다!

4. **캡처 주기 설정**
   - 예: 10분 (영상의 0분, 10분, 20분... 시점을 캡처)

5. **▶️ 시작 버튼 클릭**
   - 자동으로 캡처가 시작됩니다
   - 디스코드 채널에 스크린샷이 전송됩니다

6. **⏹️ 중지 버튼으로 언제든지 중지 가능**

---

## 📋 체크리스트

설치 전 확인사항:

- [ ] Python 3.11 또는 3.12 설치됨
- [ ] Python이 PATH에 등록됨 (`python --version` 작동)
- [ ] FFMPEG 설치됨 (`ffmpeg -version` 작동)
- [ ] 필요한 Python 패키지 설치됨
- [ ] 디스코드 웹훅 URL 준비됨

---

## 🎬 동작 예시

### 10분 주기로 설정한 경우:

1. **0분 시점**: 첫 번째 스크린샷 → 디스코드 전송
2. **10분 대기**
3. **10분 시점**: 두 번째 스크린샷 → 디스코드 전송
4. **10분 대기**
5. **20분 시점**: 세 번째 스크린샷 → 디스코드 전송
6. ... (영상 끝까지 반복)

### 디스코드에 전송되는 메시지:

```
📸 **자동 캡처**
⏱️ 영상 시점: 10분 0초
🎬 총 길이: 45분 30초
[스크린샷 이미지]
```

---

## ❓ 자주 묻는 질문

### Q1: Python이 설치되어 있는데 인식이 안 돼요
**A:** PowerShell/CMD를 완전히 종료하고 다시 열어보세요. 안 되면 컴퓨터를 재시작하세요.

### Q2: FFMPEG 설치가 어려워요
**A:** 
1. PowerShell을 **관리자 권한**으로 실행
2. Chocolatey 설치:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. FFMPEG 설치:
   ```powershell
   choco install ffmpeg
   ```

### Q3: 디스코드에 이미지가 안 올라가요
**A:** 
- 웹훅 URL이 정확한지 확인
- 디스코드에서 웹훅이 삭제되지 않았는지 확인
- 인터넷 연결 확인

### Q4: 서버가 시작되지 않아요
**A:**
- 5000번 포트가 사용 중일 수 있습니다
- `app.py` 파일을 열고 마지막 줄의 `port=5000`을 `port=8080`으로 변경
- 그리고 http://127.0.0.1:8080 으로 접속

---

## 🆘 도움이 필요하면

1. **오류 메시지를 정확히 복사**
2. **어떤 단계에서 문제가 발생했는지 확인**
3. **`INSTALL_GUIDE.md` 파일을 참고**

---

## 🎉 성공하면

디스코드 채널 (ID: 1435107412557430845)에서 자동으로 영상 스크린샷이 올라오는 것을 확인할 수 있습니다!

**즐거운 사용 되세요! 🚀**
