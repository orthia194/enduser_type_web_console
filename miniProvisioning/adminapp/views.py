import boto3
import subprocess
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from botocore.exceptions import ClientError
from decouple import config 
# EC2 인스턴스를 생성하고, 해당 인스턴스에 스크립트를 실행하는 함수
def instance_create(request):
    return render(request, 'instance_create.html')

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
        instance_ids = request.POST.getlist('instanceIds[]')  # JSON 데이터로 전송된 instanceIds를 가져옵니다.

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
        instance_ids = request.POST.getlist('instanceIds[]')  # JSON 데이터로 전송된 instanceIds를 가져옵니다.

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
        instance_ids = request.POST.getlist('instanceIds[]')  # JSON 데이터로 전송된 instanceIds를 가져옵니다.

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

#추가된 코드
def api_endpoint(request):
    data = {"message": "Hello, Node.js!"}
    return JsonResponse(data)

def terminal(request):
    return HttpResponse("This is the terminal view.")
