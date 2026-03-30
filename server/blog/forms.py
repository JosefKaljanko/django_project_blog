from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "content",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "field field--input"}),
            "slug": forms.TextInput(attrs={"class": "field field--input"}),
            "content": forms.Textarea(attrs={"class": "field field--textarea", "rows": 10}),
            "status": forms.Select(attrs={"class": "field field--input"}),
        }