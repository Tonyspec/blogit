from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileUser

class UserSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=False)
    bio = forms.CharField(widget=forms.Textarea, max_length=500, required=False)
    location = forms.CharField(max_length=100, required=False)
    profile_image = forms.ImageField(required=False)
    email = forms.EmailField(required=True)  # Email is required for verification

    class Meta:
        model = ProfileUser
        fields = ('username', 'name', 'email', 'bio', 'location', 'profile_image', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass  # You can customize the form here if needed, but for now, we'll use the default fields

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['name', 'bio', 'location', 'profile_image', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['name', 'bio', 'location', 'profile_image', 'email']  # Include profile_image

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_image']