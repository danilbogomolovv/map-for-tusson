# Generated by Django 3.2.4 on 2021-09-23 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0039_auto_20210923_1259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='right_components',
            old_name='administrative_area_level_1_political',
            new_name='administrative_area_level_1',
        ),
        migrations.RenameField(
            model_name='right_components',
            old_name='administrative_area_level_2_political',
            new_name='administrative_area_level_2',
        ),
        migrations.RenameField(
            model_name='right_components',
            old_name='country_political',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='right_components',
            old_name='locality_political',
            new_name='locality',
        ),
        migrations.RenameField(
            model_name='right_components',
            old_name='political_sublocality_sublocality_level_1',
            new_name='sublocality_level_1',
        ),
    ]
