# myapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('features/', views.features_view, name='features'),
    path('create-tree/', views.create_tree_view, name='create_tree'),
    path('my-trees/', views.my_trees_view, name='my_trees'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('family-tree/', views.family_tree_view, name='family_tree'),
    path('api/family-tree/', views.family_tree_data, name='family_tree_data'),
    path('api/family-tree/edit/', views.edit_family_tree_view, name='edit_family_tree'),
]
