from django.contrib import admin
from .models import (Category, Thread, Topic, Post)

# Register your models here.
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Topic)
admin.site.register(Post)