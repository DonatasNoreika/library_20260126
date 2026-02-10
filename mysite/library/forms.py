from django.contrib.auth.models import User
from .models import BookReview
from django import forms


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

