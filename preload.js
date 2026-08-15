const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  chat: (message) => ipcRenderer.invoke('api-chat', message),
});
