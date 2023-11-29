import os , shutil
from .forms import MemberForm
from .models import Member 
from .utils import check_existing_id, check_existing_email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import  JsonResponse
from decouple import config
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password


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
            return render(request, 'test.html')
        else:
            return render(request, 'login.html')
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

def admin_view(request):
    if request.session.get('username') == 'admin':
        users = {}
        # 세션에서 'username' 키의 값이 'admin'인 경우
        users['users'] = Member.objects.all()
        return render(request, 'admin_view.html', users)
    else:
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

        # Delete the member1
        member.delete()

        return JsonResponse({'message': 'User deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

def signup(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()

            # 폴더 생성
            folder_name = str(member.id)
            folder_path = os.path.join('index', folder_name)
            os.makedirs(folder_path)

            return redirect('home')  # 회원 가입 성공 시 home 페이지로 리다이렉트
    else:
        form = MemberForm()

    return render(request, 'signup.html', {'form': form})

    def check_existing_id(request):
        id = request.GET.get('id', '')
        exists = User.objects.filter(username=id).exists()  # 사용자 모델에 따라서 확인 필요

    return JsonResponse({'exists': exists})

    def check_existing_email(request):
        email = request.GET.get('email', '')
        exists = User.objects.filter(email=email).exists()  # 사용자 모델에 따라서 확인 필요

        return JsonResponse({'exists': exists})



def success(request):
    return render(request, 'success.html')  # success.html 템플릿 파일을 렌더링하도록 변경

def test(request):
    return render(request, 'test.html')