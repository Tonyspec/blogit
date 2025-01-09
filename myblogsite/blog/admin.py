from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin


from .models import Post, ProfileUser
admin.site.register(Post)
admin.site.register(ProfileUser)
