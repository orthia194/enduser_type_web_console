#!/bin/bash

# Gunicorn 서비스 시작
start() {
    sudo systemctl start gunicorn-orthia
}

# Gunicorn 서비스 중지
stop() {
    sudo systemctl stop gunicorn-orthia
}

# Gunicorn 서비스 재시작
restart() {
    sudo systemctl restart gunicorn-orthia
}

# 명령어에 따라 실행
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0

