# Generated by Django 2.2.16 on 2022-03-19 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220319_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
