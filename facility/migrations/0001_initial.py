# Generated by Django 3.2.12 on 2022-04-23 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100, verbose_name='型号')),
                ('facility_name', models.CharField(max_length=100, verbose_name='名称')),
                ('price', models.BigIntegerField(verbose_name='价格')),
                ('buy_time', models.DateField(auto_now_add=True, verbose_name='购买时间')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.userprofile', verbose_name='购买人')),
            ],
            options={
                'verbose_name': '设备信息',
                'verbose_name_plural': '设备信息',
            },
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baoxiu_staff_tel', models.CharField(blank=True, max_length=11, null=True, verbose_name='联系方式')),
                ('baoxiu_time', models.DateField(auto_now=True, null=True, verbose_name='报修时间')),
                ('baoxiu_complementary', models.CharField(blank=True, max_length=200, null=True, verbose_name='报修描述')),
                ('repair_time', models.DateField(auto_now=True, null=True, verbose_name='维修时间')),
                ('baoxiu_staff_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='aaa', to='user.userprofile', verbose_name='报修人')),
                ('facility_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.facility', verbose_name='故障设备')),
                ('repair_staff_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bbb', to='user.userprofile', verbose_name='维修人')),
            ],
            options={
                'verbose_name': '维修信息',
                'verbose_name_plural': '维修信息',
                'ordering': ['-baoxiu_time'],
            },
        ),
    ]
