from django import forms
from django.contrib.auth.models import User
from .models import TodoModel
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

###
# ログインフォーム


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ユーザー名', max_length=50)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # それぞれのフォームに対してクラスを付与する
        self.fields['username'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['password'].widget.attrs['class'] = 'form-control mb-3'

###

# ユーザーの新規登録用


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control mb-3"

###
# Todoフォーム


class TodoForm(forms.ModelForm):
    # 完了日フィールド（登録時）
    # is_finishedは、完了フラグを表すブール値フィールドです。
    # forms.BooleanFieldを使用して定義されており、required=Falseで必須ではないことを示しています。
    # また、labelパラメータを使用してフィールドの表示ラベルを設定しています。
    is_finished = forms.BooleanField(required=False, label="完了")
    # Metaクラス内には、TodoFormクラスのメタデータが定義されています。
    # model属性にはTodoModelモデルが指定されており、
    # fields属性にはフォームで使用するフィールドが指定されています。
    # labels属性には各フィールドに対するラベルが定義されており、error_messages属性には各フィールドに対するエラーメッセージが定義されています。
    # widgets属性では、expire_dateフィールドに対してforms.DateInputウィジェットを指定しています。

    class Meta:
        model = TodoModel
        # どのフィールドを使用するか
        fields = ('item_name', 'user', 'expire_date',
                  'is_finished', 'finished_date')
        # フィールドに対するラベル
        labels = {
            'item_name': '項目名',
            'user': '担当者',
            'expire_date': '期限日',
        }
        # 基本的なバリデーション
        error_messages = {
            "item_name": {
                "required": "項目名が入力されていません",
            },
            "user": {
                "required": "担当者名が入力されていません",
            },
            "expire_date": {
                "required": "期限日が入力されていません",
            },
        }
        # ウィジェット
        widgets = {
            'expire_date': forms.DateInput(attrs={"type": "date"})
        }
    # 登録時および更新時、初期設定
    # __init__メソッドは、フォームの初期化時に実行されます。
    # 親クラスの__init__メソッドを呼び出し、その後の処理で特定の設定を行っています。
    # self.fields['finished_date'].widgetをforms.HiddenInput()で上書きしているため、
    # finished_dateフィールドは非表示になります。
    # また、forループで各フィールドのウィジェットにclass属性としてform-controlを設定しています。

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['finished_date'].widget = forms.HiddenInput()
        for field in self.fields:
            if field != "is_finished":
                self.fields[field].widget.attrs["class"] = "form-control"
    # 項目名に対するバリデーション
    # clean_item_nameメソッドは、item_nameフィールドに対するバリデーションを行います。
    # cleaned_dataからitem_nameの値を取得し、文字列の長さが100以上の場合にエラーを追加します。

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if len(item_name) >= 100:
            self.add_error('item_name', '項目名は100文字以内で入力してください')
        return item_name
    # 期限日に対するバリデーション
    # clean_expire_dateメソッドは、expire_dateフィールドに対するバリデーションを行います。
    # cleaned_dataからexpire_dateの値を取得し、strftimeメソッドを使って日付の形式が正しいかどうかをチェックします。
    # 日付の形式が正しくない場合やexpire_dateがNoneの場合にエラーを追加します。

    def clean_expire_date(self):
        expire_date = self.cleaned_data.get('expire_date')
        try:
            expire_date.strftime('%Y/%m/%d %H:%M:%S')
        except:
            if expire_date is None:
                self.add_error('expire_date', '期限日が入力されていません')
            else:
                self.add_error('expire_date', '日付の形式で入力してください')
        return expire_date
    # 完了日に対する処理
    # cleanメソッドは、フォーム全体に対するバリデーションを行います。
    # 親クラスのcleanメソッドを呼び出し、その後の処理で特定の設定を行っています。
    # cleaned_dataからis_finishedの値を取得し、チェックが入っている場合はfinished_dateに現在の日時を設定し、
    # チェックが入っていない場合はNoneを設定します。最終的に、バリデーションを通過したデータを返します。

    def clean(self):
        cleaned_data = super().clean()
        is_finished = cleaned_data.get('is_finished')
        if is_finished:
            cleaned_data['finished_date'] = timezone.now()
        else:
            cleaned_data['finished_date'] = None
        return cleaned_data
