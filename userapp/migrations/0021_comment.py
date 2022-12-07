# Generated by Django 4.1.3 on 2022-11-28 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0020_alter_resource_comments_alter_resource_countlikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('resource', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userapp.resource')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userapp.users')),
            ],
        ),
    ]
