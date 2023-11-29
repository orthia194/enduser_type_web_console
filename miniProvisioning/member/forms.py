# forms.py

from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['id', 'email', 'password']

    def save(self, commit=True):
        member = super(MemberForm, self).save(commit=False)
        member.set_password(self.cleaned_data["password"])
        if commit:
            member.save()
        return member
