# Generated by Django 3.0.5 on 2023-03-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0005_auto_20230329_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
