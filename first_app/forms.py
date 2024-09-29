from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your first name','id':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your last name','id':'required'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email','id':'required'}))
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=True
    )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password
    
class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']