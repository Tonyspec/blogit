from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.


from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from crispy_forms.layout import Layout, Field

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserSignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')  # Redirect to a success page or home page
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or wherever after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProfileEditForm  # Make sure this import reflects your actual form name

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile edited successfully!')
            return redirect('profile')  # Or another appropriate redirection
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required(login_url='login')  # Redirect to login if not authenticated
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to profile page after update
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

from .forms import PostForm
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assuming ProfileUser is related to User
            post.save()
            return redirect('home')  # Assuming 'post_list' is the name of your view showing all posts
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def home(request):
    # Fetch all posts or latest posts, here we're fetching all
    posts = Post.objects.all().order_by('-date_posted', '-time_posted')[:10]  # Latest 10 posts
    return render(request, 'blog/home.html', {'posts': posts})