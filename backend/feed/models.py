from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True)
    is_product = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Post by {self.author.username} on {self.date_posted}'
