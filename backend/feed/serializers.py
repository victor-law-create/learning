from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'is_product', 'price', 'category', 'date_posted']
        read_only_fields = ['author']
