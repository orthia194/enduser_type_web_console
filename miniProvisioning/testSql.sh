#!/bin/bash

# MySQL 연결 정보
MYSQL_HOST="database-1.c26odpmo5jsk.ap-northeast-2.rds.amazonaws.com"
MYSQL_USER="admin"
MYSQL_PASSWORD="wkdrbgus"
MYSQL_DATABASE="member"

CURRENT_USER_ID=$(whoami)
echo $CURRENT_USER_ID

# SQL 쿼리
SQL_QUERY="SELECT employee_number FROM member WHERE id = '$CURRENT_USER_ID';"

# MySQL 쿼리 실행
EMPLOYEE_NUMBER=$(mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "$SQL_QUERY" --batch --skip-column-names)

# 결과 출력
echo $EMPLOYEE_NUMBER

export WEB_PORT=$((EMPLOYEE_NUMBER + 1000))
export EMPLOYEE_NUMBER
docker-compose up -d