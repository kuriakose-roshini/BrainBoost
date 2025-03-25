# Admin/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomAdmin


class CustomAdminRegistrationForm(UserCreationForm):
    """
    Registration form for Admin
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomAdmin
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'phone_number'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        user.is_superuser = True  # Give full access

        if commit:
            user.save()
        return user


class CustomAdminLoginForm(AuthenticationForm):
    """
    Custom login form for admin
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )