# Generated by Django 3.0.5 on 2023-03-31 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0009_auto_20230330_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': (('can_undelete', 'Can undelete this object'),)},
        ),
        migrations.AddField(
            model_name='category',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True),
        ),
    ]
