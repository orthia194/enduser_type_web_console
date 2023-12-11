#!/bin/bash

# Copy files
sudo scp -o StrictHostKeyChecking=no -i /home/project/admin.pem -r /home/ubuntu/webconsole/ ubuntu@52.78.224.192:/home/ubuntu/
sudo scp -o StrictHostKeyChecking=no -i /home/project/admin.pem -r /etc/systemd/system/orthia_nodejs.service ubuntu@52.78.224.192:/tmp/

# SSH into the server
ssh -o StrictHostKeyChecking=no -i /home/project/admin.pem ubuntu@52.78.224.192<< 'EOF'
    sudo apt update
    sudo apt install nodejs -y
    sudo apt install npm -y
    sudo npm install express socket.io node-pty xterm
    sudo mv /tmp/orthia_nodejs.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable orthia_nodejs.service
    sudo systemctl start orthia_nodejs.service
EOF

