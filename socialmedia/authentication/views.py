# authentication/views.py
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ChangePasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.shortcuts import redirect
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# đăng kí 
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'authentication/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)  # This will create the user
        profile_pic_path = 'cover_photos/logotdc.jpg'  # Replace with the actual path to your static image
        Profile.objects.create(user=self.object, profile_pic=profile_pic_path)  #
        return response  # Return the response object to continue the no

# đăng nhập
class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        if user.is_authenticated:
            context = {
                'user': user,
            }            
            return redirect('home')  
        return super().form_valid(form)

# đổi mật khẩu
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'authentication/password_reset.html' 

