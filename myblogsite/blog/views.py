from django.shortcuts import render, get_object_or_404
from .models import Post, ProfileUser, Like, Comment
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CommentForm, UserSignUpForm, LoginForm, ProfileEditForm

from django.contrib.auth import login


from django.shortcuts import render, redirect
from django.contrib import messages



from .forms import PostForm, PostImage
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'blog/home.html')

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url='login')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_registration_email(user_name, user_email):
    subject = 'Welcome to MyWeb'
    html_content = render_to_string('welcome_email.html', {'user_name': user_name})
    text_content = strip_tags(html_content)  # Plain text version for email clients without HTML support

    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [user_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False, verify=False)

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            send_registration_email(user.name, user.email)  
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')  # Redirect to a success page or home page
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


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





@login_required(login_url='login')
def profile(request, username=None):
    if username is None:
        user = request.user
    else:
        user = get_object_or_404(ProfileUser, username=username)
    
    # This should fetch posts for the correct user
    posts = Post.objects.filter(author=user).order_by('-date_posted', '-time_posted')
    
    return render(request, 'profile.html', {
        'user_profile': user,
        'posts': posts,
        'username': username
    })

@login_required
def edit_profile(request, username):
    user = get_object_or_404(ProfileUser, username=username)
    if user != request.user:
        # You might want to redirect or raise an error if someone tries to edit another user's profile
        messages.error(request, "You can only edit your own profile.")
        return redirect('profile')  # Assuming 'profile' is a URL name for the user's profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile edited successfully!')
            return redirect('profile', username=username)  # Or another appropriate redirection
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

#CREATE POST
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Save with commit=False to set author
            post.author = request.user  # Set the author
            post.save()  # Now save the post with the author set
            
            # Handle tags after saving the instance
            form.save_m2m()

            # Handle images if they were uploaded
            images = form.cleaned_data.get('images', [])
            for image in images:
                PostImage.objects.create(post=post, image=image)

            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

from taggit.models import Tag

def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    return render(request, 'tag_detail.html', {'tag': tag, 'posts': posts})


def home(request):
    # Fetch all posts or latest posts, here we're fetching all
    posts = Post.objects.all().order_by('-date_posted', '-time_posted')[:10]  # Latest 10 posts
    return render(request, 'blog/home.html', {'posts': posts})

#LIKE POST 
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).delete()
            liked = False
        else:
            Like.objects.create(user=user, post=post)
            liked = True
        
        # Return JSON response
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count()
        })
    
    # If not an AJAX request, redirect (though this should not occur with AJAX setup)
    return redirect('post_detail', pk=post_id)


@login_required
def post_list(request):
    posts = Post.objects.all()
    
    if request.method == 'POST' and 'comment_content' in request.POST:
        post_id = request.POST.get('post_id')
        content = request.POST.get('comment_content')
        post = get_object_or_404(Post, id=post_id)
        Comment.objects.create(post=post, author=request.user, content=content)
        # Redirect back to homepage or refresh data via AJAX
        return redirect('home')

    return render(request, 'home.html', {'posts': posts})

#LIKE COMMENT
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post_detail', pk=comment.post.pk)