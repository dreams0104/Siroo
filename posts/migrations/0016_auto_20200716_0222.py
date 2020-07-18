# Generated by Django 3.0.8 on 2020-07-15 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20200716_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='taginpost',
        ),
        migrations.AddField(
            model_name='post',
            name='taginpost',
            field=models.ManyToManyField(related_name='taged_post', to='posts.Tag'),
        ),
    ]