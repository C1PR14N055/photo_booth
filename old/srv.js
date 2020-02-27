let express = require('express')
let ws = require('ws')
let fs = require('fs')

let port = 3000;
let picFolder = './pics';
let app = express()

// app.use(express.static('/home/pi/selphone/assets/'))
app.use(express.static('.'));

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/views/index.html')
})

app.get('/people', function (req, res) {
  res.sendFile(__dirname + '/views/people.html')
})

app.get('/photos', function (req, res) {
  let html = '<style> html, body { margin: 0; padding: 0; background: #111; } </style>';
  fs.readdirSync(picFolder).forEach((file) => {
    html += '<a target="_blank" href="/pics/' + file + '"><img style="max-width: calc(20% - 20px); margin: 10px; float: left;" src="/pics/' + file + '"></a>';
  })
  res.writeHeader(200, {
    "Content-Type": "text/html"
  });
  res.write(html);
  res.end();
})

app.listen(port, function () {
  console.log('Runnig on port', port)
})

wss = new ws.Server({
  port: 40510
})

wss.on('connection', function (ws) {
  ws.on('message', function (data) {
    write(data)
    sendToAll()
  })
  sendToAll()
})

function sendToAll() {
  data = JSON.stringify(read())
  wss.clients.forEach(function each(ws) {
    try {
      ws.send(data);
    } catch (e) {
      // ws closed
    }
  });
}

function write(data) {
  fs.writeFileSync('data.json', data)
}

function read() {
  return JSON.parse(fs.readFileSync('data.json').toString())
}