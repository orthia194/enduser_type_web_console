# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import os

@receiver(post_save, sender=get_user_model())
def create_user_folder(sender, instance, created, **kwargs):
    if created:
        # 폴더를 생성할 디렉터리 경로 설정
        base_folder = "/templates/index/"

        # 사용자의 사원번호를 폴더명으로 사용
        user_folder = os.path.join(base_folder, str(instance.employee_number))

        # 폴더를 생성
        os.makedirs(user_folder, exist_ok=True)
