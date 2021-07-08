from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("text", "group")
        labels = {
            "text": "текст",
            "group": "группа"
        }
        help_text = "Введите текст"
