from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单名称', max_length=32, unique=True)
    icon = models.CharField(max_length=128, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "菜单信息"
        verbose_name_plural = verbose_name


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='权限标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    action = models.ForeignKey(verbose_name='操作', to='Action', null=True, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey(verbose_name='父权限', to='self',
                               null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'parent__isnull':True})
    menu = models.ForeignKey(verbose_name='菜单', to='Menu', null=True, blank=True, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "权限信息"
        verbose_name_plural = verbose_name


class Action(models.Model):
    """
    操作：增删改查
    """
    title = models.CharField(verbose_name='操作标题', max_length=32)
    code = models.CharField(verbose_name='方法', max_length=32)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "操作信息"
        verbose_name_plural = verbose_name


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    desc = models.CharField(verbose_name='角色描述', max_length=64, null=True, blank=True)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', blank=True, to='Permission')
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "角色信息"
        verbose_name_plural = verbose_name


class UserProfile(models.Model):
    GENDER = (
        ('male', '男'),
        ('female', '女')
    )
    password = models.CharField(verbose_name="密码", max_length=128)
    last_login = models.DateField(blank=True, null=True, auto_now=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(verbose_name="是否有效", default=True)
    staff_code = models.CharField(verbose_name="员工编号", max_length=32, unique=True)
    staff_phone = models.CharField(verbose_name="员工手机号", max_length=11, unique=True)
    staff_age = models.PositiveIntegerField(verbose_name="年龄", null=True)
    staff_home = models.CharField(max_length=100, verbose_name="籍贯", null=True)
    staff_gender = models.CharField(choices=GENDER, max_length=6, verbose_name="性别")
    staff_nationality = models.CharField(max_length=20, verbose_name="民族", null=True)
    id_card = models.CharField(max_length=20, verbose_name="身份证", unique=True)
    address = models.CharField(max_length=50, verbose_name="地址", null=True, blank=True)
    salary_pre_hour = models.IntegerField(verbose_name="时薪")
    date_joined = models.DateField(_('date joined'), default=timezone.now)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, related_name="roles", blank=True)

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

