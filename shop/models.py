from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from image_cropping import ImageRatioField


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Good(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    com_qty = models.IntegerField()
    sel_qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, upload_to='goods/image/')
    cropping = ImageRatioField('image', '300x300')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def clean(self):
        if self.sel_qty > self.com_qty:
            raise ValidationError("More sold than in stock.")

    def __str__(self):
        return f"{self.title}"
    