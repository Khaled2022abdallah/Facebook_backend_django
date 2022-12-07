# Generated by Django 4.1.3 on 2022-11-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('color', models.CharField(max_length=100)),
                ('pantone_value', models.CharField(max_length=100)),
                ('urlSupport', models.URLField()),
                ('textSupport', models.TextField()),
                ('user_id', models.IntegerField(blank=True, default='1', null=True)),
            ],
        ),
    ]
