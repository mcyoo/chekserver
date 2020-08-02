from django.db import models

# Create your models here.
# 다른 앱에 모든 클래스 에 상속하기 위한 부모 클래스  다른 모델은 이필드가 내장되어있다.


class TimeStampedModel(models.Model):
    """ Time Stamped Model """

    # 객체가 언제 생성됬고, 언제 수정됬는지 확인 가능
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
