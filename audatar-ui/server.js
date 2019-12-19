const express = require('express')
const path = require('path')
const app = express()

app.use(express.static(path.join(__dirname, 'build')))

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
})

app.all('/alive.txt', function(req, res){
  res.status(200).json('OK');
})

app.listen(5000, () => console.log('Audatar UI listening on port 5000!'))
