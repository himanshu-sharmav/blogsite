from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog,Comment,Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count',read_only=True) 
    comments_count = serializers.IntegerField(source='comments.count',read_only=True)

    class Meta:
        model = Blog
        fields = ('id','title','content','author','likes_count','comments_count','created_at','updated_at')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id','blog','author','content','created_at')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id','blog','user')
        
                