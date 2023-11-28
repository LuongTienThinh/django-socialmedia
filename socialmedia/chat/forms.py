from django import forms
from .models import ChatRoom

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name','image']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Nhập tên phòng' }),
        }