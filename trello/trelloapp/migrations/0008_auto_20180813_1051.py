# Generated by Django 2.0.7 on 2018-08-13 10:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trelloapp', '0007_auto_20180813_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='userid',
        ),
        migrations.AddField(
            model_name='project',
            name='userid',
            field=models.ManyToManyField(related_name='projectmember', to=settings.AUTH_USER_MODEL),
        ),
    ]