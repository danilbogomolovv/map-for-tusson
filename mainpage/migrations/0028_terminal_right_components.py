# Generated by Django 3.2.4 on 2021-08-04 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0027_auto_20210711_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='right_components',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
