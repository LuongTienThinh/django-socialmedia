# authentication/views.py
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponse

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ChangePasswordForm, ForgotPasswordForm
from .models import OTP, User
from profiles.models import Profile

import random

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

# quên mật khẩu
class ForgotPasswordView(View):
    form_class = ForgotPasswordForm
    template_name = 'authentication/forgot_password.html' 

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(Q(email=request.POST.get('email'))).first()
            if (user):
                otp_form = form.save(commit=False)
                code = random.randint(100000, 999999)
                OTP.objects.create(user=user, code=code)

                print(otp_form.email)
                return redirect('send')
        return render(request, self.template_name, {'form': form})

# Send mail
def send(request):
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        ["ltthinh2001120422@gmail.com"],
    )
    return HttpResponse('success')
