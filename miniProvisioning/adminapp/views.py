import json
import boto3
import requests
import paramiko
import subprocess
from member.models import Member
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from botocore.exceptions import ClientError
from decouple import config
# EC2 인스턴스를 생성하고, 해당 인스턴스에 스크립트를 실행하는 함수
#def instance_create(request):
#    return render(request, 'instance_create.html')

def admin_ec2_view(request):
    if request.session.get('username') == 'admin':
        users = {}
        # 세션에서 'username' 키의 값이 'admin'인 경우
        users['users'] = Member.objects.all()
        return render(request, 'instance_create.html', users)
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect('login')

def start_ec2_instance(request):
    aws_access_key = config('your_aws_access_key')
    aws_secret_key = config('your_aws_secret_key')
    region_name = 'ap-northeast-2'

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    if request.method == 'POST':
        instance_type = request.POST.get('instance_type')
        tag_instance_name = request.POST.get('tag_instance_name')
        tag_instance_hname = request.POST.get('tag_instance_hname')
        tag_instance_pnumber = request.POST.get('tag_instance_pnumber')
        tag_instance_addr = request.POST.get('tag_instance_addr')

        response = ec2.run_instances(
            ImageId='ami-086cae3329a3f7d75',
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName='admin',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': tag_instance_name},
                        {'Key': 'cus_name', 'Value': tag_instance_hname},
                        {'Key': 'cus_pnumber', 'Value': tag_instance_pnumber},
                        {'Key': 'cus_addr', 'Value': tag_instance_addr}
                    ]
                }
            ]
        )

        instance_id = response['Instances'][0]['InstanceId']

        return HttpResponse(f"EC2 인스턴스가 시작되었습니다. 인스턴스 ID: {instance_id}")

    return render(request, 'instance_create.html', context={})

def start_instances(request):
    if request.method == 'POST':
        print(request.POST)
        data = json.loads(request.body)
        instance_ids = data.get('instanceIds')
        #instance_ids = request.POST.getlist('instanceIds')  # JSON 데이터로 전송된 instanceIds를 가져옵니다.
        aws_access_key = config('your_aws_access_key')
        aws_secret_key = config('your_aws_secret_key')
        region_name = 'ap-northeast-2'

        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

        try:
            # EC2 인스턴스들을 시작합니다.
            ec2.start_instances(InstanceIds=instance_ids)
            return JsonResponse({'status': 'success'})  # 처리가 완료되면 성공 응답을 반환합니다.
        except ClientError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})  # 에러가 발생하면 에러 응답을 반환합니다.

    return JsonResponse({'status': 'error', 'message': 'POST method required'})  # POST 요청이 아닐 경우 에러 응답을 반환합니다.

def stop_instances(request):
    if request.method == 'POST':
        print(request.POST)
        data = json.loads(request.body)
        instance_ids = data.get('instanceIds')
        #instance_ids = request.POST.getlist('instanceIds')  # JSON 데이터로 전송된 instanceIds를 가져옵니다.
        aws_access_key = config('your_aws_access_key')
        aws_secret_key = config('your_aws_secret_key')
        region_name = 'ap-northeast-2'
        
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

        try:
            # EC2 인스턴스들을 중지합니다.
            ec2.stop_instances(InstanceIds=instance_ids)
            return JsonResponse({'status': 'success'})  # 처리가 완료되면 성공 응답을 반환합니다.
        except ClientError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})  # 에러가 발생하면 에러 응답을 반환합니다.

    return JsonResponse({'status': 'error', 'message': 'POST method required'})  # POST 요청이 아닐 경우 에러 응답을 반환합니다.

def terminate_instances(request):
    if request.method == 'POST':
        print(request.POST)
        data = json.loads(request.body)
        instance_ids = data.get('instanceIds')
        #instance_ids = request.POST.getlist('instanceIds[]')  # JSON 데이터로 전송된 instanceIds를 가져옵니다.
        aws_access_key = config('your_aws_access_key')
        aws_secret_key = config('your_aws_secret_key')
        region_name = 'ap-northeast-2'

        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

        try:
            # EC2 인스턴스들을 삭제합니다.
            ec2.terminate_instances(InstanceIds=instance_ids)
            return JsonResponse({'status': 'success'})  # 처리가 완료되면 성공 응답을 반환합니다.
        except ClientError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})  # 에러가 발생하면 에러 응답을 반환합니다.

    return JsonResponse({'status': 'error', 'message': 'POST method required'})  # POST 요청이 아닐 경우 에러 응답을 반환합니다.

# EC2 인스턴스 목록을 가져오는 함수
def list_ec2_instances(request):
    aws_access_key = config('your_aws_access_key')
    aws_secret_key = config('your_aws_secret_key')
    region_name = 'ap-northeast-2'

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )

    instances = ec2.describe_instances()

    instance_names = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_names.append(tag['Value'])

    return render(request, 'instance_list.html', {'instances': instances, 'instance_names': instance_names})

def copy_files_to_server():
    scp_commands = [
        'sudo scp -o StrictHostKeyChecking=no -i /home/ubuntu/admin.pem -r /home/ubuntu/webconsole/ ubuntu@52.79.248.11:/home/ubuntu/',
        'sudo scp -o StrictHostKeyChecking=no -i /home/ubuntu/admin.pem -r /etc/systemd/system/orthia_nodejs.service ubuntu@52.79.248.11:/tmp/'
    ]

    for command in scp_commands:
        subprocess.run(command, shell=True, check=True)
    
def execute_remote_commands():
    ssh_key_path = '/home/ubuntu/admin.pem'
    server_ip = '52.79.248.11'
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip, username='ubuntu', key_filename=ssh_key_path)

    commands = [
        'sudo apt update',
        'sudo apt install nodejs -y',
        'sudo apt install npm -y',
        'sudo npm install express socket.io node-pty xterm',
        'sudo mv /tmp/orthia_nodejs.service /etc/systemd/system/',
        'sudo systemctl daemon-reload',
        'sudo systemctl enable orthia_nodejs.service',
        'sudo systemctl start orthia_nodejs.service'
    ]

    for command in commands:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')
        if output:
            print(f"Output: {output}")
        if errors:
            print(f"Errors: {errors}")

    ssh_client.close()
    
def copy_files_view(request):
    copy_files_to_server()
    return HttpResponse("Files copied to server successfully.")

def execute_commands_view(request):
    execute_remote_commands()
    return HttpResponse("Remote commands executed successfully.")

#추가된 코드
def api_endpoint(request):
    data = {"message": "Hello, Node.js!"}
    return JsonResponse(data)
def terminal(request):
    # Node.js 서버의 URL 설정
    nodejs_url = 'http://15.165.251.209:3000'

    # Node.js 서버로 GET 요청을 보내서 결과를 받아옴
    response = requests.get(nodejs_url)

    # Node.js 서버의 응답을 HttpResponse로 반환
    return HttpResponse(response.text)
def index(request):
    return render(request, 'index.html')
