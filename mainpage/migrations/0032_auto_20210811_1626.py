# Generated by Django 3.2.4 on 2021-08-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0031_alter_marker_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='lat',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='marker',
            name='lng',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
