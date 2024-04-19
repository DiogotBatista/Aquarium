from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from manutencao import views
from manutencao.views import register

urlpatterns = [
                  path('', views.index, name='index'),
                  path('aquarium_bd/', admin.site.urls),
                  path('aquarium/', include('manutencao.urls')),
                  path('register/', register, name='register'),
                  path('login/', views.login_view, name='login'),
                  path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
