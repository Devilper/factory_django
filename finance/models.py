from django.db import models

# Create your models here.
from user.models import UserProfile


class Salary(models.Model):  # 工资
    current_time = models.DateField(auto_now_add=True, verbose_name="时间")
    staff_name = models.ForeignKey("user.UserProfile", on_delete=models.CASCADE, verbose_name="姓名")
    attend_days = models.FloatField(verbose_name="出勤", default=0)
    leave_days = models.FloatField(verbose_name="请假", default=0)
    absent_days = models.FloatField(verbose_name="旷班", default=0)
    business_days = models.FloatField(verbose_name="出差", default=0)
    zaotui_days = models.FloatField(verbose_name="早退", default=0)
    late_days = models.FloatField(verbose_name="迟到", default=0)
    overtime = models.FloatField(verbose_name="加班时长", default=0)
    base_salary = models.FloatField(verbose_name="基础工资", default=0)
    overtime_salary = models.FloatField(verbose_name="加班工资", default=0)
    kouchu = models.FloatField(verbose_name="应扣", default=0)
    allowance = models.FloatField(verbose_name="补贴", default=0)
    should_pay = models.FloatField(verbose_name="应发", default=0)
    tax = models.FloatField(verbose_name="个人所得税", default=0)
    actual_pay = models.FloatField(verbose_name="实发", default=0)
    objects = models.Manager()

    class Meta:
        ordering = ['-current_time']
        verbose_name = "工资信息"
        verbose_name_plural = verbose_name


class Attendance(models.Model):  # 考勤
    current_time = models.DateField(verbose_name="日期")
    staff_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="姓名")
    flag_leave = models.BooleanField(default=False, verbose_name="请假")
    flag_business = models.BooleanField(default=False, verbose_name="出差")
    start_time = models.DateTimeField(verbose_name="上班时间")
    end_time = models.DateTimeField(verbose_name="下班时间")
    supplement = models.CharField(max_length=100, verbose_name="补充", null=True, default='无', blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-current_time']
        unique_together = ('current_time', 'staff_name')
