from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_student, name='add_student'),
    path('update/', views.update_student_ajax, name='update_student_ajax'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('register/', views.register_view, name='register'),
]
