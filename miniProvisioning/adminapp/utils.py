# utils.py

from django.http import JsonResponse
from django.contrib.auth.models import User

def check_existing_id(request):
    id = request.GET.get('id', '')
    exists = User.objects.filter(username=id).exists()
    return JsonResponse({'exists': exists})

def check_existing_email(request):
    email = request.GET.get('email', '')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
