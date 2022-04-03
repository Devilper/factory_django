from django.db import models

from user.models import UserProfile


class Facility(models.Model):#设备
    version = models.CharField(max_length=100, verbose_name="型号")
    facility_name = models.CharField(max_length=100, verbose_name="名称")
    price = models.BigIntegerField(verbose_name="价格")
    buyer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="购买人")
    buy_time = models.DateField(auto_now_add=True, verbose_name="购买时间")
    objects = models.Manager()

    def __str__(self):
        return self.facility_name

    class Meta:
        verbose_name = "设备信息"
        verbose_name_plural = verbose_name


class Repair(models.Model):  # 维修
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name="故障设备")
    baoxiu_staff_name = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="报修人", related_name='aaa', null=True, blank=True)
    baoxiu_staff_tel = models.CharField(max_length=11, null=True, blank=True, verbose_name="联系方式")
    baoxiu_time = models.DateField(auto_now=True, verbose_name="报修时间", null=True, blank=True)
    baoxiu_complementary = models.CharField(max_length=200, verbose_name="报修描述", null=True, blank=True)
    repair_staff_name = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="维修人", related_name='bbb', null=True, blank=True)
    repair_time = models.DateField(auto_now=True, verbose_name="维修时间", null=True, blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-baoxiu_time']
        verbose_name = "维修信息"
        verbose_name_plural = verbose_name
