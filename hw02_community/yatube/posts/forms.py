from django import forms
from .models import *


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Post
        fields = ('text', 'group')