const express = require('express')
const path = require('path')
const app = express()
const port = 3000

app.use('/css', express.static('build/css'));
app.use('/img', express.static('build/img'));
app.use('/script', express.static('build/script'));
// app.use('/html', express.static('build/html'));

app.get('/', function(req, res) {
res.sendFile(path.resolve(__dirname, 'build/index.html')); // default same path as index.html
});

app.listen( process.env.PORT || port, function(err) {
  if (err) {
    console.log(err);
    return;
  }
  console.log('Listening at http://localhost:' + port);
});