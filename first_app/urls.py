from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('signup/', views.signup,name="signup"),
    path('login/', views.userLogin,name="login"),
    path('logout/', views.userLogout,name="logout"),
    path('profile/', views.profile,name="profile"),
    # path('passwordChange/', views.changePassword,name="passwordChange"), # change with old password
    path('setPasswordChange/', views.setPassword,name="setPasswordChange"),
    path('updateUser', views.updateUser, name='updateUser'),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',html_email_template_name='password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<str:token>/', views.activate, name='activate'),
]