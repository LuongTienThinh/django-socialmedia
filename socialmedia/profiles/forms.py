# profiles/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'user', 'bio', 'profile_pic', 'cover_photo', 'phone_number', 'address']