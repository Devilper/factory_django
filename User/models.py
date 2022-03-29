from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Position(models.Model):
    position = models.CharField(max_length=100)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "职位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.position


class UserProfile(AbstractUser):
    GENDER = (
        ('male', '男'),
        ('female', '女')
    )
    staff_code = models.CharField(verbose_name="员工编号", max_length=32)
    staff_age = models.PositiveIntegerField(verbose_name="年龄")
    staff_home = models.CharField(max_length=100, verbose_name="籍贯")
    staff_gender = models.CharField(choices=GENDER, max_length=6, verbose_name="性别")
    staff_nationality = models.CharField(max_length=20, verbose_name="民族")
    id_card = models.CharField(max_length=20, verbose_name="身份证")
    address = models.CharField(max_length=50, verbose_name="地址", null=True, blank=True)
    salary_pre_hour = models.IntegerField(verbose_name="时薪")

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
