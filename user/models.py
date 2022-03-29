from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone


class Position(models.Model):
    position = models.CharField(max_length=100)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="+")

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
    username_validator = UnicodeUsernameValidator()

    password = models.CharField(verbose_name="密码", max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(verbose_name="是否有效", default=True)
    staff_code = models.CharField(verbose_name="员工编号", max_length=32)
    staff_age = models.PositiveIntegerField(verbose_name="年龄")
    staff_home = models.CharField(max_length=100, verbose_name="籍贯")
    staff_gender = models.CharField(choices=GENDER, max_length=6, verbose_name="性别")
    staff_nationality = models.CharField(max_length=20, verbose_name="民族")
    id_card = models.CharField(max_length=20, verbose_name="身份证")
    address = models.CharField(max_length=50, verbose_name="地址", null=True, blank=True)
    salary_pre_hour = models.IntegerField(verbose_name="时薪")
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    _password = None

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)


