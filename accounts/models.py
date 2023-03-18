from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Profile(models.Model):
    CONSUMER = "consumer"
    DEALER = "dealer"
    FARMER = "farmer"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150,blank=False,unique=True)
    phone = PhoneNumberField(blank=True)
    role = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    if not instance.is_superuser:
        instance.profile.save()