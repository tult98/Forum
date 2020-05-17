from django import forms
from category.models import Category, Topic, Post, Thread


# class NewTopicForm(forms.ModelForm):
#     message = forms.CharField(widget=forms.Textarea(
#         attrs={'rows': 5, 'placeholder': 'Bạn đang nghĩ gì?'}
#     ))

#     class Meta:
#         model = Topic
#         fields = ['title', 'message']

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['content']

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'description']

# class ThreadForm(forms.ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.all())
#     class Meta:
#         model = Thread
#         fields = ['name', 'description', 'category']