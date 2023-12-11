import os , shutil , subprocess, docker
from .forms import MemberForm
from .models import Member
from django.shortcuts import render, redirect
from django.http import  HttpResponseForbidden, JsonResponse , HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password ,make_password
from django.contrib.auth.decorators import login_required
from adminapp.views import list_ec2_instances



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
            return list_ec2_instances(request)
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
        messages.error(request, '권한이 없습니다.')
    return redirect('login')

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        employee_number = request.POST.get('employee_number')
        member = Member.objects.get(employee_number=employee_number)
  
        # Get the Docker container name based on the member's ID
        container_name = str(member.id)

        # Stop and remove the Docker container
        rm = f'docker rm -f {container_name}'
        print(rm)
        subprocess.run(rm, shell=True)

        # Get the folder path and delete it
        folder_name = str(member.id)
        home_folder_path = os.path.join('/home', folder_name)  # 리눅스 홈 디렉터리에 위치한 폴더 경로
        index_folder_path = os.path.join('./index', folder_name)
        print(home_folder_path)
        print(index_folder_path)
        print("Current working directory:", os.getcwd())
        # ./index/ 디렉터리에 위치한 폴더 경로

        # home디렉터리와 index디렉토리의 id 폴더삭제
        if os.path.exists(index_folder_path):
            shutil.rmtree(index_folder_path)
        if os.path.exists(home_folder_path):
            shutil.rmtree(home_folder_path)
        
        # 리눅스 유저 삭제
        linux_username = str(member.id)
        delUser = f'sudo userdel -r {linux_username}'
        print('리눅스 유저 이름 :', delUser)
        subprocess.run(delUser, shell=True)

        # Delete the member
        member.delete()

        return JsonResponse({'message': 'User deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


def start_docker(request):
    # 사용자의 ID를 가져오기
    user_id = request.POST.get('id')
    
    # (optional) 사용자 객체 전체를 가져오려면
    user = request.user

     #여기서 user_id를 템플릿으로 전달하거나 다른 로직에 활용할 수 있음
    print("Current working directory:", os.getcwd())
    if request.method == 'POST':
         
        user_folder_path = f'./index/{user_id}'
        os.chdir(user_folder_path)
    
        script_path = f'./3tierinstall.sh'

        try: 
            subprocess.run(['/bin/bash', script_path], check=True)
            return HttpResponse("성공적으로 실행되었습니다.")
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error starting Docker: {e}", status=500)

    return render(request, 'test.html', {'user_id': user_id})  # your_template.html은 실제 템플릿 파일명으로 변경해야 합니다.

@login_required
def connect_container(request, container_name):
    username = str(request.user.id)
    
    if container_name != f'{username}_container':
        # 현재 로그인한 사용자와 컨테이너의 이름이 일치하지 않으면 접속 거부
        print('비정상적인 접속 감지')
        return HttpResponseForbidden("본인의 아이디로된 컨테이너는 본인의 아이디로만 접속이 가능합니다.")

    # Docker exec 명령어를 사용하여 컨테이너 내부에 접속
    exec_command = f'docker exec -it {container_name} /bin/bash'
    subprocess.run(exec_command, shell=True)
    print("컨테이너 접속 완료")
    return HttpResponse("컨테이너에 접속하였습니다.")

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        employee_number = request.POST.get('employee_number')
        return render(request, 'reset_password.html', {'employee_number': employee_number })
    else:
        return redirect('admin_view')
    
def perform_password_reset(request):
    if request.method == 'POST':
        employee_number = request.POST.get('employee_number')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:    
            member = Member.objects.get(employee_number=employee_number)
            member.password = make_password(new_password)
            member.save()
            return redirect('admin_view')
        else:
            # Passwords don't match, handle appropriately (redirect to an error page or show a message)
            return redirect('admin_view')
    else:
        return redirect('admin_view')
    
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

            # Docker 컨테이너 생성
            container_name = f'{username}'
            docker_image = 'ubuntu:latest'  # 적절한 Docker 이미지로 수정
            com = f'docker run -d --name {container_name} {docker_image} tail -f /dev/null'
            subprocess.run(com, shell=True)

            # docker 권한 주기
            give_permission = f'sudo usermod -aG docker {container_name}'

            print(give_permission)
          
            subprocess.run(give_permission, shell=True)

            # 리눅스 아이디가 생성된 이후 con_terminal.tar.gz를 복사해서 넣은 후 압축을 푼다음 node server.js를 실행
            con_terminal_path = '/home/' + username
            con_terminal_tar_path = './con_terminal.tar.gz'
            # con_terminal.tar.gz의 실제 경로로 수정
            shutil.copy(con_terminal_tar_path, con_terminal_path)
            
            # con_terminal.tar.gz 압축 해제
            GZ = f'tar -xzvf {os.path.join(con_terminal_path, "con_terminal.tar.gz")} -C {con_terminal_path}'
            subprocess.run(GZ, shell=True)

            # node server.js 실행
            log_file_path = f'/home/project/miniProvisioning/index/{username}/{username}_node_log.txt'
            Nojs = f'cd {con_terminal_path}/con_terminal && sudo -u {username} node server.js > {log_file_path} 2>&1 &'
            subprocess.run(Nojs, shell=True)
           

            return redirect('admin_view')  # 회원 가입 성공 시 login 페이지로 리다이렉트
    else:
        form = MemberForm()

    return render(request, 'signup.html', {'form': form})
     
@login_required
def test(request):
    # 로그인한 사용자의 사용자명 가져오기
    user_id = request.user.id  # 사용자의 ID를 가져오는 방법으로 수정

    # 로그 파일 경로 설정
    log_file_path = f'/home/project/miniProvisioning/index/{user_id}/{user_id}_node_log.txt'
    read = f'cat {log_file_path}'

    # 컨텍스트에 로그 내용 추가
    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()

    return render(request, 'test.html', {'log_content': log_content})
 
def execute_script(script_path, user_id):
    try:
        # 스크립트 실행 및 결과 획득
        # user_folder_path를 절대 경로로 설정
        user_folder_path = os.path.abspath(f'./index/{user_id}')
        
        # 환경 변수 설정
        env = os.environ.copy()
        env["WEB_USER_ID"] = user_id

        # subprocess 모듈을 사용하여 스크립트 실행
        result = subprocess.check_output(['bash', script_path], text=True, env=env, cwd=user_folder_path)

        return result
    except subprocess.CalledProcessError as e:
        # 스크립트 실행 중 오류가 발생한 경우 처리
        return f"에러: {e}"

def start_container(request):
    # 사용자의 ID를 가져오기
    user_id = request.POST.get('id')

    # 여기서 user_id를 템플릿으로 전달하거나 다른 로직에 활용할 수 있음
    print("현재 작업 디렉토리:", os.getcwd())
    if request.method == 'POST':
        # 실행할 스크립트 경로 설정
        script_path = os.path.abspath(f'./index/{user_id}/read_log.sh')
        print(script_path)

        # 스크립트 실행 및 결과 얻기
        script_result = execute_script(script_path, user_id)

        # 템플릿에 전달할 데이터 설정
        context = {
            'user_id': user_id,
            'script_result': script_result,
        }

        # test.html 템플릿을 렌더링하여 응답
        return render(request, 'test.html', context)