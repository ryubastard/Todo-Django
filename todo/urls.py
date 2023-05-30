from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoList.as_view(), name='todo_list'),
    path('login', views.Login.as_view(), name="Login"),
    path("logout", views.Logout.as_view(), name="Logout"),
    path('todo_create/', views.TodoCreate.as_view(), name='todo_create'),
    path('todo_update/<int:pk>/', views.TodoUpdate.as_view(), name='todo_update'),
    path('todo_delete', views.TodoDelete.as_view(), name='todo_delete'),
    path('register', views.UserCreate.as_view(), name='register'),
]
