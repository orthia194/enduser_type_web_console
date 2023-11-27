import boto3
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from decouple import config
from .forms import MemberForm
from .models import Member
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('test')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

@login_required
def home(request):
    return render(request, 'test.html')

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

            return redirect('home')  # 회원 가입 성공 시 test 페이지로 리다이렉트
    else:
        form = MemberForm()

    return render(request, 'signup.html', {'form': form})

def success(request):
    return render(request, 'success.html')  # success.html 템플릿 파일을 렌더링하도록 변경

def test(request):
    return render(request, 'test.html')