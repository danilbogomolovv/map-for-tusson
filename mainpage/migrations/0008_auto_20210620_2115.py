# Generated by Django 3.2.4 on 2021-06-20 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0007_terminalname'),
    ]

    operations = [
        migrations.AddField(
            model_name='errorterminal',
            name='cots',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='errorterminal',
            name='cparta',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='existterminal',
            name='cots',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='existterminal',
            name='cparta',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='terminal',
            name='cots',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='terminal',
            name='cparta',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
