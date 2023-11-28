import boto3, os
from .forms import MemberForm
from .models import Member 
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from decouple import config
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .utils import check_existing_id, check_existing_email

def home(request):
    return render(request, 'test.html', context={})

@csrf_exempt
def loginCheck(request):
    request.session['username'] = ''
    _ID = request.POST.get('id')
    _PASSWORD = request.POST.get('password')

    try:
        getUserInfoforID = Member.objects.get(id=_ID)
        if _ID == 'admin':
            request.session['username'] = _ID
            return admin_view(request)  # admin_view를 직접 호출
        else:
            return render(request, 'test.html')
    except Member.DoesNotExist:
        return render(request, 'login.html')
    except Exception as e:
        return render(request, 'login.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('test')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

#@user_passes_test(lambda u: u.is_staff, login_url='login')
def admin_view(request):
    print(request.session.get('username'))

    if request.session.get('username') == 'admin':
        print('a')
        users = {}
        # 세션에서 'username' 키의 값이 'admin'인 경우
        users['users'] = Member.objects.all()
        
        print(users)
        return render(request, 'admin_view.html', users)
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect('login')

#@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_user(request, user_id):
    try:
        user = Member.objects.get(id=user_id)
        user.delete()
        return redirect('admin_view')
    except Member.DoesNotExist:
        return redirect('admin_view')
from django.contrib.auth import login



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
        ImageId='ami-01123b84e2a4fba05',  # 사용할 AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',  # 인스턴스 유형 (예: 't2.micro')
        KeyName='admin',  # EC2 인스턴스에 연결할 키페어 이름
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'orthia-test'},  # 인스턴스 이름 지정
                    {'Key': 'Customer', 'Value': '홍길동'}  # 고객 정보 태그 추가
                ]
            }
        ]
    )

    # 생성된 인스턴스 ID 가져오기
    instance_id = response['Instances'][0]['InstanceId']

    return HttpResponse(f"EC2 인스턴스가 시작되었습니다. 인스턴스 ID: {instance_id}")

def signup(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()

            user = form.save(commit=False)
            # 비밀번호를 암호화하여 저장
            user.set_password(form.cleaned_data['password1'])
            user.save()

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