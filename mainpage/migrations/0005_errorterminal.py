# Generated by Django 3.2.4 on 2021-06-17 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_rename_lan_terminal_lat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorTerminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cimei', models.CharField(max_length=50, null=True)),
                ('inr', models.CharField(max_length=50, null=True)),
                ('ctid', models.CharField(max_length=50, null=True)),
                ('cmid', models.CharField(max_length=50, null=True)),
                ('cpodr', models.CharField(max_length=50, null=True)),
                ('cadres', models.CharField(max_length=50, null=True)),
                ('cgorod', models.CharField(max_length=50, null=True)),
                ('cobl', models.CharField(max_length=50, null=True)),
                ('craion', models.CharField(max_length=50, null=True)),
                ('ddatan', models.DateField(max_length=50, null=True)),
                ('cname', models.CharField(max_length=70, null=True)),
            ],
        ),
    ]
