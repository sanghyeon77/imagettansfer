"""
FFmpeg를 이용한 영상 압축 및 디스코드 자동 업로드 스크립트 (video1 + video2 동시 처리)
- video1/20251107_150053 - Trim.mp4와 video2/20251114_123534.mp4를 동시에 압축
- 1분마다 두 영상에서 이미지를 추출하여 각각의 디스코드 웹훅으로 전송
"""

import subprocess
import os
import time
import requests
from datetime import datetime
from pathlib import Path
import threading
from queue import Queue
import json

# 설정 파일 로드
def load_config():
    """config.json 파일에서 설정 로드"""
    config_path = "config.json"
    if not os.path.exists(config_path):
        print("❌ config.json 파일을 찾을 수 없습니다.")
        print("📝 config.example.json을 복사하여 config.json을 생성하고 웹훅 URL을 설정하세요.")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ config.json 로드 실패: {e}")
        return None

# 설정 로드
config = load_config()
if config is None:
    exit(1)

VIDEOS = config.get("videos", [])
INTERVAL_SECONDS = config.get("interval_seconds", 60)
TEMP_IMAGES_DIR = "temp_images"

def check_ffmpeg():
    """FFmpeg 설치 확인"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg가 설치되어 있습니다.")
            return True
    except FileNotFoundError:
        print("❌ FFmpeg가 설치되어 있지 않습니다.")
        print("📥 INSTALL_GUIDE.md를 참고하여 FFmpeg를 설치해주세요.")
        return False
    except Exception as e:
        print(f"❌ FFmpeg 확인 중 오류: {e}")
        return False

def get_video_duration(video_path):
    """영상 길이 확인 (초 단위)"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        print(f"❌ 영상 길이 확인 실패: {e}")
        return None

