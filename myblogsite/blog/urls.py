from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import signup_view

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('login/', views.custom_login, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile_self'),
    path('profile/edit/<str:username>/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('new_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]