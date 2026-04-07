// src/main.ts
import { app, BrowserWindow, ipcMain } from "electron";
import { EventEmitter } from "events";
import * as path from "path";

// -----------------------------------------------------
// 1. Global Event Bus
// -----------------------------------------------------
export const omniEvents = new EventEmitter();

// -----------------------------------------------------
// 2. Create Browser Window
// -----------------------------------------------------
let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadURL("http://localhost:5173"); // or your build path
}

// -----------------------------------------------------
// 3. App Lifecycle
// -----------------------------------------------------
app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// -----------------------------------------------------
// 4. IPC Handlers (Example)
// -----------------------------------------------------
ipcMain.handle("ping", () => "pong");

// -----------------------------------------------------
// 5. Event Loop → Renderer Bridge
// -----------------------------------------------------
omniEvents.on("update", (data) => {
  if (mainWindow && mainWindow.webContents) {
    mainWindow.webContents.send("omni:update", data);
  }
});

// -----------------------------------------------------
// 6. Example Emitters (You will replace with real logic)
// -----------------------------------------------------
function emitTestEvent() {
  omniEvents.emit("update", {
    type: "system_test",
    payload: { message: "Event loop operational" },
  });
}

// Emit a test event 2 seconds after startup
setTimeout(emitTestEvent, 2000);
