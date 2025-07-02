from django.db import models

from shop.models import Goods
from user.models import User

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('failed', 'Failed'),
        ('on_hold', 'On hold'),
    ]
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    goods = models.ManyToManyField(to=Goods)
    status = models.CharField(choices=STATUS_CHOICES, default='new', max_length=20)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip = models.SmallIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
