#!/bin/bash
# Google Cloud Platform 서버 설정 스크립트

echo "=========================================="
echo "🚀 GCP 서버 설정 시작"
echo "=========================================="

# 시스템 업데이트
echo "📦 시스템 업데이트 중..."
sudo apt update && sudo apt upgrade -y

# FFmpeg 설치
echo "🎬 FFmpeg 설치 중..."
sudo apt install ffmpeg -y

# Python 및 pip 설치
echo "🐍 Python 설치 중..."
sudo apt install python3 python3-pip -y

# 필요한 Python 패키지 설치
echo "📚 Python 패키지 설치 중..."
pip3 install requests

# 프로젝트 디렉토리 생성
echo "📁 프로젝트 디렉토리 생성..."
mkdir -p ~/video_discord
cd ~/video_discord

# temp_images 디렉토리 생성
mkdir -p temp_images

echo ""
echo "=========================================="
echo "✅ 설정 완료!"
echo "=========================================="
echo ""
echo "다음 단계:"
echo "1. 영상 파일을 업로드하세요"
echo "2. config.json 파일을 생성하고 웹훅 URL을 설정하세요"
echo "3. 스크립트 실행: nohup python3 dual_video_to_discord.py > output.log 2>&1 &"
echo ""
