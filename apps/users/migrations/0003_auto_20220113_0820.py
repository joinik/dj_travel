# Generated by Django 2.2.5 on 2022-01-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220113_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=0, verbose_name='年龄'),
        ),
    ]
