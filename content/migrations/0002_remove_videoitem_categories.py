# Generated by Django 5.1.1 on 2024-09-20 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoitem',
            name='categories',
        ),
    ]
