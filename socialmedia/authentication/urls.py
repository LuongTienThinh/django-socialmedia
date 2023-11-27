from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CustomPasswordChangeView, ForgotPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
]