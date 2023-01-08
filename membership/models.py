from django.db import models
from django.conf import settings
# Create your models here.

MEMBERSHIP_CHOICES = (
    ('Pro','p'),
    ('Free','f')
)

class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices = MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30
    )
    price = models.IntegerField(default=15)

    def __str__(self):
        return self.membership_type
    
class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.user.username