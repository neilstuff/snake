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
const https = require('https');
var JSZip = require("jszip");

var mainWindow = null;

function createWindow() {

    mainWindow = new BrowserWindow({
        width: (config.mode == "debug") ? 1200 : 1000,
        height: 700,
        resizable: true,
        frame: true,
        maximizable: true,
        minHeight: 700,
        minWidth: (config.mode == "debug") ? 1200 : 1000,
        fullscreenable: true,
        autoHideMenuBar: true,

        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            webSecurity: false,
            preload: path.join(__dirname, "preload.js")
        }

    });

    if (config.mode == "debug") {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.setMenu(null);
    mainWindow.setTitle('Dr Neil\'s Stuff');
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'html',
        slashes: true
    }))

    mainWindow.on('closed', () => {
        mainWindow = null
    })

}

app.on('ready', () => {

    protocol.registerBufferProtocol('html', function(request, callback) {
        let pathName = (new URL(request.url).pathname).substring(os.platform() == 'win32' ? 1 : 0);
        let extension = path.extname(pathName);

        if (extension == "") {
            extension = ".js";
            pathName += extension;
        }

        return callback({ data: fs.readFileSync(path.normalize(pathName)), mimeType: mime.getType(extension) });

    });

    createWindow();

});


ipcMain.on('retrieve', function(event, arg) {
    var data = [];
    var zipfile = path.basename(new URL(arg).pathname);
    var content = "";

    var request = https.get(url.parse(arg), function(response) {
        response.on('data', (chunk) => {
            data.push(chunk);
        });

        response.on('end', function() {
            function getContent(zip) {

                return new Promise(async(accept, reject) => {

                    zip.forEach(async function(relativePath, zipEntry) {

                        if (zipEntry.name.endsWith("manifest.json")) {
                            content = await zipEntry.async("string");
                            accept(content);
                        }

                    })

                });

            }

            var buffer = Buffer.concat(data);

            JSZip.loadAsync(buffer).then(async function(zip) {
                var dir = path.join(__dirname, 'packages');

                fs.mkdirSync(dir, {

                    recursive: true
                }, (err) => {
                    if (err) {
                        event.sender.send('retrieve-complete', err);
                        console.log("error occurred in creating new directory", err);
                        return;
                    }
                });

                var content = await getContent(zip);

                fs.writeFile(path.join(dir, zipfile), buffer, "binary", function(err) {

                    if (err) {
                        console.log(err);
                    }

                });

                event.sender.send('retrieve-complete', content);

            }).then(function(text) {});

        });

    }).on('error', function(err) {
        console.log(err.message);
        event.sender.send('retrieve-complete', err.message);
    });

});

ipcMain.on('load', async function(event, arg) {
    function processZip(data) {

        return new Promise(async(accept, reject) => {
            var zip = new JSZip();
            var manifest = {};

            zip.loadAsync(data).then(async function(zip) {

                var files = zip.filter(function(relativePath, file) {
                    return relativePath.endsWith(".manifest/manifest.json");
                });

                var content = await files[0].async("string");

                manifest = JSON.parse(content);

            }).then(function() {
                accept(manifest);
            });

        });

    }

    var dir = path.join(__dirname, 'packages');
    const files = await fs.promises.readdir(dir);

    var manifests = [];

    for (const file of files) {
        function readZip(filename) {
            return new Promise(async(accept, reject) => {

                fs.readFile(filename, async function(err, data) {

                    if (err) {

                        reject(err);
                    }

                    var manifest = await processZip(data);

                    manifest["filename"] = filename;
                    manifest["base"] = file.replace(".zip", "");


                    accept(manifest);

                });

            });

        }

        var filename = path.join(__dirname, 'packages', file);
        console.log("Loading...", filename);

        var manifest = await readZip(filename)

        manifests.push(manifest);

    }

    console.log("Load Completed...", JSON.stringify(manifests));


    event.sender.send('load-complete', JSON.stringify(manifests));

});