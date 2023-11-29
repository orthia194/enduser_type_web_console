# adminapp/signals.py

import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def create_user_folder(sender, instance, created, **kwargs):
    """
    사용자가 생성될 때 호출되는 시그널 핸들러.
    사용자가 생성되면 폴더를 생성합니다.
    """
    if created:
        folder_name = instance.username  # 또는 instance.id, instance.email 등을 사용할 수 있습니다.
        folder_path = os.path.join('index', folder_name)
        
        try:
            os.makedirs(folder_path)
            print(f"폴더가 생성되었습니다: {folder_path}")
        except OSError as e:
            print(f"폴더 생성 오류: {e}")


