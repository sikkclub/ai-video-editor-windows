# AI Video Editor for Windows - Final Setup Guide

Complete step-by-step installation for Windows. Follow each section in order.

## Prerequisites Summary

- Windows 10/11
- Internet connection
- ~5GB free disk space
- Administrator access (for some installations)

## STEP 1: Install Node.js

1. Go to: https://nodejs.org/
2. Download **LTS version** (recommended for stability)
3. Run installer
4. Accept defaults, make sure "Add to PATH" is checked
5. Restart your computer

Verify installation:
```bash
node -v
npm -v
```

Should show version numbers.

## STEP 2: Install Python

1. Go to: https://www.python.org/downloads/
2. Download **Python 3.11** or **3.12**
3. Run installer
4. **IMPORTANT**: Check "Add Python to PATH" at the bottom
5. Click "Install Now"
6. Wait for installation to complete

Verify installation:
```bash
python --version
pip --version
```

Should show version numbers.

## STEP 3: Install FFmpeg

1. Go to: https://www.ffmpeg.org/download.html
2. Choose Windows build from BtbN (recommended)
   - Link: https://github.com/BtbN/FFmpeg-Builds/releases
   - Download: `ffmpeg-full` (latest release)
3. Extract to folder, for example: `C:\ffmpeg`
4. Add to Windows PATH:
   - Press Windows key + X, click "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", click "Path", then "Edit"
   - Click "New"
   - Paste: `C:\ffmpeg\bin`
   - Click OK, OK, OK

Verify installation:
```bash
ffmpeg -version
```

Should show FFmpeg version and libraries.

## STEP 4: Install Ollama

1. Go to: https://ollama.com/download/windows
2. Download installer
3. Run installer, follow defaults
4. Restart your computer

Verify installation:
```bash
ollama --version
```

Should show version number.

## STEP 5: Pull Qwen Model

Open terminal (Command Prompt or PowerShell) and run:

```bash
ollama pull qwen2.5:7b
```

This will download ~5GB model. Wait for completion.

Alternative smaller model (faster but less accurate):
```bash
ollama pull qwen2.5:3b
```

Verify model is installed:
```bash
ollama list
```

Should show `qwen2.5:7b` in the list.

## STEP 6: Clone or Download Project

Option A: Using Git
```bash
git clone https://github.com/sikkclub/ai-video-editor-windows.git
cd ai-video-editor-windows
```

Option B: Download as ZIP
1. Go to: https://github.com/sikkclub/ai-video-editor-windows
2. Click Code → Download ZIP
3. Extract folder
4. Open terminal in extracted folder

## STEP 7: Install Node Dependencies

In project folder, run:
```bash
npm install
```

This will download and install Electron and dependencies (~300MB).

## STEP 8: Create Python Environment

In project folder, run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

This will:
1. Create virtual environment `.venv`
2. Activate it
3. Install Python packages (Whisper, FFmpeg, OpenCV, etc.)

Takes 2-5 minutes depending on internet speed.

## STEP 9: First Run

Make sure you have these running in separate terminal windows:

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

Keep this running. Should show:
```
Listening on 127.0.0.1:11434
```

**Terminal 2 - Start the app:**
In project folder, make sure Python env is activated:
```bash
.venv\Scripts\activate
npm start
```

Electron app should open. Wait 10-15 seconds for startup.

## STEP 10: Using the App

1. Click "Video Input" - select a video file from your computer
2. Choose target duration (15s, 30s, 60s)
3. Choose platform (TikTok, Instagram Reels, YouTube Shorts)
4. Click "Generate"
5. App will:
   - Transcribe video using Whisper
   - Send transcript to Qwen for analysis
   - Extract highlight moments
   - Cut video segments using FFmpeg
   - Render final output
6. Result saved to: `data/output/final_output.mp4`

Processing time:
- 5-10 min video: ~3-5 minutes
- 20-30 min video: ~8-15 minutes