def compress_video(input_path, output_path, video_name):
    """FFmpeg를 이용한 영상 압축"""
    print(f"\n{'='*60}")
    print(f"🔄 [{video_name}] 영상 압축 시작...")
    print(f"{'='*60}")
    
    if not os.path.exists(input_path):
        print(f"❌ [{video_name}] 입력 파일을 찾을 수 없습니다: {input_path}")
        return False
    
    # 원본 파일 크기
    original_size = os.path.getsize(input_path) / (1024 * 1024 * 1024)  # GB
    print(f"📦 [{video_name}] 원본 파일 크기: {original_size:.2f} GB")
    
    # 이미 압축된 파일이 있으면 건너뛰기
    if os.path.exists(output_path):
        compressed_size = os.path.getsize(output_path) / (1024 * 1024 * 1024)
        print(f"✅ [{video_name}] 이미 압축된 파일이 존재합니다: {output_path}")
        print(f"📦 [{video_name}] 압축 파일 크기: {compressed_size:.2f} GB")
        return True
    
    try:
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', 'scale=-2:720',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-b:v', '1500k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-y',
            output_path
        ]
        
        print(f"⏳ [{video_name}] 압축 진행 중... (시간이 오래 걸릴 수 있습니다)")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        for line in process.stdout:
            if 'time=' in line:
                print(f"⏳ [{video_name}] {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0 and os.path.exists(output_path):
            compressed_size = os.path.getsize(output_path) / (1024 * 1024 * 1024)
            reduction = ((original_size - compressed_size) / original_size) * 100
            print(f"\n{'='*60}")
            print(f"✅ [{video_name}] 압축 완료!")
            print(f"📦 [{video_name}] 압축 전: {original_size:.2f} GB")
            print(f"📦 [{video_name}] 압축 후: {compressed_size:.2f} GB")
            print(f"📉 [{video_name}] 용량 감소: {reduction:.1f}%")
            print(f"{'='*60}")
            return True
        else:
            print(f"❌ [{video_name}] 압축 실패")
            return False
            
    except Exception as e:
        print(f"❌ [{video_name}] 압축 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

def extract_frame(video_path, timestamp, output_path):
    """특정 시점의 프레임을 이미지로 추출"""
    try:
        cmd = [
            'ffmpeg',
            '-ss', str(timestamp),
            '-i', video_path,
            '-frames:v', '1',
            '-q:v', '2',
            '-y',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        return result.returncode == 0 and os.path.exists(output_path)
    except Exception as e:
        return False

def send_to_discord(image_path, timestamp, total_duration, webhook_url, video_name):
    """디스코드 웹훅으로 이미지 전송"""
    try:
        minutes = int(timestamp // 60)
        seconds = int(timestamp % 60)
        total_minutes = int(total_duration // 60)
        total_seconds = int(total_duration % 60)
        
        message = f"📸 **자동 캡처 ({video_name})**\n⏱️ 영상 시점: {minutes}분 {seconds}초\n🎬 총 길이: {total_minutes}분 {total_seconds}초"
        
        with open(image_path, 'rb') as f:
            files = {
                'file': (os.path.basename(image_path), f, 'image/jpeg')
            }
            data = {
                'content': message
            }
            
            response = requests.post(webhook_url, data=data, files=files, timeout=30)
            
            if response.status_code == 200 or response.status_code == 204:
                print(f"✅ [{video_name}] 디스코드 전송 성공: {minutes}분 {seconds}초")
                return True
            else:
                print(f"❌ [{video_name}] 디스코드 전송 실패: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ [{video_name}] 디스코드 전송 중 오류: {e}")
        return False

def process_video(video_config, start_event):
    """개별 영상 처리 (스레드에서 실행)"""
    video_name = video_config["name"]
    video_input = video_config["input"]
    video_output = video_config["output"]
    webhook_url = video_config["webhook"]
    
    print(f"\n[{video_name}] 처리 시작")
    
    # 영상 압축
    if not os.path.exists(video_input):
        print(f"❌ [{video_name}] 영상 파일을 찾을 수 없습니다: {video_input}")
        return
    
    compress_success = compress_video(video_input, video_output, video_name)
    if not compress_success:
        print(f"❌ [{video_name}] 영상 압축에 실패했습니다.")
        return
    
    # 영상 길이 확인
    video_path = video_output if os.path.exists(video_output) else video_input
    duration = get_video_duration(video_path)
    if duration is None:
        print(f"❌ [{video_name}] 영상 길이를 확인할 수 없습니다.")
        return
    
    duration_min = int(duration // 60)
    duration_sec = int(duration % 60)
    print(f"📹 [{video_name}] 영상 길이: {duration_min}분 {duration_sec}초")
    
    # 모든 영상이 준비될 때까지 대기
    print(f"⏳ [{video_name}] 다른 영상 준비 대기 중...")
    start_event.wait()
    
    # 이미지 추출 및 전송
    print(f"\n📤 [{video_name}] 디스코드 자동 업로드 시작")
    
    current_time = 0
    image_count = 0
    
    while current_time < duration:
        image_count += 1
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{video_name}_frame_{image_count:04d}_{timestamp_str}.jpg"
        image_path = os.path.join(TEMP_IMAGES_DIR, image_filename)
        
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        print(f"\n[{video_name}][{image_count}] {minutes}분 {seconds}초 시점 처리 중...")
        
        # 프레임 추출
        if extract_frame(video_path, current_time, image_path):
            print(f"   ✅ [{video_name}] 이미지 추출 완료: {image_filename}")
            
            # 디스코드 전송
            if send_to_discord(image_path, current_time, duration, webhook_url, video_name):
                try:
                    os.remove(image_path)
                except:
                    pass
            
            # 다음 시점으로 이동
            current_time += INTERVAL_SECONDS
            
            # 영상 끝이 아니면 대기
            if current_time < duration:
                print(f"   ⏳ [{video_name}] 다음 전송까지 {INTERVAL_SECONDS}초 대기 중...")
                time.sleep(INTERVAL_SECONDS)
        else:
            print(f"   ❌ [{video_name}] 이미지 추출 실패")
            current_time += INTERVAL_SECONDS
    
    print(f"\n✅ [{video_name}] 모든 이미지 전송 완료! (총 {image_count}개)")

def main():
    """메인 실행 함수"""
    print("\n" + "="*60)
    print("🎬 영상 압축 및 디스코드 자동 업로드 시작 (video1 + video2)")
    print("="*60)
    
    # FFmpeg 확인
    if not check_ffmpeg():
        return
    
    # 임시 이미지 폴더 생성
    os.makedirs(TEMP_IMAGES_DIR, exist_ok=True)
    
    # 동기화 이벤트 (모든 영상이 압축 완료되면 동시에 전송 시작)
    start_event = threading.Event()
    
    # 각 영상을 별도 스레드에서 처리
    threads = []
    for video_config in VIDEOS:
        thread = threading.Thread(target=process_video, args=(video_config, start_event))
        thread.start()
        threads.append(thread)
    
    # 모든 영상이 압축될 때까지 대기
    print("\n⏳ 모든 영상 압축 완료 대기 중...")
    time.sleep(5)  # 압축 시작을 위한 짧은 대기
    
    # 압축 완료 확인
    all_compressed = False
    while not all_compressed:
        all_compressed = True
        for video_config in VIDEOS:
            if not os.path.exists(video_config["output"]) and os.path.exists(video_config["input"]):
                all_compressed = False
                break
        if not all_compressed:
            time.sleep(10)
    
    # 모든 스레드에 시작 신호
    print("\n" + "="*60)
    print("✅ 모든 영상 준비 완료! 동시 전송 시작")
    print("="*60)
    start_event.set()
    
    # 모든 스레드 완료 대기
    for thread in threads:
        thread.join()
    
    print("\n" + "="*60)
    print("✅ 모든 영상 처리 완료!")
    print("="*60)

if __name__ == "__main__":
    try:
        while True:  # 무한 반복
            main()
            print("\n" + "="*60)
            print("🔄 모든 이미지 전송 완료! 10초 후 처음부터 다시 시작합니다...")
            print("="*60)
            time.sleep(10)  # 10초 대기 후 재시작
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()
