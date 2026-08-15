const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let apiProcess;

function startAPIServer() {
  return new Promise((resolve) => {
    console.log('[ELECTRON] Starting API server...');
    
    const projectDir = '/Users/charliekb/Desktop/angry_ami_project';
    const pythonPath = path.join(projectDir, 'venv/bin/python');
    const apiScript = path.join(projectDir, 'src/api_server.py');
    
    apiProcess = spawn(pythonPath, [apiScript], {
      cwd: projectDir,
      env: { ...process.env, PYTHONPATH: projectDir }
    });

    apiProcess.stdout.on('data', (data) => {
      const output = data.toString();
      console.log(`[API] ${output}`);
      if (output.includes('HERMES AGENT FULLY INITIALIZED')) {
        resolve();
      }
    });

    apiProcess.stderr.on('data', (data) => {
      console.error(`[API ERROR] ${data}`);
    });

    setTimeout(() => {
      resolve();
    }, 30000);
  });
}

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  const startUrl = 'http://localhost:3000';

  mainWindow.loadURL(startUrl);

  // NO DEV TOOLS - CLEAN APP ONLY

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', async () => {
  await startAPIServer();
  createWindow();
});

app.on('window-all-closed', () => {
  if (apiProcess) {
    apiProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

ipcMain.handle('api-chat', async (event, message) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    return await response.json();
  } catch (error) {
    return { error: error.message };
  }
});