## STEP 11: Troubleshooting

### FFmpeg not found error
- Verify FFmpeg is in PATH: `ffmpeg -version`
- Restart computer after adding to PATH
- Check path folder exists: `C:\ffmpeg\bin`

### Ollama connection failed
- Make sure Ollama is running in separate terminal
- Check: `ollama serve` is active
- Restart Ollama if needed

### Whisper takes very long
- First run downloads model (~1.5GB)
- Subsequent runs are faster
- If stuck, restart app

### Python module not found
- Make sure virtual environment is activated
- Run: `.venv\Scripts\activate`
- Reinstall packages: `pip install -r backend\requirements.txt`

### Electron app won't start
- Check Node.js is installed: `node -v`
- Check npm packages: `npm install`
- Delete `node_modules` and run `npm install` again

## STEP 12: Project Folder Structure

After setup, your folder should look like:
```
ai-video-editor-windows/
├── package.json
├── main.js
├── preload.js
├── README.md
├── backend/
│   ├── pipeline.py
│   └── requirements.txt
├── renderer/
│   └── index.html
├── data/
│   ├── uploads/
│   └── output/
├── node_modules/
└── .venv/
```

## STEP 13: First Test Run

Create test video or use existing one. Run:

1. Start Ollama (Terminal 1):
```bash
ollama serve
```

2. Start app (Terminal 2):
```bash
.venv\Scripts\activate
npm start
```

3. In app:
   - Select video
   - Choose 30s duration
   - Click Generate
   - Watch status tab for progress

Expected output:
- Transcription log
- Extracted highlights (3-5 moments)
- Generated captions
- Final MP4 file

## STEP 14: Daily Use

Every time you use the app:

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
cd C:\path\to\ai-video-editor-windows
.venv\Scripts\activate
npm start
```

Then:
1. Select video
2. Configure settings
3. Click Generate
4. Wait for processing
5. Find output in `data/output/` folder

## STEP 15: Important Notes

- Whisper model (~1.5GB) downloads on first run - be patient
- Qwen model (~5GB) already pulled in STEP 5
- FFmpeg must be in PATH - restart Windows if it doesn't work
- Ollama must run in separate terminal - don't close it
- Python virtual environment must be activated before running app

## STEP 16: Next Steps / Customization

After basic setup, you can:
- Edit prompts in `backend/pipeline.py`
- Adjust highlight selection logic
- Add subtitle burn-in
- Customize UI colors in `renderer/index.html`
- Add new video platforms/presets

## STEP 17: Uninstall (if needed)

To completely remove:
1. Close all terminals and app
2. Delete project folder
3. Remove Ollama: Settings → Apps → Uninstall Ollama
4. (Optional) Uninstall Node.js: Settings → Apps → Uninstall Node.js
5. (Optional) Uninstall Python: Settings → Apps → Uninstall Python
6. (Optional) Remove FFmpeg folder manually

## STEP 18: Support & Issues

If you encounter problems:
1. Check all prerequisites are installed
2. Verify each command shows correct version numbers
3. Restart Ollama and app
4. Check logs in Status tab
5. Try with smaller video file first

## Summary Checklist

- [ ] Node.js installed
- [ ] Python 3.11+ installed
- [ ] FFmpeg installed and in PATH
- [ ] Ollama installed
- [ ] Qwen model pulled (`ollama list` shows qwen2.5:7b)
- [ ] Project cloned/downloaded
- [ ] npm install completed
- [ ] Python venv created and activated
- [ ] requirements.txt installed
- [ ] Ollama running in Terminal 1
- [ ] App running with `npm start`
- [ ] Test video processed successfully

## You're Ready!

Once all steps are complete, you have a working local AI video editor running entirely on your Windows computer with:
- Whisper for transcription
- Qwen for AI analysis
- FFmpeg for video processing
- Electron desktop UI

Enjoy editing!
