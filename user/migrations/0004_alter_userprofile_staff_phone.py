# Generated by Django 3.2.12 on 2022-04-16 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220415_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='staff_phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='员工手机号'),
        ),
    ]