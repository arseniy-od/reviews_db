# Generated by Django 3.0.5 on 2023-03-29 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_comment_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.DateField(blank=True, null=True),
        ),
    ]
