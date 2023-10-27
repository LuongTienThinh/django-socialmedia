from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import CustomUserCreationForm,CustomAuthenticationForm,ChangePasswordForm
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.shortcuts import redirect,HttpResponse
from django.contrib.auth.decorators import login_required

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'authentication/register.html'

class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    def form_valid(self, form):
        user = form.get_user()
        if user.is_authenticated:
            context = {
                'user': user,
            }            
            return render(self.request, 'index.html', context)        
        return super().form_valid(form)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'authentication/password_reset.html' 

