# Generated by Django 4.1.3 on 2022-11-28 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0013_remove_likescomments_user_likescomments_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likescomments',
            name='resource',
        ),
        migrations.AddField(
            model_name='likescomments',
            name='resource',
            field=models.ManyToManyField(to='userapp.resource'),
        ),
    ]
