# Generated by Django 2.0.7 on 2018-08-19 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trelloapp', '0012_project_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=models.FileField(default='default.jpeg', upload_to=''),
        ),
    ]
