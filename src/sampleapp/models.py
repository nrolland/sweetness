from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):

    author = models.ForeignKey(User)
    slug = models.CharField(max_length=50)
    title = models.CharField(max_length=128)
    body = models.TextField()
