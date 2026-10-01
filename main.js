const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 950,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

ipcMain.handle('generate-video', async (event, payload) => {
  return new Promise((resolve, reject) => {
    const pythonExecutable = process.platform === 'win32'
      ? path.join(__dirname, '.venv', 'Scripts', 'python.exe')
      : 'python3';

    const child = spawn(pythonExecutable, ['backend/pipeline.py', JSON.stringify(payload)], {
      cwd: app.getAppPath(),
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(stderr || 'Pipeline failed'));
        return;
      }

      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (err) {
        reject(new Error('Invalid output from Python pipeline'));
      }
    });
  });
});
