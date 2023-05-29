from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django import forms
from .models import TodoModel
from django.urls import reverse_lazy
from .forms import LoginForm, TodoForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# 会員登録ページに関する処理
class UserCreate(CreateView):
    template_name = 'todo/todo_login.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('todo:todo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crud'] = '新規登録'  # 画面に渡すパラメータにセット
        return context

# ログイン


class Login(LoginView):
    template_name = 'todo/todo_login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crud'] = 'ログイン'  # 画面に渡すパラメータにセット
        return context

# ログアウト


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'todo/todo_login.html'


class TodoList(LoginRequiredMixin, ListView):
    model = TodoModel
    context_object_name = 'todos'
    template_name = 'todo/todo_list.html'


class TodoCreate(LoginRequiredMixin, CreateView):
    model = TodoModel
    form_class = TodoForm
    template_name = 'todo/todo_edit.html'
    success_url = reverse_lazy('todo:todo_list')
    # 登録画面として表示する

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crud'] = '登録'  # 画面に渡すパラメータにセット
        return context


class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = TodoModel
    form_class = TodoForm
    template_name = 'todo/todo_edit.html'
    success_url = reverse_lazy('todo:todo_list')
    is_finished = True
    # フォームの完了日のvalueを編集する

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['is_finished'] = forms.BooleanField(
            label='完了', initial=self.is_finished, required=False)
        context['crud'] = '編集'
        return context


class TodoDelete(LoginRequiredMixin, UpdateView):
    model = TodoModel
    fields = ('is_deleted', )
    success_url = reverse_lazy('todo:todo_list')


class TodoComplete(LoginRequiredMixin, UpdateView):
    model = TodoModel
    fields = ('finished_date', )
    success_url = reverse_lazy('todo:todo_list')
