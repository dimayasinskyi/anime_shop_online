from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from image_cropping import ImageRatioField
from cloudinary.uploader import upload

class Category(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Categories"

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
    cloudinary_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        from django.core.files.storage import default_storage

        super().save(*args, **kwargs)

        if self.image and not self.cloudinary_url:
            local_path = self.image.path
            result = upload(local_path)
            self.cloudinary_url = result['secure_url']
            super().save(update_fields=['cloudinary_url'])

    def clean(self):
        if self.sel_qty > self.com_qty:
            raise ValidationError("More sold than in stock.")

    def __str__(self):
        return f"{self.title}"
    