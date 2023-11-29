import boto3, os
from .forms import MemberForm
from .models import Member 
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from decouple import config

def instance_create(request):
    return render(request, 'instance_create.html', context={})
def start_ec2_instance(request):
    # AWS 자격 증명 설정
    aws_access_key = config('your_aws_access_key')
    aws_secret_key = config('your_aws_secret_key')
    region_name = 'ap-northeast-2'

    # AWS 자격 증명을 사용하여 Boto3 클라이언트 생성
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
    # EC2 인스턴스 시작 요청
    response = ec2.run_instances(
        ImageId='ami-01123b84e2a4fba05',  # 사용할 AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,  # 인스턴스 유형 (예: 't2.micro')
        KeyName='admin',  # EC2 인스턴스에 연결할 키페어 이름
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': tag_instance_name},  # 인스턴스 이름 지정
                    {'Key': 'cus_name', 'Value': tag_instance_hname},  # 고객 정보 태그 추가
                    {'Key': 'cus_pnumber', 'Value': tag_instance_pnumber},  # 고객 정보 태그 추가
                    {'Key': 'cus_addr', 'Value': tag_instance_addr}  # 고객 정보 태그 추가
                ]
            }
        ]
    )

    # 생성된 인스턴스 ID 가져오기
    instance_id = response['Instances'][0]['InstanceId']

    return HttpResponse(f"EC2 인스턴스가 시작되었습니다. 인스턴스 ID: {instance_id}")


    return render(request, 'test.html')
def list_ec2_instances(request):
    # AWS 자격 증명 설정
    aws_access_key = config('your_aws_access_key')
    aws_secret_key = config('your_aws_secret_key')
    region_name = 'ap-northeast-2'

    # AWS 자격 증명을 사용하여 Boto3 클라이언트 생성
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )

    # EC2 인스턴스 목록 가져오기
    instances = ec2.describe_instances()
    
 # 각 인스턴스의 이름 가져오기
    instance_names = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    instance_names.append(tag['Value'])

    # 인스턴스 목록과 인스턴스 이름들을 HTML에 전달
    return render(request, 'instance_list.html', {'instances': instances, 'instance_names': instance_names})