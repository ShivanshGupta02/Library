from django.db import models
from django.conf import settings
from . import enums
# Create your models here.


class Membership(models.Model):
    description = models.CharField(max_length=100,null=True)
    membership_type = models.CharField(
        choices = enums.MEMBERSHIP_CHOICES.choices,
        default=enums.MEMBERSHIP_CHOICES.FREE,
        max_length=30
    )
    price = models.IntegerField(default=15)

    def __str__(self):
        return self.membership_type
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price/100)    
    
    
class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL,null=True)
    payment_status = models.CharField(
        max_length = 100,
        choices = enums.PaymentStatus.choices,
        default = enums.PaymentStatus.PENDING,
    )
    def __str__(self):
        return f'{self.user.username} has taken {self.membership.membership_type} membership'
    
