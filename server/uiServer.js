const express = require('express');
const fs = require('fs');
const app = express();
app.use(express.static('public'));

app.set('port', 7777);
app.get('/photoCaptureInformation', (req, res) => {
    fs.readFile('photoCaptureInformation.html', (err, data) => {
        if(err) {
            res.statusCode = 500;
        }
        else {
            res.setHeader('Content-type','text/html');
            res.end(data);
        }
    })
});

app.get('/photoCaptureCountdown', (req, res) => {
    fs.readFile('photoCaptureCountdown.html', (err, data) => {
        if(err) {
            res.statusCode = 500;
        }
        else {
            res.setHeader('Content-type','text/html');
            res.end(data);
        }
    })
});
app.get('/savePhoto', (req, res) => {
    fs.readFile('savePhoto.html', (err, data) => {
        if(err) {
            res.statusCode = 500;
        }
        else {
            res.setHeader('Content-type','text/html');
            res.end(data);
        }
    })
});
app.get('/photoGalleryInformation', (req, res) => {
    fs.readFile('photoGalleryInformation.html', (err, data) => {
        if(err) {
            res.statusCode = 500;
        }
        else {
            res.setHeader('Content-type','text/html');
            res.end(data);
        }
    })
});
app.get('/photoGallery', (req, res) => {
    fs.readFile('photoGallery.html', (err, data) => {
        if(err) {
            res.statusCode = 500;
        }
        else {
            res.setHeader('Content-type','text/html');
            res.end(data);
        }
    })
});
app.listen(app.get('port'), () => {
    console.log(`Node.js server is running`);
    console.log(`Listening for clients on port ${app.get('port')}`);
    console.log('http://localhost:7777');
    console.log('http://127.0.0.1:7777');
})
