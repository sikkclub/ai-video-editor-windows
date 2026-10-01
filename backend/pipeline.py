import json
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout


def main():
    payload = json.loads(sys.argv[1])
    file_path = payload.get('filePath')
    length = payload.get('length', 30)
    platform = payload.get('platform', 'TikTok')

    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f'File not found: {file_path}')

    root = Path(__file__).resolve().parent.parent
    output_dir = root / 'data' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_video = output_dir / 'rendered.mp4'

    cmd = [
        'ffmpeg', '-y',
        '-i', file_path,
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:black',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        str(output_video)
    ]

    run_command(cmd)

    result = {
        'status': 'success',
        'outputVideo': str(output_video),
        'platform': platform,
        'targetLength': length,
        'message': 'FFmpeg render completed successfully. Extend pipeline.py to add Whisper + Qwen + auto cut.'
    }

    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}))
        sys.exit(1)
