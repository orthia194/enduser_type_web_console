const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const pty = require('node-pty');
const app = express();
const server = http.createServer(app); // 서버를 생성하는 데에는 http.createServer()를 사용합니다.
const io = socketIO(server); // io 객체를 생성하는 데에는 socketIO()를 사용합니다.
const getApiEndpoint = require('./apiRequests');

getApiEndpoint().then(data => console.log(data));
app.use('/static/', express.static('/home/project/miniProvisioning/static_root/'));

io.on('connection', (socket) => {
    const shell = pty.spawn('bash', [], {
        name: 'xterm-color',
        cwd: process.env.HOME,
        env: process.env
    });

    shell.on('data', (data) => {
        socket.emit('output', data);
    });

    socket.on('input', (data) => {
        shell.write(data);
    });

    socket.on('resize', (size) => {
        shell.resize(size.cols, size.rows);
    });

    socket.on('disconnect', () => {
        shell.kill();
    });
});

const PORT = process.env.PORT || 3000;

// 서버가 이미 리스닝 중이지 않은 경우에만 listen을 호출합니다.
if (!server.listening) {
    server.listen(PORT, () => {
        console.log(`Node.js 서버가 포트 ${PORT}에서 실행 중입니다.`);
    });
} else {
    console.log('서버가 이미 실행 중입니다.');
}
