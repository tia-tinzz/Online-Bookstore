from django import forms
from django.contrib.auth.forms import User
from.models import Book
class EditForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=('name','author','desc','pdf')