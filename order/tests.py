from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from datetime import timedelta

from .models import Order, OrderGood
from shop.models import Goods, Categories
from user.models import User

class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(title='Test category')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif',
        )
        self.good = Goods.objects.create(title='Test good', description='This is test good', com_qty=500, sel_qty=500, price=500.00, image=image, category=self.category, cropping='1x1')
        self.user = User.objects.create(first_name='Test_first_name', last_name='Test_last_name', username='test_user', email='test_email@gmail.com', password='test_password', gender='other', address='This_is_test_address', address2='This_is_test_address2', city='Test_city', state='Test_state', zip=111111)
        self.order = Order.objects.create(user=self.user,address='Test_address', city='Test_city', state='Test_state', zip=111111)
        self.ordergood = OrderGood.objects.create(order=self.order, good=self.good, quantity=2)


    def test_create_ordergood(self):
        order_good = OrderGood.objects.get(order=self.order)
        expected = {
            "order": self.order,
            "good": self.good,
            "quantity": 2
        }
        for field, value in expected.items():
            self.assertEqual(getattr(order_good, field), value)
            

    def test_create_order(self):
        order = Order.objects.get(user=self.user)
        expected = {
            'user': self.user,
            'address': 'Test_address',
            'city': 'Test_city',
            'state': 'Test_state',
            'zip': 111111,
        }
        for field, value in expected.items():
            self.assertEqual(getattr(order, field), value)
        self.assertLessEqual(timezone.now() - order.create_time, timedelta(seconds=30))

        Goods.objects.get(title='Test good').delete()
