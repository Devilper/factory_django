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
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_time', models.DateField(auto_now_add=True, verbose_name='时间')),
                ('attend_days', models.FloatField(default=0, verbose_name='出勤')),
                ('leave_days', models.FloatField(default=0, verbose_name='请假')),
                ('absent_days', models.FloatField(default=0, verbose_name='旷班')),
                ('business_days', models.FloatField(default=0, verbose_name='出差')),
                ('zaotui_days', models.FloatField(default=0, verbose_name='早退')),
                ('late_days', models.FloatField(default=0, verbose_name='迟到')),
                ('overtime', models.FloatField(default=0, verbose_name='加班时长')),
                ('base_salary', models.FloatField(default=0, verbose_name='基础工资')),
                ('overtime_salary', models.FloatField(default=0, verbose_name='加班工资')),
                ('kouchu', models.FloatField(default=0, verbose_name='应扣')),
                ('allowance', models.FloatField(default=0, verbose_name='补贴')),
                ('should_pay', models.FloatField(default=0, verbose_name='应发')),
                ('tax', models.FloatField(default=0, verbose_name='个人所得税')),
                ('actual_pay', models.FloatField(default=0, verbose_name='实发')),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='姓名')),
            ],
            options={
                'verbose_name': '工资信息',
                'verbose_name_plural': '工资信息',
                'ordering': ['-current_time'],
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_time', models.DateField(verbose_name='日期')),
                ('flag_leave', models.BooleanField(default=False, verbose_name='请假')),
                ('flag_business', models.BooleanField(default=False, verbose_name='出差')),
                ('start_time', models.DateTimeField(verbose_name='上班时间')),
                ('end_time', models.DateTimeField(verbose_name='下班时间')),
                ('supplement', models.CharField(blank=True, default='无', max_length=100, null=True, verbose_name='补充')),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='姓名')),
            ],
            options={
                'ordering': ['-current_time'],
                'unique_together': {('current_time', 'staff_name')},
            },
        ),
    ]
