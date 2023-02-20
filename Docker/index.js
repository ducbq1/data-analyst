const http = require('http')

const server = http.createServer((req, res) => {
  res.end('Hello kubernetes\n')
})

server.listen(3000, () => {
  console.log('Serverlisten on port 3000')
})