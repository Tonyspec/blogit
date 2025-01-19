from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin


from .models import Post, ProfileUser, Subheading, Article
admin.site.register(Post)
admin.site.register(ProfileUser)
admin.site.register(Subheading)
admin.site.register(Article)