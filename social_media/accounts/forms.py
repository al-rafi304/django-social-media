from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', 'dob', 'username', 'email', 'password1', 'password2', 'profile_img', 'cover_img')

        labels = {
            'first_name': 'Name',
            'dob': 'Date of Birth (YYYY-MM-DD)',
            'profile_img': 'Profile Picture',
            'cover_img': 'Cover Picture'
        }

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        class_attr = 'form-control rounded-4'

        # HTML class attributes
        self.fields['first_name'].widget.attrs['class'] = class_attr
        self.fields['username'].widget.attrs['class'] = class_attr
        self.fields['email'].widget.attrs['class'] = class_attr
        self.fields['password1'].widget.attrs['class'] = class_attr
        self.fields['password2'].widget.attrs['class'] = class_attr
        self.fields['dob'].widget.attrs['class'] = class_attr
        self.fields['profile_img'].widget.attrs['class'] = class_attr
        self.fields['cover_img'].widget.attrs['class'] = class_attr