# Generated by Django 3.2.5 on 2023-04-16 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='featured',
            field=models.IntegerField(default=0),
        ),
    ]