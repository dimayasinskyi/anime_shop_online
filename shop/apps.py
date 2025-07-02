from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        import os
        from django.db.models.signals import post_delete
        from django.dispatch import receiver
        from .models import Goods
        
        @receiver(post_delete, sender=Goods)
        def delete_image_file(sender, instance, **kwargs):
            if instance.image:
                if instance.image.path and os.path.isfile(instance.image.path):
                    os.remove(instance.image.path)
                    os.remove(str(instance.image.path) + ".300x300_q85_detail_upscale.jpg")