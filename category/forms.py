from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Bạn đang nghĩ gì?'}
    ))

    class Meta:
        model = Topic
        fields = ['title', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']