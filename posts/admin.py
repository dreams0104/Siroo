from django.contrib import admin
from .models import Post
from .models import Comment
from .models import Tag, User_profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(User_profile)
# Register your models here.
