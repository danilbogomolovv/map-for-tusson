# Generated by Django 3.2.4 on 2021-08-10 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0029_marker'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='count',
            field=models.CharField(max_length=10, null=True),
        ),
    ]