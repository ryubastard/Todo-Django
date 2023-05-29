from django.conf import settings
from django.db import models
from django.utils import timezone


class TodoModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # user フィールドは、他のモデル（おそらくユーザーモデル）への外部キーを表します。
    # settings.AUTH_USER_MODEL は、Djangoの設定ファイルで定義されたユーザーモデルを指す変数です。
    # on_delete=models.CASCADE は、関連するオブジェクトが削除された場合に関連オブジェクトも削除することを意味します。

    item_name = models.CharField(max_length=100)
    # item_name フィールドは、最大長が100文字の文字列フィールドです。
    # このフィールドはアイテムの名前を格納します。

    registration_date = models.DateTimeField(blank=True, null=True)
    # registration_date フィールドは、日時を格納するための日時フィールドです。
    # blank=True は、フィールドが空であることを許可することを意味します。
    # null=True は、データベースでのフィールドの値として NULL を許可することを意味します。

    expire_date = models.DateTimeField(blank=True, null=True)
    # expire_date フィールドは、アイテムの有効期限を格納するための日時フィールドです。
    # blank=True と null=True は、上記と同様の意味を持ちます。

    finished_date = models.DateTimeField(blank=True, null=True)
    # finished_date フィールドは、アイテムの完了日時を格納するための日時フィールドです。
    # blank=True と null=True は、上記と同様の意味を持ちます。

    is_deleted = models.BooleanField(default=False)
    # is_deleted フィールドは、アイテムが削除されたかどうかを示すブールフィールドです。
    # default=False は、デフォルト値を False に設定することを意味します。

    create_date_time = models.DateTimeField(default=timezone.now)
    # create_date_time フィールドは、アイテムが作成された日時を格納するための日時フィールドです。
    # default=timezone.now は、フィールドのデフォルト値を現在のタイムゾーンの現在の日時に設定することを意味します。

    update_date_time = models.DateTimeField(default=timezone.now)
    # update_date_time フィールドは、アイテムが最後に更新された日時を格納するための日時フィールドです。
    # default=timezone.now は、フィールドのデフォルト値を現在のタイムゾーンの現在の日時に設定することを意味します。

    def publish(self):
        self.save()
    # publish メソッドは、モデルの保存を行います。
    # self.save() は、現在のオブジェクトの状態をデータベースに保存するためのメソッドです。

    def __str__(self):
        return self.item_name
    # __str__ メソッドは、モデルの文字列表現を返します。
    # この場合、item_name フィールドの値が返されます。

    @property
    def is_finished(self):
        if self.finished_date is None:
            return models.BooleanField(default=False)
        else:
            return models.BooleanField(default=True)
    # is_finished メソッドは、アイテムが完了したかどうかを示すブール値を返します。
    # finished_date が None の場合は False を、それ以外の場合は True を返します。

    @property
    def expire(self):
        return self.expire_date < timezone.now()
    # expire メソッドは、アイテムの有効期限が現在の時刻よりも過去であるかどうかを示すブール値を返します。
    # expire_date が現在の時刻よりも前の場合は True を、それ以外の場合は False を返します。