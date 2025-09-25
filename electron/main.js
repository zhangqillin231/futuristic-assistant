
// electron/main.js - Electron bridge scaffold
const { app, BrowserWindow, ipcMain, shell } = require('electron');
const WebSocket = require('ws');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');

let mainWindow = null;
let ws = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 400,
    height: 300,
    show: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  mainWindow.loadURL('about:blank');
  mainWindow.on('closed', () => { mainWindow = null; });
}

app.whenReady().then(() => {
  createWindow();
  // connect to backend websocket bridge
  const BACKEND_WS = process.env.BACKEND_WS || 'ws://localhost:8000/ws/bridge';
  const TOKEN = process.env.DEVICE_TOKEN || ''; // Bearer token or raw token
  const connectUrl = BACKEND_WS + (TOKEN ? ('?token=' + encodeURIComponent(TOKEN)) : '');
  ws = new WebSocket(connectUrl);
  ws.on('open', () => {
    console.log('Connected to backend bridge');
  });
  ws.on('message', async (msg) => {
    try {
      const data = JSON.parse(msg);
      if (data.type === 'execute') {
        handleAction(data.action, data.params);
      }
    } catch (e) { console.error('ws msg err', e); }
  });
  ws.on('close', () => { console.log('bridge closed'); });
});

function handleAction(action, params) {
  console.log('Executing action', action, params);
  if (action === 'open_url') {
    const url = params.url;
    if (url) shell.openExternal(url);
  } else if (action === 'play_sound') {
    // play system beep as demo
    if (process.platform === 'win32') {
      exec('powershell -c (New-Object Media.SoundPlayer "C:\\Windows\\Media\\chimes.wav").PlaySync();');
    } else if (process.platform === 'darwin') {
      exec('afplay /System/Library/Sounds/Glass.aiff'); // mac sound
    } else {
      // linux - try aplay if present
      exec('aplay /usr/share/sounds/alsa/Front_Center.wav || true');
    }
  } else if (action === 'set_volume') {
    const level = params.level || 50;
    // simple implementations - platform dependent; left as exercise to refine
    if (process.platform === 'darwin') {
      exec(`osascript -e "set volume output volume ${level}"`);
    } else if (process.platform === 'win32') {
      // use nircmd or powershell - omitted for brevity
    } else {
      // linux - use amixer if available
      exec(`amixer -D pulse sset Master ${level}% || true`);
    }
  }
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
