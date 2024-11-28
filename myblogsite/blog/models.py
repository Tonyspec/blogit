from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError

class ProfileUser(AbstractUser):
    # Inherits all fields from AbstractUser (username, password, email, etc.)
    name = models.CharField(max_length=150, blank=True, null=True)  # Optional full name
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)  # Extended length for detailed locations
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username if self.name is None else self.name

class PostImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Now can hold larger articles
    date_posted = models.DateField(default=timezone.now)
    time_posted = models.TimeField(default=timezone.now)
    author = models.ForeignKey('blog.ProfileUser', on_delete=models.CASCADE)
    tags = TaggableManager()  # Tags for the post, at least one is required

    def likes_count(self):
        return Like.objects.filter(post=self).count()
    
    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/post/{self.pk}/"
    
# In your models.py

from django.db import models
from django.contrib.auth import get_user_model

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


