# Generated by Django 3.2.4 on 2021-09-23 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0038_alter_terminal_right_components'),
    ]

    operations = [
        migrations.CreateModel(
            name='Right_components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_number', models.CharField(max_length=400, null=True)),
                ('route', models.CharField(max_length=400, null=True)),
                ('political_sublocality_sublocality_level_1', models.CharField(max_length=400, null=True)),
                ('locality_political', models.CharField(max_length=400, null=True)),
                ('administrative_area_level_2_political', models.CharField(max_length=400, null=True)),
                ('administrative_area_level_1_political', models.CharField(max_length=400, null=True)),
                ('country_political', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='terminal',
            name='right_components',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainpage.right_components'),
        ),
    ]
