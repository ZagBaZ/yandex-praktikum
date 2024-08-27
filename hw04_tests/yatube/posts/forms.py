from typing import Type

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model: Type[Post] = Post
        fields = ('text', 'group',)
