# Generated by Django 5.1.1 on 2024-09-20 15:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_remove_videoitem_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoitem',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
    ]
