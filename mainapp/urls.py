from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.create_user, name='register'),
    path('get_random_questions/', views.get_random_questions, name='get_random_questions'),
    path('answer/submit/', views.submit_answer, name='submit_answer'),
]
