from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('create/', views.create, name='create'),
    path('setting/', views.setting, name='setting'),
    path('like/<int:card_id>/', views.like, name='like'),
    path('dislike/<int:card_id>/', views.dislike, name='dislike')
]
