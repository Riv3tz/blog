from .models import BlogPost, User
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'owner', 'is_published']