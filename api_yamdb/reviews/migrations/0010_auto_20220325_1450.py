# Generated by Django 2.2.16 on 2022-03-25 11:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20220325_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genretitle',
            name='genre_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Genre'),
        ),
    ]
