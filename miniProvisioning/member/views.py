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