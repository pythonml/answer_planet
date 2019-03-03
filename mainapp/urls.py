from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_html, name='login'),
    path('register/', views.register_html, name='register'),
    path('menu/', views.menu_html, name='menu'),
    path('auth/', views.auth_user, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('user/create/', views.create_user, name='create_user'),
    path('questions/', views.questions, name='questions'),
    path('answer_result/', views.answer_result, name='answer_result'),
    path('prize/', views.prize, name='prize'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('get_random_questions/', views.get_random_questions, name='get_random_questions'),
    path('answer/submit/', views.submit_answer, name='submit_answer'),
    path('invite/', views.invite_html, name='invite'),
]
