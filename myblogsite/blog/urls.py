from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile_self'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('new_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('tag/<slug:tag_slug>/', views.tag_detail, name='tag_detail'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('search/', views.placeholder_view, name='search'),
    path('tags/', views.all_tags, name='tags'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/unfollow/', views.unfollow, name='unfollow'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('fetch_comments/<int:post_id>/', views.fetch_comments, name='fetch_comments'),
    path('submit_comment/<int:post_id>/', views.submit_comment, name='submit_comment'),
    path('profile/<str:username>/following/', views.following, name='following'),
    path('profile/<str:username>/followers/', views.followers, name='followers')
]