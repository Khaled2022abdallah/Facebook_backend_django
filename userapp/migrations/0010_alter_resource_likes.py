# Generated by Django 4.1.3 on 2022-11-28 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_alter_resource_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='likes',
            field=models.ManyToManyField(to='userapp.users'),
        ),
    ]
