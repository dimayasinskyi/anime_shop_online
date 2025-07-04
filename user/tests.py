from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from datetime import timedelta
import re, glob, os

from .models import User, Basket, SaveGood, Comment
from shop.models import Categories, Goods

class AuthenticationModelTest(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif',
        )
        self.user = User.objects.create(first_name='Test_first_name', last_name='Test_last_name', username='test_user', email='test_email@gmail.com', password='test_password', gender='other', address='This_is_test_address', address2='This_is_test_address2', city='Test_city', state='Test_state', zip=111111,image=image)
        category = Categories.objects.create(title='Test category')
        self.good = Goods.objects.create(title='Test good', description='This is test good', com_qty=500, sel_qty=500, price=500.00, image=image, category=category, cropping='1x1')
        self.basket = Basket.objects.create(user=self.user, good=self.good, quantity=2)
        self.savegood = SaveGood.objects.create(user=self.user, good=self.good)
        self.comment = Comment.objects.create(user=self.user, good=self.good, text='This_is_test_text')

    def test_create_comment(self):
        comment = Comment.objects.get(user=self.user)
        expected = {
            'user': self.user,
            'good': self.good,
            'text': 'This_is_test_text',
        }
        for field, value in expected.items():
            self.assertEqual(getattr(comment, field), value)
        self.assertIsNotNone(comment.create_time)
        self.assertLessEqual(timezone.now() - comment.create_time, timedelta(seconds=30))
        

    def test_create_savegood(self):
        savegood = SaveGood.objects.get(user=self.user)
        expected = {
            'user': self.user,
            'good': self.good,
        }
        for field, value in expected.items():
            self.assertEqual(getattr(savegood, field), value)
        self.assertEqual(str(savegood), f"User {self.user.username} | goods {self.good.title}")
        self.assertIsNotNone(savegood.created_timestamp)
        self.assertLessEqual(timezone.now() - savegood.created_timestamp, timedelta(seconds=30))


    def test_create_basket(self):
        basket = Basket.objects.get(user=self.user)
        expected = {
        'user': self.user,
        'good': self.good,
        'quantity': 2,
        }
        for field, value in expected.items():
            self.assertEqual(getattr(basket, field), value)
        self.assertEqual(str(basket), "Basket user test_user | Goods Test good")
        self.assertEqual(basket.sum(), self.good.price * expected['quantity'])
        self.assertEqual(basket.add_good(), expected['quantity'] + 1)
        self.assertIsNotNone(basket.created_timestamp)
        self.assertLessEqual(timezone.now() - basket.created_timestamp, timedelta(seconds=30))

    def test_create_user(self):
        user = User.objects.get(username='test_user')

        expected = {
        'first_name': 'Test_first_name',
        'last_name': 'Test_last_name',
        'username': 'test_user',
        'email': 'test_email@gmail.com',
        'password': 'test_password',
        'gender': 'other',
        'address': 'This_is_test_address',
        'address2': 'This_is_test_address2',
        'city': 'Test_city',
        'state': 'Test_state',
        'zip': 111111,
        }
        for field, value in expected.items():
            self.assertEqual(getattr(user, field), value)
        
        self.assertIn('test_image', user.image.name)

        url = os.path.splitext(re.sub(r'_[A-Za-z0-9]+(?=\.)', '', user.image.path))[0]
        user.delete()
        self.good.delete()
        for img in glob.glob(url+'*'):
            self.assertFalse(os.path.isfile(img), msg="Файл зображення не видалено автоматично")