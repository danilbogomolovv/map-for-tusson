# Generated by Django 3.2.4 on 2021-09-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0040_auto_20210923_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='right_components',
            field=models.CharField(max_length=800, null=True),
        ),
        migrations.DeleteModel(
            name='Right_components',
        ),
    ]
