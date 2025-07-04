from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from tastypie.bundle import Bundle

from shop.models import Categories, Goods
from .models import GoodsResource

class GoodResourceTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(title='Test category')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif',
        )
        self.good = Goods.objects.create(title='Test good', description='This is test good', com_qty=500, sel_qty=500, price=500.00, image=image, category=self.category, cropping='1x1')
        self.resource = GoodsResource()

    def test_dehydrate_title_returns_uppercase(self):
        bundle = Bundle(obj=self.good, data={'title': self.good.title})
        result = self.resource.dehydrate_title(bundle)
        self.assertEqual(result, self.good.title.upper())