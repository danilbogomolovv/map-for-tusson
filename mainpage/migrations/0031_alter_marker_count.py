# Generated by Django 3.2.4 on 2021-08-10 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0030_marker_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]
