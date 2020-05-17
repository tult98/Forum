from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
import math
from django.utils.html import mark_safe
from markdown import markdown
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

    def get_list_thread(self):
        return self.threads.order_by('id')

    def get_absolute_url(self):
        return reverse('admin_home')


class Thread(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, related_name='threads', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objects.filter(topic__thread=self).count()
    
    def get_topic_count(self):
        return Topic.objects.filter(ischecked=True, thread=self).count()

    def get_last_topic(self):
        return self.topics.filter(ischecked=True).order_by('-last_updated').first()
    
    def get_absolute_url(self):
        return reverse('admin_threads')
    
class Topic(models.Model):
    title = models.CharField(max_length=255, blank=False)
    message = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    ischecked = models.BooleanField(default=False)
    thread = models.ForeignKey(Thread, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)

    def __str__(self):
        truncated_title = Truncator(self.title)
        return truncated_title.chars(30)
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


    def get_post_count(self):
        return self.posts.count()
    
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 2
        return math.ceil(pages)
    
    def get_topics_by_user(self):   
        current_user = self.request.user
        return self.objects.filter(starter=current_user)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6
    
    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)
    
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]
    
    def get_absolute_url(self):
        return reverse('admin_topics1')

class Post(models.Model):
    content = models.TextField()
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    
    def __str__(self):
        truncated_message = Truncator(self.content)
        return truncated_message.chars(30)
    
    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def get_absolute_url(self):
        return reverse('admin_posts')

