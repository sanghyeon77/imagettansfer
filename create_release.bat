@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo 배포용 ZIP 파일 생성 스크립트
echo ============================================================
echo.

:: 날짜와 시간으로 파일명 생성
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set RELEASE_NAME=video_auto_capture_%datetime:~0,8%_%datetime:~8,6%

echo 📦 생성할 파일명: %RELEASE_NAME%.zip
echo.

:: 임시 폴더 생성
set TEMP_DIR=%TEMP%\%RELEASE_NAME%
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

echo [1/5] 필수 파일 복사 중...

:: Python 스크립트
copy "dual_video_to_discord.py" "%TEMP_DIR%\" >nul
copy "video1_to_discord.py" "%TEMP_DIR%\" >nul 2>nul
copy "video2_to_discord.py" "%TEMP_DIR%\" >nul 2>nul

:: 설정 파일
copy "config.example.json" "%TEMP_DIR%\" >nul
copy "requirements.txt" "%TEMP_DIR%\" >nul

:: 배치 파일
copy "install.bat" "%TEMP_DIR%\" >nul
copy "stop.bat" "%TEMP_DIR%\" >nul
copy "start_auto.bat" "%TEMP_DIR%\" >nul 2>nul
copy "register_autostart.bat" "%TEMP_DIR%\" >nul 2>nul
copy "unregister_autostart.bat" "%TEMP_DIR%\" >nul 2>nul

:: 문서 파일
copy "README.md" "%TEMP_DIR%\" >nul
copy "INSTALL_GUIDE.md" "%TEMP_DIR%\" >nul 2>nul
copy "QUICK_START.md" "%TEMP_DIR%\" >nul 2>nul
copy "START_HERE.txt" "%TEMP_DIR%\" >nul 2>nul
copy "AUTOSTART_GUIDE.md" "%TEMP_DIR%\" >nul 2>nul
copy "DEPLOYMENT_GUIDE.md" "%TEMP_DIR%\" >nul 2>nul
copy "GCP_DEPLOY_GUIDE.md" "%TEMP_DIR%\" >nul 2>nul

echo    ✅ 파일 복사 완료
echo.

echo [2/5] 폴더 구조 생성 중...

:: 필요한 폴더 생성
mkdir "%TEMP_DIR%\temp_images" >nul 2>nul
mkdir "%TEMP_DIR%\video1" >nul 2>nul
mkdir "%TEMP_DIR%\video2" >nul 2>nul

:: .gitkeep 파일 생성
echo. > "%TEMP_DIR%\temp_images\.gitkeep"

echo    ✅ 폴더 생성 완료
echo.

echo [3/5] 사용자 가이드 생성 중...

:: 간단한 시작 가이드 생성
(
echo ============================================================
echo 영상 자동 캡처 ^& 디스코드 업로드 시스템
echo ============================================================
echo.
echo 📋 빠른 시작 가이드
echo.
echo 1. install.bat 실행 ^(Python 패키지 설치^)
echo 2. config.example.json을 config.json으로 복사
echo 3. config.json에서 웹훅 URL과 영상 경로 설정
echo 4. video1, video2 폴더에 영상 파일 배치
echo 5. dual_video_to_discord.py 실행
echo.
echo 📖 자세한 내용은 README.md를 참고하세요.
echo.
echo ⚙️ 자동 시작 설정
echo - register_autostart.bat ^(관리자 권한으로 실행^)
echo.
echo 🛑 프로그램 중지
echo - stop.bat 실행 또는 Ctrl+C
echo.
echo ============================================================
) > "%TEMP_DIR%\시작하기.txt"

echo    ✅ 가이드 생성 완료
echo.

echo [4/5] ZIP 파일 생성 중...

:: PowerShell을 사용하여 ZIP 파일 생성
powershell -command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%CD%\%RELEASE_NAME%.zip' -Force"

if exist "%RELEASE_NAME%.zip" (
    echo    ✅ ZIP 파일 생성 완료
) else (
    echo    ❌ ZIP 파일 생성 실패
    goto :cleanup
)

echo.

echo [5/5] 정리 중...
rmdir /s /q "%TEMP_DIR%"
echo    ✅ 임시 파일 정리 완료
echo.

:: 파일 크기 확인
for %%A in ("%RELEASE_NAME%.zip") do set SIZE=%%~zA
set /a SIZE_MB=!SIZE! / 1048576

echo ============================================================
echo ✅ 배포 패키지 생성 완료!
echo ============================================================
echo.
echo 📦 파일명: %RELEASE_NAME%.zip
echo 📊 크기: !SIZE_MB! MB
echo 📁 위치: %CD%\%RELEASE_NAME%.zip
echo.
echo 이 ZIP 파일을 다른 컴퓨터에 복사하여 사용할 수 있습니다.
echo.

:cleanup
pause
