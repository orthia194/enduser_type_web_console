import json
import boto3
import requests
import paramiko
import subprocess
from member.models import Member
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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

def run_script(request):
    if request.method == 'POST':
        try:
            # POST로 받은 JSON 데이터 추출
            data = json.loads(request.body)
            ip_address = data.get('ip_address')  # JSON 데이터에서 필요한 값 추출

            # 쉘 스크립트 실행
            subprocess.run(['bash', '/home/project/setup_script.sh', ip_address], check=True)

            return JsonResponse({"message": "Script executed successfully"})
        except Exception as e:
            return JsonResponse({"message": f"Error: {e}"}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=400)

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
