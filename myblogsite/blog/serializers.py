import django.utils.translation as original_translation
original_translation.ugettext_lazy = original_translation.gettext_lazy
from rest_framework import serializers
from .models import ProfileUser, PostImage, Post, Like, Comment, Follow, CommentLike
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

class ProfileUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers_count', read_only=True)
    following_count = serializers.IntegerField(source='following_count', read_only=True)
    post_count = serializers.IntegerField(source='post_count', read_only=True)

    class Meta:
        model = ProfileUser
        fields = ['id', 'username', 'name', 'bio', 'location', 'profile_image', 'followers_count', 'following_count', 'post_count']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = ProfileUserSerializer(read_only=True)  # Assuming you want to serialize the author's details
    images = PostImageSerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'time_posted', 'author', 'tags', 'images', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes_count()

    def get_comments_count(self, obj):
        return obj.comments_count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'date_created']

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_date', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes_count

class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileUserSerializer(read_only=True)
    followed = ProfileUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'date_created']

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'user', 'date_created']
