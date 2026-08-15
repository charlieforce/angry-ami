const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = require('electron-is-dev');

let mainWindow;
let apiProcess;

function startAPIServer() {
  return new Promise((resolve) => {
    console.log('[ELECTRON] Starting API server...');
    
    const pythonPath = '/Users/charliekb/Desktop/angry_ami_project/venv/bin/python';
    
    apiProcess = spawn(pythonPath, ['src/api_server.py'], {
      cwd: __dirname,
      env: { ...process.env, PYTHONPATH: __dirname }
    });

    apiProcess.stdout.on('data', (data) => {
      const output = data.toString();
      console.log(`[API] ${output}`);
      if (output.includes('HERMES AGENT READY')) {
        console.log('[ELECTRON] API Ready!');
        resolve();
      }
    });

    apiProcess.stderr.on('data', (data) => {
      console.error(`[API ERROR] ${data}`);
    });

    setTimeout(() => {
      console.log('[ELECTRON] API timeout - proceeding anyway');
      resolve();
    }, 15000);
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

  const startUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, 'build/index.html')}`;

  mainWindow.loadURL(startUrl);

  // Only open dev tools in development
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

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
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    return await response.json();
  } catch (error) {
    return { error: error.message };
  }
});
