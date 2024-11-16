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