from django.contrib import admin
from django.contrib.auth import views as authorization_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('stuff.urls')),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', authorization_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', authorization_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         authorization_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='password_reset'
         ),
    path('profile/', user_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
