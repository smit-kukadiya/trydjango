# Generated by Django 4.2.4 on 2023-08-21 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='photo',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
