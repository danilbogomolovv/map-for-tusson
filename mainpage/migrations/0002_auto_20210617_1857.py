# Generated by Django 3.2.4 on 2021-06-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='cadres',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='cgorod',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='cimei',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='cmid',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='cname',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='cobl',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='cpodr',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='craion',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='ctid',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='ddatan',
            field=models.DateField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='terminal',
            name='inr',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
