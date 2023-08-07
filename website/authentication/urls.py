from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('logout', views.log_out, name='logout'),
    path('choose-role', views.choose_role, name='choose-role'),
    path('complete-name', views.complete_name, name='complete-name'),
    path('complete-email', views.complete_email, name='complete-email'),
    path('complete-username', views.complete_username, name='complete-username'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('change-password', views.change_password, name='change-password'),
    path('delete-account', views.delete_account, name='delete-account'),
    path('complete-citizenship', views.complete_citizenship, name='complete-citizenship'),
    path('complete-phone', views.complete_phone, name='complete-phone'),
    path('banned', views.banned, name='banned'),
    path('resend-verification-email', views.resend_verification_email, name='resend-verification-email'),
    path('two-factor', views.two_factor, name='two-factor'),
    path('two-factor/enable', views.two_factor_enable, name='two-factor-enable'),
    path('two-factor/disable', views.two_factor_disable, name='two-factor-disable'),
    path('two-factor/enable/verify', views.two_factor_enable_confirm, name='two-factor-verify'),

]