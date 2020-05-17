from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewTopicForm, PostForm
from django.db.models import Q
from .models import (
    Category,
    Thread, 
    Topic, 
    Post
)

# Create your views here.

class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'home.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            queryset = Category.objects.filter(
                Q(name__icontains=query)
            )
        else: 
            queryset = Category.objects.all()
        return queryset

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'

    def get_context_data(self, **kwargs):
        kwargs['thread'] = self.thread
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, pk=self.kwargs.get('pk'))
        query = self.request.GET.get('q')
        if (query):
            queryset = self.thread.topics.filter(
                Q(title__icontains=query)
            ).order_by('-last_updated')
        else: 
            queryset = self.thread.topics.order_by('-last_updated')
        return queryset
        # queryset = self.thread.topics.order_by('-last_updated')
        # return queryset

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, thread__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def new_topic(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.thread = thread
            topic.starter = user
            topic.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'thread': thread, 'form': form})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, thread__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})