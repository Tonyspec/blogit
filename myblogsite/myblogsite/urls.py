"""myblogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap  # Add this import


from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from blog.models import Post  # with your article model

post_dict = {
    'queryset': Post.objects.filter(published=True),  # Only include published posts
    'date_field': 'date_posted',  # Use the date field for sitemap
}

sitemaps = {
    'posts': GenericSitemap(post_dict, priority=0.6),
}

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    # path('new_post/', views.create_post, name='create_post'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #path('api/', include('blog.urls')),  # if you have a separate urls.py for your api
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
