# Generated by Django 4.1.3 on 2022-11-28 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0024_alter_group_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(auto_now_add=True),
        ),
    ]
