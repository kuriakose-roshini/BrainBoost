from django import forms
from django.contrib.auth.models import User
from .models import Aspirant
from datetime import date
import re


class AspirantRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Re-enter Password")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    parent_name = forms.CharField(max_length=150, required=False)
    parent_email = forms.EmailField(required=False)

    class Meta:
        model = Aspirant
        fields = ['username', 'email', 'password', 'confirm_password', 'date_of_birth', 'parent_name', 'parent_email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        dob = cleaned_data.get("date_of_birth")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 16:
            if not cleaned_data.get("parent_name") or not cleaned_data.get("parent_email"):
                self.add_error("parent_name", "Parent's name is required for applicants under 16.")
                self.add_error("parent_email", "Parent's email is required for applicants under 16.")

        return cleaned_data


class AspirantLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
