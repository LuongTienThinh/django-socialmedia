# authentication/views.py
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

from django.core.mail import send_mail
from django.http import HttpResponse

from socialmedia.settings import EMAIL_HOST_USER
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ChangePasswordForm, ForgotPasswordForm
from .models import OTP, User
from profiles.models import Profile

import random
import string

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

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Tên đăng nhập hoặc mật khẩu không đúng.",
        # Các thông báo lỗi khác nếu cần
    }

# đăng nhập
class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    def form_invalid(self, form):
        messages.error(self.request, form.error_messages['invalid_login'])
        return super().form_invalid(form)
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
    success_url = reverse_lazy('home')
    

# quên mật khẩu
class ForgotPasswordView(View):
    form_class = ForgotPasswordForm
    template_name = 'authentication/forgot_password.html' 

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, { 'form': form, 'check_email': True, 'check_otp': True })

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        first_filter = Q(email=request.POST.get('email'))
        second_filter = Q(email=request.session.get('email'))
        user = User.objects.filter(first_filter | second_filter).first()
        print(user)

        if not user:
            return render(request, self.template_name, { 'form': form, 'check_email': False, 'check_otp': True })
        elif 'send-otp' in request.POST:
            rs_form = ForgotPasswordForm(request.POST, initial={'email': request.POST.get('email')})
            if not request.session.get('email'):
                request.session['email'] = request.POST.get('email')
            code = random.randint(100000, 999999)
            OTP.objects.create(user=user, code=code, is_active=True)

            subject = 'Django social - OTP reset password'
            message = f'Your OTP is: {code}'
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            return render(request, self.template_name, { 'form': rs_form, 'email': request.POST.get('email') or request.session.get('email'), 'check_email': True, 'check_otp': True })
        else:
            otp = OTP.objects.filter(Q(is_active=True, user=user)).last()
            if otp.code == request.POST.get('otp'):
                print(f"otp is: {otp.code}", user.password)
                new_password = random_password()
                user.set_password(new_password)
                user.save()
                return render(request, self.template_name, { 
                    'form': form, 
                    'email': request.session.get('email'), 
                    'otp': otp.code,
                    'newpassword': new_password,
                    'check_email': True,
                    'check_otp': True
                })
            otp.is_active = False
            otp.save()
            return render(request, self.template_name, { 'form': form, 'email': request.session.get('email'), 'check_email': True, 'check_otp': False })

# Send mail
def random_password(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    return password
