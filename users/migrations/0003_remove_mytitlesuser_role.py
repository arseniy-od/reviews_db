# Generated by Django 3.0.5 on 2023-03-22 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230322_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mytitlesuser',
            name='role',
        ),
    ]