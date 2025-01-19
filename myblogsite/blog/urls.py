from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'posts', views.PostViewSet)
# router.register(r'users', views.ProfileUserViewSet)
# router.register(r'comments', views.CommentViewSet)
# router.register(r'comments', views.LikeViewSet)
# router.register(r'comments', views.CommentLikeViewSet)
# router.register(r'comments', views.FollowViewSet)

# from django.contrib.sitemaps.views import sitemap
# from django.contrib.sitemaps import GenericSitemap
# from .models import Post  # with your article model

# post_dict = {
#     'queryset': Post.objects.filter(published=True),  # Only include published posts
#     'date_field': 'date_posted',  # Use the date field for sitemap
# }

# sitemaps = {
#     'posts': GenericSitemap(post_dict, priority=0.6),
# }



urlpatterns = [
    #path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile_self'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('tag/<slug:tag_slug>/', views.tag_detail, name='tag_detail'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('search/', views.search, name='search'),
    path('tags/', views.all_tags, name='tags'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/unfollow/', views.unfollow, name='unfollow'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('fetch_comments/<int:post_id>/', views.fetch_comments, name='fetch_comments'),
    path('submit_comment/<int:post_id>/', views.submit_comment, name='submit_comment'),
    path('profile/<str:username>/following/', views.following, name='following'),
    path('profile/<str:username>/followers/', views.followers, name='followers'),
    path('new_post/', views.create_post, name='create_post'),
    #path('api/', include(router.urls)),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('tag/<slug:tag_slug>/', views.tag_detail, name='tag_detail'),
    path('tag/<slug:tag_slug>/toggle-favourite/', views.toggle_favourite_tag, name='toggle_favourite_tag'),
    path('about/', views.about_project, name='about_project'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]