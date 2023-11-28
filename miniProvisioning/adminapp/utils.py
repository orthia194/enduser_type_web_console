# utils.py

from django.http import JsonResponse
from .models import Member

def check_existing_id(request):
    id = request.GET.get('id', '')
    exists = Member.objects.filter(id=id).exists()
    return JsonResponse({'exists': exists})

def check_existing_email(request):
    email = request.GET.get('email', '')
    exists = Member.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
