# Generated by Django 2.0.7 on 2018-08-19 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trelloapp', '0011_task_completed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='picture',
            field=models.ImageField(default='default.jpeg', upload_to=''),
        ),
    ]
