# Generated by Django 3.2.4 on 2021-07-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0021_auto_20210630_1529'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Terminal_for_check',
        ),
        migrations.DeleteModel(
            name='TerminalName',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cbank',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cgorod',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cimei',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cmid',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cname',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cobl',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cots',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cparta',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cpodr',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='craion',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='ctid',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='ctype',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cunn',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='cvsoba',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='czona',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='ddatan',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='inr',
        ),
        migrations.RemoveField(
            model_name='errorterminal',
            name='zona_name',
        ),
        migrations.AddField(
            model_name='terminal',
            name='cmemo',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='terminal',
            name='cstatus',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='terminal',
            name='ddatap',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='terminal',
            name='ss_nom',
            field=models.CharField(max_length=150, null=True),
        ),
    ]