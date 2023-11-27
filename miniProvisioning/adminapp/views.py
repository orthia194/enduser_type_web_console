import boto3
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from decouple import config
from .forms import MemberForm
from .models import Member
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, 'home.html')

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

def signup(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()

            # 폴더 생성
            folder_name = member.id
            folder_path = os.path.join('index', folder_name)
            os.makedirs(folder_path)

            return redirect('success')  # 회원 가입 성공 페이지로 리다이렉트
    else:
        form = MemberForm()

    return render(request, 'signup.html', {'form': form})

def success(request):
    # 회원 가입 성공 후 로그인 처리
    if request.method == 'POST':
        username = request.POST['id']  # 사용자가 입력한 아이디 필드 이름에 맞게 수정
        password = request.POST['password']  # 사용자가 입력한 비밀번호 필드 이름에 맞게 수정
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('login')  # 로그인이 성공하면 로그인 페이지로 이동
        else:
            # 로그인 실패 시 원하는 처리 추가
            pass

    return render(request, 'login.html')