const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  generateVideo: (payload) => ipcRenderer.invoke('generate-video', payload),
});
