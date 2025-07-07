from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    GENDER_CHOICES = [
        ('man', 'Man'),
        ('gril', 'Gril'),
        ('other', 'Other'),
        ('no_info', 'No Info'),
    ]
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default='no info')
    address = models.TextField(null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    good = models.ForeignKey(to='shop.Good', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Basket user { self.user.username } | Goods { self.good.title }"
    
    def sum(self):
        return self.good.price * self.quantity
    
    def add_good(self):
        return self.quantity + 1
    

class SaveGood(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    good = models.OneToOneField(to='shop.Good', on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user.username} | goods {self.good.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    good = models.ForeignKey(to='shop.Good', on_delete=models.CASCADE)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
