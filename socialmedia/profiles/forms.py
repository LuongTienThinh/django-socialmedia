# profiles/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'bio', 'profile_pic', 'cover_photo', 'phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Nhập số điện thoại'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Nhập địa chỉ'}),
            'bio': forms.Textarea(attrs={'class':'form-control','placeholder' : 'Nhập tiểu sử'}),           
        }