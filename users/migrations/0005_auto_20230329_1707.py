# Generated by Django 3.0.5 on 2023-03-29 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230322_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytitlesuser',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]