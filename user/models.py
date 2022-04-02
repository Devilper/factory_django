from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Position(models.Model):
    position = models.CharField(max_length=100)
    objects = models.Manager()
    class Meta:
        verbose_name = "职位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.position


class UserProfile(models.Model):
    GENDER = (
        ('male', '男'),
        ('female', '女')
    )
    password = models.CharField(verbose_name="密码", max_length=128)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(verbose_name="是否有效", default=True)
    staff_code = models.CharField(verbose_name="员工编号", max_length=32, unique=True)
    staff_phone = models.CharField(verbose_name="员工手机号", max_length=11)
    staff_age = models.PositiveIntegerField(verbose_name="年龄")
    staff_home = models.CharField(max_length=100, verbose_name="籍贯")
    staff_gender = models.CharField(choices=GENDER, max_length=6, verbose_name="性别")
    staff_nationality = models.CharField(max_length=20, verbose_name="民族")
    id_card = models.CharField(max_length=20, verbose_name="身份证", unique=True)
    address = models.CharField(max_length=50, verbose_name="地址", null=True, blank=True)
    salary_pre_hour = models.IntegerField(verbose_name="时薪")
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    position = models.ForeignKey("Position", on_delete=models.CASCADE, related_name="+")

    objects = models.Manager()

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

