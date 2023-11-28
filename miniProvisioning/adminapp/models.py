# models.py

from django.db import models

class Member(models.Model):
    employee_number = models.AutoField(primary_key=True)
    id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
