# Generated by Django 3.0.5 on 2023-03-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytitlesuser',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin'), ('django_admin', 'Django Admin')], default='user', max_length=15),
        ),
    ]
