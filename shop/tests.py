from django.test import TestCase
from django.db.models.signals import pre_save
from django.core.files.uploadedfile import SimpleUploadedFile

import re, glob, os

from .models import Good, Category


class GoodAndCategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test category')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif',
        )
        self.good = Good.objects.create(title='Test good', description='This is test good', com_qty=500, sel_qty=500, price=500.00, image=image, category=self.category, cropping='1x1').full_clean()

    def test_create_category(self):
        category = Category.objects.get(title='Test category')
        self.assertEqual(str(category), category.title)

    def test_create_good_and_connection_category(self):
        good = Good.objects.get(title='Test good')

        expected = {
            'title': 'Test good',
            'description': 'This is test good',
            'com_qty': 500,
            'sel_qty': 500,
            'price': 500.00,
            'category': self.category,
        }
        for field, value in expected.items():
            self.assertEqual(getattr(good, field), value)
        
        self.assertIn('test_image', good.image.name)
        self.assertEqual(str(good), good.title)
        
        good_in_category = self.category.good_set.all()
        self.assertIn(good, good_in_category)
        self.assertEqual(good_in_category.count(), 1)

        self.assertTrue(os.path.isfile(good.image.path), msg="Зображення не завантажене")

        url = os.path.splitext(re.sub(r'_[A-Za-z0-9]+(?=\.)', '', good.image.path))[0]
        good.delete()
        for img in glob.glob(url+'*'):
            self.assertFalse(os.path.isfile(img), msg="Файл зображення не видалено автоматично")

