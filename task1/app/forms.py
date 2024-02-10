from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect())

    address_line1 = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=6)

    profile_pictures = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','profile_pictures', 'username', 'email', 'password1', 'password2', 'user_type', 'address_line1', 'city', 'state', 'pincode']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Please enter a username.')
        if not username.isalnum():
            raise ValidationError('Username can only contain letters and digits.')
        return username
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)