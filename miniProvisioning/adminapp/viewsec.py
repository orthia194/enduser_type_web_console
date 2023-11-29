import boto3
import subprocess
from django.shortcuts import render
from django.http import HttpResponse
from decouple import config

# EC2 인스턴스를 생성하고, 해당 인스턴스에 스크립트를 실행하는 함수
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

        # EC2 인스턴스 상태 확인 및 스크립트 실행
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        while instance['Reservations'][0]['Instances'][0]['State']['Name'] != 'running':
            instance = ec2.describe_instances(InstanceIds=[instance_id])

        # SCP를 사용하여 스크립트 파일을 EC2로 전송
        public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        subprocess.run(["scp", "-i", "/home/project/admin.pem", "/home/project/script.sh", f"ubuntu@{public_ip}:/home/ubuntu"])

        # SSH를 통해 EC2에 연결하여 스크립트 실행
        script_path = '/home/ubuntu/script.sh'  # 스크립트 경로
        command = f"sh {script_path}"
        subprocess.run(f"ssh -i /home/project/admin.pem ubuntu@{public_ip} {command}", shell=True)

        return HttpResponse(f"EC2 인스턴스가 시작되었습니다. 인스턴스 ID: {instance_id}")

    return render(request, 'instance_create.html', context={})
