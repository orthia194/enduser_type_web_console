#!/bin/bash


# 웹훅 실행
WEBHOOK_URL="https://discord.com/api/webhooks/1183965268691648542/ANJW2ALqp-RPnTW8Z9lf5Ue0MUArgWamSndEl2h6B732uQiUAnpyGcAUZts6ZZHKdNgK" # 실제 웹훅 URL로 변경
WEBHOOK_DATA='{"content": "실행되었습니다." "username": "내 봇"}' # 필요에 따라 데이터를 변경하세요
curl -X POST -H "Content-Type: application/json" -d "$WEBHOOK_DATA" $WEBHOOK_URL
# 시작 시간 기록
start_time=$(date +%s)

ip_address=$1

echo "Copying files to $ip_address..."
sudo scp -o StrictHostKeyChecking=no -i /home/project/admin.pem -r /home/ubuntu/webconsole/ ubuntu@$ip_address:/home/ubuntu/
sudo scp -o StrictHostKeyChecking=no -i /home/project/admin.pem -r /etc/systemd/system/orthia_nodejs.service ubuntu@$ip_address:/tmp/
echo "Files copied successfully to $ip_address"

echo "Connecting to server $ip_address..."
ssh -o StrictHostKeyChecking=no -i /home/project/admin.pem ubuntu@$ip_address << 'EOF'
    echo "Running updates..."
    sudo apt update
    echo "Installing nodejs..."
    sudo apt install nodejs -y
    echo "Installing npm..."
    sudo apt install npm -y
    echo "Installing Node.js packages..."
    sudo npm install express socket.io node-pty xterm
    echo "Moving orthia_nodejs.service..."
    sudo mv /tmp/orthia_nodejs.service /etc/systemd/system/
    echo "Reloading daemon..."
    sudo systemctl daemon-reload
    echo "Enabling orthia_nodejs.service..."
    sudo systemctl enable orthia_nodejs.service
    echo "Starting orthia_nodejs.service..."
    sudo systemctl start orthia_nodejs.service
    echo "Script execution completed on $ip_address"
    
EOF

# 종료 시간 기록 및 실행 시간 계산
end_time=$(date +%s)
elapsed_time=$((end_time - start_time))

# 실행 시간 확인 및 결과 처리
if [ $elapsed_time -le 300 ]; then
    WEBHOOK_DATA='{"content": "정상적으로 처리됐습니다." "username": "내 봇"}' # 필요에 따라 데이터를 변경하세요
    curl -X POST -H "Content-Type: application/json" -d "$WEBHOOK_DATA" $WEBHOOK_URL
else
    WEBHOOK_DATA='{"content": "초과했습니다. 에러로 처리합니다." "username": "내 봇"}' # 필요에 따라 데이터를 변경하세요
    curl -X POST -H "Content-Type: application/json" -d "$WEBHOOK_DATA" $WEBHOOK_URL
fi