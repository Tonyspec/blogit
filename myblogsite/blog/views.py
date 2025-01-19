from django.shortcuts import render, get_object_or_404
from .models import Post, ProfileUser, Like, Comment, Follow, CommentLike, Notification, Subheading, Article
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CommentForm, UserSignUpForm, LoginForm, ProfileEditForm, SearchForm, PostForm, ArticleForm, ArticleFormSet, SubheadingForm, SubheadingFormSet
import logging
from django.contrib.auth import login
from django.db import transaction, models
from django.core.mail import send_mail


from django.shortcuts import render, redirect
from django.contrib import messages

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta



from .forms import PostForm, PostImage
from django.contrib.auth.decorators import login_required

def placeholder_view(request):
    return render(request, 'placeholder.html')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    liked_by_user = post.like_set.filter(user=request.user).exists() if request.user.is_authenticated else False

    # Check which comments are liked by the user
    if request.user.is_authenticated:
        liked_comments = set(request.user.commentlike_set.values_list('comment_id', flat=True))
        for comment in comments:
            comment.liked_by_user = comment.id in liked_comments
    else:
        for comment in comments:
            comment.liked_by_user = False

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                Notification.objects.create(
                    user=post.author,
                    notification_type='C',
                    post=post,
                    comment=comment,
                    actor=request.user,
                    text=f'{request.user.username} commented on your post!'
                )
                return redirect('post_detail', slug=post.slug)
        else:
            # Optionally redirect to login or show a message
            return redirect('login')  # or return an error message like "Please log in to comment."
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'liked_by_user': liked_by_user,
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the user is the author of the post
    if request.user == post.author:
        if request.method == 'POST':
            # Delete the post
            post.delete()
            messages.success(request, 'Post has been deleted successfully.')
            return redirect('home')  # Redirect to home or another relevant page
        else:
            # If it's not a POST request, show a confirmation page or handle accordingly
            return render(request, 'confirm_delete.html', {'post': post})
    else:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_detail', pk=pk)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user is the author of the comment
    if request.user == comment.author:
        if request.method == 'POST':
            # Delete the comment
            comment.delete()
            messages.success(request, 'Comment has been deleted successfully.')
            return redirect('post_detail', slug=comment.post.slug)  # Redirect back to post detail
        else:
            # If it's not a POST request, show a confirmation page if needed
            return render(request, 'confirm_delete.html', {'comment': comment})
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('post_detail', slug=comment.post.slug)

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Send confirmation email
            subject = 'Account created on VoxPop'
            message = f'Hello {user.username},\n\nYour account on VoxPop has been created!\n\nThank you for joining us!'
            send_mail(subject, message, 'testerbender0131@gmail.com', [user.email], fail_silently=False)
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
                messages.error(request, "Invalid username or passworD.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html')

#@login_required(login_url='login')
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
logger = logging.getLogger(__name__)
@login_required
@transaction.atomic
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        print("All POST data:", request.POST)
        print("Form Data:", request.POST)
        print("Form Validity:", form.is_valid())

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published = True
            post.save()
            form.save_m2m()

            # Handle images
            images = request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=post, image=image)

            # Process dynamic content
            subheadings = {}
            for key, value in request.POST.items():
                if key.startswith('sub-'):
                    index = key.split('-')[1]
                    subheadings[index] = {'title': value, 'paragraphs': []}
                elif key.startswith('paragraph-'):
                    parts = key.split('-')
                    if len(parts) == 3:  # 'paragraph-[subIndex]-[paraIndex]'
                        subIndex, paraIndex = parts[1], parts[2]
                        if subIndex in subheadings:
                            subheadings[subIndex]['paragraphs'].append(value)

            print("Processed subheadings:", subheadings)

            # Create Subheading with associated Paragraphs
            for index, data in subheadings.items():
                sub = Subheading.objects.create(post=post, title=data['title'])
                for paragraph_content in data['paragraphs']:
                    Article.objects.create(subheading=sub, post=post, content=paragraph_content)

            return redirect('home')
        else:
            print("Validation errors:", form.errors)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

from taggit.models import Tag

@login_required
def toggle_favourite_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    user = request.user
    if tag in user.favourite_tags.all():
        user.favourite_tags.remove(tag)
        action = "removed"
    else:
        user.favourite_tags.add(tag)
        action = "added"
    return JsonResponse({'action': action, 'tag_slug': tag.slug})

