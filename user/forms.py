from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Comment


User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(required=False, widget=forms.FileInput())
    first_name  = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Your first name",
        "class": "form-control",
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        "class": "form-control",
    }))
    gender = forms.ChoiceField(required=False, choices=User.GENDER_CHOICES, widget=forms.Select(attrs={
        "placeholder": "Choose...", 
        "class": "form-control",
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        "placeholder": "Your email",
        "class": "form-control",
    }))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your first address',
        "class": "form-control",
    }))
    address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your second address',
        "class": "form-control"
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your sity',
        "class": "form-control",
    }))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your state',
        "class": "form-control",
    }))
    zip = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Your zip',
        "class": "form-control",
    })) 


    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", "username", "email", "address", "address2", "image", "city", "zip"]
        

class CommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your messeng',
    }))
    class Meta:
        model = Comment
        fields = ['text']
        exclude = ['create_time']

# пароль 11
# пароль 1dsdsdsw!