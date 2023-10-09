from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import UserCreateView, VerifyCodeView, success_view, reset_password
from users.models import User

app_name = 'users'

urlpatterns = [path('registration/', UserCreateView.as_view(), name='user_create'),
               path('verify/', VerifyCodeView.as_view(), name='verify_code'),
               path('registration/success/', success_view, name='success_regist'),
               path('login/', LoginView.as_view(template_name='user/user_login.html'), name='login'),
               path('logout/', LogoutView.as_view(template_name='user/user_logout.html'), name='logout'),
               path('reset_password/', reset_password, name='reset_password')]