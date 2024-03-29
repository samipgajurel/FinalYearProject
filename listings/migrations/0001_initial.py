# Generated by Django 3.2.5 on 2023-03-18 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=1000)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('category', models.CharField(max_length=100, null=True)),
                ('sub_category', models.CharField(max_length=100, null=True)),
                ('unit', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField(default=0)),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastModified', models.DateTimeField(default=django.utils.timezone.now)),
                ('views', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'listings',
            },
        ),
    ]
