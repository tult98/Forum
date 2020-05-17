from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from category.models import (
    Category,
    Thread, 
    Topic, 
    Post
)

# Create your views here.


class CategoryListView(LoginRequiredMixin, ListView):
    login_url = '/admin/login/'
    model = Category
    context_object_name = 'categories'
    template_name = 'admin_home.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            queryset = Category.objects.filter(
                Q(name__icontains=query)
            )
        else: 
            queryset = Category.objects.all()
        return queryset

class CategoryCreateView(CreateView):
    model = Category
    template_name='category_form.html'
    fields = ['name', 'description']

class ThreadCreateView(CreateView):
    model = Thread
    template_name = 'thread_form.html'
    fields = ['name', 'description', 'category']

class ThreadListView(ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = 'admin_threads.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            queryset = Thread.objects.filter(
                Q(name__icontains=query)
            )
        else: 
            queryset = Thread.objects.all()
        return queryset

class TopicListView1(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'admin_topics.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            queryset = Topic.objects.filter(
                Q(title__icontains=query)
            )
        else: 
            queryset = Topic.objects.filter(ischecked=True)
        return queryset

class TopicListView2(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'admin_topics.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            queryset = Topic.objects.filter(
                Q(title__icontains=query)
            )
        else: 
            queryset = Topic.objects.filter(ischecked=False)
        return queryset

class TopicCreateView(CreateView):
    model = Topic
    template_name = 'topic_form.html'
    fields = ['title', 'message', 'thread', 'ischecked']

    def form_valid(self, form):
        form.instance.starter = self.request.user
        return super().form_valid(form)

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['content', 'topic']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'admin_posts.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            queryset = Post.objects.filter(
                Q(content__icontains=query)
            )
        else: 
            queryset = Post.objects.all()
        return queryset

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('admin_posts')

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = "topic_confirm_delete.html"
    success_url = reverse_lazy('admin_topics1')

class ThreadDeleteView(DeleteView):
    model = Thread
    template_name = 'thread_confirm_delete.html'
    success_url = reverse_lazy('admin_threads')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('admin_home')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['content']
    template_name = 'post_update_form.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TopicUpdateView(UpdateView):
    model = Topic
    fields = ['title', 'message', 'ischecked']
    template_name = 'topic_update_form.html'

class ThreadUpdateView(UpdateView):
    model = Thread
    fields = ['name', 'description']
    template_name = 'thread_update_form.html'

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'category_update_form.html'