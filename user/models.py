from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings #장고가 관리하는 setting

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = 'my_user'

    bio = models.CharField(max_length=256, default='')
    #many to many model 생성 follow followee 관계 잘 파악하기
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followee")


# class UserModel(models.Model):
#     class Meta:
#         db_table = 'my_user'
#     # username = models.CharField(max_length=20, null=False)
#     # password = models.CharField(max_length=256, null=False)
#     bio = models.CharField(max_length=256, default='')
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # updated_at = models.DateTimeField(auto_now=True)