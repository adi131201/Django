from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileImg = models.ImageField(upload_to='profileImages', default='blank-profile-picture.webp')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    createdAt = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    postId = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username