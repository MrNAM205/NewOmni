// src/preload.ts
import { contextBridge, ipcRenderer } from "electron";

// -----------------------------------------------------
// 1. IPC Invoke Bridges
// -----------------------------------------------------
contextBridge.exposeInMainWorld("omni", {
  ping: () => ipcRenderer.invoke("ping"),

  // Add your other invoke handlers here:
  // apex: (input: string) => ipcRenderer.invoke("omni-apex", input),
  // getGlobalIntelligence: () => ipcRenderer.invoke("omni:get_global_intelligence"),
});

// -----------------------------------------------------
// 2. Event Listener Bridge
// -----------------------------------------------------
contextBridge.exposeInMainWorld("omniEvents", {
  onUpdate: (callback: (data: any) => void) => {
    ipcRenderer.on("omni:update", (_, data) => callback(data));
  },
});