def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag])
    # Check if the user is authenticated before accessing profileuser
    if request.user.is_authenticated:
        is_favourite = tag in request.user.favourite_tags.all()
    else:
        is_favourite = False  # or you might choose not to show this info at all for anonymous users

    return render(request, 'tag_detail.html', {
        'tag': tag,
        'posts': posts,
        'is_favourite': is_favourite
    })


def home(request):
    # Assuming the user has favorite tags stored under 'favourite_tags'
    if request.user.is_authenticated:
        user_favorite_tags = request.user.favourite_tags.all()
        followed_users = [follow.followed for follow in request.user.following.all()]
    else:
        user_favorite_tags = []
        followed_users = []

    # Today's date for checking recent posts
    today = timezone.now().date()

    # Query for all posts
    posts = Post.objects.filter(published=True)

    # Annotate and order all posts
    posts = posts.annotate(
        like_count=Count('like'),
        comment_count=Count('comments'),
        has_fav_tag=Count('tags', filter=Q(tags__in=user_favorite_tags), distinct=True),
        from_followed_user=Count('author', filter=Q(author__in=followed_users)),
    ).annotate(
        # Create an ordering field. Higher values mean higher priority
        priority=models.Case(
            models.When(has_fav_tag__gt=0, then=4),  # Highest for posts with favorite tags
            models.When(from_followed_user__gt=0, then=3),  # High for posts from followed users
            #models.When(date_posted__gte=today - timedelta(days=1), then=2),  # Medium for recent posts
            models.When(Q(like_count__gt=0) | Q(comment_count__gt=0), then=1),  # Lower for posts with engagement
            default=0,  # Lowest for others
            output_field=models.IntegerField()
        )
    ).order_by(
        '-priority',  # First by our custom priority
        '-like_count',  # Then by likes
        '-comment_count',  # Then by comments
        '-date_posted'  # Then by date, most recent first
    )

    # Check which posts are liked by the user
    if request.user.is_authenticated:
        liked_posts = set(request.user.like_set.values_list('post_id', flat=True))
        posts = list(posts)
        for post in posts:
            post.liked_by_user = post.id in liked_posts
    else:
        for post in posts:
            post.liked_by_user = False

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
            new_notification = Notification.objects.create(
            user=post.author,
            notification_type='LP',
            post=post,
            actor=request.user,
            text=f'{request.user.username} liked your post!'
            )

        # Return JSON response
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes_count()
        })

    # If not an AJAX request, redirect (though this should not occur with AJAX setup)
    return redirect('post_detail', kwargs={'slug':post.slug})


@login_required
def post_list(request):
    posts = Post.objects.all()

    if request.method == 'POST' and 'comment_content' in request.POST:
        post_id = request.POST.get('post_id')
        content = request.POST.get('comment_content')
        post = get_object_or_404(Post, id=post_id)
        comments = fetch_comments(request, post_id)
        Comment.objects.create(post=post, author=request.user, content=content)
        Notification.objects.create(
                user=post.author,
                notification_type='C',
                post=post,
                comment=comment,
                actor=request.user,
                text=f'{request.user.username} testcommented on your post!'
            )
        # Redirect back to homepage or refresh data via AJAX
        return redirect('home')

    return render(request, 'home.html', {'posts': posts})


