from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('create-user/', views.create_user, name='create-user'),
    path('user-list/', views.user_list, name='user-list'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit-user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete-user'),
]
