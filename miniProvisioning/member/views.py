from logging.config import IDENTIFIER
import os , shutil , subprocess
from .forms import MemberForm
from .models import Member 
from django.shortcuts import render, redirect
from django.http import  JsonResponse , HttpResponse
from decouple import config
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

@csrf_exempt
def loginCheck(request):
    request.session['username'] = ''
    _ID = request.POST.get('id')
    _PASSWORD = request.POST.get('password')

    try:
        getUserInfoforID = Member.objects.get(id=_ID)
        myID = getUserInfoforID.id
        if _ID == 'admin' and check_password(_PASSWORD, getUserInfoforID.password):
            request.session['username'] = _ID
            return admin_view(request)
        elif check_password(_PASSWORD, getUserInfoforID.password):
            # 안전하게 사용자 ID 전달
            return render(request, 'test.html', {'user_id': myID})
        else:
            return render(request, 'login.html')
    except Member.DoesNotExist:
        return render(request, 'login.html')
    except Exception as e:
        return render(request, 'login.html')

def admin_view(request):
    if request.session.get('username') == 'admin':
        users = {}
        # 세션에서 'username' 키의 값이 'admin'인 경우
        users['users'] = Member.objects.all()
        return render(request, 'admin_view.html', users)
    else:
        print("abd")
        messages.error(request, '권한이 없습니다.')
    return redirect('login')

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        employee_number = request.POST.get('employee_number')
        member = Member.objects.get(employee_number=employee_number)

        # Get the folder path and delete it
        folder_name = str(member.id)
        print(folder_name)
        folder_path = os.path.join('index', folder_name)
        print(folder_path)

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Delete the member
        member.delete()

        return JsonResponse({'message': 'User deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

def signup(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            # 양식 데이터 저장 및 Member 인스턴스 생성
            member = form.save()

            # 회원의 id를 사용하여 Linux 사용자 생성
            username = str(member.id)
            password = form.cleaned_data['password']  # 이 부분은 실제 비밀번호 필드 이름으로 수정
            subprocess.run(f'sudo adduser --disabled-password --gecos "" {username}', shell=True)

            # 비밀번호 설정
            subprocess.run(f'sudo echo "{username}:{password}" | sudo chpasswd', shell=True)

            # 폴더 생성
            folder_name = username
            folder_path = os.path.join('index', folder_name)
            os.makedirs(folder_path)

            # SHfile의 파일들을 id 폴더로 복사
            shfile_path = 'SHfile'  # SHfile 경로를 적절히 수정

            for filename in os.listdir(shfile_path):
                file_path = os.path.join(shfile_path, filename)
                if os.path.isfile(file_path):
                    destination_file_path = os.path.join(folder_path, filename)
                    shutil.copy(file_path, destination_file_path)

            return redirect('login')  # 회원 가입 성공 시 login 페이지로 리다이렉트
    else:
        form = MemberForm()

    return render(request, 'signup.html', {'form': form})

def start_docker(request):
    # 사용자의 ID를 가져오기
    user_id = request.POST.get('id')
    print(user_id)
    
    # (optional) 사용자 객체 전체를 가져오려면
    user = request.user

     #여기서 user_id를 템플릿으로 전달하거나 다른 로직에 활용할 수 있음
    print("Current working directory:", os.getcwd())
    if request.method == 'POST':
         script_path = f'./index/{user_id}/3tierinstall.sh'

         try: 
            subprocess.run(['/bin/bash', script_path], check=True)
            return HttpResponse("성공적으로 실행되었습니다.")
         except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error starting Docker: {e}", status=500)

    return render(request, 'test.html', {'user_id': user_id})  # your_template.html은 실제 템플릿 파일명으로 변경해야 합니다.

     
def test(request):
    return render(request, 'test.html')
