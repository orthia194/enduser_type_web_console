var term = new Terminal();
term.open(document.getElementById('terminal'));

var socket = io.connect();

socket.on('connect', function () {
    term.onData(function (data) {
        socket.emit('input', data);
    });

    term.onResize(function (size) {
        socket.emit('resize', { col: size.cols, row: size.rows });
    });

    socket.on('output', function (data) {
        term.write(data);
    });

    term.resize(window.innerWidth / 10, window.innerHeight / 17);
});

