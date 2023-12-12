#!/bin/bash

# 사용자 ID를 받아옴
user_id=$(whoami)

# 로그 파일 경로 설정
log_file_path="/home/project/miniProvisioning/index/${user_id}/${user_id}_node_log.txt"

# 로그 파일 내용 출력
cat $log_file_path
