from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Listings(models.Model):
    title = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    picture = models.ImageField(upload_to='images/',blank=True,null=True)
    category = models.CharField(max_length=100,null=True)
    sub_category = models.CharField(max_length=100,null=True)
    unit = models.CharField(max_length=100,null=True)
    price = models.FloatField(default=0)
    dateCreated = models.DateTimeField(default=timezone.now)
    lastModified = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    featured = models.IntegerField(default=0)
    class Meta:
        db_table = "listings"