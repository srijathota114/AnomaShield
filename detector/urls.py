from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('results/<int:upload_id>/', views.results, name='results'),
    path('download/<int:upload_id>/', views.download_clean_data, name='download_clean_data'),
    path('history/', views.upload_history, name='upload_history'),
    path('delete/<int:upload_id>/', views.delete_upload, name='delete_upload'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/reset/', views.reset_settings, name='reset_settings'),
    
    # Authentication URLs (to be implemented)
    # path('login/', auth_views.LoginView.as_view(template_name='detector/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name='register'),
    # path('profile/', views.profile, name='profile'),
] 