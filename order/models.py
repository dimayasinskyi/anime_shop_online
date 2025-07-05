from django.db import models


from user.models import User


class OrderGood(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    good = models.ForeignKey('shop.Good', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def sum(self):
        return self.good.price * self.quantity


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
    goods = models.ManyToManyField(to='shop.Good', through='OrderGood', related_name='order_goods')
    status = models.CharField(choices=STATUS_CHOICES, default='new', max_length=20)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip = models.SmallIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        goods = ', '.join([good.title for good in self.goods.all()])
        return f'User: {self.user.username} | Goods: {goods}'
    
    def total_sum(self):
        return sum(order_good.sum() for order_good in self.ordergood_set.all())
    