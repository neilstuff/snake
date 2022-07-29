'use strict';

const config = require('./config.json');

const electron = require('electron');
const { app } = electron;
const { protocol } = electron;
const { ipcMain } = electron;

const BrowserWindow = electron.BrowserWindow;

const mime = require('mime');
const path = require('path');
const url = require('url');
const fs = require('fs');
const os = require('os');

var mainWindow = null;

function createWindow() {

    mainWindow = new BrowserWindow({
        width: (config.mode == "debug") ? 600 : 700,
        height: 600,
        resizable: false,
        frame: true,
        maximizable: true,
        minHeight: 600,
        minWidth: (config.mode == "debug") ? 600 : 700,
        fullscreenable: true,
        autoHideMenuBar: true,

        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            webSecurity: false
        }

    });

    if (config.mode == "debug") {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.setMenu(null);
    mainWindow.setTitle('Snake');
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file',
        slashes: true
    }))

    mainWindow.on('closed', () => {
        mainWindow = null
    })

}

app.on('ready', () => {

    createWindow();

});