from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
import re
import glob
from .models import User


@receiver(pre_delete, sender=User)
def delete_img(sender, instance, **kwargs):
    if instance.image and instance.image.path:
        imgs = os.path.splitext(re.sub(r'_[A-Za-z0-9]+(?=\.)', '', instance.image.path))[0]
        for img in glob.glob(imgs+'*'):
            if os.path.isfile(img):
                os.remove(img)