@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(ProfileUser, username=username)
    Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    Notification.objects.create(
        user=user_to_follow,
        notification_type='F',
        actor=request.user,
        text=f'{request.user.username} started following you!'
    )
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

    try:
        # Try to fetch the existing like
        like = CommentLike.objects.get(comment=comment, user=user)
        # If we find a like, we remove it (dislike)
        like.delete()
    except CommentLike.DoesNotExist:
        # If no like exists, create one
        CommentLike.objects.create(comment=comment, user=user)
        Notification.objects.create(
            user=comment.author,
            notification_type='LC',
            comment=comment,
            actor=request.user,
            text=f'{request.user.username} liked your comment!'
        )

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
        print("Comment submission received:", request.body)
        Comment.objects.create(
            post=post,
            author=request.user,
            content=comment_text
        )
        Notification.objects.create(
                user=post.author,
                notification_type='C',
                post=post,
                actor=request.user,
                text=f'{request.user.username} commented on your post!'
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Comment text is required.'})

from django.db.models import Count
def all_tags(request):
    # Popular Tags: based on usage frequency
    popular_tags = Tag.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:20]  # Top 20

    # Main Categories: Predefined categories
    main_categories = [
        'World', 'Politics', 'Business', 'Economy', 'Technology',
        'Science', 'Health', 'Environment', 'Sports', 'Entertainment',
        'Arts & Culture', 'Crime', 'Education', 'Media', 'Weather',
        'Military', 'Human Rights', 'Energy', 'Travel', 'Lifestyle'
    ]

    # Convert main categories to Tag objects if needed
    main_tags = Tag.objects.filter(name__in=main_categories).annotate(num_posts=Count('post'))

    # Favorite Tags: Only for authenticated users
    if request.user.is_authenticated:
        favourite_tags = request.user.favourite_tags.all()
    else:
        favourite_tags = None

    # Scale tag size for visual representation
    # Scale tag size for visual representation
    def scale_size(tags):
        if tags:
            post_counts = [tag.num_posts for tag in tags if hasattr(tag, 'num_posts')]
            if post_counts:
                max_count = max(post_counts)
                for tag in tags:
                    if hasattr(tag, 'num_posts'):
                        # Avoid division by zero
                        if max_count > 0:
                            tag.size = 1 + (tag.num_posts / max_count) * 2
                        else:
                            tag.size = 1  # Default size if no posts are tagged
                    else:
                        tag.size = 1.5  # Default for tags without count data
            else:
                for tag in tags:
                    tag.size = 1  # If no tags have posts, set a uniform size for all
        return tags

    popular_tags = scale_size(popular_tags)
    main_tags = scale_size(main_tags)

    return render(request, 'tags.html', {
        'popular_tags': popular_tags,
        'main_tags': main_tags,
        'favourite_tags': favourite_tags
    })


from django.db.models import Q
def search(request):
    query = None
    post_results = []
    user_results = []
    tag_results = []
    form = SearchForm()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # Search for posts
            post_results = Post.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query)
            )

            # Search for users
            user_results = ProfileUser.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

           # Search for tags
            tag_results = Tag.objects.filter(name__icontains=query)

            # If tags are found, include posts that have these tags
            if tag_results:
                # Use the tag objects to find posts
                posts_with_tags = Post.objects.filter(tags__in=tag_results)
                # Combine these results with existing post results
                post_results = (post_results | posts_with_tags).distinct()

    return render(request, 'search.html', {
        'form': form,
        'query': query,
        'post_results': post_results,
        'user_results': user_results,
        'tag_results': tag_results,
    })

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.user == request.user:
        notification.is_read = True
        notification.save()
    return redirect('notifications')  # Assuming you have a route named 'notifications'

@login_required
def delete_account(request):
    if request.method == 'POST':
        # This is a security measure to ensure the user really wants to delete the account
        if 'confirm_delete' in request.POST:
            user = request.user
            email = user.email
            username = user.username

            # Delete the user
            user.delete()

            # Send confirmation email
            subject = 'Account Deletion Confirmation'
            message = f'Hello {username},\n\nYour account with the email {email} has been deleted from our system.'
            send_mail(subject, message, 'testerbender0131@gmail.com', [email], fail_silently=False)

            # Log out the user (if the session still exists)
            from django.contrib.auth import logout
            logout(request)

            messages.success(request, 'Your account has been deleted. A confirmation email has been sent to your email address.')
            return redirect('home')  # Redirect to home or any other appropriate page

    return render(request, 'confirm_delete.html')

from django.shortcuts import render

def about_project(request):
    context = {
        'title': 'About VoxPop',
        'description': 'VoxPop is a platform where everyone has the voice of a journalist. Share your stories, report on the news, and engage with a community passionate about uncovering the truth.'
    }
    return render(request, 'about_project.html', context)

from rest_framework import viewsets
from .models import Post, ProfileUser, Like, Comment, Follow, CommentLike
from .serializers import PostSerializer, ProfileUserSerializer, LikeSerializer, CommentSerializer, FollowSerializer, CommentLikeSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ProfileUserViewSet(viewsets.ModelViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer