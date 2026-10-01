import json
import os
import subprocess
import sys
from pathlib import Path
import whisper
import requests
import re


def run_command(cmd):
    """Run shell command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout


def transcribe_video(video_path: str):
    """Transcribe video using Whisper."""
    print("[*] Starting Whisper transcription...")
    model = whisper.load_model("base")
    result = model.transcribe(video_path, fp16=False)
    print(f"[+] Transcription complete. Found {len(result['segments'])} segments.")
    return result


def ask_qwen(prompt: str) -> str:
    """Send prompt to Qwen via Ollama."""
    print("[*] Sending prompt to Qwen...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:7b",
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )
        if response.status_code != 200:
            raise Exception(f"Qwen request failed: {response.text}")
        result = response.json()["response"]
        print("[+] Qwen response received.")
        return result
    except requests.exceptions.ConnectionError:
        raise Exception(
            "Cannot connect to Ollama. Make sure Ollama is running and Qwen is loaded: ollama run qwen2.5:7b"
        )


def extract_highlights(transcript, target_length: int):
    """Use Qwen to extract highlight moments from transcript."""
    segments = transcript.get("segments", [])
    transcript_text = "\n".join(
        f"{seg['start']:.1f}-{seg['end']:.1f}s: {seg['text']}" for seg in segments[:150]
    )

    prompt = f"""You are a video editor AI. Analyze the transcript and identify the best highlight moments for a {target_length}-second social media clip.

Return ONLY valid JSON as a raw array without markdown fences or explanations.

Format:
[
  {{"start": 12.5, "end": 18.2, "reason": "Key point"}},
  {{"start": 45.0, "end": 51.5, "reason": "Engaging moment"}}
]

Rules:
- Keep segments short and informative
- Prefer moments with clear value or action
- Total duration should be close to {target_length} seconds
- Return only JSON array

Transcript:
{transcript_text}"""

    qwen_response = ask_qwen(prompt)

    try:
        match = re.search(r"\[.*\]", qwen_response, re.DOTALL)
        if match:
            result = json.loads(match.group(0))
        else:
            result = json.loads(qwen_response)
        print(f"[+] Extracted {len(result)} highlights from Qwen.")
        return result
    except json.JSONDecodeError as exc:
        print(f"[!] Could not parse Qwen JSON response: {exc}")
        print(f"[!] Raw response: {qwen_response}")
        return []


def cut_video_segment(input_path: str, start: float, end: float, output_path: str):
    """Cut a video segment using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        str(output_path),
    ]
    print(f"[*] Cutting segment {start:.1f}s - {end:.1f}s...")
    run_command(cmd)
    print(f"[+] Segment saved: {output_path}")


def generate_captions(transcript, start: float, end: float):
    """Generate captions for a clip range."""
    captions = []
    for seg in transcript.get("segments", []):
        seg_start = seg["start"]
        seg_end = seg["end"]
        if seg_start < end and seg_end > start:
            captions.append({
                "start": max(0, seg_start - start),
                "end": seg_end - start,
                "text": seg["text"].strip(),
            })
    return captions


def render_final_video(clips, output_path: str):
    """Render final video from multiple clips."""
    print(f"[*] Rendering final video with {len(clips)} clips...")
    concat_file = Path(output_path).parent / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output_path),
    ]
    run_command(cmd)
    concat_file.unlink()
    print(f"[+] Final video rendered: {output_path}")


def main():
    payload = json.loads(sys.argv[1])
    video_path = payload.get("filePath")
    target_length = payload.get("length", 30)
    platform = payload.get("platform", "TikTok")

    if not video_path or not os.path.exists(video_path):
        raise FileNotFoundError(f"File not found: {video_path}")

    root = Path(__file__).resolve().parent.parent
    output_dir = root / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Transcribe
    print("\n=== STEP 1: TRANSCRIPTION ===")
    transcript = transcribe_video(video_path)
    total_duration = transcript.get("duration", 0)
    print(f"[+] Video duration: {total_duration:.1f}s")

    # Step 2: Extract highlights with Qwen
    print("\n=== STEP 2: HIGHLIGHT EXTRACTION ===")
    highlights = extract_highlights(transcript, target_length)
    if not highlights:
        raise Exception("No highlights extracted by Qwen.")

    # Step 3: Cut clips
    print("\n=== STEP 3: CUTTING CLIPS ===")
    temp_clips = []
    for i, highlight in enumerate(highlights[:3]):
        temp_clip = output_dir / f"clip_{i}.mp4"
        cut_video_segment(video_path, highlight["start"], highlight["end"], str(temp_clip))
        temp_clips.append(str(temp_clip))

    # Step 4: Generate captions for first clip
    first_highlight = highlights[0]
    captions = generate_captions(transcript, first_highlight["start"], first_highlight["end"])

    # Step 5: Render final video
    print("\n=== STEP 5: RENDERING FINAL VIDEO ===")
    final_output = output_dir / "final_output.mp4"
    render_final_video(temp_clips, str(final_output))

    result = {
        "status": "success",
        "outputVideo": str(final_output),
        "platform": platform,
        "targetLength": target_length,
        "transcriptionSegments": len(transcript.get("segments", [])),
        "highlightsExtracted": len(highlights),
        "highlights": highlights,
        "captions": captions,
        "totalDuration": total_duration,
        "message": "Whisper transcription + Qwen highlight extraction + FFmpeg rendering completed successfully.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
