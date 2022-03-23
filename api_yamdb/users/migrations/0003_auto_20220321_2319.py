# Generated by Django 2.2.16 on 2022-03-21 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220319_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamdbuser',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'), ('superuser', 'superuser')], default='user', max_length=16, verbose_name='Роль'),
        ),
    ]
