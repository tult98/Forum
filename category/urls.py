from django.urls import path, include, re_path
from .views import (
    CategoryListView, 
    TopicListView,
    PostListView,
    new_topic,
    reply_topic
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    re_path(r'^threads/(?P<pk>\d+)/$', TopicListView.as_view(), name='thread_topics'),
    re_path(r'^threads/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', PostListView.as_view(), name='topic_posts'),
    re_path(r'^threads/(?P<pk>\d+)/new/$', new_topic, name='new_topic'),
    re_path(r'^threads/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', reply_topic, name='reply_topic'),
]
