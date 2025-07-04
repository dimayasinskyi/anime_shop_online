from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
import glob
import re

from .models import Goods


@receiver(pre_delete, sender=Goods)
def delete_img_and_cropping(sender, instance, **kwargs):
    if instance.image and instance.image.path:
        imgs = os.path.splitext(re.sub(r'_[A-Za-z0-9]+(?=\.)', '', instance.image.path))[0]
        for img in glob.glob(imgs+'*'):
            if os.path.isfile(img):
                os.remove(img)