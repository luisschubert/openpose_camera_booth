const express = require('express');
const fs = require('fs');
const app = express();
app.use('/gallery',express.static(__dirname+'/gallery'));
app.use('/savePhoto',express.static(__dirname+'/savePhoto'));


app.set('port', 7777);
app.get('/gallery/:photoid', (req, res) => {
    var photoid = request.params.photoid;
    fs.readFile('gallery.html', (err, data) => {
        if(err) {
            res.statusCode = 500;
        }
        else {
            res.setHeader('Content-type','text/html');
            templated = util.format(data.toString(),photoid.toString())
            res.end(Buffer.from(templated));
        }
    })
});
app.listen(app.get('port'), () => {
    console.log(`Node.js server is running`);
    console.log(`Listening for clients on port ${app.get('port')}`);
    console.log('http://localhost:7777');
    console.log('http://127.0.0.1:7777');
})
