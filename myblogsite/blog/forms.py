from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileUser, Post, PostImage

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

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    widget = MultipleFileInput
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class PostForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tags')
        if tags is None or not tags:
            self.add_error('tags', "At least one tag is required.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()  # Save the post instance first

        # Handle tags AFTER saving the instance
        if commit:
            tags = self.cleaned_data.get('tags')
            if tags:
                instance.tags.set(*tags)

        return instance  # Don't handle images here; do it in the view