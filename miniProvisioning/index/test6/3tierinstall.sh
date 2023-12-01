#!/bin/bash

mkdir dockers was web db

# 커넥터 설치 
echo " 커넥터 설치 시작"
wget https://downloads.mysql.com/archives/get/p/3/file/mysql-connector-java-5.1.40.tar.gz
echo " 커넥터 설치 완료 압축 해제 시작"
tar zxvf mysql-connector-java-5.1.40.tar.gz
echo "압축 해제 완 파일 복사 시작"
cp mysql-connector-java-5.1.40/mysql-connector-java-5.1.40-bin.jar /usr/local/tomcat/lib/
rm -R mysql-*
echo "파일복사 완료 /usr/local/tomcat/lib/ 밑을 확인해주세요"

cd dockers

cat <<EOL > dockerfile.was
from tomcat
workdir /usr/local/tomcat
cmd ["/usr/local/tomcat/bin/catalina.sh", "run"]
EOL

echo "dockerfile.was 파일 생성 완료"

cat <<EOL > dockerfile.db
from mariadb

copy ./data/db_init.sql /docker-entrypoint-initdb.d/
EOL

echo "dockerfile.db 파일 생성 완료"

mkdir data
cd data

cat <<EOL > db_init.sql
create database cloud_op_manager;

use cloud_op_manager;

create table userInfo ( uid int, uname varchar(20), pass varchar(128), profile varchar(200), priority int );

insert into userInfo (uid, uname, pass, profile, priority)values(0, "admin", password("1234"), "관리자", 0);

insert into userInfo (uid, uname, pass, profile, priority)values(1, "user1", password("user1"), "user-1", 1);

insert into userInfo (uid, uname, pass, profile, priority)values(2, "user2", password("user2"), "user-2", 1);

insert into userInfo (uid, uname, pass, profile, priority)values(3, "user3", password("user3"), "user-3", 1);
EOL

echo"/dockers/data 폴더에 sql 파일 생성 완료 수정을 미리 권장드립니다"

cd ..
cd ..

cd web
mkdir conf
cd conf

cat <<EOL > default.conf
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        proxy_pass  http://was:8080;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
EOL

echo "/web/conf/default.conf 파일 생성 완료"

cd ..
cd ..

cd was
mkdir data
cd data

cat <<EOL > test.html
hello!! world!!
EOL

echo "/was/data/test.html 생성 완료 해당 페이지 수정을 권장드립니다"

cd ..
cd ..

cat << EOL> docker-compose.yml
version: "3.0"

services:
  web:
    container_name: Main_Web_Console
    image: nginx
    volumes:
      - ./web/conf/default.conf:/etc/nginx/conf.d/default.conf
    ports:
      - "${WEB_PORT:-80}:80"
    environment:
      - EMPLOYEE_NUMBER=${EMPLOYEE_NUMBER:-1} # Default value if not set
    depends_on:
      - was

  was:
    container_name: Main_Was_Console
    image: tomcat
    build:
      context: ./dockers
      dockerfile: dockerfile.was
    volumes:
      - ./was/data:/usr/local/tomcat/webapps/ROOT
    ports:
      - "${WAS_PORT:-8080}:8080"
    depends_on:
      - db
    environment:
      - EMPLOYEE_NUMBER=${EMPLOYEE_NUMBER:-1} # Default value if not set

  db:
    container_name: Main_DB_Console
    image: mariadb
    build:
      context: ./dockers
      dockerfile: dockerfile.db
    volumes:
      - ./db/data:/var/lib/mysql
    environment:
      MARIADB_ROOT_PASSWORD: abcd

  phpmyadmin:
    container_name: Main_PHP_Console
    image: phpmyadmin
    restart: always
    ports:
      - 9090:8080
    environment:
      - PMA_ARBITRARY=1
EOL

echo "docker-compose.yml 파일 생성 완료"

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

# Docker Compose 실행
export WEB_PORT=$((EMPLOYEE_NUMBER + 1000))
export EMPLOYEE_NUMBER

docker compose build

echo "**************************bulid 완료******************************** "
docker compose up -d

echo "**************************compose up 완료******************************** "
echo "docker ps 커맨드로 모두 올라와 있는지 확인해 주세요. "
