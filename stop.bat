@echo off
echo ========================================
echo 프로세스 중단 중...
echo ========================================
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *dual_video_to_discord*"
if %ERRORLEVEL% EQU 0 (
    echo ✅ 프로세스가 성공적으로 중단되었습니다.
) else (
    echo ⚠️ 실행 중인 프로세스를 찾을 수 없습니다.
    echo 수동으로 중단하려면 Ctrl+C를 누르세요.
)
echo ========================================
pause
