# Generated by Django 2.0.7 on 2018-08-19 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trelloapp', '0014_auto_20180819_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=models.FileField(default='default.jpeg', upload_to=''),
        ),
    ]