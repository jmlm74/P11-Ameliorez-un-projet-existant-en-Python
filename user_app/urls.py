"""
    home_app URL Configuration

"""
from django.urls import path
from django.contrib.auth import views as auth_views


from user_app import views as uav
from home_app import views as hav


app_name = 'user_app'
urlpatterns = [
    path('', hav.index, name='index'),
    path('user_create', uav.user_create, name='user_create'),
    path('login', uav.user_login, name='login'),
    path('user_logout', uav.user_logout, name='ulogout'),
    path('change_password', uav.change_password, name='change_password'),
    # Reset password
    path('reset_password', uav.reset_psw, name='reset_password'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_password_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'),
         name='password_reset_complete'),


]
