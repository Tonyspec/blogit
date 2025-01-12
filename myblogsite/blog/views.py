from django.shortcuts import render, get_object_or_404
from .models import Post, ProfileUser, Like, Comment, Follow, CommentLike
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CommentForm, UserSignUpForm, LoginForm, ProfileEditForm, SearchForm

from django.contrib.auth import login


from django.shortcuts import render, redirect
from django.contrib import messages



from .forms import PostForm, PostImage
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'blog/home.html')

def placeholder_view(request):
    return render(request, 'placeholder.html')

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
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists() if request.user.is_authenticated else False
    post_count = user.post_count
    return render(request, 'profile.html', {
        'user_profile': user,
        'posts': posts,
        'username': username,
        'post_count': post_count,
        'followers_count': user.followers_count,
        'following_count': user.following_count,
        'is_following': is_following
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

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(ProfileUser, username=username)
    Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(ProfileUser, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('profile', username=username)

def following(request, username):
    user = get_object_or_404(ProfileUser, username=username)
    following = user.following.all()
    return render(request, 'following.html', {'user': user, 'following': following})

def followers(request, username):
    user = get_object_or_404(ProfileUser, username=username)
    followers = user.followers.all()
    return render(request, 'followers.html', {'user': user, 'followers': followers})


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if CommentLike.objects.filter(comment=comment, user=user).exists():
        # User already likes this comment, so unlike it
        CommentLike.objects.filter(comment=comment, user=user).delete()
    else:
        # User does not like this comment, so like it
        CommentLike.objects.create(comment=comment, user=user)

    # Redirect back to the referrer if available, otherwise to post detail
    return redirect(request.META.get('HTTP_REFERER') or reverse('post_detail', kwargs={'post_id': comment.post.id}))

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

@require_GET
def fetch_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    data = [{'author': {'username': comment.author.username}, 'content': comment.content, 'created_date': comment.created_date} for comment in comments]
    return JsonResponse(data, safe=False)

import json 
@login_required
@require_POST
def submit_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = json.loads(request.body)
    comment_text = data.get('comment_text', '').strip()
    if comment_text:
        Comment.objects.create(
            post=post,
            author=request.user,
            content=comment_text
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Comment text is required.'})

from django.db.models import Count
def all_tags(request):
    # Here you would calculate or fetch the tag sizes based on your logic
    # For example, based on how many posts each tag is associated with
    tags = Tag.objects.annotate(size=Count('post')).order_by('-size')
    
    # Convert the count to a size for the tag cloud (this is just an example)
    for tag in tags:
        tag.size = 1 + (tag.size / max(tag.size for tag in tags)) * 2  # Scale size between 1em and 3em
    
    return render(request, 'tags.html', {'tags': tags})

from django.db.models import Q
def search(request):
    query = None
    results = []
    form = SearchForm()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(author__username__icontains=query)
            )

    return render(request, 'search.html', {
        'form': form,
        'query': query,
        'results': results,
    })