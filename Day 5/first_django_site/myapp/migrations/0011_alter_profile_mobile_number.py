# Generated by Django 5.0 on 2024-01-12 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_profile_mobile_number_alter_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(default='0000', max_length=15),
        ),
    ]
