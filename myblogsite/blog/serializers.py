from rest_framework import serializers
from .models import Post, ProfileUser, Comment, Like, Follow, CommentLike

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # or specify fields if you want to restrict

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'