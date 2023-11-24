import boto3
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from decouple import config

def home(request):
    return render(request, 'test.html', context={})

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

    # EC2 인스턴스 시작 요청
    response = ec2.run_instances(
        ImageId='AMI_ID',  # 사용할 AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='INSTANCE_TYPE',  # 인스턴스 유형 (예: 't2.micro')
        KeyName='KEY_PAIR_NAME'  # EC2 인스턴스에 연결할 키페어 이름
    )

    # 생성된 인스턴스 ID 가져오기
    instance_id = response['Instances'][0]['InstanceId']

    return HttpResponse(f"EC2 인스턴스가 시작되었습니다. 인스턴스 ID: {instance_id}")