from django.contrib.auth.models import User
from .models import BookReview, CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

# class UserChangeForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'photo']

