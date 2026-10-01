# AI Video Editor for Windows

Starter desktop app for local AI video editing workflow on Windows.

Features included in this starter:
- Electron desktop GUI
- Python backend pipeline
- FFmpeg render placeholder
- easy extension for Whisper + Qwen + local AI workflow

## Requirements

Install on Windows:
- Node.js LTS
- Python 3.11+
- FFmpeg and add to PATH
- Ollama for local LLM (e.g. Qwen)
- Git optional

## Install

1. Clone or copy this project.
2. In project root run:

```bash
npm install
```

3. Create Python virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

4. Start Ollama model if using local Qwen:

```bash
ollama run qwen2.5:7b
```

5. Run the app:

```bash
npm start
```

## Notes

This starter includes the desktop shell and Python pipeline with an FFmpeg render stub. To complete the AI-powered video editing workflow, extend the Python script with:
- Whisper transcription
- Qwen highlight extraction
- FFmpeg clip selection
- subtitle generation
- export to final MP4

## Project structure

```text
ai-video-editor-windows/
  package.json
  main.js
  preload.js
  renderer/
    index.html
  backend/
    pipeline.py
    requirements.txt
  data/
    uploads/
    output/
```
