from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django import forms
from .models import TodoModel
from django.urls import reverse_lazy
from .forms import LoginForm, TodoForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

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


# 一覧画面


class TodoList(LoginRequiredMixin, ListView):
    model = TodoModel
    context_object_name = 'todos'
    template_name = 'todo/todo_list.html'


# 新規作成画面


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

    # 保存前にフォームのデータを変更する
    def form_valid(self, form):
        todo_form = form.save(commit=False)
        todo_form.registration_date = timezone.now()  # 登録日を本日にセット
        todo_form.save()  # 保存する
        return redirect('/')


# 更新画面


class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = TodoModel
    form_class = TodoForm
    template_name = 'todo/todo_edit.html'
    success_url = reverse_lazy('todo:todo_list')
    is_finished = True

    # 編集画面として表示する
    # 編集する予定のTodoを取得して、完了日が入力されているかチェックする
    def get_object(self):
        query_result = TodoModel.objects.get(pk=self.kwargs["pk"])  # データを取得する
        if query_result.finished_date is None:
            self.is_finished = False
        return query_result

    # フォームの完了日のvalueを編集する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['is_finished'] = forms.BooleanField(
            label='完了', initial=self.is_finished, required=False)
        context['crud'] = '編集'
        return context


# 削除処理　*POSTのみ


class TodoDelete(LoginRequiredMixin, UpdateView):
    model = TodoModel
    fields = ('is_deleted', )
    success_url = reverse_lazy('todo:todo_list')
    # 削除対象であり、ログイン中のユーザーのIDのTodoを取得

    def get_object(self):
        return get_object_or_404(TodoModel, pk=self.request.POST["id"], user=self.request.user)
    # 削除フィールドを更新する

    def form_valid(self, form):
        todo_form = form.save(commit=False)
        todo_form.is_deleted = True  # 削除処理
        todo_form.save()  # 保存する
        return redirect('/')


# 完了処理　*POSTのみ


class TodoComplete(LoginRequiredMixin, UpdateView):
    model = TodoModel
    fields = ('finished_date', )
    success_url = reverse_lazy('todo:todo_list')

    # 完了対象であり、ログイン中のユーザーのIDのTodoを取得
    def get_object(self):
        return get_object_or_404(TodoModel, pk=self.request.POST["id"], user=self.request.user)

    # 完了日フィールドを更新する
    def form_valid(self, form):
        todo_form = form.save(commit=False)
        todo_form.finished_date = timezone.now()  # 削除処理
        todo_form.save()  # 保存する
        return redirect('/')
