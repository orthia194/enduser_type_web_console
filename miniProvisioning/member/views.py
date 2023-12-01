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
        if _ID == 'admin' and check_password(_PASSWORD, getUserInfoforID.password):
            request.session['username'] = _ID
            return admin_view(request)
        elif check_password(_PASSWORD, getUserInfoforID.password):
            return render(request, 'test.html', {'user_id': _ID})
        else:
            return render(request, 'login.html')
    except Member.DoesNotExist:
        return render(request, 'login.html')
    except Exception as e:
        return render(request, 'login.html')

@login_required(login_url='login')
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
            # 제출된 양식이 유효한 경우, 양식 데이터를 저장하여 새로운 Member 인스턴스를 생성
            member = form.save()

            # 폴더 생성
            folder_name = str(member.id)
            folder_path = os.path.join('index', folder_name)
            os.makedirs(folder_path)

            # SHfile에 있는 파일들을 복사해서 본인의 id 폴더 안에 복사
            shfile_path = 'SHfile'  # SHfile 경로를 적절히 수정

            # SHfile의 모든 파일을 id 폴더로 복사
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            # 사용자의 ID를 현재 접속중인 사용자의 ID로 변경
            user_id = request.user.member.id
            print(user_id)

            script_path = f'/index/{user_id}/3tierinstall.sh'

            try:
                subprocess.run(['bash', script_path], check=True)
                return HttpResponse("성공적으로 실행되었습니다.")
            except subprocess.CalledProcessError as e:
                return HttpResponse(f"Error starting Docker: {e}", status=500)

    return render(request, 'test.html')  # your_template.html은 실제 템플릿 파일명으로 변경해야 합니다.

     
def test(request):
    return render(request, 'test.html')
