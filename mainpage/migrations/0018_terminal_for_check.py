# Generated by Django 3.2.4 on 2021-06-29 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0017_auto_20210629_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terminal_for_check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ss_nom', models.CharField(max_length=150, null=True)),
                ('right_adres', models.CharField(max_length=150, null=True)),
                ('right_city_distrcit', models.CharField(max_length=150, null=True)),
                ('right_district', models.CharField(max_length=150, null=True)),
                ('right_area', models.CharField(max_length=150, null=True)),
            ],
        ),
    ]
