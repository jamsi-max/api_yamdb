# Generated by Django 2.2.16 on 2022-03-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamdbuser',
            name='role',
            field=models.CharField(choices=[('US', 'user'), ('MO', 'moderator'), ('AD', 'admin'), ('SU', 'superuser')], default='user', max_length=16, verbose_name='Роль'),
        ),
    ]