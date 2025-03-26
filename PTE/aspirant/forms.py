# forms.py in your aspirant app
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Aspirant
from datetime import date


class AspirantRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="We need this to verify if parental consent is required"
    )
    parent_email = forms.EmailField(
        required=False,
        help_text="Required only if you're under 16 years old"
    )

    class Meta:
        model = Aspirant
        fields = ('username', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'parent_email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        parent_email = cleaned_data.get('parent_email')

        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            if age < 16 and not parent_email:
                self.add_error(
                    'parent_email',
                    "Parent email is required for users under 16 years old."
                )

        return cleaned_data

class AspirantLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
