import boto3
from datetime import datetime
import pytz

# AWS 계정 및 리전 설정
aws_access_key_id = 'AKIAXHF2E7ODPSGWVBXF'
aws_secret_access_key = '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'
region_name = 'ap-northeast-2'

# Boto3 EC2 클라이언트 생성
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# 한국 표준시 (KST) 타임존 설정
kst = pytz.timezone('Asia/Seoul')

# 현재 실행 중인 모든 EC2 인스턴스 및 해당 인스턴스에 연결된 EBS 볼륨 정보 가져오기
response = ec2_client.describe_instances()
instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

# 각 인스턴스에 대해 스냅샷 생성
for instance in instances:
    instance_id = instance['InstanceId']

    # 인스턴스에 이름이 있는지 확인하고, 없으면 기본값 'UnknownInstance'를 사용합니다.
    instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'UnknownInstance')

    for block_device in instance['BlockDeviceMappings']:
        volume_id = block_device['Ebs']['VolumeId']

        # 현재 시간 (KST) 구하기
        current_time = datetime.now(kst)

        # 스냅샷 설명 설정
        snapshot_description = f'{instance_name} - {current_time.strftime("%Y-%m-%d")}'

        # EBS 스냅샷 생성
        response = ec2_client.create_snapshot(
            Description=snapshot_description,
            VolumeId=volume_id,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': snapshot_description
                        },
                    ]
                },
            ],
        )

        # 스냅샷 ID 확인
        snapshot_id = response['SnapshotId']
        print(f'Snapshot {snapshot_id} created for instance {instance_name} ({instance_id})')
